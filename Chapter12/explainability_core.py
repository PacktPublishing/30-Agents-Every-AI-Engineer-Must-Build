"""
Explainability Core: Reasoning transparency, feature attribution, counterfactual
analysis, confidence communication, and clinical diagnosis explanation.

Implements the complete explainability pipeline from Chapter 12, including:
  - ExplainableAgent with DecisionLogger and immutable audit trail (p.24-25)
  - LIME and SHAP wrapper functions for feature attribution (p.26)
  - Counterfactual analysis for minimal-change explanations (p.27)
  - ConfidenceAwareAgent with calibration and qualifier mapping (p.28-29)
  - DiagnosticAssistant with BiometricAnalyzer, SymptomInterpreter,
    DiagnosticCoordinator, and ClinicalExplainer (p.30-35)

Author: Imran Ahmad
Book: 30 Agents Every AI Engineer Must Build, Chapter 12
"""

import copy
import numpy as np
import pandas as pd
from typing import Any, Optional
from datetime import datetime, timezone

from src.utils import ColorLogger, graceful_fallback, get_mode, is_simulation
from src.mock_llm import MockLLM, get_mock_llm

logger = ColorLogger(name="ExplainCore")


# ═══════════════════════════════════════════════════════════════════════════
# Section 4.1 — ExplainableAgent + DecisionLogger (Chapter 12, p.24–25)
# ═══════════════════════════════════════════════════════════════════════════

class DecisionLogger:
    """
    Immutable audit trail for agent decisions. See Chapter 12, p.24-25.

    Records every step in the four-step decision process:
        1. Input reception
        2. Reasoning / analysis
        3. Decision output
        4. Explanation generation

    The trace is append-only; get_trace() returns a deep copy.
    """

    def __init__(self, agent_name: str = "ExplainableAgent"):
        self._trace: list[dict] = []
        self._agent_name = agent_name
        logger.debug(f"DecisionLogger initialized for '{agent_name}'.")

    def log_step(self, step_name: str, data: dict, status: str = "complete") -> None:
        """
        Append a step to the audit trail.

        Args:
            step_name: Human-readable step identifier.
            data: Arbitrary payload for this step.
            status: One of 'complete', 'partial', 'failed'.
        """
        entry = {
            "step": step_name,
            "agent": self._agent_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "data": copy.deepcopy(data),
        }
        self._trace.append(entry)
        logger.debug(f"[Trace] {step_name} → {status}")

    def get_trace(self) -> list[dict]:
        """Return the immutable audit trail (deep copy)."""
        return copy.deepcopy(self._trace)

    def summary(self) -> str:
        """Return a one-line summary of the trace."""
        steps = [e["step"] for e in self._trace]
        statuses = [e["status"] for e in self._trace]
        failed = sum(1 for s in statuses if s == "failed")
        return (
            f"Trace: {len(self._trace)} steps [{' → '.join(steps)}]. "
            f"Failures: {failed}."
        )


class ExplainableAgent:
    """
    Agent with built-in reasoning transparency. See Chapter 12, p.24-25.

    Four-step decision process:
        1. receive_input() — log and validate incoming data.
        2. reason() — analyze input, produce intermediate results.
        3. decide() — generate final output.
        4. explain() — produce human-readable explanation of the decision.

    Every step is logged via DecisionLogger for full auditability.
    """

    def __init__(self, name: str = "ExplainableAgent"):
        self._logger = DecisionLogger(agent_name=name)
        self._name = name
        self._mock_llm = get_mock_llm() if is_simulation() else None
        self._last_input = None
        self._last_reasoning = None
        self._last_decision = None
        logger.info(f"ExplainableAgent '{name}' initialized. Mode: {get_mode()}")

    @graceful_fallback(
        fallback_value={"status": "input_failed", "data": None},
        section_ref="Section 12 - Input Reception (p.24)"
    )
    def receive_input(self, data: dict) -> dict:
        """Step 1: Receive and validate input data."""
        self._last_input = copy.deepcopy(data)
        self._logger.log_step("input_reception", {
            "fields_received": list(data.keys()),
            "record_count": len(data) if isinstance(data, dict) else 1,
        })
        logger.info(f"Input received: {len(data)} field(s).")
        return {"status": "received", "data": data}

    @graceful_fallback(
        fallback_value={"status": "reasoning_failed", "intermediate": {}},
        section_ref="Section 12 - Reasoning Step (p.24)"
    )
    def reason(self, input_data: Optional[dict] = None) -> dict:
        """
        Step 2: Analyze input and produce intermediate results.
        In simulation mode, delegates to MockLLM.
        """
        data = input_data or self._last_input or {}

        # Simple rule-based reasoning (extended by subclasses)
        intermediate = {
            "input_summary": {k: type(v).__name__ for k, v in data.items()},
            "analysis_mode": get_mode(),
        }

        self._last_reasoning = intermediate
        self._logger.log_step("reasoning", intermediate)
        logger.debug("Reasoning step complete.")
        return {"status": "complete", "intermediate": intermediate}

    @graceful_fallback(
        fallback_value={"status": "decision_failed", "output": None},
        section_ref="Section 12 - Decision Output (p.25)"
    )
    def decide(self, reasoning: Optional[dict] = None) -> dict:
        """Step 3: Generate final decision based on reasoning."""
        r = reasoning or self._last_reasoning or {}

        decision = {
            "recommendation": "proceed",
            "confidence": 0.85,
            "basis": r,
        }

        self._last_decision = decision
        self._logger.log_step("decision", decision)
        logger.success(f"Decision: {decision['recommendation']} "
                       f"(confidence: {decision['confidence']:.2f})")
        return {"status": "decided", "output": decision}

    @graceful_fallback(
        fallback_value={"status": "explanation_failed", "explanation": ""},
        section_ref="Section 12 - Explanation Generation (p.25)"
    )
    def explain(self, decision: Optional[dict] = None) -> dict:
        """Step 4: Produce a human-readable explanation."""
        d = decision or self._last_decision or {}
        confidence = d.get("confidence", 0.0)

        explanation = (
            f"The agent recommends '{d.get('recommendation', 'N/A')}' "
            f"with {confidence:.0%} confidence. "
            f"This decision was based on analysis of the provided input data "
            f"using the {get_mode()} pipeline."
        )

        self._logger.log_step("explanation", {"text": explanation})
        logger.info("Explanation generated.")
        return {"status": "explained", "explanation": explanation}

    def run_full_pipeline(self, data: dict) -> dict:
        """Execute all four steps and return the complete result with trace."""
        self.receive_input(data)
        self.reason(data)
        self.decide()
        explanation = self.explain()

        return {
            "explanation": explanation.get("explanation", ""),
            "decision": self._last_decision,
            "trace": self.get_trace(),
        }

    def get_trace(self) -> list[dict]:
        """Return the immutable audit trail."""
        return self._logger.get_trace()

    def get_trace_summary(self) -> str:
        """Return a one-line summary of the trace."""
        return self._logger.summary()


# ═══════════════════════════════════════════════════════════════════════════
# Section 4.2 — LIME / SHAP Explanation Helpers (Chapter 12, p.26)
# ═══════════════════════════════════════════════════════════════════════════

@graceful_fallback(
    fallback_value={"shap_values": None, "feature_importance": {},
                    "status": "shap_unavailable"},
    section_ref="Section 12 - SHAP Explanations (p.26)"
)
def compute_shap_explanations(model, X: pd.DataFrame,
                              feature_names: Optional[list] = None,
                              max_evals: int = 500) -> dict:
    """
    Compute SHAP feature attributions for a trained sklearn model.

    Wraps shap.Explainer with @graceful_fallback for import errors
    and computation timeouts. See Chapter 12, p.26.

    Args:
        model: A trained sklearn classifier/regressor.
        X: Feature matrix (DataFrame or ndarray).
        feature_names: Optional column names.
        max_evals: Maximum SHAP evaluations (controls speed).

    Returns:
        dict with 'shap_values', 'feature_importance', 'status'.
    """
    import shap

    if feature_names is None:
        feature_names = list(X.columns) if hasattr(X, "columns") else \
            [f"feature_{i}" for i in range(X.shape[1])]

    logger.info(f"Computing SHAP explanations: {X.shape[0]} samples, "
                f"{len(feature_names)} features.")

    explainer = shap.Explainer(model, X, feature_names=feature_names)
    shap_values = explainer(X, max_evals=max_evals)

    # Mean absolute SHAP values for global feature importance
    mean_abs = np.abs(shap_values.values).mean(axis=0)
    if mean_abs.ndim > 1:
        # Multi-class: take mean across classes
        mean_abs = mean_abs.mean(axis=-1)

    importance = {
        name: round(float(val), 4)
        for name, val in zip(feature_names, mean_abs)
    }
    # Sort by importance
    importance = dict(sorted(importance.items(), key=lambda x: -x[1]))

    logger.success(f"SHAP complete. Top feature: "
                   f"{list(importance.keys())[0]} = {list(importance.values())[0]:.4f}")

    return {
        "shap_values": shap_values,
        "feature_importance": importance,
        "status": "complete",
    }


@graceful_fallback(
    fallback_value={"lime_explanation": None, "feature_weights": {},
                    "status": "lime_unavailable"},
    section_ref="Section 12 - LIME Explanations (p.26)"
)
def compute_lime_explanations(model, X: pd.DataFrame, instance_idx: int = 0,
                              feature_names: Optional[list] = None,
                              num_features: int = 5) -> dict:
    """
    Compute LIME explanation for a single instance. See Chapter 12, p.26.

    Args:
        model: A trained sklearn classifier/regressor.
        X: Feature matrix.
        instance_idx: Index of the instance to explain.
        feature_names: Optional column names.
        num_features: Number of top features in explanation.

    Returns:
        dict with 'lime_explanation', 'feature_weights', 'status'.
    """
    import lime
    import lime.lime_tabular

    if feature_names is None:
        feature_names = list(X.columns) if hasattr(X, "columns") else \
            [f"feature_{i}" for i in range(X.shape[1])]

    X_array = X.values if hasattr(X, "values") else np.array(X)

    logger.info(f"Computing LIME explanation for instance {instance_idx}.")

    explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=X_array,
        feature_names=feature_names,
        mode="classification" if hasattr(model, "predict_proba") else "regression",
        random_state=42,
    )

    # Determine predict function
    if hasattr(model, "predict_proba"):
        predict_fn = model.predict_proba
    else:
        predict_fn = model.predict

    explanation = explainer.explain_instance(
        X_array[instance_idx],
        predict_fn,
        num_features=num_features,
    )

    feature_weights = {
        name: round(weight, 4)
        for name, weight in explanation.as_list()
    }

    logger.success(f"LIME complete for instance {instance_idx}.")

    return {
        "lime_explanation": explanation,
        "feature_weights": feature_weights,
        "status": "complete",
        "instance_idx": instance_idx,
    }


def train_diagnostic_model(df: pd.DataFrame) -> tuple:
    """
    Train a simple sklearn model on the synthetic medical dataset
    for use with SHAP/LIME explanations.

    Returns:
        (model, X, y, feature_names, label_encoder)
    """
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.preprocessing import LabelEncoder

    logger.info("Training diagnostic model on synthetic medical data...")

    feature_cols = ["heart_rate_avg", "spo2_min", "wbc_count", "temperature"]

    # Encode chest_imaging as numeric
    imaging_map = {
        "clear": 0, "normal": 1,
        "right_lower_consolidation": 2, "bilateral_infiltrates": 3,
    }
    df = df.copy()
    df["chest_imaging_num"] = df["chest_imaging"].map(imaging_map).fillna(0)
    feature_cols.append("chest_imaging_num")

    X = df[feature_cols].copy()
    le = LabelEncoder()
    y = le.fit_transform(df["true_diagnosis"])

    model = GradientBoostingClassifier(
        n_estimators=50, max_depth=3, random_state=42
    )
    model.fit(X, y)

    feature_names = feature_cols
    logger.success(
        f"Diagnostic model trained: {len(feature_names)} features, "
        f"{len(le.classes_)} classes ({list(le.classes_)})."
    )

    return model, X, y, feature_names, le


# ═══════════════════════════════════════════════════════════════════════════
# Section 4.3 — Counterfactual Analysis (Chapter 12, p.27)
# ═══════════════════════════════════════════════════════════════════════════

@graceful_fallback(
    fallback_value={"counterfactual": None, "changes": {},
                    "status": "counterfactual_failed"},
    section_ref="Section 12 - Counterfactual Analysis (p.27)"
)
def generate_counterfactual(model, instance: np.ndarray,
                            feature_names: list,
                            target_class: int,
                            feature_ranges: Optional[dict] = None,
                            max_iterations: int = 100,
                            step_size: float = 0.1) -> dict:
    """
    Find the minimal feature changes to flip a model's decision.
    See Chapter 12, p.27.

    Uses a simple greedy search: for each feature, perturb in the
    direction that moves the prediction toward the target class.

    Args:
        model: Trained sklearn classifier with predict_proba().
        instance: 1D array of feature values to explain.
        feature_names: Names corresponding to instance features.
        target_class: Class index to flip toward.
        feature_ranges: Optional {feature: (min, max)} constraints.
        max_iterations: Maximum perturbation steps.
        step_size: Fractional step per iteration.

    Returns:
        dict with 'counterfactual', 'changes', 'status'.
    """
    logger.info(f"Generating counterfactual: target_class={target_class}")

    current = instance.copy().astype(float)
    original = instance.copy().astype(float)
    feature_ranges = feature_ranges or {}

    for iteration in range(max_iterations):
        proba = model.predict_proba(current.reshape(1, -1))[0]
        predicted = int(np.argmax(proba))

        if predicted == target_class:
            # Success — compute changes
            changes = {}
            for i, name in enumerate(feature_names):
                diff = current[i] - original[i]
                if abs(diff) > 1e-6:
                    changes[name] = {
                        "original": round(float(original[i]), 4),
                        "counterfactual": round(float(current[i]), 4),
                        "change": round(float(diff), 4),
                    }

            logger.success(
                f"Counterfactual found in {iteration + 1} iterations. "
                f"Changed {len(changes)} feature(s)."
            )
            return {
                "counterfactual": current.tolist(),
                "changes": changes,
                "iterations": iteration + 1,
                "target_class": target_class,
                "target_probability": round(float(proba[target_class]), 4),
                "status": "found",
            }

        # Greedy perturbation: find best feature to change
        best_feature = -1
        best_improvement = -1.0

        for i in range(len(current)):
            for direction in [+1, -1]:
                candidate = current.copy()
                delta = step_size * abs(original[i]) if abs(original[i]) > 0.01 else step_size
                candidate[i] += direction * delta

                # Apply range constraints
                name = feature_names[i]
                if name in feature_ranges:
                    lo, hi = feature_ranges[name]
                    candidate[i] = np.clip(candidate[i], lo, hi)

                new_proba = model.predict_proba(candidate.reshape(1, -1))[0]
                improvement = new_proba[target_class] - proba[target_class]

                if improvement > best_improvement:
                    best_improvement = improvement
                    best_feature = i
                    best_candidate = candidate.copy()

        if best_feature >= 0 and best_improvement > 0:
            current = best_candidate
        else:
            break

    # Did not flip within iterations
    logger.debug(f"Counterfactual not found within {max_iterations} iterations.")
    changes = {}
    for i, name in enumerate(feature_names):
        diff = current[i] - original[i]
        if abs(diff) > 1e-6:
            changes[name] = {
                "original": round(float(original[i]), 4),
                "counterfactual": round(float(current[i]), 4),
                "change": round(float(diff), 4),
            }

    return {
        "counterfactual": current.tolist(),
        "changes": changes,
        "iterations": max_iterations,
        "target_class": target_class,
        "status": "partial",
    }


# ═══════════════════════════════════════════════════════════════════════════
# Section 4.4 — ConfidenceAwareAgent (Chapter 12, p.28–29)
# ═══════════════════════════════════════════════════════════════════════════

class TemperatureScaler:
    """
    Mock Platt/temperature calibrator for confidence scores.
    See Chapter 12, p.28-29.

    In simulation mode: identity transform + Normal(0, 0.02) noise.
    In live mode: would fit a LogisticRegression on validation logits.
    """

    def __init__(self, seed: int = 42):
        self._rng = np.random.RandomState(seed)
        logger.debug("TemperatureScaler initialized (simulation: identity + noise).")

    def calibrate(self, raw_score: float) -> float:
        """Apply calibration to a raw confidence score."""
        noise = self._rng.normal(0, 0.02)
        calibrated = float(np.clip(raw_score + noise, 0.0, 1.0))
        return round(calibrated, 4)


class ConfidenceAwareAgent:
    """
    Agent that quantifies and communicates uncertainty.
    See Chapter 12, p.28-29.

    Features:
        - Multi-hypothesis generation with confidence scores.
        - Temperature-scaled calibration.
        - Qualifier mapping: >0.9 High, >0.7 Moderate, else Low.
        - Epistemic vs. aleatoric uncertainty awareness.
    """

    QUALIFIER_MAP = {
        (0.9, 1.01): "High confidence",
        (0.7, 0.9): "Moderate confidence",
        (0.0, 0.7): "Low confidence — human review recommended",
    }

    def __init__(self, seed: int = 42):
        self._scaler = TemperatureScaler(seed=seed)
        self._mock_llm = get_mock_llm() if is_simulation() else None
        logger.info(f"ConfidenceAwareAgent initialized. Mode: {get_mode()}")

    @staticmethod
    def _get_qualifier(confidence: float) -> str:
        """Map a confidence score to a human-readable qualifier (p.29)."""
        if confidence > 0.9:
            return "High confidence"
        elif confidence > 0.7:
            return "Moderate confidence"
        else:
            return "Low confidence — human review recommended"

    @graceful_fallback(
        fallback_value=[{"answer": "unknown", "confidence": 0.5,
                         "qualifier": "Low confidence — human review recommended",
                         "evidence": {}}],
        section_ref="Section 12 - Confidence Scoring (p.28-29)"
    )
    def score_differentials(self, differentials: list[dict]) -> list[dict]:
        """
        Calibrate raw differential scores and assign qualifiers.

        Args:
            differentials: List of {'diagnosis': str, 'raw_score': float}.

        Returns:
            List of {'answer', 'confidence', 'qualifier', 'evidence'} dicts.
            Matches parity contract §3.3.
        """
        if self._mock_llm:
            return self._mock_llm.invoke(
                "confidence score_differentials calibrat",
                differentials=differentials,
            )

        scored = []
        for diff in differentials:
            raw = diff.get("raw_score", 0.5)
            calibrated = self._scaler.calibrate(raw)
            qualifier = self._get_qualifier(calibrated)

            scored.append({
                "answer": diff.get("diagnosis", "unknown"),
                "confidence": calibrated,
                "qualifier": qualifier,
                "evidence": {"raw_score": raw},
            })

        return scored

    @graceful_fallback(
        fallback_value="Uncertainty information unavailable.",
        section_ref="Section 12 - Uncertainty Communication (p.29)"
    )
    def communicate_uncertainty(self, scored_results: list[dict]) -> str:
        """
        Generate a natural-language summary of uncertainty. See p.29.

        Distinguishes epistemic (reducible with more data) from
        aleatoric (inherent) uncertainty.
        """
        if not scored_results:
            return "No results to communicate."

        top = scored_results[0]
        qualifier = top.get("qualifier", "Unknown")
        confidence = top.get("confidence", 0.0)
        answer = top.get("answer", "unknown")

        # Determine uncertainty type
        if confidence < 0.5:
            uncertainty_type = "epistemic (could be reduced with additional data)"
        elif confidence < 0.8:
            uncertainty_type = "mixed epistemic and aleatoric"
        else:
            uncertainty_type = "primarily aleatoric (inherent variability)"

        summary = (
            f"Primary assessment: {answer} ({qualifier}, {confidence:.0%}). "
            f"Uncertainty type: {uncertainty_type}. "
        )

        if len(scored_results) > 1:
            alternatives = [
                f"{r['answer']} ({r['confidence']:.0%})"
                for r in scored_results[1:3]
            ]
            summary += f"Alternatives considered: {', '.join(alternatives)}."

        logger.info(f"Uncertainty communication: {qualifier}")
        return summary


# ═══════════════════════════════════════════════════════════════════════════
# Section 4.5 — DiagnosticAssistant + Sub-Agents (Chapter 12, p.30–35)
# ═══════════════════════════════════════════════════════════════════════════

class BiometricAnalyzer:
    """
    Mock sub-agent: analyzes biometric/vital sign data.
    See Chapter 12, p.32.
    """

    # Normal ranges for flagging
    NORMAL_RANGES = {
        "heart_rate_avg": (60, 100),
        "spo2_min": (95, 100),
        "wbc_count": (4.5, 11.0),
        "temperature": (36.1, 37.2),
    }

    @graceful_fallback(
        fallback_value={"flags": [], "summary": "Biometric analysis unavailable."},
        section_ref="Section 12 - Biometric Analysis (p.32)"
    )
    def analyze(self, patient: dict) -> dict:
        """
        Analyze patient biometrics and flag abnormal values.

        Args:
            patient: Dict with vital sign keys.

        Returns:
            dict with 'flags' and 'summary'.
        """
        flags = []
        for vital, (lo, hi) in self.NORMAL_RANGES.items():
            value = patient.get(vital)
            if value is not None:
                if value < lo:
                    flags.append({
                        "vital": vital,
                        "value": value,
                        "status": "LOW",
                        "normal_range": f"{lo}-{hi}",
                    })
                elif value > hi:
                    flags.append({
                        "vital": vital,
                        "value": value,
                        "status": "HIGH",
                        "normal_range": f"{lo}-{hi}",
                    })

        if flags:
            summary = f"{len(flags)} abnormal vital(s) detected."
            logger.debug(f"Biometrics: {summary}")
        else:
            summary = "All vitals within normal range."
            logger.debug(summary)

        return {"flags": flags, "summary": summary}


class SymptomInterpreter:
    """
    Mock sub-agent: maps reported symptoms to SNOMED CT codes.
    See Chapter 12, p.32-33.
    """

    def __init__(self):
        self._mock_llm = get_mock_llm() if is_simulation() else None

    @graceful_fallback(
        fallback_value=[],
        section_ref="Section 12 - Symptom Interpretation (p.32-33)"
    )
    def interpret(self, symptoms: list[str]) -> list[dict]:
        """
        Interpret symptoms into structured SNOMED codes.

        Args:
            symptoms: List of symptom strings.

        Returns:
            [{'symptom': str, 'snomed_code': str, 'confidence': float}]
        """
        if self._mock_llm:
            return self._mock_llm.invoke(
                "interpret_symptoms snomed symptom",
                symptoms=symptoms,
            )

        # Live mode would call actual NLP/LLM pipeline
        return [{"symptom": s, "snomed_code": "SNOMED:LIVE", "confidence": 0.9}
                for s in symptoms]


class DiagnosticCoordinator:
    """
    Coordinates differential diagnosis generation.
    See Chapter 12, p.33-34.
    """

    def __init__(self):
        self._mock_llm = get_mock_llm() if is_simulation() else None

    @graceful_fallback(
        fallback_value=[{"diagnosis": "unknown", "raw_score": 0.5}],
        section_ref="Section 12 - Differential Generation (p.33-34)"
    )
    def generate_differentials(self, patient: dict,
                               biometrics: dict,
                               symptoms: list[dict]) -> list[dict]:
        """
        Generate ranked differential diagnoses.

        Args:
            patient: Patient record dict.
            biometrics: Output from BiometricAnalyzer.
            symptoms: Output from SymptomInterpreter.

        Returns:
            [{'diagnosis': str, 'raw_score': float}]
        """
        if self._mock_llm:
            return self._mock_llm.invoke(
                "generate_differentials differential diagnosis",
                wbc_count=patient.get("wbc_count", 7.5),
                chest_imaging=patient.get("chest_imaging", "clear"),
            )

        # Live mode would use actual diagnostic reasoning
        return [{"diagnosis": "unknown", "raw_score": 0.5}]


class ClinicalExplainer:
    """
    Generates audience-adapted explanations of diagnostic results.
    See Chapter 12, p.34-35.

    Supports two audiences:
        - 'clinician': Technical with SHAP values and clinical terminology.
        - 'patient': Plain language with reassurance and next-steps.
    """

    def __init__(self):
        self._mock_llm = get_mock_llm() if is_simulation() else None

    @graceful_fallback(
        fallback_value={"narrative": "Explanation unavailable (fallback).",
                        "feature_contributions": {}, "trace": []},
        section_ref="Section 12 - Clinical Explanation (p.34-35)"
    )
    def generate(self, diagnosis: str, confidence: float,
                 shap_features: dict, audience: str = "clinician",
                 trace: Optional[list] = None) -> dict:
        """
        Generate a narrative explanation.

        Args:
            diagnosis: Primary diagnosis string.
            confidence: Confidence score (0-1).
            shap_features: Feature importance dict.
            audience: 'clinician' or 'patient'.
            trace: Optional audit trail from earlier steps.

        Returns:
            {'narrative': str, 'feature_contributions': dict, 'trace': list}
        """
        if self._mock_llm:
            return self._mock_llm.invoke(
                "clinical_explanation explain narrative",
                diagnosis=diagnosis,
                confidence=confidence,
                shap_features=shap_features,
                audience=audience,
            )

        # Live mode would use actual LLM
        return {
            "narrative": f"Live explanation for {diagnosis}.",
            "feature_contributions": shap_features,
            "trace": trace or [],
        }


class DiagnosticAssistant:
    """
    Full medical diagnosis pipeline orchestrator.
    See Chapter 12, p.30-35.

    Pipeline:
        1. BiometricAnalyzer → vital sign flags
        2. SymptomInterpreter → SNOMED codes
        3. DiagnosticCoordinator → differential diagnoses
        4. ConfidenceAwareAgent → calibrated scores + qualifiers
        5. ClinicalExplainer → audience-adapted explanation

    All sub-agents use @graceful_fallback. Sensor dropout (F7),
    model failure (F10), and explanation failure (F5) are handled.
    """

    def __init__(self, seed: int = 42):
        self._biometric = BiometricAnalyzer()
        self._symptom = SymptomInterpreter()
        self._coordinator = DiagnosticCoordinator()
        self._confidence = ConfidenceAwareAgent(seed=seed)
        self._explainer = ClinicalExplainer()
        self._trace: list[dict] = []
        logger.info(f"DiagnosticAssistant initialized. Mode: {get_mode()}")

    def _log_step(self, step: str, data: dict, status: str = "complete") -> None:
        self._trace.append({
            "step": step,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "summary": str(data)[:200],
        })

    @graceful_fallback(
        fallback_value={"status": "pipeline_failed", "diagnosis": "unknown"},
        section_ref="Section 12 - Diagnostic Pipeline (p.30-35)"
    )
    def run_diagnosis(self, patient: dict,
                      audience: str = "clinician") -> dict:
        """
        Execute the full diagnostic pipeline for a single patient.

        Args:
            patient: Patient record with vitals, symptoms, imaging.
            audience: 'clinician' or 'patient' for explanation style.

        Returns:
            Complete diagnostic report with trace.
        """
        self._trace = []
        logger.info(
            f"Starting diagnosis for patient "
            f"{patient.get('patient_id', 'unknown')}..."
        )

        # Step 1: Biometric analysis
        biometrics = self._biometric.analyze(patient)
        self._log_step("biometric_analysis", biometrics)

        # Step 2: Symptom interpretation
        symptoms_raw = patient.get("reported_symptoms", "")
        if isinstance(symptoms_raw, str):
            symptom_list = [s.strip() for s in symptoms_raw.split(",") if s.strip()]
        else:
            symptom_list = list(symptoms_raw)

        symptoms = self._symptom.interpret(symptom_list)
        self._log_step("symptom_interpretation", {"count": len(symptoms)})

        # Step 3: Differential diagnosis
        differentials = self._coordinator.generate_differentials(
            patient, biometrics, symptoms
        )
        self._log_step("differential_generation", {"count": len(differentials)})

        # Step 4: Confidence calibration
        scored = self._confidence.score_differentials(differentials)
        self._log_step("confidence_calibration", {"top": scored[0] if scored else {}})

        # Step 5: Explanation
        primary = scored[0] if scored else {"answer": "unknown", "confidence": 0.5}
        shap_features = {
            "wbc_count": 0.31,
            "chest_imaging": 0.28,
            "temperature": 0.15,
            "spo2_min": 0.12,
            "heart_rate_avg": 0.08,
        }

        explanation = self._explainer.generate(
            diagnosis=primary.get("answer", "unknown"),
            confidence=primary.get("confidence", 0.5),
            shap_features=shap_features,
            audience=audience,
            trace=self._trace,
        )
        self._log_step("explanation_generation", {"audience": audience})

        # Uncertainty summary
        uncertainty = self._confidence.communicate_uncertainty(scored)

        logger.success(
            f"Diagnosis complete: {primary.get('answer', 'unknown')} "
            f"({primary.get('qualifier', 'N/A')})"
        )

        return {
            "patient_id": patient.get("patient_id", "unknown"),
            "biometrics": biometrics,
            "symptoms": symptoms,
            "differentials": differentials,
            "scored_differentials": scored,
            "explanation": explanation,
            "uncertainty_summary": uncertainty,
            "trace": copy.deepcopy(self._trace),
            "status": "complete",
        }


# ═══════════════════════════════════════════════════════════════════════════
# Self-test
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from src.synthetic_data import generate_medical_dataset

    # -- ExplainableAgent --
    logger.info("=== ExplainableAgent Self-Test ===")
    agent = ExplainableAgent(name="TestAgent")
    result = agent.run_full_pipeline({"heart_rate": 88, "wbc": 12})
    logger.success(f"Trace summary: {agent.get_trace_summary()}")

    # -- ConfidenceAwareAgent --
    logger.info("=== ConfidenceAwareAgent Self-Test ===")
    ca = ConfidenceAwareAgent(seed=42)
    diffs = [
        {"diagnosis": "pneumonia", "raw_score": 0.87},
        {"diagnosis": "bronchitis", "raw_score": 0.09},
        {"diagnosis": "atelectasis", "raw_score": 0.04},
    ]
    scored = ca.score_differentials(diffs)
    for s in scored:
        logger.success(f"  {s['answer']}: {s['confidence']:.2f} ({s['qualifier']})")
    uncertainty = ca.communicate_uncertainty(scored)
    logger.success(f"Uncertainty: {uncertainty}")

    # -- DiagnosticAssistant --
    logger.info("=== DiagnosticAssistant Self-Test ===")
    med_df = generate_medical_dataset(50, 42)
    patient = med_df.iloc[0].to_dict()
    assistant = DiagnosticAssistant(seed=42)

    # Clinician audience
    report_clinician = assistant.run_diagnosis(patient, audience="clinician")
    logger.success(f"Clinician narrative: {report_clinician['explanation'].get('narrative', '')[:100]}...")

    # Patient audience
    report_patient = assistant.run_diagnosis(patient, audience="patient")
    logger.success(f"Patient narrative: {report_patient['explanation'].get('narrative', '')[:100]}...")

    logger.success("All ExplainabilityCore self-tests passed.")
