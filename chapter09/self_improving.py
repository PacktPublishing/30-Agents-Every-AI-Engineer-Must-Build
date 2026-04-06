# src/self_improving.py
# Chapter 9: Software Development Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Author: Imran Ahmad
#
# Self-Improving Agent components implementing the closed-loop
# execute → observe → learn → adapt control system.
#
# Components:
#   - SensingLayer — multi-modal feedback collection
#   - CriticAgent — KPI evaluation against thresholds
#   - PlannerAgent — improvement hypothesis generation via LLM
#   - LearningLayer — applies approved adaptations
#   - HITLCheckpoint — simulates human approval/rejection
#   - run_self_improvement_loop() — orchestrates the full cycle
#
# Ref: §9.4, "Architectural Principles: The Closed-Loop Control System"
# Ref: §9.4, "Learning Mechanisms and Feedback Translation"
# Ref: §9.4, "Practical Implementation: Adaptive Customer Support Agent"

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from chapter09.utils import ColorLog, fail_gracefully
from chapter09.state_models import (
    FeedbackRecord,
    AdaptationType,
    ImprovementHypothesis,
    PlannerOutput,
)


# ===================================================================
# SensingLayer — Multi-Modal Feedback Collection
# ===================================================================

class SensingLayer:
    """
    Collects feedback from three channels as described in Figure 9.5:

    - Explicit feedback: Direct human signals (ratings, comments,
      corrections from users or reviewers).
    - Implicit feedback: Behavioral indicators (session duration,
      task abandonment, iteration counts, acceptance rates).
    - Synthetic feedback: Automatically generated through consistency
      checks, benchmarks, or comparison against gold-standard outputs.

    Ref: §9.4, "The Sensing Layer" and "Multi-Modal Feedback Collection"
    """

    def __init__(self):
        self._records: List[FeedbackRecord] = []
        ColorLog.info("SensingLayer initialized (empty).")

    def collect_explicit(self, signal: str, metadata: Optional[Dict] = None):
        """
        Record explicit feedback (ratings, comments, corrections).
        Ref: §9.4, "Explicit feedback arrives as direct human signals"
        """
        record = FeedbackRecord(
            source_type="explicit",
            signal=signal,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
        )
        self._records.append(record)
        ColorLog.info(f"SensingLayer: Collected explicit — '{signal[:50]}...'")

    def collect_implicit(self, signal: str, metadata: Optional[Dict] = None):
        """
        Record implicit feedback (behavioral indicators).
        Ref: §9.4, "Implicit feedback emerges from behavioral indicators"
        """
        record = FeedbackRecord(
            source_type="implicit",
            signal=signal,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
        )
        self._records.append(record)
        ColorLog.info(f"SensingLayer: Collected implicit — '{signal[:50]}...'")

    def collect_synthetic(self, signal: str, metadata: Optional[Dict] = None):
        """
        Record synthetic feedback (automated evaluation).
        Ref: §9.4, "Synthetic feedback is automatically generated"
        """
        record = FeedbackRecord(
            source_type="synthetic",
            signal=signal,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
        )
        self._records.append(record)
        ColorLog.info(
            f"SensingLayer: Collected synthetic — '{signal[:50]}...'"
        )

    def get_summary(self) -> Dict[str, Any]:
        """Aggregate feedback counts by source type."""
        counts = {"explicit": 0, "implicit": 0, "synthetic": 0}
        for r in self._records:
            counts[r.source_type] = counts.get(r.source_type, 0) + 1
        return {
            "total_records": len(self._records),
            "by_type": counts,
            "collection_period": {
                "start": (
                    self._records[0].timestamp if self._records else None
                ),
                "end": (
                    self._records[-1].timestamp if self._records else None
                ),
            },
        }

    def get_records(
        self, source_type: Optional[str] = None
    ) -> List[FeedbackRecord]:
        """Retrieve records, optionally filtered by source type."""
        if source_type:
            return [r for r in self._records if r.source_type == source_type]
        return list(self._records)

    @property
    def count(self) -> int:
        return len(self._records)


# ===================================================================
# CriticAgent — KPI Evaluation
# ===================================================================

class CriticAgent:
    """
    Evaluates agent output against defined KPI thresholds.

    Tracked KPIs (from §9.4):
      - Task Completion Rate (target: 0.80)
      - Error Recovery Ratio (target: 0.85)
      - Latency P95 (target: 3.0s)
      - User Satisfaction Index (target: 4.0)
      - Improvement Velocity (target: 0.10)

    Ref: §9.4, "The Critic Agent" — KPI evaluation listing
    """

    DEFAULT_THRESHOLDS = {
        "task_completion_rate": 0.80,
        "error_recovery_ratio": 0.85,
        "latency_p95": 3.0,
        "user_satisfaction_index": 4.0,
        "improvement_velocity": 0.10,
    }

    def __init__(
        self,
        thresholds: Optional[Dict[str, float]] = None,
        llm: Any = None,
    ):
        self.thresholds = thresholds or self.DEFAULT_THRESHOLDS.copy()
        self.llm = llm
        ColorLog.info(
            f"CriticAgent initialized with {len(self.thresholds)} "
            f"KPI thresholds."
        )

    @fail_gracefully(fallback_return=lambda: {})
    def evaluate(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluate observed metrics against KPI thresholds.

        Args:
            metrics: Dict of metric_name → observed_value.

        Returns:
            Evaluation report with scores, status, and failure modes.

        Ref: §9.4, "The Critic Agent evaluates against certain KPIs"
        """
        ColorLog.info("CriticAgent: Evaluating KPI metrics...")

        scores = {}
        below_target = []
        above_target = []

        for metric, threshold in self.thresholds.items():
            observed = metrics.get(metric)
            if observed is None:
                scores[metric] = {"status": "MISSING", "observed": None}
                continue

            # Latency is an upper-bound metric (lower is better)
            if "latency" in metric:
                status = "WITHIN RANGE" if observed <= threshold else "ABOVE TARGET"
                if observed > threshold:
                    below_target.append(metric)
                else:
                    above_target.append(metric)
            else:
                status = (
                    "ABOVE TARGET" if observed >= threshold
                    else "BELOW TARGET"
                )
                if observed < threshold:
                    below_target.append(metric)
                else:
                    above_target.append(metric)

            scores[metric] = {
                "observed": observed,
                "threshold": threshold,
                "status": status,
            }

        evaluation = {
            "scores": scores,
            "below_target": below_target,
            "above_target": above_target,
            "overall_health": (
                "HEALTHY" if not below_target else "NEEDS IMPROVEMENT"
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # LLM-enhanced evaluation (optional)
        if self.llm and below_target:
            prompt = (
                f"You are a critic agent evaluating agent performance.\n"
                f"The following KPIs are below target: {below_target}\n"
                f"Current metrics: {metrics}\n"
                f"Thresholds: {self.thresholds}\n\n"
                f"Identify specific failure modes and recommend routing "
                f"to the Planner Agent for hypothesis generation."
            )
            response = self.llm.invoke(prompt)
            evaluation["llm_analysis"] = response.content

        if below_target:
            ColorLog.error(
                f"CriticAgent: {len(below_target)} KPI(s) below target — "
                f"{below_target}"
            )
        else:
            ColorLog.success("CriticAgent: All KPIs within acceptable range.")

        return evaluation


# ===================================================================
# PlannerAgent — Improvement Hypothesis Generation
# ===================================================================

class PlannerAgent:
    """
    Synthesizes feedback from the CriticAgent and generates structured
    ImprovementHypothesis objects for the HITL checkpoint.

    Each hypothesis carries explicit evidence, confidence metrics, and
    a rollback_safe flag to determine routing at the checkpoint.

    Ref: §9.4, "The Planner Agent synthesizes feedback"
    Ref: §9.4, "Learning Mechanisms — Pydantic models listing"
    """

    def __init__(self, llm: Any = None):
        self.llm = llm
        ColorLog.info("PlannerAgent initialized.")

    @fail_gracefully(fallback_return=lambda: PlannerOutput(
        hypotheses=[], requires_human_review=True, baseline_metrics={}
    ))
    def generate_hypotheses(
        self,
        critic_evaluation: Dict[str, Any],
        sensing_summary: Optional[Dict] = None,
    ) -> PlannerOutput:
        """
        Generate structured improvement hypotheses from critic evaluation.

        Args:
            critic_evaluation: Output from CriticAgent.evaluate().
            sensing_summary: Optional SensingLayer.get_summary() data.

        Returns:
            PlannerOutput with hypotheses and review requirements.

        Ref: §9.4, "PlannerOutput" Pydantic model listing
        """
        ColorLog.info("PlannerAgent: Generating improvement hypotheses...")

        hypotheses = []
        below_target = critic_evaluation.get("below_target", [])
        scores = critic_evaluation.get("scores", {})

        # If LLM available, use it for hypothesis generation
        if self.llm:
            prompt = (
                f"You are a planner agent for a self-improving system.\n"
                f"Analyze these underperforming KPIs and propose "
                f"improvement hypotheses:\n\n"
                f"Below target: {below_target}\n"
                f"Scores: {json.dumps(scores, default=str)}\n"
                f"Sensing data: {json.dumps(sensing_summary or {}, default=str)}\n\n"
                f"For each hypothesis, specify:\n"
                f"  - source_signal\n"
                f"  - adaptation_type (prompt_update, threshold_adjustment, "
                f"retrieval_strategy, tool_reordering)\n"
                f"  - proposed_change\n"
                f"  - confidence (0.0–1.0)\n"
                f"  - evidence_count\n"
                f"  - rollback_safe (true/false)\n\n"
                f"Return as JSON."
            )
            response = self.llm.invoke(prompt)

            # Parse LLM response (MockLLM returns valid JSON)
            try:
                data = json.loads(response.content)
                for h in data.get("hypotheses", []):
                    hypotheses.append(ImprovementHypothesis(
                        source_signal=h["source_signal"],
                        adaptation_type=AdaptationType(h["adaptation_type"]),
                        proposed_change=h["proposed_change"],
                        confidence=h["confidence"],
                        evidence_count=h["evidence_count"],
                        rollback_safe=h.get("rollback_safe", True),
                    ))
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                ColorLog.error(
                    f"PlannerAgent: Failed to parse LLM response — {e}"
                )

        # Fallback: generate deterministic hypotheses from below-target KPIs
        if not hypotheses:
            for metric in below_target:
                observed = scores.get(metric, {}).get("observed", 0)
                threshold = scores.get(metric, {}).get("threshold", 0)
                hypotheses.append(ImprovementHypothesis(
                    source_signal=(
                        f"{metric} at {observed} vs target {threshold}"
                    ),
                    adaptation_type=AdaptationType.PROMPT_UPDATE,
                    proposed_change=(
                        f"Investigate and improve {metric} through "
                        f"prompt refinement and context enhancement."
                    ),
                    confidence=0.65,
                    evidence_count=1,
                    rollback_safe=True,
                ))

        # Determine if human review is needed
        requires_review = any(
            h.confidence < 0.70 or not h.rollback_safe
            for h in hypotheses
        )

        baseline_metrics = {
            k: v.get("observed", 0) for k, v in scores.items()
            if isinstance(v, dict)
        }

        output = PlannerOutput(
            hypotheses=hypotheses,
            requires_human_review=requires_review,
            baseline_metrics=baseline_metrics,
        )

        ColorLog.success(
            f"PlannerAgent: Generated {len(hypotheses)} hypothesis(es). "
            f"Human review {'required' if requires_review else 'not required'}."
        )

        return output


# ===================================================================
# HITLCheckpoint — Human-in-the-Loop Approval Simulation
# ===================================================================

class HITLCheckpoint:
    """
    Simulates the human validation checkpoint from Figure 9.5.

    Not all improvements should deploy automatically. When the planner
    proposes significant changes, the system pauses for human review.

    In Simulation Mode, auto_approve can be toggled to demonstrate
    both approval and rejection flows.

    Ref: §9.4, "HITL Checkpoint" in Figure 9.5
    Ref: §9.4, "Automated Adaptations and Human Validation"
    """

    def __init__(self, auto_approve: bool = True):
        self.auto_approve = auto_approve
        self._review_log: List[Dict[str, Any]] = []
        ColorLog.info(
            f"HITLCheckpoint initialized "
            f"(auto_approve={auto_approve})."
        )

    @fail_gracefully(fallback_return=lambda: [])
    def review(self, planner_output: PlannerOutput) -> List[Dict[str, Any]]:
        """
        Review planner hypotheses and return approval decisions.

        Args:
            planner_output: PlannerOutput from PlannerAgent.

        Returns:
            List of decision dicts with 'hypothesis', 'approved',
            and 'justification' fields.
        """
        ColorLog.header("HITL CHECKPOINT — Human Review")
        decisions = []

        for i, hypothesis in enumerate(planner_output.hypotheses, 1):
            # High-confidence, rollback-safe changes auto-approve
            if (hypothesis.confidence >= 0.70
                    and hypothesis.rollback_safe
                    and self.auto_approve):
                approved = True
                justification = (
                    f"Auto-approved: confidence={hypothesis.confidence:.2f}, "
                    f"rollback_safe=True, evidence_count="
                    f"{hypothesis.evidence_count}"
                )
                ColorLog.success(
                    f"  Hypothesis {i}: APPROVED — "
                    f"'{hypothesis.proposed_change[:60]}...'"
                )
            elif (not hypothesis.rollback_safe
                    or hypothesis.confidence < 0.50):
                approved = False
                justification = (
                    f"Rejected: {'not rollback-safe' if not hypothesis.rollback_safe else ''}"
                    f"{'low confidence (' + str(hypothesis.confidence) + ')' if hypothesis.confidence < 0.50 else ''}"
                )
                ColorLog.error(
                    f"  Hypothesis {i}: REJECTED — "
                    f"'{hypothesis.proposed_change[:60]}...'"
                )
            else:
                approved = self.auto_approve
                justification = (
                    f"Marginal case (confidence={hypothesis.confidence:.2f}). "
                    f"{'Auto-approved per simulation config.' if self.auto_approve else 'Requires manual review.'}"
                )
                level = ColorLog.success if approved else ColorLog.warning
                level(
                    f"  Hypothesis {i}: "
                    f"{'APPROVED' if approved else 'PENDING'} — "
                    f"'{hypothesis.proposed_change[:60]}...'"
                )

            decision = {
                "hypothesis": hypothesis.model_dump(),
                "approved": approved,
                "justification": justification,
                "reviewed_at": datetime.now(timezone.utc).isoformat(),
            }
            decisions.append(decision)
            self._review_log.append(decision)

        approved_count = sum(1 for d in decisions if d["approved"])
        ColorLog.info(
            f"HITL Checkpoint: {approved_count}/{len(decisions)} "
            f"hypotheses approved."
        )

        return decisions


# ===================================================================
# LearningLayer — Apply Approved Adaptations
# ===================================================================

class LearningLayer:
    """
    Applies approved adaptations to agent configuration, updating
    internal parameters, strategies, or prompts.

    Every change is versioned and associated with the feedback that
    motivated it, ensuring traceability.

    Ref: §9.4, "The Learning Layer updates internal parameters"
    Ref: §9.4, "Operationalizing Continuous Adaptation"
    """

    def __init__(self):
        self._applied: List[Dict[str, Any]] = []
        self._version = 0
        ColorLog.info("LearningLayer initialized (v0).")

    @fail_gracefully(fallback_return=None)
    def apply(self, decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Apply approved adaptations from HITL checkpoint decisions.

        Args:
            decisions: List of decision dicts from HITLCheckpoint.review().

        Returns:
            Summary of applied adaptations.
        """
        ColorLog.info("LearningLayer: Applying approved adaptations...")
        applied_this_round = []

        for decision in decisions:
            if not decision.get("approved", False):
                continue

            hypothesis = decision["hypothesis"]
            self._version += 1

            adaptation = {
                "version": self._version,
                "adaptation_type": hypothesis["adaptation_type"],
                "proposed_change": hypothesis["proposed_change"],
                "source_signal": hypothesis["source_signal"],
                "confidence": hypothesis["confidence"],
                "applied_at": datetime.now(timezone.utc).isoformat(),
            }
            self._applied.append(adaptation)
            applied_this_round.append(adaptation)

            ColorLog.success(
                f"LearningLayer: Applied v{self._version} — "
                f"{hypothesis['adaptation_type']}: "
                f"'{hypothesis['proposed_change'][:50]}...'"
            )

        summary = {
            "adaptations_applied": len(applied_this_round),
            "current_version": self._version,
            "total_adaptations": len(self._applied),
            "details": applied_this_round,
        }

        ColorLog.info(
            f"LearningLayer: {len(applied_this_round)} adaptation(s) "
            f"applied. Current version: v{self._version}."
        )

        return summary

    def rollback(self, to_version: int) -> Dict[str, Any]:
        """
        Rollback to a previous version, removing later adaptations.

        Ref: §9.4, "Governance — Immutable Version History and Rollback"
        """
        removed = [a for a in self._applied if a["version"] > to_version]
        self._applied = [
            a for a in self._applied if a["version"] <= to_version
        ]
        self._version = to_version

        ColorLog.warning(
            f"LearningLayer: Rolled back to v{to_version}. "
            f"Removed {len(removed)} adaptation(s)."
        )

        return {
            "rolled_back_to": to_version,
            "removed_count": len(removed),
            "removed": removed,
        }

    def get_history(self) -> List[Dict[str, Any]]:
        """Return the full adaptation history."""
        return list(self._applied)


# ===================================================================
# run_self_improvement_loop() — Full Cycle Orchestrator
# ===================================================================

@fail_gracefully(fallback_return=lambda: {})
def run_self_improvement_loop(
    llm: Any,
    feedback_data: Optional[Dict[str, Any]] = None,
    metrics: Optional[Dict[str, float]] = None,
    auto_approve: bool = True,
) -> Dict[str, Any]:
    """
    Orchestrates the full execute → observe → learn → adapt cycle
    as depicted in Figure 9.5.

    Steps:
      1. Sensing Layer collects feedback (or uses provided data)
      2. Critic Agent evaluates KPIs against thresholds
      3. Planner Agent generates improvement hypotheses
      4. HITL Checkpoint reviews and approves/rejects
      5. Learning Layer applies approved adaptations
      6. Returns summary of the full cycle

    Args:
        llm: Language model (MockLLM or ChatOpenAI).
        feedback_data: Optional pre-collected feedback signals.
        metrics: Optional observed KPI metrics.
        auto_approve: Whether HITL auto-approves (default True).

    Returns:
        Dict summarizing the complete improvement cycle.

    Ref: §9.4, "Practical Implementation — Customer Support Case Study"
    """
    ColorLog.header("SELF-IMPROVEMENT LOOP — Execute → Observe → Learn → Adapt")

    # --- Step 1: Sensing Layer ---
    sensing = SensingLayer()

    if feedback_data:
        for fb in feedback_data.get("explicit", []):
            sensing.collect_explicit(fb)
        for fb in feedback_data.get("implicit", []):
            sensing.collect_implicit(fb)
        for fb in feedback_data.get("synthetic", []):
            sensing.collect_synthetic(fb)
    else:
        # Default simulation data (customer support case study)
        sensing.collect_explicit(
            "User rated 3/5 — 'Agent didn't understand my question'",
            {"rating": 3, "category": "comprehension"},
        )
        sensing.collect_explicit(
            "User rated 5/5 — 'Quick and accurate response'",
            {"rating": 5, "category": "satisfaction"},
        )
        sensing.collect_implicit(
            "Avg 4.2 turns per resolution; 23% rephrased questions",
            {"avg_turns": 4.2, "rephrase_rate": 0.23},
        )
        sensing.collect_implicit(
            "Escalation rate: 45% for policy-related queries",
            {"escalation_rate": 0.45, "category": "policy"},
        )
        sensing.collect_synthetic(
            "Benchmark: 91% functional correctness, 78% code quality",
            {"correctness": 0.91, "quality": 0.78},
        )

    summary_sensing = sensing.get_summary()
    ColorLog.info(
        f"Sensing: {summary_sensing['total_records']} records collected "
        f"({summary_sensing['by_type']})"
    )

    # --- Step 2: Critic Agent ---
    critic = CriticAgent(llm=llm)
    observed_metrics = metrics or {
        "task_completion_rate": 0.74,
        "error_recovery_ratio": 0.89,
        "latency_p95": 2.3,
        "user_satisfaction_index": 3.8,
        "improvement_velocity": 0.12,
    }
    evaluation = critic.evaluate(observed_metrics)

    # --- Step 3: Planner Agent ---
    planner = PlannerAgent(llm=llm)
    planner_output = planner.generate_hypotheses(
        evaluation, summary_sensing
    )

    # --- Step 4: HITL Checkpoint ---
    checkpoint = HITLCheckpoint(auto_approve=auto_approve)
    decisions = checkpoint.review(planner_output)

    # --- Step 5: Learning Layer ---
    learning = LearningLayer()
    adaptation_summary = learning.apply(decisions)

    # --- Compile Results ---
    result = {
        "sensing_summary": summary_sensing,
        "critic_evaluation": evaluation,
        "planner_output": planner_output.model_dump(),
        "hitl_decisions": decisions,
        "adaptation_summary": adaptation_summary,
        "cycle_complete": True,
    }

    ColorLog.header("SELF-IMPROVEMENT CYCLE COMPLETE")
    ColorLog.success(
        f"Hypotheses generated: {len(planner_output.hypotheses)}"
    )
    approved = sum(1 for d in decisions if d["approved"])
    ColorLog.success(f"Approved: {approved}/{len(decisions)}")
    if adaptation_summary:
        ColorLog.success(
            f"Adaptations applied: "
            f"{adaptation_summary.get('adaptations_applied', 0)}"
        )

    return result
