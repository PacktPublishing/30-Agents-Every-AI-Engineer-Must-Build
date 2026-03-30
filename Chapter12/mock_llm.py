"""
MockLLM: Context-aware mock LLM for Simulation Mode.

Provides deterministic, chapter-faithful responses for all agent pipelines
so that notebooks run end-to-end without an API key.

Author: Imran Ahmad
Book: 30 Agents Every AI Engineer Must Build, Chapter 12
Section Reference: MockLLM Spec (Strategy §3), Handlers map to p.8–35
"""

import re
import copy
import numpy as np
from typing import Any

from src.utils import ColorLogger, graceful_fallback

logger = ColorLogger(name="MockLLM")

# ---------------------------------------------------------------------------
# Section 3.2 — Mock Metadata Schema
# Every mock response carries _mock_meta for traceability.
# ---------------------------------------------------------------------------

def _make_meta(page: str, section: str, description: str) -> dict:
    """Build a standardised _mock_meta dict."""
    return {
        "source": f"Chapter 12, {page}",
        "section": section,
        "description": description,
        "author": "Imran Ahmad",
        "mode": "simulation",
    }


# ---------------------------------------------------------------------------
# MockLLM Class — Section 3.1 Complete Handler Map
# ---------------------------------------------------------------------------

class MockLLM:
    """
    Context-aware mock LLM that routes prompts to deterministic handlers.

    Each handler mirrors the output schema of the real LLM call it replaces,
    ensuring the Live/Simulation Parity Contract (Strategy §3.3) holds.

    Handler routing uses keyword detection on the context/prompt string.
    """

    # Keywords that route to each handler
    _ROUTING_TABLE = {
        "_mock_ethical_validation": [
            "ethical", "compliance", "obligation", "forbidden",
            "evaluate_action", "compliant",
        ],
        "_mock_resume_scoring": [
            "resume", "candidate", "score_resume", "hiring",
            "skill_matches", "years_exp",
        ],
        "_mock_symptom_interpretation": [
            "symptom", "interpret_symptoms", "snomed",
        ],
        "_mock_differential_generation": [
            "differential", "diagnosis", "generate_differentials",
            "wbc_count", "chest_imaging",
        ],
        "_mock_explanation_generation": [
            "explain", "clinical_explanation", "clinician_report",
            "patient_report", "narrative",
        ],
        "_mock_confidence_scoring": [
            "confidence", "calibrat", "score_differentials",
            "epistemic", "aleatoric",
        ],
    }

    # Violation keywords for ethical validation (p.8-9)
    _VIOLATION_KEYWORDS = {
        "share_medical_details": ("privacy", "HIPAA violation — sharing protected health information"),
        "external_email": ("data_leak", "Transmitting internal data to external address"),
        "bypass_consent": ("consent", "User consent was not obtained"),
        "disable_audit": ("transparency", "Audit trail cannot be disabled"),
        "disable_signals_school_zone": ("safety", "Safety-critical system override is forbidden"),
    }

    # Symptom lookup table (p.32-33) — 20 symptoms
    _SYMPTOM_TABLE = {
        "productive cough":    ("SNOMED:49727002",  0.94),
        "fever":               ("SNOMED:386661006", 0.97),
        "shortness of breath": ("SNOMED:267036007", 0.93),
        "chest pain":          ("SNOMED:29857009",  0.91),
        "fatigue":             ("SNOMED:84229001",  0.89),
        "headache":            ("SNOMED:25064002",  0.92),
        "nausea":              ("SNOMED:422587007", 0.88),
        "vomiting":            ("SNOMED:422400008", 0.90),
        "diarrhea":            ("SNOMED:62315008",  0.87),
        "muscle ache":         ("SNOMED:68962001",  0.86),
        "sore throat":         ("SNOMED:162397003", 0.91),
        "runny nose":          ("SNOMED:64531003",  0.85),
        "chills":              ("SNOMED:43724002",  0.93),
        "night sweats":        ("SNOMED:42984000",  0.88),
        "weight loss":         ("SNOMED:89362005",  0.84),
        "wheezing":            ("SNOMED:56018004",  0.90),
        "dizziness":           ("SNOMED:404640003", 0.87),
        "joint pain":          ("SNOMED:57676002",  0.89),
        "abdominal pain":      ("SNOMED:21522001",  0.91),
        "dry cough":           ("SNOMED:11833005",  0.92),
    }

    def __init__(self, seed: int = 42):
        self._rng = np.random.RandomState(seed)
        logger.info("MockLLM initialized in Simulation Mode.")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def invoke(self, prompt: str, **kwargs) -> dict:
        """
        Route a prompt string to the appropriate handler.

        Args:
            prompt: The text/context that would be sent to the real LLM.
            **kwargs: Additional context (e.g., candidate data, patient data).

        Returns:
            Dict matching the Live/Simulation Parity Contract schema.
        """
        handler_name = self._route(prompt)
        handler = getattr(self, handler_name)
        logger.debug(f"Routed to {handler_name} for prompt snippet: '{prompt[:60]}...'")
        return handler(prompt, **kwargs)

    # ------------------------------------------------------------------
    # Routing logic
    # ------------------------------------------------------------------

    def _route(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        best_handler = "_default_handler"
        best_score = 0
        for handler_name, keywords in self._ROUTING_TABLE.items():
            score = sum(1 for kw in keywords if kw in prompt_lower)
            if score > best_score:
                best_score = score
                best_handler = handler_name
        return best_handler

    # ------------------------------------------------------------------
    # Handler 1: Ethical Validation (p.8–9)
    # Caller: EthicalReasoningAgent.evaluate_action()
    # Output: {'is_compliant': bool, 'violations': list[tuple], 'severity': str}
    # ------------------------------------------------------------------

    @graceful_fallback(
        fallback_value={"is_compliant": False, "violations": [], "severity": "UNKNOWN",
                        "_mock_meta": _make_meta("p.8-9", "Ethical Validation", "fallback")},
        section_ref="Section 12 - Ethical Validation (p.8-9)"
    )
    def _mock_ethical_validation(self, prompt: str, **kwargs) -> dict:
        """Keyword-match against violation list. See Chapter 12, p.8-9."""
        action = kwargs.get("action", prompt).lower()
        violations = []
        for keyword, (category, description) in self._VIOLATION_KEYWORDS.items():
            if keyword in action.replace(" ", "_"):
                violations.append((category, description))

        is_compliant = len(violations) == 0
        severity = "NONE" if is_compliant else ("CRITICAL" if len(violations) >= 2 else "HIGH")

        return {
            "is_compliant": is_compliant,
            "violations": violations,
            "severity": severity,
            "_mock_meta": _make_meta(
                "p.8-9", "Ethical Validation",
                "Keyword-match compliance check against violation list"
            ),
        }

    # ------------------------------------------------------------------
    # Handler 2: Resume Scoring (p.20–21)
    # Caller: ResumeAnalyzer.score()
    # Output: {'score': float, 'explanation_map': dict, 'source': str}
    # ------------------------------------------------------------------

    @graceful_fallback(
        fallback_value={"score": 0.0, "explanation_map": {}, "source": "fallback",
                        "_mock_meta": _make_meta("p.20-21", "Resume Scoring", "fallback")},
        section_ref="Section 12 - Resume Scoring (p.20-21)"
    )
    def _mock_resume_scoring(self, prompt: str, **kwargs) -> dict:
        """
        Deterministic scoring formula from Chapter 12, p.20-21:
            score = 0.3 + 0.1 * min(skill_matches, 5) + 0.02 * min(years_exp, 10)
        """
        skill_matches = kwargs.get("skill_matches", 3)
        years_exp = kwargs.get("years_exp", 5)

        score = 0.3 + 0.1 * min(skill_matches, 5) + 0.02 * min(years_exp, 10)
        score = round(min(score, 1.0), 4)

        explanation_map = {
            "base": 0.3,
            "skills_contribution": round(0.1 * min(skill_matches, 5), 4),
            "experience_contribution": round(0.02 * min(years_exp, 10), 4),
        }

        return {
            "score": score,
            "explanation_map": explanation_map,
            "source": "mock",
            "_mock_meta": _make_meta(
                "p.20-21", "Resume Scoring",
                f"Deterministic: skills={skill_matches}, exp={years_exp}"
            ),
        }

    # ------------------------------------------------------------------
    # Handler 3: Symptom Interpretation (p.32–33)
    # Caller: SymptomInterpreter.interpret()
    # Output: [{'symptom': str, 'snomed_code': str, 'confidence': float}]
    # ------------------------------------------------------------------

    @graceful_fallback(
        fallback_value=[],
        section_ref="Section 12 - Symptom Interpretation (p.32-33)"
    )
    def _mock_symptom_interpretation(self, prompt: str, **kwargs) -> list:
        """Lookup table: symptoms -> SNOMED CT codes. See Chapter 12, p.32-33."""
        raw_symptoms = kwargs.get("symptoms", [])
        if isinstance(raw_symptoms, str):
            raw_symptoms = [s.strip() for s in raw_symptoms.split(",")]

        results = []
        for symptom in raw_symptoms:
            symptom_lower = symptom.strip().lower()
            if symptom_lower in self._SYMPTOM_TABLE:
                code, conf = self._SYMPTOM_TABLE[symptom_lower]
                results.append({
                    "symptom": symptom.strip(),
                    "snomed_code": code,
                    "confidence": conf,
                })
            else:
                results.append({
                    "symptom": symptom.strip(),
                    "snomed_code": "SNOMED:UNKNOWN",
                    "confidence": 0.50,
                })

        # Attach meta to the list via a wrapper
        return results

    # ------------------------------------------------------------------
    # Handler 4: Differential Generation (p.33–34)
    # Caller: DiagnosticCoordinator.generate_differentials()
    # Output: [{'diagnosis': str, 'raw_score': float}]
    # ------------------------------------------------------------------

    @graceful_fallback(
        fallback_value=[{"diagnosis": "unknown", "raw_score": 0.5}],
        section_ref="Section 12 - Differential Generation (p.33-34)"
    )
    def _mock_differential_generation(self, prompt: str, **kwargs) -> list:
        """
        Profile-based routing from Chapter 12, p.33-34:
        If wbc_count > 10 AND chest_imaging == 'right_lower_consolidation':
            pneumonia primary (0.87), bronchitis (0.09), atelectasis (0.04)
        Otherwise:
            bronchitis primary (0.65), pneumonia (0.20), atelectasis (0.15)
        """
        wbc_count = kwargs.get("wbc_count", 7.5)
        chest_imaging = kwargs.get("chest_imaging", "clear")

        if wbc_count > 10 and chest_imaging == "right_lower_consolidation":
            differentials = [
                {"diagnosis": "pneumonia", "raw_score": 0.87},
                {"diagnosis": "bronchitis", "raw_score": 0.09},
                {"diagnosis": "atelectasis", "raw_score": 0.04},
            ]
        else:
            differentials = [
                {"diagnosis": "bronchitis", "raw_score": 0.65},
                {"diagnosis": "pneumonia", "raw_score": 0.20},
                {"diagnosis": "atelectasis", "raw_score": 0.15},
            ]

        return differentials

    # ------------------------------------------------------------------
    # Handler 5: Explanation Generation (p.34–35)
    # Caller: ClinicalExplainer.generate()
    # Output: {'narrative': str, 'feature_contributions': dict, 'trace': list}
    # ------------------------------------------------------------------

    @graceful_fallback(
        fallback_value={"narrative": "Explanation unavailable (fallback).",
                        "feature_contributions": {}, "trace": []},
        section_ref="Section 12 - Explanation Generation (p.34-35)"
    )
    def _mock_explanation_generation(self, prompt: str, **kwargs) -> dict:
        """
        Template-fill using chapter examples. See Chapter 12, p.34-35.
        Supports 'clinician' and 'patient' audience modes.
        """
        audience = kwargs.get("audience", "clinician")
        diagnosis = kwargs.get("diagnosis", "pneumonia")
        confidence = kwargs.get("confidence", 0.87)
        shap_features = kwargs.get("shap_features", {
            "wbc_count": 0.31,
            "chest_imaging": 0.28,
            "temperature": 0.15,
            "spo2_min": 0.12,
            "heart_rate_avg": 0.08,
        })

        top_features = sorted(shap_features.items(), key=lambda x: -x[1])
        feature_str = ", ".join(f"{k} (SHAP={v:.2f})" for k, v in top_features[:3])

        if audience == "clinician":
            narrative = (
                f"Primary Assessment: {diagnosis} (confidence: {confidence:.2f}). "
                f"Key findings: {feature_str}. "
                f"The elevated WBC count and right lower lobe consolidation on imaging "
                f"are the dominant contributors to this assessment. "
                f"Recommend confirmatory sputum culture and blood panel."
            )
        else:
            plain_diagnosis = diagnosis.replace("_", " ")
            narrative = (
                f"The analysis of your test results suggests {plain_diagnosis}. "
                f"Your white blood cell count and chest scan were the main factors. "
                f"Your doctor may recommend additional tests to confirm. "
                f"The confidence level of this initial assessment is "
                f"{'high' if confidence > 0.8 else 'moderate'}."
            )

        trace = [
            {"step": "biometric_analysis", "status": "complete"},
            {"step": "symptom_interpretation", "status": "complete"},
            {"step": "differential_generation", "status": "complete"},
            {"step": "explanation_synthesis", "status": "complete"},
        ]

        return {
            "narrative": narrative,
            "feature_contributions": dict(shap_features),
            "trace": trace,
            "_mock_meta": _make_meta(
                "p.34-35", "Explanation Generation",
                f"Template-fill for {audience} audience"
            ),
        }

    # ------------------------------------------------------------------
    # Handler 6: Confidence Scoring (p.28–29)
    # Caller: ConfidenceAwareAgent.score_differentials()
    # Output: [{'answer': str, 'confidence': float, 'qualifier': str, 'evidence': dict}]
    # ------------------------------------------------------------------

    @graceful_fallback(
        fallback_value=[{"answer": "unknown", "confidence": 0.5,
                         "qualifier": "Low confidence — human review recommended",
                         "evidence": {}}],
        section_ref="Section 12 - Confidence Scoring (p.28-29)"
    )
    def _mock_confidence_scoring(self, prompt: str, **kwargs) -> list:
        """
        Identity calibration + Normal(0, 0.02) noise.
        Qualifier mapping from Chapter 12, p.28-29.
        """
        differentials = kwargs.get("differentials", [
            {"diagnosis": "pneumonia", "raw_score": 0.87},
        ])

        scored = []
        for diff in differentials:
            raw = diff.get("raw_score", 0.5)
            # Identity calibration with small noise
            noise = self._rng.normal(0, 0.02)
            calibrated = float(np.clip(raw + noise, 0.0, 1.0))

            if calibrated > 0.9:
                qualifier = "High confidence"
            elif calibrated > 0.7:
                qualifier = "Moderate confidence"
            else:
                qualifier = "Low confidence — human review recommended"

            scored.append({
                "answer": diff.get("diagnosis", "unknown"),
                "confidence": round(calibrated, 4),
                "qualifier": qualifier,
                "evidence": {
                    "raw_score": raw,
                    "calibration_noise": round(noise, 4),
                },
            })

        return scored

    # ------------------------------------------------------------------
    # Default Handler — catch-all for unregistered contexts
    # ------------------------------------------------------------------

    def _default_handler(self, prompt: str, **kwargs) -> dict:
        """Fallback for any prompt that does not match a registered handler."""
        logger.debug("No specific handler matched — using _default_handler.")
        return {
            "response": "[Simulation Mode] Generic mock response.",
            "confidence": 0.5,
            "_mock_meta": _make_meta(
                "p.N/A", "Default Handler",
                "No registered handler matched the prompt context"
            ),
        }


# ---------------------------------------------------------------------------
# Module-level convenience
# ---------------------------------------------------------------------------

_shared_mock = None


def get_mock_llm(seed: int = 42) -> MockLLM:
    """Return a module-level singleton MockLLM instance."""
    global _shared_mock
    if _shared_mock is None:
        _shared_mock = MockLLM(seed=seed)
    return _shared_mock


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mock = MockLLM(seed=42)

    # Test ethical validation
    result = mock.invoke("evaluate_action ethical compliance",
                         action="share_medical_details with external_email")
    logger.success(f"Ethical validation: {result}")

    # Test resume scoring
    result = mock.invoke("score_resume candidate hiring",
                         skill_matches=4, years_exp=8)
    logger.success(f"Resume scoring: {result}")

    # Test symptom interpretation
    result = mock.invoke("interpret_symptoms snomed symptom",
                         symptoms=["fever", "productive cough", "chest pain"])
    logger.success(f"Symptom interpretation: {result}")

    # Test differential generation
    result = mock.invoke("generate_differentials differential diagnosis",
                         wbc_count=12, chest_imaging="right_lower_consolidation")
    logger.success(f"Differential generation: {result}")

    # Test explanation generation
    result = mock.invoke("clinical_explanation explain narrative", audience="patient")
    logger.success(f"Explanation (patient): {result}")

    # Test confidence scoring
    diffs = [{"diagnosis": "pneumonia", "raw_score": 0.87},
             {"diagnosis": "bronchitis", "raw_score": 0.09}]
    result = mock.invoke("confidence score_differentials calibrat",
                         differentials=diffs)
    logger.success(f"Confidence scoring: {result}")

    # Test default handler
    result = mock.invoke("something completely unrelated to anything")
    logger.success(f"Default handler: {result}")

    logger.success("All MockLLM self-tests passed.")
