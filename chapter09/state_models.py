# src/state_models.py
# Chapter 9: Software Development Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Author: Imran Ahmad
#
# Pydantic data models and TypedDict state definitions for:
#   - Task and AgentState (§9.2 — State Management)
#   - AdaptationType, ImprovementHypothesis, PlannerOutput (§9.4 — Learning Mechanisms)
#
# Ref: §9.2 "Implementing State Management" code listings;
#      §9.4 "Learning Mechanisms and Feedback Translation" Pydantic models.

from __future__ import annotations

import operator
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence

from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict


# ---------------------------------------------------------------------------
# §9.2 — Code-Generation Agent State Models
# ---------------------------------------------------------------------------

class Task(BaseModel):
    """
    Represents a single development task within the TDG workflow.

    Tracks the full lifecycle: assignment → code generation → testing →
    refinement iterations. The 'iterations' counter enforces the loop
    limit in LangGraph conditional edges (default max: 3).

    Ref: §9.2, "Implementing State Management"
    """
    task_id: str
    description: str
    task_type: str  # 'backend', 'frontend', or 'integration'
    status: str = "pending"
    dependencies: List[str] = Field(default_factory=list)
    code: Optional[str] = None
    tests: Optional[str] = None
    test_results: Optional[str] = None
    iterations: int = 0


class AgentState(TypedDict):
    """
    Global state shared across all agents in the LangGraph workflow.

    The 'messages' field uses LangGraph's operator.add annotation to
    accumulate conversation history across nodes, providing agents
    with full context of prior decisions.

    Ref: §9.2, "Implementing State Management"
    """
    user_story: str
    tasks: List[Task]
    current_task: Optional[Task]
    backend_code: Dict[str, str]
    frontend_code: Dict[str, str]
    test_code: Dict[str, str]
    messages: Annotated[Sequence[str], operator.add]
    final_output: Optional[Dict[str, Any]]


# ---------------------------------------------------------------------------
# §9.4 — Self-Improving Agent Models
# ---------------------------------------------------------------------------

class AdaptationType(str, Enum):
    """
    Categorizes the type of behavioral adaptation the planner agent
    can propose. Each type maps to a distinct modification mechanism
    in the Learning Layer.

    Ref: §9.4, "Learning Mechanisms and Feedback Translation"
    """
    PROMPT_UPDATE = "prompt_update"
    THRESHOLD_ADJUSTMENT = "threshold_adjustment"
    RETRIEVAL_STRATEGY = "retrieval_strategy"
    TOOL_REORDERING = "tool_reordering"


class ImprovementHypothesis(BaseModel):
    """
    A structured proposal from the planner agent for improving agent
    behavior. Each hypothesis carries explicit evidence and confidence
    metrics to support the HITL review checkpoint.

    Ref: §9.4, "Learning Mechanisms and Feedback Translation"
    """
    source_signal: str = Field(
        description="Feedback pattern that triggered this hypothesis"
    )
    adaptation_type: AdaptationType
    proposed_change: str = Field(
        description="Specific modification to agent behavior"
    )
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_count: int = Field(
        description="Number of feedback instances supporting this"
    )
    rollback_safe: bool = Field(default=True)


class PlannerOutput(BaseModel):
    """
    Aggregated output from the planner agent after processing a batch
    of feedback from the critic agent. The 'requires_human_review'
    flag determines routing at the HITL checkpoint in Figure 9.5.

    Ref: §9.4, "Learning Mechanisms and Feedback Translation"
    """
    hypotheses: List[ImprovementHypothesis]
    requires_human_review: bool = Field(
        description="True if any hypothesis exceeds risk threshold"
    )
    baseline_metrics: dict


# ---------------------------------------------------------------------------
# §9.4 — Feedback Record (Sensing Layer input)
# ---------------------------------------------------------------------------

class FeedbackRecord(BaseModel):
    """
    A single feedback signal captured by the Sensing Layer.

    source_type must be one of: 'explicit', 'implicit', 'synthetic'.
    These three channels correspond to the multi-modal feedback
    collection described in Figure 9.5.

    Ref: §9.4, "Architectural Principles: The Closed-Loop Control System"
    """
    source_type: str = Field(
        description="One of: explicit, implicit, synthetic"
    )
    signal: str = Field(
        description="The feedback content or metric value"
    )
    timestamp: str = Field(
        description="ISO-8601 timestamp of feedback collection"
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)
