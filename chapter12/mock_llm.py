# src/mock_llm.py
# Author: Imran Ahmad
# Book: 30 Agents Every AI Engineer Must Build, Chapter 12
# Ref: Strategy §3.1 (MockLLM Handler Map), §3.2 (Mock Metadata Schema)
# Description: Context-aware MockLLM with response handlers mapped to chapter
#              sections. Enables full Simulation Mode without an API key.

import random
import copy
from datetime import datetime
from typing import Any

from src.utils import ColorLogger, graceful_fallback

logger = ColorLogger("MockLLM")


# ---------------------------------------------------------------------------
# Mock Metadata Helper
# Ref: Strategy §3.2 — every mock response includes _mock_meta
# ---------------------------------------------------------------------------

def _make_meta(page: str, section: str, description: str) -> dict:
    """Build the standard _mock_meta dict attached to every mock response."""
    return {
        "source": f"Chapter 12, {page}",
        "section": section,
        "description": description,
        "author": "Imran Ahmad",
        "mode": "simulation",
    }


# ---------------------------------------------------------------------------
# MockLLM — Central Simulation Engine
# ---------------------------------------------------------------------------

class MockLLM:
    """
    Context-aware mock LLM that routes requests to chapter-derived handlers.

    Every handler returns structurally valid output with a ``_mock_meta``
    dict (stripped before notebook display). The output schema of each
    handler is identical to its live-mode counterpart, ensuring the
    Live/Simulation Parity Contract (Strategy §3.3) holds.

    Handlers (Strategy §3.1):
        1. _mock_ethical_validation      — p.8–9
        2. _mock_resume_scoring          — p.20–21
        3. _mock_symptom_interpretation  — p.32–33
        4. _mock_differential_generation — p.33–34
        5. _mock_explanation_generation  — p.34–35
        6. _mock_confidence_scoring      — p.28–29
        7. _default_handler              — fallback
    """

    def __init__(self, seed: int = 42):
        self._rng = random.Random(seed)
        self._handlers = {
            "ethical_validation": self._mock_ethical_validation,
            "resume_scoring": self._mock_resume_scoring,
            "symptom_interpretation": self._mock_symptom_interpretation,
            "differential_generation": self._mock_differential_generation,
            "explanation_generation": self._mock_explanation_generation,
            "confidence_scoring": self._mock_confidence_scoring,
        }
        logger.debug("MockLLM initialized with 7 handler methods.")

    # ------------------------------------------------------------------
    # Public dispatch
    # ------------------------------------------------------------------

    def invoke(self, context_tag: str, payload: dict | None = None) -> dict:
        """
        Route a request to the appropriate handler based on *context_tag*.

        Parameters
        ----------
        context_tag : str
            One of the registered handler keys (e.g. 'resume_scoring').
        payload : dict, optional
            Input data for the handler.

        Returns
        -------
        dict
            Handler response with ``_mock_meta`` attached.
        """
        handler = self._handlers.get(context_tag, self._default_handler)
        payload = payload or {}
        result = handler(payload)
        return result

    # ------------------------------------------------------------------
    # Handler 1: Ethical Validation
    # Ref: EthicalReasoningAgent.evaluate_action(), p.8–9
    # Keyword-match against violation list.
    # ------------------------------------------------------------------

    def _mock_ethical_validation(self, payload: dict) -> dict:
        """
        Validate a proposed action against ethical constraints.

        Violation keywords: share_medical_details, external_email,
        bypass_consent, disable_audit, disable_signals_school_zone.

        Ref: Listing on p.8–9, EthicalReasoningAgent.evaluate_action()
        """
        action = payload.get("action", "").lower()
        context = payload.get("context", {})

        violation_rules = {
            "share_medical_details": (
                "human_rights",
                "Sharing medical details externally violates patient privacy.",
                "HIGH",
            ),
            "external_email": (
                "transparency",
                "Sending data to external recipients without consent.",
                "HIGH",
            ),
            "bypass_consent": (
                "human_rights",
                "Bypassing user consent is prohibited.",
                "HIGH",
            ),
            "disable_audit": (
                "accountability",
                "Disabling audit logging removes accountability.",
                "MEDIUM",
            ),
            "disable_signals_school_zone": (
                "well_being",
                "Disabling traffic signals in a school zone is forbidden.",
                "HIGH",
            ),
        }

        violations = []
        for keyword, (principle, explanation, severity) in violation_rules.items():
            if keyword in action:
                violations.append((principle, explanation, severity))

        is_compliant = len(violations) == 0
        severity = "LOW"
        if violations:
            severity = max(v[2] for v in violations)

        return {
            "is_compliant": is_compliant,
            "violations": violations,
            "severity": severity,
            "action": action,
            "_mock_meta": _make_meta(
                "p.8–9",
                "EthicalReasoningAgent.evaluate_action()",
                "Keyword-match ethical validation against violation list",
            ),
        }

    # ------------------------------------------------------------------
    # Handler 2: Resume Scoring
    # Ref: ResumeAnalyzer.score(), p.20–21
    # Deterministic: score = 0.3 + 0.1 * min(skill_matches, 5)
    #                       + 0.02 * min(years_exp, 10)
    # ------------------------------------------------------------------

    def _mock_resume_scoring(self, payload: dict) -> dict:
        """
        Score a resume deterministically based on skills and experience.

        Formula (Strategy §3.1):
            score = 0.3 + 0.1 * min(skill_matches, 5) + 0.02 * min(years_exp, 10)

        Ref: FairHiringAgent case study, p.20–21
        """
        skills = payload.get("skills", [])
        job_skills = payload.get("job_requirements", {}).get("required_skills", [])
        years_exp = payload.get("years_experience", 0)

        skill_matches = len(set(s.lower() for s in skills) &
                           set(s.lower() for s in job_skills))
        score = 0.3 + 0.1 * min(skill_matches, 5) + 0.02 * min(years_exp, 10)
        score = round(min(score, 1.0), 4)

        explanation_map = {
            "skill_match_count": skill_matches,
            "skill_match_contribution": round(0.1 * min(skill_matches, 5), 4),
            "experience_years": years_exp,
            "experience_contribution": round(0.02 * min(years_exp, 10), 4),
            "base_score": 0.3,
        }

        return {
            "score": score,
            "explanation_map": explanation_map,
            "source": "simulation",
            "_mock_meta": _make_meta(
                "p.20–21",
                "ResumeAnalyzer.score()",
                "Deterministic resume scoring from skills + experience",
            ),
        }

    # ------------------------------------------------------------------
    # Handler 3: Symptom Interpretation
    # Ref: SymptomInterpreter.interpret(), p.32–33
    # Lookup table: 20 symptoms → SNOMED CT codes
    # ------------------------------------------------------------------

    SYMPTOM_LOOKUP = {
        "productive cough":        ("SNOMED:49727002",  0.94),
        "dry cough":               ("SNOMED:11833005",  0.92),
        "fever":                   ("SNOMED:386661006", 0.97),
        "chills":                  ("SNOMED:43724002",  0.93),
        "shortness of breath":     ("SNOMED:267036007", 0.95),
        "chest pain":              ("SNOMED:29857009",  0.91),
        "fatigue":                 ("SNOMED:84229001",  0.89),
        "headache":                ("SNOMED:25064002",  0.90),
        "muscle aches":            ("SNOMED:68962001",  0.88),
        "sore throat":             ("SNOMED:162397003", 0.91),
        "runny nose":              ("SNOMED:64531003",  0.87),
        "nausea":                  ("SNOMED:422587007", 0.90),
        "vomiting":                ("SNOMED:422400008", 0.92),
        "diarrhea":                ("SNOMED:62315008",  0.91),
        "loss of appetite":        ("SNOMED:79890006",  0.86),
        "night sweats":            ("SNOMED:42984000",  0.88),
        "wheezing":                ("SNOMED:56018004",  0.93),
        "rapid breathing":         ("SNOMED:271823003", 0.90),
        "confusion":               ("SNOMED:40917007",  0.85),
        "dizziness":               ("SNOMED:404640003", 0.87),
    }

    def _mock_symptom_interpretation(self, payload: dict) -> dict:
        """
        Map reported symptoms to SNOMED CT codes via lookup table.

        Ref: SymptomInterpreter.interpret(), p.32–33
        """
        raw_symptoms = payload.get("reported_symptoms", "")
        if isinstance(raw_symptoms, str):
            symptom_list = [s.strip().lower() for s in raw_symptoms.split(",") if s.strip()]
        else:
            symptom_list = [s.strip().lower() for s in raw_symptoms]

        interpreted = []
        for symptom in symptom_list:
            match = self.SYMPTOM_LOOKUP.get(symptom)
            if match:
                code, conf = match
                interpreted.append({
                    "symptom": symptom,
                    "snomed_code": code,
                    "confidence": conf,
                })
            else:
                # Partial match fallback
                for known, (code, conf) in self.SYMPTOM_LOOKUP.items():
                    if symptom in known or known in symptom:
                        interpreted.append({
                            "symptom": symptom,
                            "snomed_code": code,
                            "confidence": round(conf * 0.85, 2),
                        })
                        break
                else:
                    interpreted.append({
                        "symptom": symptom,
                        "snomed_code": "SNOMED:UNKNOWN",
                        "confidence": 0.50,
                    })

        return {
            "symptoms": interpreted,
            "_mock_meta": _make_meta(
                "p.32–33",
                "SymptomInterpreter.interpret()",
                "Lookup-table symptom → SNOMED CT mapping",
            ),
        }

    # ------------------------------------------------------------------
    # Handler 4: Differential Diagnosis Generation
    # Ref: DiagnosticCoordinator.generate_differentials(), p.33–34
    # Profile-based routing using vital signs and imaging.
    # ------------------------------------------------------------------

    def _mock_differential_generation(self, payload: dict) -> dict:
        """
        Generate ranked differential diagnoses based on vitals and imaging.

        Primary routing rule (from chapter p.34):
            If wbc_count > 10 AND chest_imaging == 'right_lower_consolidation'
            → pneumonia primary (0.87), bronchitis (0.09), atelectasis (0.04)
            Otherwise → bronchitis primary.

        Ref: DiagnosticCoordinator.generate_differentials(), p.33–34
        """
        vitals = payload.get("vitals", {})
        wbc = vitals.get("wbc_count", 7.5)
        imaging = vitals.get("chest_imaging", "clear")

        if wbc > 10 and imaging == "right_lower_consolidation":
            differentials = [
                {"diagnosis": "community-acquired pneumonia", "raw_score": 0.87},
                {"diagnosis": "acute bronchitis", "raw_score": 0.09},
                {"diagnosis": "atelectasis", "raw_score": 0.04},
            ]
        elif imaging == "bilateral_infiltrates":
            differentials = [
                {"diagnosis": "community-acquired pneumonia", "raw_score": 0.72},
                {"diagnosis": "pulmonary embolism", "raw_score": 0.15},
                {"diagnosis": "acute bronchitis", "raw_score": 0.13},
            ]
        elif wbc > 10:
            differentials = [
                {"diagnosis": "acute bronchitis", "raw_score": 0.55},
                {"diagnosis": "community-acquired pneumonia", "raw_score": 0.30},
                {"diagnosis": "atelectasis", "raw_score": 0.15},
            ]
        else:
            differentials = [
                {"diagnosis": "acute bronchitis", "raw_score": 0.60},
                {"diagnosis": "atelectasis", "raw_score": 0.25},
                {"diagnosis": "community-acquired pneumonia", "raw_score": 0.15},
            ]

        return {
            "differentials": differentials,
            "_mock_meta": _make_meta(
                "p.33–34",
                "DiagnosticCoordinator.generate_differentials()",
                "Profile-based differential diagnosis routing",
            ),
        }

    # ------------------------------------------------------------------
    # Handler 5: Clinical Explanation Generation
    # Ref: ClinicalExplainer.generate(), p.34–35
    # Template fill using chapter examples.
    # ------------------------------------------------------------------

    def _mock_explanation_generation(self, payload: dict) -> dict:
        """
        Generate audience-adapted clinical explanations.

        Clinician template: structured assessment with SHAP contributions.
        Patient template: plain-language summary.

        Ref: ClinicalExplainer.generate(), p.34–35, p.39
        """
        audience = payload.get("audience", "clinician")
        scored = payload.get("scored_differentials", [])
        shap_values = payload.get("shap_values", {})

        top = scored[0] if scored else {"diagnosis": "unknown", "raw_score": 0.5}
        diagnosis = top.get("diagnosis", top.get("answer", "unknown"))
        confidence = top.get("raw_score", top.get("confidence", 0.5))
        alternatives = scored[1:] if len(scored) > 1 else []

        # Default SHAP contributions from chapter p.34
        default_shap = {
            "elevated white blood cell count": 0.31,
            "right lower lobe consolidation on chest imaging": 0.28,
            "productive cough with fever for 4 days": 0.19,
            "oxygen saturation decline from baseline": 0.09,
        }
        features = shap_values if shap_values else default_shap

        if audience == "clinician":
            feature_lines = ", ".join(
                f"{feat} (SHAP contribution: {val:.2f})"
                for feat, val in features.items()
            )
            alt_text = ", ".join(
                f"{a.get('diagnosis', a.get('answer', '?'))} "
                f"({a.get('raw_score', a.get('confidence', 0)):.2f})"
                for a in alternatives
            )
            narrative = (
                f"Primary Assessment: {diagnosis.title()} "
                f"(confidence: {confidence:.2f}). "
                f"Key findings: {feature_lines}. "
                f"Differential: {alt_text}. "
                f"Recommended: Sputum culture, blood cultures, initiation of "
                f"empiric antibiotic therapy per institutional guidelines."
            )
        else:
            narrative = (
                f"The analysis of your test results and symptoms suggests "
                f"a lung infection called {diagnosis}. Your blood tests show "
                f"signs that your body is fighting an infection, and the "
                f"chest scan shows an area of concern in the lower right "
                f"portion of your lung. Your doctor will review these "
                f"findings and may recommend antibiotics and additional "
                f"tests to confirm the diagnosis."
            )

        trace = [
            {"step": "Input Analysis", "detail": "Vitals and symptoms aggregated"},
            {"step": "Rule Application", "detail": f"Profile matched: {diagnosis}"},
            {"step": "Risk Assessment", "detail": f"Confidence: {confidence:.2f}"},
            {"step": "Explanation Generation", "detail": f"Audience: {audience}"},
        ]

        return {
            "narrative": narrative,
            "feature_contributions": features,
            "trace": trace,
            "_mock_meta": _make_meta(
                "p.34–35",
                "ClinicalExplainer.generate()",
                f"Template-filled {audience} explanation",
            ),
        }

    # ------------------------------------------------------------------
    # Handler 6: Confidence Scoring
    # Ref: ConfidenceAwareAgent.score_differentials(), p.28–29
    # Identity calibration + Normal(0, 0.02) noise.
    # ------------------------------------------------------------------

    def _mock_confidence_scoring(self, payload: dict) -> dict:
        """
        Score differentials with calibrated confidence and qualifiers.

        Calibration: identity + Normal(0, 0.02) noise.
        Qualifiers (p.29):
            >0.9  → "High confidence"
            >0.7  → "Moderate confidence"
            else  → "Low confidence — human review recommended"

        Ref: ConfidenceAwareAgent.score_differentials(), p.28–29
        """
        differentials = payload.get("differentials", [])
        evidence = payload.get("evidence", {})

        scored = []
        for diff in differentials:
            raw = diff.get("raw_score", 0.5)
            noise = self._rng.gauss(0, 0.02)
            calibrated = round(max(0.0, min(1.0, raw + noise)), 4)

            if calibrated > 0.9:
                qualifier = "High confidence"
            elif calibrated > 0.7:
                qualifier = "Moderate confidence"
            else:
                qualifier = "Low confidence — human review recommended"

            scored.append({
                "answer": diff.get("diagnosis", "unknown"),
                "confidence": calibrated,
                "qualifier": qualifier,
                "evidence": evidence,
            })

        scored.sort(key=lambda h: h["confidence"], reverse=True)

        return {
            "scored": scored,
            "_mock_meta": _make_meta(
                "p.28–29",
                "ConfidenceAwareAgent.score_differentials()",
                "Identity calibration + Normal(0,0.02) noise with qualifiers",
            ),
        }

    # ------------------------------------------------------------------
    # Handler 7: Default Handler
    # Ref: Strategy §3.1 — fallback for unregistered context tags
    # ------------------------------------------------------------------

    def _default_handler(self, payload: dict) -> dict:
        """
        Fallback for unregistered context tags.

        Returns a generic simulation response with confidence 0.5.
        """
        logger.debug(
            f"Default handler invoked. No specific handler for payload keys: "
            f"{list(payload.keys())}"
        )
        return {
            "response": "[Simulation Mode] Generic mock response.",
            "confidence": 0.5,
            "_mock_meta": _make_meta(
                "—",
                "DefaultHandler",
                "No specific handler matched; generic fallback",
            ),
        }


# ---------------------------------------------------------------------------
# Utility: strip _mock_meta before display
# ---------------------------------------------------------------------------

def strip_meta(response: dict) -> dict:
    """Return a copy of *response* without the ``_mock_meta`` key."""
    cleaned = copy.deepcopy(response)
    cleaned.pop("_mock_meta", None)
    return cleaned


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mock = MockLLM(seed=42)

    # Test ethical validation
    result = mock.invoke("ethical_validation", {
        "action": "share_medical_details with employer"
    })
    print("Ethical:", strip_meta(result))

    # Test resume scoring
    result = mock.invoke("resume_scoring", {
        "skills": ["python", "ml", "sql"],
        "job_requirements": {"required_skills": ["python", "ml", "java", "sql", "aws"]},
        "years_experience": 8,
    })
    print("Resume:", strip_meta(result))

    # Test symptom interpretation
    result = mock.invoke("symptom_interpretation", {
        "reported_symptoms": "productive cough, fever, shortness of breath",
    })
    print("Symptoms:", strip_meta(result))

    # Test differential generation
    result = mock.invoke("differential_generation", {
        "vitals": {"wbc_count": 12.5, "chest_imaging": "right_lower_consolidation"},
    })
    print("Differentials:", strip_meta(result))

    # Test confidence scoring
    diffs = result["differentials"]
    result = mock.invoke("confidence_scoring", {
        "differentials": diffs,
        "evidence": {"vitals": "aggregated", "symptoms": "mapped"},
    })
    print("Confidence:", strip_meta(result))

    # Test explanation generation
    result = mock.invoke("explanation_generation", {
        "audience": "clinician",
        "scored_differentials": [
            {"diagnosis": "community-acquired pneumonia", "raw_score": 0.87},
            {"diagnosis": "acute bronchitis", "raw_score": 0.09},
        ],
    })
    print("Explanation (clinician):", strip_meta(result)["narrative"][:120], "...")

    # Test default handler
    result = mock.invoke("unknown_tag", {"data": "test"})
    print("Default:", strip_meta(result))

    logger.success("MockLLM self-test complete — all 7 handlers verified.")
