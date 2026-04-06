# src/ethical_core.py
# Author: Imran Ahmad
# Book: 30 Agents Every AI Engineer Must Build, Chapter 12
# Ref: The Ethical Reasoning Agent (p.3–23)
# Description: Complete ethical reasoning pipeline — deontic logic helpers,
#              value alignment framework, bias detection and mitigation,
#              EU AI Act compliance, and the FairHiringAgent case study.

from __future__ import annotations

import copy
import collections
from datetime import datetime, timezone
from typing import Any

from chapter12.utils import ColorLogger, graceful_fallback, is_simulation
from chapter12.mock_llm import MockLLM, _make_meta

logger = ColorLogger("EthicalCore")


# ═══════════════════════════════════════════════════════════════════════════
# §3.1  Deontic Logic Helpers
# Ref: Value Alignment Frameworks, p.5–7
# ═══════════════════════════════════════════════════════════════════════════

class DeonticOperator:
    """
    Formal deontic logic operators for ethical constraint evaluation.

    Implements the three modal operators (p.5–6):
        O(φ)  — Obligatory: agent must perform φ
        P(φ)  — Permitted: agent may perform φ
        F(φ)  — Forbidden: agent must not perform φ

    And three fundamental axioms (p.6):
        Axiom 1: O(φ) ⇔ F(¬φ)    — obligation ↔ prohibition of omission
        Axiom 2: P(φ) ⇔ ¬F(φ)    — permission ↔ absence of prohibition
        Axiom 3: O(φ→ψ) → (O(φ)→O(ψ))  — distribution of obligation
    """

    def __init__(self):
        self._obligations: set[str] = set()
        self._prohibitions: set[str] = set()
        self._implications: list[tuple[str, str]] = []
        logger.debug("DeonticOperator initialized.")

    def add_obligation(self, action: str) -> None:
        """Mark action as obligatory: O(φ). Ref: p.5"""
        self._obligations.add(action)
        # Axiom 1: O(φ) ⇔ F(¬φ) — omission becomes forbidden
        self._prohibitions.add(f"omit_{action}")

    def add_prohibition(self, action: str) -> None:
        """Mark action as forbidden: F(φ). Ref: p.5–6"""
        self._prohibitions.add(action)

    def add_implication(self, antecedent: str, consequent: str) -> None:
        """
        Register an obligation implication: O(φ→ψ).
        By Axiom 3 (p.6), if φ is obligatory then ψ becomes obligatory too.
        """
        self._implications.append((antecedent, consequent))

    def is_obligatory(self, action: str) -> bool:
        """Check if action is obligatory: O(φ). Ref: p.5"""
        return action in self._obligations

    def is_forbidden(self, action: str) -> bool:
        """Check if action is forbidden: F(φ). Ref: p.5–6"""
        return action in self._prohibitions

    def is_permitted(self, action: str) -> bool:
        """
        Check if action is permitted: P(φ) ⇔ ¬F(φ).
        Axiom 2 (p.6): permitted iff not forbidden.
        """
        return not self.is_forbidden(action)

    def propagate_obligations(self) -> None:
        """
        Apply Axiom 3 (p.6): distribution of obligation.
        O(φ→ψ) → (O(φ) → O(ψ))
        If φ is obligatory and φ→ψ is registered, make ψ obligatory.
        """
        changed = True
        while changed:
            changed = False
            for antecedent, consequent in self._implications:
                if antecedent in self._obligations and consequent not in self._obligations:
                    self.add_obligation(consequent)
                    changed = True

    def check_consistency(self, rule_set: set[str], candidate_action: str) -> dict:
        """
        Ethical Consistency Theorem (p.7):
        ∀a ∈ A: Consistent(E ∪ {a}) → P(a)

        Check whether adding *candidate_action* to *rule_set* creates any
        contradiction with the current prohibition set. If consistent,
        the action is permitted.

        Parameters
        ----------
        rule_set : set[str]
            Current ethical rule set E.
        candidate_action : str
            The action to evaluate.

        Returns
        -------
        dict
            {'is_consistent': bool, 'is_permitted': bool,
             'conflicting_rules': list[str]}
        """
        conflicts = []
        for rule in rule_set:
            if rule in self._prohibitions and rule == candidate_action:
                conflicts.append(rule)
            if candidate_action in self._prohibitions:
                conflicts.append(candidate_action)
                break

        is_consistent = len(conflicts) == 0
        return {
            "is_consistent": is_consistent,
            "is_permitted": is_consistent,
            "conflicting_rules": list(set(conflicts)),
            "candidate_action": candidate_action,
        }


# ═══════════════════════════════════════════════════════════════════════════
# §3.2  EthicalReasoningAgent
# Ref: p.8–9, extended cognitive loop with ethical checkpoint
# ═══════════════════════════════════════════════════════════════════════════

class ComplianceResult:
    """Result of a single principle validation. Ref: p.9"""

    def __init__(self, is_compliant: bool, explanation: str | None = None,
                 severity: str = "LOW"):
        self.is_compliant = is_compliant
        self.explanation = explanation
        self.severity = severity

    def to_dict(self) -> dict:
        return {
            "is_compliant": self.is_compliant,
            "explanation": self.explanation,
            "severity": self.severity,
        }


class _BasePrincipleChecker:
    """
    Base class for IEEE Ethically Aligned Design principle checkers.
    Each checker maintains an internal constraint set (p.9).
    """

    def __init__(self, name: str, violation_keywords: list[str]):
        self.name = name
        self._violation_keywords = [kw.lower() for kw in violation_keywords]

    def validate(self, proposed_action: str, context: dict) -> ComplianceResult:
        action_lower = proposed_action.lower()
        for kw in self._violation_keywords:
            if kw in action_lower:
                return ComplianceResult(
                    is_compliant=False,
                    explanation=f"{self.name}: action contains prohibited term '{kw}'",
                    severity="HIGH",
                )
        return ComplianceResult(is_compliant=True)

    def get_mitigation(self) -> dict:
        return {"strategy": "remove_violation", "principle": self.name}


class HumanRightsChecker(_BasePrincipleChecker):
    """Ref: IEEE Ethically Aligned Design — Human Rights, p.8"""
    def __init__(self):
        super().__init__("human_rights", [
            "share_medical_details", "bypass_consent", "expose_personal_data",
            "deny_access_based_on_race", "deny_access_based_on_gender",
        ])


class WellBeingAnalyzer(_BasePrincipleChecker):
    """Ref: IEEE Ethically Aligned Design — Well-being, p.8"""
    def __init__(self):
        super().__init__("well_being", [
            "disable_signals_school_zone", "reduce_safety_threshold",
            "ignore_emergency", "compromise_patient_safety",
        ])


class AccountabilityTracker(_BasePrincipleChecker):
    """Ref: IEEE Ethically Aligned Design — Accountability, p.8"""
    def __init__(self):
        super().__init__("accountability", [
            "disable_audit", "delete_logs", "bypass_oversight",
        ])


class TransparencyManager(_BasePrincipleChecker):
    """Ref: IEEE Ethically Aligned Design — Transparency, p.8"""
    def __init__(self):
        super().__init__("transparency", [
            "hide_decision_rationale", "suppress_explanation",
            "external_email_without_consent",
        ])


class MisuseDetector(_BasePrincipleChecker):
    """Ref: IEEE Ethically Aligned Design — Awareness of Misuse, p.8"""
    def __init__(self):
        super().__init__("awareness_misuse", [
            "weaponize_data", "enable_surveillance", "manipulate_user",
        ])


class AuditLogger:
    """
    Immutable audit log for ethical evaluations.
    Ref: p.8–9, accountability requirement.
    """

    def __init__(self):
        self._entries: list[dict] = []

    def record(self, action: str, violations: list, context: dict,
               timestamp: datetime | None = None) -> None:
        entry = {
            "timestamp": (timestamp or datetime.now(timezone.utc)).isoformat(),
            "action": action,
            "violations": violations,
            "context": context,
            "entry_id": len(self._entries),
        }
        self._entries.append(entry)

    def get_log(self) -> list[dict]:
        return copy.deepcopy(self._entries)

    def __len__(self) -> int:
        return len(self._entries)


class EthicalReasoningAgent:
    """
    Agent with embedded ethical evaluation in the decision loop.
    Validates every proposed action against IEEE ethical principles
    before execution.

    Ref: p.8–9, the extended cognitive loop with ethical checkpoint.
    """

    def __init__(self):
        self.principles = {
            "human_rights": HumanRightsChecker(),
            "well_being": WellBeingAnalyzer(),
            "accountability": AccountabilityTracker(),
            "transparency": TransparencyManager(),
            "awareness_misuse": MisuseDetector(),
        }
        self.audit_log = AuditLogger()
        self._mock = MockLLM() if is_simulation() else None
        logger.debug("EthicalReasoningAgent initialized with 5 principle checkers.")

    @graceful_fallback(
        fallback_value={"is_compliant": False, "violations": [], "severity": "UNKNOWN"},
        section_ref="Section 12 — EthicalReasoningAgent.evaluate_action() (p.8–9)",
    )
    def evaluate_action(self, proposed_action: str, context: dict | None = None) -> dict:
        """
        Validate a proposed action against all principles.

        Ref: p.8–9, evaluate_action() in the extended cognitive loop.
        """
        context = context or {}
        violations = []

        for principle, checker in self.principles.items():
            result = checker.validate(proposed_action, context)
            if not result.is_compliant:
                violations.append(
                    (principle, result.explanation, result.severity)
                )

        self.audit_log.record(
            action=proposed_action,
            violations=violations,
            context=context,
            timestamp=datetime.now(timezone.utc),
        )

        severity = "LOW"
        if violations:
            severity = max(v[2] for v in violations)

        if violations:
            logger.error(
                f"Action '{proposed_action[:60]}' has {len(violations)} "
                f"violation(s). Severity: {severity}. Routing to mitigation."
            )
            mitigated = self.mitigate(proposed_action, violations, context)
            return {
                "is_compliant": False,
                "violations": [(p, e, s) for p, e, s in violations],
                "severity": severity,
                "original_action": proposed_action,
                "mitigated_action": mitigated,
            }

        logger.success(f"Action '{proposed_action[:60]}' passed all ethical checks.")
        return {
            "is_compliant": True,
            "violations": [],
            "severity": "LOW",
            "original_action": proposed_action,
        }

    @graceful_fallback(
        fallback_value="[ESCALATED] Action requires human review.",
        section_ref="Section 12 — EthicalReasoningAgent.mitigate() (p.9)",
    )
    def mitigate(self, action: str, violations: list, context: dict) -> str:
        """
        Attempt automated mitigation, escalate if unresolvable.
        Ref: p.9, mitigation pathway.
        """
        mitigated = action
        for principle, explanation, severity in violations:
            strategy = self.principles[principle].get_mitigation()
            # Simple keyword removal as demonstration mitigation
            for kw in self.principles[principle]._violation_keywords:
                mitigated = mitigated.replace(kw, "[REDACTED]")

        # Re-validate
        remaining = []
        for principle, checker in self.principles.items():
            result = checker.validate(mitigated, context)
            if not result.is_compliant:
                remaining.append((principle, result.explanation, result.severity))

        if remaining:
            return self.escalate_to_human(action, remaining)

        logger.success(f"Mitigation successful. Cleaned action: '{mitigated[:60]}'")
        return mitigated

    def escalate_to_human(self, action: str, remaining_violations: list) -> str:
        """Escalate to human operator when automated mitigation fails. Ref: p.9"""
        logger.info(
            f"Escalating to human operator. {len(remaining_violations)} "
            f"unresolvable violation(s) for action: '{action[:60]}'"
        )
        return (
            f"[ESCALATED] Action requires human review. "
            f"Unresolved violations: {len(remaining_violations)}. "
            f"Details: {remaining_violations}"
        )


# ═══════════════════════════════════════════════════════════════════════════
# §3.3  EUCompliantAgent
# Ref: p.10–11, EU AI Act seven-requirement compliance control plane
# ═══════════════════════════════════════════════════════════════════════════

class _RequirementChecker:
    """Base checker for a single EU AI Act requirement."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._compliant = True
        self._evidence: str = "Default: compliant by design."

    def verify(self) -> dict:
        return {
            "requirement": self.name,
            "description": self.description,
            "compliant": self._compliant,
            "evidence": self._evidence,
        }

    def set_status(self, compliant: bool, evidence: str) -> None:
        self._compliant = compliant
        self._evidence = evidence


class EUCompliantAgent:
    """
    Agent with EU AI Act and GDPR compliance built in.

    Maps the seven EU AI Act requirements to dedicated checking components.
    Ref: p.10–11.
    """

    def __init__(self):
        self.requirements = {
            "human_oversight": _RequirementChecker(
                "Human Oversight",
                "Human-in-the-loop mechanisms for high-risk decisions",
            ),
            "technical_robustness": _RequirementChecker(
                "Technical Robustness",
                "Resilience to errors, faults, and adversarial attacks",
            ),
            "privacy_data_governance": _RequirementChecker(
                "Privacy & Data Governance",
                "Data minimization, consent management, GDPR compliance",
            ),
            "transparency": _RequirementChecker(
                "Transparency",
                "Decision explanation, audit trails, reasoning traces",
            ),
            "diversity_fairness": _RequirementChecker(
                "Diversity & Fairness",
                "Bias detection, fairness metrics, demographic parity",
            ),
            "societal_wellbeing": _RequirementChecker(
                "Societal Well-being",
                "Impact assessment, safety boundaries, stakeholder review",
            ),
            "accountability": _RequirementChecker(
                "Accountability",
                "Audit logging, incident response, governance documentation",
            ),
        }
        logger.debug("EUCompliantAgent initialized with 7 requirement checkers.")

    @graceful_fallback(
        fallback_value={"status": "UNKNOWN", "requirements": {}},
        section_ref="Section 12 — EUCompliantAgent.compliance_check() (p.10–11)",
    )
    def compliance_check(self) -> dict:
        """
        Verify compliance with all seven EU requirements.
        Returns a structured report suitable for release gates and audit.
        Ref: p.10–11.
        """
        report = {}
        all_compliant = True
        for req_key, checker in self.requirements.items():
            result = checker.verify()
            report[req_key] = result
            if not result["compliant"]:
                all_compliant = False

        status = "COMPLIANT" if all_compliant else "NON_COMPLIANT"
        summary = {
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_requirements": len(self.requirements),
            "compliant_count": sum(
                1 for r in report.values() if r["compliant"]
            ),
            "requirements": report,
        }

        if all_compliant:
            logger.success("EU AI Act compliance check: ALL 7 requirements met.")
        else:
            failing = [k for k, v in report.items() if not v["compliant"]]
            logger.error(
                f"EU AI Act compliance check: {len(failing)} requirement(s) failing: "
                f"{', '.join(failing)}"
            )

        return summary

    def set_requirement_status(self, requirement: str, compliant: bool,
                               evidence: str) -> None:
        """Update a specific requirement's compliance status."""
        if requirement in self.requirements:
            self.requirements[requirement].set_status(compliant, evidence)


# ═══════════════════════════════════════════════════════════════════════════
# §3.4  BiasDetector
# Ref: Bias detection and mitigation, p.16–17
# ═══════════════════════════════════════════════════════════════════════════

class DemographicParityMetric:
    """
    Demographic parity: equal positive outcome rates across groups.
    Ref: p.16
    """

    def compute(self, predictions: list[bool], sensitive_attrs: list[str],
                ground_truth: list[bool] | None = None) -> dict:
        groups: dict[str, list[bool]] = {}
        for pred, attr in zip(predictions, sensitive_attrs):
            groups.setdefault(attr, []).append(pred)

        rates = {g: sum(preds) / len(preds) if preds else 0.0
                 for g, preds in groups.items()}
        max_rate = max(rates.values()) if rates else 1.0
        min_rate = min(rates.values()) if rates else 0.0
        difference = round(max_rate - min_rate, 4)

        return {
            "metric": "demographic_parity",
            "group_rates": {g: round(r, 4) for g, r in rates.items()},
            "difference": difference,
        }


class EqualOpportunityMetric:
    """
    Equal opportunity: equal true-positive rates for qualified candidates.
    Ref: p.16
    """

    def compute(self, predictions: list[bool], sensitive_attrs: list[str],
                ground_truth: list[bool] | None = None) -> dict:
        if ground_truth is None:
            return {
                "metric": "equal_opportunity",
                "group_tpr": {},
                "difference": 0.0,
                "note": "Ground truth not provided; metric not computed.",
            }

        groups: dict[str, dict] = {}
        for pred, attr, truth in zip(predictions, sensitive_attrs, ground_truth):
            if attr not in groups:
                groups[attr] = {"tp": 0, "fn": 0}
            if truth:  # Only consider actually qualified
                if pred:
                    groups[attr]["tp"] += 1
                else:
                    groups[attr]["fn"] += 1

        tpr = {}
        for g, counts in groups.items():
            total = counts["tp"] + counts["fn"]
            tpr[g] = round(counts["tp"] / total, 4) if total > 0 else 0.0

        rates = list(tpr.values())
        difference = round(max(rates) - min(rates), 4) if rates else 0.0

        return {
            "metric": "equal_opportunity",
            "group_tpr": tpr,
            "difference": difference,
        }


class DisparateImpactMetric:
    """
    Disparate impact ratio: ratio of positive outcome rates.
    Uses the four-fifths rule (0.8 threshold) from U.S. EEOC. Ref: p.16
    """

    def compute(self, predictions: list[bool], sensitive_attrs: list[str],
                ground_truth: list[bool] | None = None) -> dict:
        groups: dict[str, list[bool]] = {}
        for pred, attr in zip(predictions, sensitive_attrs):
            groups.setdefault(attr, []).append(pred)

        rates = {g: sum(preds) / len(preds) if preds else 0.0
                 for g, preds in groups.items()}
        max_rate = max(rates.values()) if rates else 1.0
        min_rate = min(rates.values()) if rates else 0.0

        ratio = round(min_rate / max_rate, 4) if max_rate > 0 else 0.0

        return {
            "metric": "disparate_impact",
            "group_rates": {g: round(r, 4) for g, r in rates.items()},
            "ratio": ratio,
            "four_fifths_compliant": ratio >= 0.8,
        }


class BiasDetector:
    """
    Modular bias detection across protected groups.

    Three metrics:
        - DemographicParityMetric
        - EqualOpportunityMetric
        - DisparateImpactMetric

    assess_severity() applies the four-fifths rule (0.8 → HIGH)
    and 0.1 disparity threshold (→ MEDIUM). Ref: p.16–17
    """

    def __init__(self):
        self.metrics = {
            "demographic_parity": DemographicParityMetric(),
            "equal_opportunity": EqualOpportunityMetric(),
            "disparate_impact": DisparateImpactMetric(),
        }
        logger.debug("BiasDetector initialized with 3 metrics.")

    @graceful_fallback(
        fallback_value={"metrics": {}, "summary": "Fallback", "severity": "UNKNOWN",
                        "recommendations": []},
        section_ref="Section 12 — BiasDetector.analyze() (p.16–17)",
    )
    def analyze(self, predictions: list[bool], sensitive_attrs: list[str],
                ground_truth: list[bool] | None = None) -> dict:
        """
        Compute bias metrics across protected groups.
        Ref: p.16–17, BiasDetector.analyze()
        """
        results = {}
        for name, metric in self.metrics.items():
            results[name] = metric.compute(predictions, sensitive_attrs, ground_truth)

        return self.generate_report(results)

    def generate_report(self, results: dict) -> dict:
        """Produce a structured bias analysis report. Ref: p.17"""
        severity = self.assess_severity(results)
        summary = self._summarize(results, severity)
        recommendations = self._get_recommendations(results, severity)

        return {
            "metrics": results,
            "summary": summary,
            "severity": severity,
            "recommendations": recommendations,
        }

    def assess_severity(self, results: dict) -> str:
        """
        Classify bias severity for escalation decisions.
        Ref: p.17
            - disparate_impact ratio < 0.8  → HIGH (fails four-fifths rule)
            - demographic_parity diff > 0.1 → MEDIUM
            - otherwise                     → LOW
        """
        di = results.get("disparate_impact", {})
        dp = results.get("demographic_parity", {})

        if di.get("ratio", 1.0) < 0.8:
            return "HIGH"
        elif dp.get("difference", 0.0) > 0.1:
            return "MEDIUM"
        return "LOW"

    def _summarize(self, results: dict, severity: str) -> str:
        di_ratio = results.get("disparate_impact", {}).get("ratio", "N/A")
        dp_diff = results.get("demographic_parity", {}).get("difference", "N/A")
        return (
            f"Bias severity: {severity}. "
            f"Disparate impact ratio: {di_ratio}. "
            f"Demographic parity difference: {dp_diff}."
        )

    def _get_recommendations(self, results: dict, severity: str) -> list[str]:
        recs = []
        if severity == "HIGH":
            recs.append("Apply reweighting strategy to restore demographic balance.")
            recs.append("Review anonymization layer for proxy variable leakage.")
            recs.append("Consider threshold adjustment per group.")
        elif severity == "MEDIUM":
            recs.append("Monitor trends over next evaluation window.")
            recs.append("Audit feature correlations with protected attributes.")
        else:
            recs.append("Continue routine monitoring.")
        return recs


# ═══════════════════════════════════════════════════════════════════════════
# §3.5  BiasMonitoringPipeline
# Ref: p.17–19, streaming operational control loop
# ═══════════════════════════════════════════════════════════════════════════

class SlidingWindow:
    """Fixed-size sliding window for streaming bias analysis. Ref: p.18"""

    def __init__(self, size: int = 1000):
        self.size = size
        self.predictions: list[bool] = []
        self.demographics: list[str] = []
        self.ground_truth: list[bool] = []

    def add(self, prediction: bool, demographic: str,
            truth: bool | None = None) -> None:
        self.predictions.append(prediction)
        self.demographics.append(demographic)
        self.ground_truth.append(truth if truth is not None else prediction)
        # Trim to window size
        if len(self.predictions) > self.size:
            self.predictions.pop(0)
            self.demographics.pop(0)
            self.ground_truth.pop(0)

    def is_full(self) -> bool:
        return len(self.predictions) >= self.size

    def clear(self) -> None:
        self.predictions.clear()
        self.demographics.clear()
        self.ground_truth.clear()


class MockMetricsBackend:
    """Mock Prometheus/Datadog backend for simulation. Ref: p.18"""

    def __init__(self):
        self._gauges: dict[str, float] = {}

    def gauge(self, name: str, value: float) -> None:
        self._gauges[name] = value
        logger.debug(f"Metric emitted: {name} = {value:.4f}")

    def get_gauges(self) -> dict[str, float]:
        return dict(self._gauges)


class MockAlertConfig:
    """Mock alerting system for simulation. Ref: p.18–19"""

    def __init__(self):
        self._alerts: list[dict] = []

    def fire(self, level: str, message: str, runbook: str = "") -> None:
        alert = {
            "level": level,
            "message": message,
            "runbook": runbook,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._alerts.append(alert)
        logger.error(f"ALERT [{level.upper()}]: {message}")

    def get_alerts(self) -> list[dict]:
        return list(self._alerts)


class BiasMonitoringPipeline:
    """
    Real-time bias monitoring integrated with observability.

    Accumulates decisions in a sliding window, runs BiasDetector when
    the window is full, pushes metrics to the observability backend,
    and fires critical alerts when severity is HIGH.

    Ref: p.17–19, BiasMonitoringPipeline
    """

    def __init__(self, window_size: int = 100,
                 metrics_backend: MockMetricsBackend | None = None,
                 alert_config: MockAlertConfig | None = None):
        self.detector = BiasDetector()
        self.metrics = metrics_backend or MockMetricsBackend()
        self.alert_config = alert_config or MockAlertConfig()
        self.window = SlidingWindow(size=window_size)
        self._reports: list[dict] = []
        logger.debug(
            f"BiasMonitoringPipeline initialized (window={window_size})."
        )

    @graceful_fallback(
        fallback_value=None,
        section_ref="Section 12 — BiasMonitoringPipeline.on_decision() (p.17–19)",
    )
    def on_decision(self, decision: bool, demographic: str,
                    ground_truth: bool | None = None) -> dict | None:
        """
        Called after every agent decision for streaming analysis.
        Ref: p.18
        """
        self.window.add(decision, demographic, ground_truth)

        if self.window.is_full():
            report = self.detector.analyze(
                self.window.predictions,
                self.window.demographics,
                self.window.ground_truth,
            )

            # Emit metrics to observability platform
            dp_diff = report["metrics"]["demographic_parity"]["difference"]
            di_ratio = report["metrics"]["disparate_impact"]["ratio"]

            self.metrics.gauge("agent.fairness.demographic_parity", dp_diff)
            self.metrics.gauge("agent.fairness.disparate_impact", di_ratio)

            # Trigger alerts when thresholds are breached
            if report["severity"] == "HIGH":
                self.alert_config.fire(
                    level="critical",
                    message=(
                        f"Disparate impact ratio: {di_ratio:.3f} "
                        f"(below 0.8 threshold)"
                    ),
                    runbook="https://runbooks.internal/bias-response",
                )

            self._reports.append(report)
            self.window.clear()
            return report

        return None

    def get_reports(self) -> list[dict]:
        return list(self._reports)


# ═══════════════════════════════════════════════════════════════════════════
# §3.6  FairHiringAgent + FairnessEnforcer
# Ref: Case Study — HR Assistant with Fairness Constraints, p.20–23
# ═══════════════════════════════════════════════════════════════════════════

class ResumeAnalyzer:
    """
    Skills-matching evaluation for pre-anonymized resumes.
    Returns a numeric score in [0, 1] with an explanation map.
    Ref: p.20
    """

    def __init__(self):
        self._mock = MockLLM()

    @graceful_fallback(
        fallback_value={"score": 0.5, "explanation_map": {}, "source": "fallback"},
        section_ref="Section 12 — ResumeAnalyzer.score() (p.20–21)",
    )
    def score(self, anonymized_resume: dict,
              job_requirements: dict) -> dict:
        """Score a resume against job requirements. Ref: p.20–21"""
        return self._mock.invoke("resume_scoring", {
            "skills": anonymized_resume.get("skills", []),
            "job_requirements": job_requirements,
            "years_experience": anonymized_resume.get("years_experience", 0),
        })

    def remove_fields(self, resume: dict, sensitive_fields: list[str]) -> dict:
        """Remove sensitive fields from a resume dict. Ref: p.21"""
        cleaned = copy.deepcopy(resume)
        for field in sensitive_fields:
            cleaned.pop(field, None)
        return cleaned


class FairnessEnforcer:
    """
    Three mitigation strategies for bias correction.
    Ref: p.21–22, FairnessEnforcer

    Strategies:
        - reweighting: adjust feature influence
        - threshold_adjustment: per-group decision boundaries
        - representation_learning: decorrelate protected attributes
    """

    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.strategies = {
            "reweighting": self._apply_reweighting,
            "threshold_adjustment": self._apply_threshold_adjustment,
            "representation_learning": self._apply_representation_learning,
        }

    @graceful_fallback(
        fallback_value={"corrected_score": 0.5, "strategy_used": "fallback",
                        "audit_entry": {}},
        section_ref="Section 12 — FairnessEnforcer.mitigate() (p.21–22)",
    )
    def mitigate(self, evaluation: dict, bias_report: dict) -> dict:
        """
        Apply appropriate bias mitigation strategies.
        Ref: p.21–22
        """
        severity = bias_report.get("severity", "LOW")
        original_score = evaluation.get("score", evaluation.get("raw_score", 0.5))

        if severity == "HIGH":
            strategy_name = "reweighting"
        elif severity == "MEDIUM":
            strategy_name = "threshold_adjustment"
        else:
            strategy_name = "representation_learning"

        strategy_fn = self.strategies[strategy_name]
        corrected_score = strategy_fn(original_score, bias_report)

        audit_entry = {
            "original_score": original_score,
            "corrected_score": corrected_score,
            "strategy_used": strategy_name,
            "severity": severity,
            "di_ratio_before": bias_report.get("metrics", {}).get(
                "disparate_impact", {}
            ).get("ratio", "N/A"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        logger.success(
            f"FairnessEnforcer applied '{strategy_name}': "
            f"{original_score:.4f} → {corrected_score:.4f}"
        )

        return {
            "corrected_score": corrected_score,
            "strategy_used": strategy_name,
            "audit_entry": audit_entry,
        }

    def _apply_reweighting(self, score: float, bias_report: dict) -> float:
        """Reweighting: boost underrepresented group scores. Ref: p.21"""
        boost = 0.05  # Calibrated to restore DI from ~0.73 to >=0.80
        return round(min(1.0, score + boost), 4)

    def _apply_threshold_adjustment(self, score: float,
                                     bias_report: dict) -> float:
        """Threshold adjustment: lower decision boundary for affected group."""
        adjustment = 0.03
        return round(min(1.0, score + adjustment), 4)

    def _apply_representation_learning(self, score: float,
                                        bias_report: dict) -> float:
        """Representation learning: decorrelate protected attributes."""
        return round(score, 4)  # Identity in simulation


class FairHiringAgent:
    """
    Resume screening agent with three-layer fairness architecture.
    Implements anonymization, bias detection, and enforcement.

    Ref: p.20–23, FairHiringAgent case study.

    Operates in Regime 2 of the Impossibility Theorem (p.12–13):
    prioritizes demographic parity via the four-fifths rule threshold.
    """

    def __init__(self, fairness_threshold: float = 0.8):
        self.resume_analyzer = ResumeAnalyzer()
        self.bias_detector = BiasDetector()
        self.fairness_enforcer = FairnessEnforcer(threshold=fairness_threshold)
        self.audit_logger = AuditLogger()
        self.threshold = fairness_threshold
        self._batch_evaluations: list[dict] = []
        self._batch_demographics: list[str] = []
        logger.debug(
            f"FairHiringAgent initialized (threshold={fairness_threshold})."
        )

    @graceful_fallback(
        fallback_value={"score": 0.5, "bias_report": None, "mitigated": False},
        section_ref="Section 12 — FairHiringAgent.evaluate_candidate() (p.20–21)",
    )
    def evaluate_candidate(self, resume: dict,
                           job_requirements: dict) -> dict:
        """
        Evaluate a candidate with integrated fairness checks.
        Three-layer architecture: anonymize → score → detect bias → mitigate.

        Ref: p.20–21
        """
        # Layer 1: Anonymize sensitive information
        anonymized = self.anonymize(resume)

        # Layer 2: Perform skills-based evaluation
        evaluation = self.resume_analyzer.score(anonymized, job_requirements)
        score = evaluation.get("score", 0.5)

        result = {
            "candidate_id": resume.get("candidate_id", "unknown"),
            "score": score,
            "explanation_map": evaluation.get("explanation_map", {}),
            "anonymized_fields_removed": self._sensitive_fields(),
            "bias_report": None,
            "mitigated": False,
        }

        return result

    def evaluate_batch(self, candidates: list[dict],
                       job_requirements: dict) -> dict:
        """
        Evaluate a batch of candidates and run bias detection across
        the full batch. Applies mitigation when bias is detected.

        Ref: p.20–23, complete pipeline.
        """
        evaluations = []
        demographics = []

        for resume in candidates:
            eval_result = self.evaluate_candidate(resume, job_requirements)
            evaluations.append(eval_result)
            demographics.append(resume.get("gender", "unknown"))

        # Layer 3: Check for bias across current batch
        predictions = [e["score"] >= 0.65 for e in evaluations]
        ground_truth = [c.get("qualified", True) for c in candidates]

        bias_report = self.bias_detector.analyze(
            predictions, demographics, ground_truth
        )

        mitigated_evaluations = evaluations
        if bias_report["severity"] in ("HIGH", "MEDIUM"):
            logger.info(
                f"Bias detected (severity={bias_report['severity']}). "
                f"Applying mitigation..."
            )
            mitigated_evaluations = self._apply_batch_mitigation(
                evaluations, candidates, bias_report
            )

        # Log
        self.audit_logger.record(
            action="batch_evaluation",
            violations=[("bias", bias_report["summary"], bias_report["severity"])]
            if bias_report["severity"] != "LOW" else [],
            context={
                "batch_size": len(candidates),
                "severity": bias_report["severity"],
            },
        )

        return {
            "evaluations": mitigated_evaluations,
            "bias_report": bias_report,
            "batch_size": len(candidates),
        }

    def _apply_batch_mitigation(self, evaluations: list[dict],
                                 candidates: list[dict],
                                 bias_report: dict) -> list[dict]:
        """Apply mitigation to the affected group in the batch."""
        mitigated = []
        for eval_result, candidate in zip(evaluations, candidates):
            gender = candidate.get("gender", "unknown")
            # Apply mitigation to the disadvantaged group
            if gender == "female" and bias_report["severity"] in ("HIGH", "MEDIUM"):
                correction = self.fairness_enforcer.mitigate(
                    {"score": eval_result["score"]}, bias_report
                )
                new_eval = dict(eval_result)
                new_eval["original_score"] = eval_result["score"]
                new_eval["score"] = correction["corrected_score"]
                new_eval["mitigated"] = True
                new_eval["mitigation_strategy"] = correction["strategy_used"]
                mitigated.append(new_eval)
            else:
                mitigated.append(eval_result)
        return mitigated

    def anonymize(self, resume: dict) -> dict:
        """
        Remove fields that could introduce demographic bias.
        Ref: p.21
        """
        return self.resume_analyzer.remove_fields(
            resume, self._sensitive_fields()
        )

    @staticmethod
    def _sensitive_fields() -> list[str]:
        return [
            "name", "gender", "age", "nationality",
            "photo", "address", "education_institution",
        ]
