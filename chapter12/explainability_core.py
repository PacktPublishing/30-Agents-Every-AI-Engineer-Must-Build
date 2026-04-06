# src/explainability_core.py
# Author: Imran Ahmad
# Book: 30 Agents Every AI Engineer Must Build, Chapter 12
# Ref: The Explainable Agent (p.23–39)
# Description: Complete explainability pipeline — reasoning transparency,
#              LIME/SHAP explanation helpers, counterfactual analysis,
#              confidence calibration, and the DiagnosticAssistant case study.

from __future__ import annotations

import copy
import math
import random
from datetime import datetime, timezone
from typing import Any

import numpy as np

from chapter12.utils import ColorLogger, graceful_fallback, is_simulation
from chapter12.mock_llm import MockLLM, _make_meta

logger = ColorLogger("ExplainabilityCore")


# ═══════════════════════════════════════════════════════════════════════════
# §4.1  ExplainableAgent + DecisionLogger
# Ref: Reasoning Transparency Techniques, p.24–25
# ═══════════════════════════════════════════════════════════════════════════

class DecisionLogger:
    """
    Immutable decision trace logger. Records each processing stage as
    an ordered, write-once trace entry.

    Ref: p.24–25, DecisionLogger for reasoning transparency.
    """

    def __init__(self):
        self._trace: list[dict] = []
        self._recording = False

    def start_recording(self) -> None:
        """Begin a new decision trace (clears previous)."""
        self._trace = []
        self._recording = True

    def record(self, stage: str, data: Any) -> None:
        """Append a stage to the trace. Ref: p.24"""
        if not self._recording:
            return
        self._trace.append({
            "stage": stage,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "entry_index": len(self._trace),
        })

    def get_trace(self) -> list[dict]:
        """Return an immutable copy of the reasoning trace. Ref: p.25"""
        return copy.deepcopy(self._trace)

    def stop_recording(self) -> None:
        self._recording = False


class ExplanationGenerator:
    """
    Generates audience-adapted explanations from a decision trace.
    Ref: p.25, ExplanationGenerator
    """

    @graceful_fallback(
        fallback_value={"explanation": "Explanation unavailable.", "audience": "general"},
        section_ref="Section 12 — ExplanationGenerator.explain() (p.25)",
    )
    def explain(self, input_data: Any, decision: Any,
                trace: list[dict], audience: str = "general") -> dict:
        """
        Generate an explanation from the recorded trace.
        Ref: p.25 — faithful representation, not post-hoc rationalization.
        """
        steps = [f"Step {i+1} ({t['stage']}): processed"
                 for i, t in enumerate(trace)]

        if audience == "engineer":
            explanation = (
                f"Decision trace ({len(trace)} steps): "
                + " → ".join(t["stage"] for t in trace)
                + f". Final decision: {decision}"
            )
        elif audience == "clinician":
            explanation = (
                f"Clinical reasoning: {len(trace)} analysis steps completed. "
                f"Decision: {decision}"
            )
        else:
            explanation = (
                f"The system analyzed your information in {len(trace)} steps "
                f"and reached a recommendation."
            )

        return {
            "explanation": explanation,
            "audience": audience,
            "trace_length": len(trace),
            "steps": steps,
        }


class ExplainableAgent:
    """
    Agent with built-in reasoning transparency.

    Records the reasoning process at every critical stage via
    DecisionLogger. After the final decision, passes the complete
    trace to ExplanationGenerator for audience-adapted output.

    Four-step decision process:
        1. Analyze inputs
        2. Apply domain rules
        3. Assess risks and confidence
        4. Synthesize decision

    Ref: p.24–25, ExplainableAgent
    """

    def __init__(self):
        self.decision_logger = DecisionLogger()
        self.explanation_gen = ExplanationGenerator()
        logger.debug("ExplainableAgent initialized.")

    @graceful_fallback(
        fallback_value=({"decision": "fallback"}, {"explanation": "unavailable"}),
        section_ref="Section 12 — ExplainableAgent.make_decision() (p.24–25)",
    )
    def make_decision(self, input_data: dict,
                      audience: str = "general") -> tuple[dict, dict]:
        """
        Make a decision and generate its explanation.
        Ref: p.24–25, four-step decision process.
        """
        self.decision_logger.start_recording()

        # Step 1: Analyze inputs
        analysis = self.analyze_input(input_data)
        self.decision_logger.record("Input Analysis", analysis)

        # Step 2: Apply domain rules
        rule_results = self.apply_rules(analysis)
        self.decision_logger.record("Rule Application", rule_results)

        # Step 3: Assess risks and confidence
        risk = self.assess_risk(analysis, rule_results)
        self.decision_logger.record("Risk Assessment", risk)

        # Step 4: Synthesize decision
        decision = self.synthesize(analysis, rule_results, risk)
        self.decision_logger.record("Final Decision", decision)

        # Generate explanation from the recorded trace
        explanation = self.explanation_gen.explain(
            input_data, decision,
            self.decision_logger.get_trace(),
            audience=audience,
        )

        return decision, explanation

    def analyze_input(self, input_data: dict) -> dict:
        """Step 1: Analyze input data. Ref: p.24"""
        features = list(input_data.keys())
        return {
            "feature_count": len(features),
            "features": features,
            "data_quality": "complete" if all(
                v is not None for v in input_data.values()
            ) else "partial",
        }

    def apply_rules(self, analysis: dict) -> dict:
        """Step 2: Apply domain rules. Ref: p.24"""
        return {
            "rules_evaluated": 5,
            "rules_triggered": 2,
            "applicable_rules": ["qualification_threshold", "experience_weight"],
        }

    def assess_risk(self, analysis: dict, rule_results: dict) -> dict:
        """Step 3: Assess risk and confidence. Ref: p.24"""
        return {
            "risk_level": "moderate",
            "confidence": 0.82,
            "uncertainty_type": "epistemic",
        }

    def synthesize(self, analysis: dict, rule_results: dict,
                   risk: dict) -> dict:
        """Step 4: Synthesize final decision. Ref: p.24"""
        return {
            "decision": "approve",
            "confidence": risk.get("confidence", 0.5),
            "rationale": (
                f"Based on {analysis['feature_count']} features and "
                f"{rule_results['rules_triggered']} triggered rules."
            ),
        }

    def get_reasoning_trace(self) -> list[dict]:
        """Expose the full reasoning trace for audit. Ref: p.25, p.34"""
        return self.decision_logger.get_trace()


# ═══════════════════════════════════════════════════════════════════════════
# §4.2  LIME / SHAP Explanation Helpers
# Ref: Decision Explanation Frameworks, p.26
# ═══════════════════════════════════════════════════════════════════════════

@graceful_fallback(
    fallback_value={"shap_values": {}, "note": "SHAP computation unavailable."},
    section_ref="Section 12 — SHAP explanation helper (p.26)",
)
def compute_shap_explanation(model, X: np.ndarray, feature_names: list[str],
                             instance_index: int = 0) -> dict:
    """
    Compute SHAP feature attributions for a single prediction.

    Uses TreeSHAP for tree models (exact, polynomial-time per
    Lundberg et al., 2020) or KernelSHAP as model-agnostic fallback.

    Ref: p.26, SHAP provides unified feature attribution via Shapley values.

    Parameters
    ----------
    model : sklearn estimator
        Trained model supporting .predict() or .predict_proba().
    X : np.ndarray
        Feature matrix (n_samples × n_features).
    feature_names : list[str]
        Human-readable names for each feature column.
    instance_index : int
        Index of the instance to explain.

    Returns
    -------
    dict
        {'shap_values': {feature: value}, 'base_value': float,
         'predicted_value': float}
    """
    try:
        import shap
    except ImportError:
        logger.error(
            "SHAP not installed. Returning mock feature attributions. "
            "Install with: pip install shap>=0.45.1"
        )
        return _mock_shap_values(feature_names)

    try:
        # Try TreeExplainer first (exact, fast)
        explainer = shap.TreeExplainer(model)
    except Exception:
        # Fall back to KernelSHAP (model-agnostic, approximate)
        try:
            background = shap.sample(X, min(50, len(X)))
            explainer = shap.KernelExplainer(model.predict_proba, background)
        except Exception:
            explainer = shap.Explainer(model, X)

    shap_values = explainer.shap_values(X[instance_index:instance_index + 1])

    # Handle multi-class output
    if isinstance(shap_values, list):
        sv = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
    elif shap_values.ndim == 3:
        sv = shap_values[0, :, 1] if shap_values.shape[2] > 1 else shap_values[0, :, 0]
    else:
        sv = shap_values[0]

    attribution = {
        name: round(float(val), 4)
        for name, val in zip(feature_names, sv)
    }
    # Sort by absolute contribution
    attribution = dict(
        sorted(attribution.items(), key=lambda x: abs(x[1]), reverse=True)
    )

    try:
        base_value = float(explainer.expected_value)
    except (TypeError, IndexError):
        if hasattr(explainer, "expected_value"):
            ev = explainer.expected_value
            base_value = float(ev[1]) if hasattr(ev, "__len__") and len(ev) > 1 else float(ev)
        else:
            base_value = 0.5

    prediction = model.predict_proba(X[instance_index:instance_index + 1])
    pred_val = float(prediction[0][1]) if prediction.shape[1] > 1 else float(prediction[0][0])

    logger.success(
        f"SHAP computed for instance {instance_index}: "
        f"top feature = {list(attribution.keys())[0]} "
        f"({list(attribution.values())[0]:.4f})"
    )

    return {
        "shap_values": attribution,
        "base_value": round(base_value, 4),
        "predicted_value": round(pred_val, 4),
    }


def _mock_shap_values(feature_names: list[str]) -> dict:
    """Return chapter-derived mock SHAP values when library is unavailable."""
    # Default values from the chapter example (p.34)
    default_contribs = {
        "wbc_count": 0.31,
        "chest_imaging": 0.28,
        "reported_symptoms": 0.19,
        "spo2_min": 0.09,
        "heart_rate_avg": 0.06,
        "temperature": 0.04,
        "patient_history": 0.03,
    }
    attribution = {}
    for name in feature_names:
        attribution[name] = default_contribs.get(name, round(random.uniform(-0.05, 0.05), 4))
    return {
        "shap_values": attribution,
        "base_value": 0.5,
        "predicted_value": 0.87,
        "note": "Mock SHAP values (SHAP library not available).",
    }


@graceful_fallback(
    fallback_value={"lime_weights": {}, "note": "LIME computation unavailable."},
    section_ref="Section 12 — LIME explanation helper (p.26)",
)
def compute_lime_explanation(model, X: np.ndarray, feature_names: list[str],
                             instance_index: int = 0,
                             num_features: int = 6) -> dict:
    """
    Generate a LIME explanation for a single prediction.

    LIME constructs a local interpretable model approximating the
    original model's behavior in the neighborhood of the instance.

    Ref: p.26, LIME for local feature attribution.

    Returns
    -------
    dict
        {'lime_weights': {feature: weight}, 'intercept': float,
         'predicted_class': int, 'local_accuracy': float}
    """
    try:
        from lime.lime_tabular import LimeTabularExplainer
    except ImportError:
        logger.error(
            "LIME not installed. Returning mock weights. "
            "Install with: pip install lime>=0.2.0.1"
        )
        return _mock_lime_values(feature_names)

    explainer = LimeTabularExplainer(
        X,
        feature_names=feature_names,
        class_names=["negative", "positive"],
        mode="classification",
    )

    explanation = explainer.explain_instance(
        X[instance_index],
        model.predict_proba,
        num_features=num_features,
    )

    weights = {feat: round(weight, 4) for feat, weight in explanation.as_list()}
    pred_class = int(model.predict(X[instance_index:instance_index + 1])[0])

    logger.success(
        f"LIME computed for instance {instance_index}: "
        f"{len(weights)} features explained."
    )

    return {
        "lime_weights": weights,
        "intercept": round(float(explanation.intercept[1]), 4),
        "predicted_class": pred_class,
        "local_accuracy": round(float(explanation.score), 4),
    }


def _mock_lime_values(feature_names: list[str]) -> dict:
    """Return mock LIME values when library is unavailable."""
    rng = random.Random(42)
    weights = {name: round(rng.uniform(-0.3, 0.3), 4) for name in feature_names[:6]}
    return {
        "lime_weights": weights,
        "intercept": 0.45,
        "predicted_class": 1,
        "local_accuracy": 0.92,
        "note": "Mock LIME values (lime library not available).",
    }


# ═══════════════════════════════════════════════════════════════════════════
# §4.3  Counterfactual Analysis
# Ref: p.27, Minimal Counterfactual Theorem
# ═══════════════════════════════════════════════════════════════════════════

@graceful_fallback(
    fallback_value={"counterfactual": {}, "changes": {},
                    "note": "Counterfactual generation failed."},
    section_ref="Section 12 — Counterfactual analysis (p.27)",
)
def generate_counterfactual(model, instance: np.ndarray,
                            feature_names: list[str],
                            desired_class: int = 1,
                            step_size: float = 0.1,
                            max_iterations: int = 100) -> dict:
    """
    Find the minimal feature changes to flip a decision.

    Implements the Minimal Counterfactual Theorem (p.27):
    The optimal counterfactual x' for instance x minimizes d(x, x')
    subject to f(x') = desired_class.

    Uses greedy feature perturbation: at each step, nudge the feature
    with the highest gradient toward the desired class.

    Parameters
    ----------
    model : sklearn estimator
        Trained classifier with predict() and predict_proba().
    instance : np.ndarray
        1-D array of feature values for the instance to explain.
    feature_names : list[str]
        Names of each feature.
    desired_class : int
        Target class for the counterfactual (default: 1 = positive).
    step_size : float
        Perturbation magnitude per iteration.
    max_iterations : int
        Maximum search iterations.

    Returns
    -------
    dict
        {'counterfactual': {feature: new_value},
         'original': {feature: original_value},
         'changes': {feature: delta},
         'iterations': int, 'success': bool}
    """
    x = instance.copy().reshape(1, -1).astype(float)
    original = {name: round(float(x[0, i]), 4) for i, name in enumerate(feature_names)}

    for iteration in range(max_iterations):
        pred = model.predict(x)[0]
        if int(pred) == desired_class:
            cf = {name: round(float(x[0, i]), 4) for i, name in enumerate(feature_names)}
            changes = {
                name: round(cf[name] - original[name], 4)
                for name in feature_names
                if abs(cf[name] - original[name]) > 1e-6
            }
            logger.success(
                f"Counterfactual found in {iteration + 1} iterations. "
                f"{len(changes)} feature(s) changed."
            )
            return {
                "counterfactual": cf,
                "original": original,
                "changes": changes,
                "iterations": iteration + 1,
                "success": True,
            }

        # Estimate gradient via finite differences
        proba = model.predict_proba(x)[0]
        current_prob = proba[desired_class] if len(proba) > desired_class else proba[0]
        gradients = np.zeros(x.shape[1])

        for i in range(x.shape[1]):
            x_perturbed = x.copy()
            x_perturbed[0, i] += step_size
            p_perturbed = model.predict_proba(x_perturbed)[0]
            new_prob = p_perturbed[desired_class] if len(p_perturbed) > desired_class else p_perturbed[0]
            gradients[i] = (new_prob - current_prob) / step_size

        # Nudge the feature with the highest gradient
        best_feature = int(np.argmax(np.abs(gradients)))
        direction = 1.0 if gradients[best_feature] > 0 else -1.0
        x[0, best_feature] += direction * step_size

    # Did not converge
    cf = {name: round(float(x[0, i]), 4) for i, name in enumerate(feature_names)}
    changes = {
        name: round(cf[name] - original[name], 4)
        for name in feature_names
        if abs(cf[name] - original[name]) > 1e-6
    }
    logger.info(
        f"Counterfactual search did not converge in {max_iterations} iterations."
    )
    return {
        "counterfactual": cf,
        "original": original,
        "changes": changes,
        "iterations": max_iterations,
        "success": False,
    }


# ═══════════════════════════════════════════════════════════════════════════
# §4.4  ConfidenceAwareAgent
# Ref: Confidence Communication Methods, p.28–29
# ═══════════════════════════════════════════════════════════════════════════

class TemperatureScaler:
    """
    Post-hoc calibration via temperature scaling.

    Calibration means a confidence score does what it promises:
    when the agent says '80% confident', ~80% of those predictions
    should be correct. Ref: p.27

    In simulation mode, applies identity + small noise.
    """

    def __init__(self, temperature: float = 1.0):
        self.temperature = temperature

    def calibrate(self, raw_score: float) -> float:
        """Apply temperature scaling to a raw confidence score."""
        # Platt-style sigmoid rescaling
        logit = math.log(max(raw_score, 1e-8) / max(1.0 - raw_score, 1e-8))
        scaled_logit = logit / max(self.temperature, 0.01)
        calibrated = 1.0 / (1.0 + math.exp(-scaled_logit))
        return round(max(0.0, min(1.0, calibrated)), 4)


class ConfidenceAwareAgent:
    """
    Agent that generates and ranks multiple hypotheses with
    calibrated confidence scores.

    Ref: p.28–29, ConfidenceAwareAgent
    """

    def __init__(self, n_hypotheses: int = 3):
        self.n_hypotheses = n_hypotheses
        self.calibrator = TemperatureScaler(temperature=1.0)
        self._mock = MockLLM()
        self._rng = random.Random(42)
        logger.debug(
            f"ConfidenceAwareAgent initialized (n_hypotheses={n_hypotheses})."
        )

    @graceful_fallback(
        fallback_value=[],
        section_ref="Section 12 — ConfidenceAwareAgent.score_differentials() (p.28–29)",
    )
    def score_differentials(self, differentials: list[dict],
                            evidence: dict | None = None) -> list[dict]:
        """
        Score each differential with calibrated confidence.
        Ref: p.28–29
        """
        result = self._mock.invoke("confidence_scoring", {
            "differentials": differentials,
            "evidence": evidence or {},
        })
        return result.get("scored", [])

    @graceful_fallback(
        fallback_value=[{"answer": "unknown", "confidence": 0.5,
                         "qualifier": "Low confidence — human review recommended",
                         "evidence": {}}],
        section_ref="Section 12 — ConfidenceAwareAgent.reason_with_confidence() (p.28–29)",
    )
    def reason_with_confidence(self, query: str,
                               context: dict | None = None) -> list[dict]:
        """
        Generate multiple hypotheses with calibrated confidence.
        Ref: p.28–29
        """
        hypotheses = []
        for i in range(self.n_hypotheses):
            raw_score = max(0.1, 0.9 - i * 0.25 + self._rng.gauss(0, 0.03))
            calibrated = self.calibrator.calibrate(raw_score)

            hypotheses.append({
                "answer": f"Hypothesis {i + 1} for: {query[:50]}",
                "confidence": calibrated,
                "evidence": context or {},
            })

        hypotheses.sort(key=lambda h: h["confidence"], reverse=True)
        return hypotheses

    def communicate_uncertainty(self, hypotheses: list[dict]) -> dict:
        """
        Format uncertainty for user consumption.

        Qualifier mapping (p.29):
            >0.9  → 'High confidence'
            >0.7  → 'Moderate confidence'
            else  → 'Low confidence — human review recommended'

        Ref: p.29, communicate_uncertainty()
        """
        top = hypotheses[0] if hypotheses else {
            "answer": "unknown", "confidence": 0.0, "evidence": {}
        }

        conf = top.get("confidence", 0.0)
        if conf > 0.9:
            qualifier = "High confidence"
        elif conf > 0.7:
            qualifier = "Moderate confidence"
        else:
            qualifier = "Low confidence — human review recommended"

        return {
            "recommendation": top.get("answer", "unknown"),
            "confidence_level": qualifier,
            "confidence_score": round(conf, 2),
            "supporting_evidence": top.get("evidence", {}),
            "alternative_hypotheses": hypotheses[1:] if len(hypotheses) > 1 else [],
        }


# ═══════════════════════════════════════════════════════════════════════════
# §4.5  DiagnosticAssistant + ClinicalExplainer
# Ref: Case Study — Medical Diagnosis Assistant, p.30–35, p.39
# ═══════════════════════════════════════════════════════════════════════════

class BiometricAnalyzer:
    """
    Analyzes aggregated biometric data from the edge processing layer.

    Accepts a patient_data dict with a 'biometrics' field containing
    rolling-window aggregated features. Raw sensor data never reaches
    this component (p.31–32, edge computing for privacy).

    Ref: p.30–31, Biometric agents
    """

    @graceful_fallback(
        fallback_value={"vitals": {}, "anomalies": [], "status": "fallback"},
        section_ref="Section 12 — BiometricAnalyzer.analyze() (p.31–32)",
    )
    def analyze(self, patient_data: dict) -> dict:
        """Analyze biometric data and return vitals report. Ref: p.32"""
        vitals = {
            "heart_rate_avg": patient_data.get("heart_rate_avg", 75.0),
            "spo2_min": patient_data.get("spo2_min", 96.0),
            "wbc_count": patient_data.get("wbc_count", 7.5),
            "temperature": patient_data.get("temperature", 37.0),
            "chest_imaging": patient_data.get("chest_imaging", "clear"),
        }

        anomalies = []
        if vitals["spo2_min"] < 90:
            anomalies.append({"metric": "spo2_min", "value": vitals["spo2_min"],
                              "threshold": 90, "alert": "CRITICAL"})
        if vitals["wbc_count"] > 10:
            anomalies.append({"metric": "wbc_count", "value": vitals["wbc_count"],
                              "threshold": 10, "alert": "ELEVATED"})
        if vitals["temperature"] > 38.0:
            anomalies.append({"metric": "temperature", "value": vitals["temperature"],
                              "threshold": 38.0, "alert": "FEVER"})

        status = "abnormal" if anomalies else "normal"
        logger.debug(
            f"Biometrics analyzed: {status} "
            f"({len(anomalies)} anomalies detected)."
        )

        return {"vitals": vitals, "anomalies": anomalies, "status": status}


class SymptomInterpreter:
    """
    Maps patient-reported symptoms to SNOMED CT concepts using
    the MockLLM symptom lookup table.

    Ref: p.31–33, Symptom analysis agents
    """

    def __init__(self):
        self._mock = MockLLM()

    @graceful_fallback(
        fallback_value=[],
        section_ref="Section 12 — SymptomInterpreter.interpret() (p.32–33)",
    )
    def interpret(self, reported_symptoms: list[str] | str) -> list[dict]:
        """Map symptoms to SNOMED CT codes. Ref: p.32–33"""
        if isinstance(reported_symptoms, list):
            symptom_str = ", ".join(reported_symptoms)
        else:
            symptom_str = reported_symptoms

        result = self._mock.invoke("symptom_interpretation", {
            "reported_symptoms": symptom_str,
        })
        return result.get("symptoms", [])


class DiagnosticCoordinator:
    """
    Integrates biometric and symptom data to generate ranked
    differential diagnoses.

    Ref: p.31, p.33–34, Coordinator agents
    """

    def __init__(self):
        self._mock = MockLLM()

    @graceful_fallback(
        fallback_value=[{"diagnosis": "unknown", "raw_score": 0.5}],
        section_ref="Section 12 — DiagnosticCoordinator.generate_differentials() (p.33–34)",
    )
    def generate_differentials(self, vitals: dict, symptoms: list[dict],
                               history: list[str] | None = None) -> list[dict]:
        """Generate ranked differential diagnoses. Ref: p.33–34"""
        vitals_data = vitals.get("vitals", vitals)
        result = self._mock.invoke("differential_generation", {
            "vitals": vitals_data,
            "symptoms": symptoms,
            "history": history or [],
        })
        return result.get("differentials", [])


class ClinicalMemorySystem:
    """
    Memory architecture for the diagnostic assistant.

    Implements episodic, semantic, and working memory patterns
    from Chapter 5. Ref: p.31
    """

    def __init__(self):
        self._episodic: dict[str, list[dict]] = {}  # patient_id → encounters
        self._semantic: dict[str, Any] = {}          # clinical knowledge

    def retrieve_episodic(self, patient_id: str) -> list[dict]:
        """Retrieve patient interaction history. Ref: p.31"""
        return self._episodic.get(patient_id, [])

    def store_episodic(self, patient_id: str, encounter: dict) -> None:
        """Store a new patient encounter. Ref: p.31"""
        self._episodic.setdefault(patient_id, []).append({
            **encounter,
            "stored_at": datetime.now(timezone.utc).isoformat(),
        })

    def retrieve_semantic(self, key: str) -> Any:
        """Retrieve clinical knowledge. Ref: p.31"""
        return self._semantic.get(key)


class ClinicalExplainer:
    """
    Generates audience-adapted clinical explanations.

    Clinician template: structured assessment with SHAP contributions.
    Patient template: plain-language summary.

    Ref: p.34–35, p.39, ClinicalExplainer.generate()
    """

    def __init__(self):
        self._mock = MockLLM()
        self._trace: list[dict] = []

    @graceful_fallback(
        fallback_value={"narrative": "Explanation temporarily unavailable.",
                        "feature_contributions": {}, "trace": []},
        section_ref="Section 12 — ClinicalExplainer.generate() (p.34–35)",
    )
    def generate(self, scored_differentials: list[dict],
                 audience: str = "clinician",
                 evidence_sources: list[dict] | None = None,
                 shap_values: dict | None = None) -> dict:
        """
        Generate an audience-adapted clinical explanation.

        Three internal steps (p.39):
            1. Select template based on audience
            2. Format SHAP values into ranked contributing factors
            3. NLG step to produce fluent narrative

        Ref: p.34–35, p.39
        """
        result = self._mock.invoke("explanation_generation", {
            "audience": audience,
            "scored_differentials": scored_differentials,
            "shap_values": shap_values or {},
        })

        self._trace = result.get("trace", [])

        logger.success(
            f"Clinical explanation generated for audience='{audience}'. "
            f"Trace: {len(self._trace)} steps."
        )

        return {
            "narrative": result["narrative"],
            "feature_contributions": result["feature_contributions"],
            "trace": self._trace,
        }

    def get_reasoning_trace(self) -> list[dict]:
        """Expose reasoning trace for audit. Ref: p.34"""
        return copy.deepcopy(self._trace)


class DiagnosticReport:
    """Structured output of the DiagnosticAssistant. Ref: p.34"""

    def __init__(self, differentials: list[dict], explanation: dict,
                 confidence_summary: dict, audit_trail: list[dict]):
        self.differentials = differentials
        self.explanation = explanation
        self.confidence_summary = confidence_summary
        self.audit_trail = audit_trail

    def to_dict(self) -> dict:
        return {
            "differentials": self.differentials,
            "explanation": self.explanation,
            "confidence_summary": self.confidence_summary,
            "audit_trail": self.audit_trail,
        }


class DiagnosticAssistant:
    """
    Clinical decision support agent with multi-source evidence
    integration and audience-adapted explanations.

    Architecture (p.30–35):
        - BiometricAnalyzer: aggregated wearable features
        - SymptomInterpreter: NLP → SNOMED CT mapping
        - DiagnosticCoordinator: differential ranking
        - ClinicalExplainer: SHAP-based audience-adapted output
        - ConfidenceAwareAgent: calibrated uncertainty
        - ClinicalMemorySystem: episodic, semantic, working memory

    Ref: p.32–35, DiagnosticAssistant
    """

    def __init__(self, n_hypotheses: int = 5):
        self.biometric_agent = BiometricAnalyzer()
        self.symptom_agent = SymptomInterpreter()
        self.coordinator = DiagnosticCoordinator()
        self.explainer = ClinicalExplainer()
        self.confidence_engine = ConfidenceAwareAgent(n_hypotheses=n_hypotheses)
        self.memory = ClinicalMemorySystem()
        logger.debug("DiagnosticAssistant initialized with all sub-agents.")

    @graceful_fallback(
        fallback_value=DiagnosticReport(
            differentials=[], explanation={},
            confidence_summary={}, audit_trail=[],
        ),
        section_ref="Section 12 — DiagnosticAssistant.diagnose() (p.32–35)",
    )
    def diagnose(self, patient_data: dict,
                 reported_symptoms: list[str] | str,
                 audience: str = "clinician") -> DiagnosticReport:
        """
        Generate an explained, confidence-rated diagnosis.

        Pipeline:
            1. Gather evidence (biometrics, symptoms, history)
            2. Generate ranked differentials
            3. Score with calibrated confidence
            4. Generate clinical explanation
            5. Store encounter in episodic memory

        Ref: p.32–35
        """
        patient_id = patient_data.get("patient_id", "unknown")

        # Gather evidence from multiple sources
        vitals = self.biometric_agent.analyze(patient_data)
        symptoms = self.symptom_agent.interpret(reported_symptoms)
        history = self.memory.retrieve_episodic(patient_id)

        # Generate ranked differential diagnoses
        differentials = self.coordinator.generate_differentials(
            vitals, symptoms,
            history=patient_data.get("patient_history", []),
        )

        # Score each with calibrated confidence
        scored = self.confidence_engine.score_differentials(
            differentials,
            evidence={
                "vitals": vitals,
                "symptoms": symptoms,
                "history": history,
            },
        )

        # Generate clinical explanation
        explanation = self.explainer.generate(
            scored_differentials=scored if scored else differentials,
            audience=audience,
            evidence_sources=[vitals, {"symptoms": symptoms}],
        )

        # Store encounter in episodic memory
        self.memory.store_episodic(patient_id, {
            "diagnoses": scored,
            "evidence": [vitals, {"symptoms": symptoms}],
            "explanation": explanation,
        })

        # Confidence summary
        confidence_summary = self.confidence_engine.communicate_uncertainty(
            scored if scored else []
        )

        report = DiagnosticReport(
            differentials=scored if scored else differentials,
            explanation=explanation,
            confidence_summary=confidence_summary,
            audit_trail=self.explainer.get_reasoning_trace(),
        )

        logger.success(
            f"Diagnosis complete for patient {patient_id}. "
            f"Top: {confidence_summary.get('recommendation', 'N/A')} "
            f"({confidence_summary.get('confidence_level', 'N/A')})"
        )

        return report
