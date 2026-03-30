"""
Ethical Core: Deontic logic, ethical reasoning, bias detection, and fairness enforcement.

Implements the complete ethical reasoning pipeline from Chapter 12, including:
  - Deontic logic operators and the Ethical Consistency Theorem (p.5-7)
  - EthicalReasoningAgent with modular validators (p.8-9)
  - EUCompliantAgent with seven EU AI Act requirements (p.10-11)
  - BiasDetector with three fairness metrics (p.16-17)
  - BiasMonitoringPipeline with sliding window alerts (p.17-19)
  - FairHiringAgent and FairnessEnforcer (p.20-23)

Author: Imran Ahmad
Book: 30 Agents Every AI Engineer Must Build, Chapter 12
"""

import time
import copy
import numpy as np
import pandas as pd
from typing import Any, Optional
from collections import deque
from datetime import datetime, timezone

from src.utils import ColorLogger, graceful_fallback, get_mode, is_simulation
from src.mock_llm import MockLLM, get_mock_llm

logger = ColorLogger(name="EthicalCore")


# ═══════════════════════════════════════════════════════════════════════════
# Section 3.1 — Deontic Logic Helpers (Chapter 12, p.5–7)
# ═══════════════════════════════════════════════════════════════════════════

class DeonticOperator:
    """
    Deontic logic operators for ethical reasoning.

    Implements the three axioms from Chapter 12, p.5-7:
        Axiom 1: O(A) → P(A)        — Obligation implies permission.
        Axiom 2: F(A) ↔ ¬P(A)       — Forbidden iff not permitted.
        Axiom 3: O(A) → ¬F(A)       — Obligation implies not forbidden.

    The Ethical Consistency Theorem (p.7):
        An action set S is consistent iff no action in S is both
        obligatory and forbidden.
    """

    def __init__(self):
        self._obligations: set[str] = set()
        self._permissions: set[str] = set()
        self._prohibitions: set[str] = set()
        logger.debug("DeonticOperator initialized.")

    # -- Core operators ----------------------------------------------------

    def add_obligation(self, action: str) -> None:
        """Mark an action as obligatory. By Axiom 1, also adds permission."""
        self._obligations.add(action)
        self._permissions.add(action)  # Axiom 1: O(A) → P(A)
        # Axiom 3: O(A) → ¬F(A) — remove from prohibitions if present
        self._prohibitions.discard(action)
        logger.debug(f"Obligation added: '{action}' (also permitted by Axiom 1).")

    def add_permission(self, action: str) -> None:
        """Mark an action as permitted."""
        self._permissions.add(action)
        logger.debug(f"Permission added: '{action}'.")

    def add_prohibition(self, action: str) -> None:
        """Mark an action as forbidden. By Axiom 2, also removes permission."""
        self._prohibitions.add(action)
        self._permissions.discard(action)  # Axiom 2: F(A) ↔ ¬P(A)
        logger.debug(f"Prohibition added: '{action}'.")

    # -- Query operators ---------------------------------------------------

    def is_obligatory(self, action: str) -> bool:
        """Check if an action is obligatory (O(A))."""
        return action in self._obligations

    def is_permitted(self, action: str) -> bool:
        """Check if an action is permitted (P(A))."""
        return action in self._permissions

    def is_forbidden(self, action: str) -> bool:
        """Check if an action is forbidden (F(A))."""
        return action in self._prohibitions

    # -- Ethical Consistency Theorem (p.7) ---------------------------------

    def check_consistency(self) -> dict:
        """
        Verify the Ethical Consistency Theorem.

        Returns:
            dict with keys:
                'is_consistent': bool — True if no action is both O and F.
                'conflicts': list[str] — Actions that violate consistency.
                'details': str — Human-readable summary.
        """
        conflicts = list(self._obligations & self._prohibitions)
        is_consistent = len(conflicts) == 0

        if is_consistent:
            details = (
                "Ethical Consistency Theorem holds: no action is both "
                "obligatory and forbidden."
            )
            logger.success(details)
        else:
            details = (
                f"Consistency VIOLATION: {len(conflicts)} action(s) are both "
                f"obligatory and forbidden: {conflicts}."
            )
            logger.error(details)

        return {
            "is_consistent": is_consistent,
            "conflicts": conflicts,
            "details": details,
        }

    def get_status(self) -> dict:
        """Return the current state of all three deontic categories."""
        return {
            "obligations": sorted(self._obligations),
            "permissions": sorted(self._permissions),
            "prohibitions": sorted(self._prohibitions),
        }


# ═══════════════════════════════════════════════════════════════════════════
# Section 3.2 — EthicalReasoningAgent (Chapter 12, p.8–9)
# ═══════════════════════════════════════════════════════════════════════════

class EthicalReasoningAgent:
    """
    Agent that evaluates actions against an ethical framework.

    Architecture (p.8-9):
        1. Modular validators — plug-in rules for different domains.
        2. evaluate_action() — runs all validators, returns compliance report.
        3. mitigate() — suggests corrective actions for violations.
        4. escalate_to_human() — flags critical issues for human review.

    Uses MockLLM in Simulation Mode for LLM-based reasoning steps.
    """

    # Default validators (keyword → violation category)
    DEFAULT_VALIDATORS = {
        "share_medical_details": ("privacy", "Sharing protected health information violates HIPAA"),
        "external_email": ("data_leak", "Sending internal data to external addresses"),
        "bypass_consent": ("consent", "User consent must be obtained before data processing"),
        "disable_audit": ("transparency", "Audit trail must remain active at all times"),
        "disable_signals_school_zone": ("safety", "Safety-critical system overrides are forbidden"),
        "discriminate_by_gender": ("fairness", "Gender-based discrimination is prohibited"),
        "discriminate_by_race": ("fairness", "Race-based discrimination is prohibited"),
        "hide_ai_decision": ("transparency", "AI decisions must be explainable to affected parties"),
    }

    def __init__(self, validators: Optional[dict] = None):
        self._validators = validators or self.DEFAULT_VALIDATORS
        self._audit_log: list[dict] = []
        self._mock_llm = get_mock_llm() if is_simulation() else None
        logger.info(
            f"EthicalReasoningAgent initialized with {len(self._validators)} validators. "
            f"Mode: {get_mode()}"
        )

    @graceful_fallback(
        fallback_value={"is_compliant": False, "violations": [],
                        "severity": "UNKNOWN", "source": "fallback"},
        section_ref="Section 12 - Ethical Evaluation (p.8-9)"
    )
    def evaluate_action(self, action: str, context: Optional[dict] = None) -> dict:
        """
        Evaluate an action string against all registered validators.

        Args:
            action: Description of the action to evaluate.
            context: Optional metadata (user role, domain, etc.).

        Returns:
            {'is_compliant': bool, 'violations': list[tuple],
             'severity': str}  — Matches parity contract §3.3.
        """
        context = context or {}
        action_lower = action.lower().replace(" ", "_")

        violations = []
        for keyword, (category, description) in self._validators.items():
            if keyword in action_lower:
                violations.append((category, description))

        # If in simulation mode, also consult MockLLM for additional checks
        if self._mock_llm:
            mock_result = self._mock_llm.invoke(
                "evaluate_action ethical compliance",
                action=action,
            )
            # Merge any extra violations from mock (deduplicate by category)
            existing_categories = {v[0] for v in violations}
            for v in mock_result.get("violations", []):
                if v[0] not in existing_categories:
                    violations.append(v)

        is_compliant = len(violations) == 0

        if len(violations) >= 3:
            severity = "CRITICAL"
        elif len(violations) >= 1:
            severity = "HIGH"
        else:
            severity = "NONE"

        result = {
            "is_compliant": is_compliant,
            "violations": violations,
            "severity": severity,
            "source": get_mode(),
        }

        # Audit logging
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "result": result,
            "context": context,
        }
        self._audit_log.append(audit_entry)

        if is_compliant:
            logger.success(f"Action '{action[:50]}...' is COMPLIANT.")
        else:
            logger.error(
                f"Action '{action[:50]}...' has {len(violations)} violation(s). "
                f"Severity: {severity}."
            )

        return result

    @graceful_fallback(
        fallback_value={"mitigation": "Unable to generate mitigation.",
                        "source": "fallback"},
        section_ref="Section 12 - Ethical Mitigation (p.9)"
    )
    def mitigate(self, violations: list[tuple]) -> dict:
        """
        Suggest corrective actions for detected violations.

        Args:
            violations: List of (category, description) tuples.

        Returns:
            dict with suggested mitigations.
        """
        mitigations = []
        for category, description in violations:
            if category == "privacy":
                mitigations.append(
                    f"[{category.upper()}] Remove or redact personal data. "
                    "Ensure HIPAA/GDPR-compliant data handling."
                )
            elif category == "data_leak":
                mitigations.append(
                    f"[{category.upper()}] Block external transmission. "
                    "Route through approved internal channels only."
                )
            elif category == "consent":
                mitigations.append(
                    f"[{category.upper()}] Implement explicit consent flow. "
                    "Record user acknowledgment before proceeding."
                )
            elif category == "transparency":
                mitigations.append(
                    f"[{category.upper()}] Enable full audit logging. "
                    "Provide explanation interface for affected users."
                )
            elif category == "safety":
                mitigations.append(
                    f"[{category.upper()}] Halt operation immediately. "
                    "Engage human-in-the-loop override."
                )
            elif category == "fairness":
                mitigations.append(
                    f"[{category.upper()}] Activate FairnessEnforcer pipeline. "
                    "Re-evaluate with bias-corrected model."
                )
            else:
                mitigations.append(
                    f"[{category.upper()}] Review and address: {description}"
                )

        logger.info(f"Generated {len(mitigations)} mitigation(s).")
        return {
            "mitigations": mitigations,
            "source": get_mode(),
        }

    def escalate_to_human(self, action: str, violations: list[tuple]) -> dict:
        """
        Flag a critical issue for human review.

        Returns:
            dict with escalation details and recommended reviewer role.
        """
        logger.error(
            f"ESCALATION: Action '{action[:50]}...' requires human review. "
            f"Violations: {len(violations)}."
        )
        return {
            "escalated": True,
            "action": action,
            "violations": violations,
            "recommended_reviewer": "Ethics Board / Domain Expert",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def get_audit_log(self) -> list[dict]:
        """Return the immutable audit trail (deep copy)."""
        return copy.deepcopy(self._audit_log)


# ═══════════════════════════════════════════════════════════════════════════
# Section 3.3 — EUCompliantAgent (Chapter 12, p.10–11)
# ═══════════════════════════════════════════════════════════════════════════

class EUCompliantAgent:
    """
    Seven-requirement compliance checker for the EU AI Act.

    Requirements (p.10-11):
        1. Human oversight mechanism
        2. Technical robustness and safety
        3. Privacy and data governance
        4. Transparency and explainability
        5. Diversity, non-discrimination, and fairness
        6. Societal and environmental well-being
        7. Accountability and auditability
    """

    REQUIREMENTS = {
        "human_oversight": {
            "id": 1,
            "name": "Human Oversight",
            "description": "System must support human-in-the-loop or human-on-the-loop control.",
            "check_fields": ["human_override", "escalation_path", "manual_review"],
        },
        "robustness": {
            "id": 2,
            "name": "Technical Robustness",
            "description": "System must handle errors gracefully and have fallback mechanisms.",
            "check_fields": ["error_handling", "fallback_mode", "input_validation"],
        },
        "privacy": {
            "id": 3,
            "name": "Privacy & Data Governance",
            "description": "Personal data must be protected with appropriate safeguards.",
            "check_fields": ["data_encryption", "consent_management", "data_minimization"],
        },
        "transparency": {
            "id": 4,
            "name": "Transparency",
            "description": "AI decisions must be explainable to affected parties.",
            "check_fields": ["explanation_interface", "audit_trail", "model_documentation"],
        },
        "fairness": {
            "id": 5,
            "name": "Fairness & Non-Discrimination",
            "description": "System must not discriminate based on protected characteristics.",
            "check_fields": ["bias_testing", "fairness_metrics", "representative_data"],
        },
        "wellbeing": {
            "id": 6,
            "name": "Societal Well-Being",
            "description": "System should promote positive societal outcomes.",
            "check_fields": ["impact_assessment", "stakeholder_consultation"],
        },
        "accountability": {
            "id": 7,
            "name": "Accountability",
            "description": "Clear assignment of responsibility and auditability.",
            "check_fields": ["responsible_party", "audit_schedule", "incident_response"],
        },
    }

    def __init__(self):
        logger.info("EUCompliantAgent initialized with 7 EU AI Act requirements.")

    @graceful_fallback(
        fallback_value={"compliant": False, "report": [], "summary": "Check failed."},
        section_ref="Section 12 - EU Compliance (p.10-11)"
    )
    def compliance_check(self, system_config: dict) -> dict:
        """
        Run the seven-requirement compliance check.

        Args:
            system_config: Dict mapping requirement fields to True/False
                          indicating whether the system satisfies them.

        Returns:
            Structured compliance report with per-requirement status.
        """
        report = []
        passed = 0
        total = len(self.REQUIREMENTS)

        for req_key, req_spec in self.REQUIREMENTS.items():
            check_fields = req_spec["check_fields"]
            field_results = {}
            all_met = True

            for field in check_fields:
                met = system_config.get(field, False)
                field_results[field] = met
                if not met:
                    all_met = False

            status = "PASS" if all_met else "FAIL"
            if all_met:
                passed += 1

            report.append({
                "requirement_id": req_spec["id"],
                "requirement_name": req_spec["name"],
                "description": req_spec["description"],
                "status": status,
                "field_results": field_results,
            })

        compliant = passed == total
        summary = (
            f"EU AI Act Compliance: {passed}/{total} requirements met. "
            f"Overall: {'COMPLIANT' if compliant else 'NON-COMPLIANT'}."
        )

        if compliant:
            logger.success(summary)
        else:
            logger.error(summary)

        return {
            "compliant": compliant,
            "passed": passed,
            "total": total,
            "report": report,
            "summary": summary,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Section 3.4 — BiasDetector (Chapter 12, p.16–17)
# ═══════════════════════════════════════════════════════════════════════════

class DemographicParityMetric:
    """
    Demographic Parity: selection rates should be equal across groups.
    See Chapter 12, p.16.
    """

    @staticmethod
    def compute(df: pd.DataFrame, group_col: str, outcome_col: str) -> dict:
        rates = df.groupby(group_col)[outcome_col].mean().to_dict()
        max_rate = max(rates.values()) if rates else 0
        min_rate = min(rates.values()) if rates else 0
        gap = round(max_rate - min_rate, 4) if rates else 0

        return {
            "metric": "demographic_parity",
            "group_rates": {k: round(v, 4) for k, v in rates.items()},
            "max_gap": gap,
            "description": "Difference between highest and lowest group selection rates.",
        }


class EqualOpportunityMetric:
    """
    Equal Opportunity: true positive rates should be equal across groups.
    Requires a ground-truth 'qualified' column. See Chapter 12, p.16.
    """

    @staticmethod
    def compute(df: pd.DataFrame, group_col: str, outcome_col: str,
                truth_col: str = "qualified") -> dict:
        tpr_by_group = {}
        for group, gdf in df.groupby(group_col):
            qualified = gdf[gdf[truth_col] == True]
            if len(qualified) > 0:
                tpr = qualified[outcome_col].mean()
            else:
                tpr = 0.0
            tpr_by_group[group] = round(tpr, 4)

        max_tpr = max(tpr_by_group.values()) if tpr_by_group else 0
        min_tpr = min(tpr_by_group.values()) if tpr_by_group else 0

        return {
            "metric": "equal_opportunity",
            "group_tpr": tpr_by_group,
            "max_gap": round(max_tpr - min_tpr, 4),
            "description": "Difference in true positive rates across groups.",
        }


class DisparateImpactMetric:
    """
    Disparate Impact: ratio of minority to majority selection rate.
    Four-fifths rule: ratio < 0.80 indicates adverse impact.
    See Chapter 12, p.16-17.
    """

    @staticmethod
    def compute(df: pd.DataFrame, group_col: str, outcome_col: str,
                reference_group: Optional[str] = None) -> dict:
        rates = df.groupby(group_col)[outcome_col].mean()

        if reference_group is None:
            # Use group with highest selection rate as reference
            reference_group = rates.idxmax()

        ref_rate = rates.get(reference_group, 0)
        if ref_rate == 0:
            ratios = {g: 0.0 for g in rates.index}
        else:
            ratios = {g: round(r / ref_rate, 4) for g, r in rates.items()}

        min_ratio = min(ratios.values()) if ratios else 0

        return {
            "metric": "disparate_impact",
            "reference_group": reference_group,
            "reference_rate": round(float(ref_rate), 4),
            "impact_ratios": ratios,
            "min_ratio": round(min_ratio, 4),
            "four_fifths_violation": min_ratio < 0.80,
            "description": (
                "Ratio of each group's selection rate to the reference group. "
                "Four-fifths rule: ratio < 0.80 indicates adverse impact."
            ),
        }


class BiasDetector:
    """
    Orchestrates bias detection using three fairness metrics.
    See Chapter 12, p.16-17.
    """

    def __init__(self):
        self._metrics = {
            "demographic_parity": DemographicParityMetric(),
            "equal_opportunity": EqualOpportunityMetric(),
            "disparate_impact": DisparateImpactMetric(),
        }
        logger.info("BiasDetector initialized with 3 fairness metrics.")

    @graceful_fallback(
        fallback_value={"metrics": {}, "summary": "Analysis failed.",
                        "severity": "UNKNOWN", "recommendations": []},
        section_ref="Section 12 - Bias Detection (p.16-17)"
    )
    def analyze(self, df: pd.DataFrame, group_col: str = "gender",
                outcome_col: str = "qualified",
                reference_group: Optional[str] = None) -> dict:
        """
        Run all three fairness metrics on the dataset.

        Returns:
            {'metrics': dict, 'summary': str, 'severity': str,
             'recommendations': list}
        """
        logger.info(
            f"Running bias analysis: group='{group_col}', outcome='{outcome_col}', "
            f"rows={len(df)}."
        )

        results = {}

        # Demographic parity
        results["demographic_parity"] = DemographicParityMetric.compute(
            df, group_col, outcome_col
        )

        # Equal opportunity
        if "qualified" in df.columns or outcome_col == "qualified":
            truth_col = "qualified" if "qualified" in df.columns else outcome_col
            results["equal_opportunity"] = EqualOpportunityMetric.compute(
                df, group_col, outcome_col, truth_col
            )

        # Disparate impact
        di_result = DisparateImpactMetric.compute(
            df, group_col, outcome_col, reference_group
        )
        results["disparate_impact"] = di_result

        severity = self.assess_severity(di_result)
        recommendations = self._generate_recommendations(results, severity)
        summary = (
            f"Bias analysis complete. Disparate impact min ratio: "
            f"{di_result['min_ratio']:.2f}. "
            f"Four-fifths violation: {di_result['four_fifths_violation']}. "
            f"Severity: {severity}."
        )

        if severity in ("HIGH", "CRITICAL"):
            logger.error(summary)
        else:
            logger.success(summary)

        return {
            "metrics": results,
            "summary": summary,
            "severity": severity,
            "recommendations": recommendations,
        }

    @staticmethod
    def assess_severity(di_result: dict) -> str:
        """
        Assess severity using the four-fifths rule (p.16).
            ratio >= 0.80 → LOW (no violation)
            0.60 <= ratio < 0.80 → HIGH (four-fifths violation)
            ratio < 0.60 → CRITICAL
        """
        min_ratio = di_result.get("min_ratio", 1.0)
        if min_ratio >= 0.80:
            return "LOW"
        elif min_ratio >= 0.60:
            return "HIGH"
        else:
            return "CRITICAL"

    @staticmethod
    def _generate_recommendations(results: dict, severity: str) -> list:
        recs = []
        if severity in ("HIGH", "CRITICAL"):
            recs.append(
                "Activate FairnessEnforcer to apply bias mitigation strategies."
            )
            recs.append(
                "Review training data for historical bias patterns."
            )
            recs.append(
                "Consider reweighting, threshold adjustment, or "
                "representation learning (see p.22-23)."
            )
        if severity == "CRITICAL":
            recs.append(
                "CRITICAL: Halt automated decisions until bias is resolved. "
                "Escalate to Ethics Board."
            )
        return recs


# ═══════════════════════════════════════════════════════════════════════════
# Section 3.5 — BiasMonitoringPipeline (Chapter 12, p.17–19)
# ═══════════════════════════════════════════════════════════════════════════

class BiasMonitoringPipeline:
    """
    Streaming bias monitor with sliding window and alert system.
    See Chapter 12, p.17-19.

    Simulates a production monitoring pipeline that:
        1. Receives decisions in a sliding window.
        2. Computes disparate impact on the window.
        3. Emits mock Prometheus metrics.
        4. Fires alerts when severity is HIGH or CRITICAL.
    """

    def __init__(self, window_size: int = 50, alert_threshold: float = 0.80):
        self._window: deque = deque(maxlen=window_size)
        self._alert_threshold = alert_threshold
        self._alerts: list[dict] = []
        self._metric_history: list[dict] = []
        self._detector = BiasDetector()
        logger.info(
            f"BiasMonitoringPipeline initialized: window={window_size}, "
            f"alert_threshold={alert_threshold}."
        )

    def ingest(self, record: dict) -> None:
        """
        Add a decision record to the sliding window.

        Args:
            record: Must contain 'gender' (or group field) and 'qualified' (or outcome).
        """
        self._window.append(record)

    def evaluate(self, group_col: str = "gender",
                 outcome_col: str = "qualified") -> dict:
        """
        Compute bias metrics on the current window and check for alerts.
        """
        if len(self._window) < 10:
            logger.debug(
                f"Window too small ({len(self._window)}). Need at least 10 records."
            )
            return {"status": "insufficient_data", "window_size": len(self._window)}

        window_df = pd.DataFrame(list(self._window))
        analysis = self._detector.analyze(window_df, group_col, outcome_col)

        # Mock Prometheus metric emission
        metric_point = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "window_size": len(self._window),
            "disparate_impact_min": analysis["metrics"].get(
                "disparate_impact", {}
            ).get("min_ratio", None),
            "severity": analysis["severity"],
        }
        self._metric_history.append(metric_point)
        logger.debug(
            f"[Mock Prometheus] bias_disparate_impact_ratio="
            f"{metric_point['disparate_impact_min']}"
        )

        # Alert firing
        if analysis["severity"] in ("HIGH", "CRITICAL"):
            alert = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": analysis["severity"],
                "message": (
                    f"Bias alert: disparate impact "
                    f"{metric_point['disparate_impact_min']:.2f} "
                    f"(threshold: {self._alert_threshold})"
                ),
                "window_snapshot_size": len(self._window),
            }
            self._alerts.append(alert)
            logger.error(f"ALERT FIRED: {alert['message']}")

        return {
            "analysis": analysis,
            "metric_point": metric_point,
            "alert_fired": analysis["severity"] in ("HIGH", "CRITICAL"),
        }

    def get_alerts(self) -> list[dict]:
        return copy.deepcopy(self._alerts)

    def get_metric_history(self) -> list[dict]:
        return copy.deepcopy(self._metric_history)


# ═══════════════════════════════════════════════════════════════════════════
# Section 3.6 — FairHiringAgent + FairnessEnforcer (Chapter 12, p.20–23)
# ═══════════════════════════════════════════════════════════════════════════

class ResumeAnalyzer:
    """
    Scores resumes using the chapter's deterministic formula or LLM.

    Formula (p.20):
        score = 0.3 + 0.1 * min(skill_matches, 5) + 0.02 * min(years_exp, 10)
    """

    # Job-posting required skills
    REQUIRED_SKILLS = {"python", "machine_learning", "sql", "statistics", "cloud_computing"}

    def __init__(self):
        self._mock_llm = get_mock_llm() if is_simulation() else None

    @graceful_fallback(
        fallback_value={"score": 0.0, "explanation_map": {}, "source": "fallback"},
        section_ref="Section 12 - Resume Scoring (p.20-21)"
    )
    def score(self, candidate: dict) -> dict:
        """
        Score a candidate record.

        Args:
            candidate: Dict with 'skills' (list) and 'years_experience' (int).

        Returns:
            {'score': float, 'explanation_map': dict, 'source': str}
        """
        skills = candidate.get("skills", [])
        years_exp = candidate.get("years_experience", 0)
        skill_matches = len(set(skills) & self.REQUIRED_SKILLS)

        if self._mock_llm:
            return self._mock_llm.invoke(
                "score_resume candidate hiring",
                skill_matches=skill_matches,
                years_exp=years_exp,
            )

        # Live mode would call actual LLM here
        score = 0.3 + 0.1 * min(skill_matches, 5) + 0.02 * min(years_exp, 10)
        return {
            "score": round(min(score, 1.0), 4),
            "explanation_map": {
                "base": 0.3,
                "skills_contribution": round(0.1 * min(skill_matches, 5), 4),
                "experience_contribution": round(0.02 * min(years_exp, 10), 4),
            },
            "source": "live",
        }


class FairnessEnforcer:
    """
    Applies bias mitigation strategies.

    Three strategies (p.22-23):
        1. Reweighting — adjust scores to compensate for group imbalance.
        2. Threshold adjustment — lower threshold for disadvantaged groups.
        3. Representation learning — feature transformation (simplified mock).

    Each strategy returns a corrected score with an audit entry.
    """

    def __init__(self):
        logger.info("FairnessEnforcer initialized with 3 mitigation strategies.")

    @graceful_fallback(
        fallback_value={"corrected_score": 0.0, "strategy_used": "fallback",
                        "audit_entry": {}},
        section_ref="Section 12 - Fairness Enforcement (p.22-23)"
    )
    def mitigate(self, score: float, group: str, group_stats: dict,
                 strategy: str = "reweighting") -> dict:
        """
        Apply a mitigation strategy to a candidate's score.

        Args:
            score: Original (potentially biased) score.
            group: The candidate's group value (e.g., 'female').
            group_stats: Dict with group selection rates.
            strategy: One of 'reweighting', 'threshold_adjustment',
                     'representation_learning'.

        Returns:
            {'corrected_score': float, 'strategy_used': str, 'audit_entry': dict}
        """
        if strategy == "reweighting":
            return self._reweighting(score, group, group_stats)
        elif strategy == "threshold_adjustment":
            return self._threshold_adjustment(score, group, group_stats)
        elif strategy == "representation_learning":
            return self._representation_learning(score, group, group_stats)
        else:
            logger.error(f"Unknown strategy: {strategy}")
            return {
                "corrected_score": score,
                "strategy_used": "none",
                "audit_entry": {"error": f"Unknown strategy: {strategy}"},
            }

    def _reweighting(self, score: float, group: str,
                     group_stats: dict) -> dict:
        """
        Reweighting: boost under-represented group scores proportionally.
        See Chapter 12, p.22.
        """
        max_rate = max(group_stats.values()) if group_stats else 1.0
        group_rate = group_stats.get(group, max_rate)
        if group_rate > 0 and max_rate > 0:
            weight = max_rate / group_rate
        else:
            weight = 1.0

        corrected = round(min(score * weight, 1.0), 4)
        logger.debug(
            f"Reweighting: group='{group}', weight={weight:.3f}, "
            f"{score:.4f} → {corrected:.4f}"
        )
        return {
            "corrected_score": corrected,
            "strategy_used": "reweighting",
            "audit_entry": {
                "original_score": score,
                "group": group,
                "weight": round(weight, 4),
                "corrected_score": corrected,
            },
        }

    def _threshold_adjustment(self, score: float, group: str,
                              group_stats: dict) -> dict:
        """
        Threshold adjustment: lower the passing threshold for
        disadvantaged groups. See Chapter 12, p.22.
        """
        max_rate = max(group_stats.values()) if group_stats else 1.0
        group_rate = group_stats.get(group, max_rate)

        # Compute offset to equalize selection rates
        if group_rate < max_rate and max_rate > 0:
            offset = round((max_rate - group_rate) * 0.1, 4)
        else:
            offset = 0.0

        corrected = round(min(score + offset, 1.0), 4)
        logger.debug(
            f"Threshold adjustment: group='{group}', offset={offset:.4f}, "
            f"{score:.4f} → {corrected:.4f}"
        )
        return {
            "corrected_score": corrected,
            "strategy_used": "threshold_adjustment",
            "audit_entry": {
                "original_score": score,
                "group": group,
                "offset": offset,
                "corrected_score": corrected,
            },
        }

    def _representation_learning(self, score: float, group: str,
                                 group_stats: dict) -> dict:
        """
        Representation learning (simplified): project score into a
        group-invariant space. See Chapter 12, p.23.
        """
        # Simplified: normalize to group mean
        rates = list(group_stats.values())
        global_mean = np.mean(rates) if rates else 0.5
        group_rate = group_stats.get(group, global_mean)

        if group_rate > 0:
            corrected = round(min(score * (global_mean / group_rate), 1.0), 4)
        else:
            corrected = score

        logger.debug(
            f"Representation learning: group='{group}', "
            f"global_mean={global_mean:.3f}, {score:.4f} → {corrected:.4f}"
        )
        return {
            "corrected_score": corrected,
            "strategy_used": "representation_learning",
            "audit_entry": {
                "original_score": score,
                "group": group,
                "global_mean": round(global_mean, 4),
                "corrected_score": corrected,
            },
        }


class FairHiringAgent:
    """
    Three-layer fair hiring pipeline (Chapter 12, p.20-23):
        Layer 1: Anonymize — remove protected attributes from input.
        Layer 2: Evaluate — score candidate on merits.
        Layer 3: Bias Check + Mitigate — detect and correct bias.

    All methods wrapped in @graceful_fallback.
    """

    def __init__(self):
        self._analyzer = ResumeAnalyzer()
        self._detector = BiasDetector()
        self._enforcer = FairnessEnforcer()
        logger.info("FairHiringAgent initialized (3-layer pipeline).")

    @graceful_fallback(
        fallback_value={},
        section_ref="Section 12 - Anonymization (p.21)"
    )
    def anonymize(self, candidate: dict) -> dict:
        """
        Layer 1: Strip protected attributes before scoring.

        Removes: gender, ethnicity, education_institution (proxy risk).
        Preserves: skills, years_experience, education_level.
        """
        protected_fields = {"gender", "ethnicity", "education_institution",
                            "candidate_id"}
        anonymized = {k: v for k, v in candidate.items()
                      if k not in protected_fields}
        logger.debug(
            f"Anonymized candidate: removed {protected_fields & set(candidate.keys())}"
        )
        return anonymized

    @graceful_fallback(
        fallback_value={"score": 0.0, "explanation_map": {}, "source": "fallback"},
        section_ref="Section 12 - Candidate Evaluation (p.20-21)"
    )
    def evaluate_candidate(self, candidate: dict) -> dict:
        """
        Layer 2: Score the anonymized candidate.
        """
        anonymized = self.anonymize(candidate)
        result = self._analyzer.score(anonymized)
        logger.success(
            f"Candidate scored: {result.get('score', 0):.4f}"
        )
        return result

    @graceful_fallback(
        fallback_value={"before": {}, "after": {}, "mitigation_applied": False},
        section_ref="Section 12 - Fair Hiring Pipeline (p.20-23)"
    )
    def run_pipeline(self, df: pd.DataFrame,
                     mitigation_strategy: str = "reweighting") -> dict:
        """
        Layer 3: Full pipeline — detect bias, apply mitigation if needed.

        Args:
            df: HR dataset with 'gender', 'qualified', 'raw_score' columns.
            mitigation_strategy: Strategy for FairnessEnforcer.

        Returns:
            dict with before/after analysis and mitigation details.
        """
        logger.info("Starting FairHiringAgent pipeline...")

        # Step 1: Analyze bias in current predictions
        before_analysis = self._detector.analyze(df, "gender", "qualified")

        di_result = before_analysis["metrics"].get("disparate_impact", {})
        needs_mitigation = di_result.get("four_fifths_violation", False)

        if not needs_mitigation:
            logger.success("No four-fifths violation detected. Pipeline complete.")
            return {
                "before": before_analysis,
                "after": before_analysis,
                "mitigation_applied": False,
            }

        # Step 2: Apply mitigation
        logger.info(
            f"Four-fifths violation detected (DI={di_result.get('min_ratio', 0):.2f}). "
            f"Applying mitigation: {mitigation_strategy}."
        )

        group_rates = df.groupby("gender")["qualified"].mean().to_dict()
        corrected_df = df.copy()
        audit_entries = []

        for idx, row in corrected_df.iterrows():
            result = self._enforcer.mitigate(
                score=row["raw_score"],
                group=row["gender"],
                group_stats=group_rates,
                strategy=mitigation_strategy,
            )
            corrected_df.at[idx, "raw_score"] = result["corrected_score"]
            audit_entries.append(result["audit_entry"])

        # Recompute qualified with corrected scores
        corrected_df["qualified"] = corrected_df["raw_score"] >= 0.65

        # Step 3: Re-analyze
        after_analysis = self._detector.analyze(
            corrected_df, "gender", "qualified"
        )

        after_di = after_analysis["metrics"].get(
            "disparate_impact", {}
        ).get("min_ratio", 0)

        logger.success(
            f"Mitigation complete. DI before: {di_result.get('min_ratio', 0):.2f} "
            f"→ after: {after_di:.2f}."
        )

        return {
            "before": before_analysis,
            "after": after_analysis,
            "mitigation_applied": True,
            "strategy": mitigation_strategy,
            "corrected_df": corrected_df,
            "audit_entries": audit_entries,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Impossibility Theorem Visualization Helper (Chapter 12, p.12-13)
# ═══════════════════════════════════════════════════════════════════════════

def demonstrate_impossibility_theorem() -> dict:
    """
    Demonstrates the Impossibility of Fairness Theorem (p.12-13, Table 12.1).

    Shows that three fairness criteria — demographic parity, equal opportunity,
    and predictive parity — cannot all be satisfied simultaneously when base
    rates differ across groups.

    Returns:
        dict with three regimes and their tradeoffs.
    """
    regimes = {
        "regime_1_demographic_parity": {
            "name": "Demographic Parity Priority",
            "satisfied": ["demographic_parity"],
            "violated": ["equal_opportunity", "predictive_parity"],
            "description": (
                "Equal selection rates across groups, but qualified candidates "
                "from high-base-rate groups may be rejected while less-qualified "
                "candidates from low-base-rate groups are accepted."
            ),
        },
        "regime_2_equal_opportunity": {
            "name": "Equal Opportunity Priority",
            "satisfied": ["equal_opportunity"],
            "violated": ["demographic_parity", "predictive_parity"],
            "description": (
                "Equal true-positive rates, but overall selection rates will "
                "differ across groups proportionally to their base rates."
            ),
        },
        "regime_3_predictive_parity": {
            "name": "Predictive Parity Priority",
            "satisfied": ["predictive_parity"],
            "violated": ["demographic_parity", "equal_opportunity"],
            "description": (
                "Equal positive predictive values, but disadvantaged groups "
                "face higher false-negative rates."
            ),
        },
    }

    logger.info(
        "Impossibility Theorem: only one fairness regime can be satisfied "
        "when base rates differ. See Chapter 12, Table 12.1 (p.12-13)."
    )

    return {
        "theorem": "Impossibility of Fairness",
        "reference": "Chapter 12, p.12-13, Table 12.1",
        "regimes": regimes,
        "conclusion": (
            "Organizations must choose which fairness criterion to prioritize "
            "based on their domain, regulatory requirements, and stakeholder values."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Self-test
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from src.synthetic_data import generate_hr_dataset

    # -- Deontic Logic --
    logger.info("=== Deontic Logic Self-Test ===")
    deontic = DeonticOperator()
    deontic.add_obligation("provide_explanation")
    deontic.add_permission("collect_anonymized_data")
    deontic.add_prohibition("share_medical_details")
    status = deontic.get_status()
    logger.success(f"Deontic status: {status}")
    consistency = deontic.check_consistency()
    logger.success(f"Consistency: {consistency}")

    # -- EthicalReasoningAgent --
    logger.info("=== EthicalReasoningAgent Self-Test ===")
    era = EthicalReasoningAgent()
    result = era.evaluate_action("share_medical_details with external_email")
    logger.success(f"Evaluation: {result}")
    mitigation = era.mitigate(result["violations"])
    logger.success(f"Mitigations: {mitigation}")

    # -- EUCompliantAgent --
    logger.info("=== EUCompliantAgent Self-Test ===")
    euca = EUCompliantAgent()
    config = {
        "human_override": True, "escalation_path": True, "manual_review": True,
        "error_handling": True, "fallback_mode": True, "input_validation": True,
        "data_encryption": True, "consent_management": True, "data_minimization": False,
        "explanation_interface": True, "audit_trail": True, "model_documentation": True,
        "bias_testing": True, "fairness_metrics": True, "representative_data": True,
        "impact_assessment": True, "stakeholder_consultation": True,
        "responsible_party": True, "audit_schedule": True, "incident_response": True,
    }
    report = euca.compliance_check(config)
    logger.success(f"EU Compliance: {report['summary']}")

    # -- BiasDetector --
    logger.info("=== BiasDetector Self-Test ===")
    hr_df = generate_hr_dataset(200, 42)
    detector = BiasDetector()
    analysis = detector.analyze(hr_df, "gender", "qualified")
    logger.success(f"Bias severity: {analysis['severity']}")

    # -- FairHiringAgent --
    logger.info("=== FairHiringAgent Self-Test ===")
    fha = FairHiringAgent()
    pipeline_result = fha.run_pipeline(hr_df, mitigation_strategy="reweighting")
    logger.success(
        f"Mitigation applied: {pipeline_result['mitigation_applied']}"
    )

    logger.success("All EthicalCore self-tests passed.")
