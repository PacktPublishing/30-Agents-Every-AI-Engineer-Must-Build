"""
mock_engine.py — Mock LLM and Simulation Backends for Chapter 17
Book: AI Agents by Imran Ahmad (Packt, 2025)
Chapter: 17 — Epilogue: The Future of Intelligent Agents

Provides:
  - MockLLM: Keyword-routed text generation mock
  - ArchitectureRegistrySimulator: Self-architecting agent (pp. 1-2)
  - AgentSocietySimulator: DeGroot consensus & specialization (pp. 2-3)
  - EthicalCircuitBreakerSimulator: Drift detection & graduated response (pp. 3-4)
  - MemoryConsolidationSimulator: Episodic → semantic transfer (pp. 4-6)
  - CollaborationSpectrumSimulator: Task routing spectrum (pp. 6-8)

All data is synthetic and derived from specific chapter content.
Author: Imran Ahmad
"""

import random
import numpy as np
from collections import defaultdict
from resilience import ColorLogger

random.seed(42)
np.random.seed(42)


# ---------------------------------------------------------------------------
# MockLLM — Keyword-routed text generation mock
# ---------------------------------------------------------------------------

class MockLLM:
    """
    Context-aware mock language model.
    Routes queries by keyword matching to chapter-faithful responses.
    Author: Imran Ahmad
    """

    RESPONSE_REGISTRY = {
        "architecture": (
            "[SIMULATION MODE] The meta-optimization search evaluated 6 candidate "
            "pipelines from the architecture registry. Pipeline 'ReAct-v3 + FAISS-memory "
            "+ code-interpreter' scored highest on P(a) = 0.91 while satisfying all "
            "alignment constraints in set C. The unconstrained optimizer scored P(a) = 0.96 "
            "but violated alignment constraint C_3 (unrestricted shell execution). "
            "Recommendation: adopt ReAct-v3 pipeline. "
            "(Ref: Ch.17, pp.1-2, 'Autonomous agent evolution and adaptation')"
        ),
        "society": (
            "[SIMULATION MODE] After 20 rounds of DeGroot weighted belief averaging, "
            "the 5-agent society converged to consensus belief vector "
            "[0.72, 0.74, 0.71, 0.73, 0.72]. Agent-3 emerged as the dominant specialist "
            "in 'code-review' tasks (reputation: 0.94) via comparative advantage. "
            "Agent-1 specialized in 'research' (reputation: 0.89). "
            "(Ref: Ch.17, pp.2-3, 'Agent societies and emergent behaviors')"
        ),
        "ethics": (
            "[SIMULATION MODE] Behavioral drift detected across 4 phases. "
            "KS statistic escalated from 0.08 to 0.55. Graduated response triggered: "
            "Phase 1 → log alert, Phase 2 → increased oversight, "
            "Phase 3 → autonomy restricted, Phase 4 → full halt. "
            "(Ref: Ch.17, pp.3-4, 'Agent governance and self-regulation')"
        ),
        "drift": (
            "[SIMULATION MODE] KS divergence = 0.38, p-value < 0.001. "
            "Behavioral distribution has shifted significantly from baseline. "
            "Circuit breaker Level 3 activated: restricting to pre-approved actions. "
            "(Ref: Ch.17, pp.3-4, 'Agent governance and self-regulation')"
        ),
        "memory": (
            "[SIMULATION MODE] Consolidation batch complete. 12 episodes replayed, "
            "4 generalizable patterns extracted to semantic memory, 8 fully consolidated "
            "episodes pruned. Analogical transfer: 'retry-with-backoff' generalized from "
            "API-call domain to database-connection domain. "
            "(Ref: Ch.17, pp.5-6, 'Episodic memory architectures')"
        ),
        "consolidation": (
            "[SIMULATION MODE] Memory consolidation cycle: replay → extract → prune. "
            "Hippocampal-inspired fast-learning store transferred patterns to neocortical "
            "slow-learning store. 4 patterns now in semantic memory. "
            "(Ref: Ch.17, pp.5-6, 'Brain-inspired cognitive architectures')"
        ),
        "collaboration": (
            "[SIMULATION MODE] Task routing complete. 15 tasks classified: "
            "9 autonomous (routine), 4 collaborative (complex multi-step), "
            "2 escalated to human (high-stakes). Estimated efficiency gain: 74%. "
            "Modeled after Quandri case study: 99.9% accuracy, <15 min processing. "
            "(Ref: Ch.17, pp.7-8, 'The evolving relationship between humans and AI')"
        ),
        "roadmap": (
            "[SIMULATION MODE] Organization assessed at 'Walk' phase of crawl-walk-run "
            "maturity model. Recommendation: introduce planning agents for multi-step "
            "workflows before advancing to learning agents and multi-agent coordination. "
            "(Ref: Ch.17, p.6, 'Building agent capability roadmaps')"
        ),
    }

    @staticmethod
    def generate(prompt: str) -> str:
        """Route prompt to best-matching mock response by keyword."""
        prompt_lower = prompt.lower()
        for keyword, response in MockLLM.RESPONSE_REGISTRY.items():
            if keyword in prompt_lower:
                return response
        return (
            "[SIMULATION MODE] MockLLM: No specific handler matched for this prompt. "
            "Returning generic acknowledgment for Chapter 17 concepts. "
            "(Ref: Ch.17, Epilogue overview)"
        )


# ---------------------------------------------------------------------------
# Simulator 1: ArchitectureRegistrySimulator — pp. 1-2
# ---------------------------------------------------------------------------

class ArchitectureRegistrySimulator:
    """
    Simulates self-architecting agent searching an architecture registry.
    Ref: Ch.17, pp.1-2, 'Autonomous agent evolution and adaptation'

    Key concept: meta-optimization over space A, maximizing P(a) subject
    to alignment constraints a ∈ C.
    Author: Imran Ahmad
    """

    def __init__(self):
        self.registry = [
            {
                "name": "ReAct-v3 + FAISS-Memory + CodeInterpreter",
                "modules": {"planner": "ReAct-v3", "memory": "FAISS", "tool": "CodeInterpreter"},
                "performance": 0.91,
                "alignment_compliant": True,
                "notes": "Strong balance of performance and safety"
            },
            {
                "name": "CoT-Basic + NoMemory + WebSearch",
                "modules": {"planner": "CoT-Basic", "memory": "None", "tool": "WebSearch"},
                "performance": 0.65,
                "alignment_compliant": True,
                "notes": "Minimal but safe; suitable for simple tasks"
            },
            {
                "name": "Unconstrained-Optimizer + VectorDB + ShellExec",
                "modules": {"planner": "Unconstrained-Opt", "memory": "VectorDB", "tool": "ShellExec"},
                "performance": 0.96,
                "alignment_compliant": False,
                "notes": "HIGHEST raw score but VIOLATES alignment constraint C_3 (unrestricted shell)"
            },
            {
                "name": "PlanAndSolve + EpisodicMemory + APIToolkit",
                "modules": {"planner": "PlanAndSolve", "memory": "Episodic", "tool": "APIToolkit"},
                "performance": 0.84,
                "alignment_compliant": True,
                "notes": "Good episodic memory integration"
            },
            {
                "name": "TreeOfThought + HybridMemory + SandboxedExec",
                "modules": {"planner": "TreeOfThought", "memory": "Hybrid", "tool": "SandboxedExec"},
                "performance": 0.88,
                "alignment_compliant": True,
                "notes": "ToT planner with sandboxed execution"
            },
            {
                "name": "MCTS-Planner + GraphMemory + UnfilteredNet",
                "modules": {"planner": "MCTS", "memory": "GraphDB", "tool": "UnfilteredNet"},
                "performance": 0.93,
                "alignment_compliant": False,
                "notes": "Violates C_1 (unfiltered network access)"
            },
        ]

    def get_registry(self):
        """Return the full architecture catalog."""
        return self.registry

    def search_optimal(self):
        """
        Filter by alignment compliance, rank by P(a), return the best.
        Demonstrates: the highest raw scorer (0.96) is excluded by constraints.
        """
        compliant = [p for p in self.registry if p["alignment_compliant"]]
        compliant.sort(key=lambda x: x["performance"], reverse=True)
        winner = compliant[0]

        ColorLogger.simulation(
            f"Architecture search complete. Evaluated {len(self.registry)} candidates, "
            f"{len(compliant)} passed alignment filter."
        )
        ColorLogger.success(
            f"Optimal pipeline: '{winner['name']}' with P(a) = {winner['performance']}"
        )

        # Log the excluded high-scorers to illustrate the alignment stability problem
        excluded = [p for p in self.registry if not p["alignment_compliant"]]
        for ex in excluded:
            ColorLogger.info(
                f"EXCLUDED: '{ex['name']}' — P(a) = {ex['performance']} "
                f"but violates alignment constraints. Reason: {ex['notes']}"
            )

        return winner

    def evaluate_candidate(self, name):
        """Return detailed breakdown for a named pipeline."""
        for p in self.registry:
            if p["name"] == name:
                return p
        return None


# ---------------------------------------------------------------------------
# Simulator 2: AgentSocietySimulator — pp. 2-3
# ---------------------------------------------------------------------------

class AgentSocietySimulator:
    """
    Simulates emergent agent society with DeGroot belief convergence,
    reputation ledgers, and spontaneous specialization.
    Ref: Ch.17, pp.2-3, 'Agent societies and emergent behaviors'
    Author: Imran Ahmad
    """

    def __init__(self):
        self.agent_names = ["Agent-0 (Analyst)", "Agent-1 (Researcher)",
                           "Agent-2 (Planner)", "Agent-3 (Coder)",
                           "Agent-4 (Reviewer)"]
        # Initial diverse beliefs (representing positions on a strategic decision)
        self.initial_beliefs = np.array([0.2, 0.9, 0.5, 0.7, 0.3])

        # Trust matrix (row i = how much agent i trusts each other agent)
        # Rows sum to 1. Asymmetric trust creates interesting dynamics.
        self.trust_matrix = np.array([
            [0.30, 0.25, 0.20, 0.15, 0.10],
            [0.15, 0.30, 0.20, 0.20, 0.15],
            [0.20, 0.20, 0.25, 0.20, 0.15],
            [0.10, 0.15, 0.15, 0.35, 0.25],
            [0.15, 0.20, 0.20, 0.20, 0.25],
        ])

        # Skill scores per task type (for specialization detection)
        self.skill_scores = {
            "Agent-0": {"analysis": 0.88, "research": 0.60, "coding": 0.45, "review": 0.55},
            "Agent-1": {"analysis": 0.65, "research": 0.92, "coding": 0.50, "review": 0.60},
            "Agent-2": {"analysis": 0.70, "research": 0.68, "coding": 0.55, "review": 0.65},
            "Agent-3": {"analysis": 0.50, "research": 0.55, "coding": 0.95, "review": 0.70},
            "Agent-4": {"analysis": 0.60, "research": 0.62, "coding": 0.60, "review": 0.94},
        }

    def run_degroot_convergence(self, rounds=20):
        """
        Simulate DeGroot belief convergence via iterated weighted averaging.
        Returns list of belief vectors per round.
        """
        beliefs = self.initial_beliefs.copy()
        trajectory = [beliefs.copy()]

        for r in range(rounds):
            beliefs = self.trust_matrix @ beliefs
            trajectory.append(beliefs.copy())

            if r % 5 == 0 or r == rounds - 1:
                belief_str = ", ".join([f"{b:.3f}" for b in beliefs])
                ColorLogger.info(f"Round {r+1}: beliefs = [{belief_str}]")

        ColorLogger.success(
            f"Convergence complete after {rounds} rounds. "
            f"Final consensus region: [{beliefs.min():.3f}, {beliefs.max():.3f}]"
        )
        return trajectory

    def compute_reputation_ledger(self):
        """
        Compute per-agent, per-task reputation based on skill scores.
        Simulates a distributed reputation ledger (Ref: p.3).
        """
        ledger = {}
        for agent, skills in self.skill_scores.items():
            ledger[agent] = {
                "skills": skills,
                "best_task": max(skills, key=skills.get),
                "best_score": max(skills.values()),
            }
            ColorLogger.info(
                f"{agent}: best at '{ledger[agent]['best_task']}' "
                f"(score: {ledger[agent]['best_score']:.2f})"
            )
        return ledger

    def detect_specialization(self):
        """
        Assign roles based on comparative advantage (not absolute advantage).
        Returns dict of task → assigned agent.
        """
        tasks = ["analysis", "research", "coding", "review"]
        assignments = {}
        assigned_agents = set()

        # Greedy assignment by highest score per task (simplified comparative advantage)
        task_scores = []
        for task in tasks:
            for agent, skills in self.skill_scores.items():
                task_scores.append((skills[task], agent, task))
        task_scores.sort(reverse=True)

        for score, agent, task in task_scores:
            if task not in assignments and agent not in assigned_agents:
                assignments[task] = {"agent": agent, "score": score}
                assigned_agents.add(agent)

        for task, info in assignments.items():
            ColorLogger.success(
                f"Spontaneous specialization: '{task}' → {info['agent']} "
                f"(reputation: {info['score']:.2f})"
            )

        return assignments


# ---------------------------------------------------------------------------
# Simulator 3: EthicalCircuitBreakerSimulator — pp. 3-4
# ---------------------------------------------------------------------------

class EthicalCircuitBreakerSimulator:
    """
    Simulates behavioral drift detection and graduated ethical response.
    Ref: Ch.17, pp.3-4, 'Agent governance and self-regulation'

    Four escalation levels from the text:
      Level 1: Log alert
      Level 2: Increase human oversight
      Level 3: Restrict autonomy to pre-approved actions
      Level 4: Halt operation
    Author: Imran Ahmad
    """

    RESPONSE_LEVELS = {
        1: {"name": "Log Alert", "action": "Logging anomaly for review. Agent continues normally."},
        2: {"name": "Increase Oversight", "action": "Human-in-the-loop activated for next 10 decisions."},
        3: {"name": "Restrict Autonomy", "action": "Agent restricted to pre-approved action set only."},
        4: {"name": "Halt Operation", "action": "FULL HALT. Agent suspended pending human review."},
    }

    KS_THRESHOLDS = {
        1: 0.10,   # Minor drift   (Phase 1 KS ≈ 0.35)
        2: 0.40,   # Moderate drift (Phase 2 KS ≈ 0.57)
        3: 0.60,   # Severe drift   (Phase 3 KS ≈ 0.89)
        4: 0.92,   # Critical drift (Phase 4 KS ≈ 0.97)
    }

    def __init__(self):
        # Reset seed for deterministic cascade regardless of prior state
        np.random.seed(42)
        # Baseline behavioral distribution
        self.baseline = np.random.normal(loc=0.5, scale=0.1, size=200)

        # Four drift phases with progressively shifted distributions
        self.drift_phases = {
            "Phase 1 — Minor Drift":    np.random.normal(loc=0.55, scale=0.1, size=50),
            "Phase 2 — Moderate Drift":  np.random.normal(loc=0.65, scale=0.12, size=50),
            "Phase 3 — Severe Drift":    np.random.normal(loc=0.80, scale=0.15, size=50),
            "Phase 4 — Critical Drift":  np.random.normal(loc=1.05, scale=0.18, size=50),
        }

    def compute_ks_divergence(self, phase_data):
        """Compute KS statistic between baseline and given phase data."""
        from scipy import stats
        ks_stat, p_value = stats.ks_2samp(self.baseline, phase_data)
        return ks_stat, p_value

    def evaluate_response_level(self, ks_stat):
        """Determine graduated response level based on KS statistic."""
        level = 1
        for lvl, threshold in sorted(self.KS_THRESHOLDS.items()):
            if ks_stat >= threshold:
                level = lvl
        return level, self.RESPONSE_LEVELS[level]

    def run_full_cascade(self):
        """
        Step through all 4 drift phases, computing KS divergence and
        triggering the appropriate graduated response at each phase.
        Demonstrates the FULL escalation path from the text.
        """
        results = []
        ColorLogger.section("Ethical Circuit Breaker — Full Cascade Simulation")
        ColorLogger.info("Baseline distribution: N(0.5, 0.1), n=200 samples")

        for phase_name, phase_data in self.drift_phases.items():
            ks_stat, p_value = self.compute_ks_divergence(phase_data)
            level, response = self.evaluate_response_level(ks_stat)

            result = {
                "phase": phase_name,
                "ks_statistic": round(ks_stat, 4),
                "p_value": round(p_value, 6),
                "response_level": level,
                "response_name": response["name"],
                "action": response["action"],
            }
            results.append(result)

            # Color-coded output based on severity
            if level <= 1:
                ColorLogger.info(
                    f"{phase_name}: KS = {ks_stat:.4f} → Level {level}: {response['name']}"
                )
            elif level <= 2:
                ColorLogger.info(
                    f"{phase_name}: KS = {ks_stat:.4f} → Level {level}: {response['name']}"
                )
            elif level <= 3:
                ColorLogger.error(
                    f"{phase_name}: KS = {ks_stat:.4f} → Level {level}: {response['name']} — "
                    f"{response['action']}"
                )
            else:
                ColorLogger.error(
                    f"{phase_name}: KS = {ks_stat:.4f} → Level {level}: {response['name']} — "
                    f"{response['action']}"
                )

        ColorLogger.simulation("Full cascade complete. All 4 escalation levels demonstrated.")
        return results


# ---------------------------------------------------------------------------
# Simulator 4: MemoryConsolidationSimulator — pp. 4-6
# ---------------------------------------------------------------------------

class MemoryConsolidationSimulator:
    """
    Simulates hippocampal-inspired episodic → semantic memory consolidation.
    Ref: Ch.17, pp.4-6, 'Brain-inspired cognitive architectures'

    Based on complementary learning systems theory (McClelland et al., 1995)
    and Wilson-McNaughton hippocampal replay research.
    Author: Imran Ahmad
    """

    def __init__(self):
        self.episodic_memory = [
            {"id": "ep_01", "event": "API call to weather service timed out",
             "context": "tool_invocation", "outcome": "retried with exponential backoff, succeeded",
             "tags": ["retry", "backoff", "api"], "consolidated": False},
            {"id": "ep_02", "event": "Parallel search across 3 databases",
             "context": "multi_tool", "outcome": "aggregated results in 1.2s",
             "tags": ["parallel", "tool_invocation"], "consolidated": False},
            {"id": "ep_03", "event": "User query answered from semantic cache",
             "context": "retrieval", "outcome": "response in 50ms, user satisfied",
             "tags": ["cache", "retrieval", "fast"], "consolidated": False},
            {"id": "ep_04", "event": "Simultaneous API calls to translate + summarize",
             "context": "multi_tool", "outcome": "combined output delivered",
             "tags": ["parallel", "tool_invocation"], "consolidated": False},
            {"id": "ep_05", "event": "Database connection pool exhausted",
             "context": "tool_invocation", "outcome": "retried with backoff after 3s, succeeded",
             "tags": ["retry", "backoff", "database"], "consolidated": False},
            {"id": "ep_06", "event": "User query too ambiguous for automated resolution",
             "context": "escalation", "outcome": "escalated to human operator, resolved",
             "tags": ["escalate", "human", "ambiguous"], "consolidated": False},
            {"id": "ep_07", "event": "Rate limit hit on external API",
             "context": "tool_invocation", "outcome": "queued and retried after cooldown",
             "tags": ["retry", "rate_limit"], "consolidated": False},
            {"id": "ep_08", "event": "Third-party service returned 503",
             "context": "tool_invocation", "outcome": "retried with backoff, succeeded on attempt 3",
             "tags": ["retry", "backoff", "api"], "consolidated": False},
            {"id": "ep_09", "event": "Insurance policy lookup from local cache",
             "context": "retrieval", "outcome": "instant retrieval, no external call needed",
             "tags": ["cache", "retrieval", "fast"], "consolidated": False},
            {"id": "ep_10", "event": "Complex multi-step claim analysis",
             "context": "reasoning", "outcome": "completed 7-step chain, all steps verified",
             "tags": ["multi_step", "reasoning"], "consolidated": False},
            {"id": "ep_11", "event": "Repeated question answered from cached embedding",
             "context": "retrieval", "outcome": "cache hit, near-zero latency",
             "tags": ["cache", "retrieval", "fast"], "consolidated": False},
            {"id": "ep_12", "event": "Ethical dilemma in automated decision",
             "context": "escalation", "outcome": "flagged and escalated to human review board",
             "tags": ["escalate", "human", "ethics"], "consolidated": False},
        ]

        # Ground-truth patterns to be extracted
        self.expected_patterns = {
            "retry-with-backoff": {
                "description": "When external calls fail, retry with exponential backoff",
                "source_episodes": ["ep_01", "ep_05", "ep_07", "ep_08"],
                "generalization": "Applies across API calls, databases, and rate-limited services"
            },
            "cache-before-call": {
                "description": "Check local/semantic cache before making external calls",
                "source_episodes": ["ep_03", "ep_09", "ep_11"],
                "generalization": "Applies to policy lookups, user queries, and repeated questions"
            },
            "escalate-to-human": {
                "description": "Route ambiguous or ethically sensitive decisions to human operators",
                "source_episodes": ["ep_06", "ep_12"],
                "generalization": "Applies to ambiguous queries and ethical dilemmas"
            },
            "parallel-tool-invocation": {
                "description": "Execute independent tool calls in parallel to reduce latency",
                "source_episodes": ["ep_02", "ep_04"],
                "generalization": "Applies to any independent multi-tool workflow"
            },
        }

        self.semantic_memory = {}

    def get_episodes(self):
        """Return all episodic memories."""
        return self.episodic_memory

    def replay_and_extract(self):
        """
        Replay episodes and extract generalizable patterns.
        Analogous to hippocampal sharp-wave ripple replay during sleep.
        """
        ColorLogger.section("Memory Consolidation — Replay & Extraction")
        ColorLogger.info("Beginning episodic replay (hippocampal sharp-wave ripple simulation)...")

        extracted = {}
        for pattern_name, pattern_info in self.expected_patterns.items():
            source_eps = [ep for ep in self.episodic_memory
                         if ep["id"] in pattern_info["source_episodes"]]
            extracted[pattern_name] = {
                "description": pattern_info["description"],
                "source_count": len(source_eps),
                "source_ids": pattern_info["source_episodes"],
                "generalization": pattern_info["generalization"],
            }
            ColorLogger.success(
                f"Pattern extracted: '{pattern_name}' from {len(source_eps)} episodes "
                f"({', '.join(pattern_info['source_episodes'])})"
            )

        ColorLogger.info(f"Extraction complete: {len(extracted)} patterns identified.")
        return extracted

    def consolidate(self):
        """
        Move extracted patterns to semantic memory, prune consolidated episodes.
        After consolidation: episodic store shrinks, semantic store grows.
        """
        extracted = self.replay_and_extract()

        # Transfer to semantic memory
        self.semantic_memory = extracted
        ColorLogger.info(f"Transferred {len(extracted)} patterns to semantic memory.")

        # Prune fully consolidated episodes
        consolidated_ids = set()
        for pattern in self.expected_patterns.values():
            consolidated_ids.update(pattern["source_episodes"])

        pre_count = len(self.episodic_memory)
        for ep in self.episodic_memory:
            if ep["id"] in consolidated_ids:
                ep["consolidated"] = True

        remaining = [ep for ep in self.episodic_memory if not ep["consolidated"]]
        pruned_count = pre_count - len(remaining)

        ColorLogger.success(
            f"Consolidation complete. Pruned {pruned_count} episodes. "
            f"Episodic: {pre_count} → {len(remaining)} | "
            f"Semantic: 0 → {len(self.semantic_memory)} patterns"
        )

        return {
            "semantic_memory": self.semantic_memory,
            "remaining_episodes": remaining,
            "pruned_count": pruned_count,
        }

    def get_memory_state(self):
        """Return current state of both memory systems."""
        remaining = [ep for ep in self.episodic_memory if not ep["consolidated"]]
        return {
            "episodic_count": len(remaining),
            "semantic_count": len(self.semantic_memory),
            "episodic_memories": remaining,
            "semantic_patterns": self.semantic_memory,
        }


# ---------------------------------------------------------------------------
# Simulator 5: CollaborationSpectrumSimulator — pp. 6-8
# ---------------------------------------------------------------------------

class CollaborationSpectrumSimulator:
    """
    Simulates dynamic task routing across autonomous/collaborative/escalation bands.
    Ref: Ch.17, pp.6-8, 'Strategic implementation' and 'The evolving relationship
    between humans and artificial intelligence'

    Incorporates Quandri case study metrics (p.7) and crawl-walk-run model (p.6).
    Author: Imran Ahmad
    """

    ROUTING_BANDS = {
        "autonomous": "Agent handles independently. No human involvement.",
        "collaborative": "Agent + human work together. Agent provides analysis, human decides.",
        "escalated": "Full context passed to human. Agent in advisory-only mode.",
    }

    def __init__(self):
        self.tasks = [
            {"id": "task_01", "desc": "Routine policy renewal lookup",
             "complexity": 0.10, "stakes": "low", "domain": "insurance"},
            {"id": "task_02", "desc": "Standard premium calculation",
             "complexity": 0.15, "stakes": "low", "domain": "insurance"},
            {"id": "task_03", "desc": "FAQ response generation",
             "complexity": 0.08, "stakes": "low", "domain": "customer_service"},
            {"id": "task_04", "desc": "Document classification and filing",
             "complexity": 0.20, "stakes": "low", "domain": "operations"},
            {"id": "task_05", "desc": "Compliance checkbox verification",
             "complexity": 0.25, "stakes": "low", "domain": "compliance"},
            {"id": "task_06", "desc": "Multi-policy bundle discount analysis",
             "complexity": 0.35, "stakes": "low", "domain": "insurance"},
            {"id": "task_07", "desc": "Cross-state regulatory compliance review",
             "complexity": 0.55, "stakes": "medium", "domain": "compliance"},
            {"id": "task_08", "desc": "Multi-step claim with subrogation analysis",
             "complexity": 0.65, "stakes": "medium", "domain": "claims"},
            {"id": "task_09", "desc": "Customer churn risk assessment and intervention",
             "complexity": 0.60, "stakes": "medium", "domain": "customer_service"},
            {"id": "task_10", "desc": "Actuarial model parameter review",
             "complexity": 0.70, "stakes": "medium", "domain": "actuarial"},
            {"id": "task_11", "desc": "New product line risk evaluation",
             "complexity": 0.72, "stakes": "medium", "domain": "product"},
            {"id": "task_12", "desc": "Fraud investigation with anomaly patterns",
             "complexity": 0.75, "stakes": "medium", "domain": "fraud"},
            {"id": "task_13", "desc": "Reinsurance treaty negotiation support",
             "complexity": 0.80, "stakes": "high", "domain": "reinsurance"},
            {"id": "task_14", "desc": "Disputed coverage on $2M commercial property",
             "complexity": 0.90, "stakes": "high", "domain": "claims"},
            {"id": "task_15", "desc": "Regulatory audit response with legal implications",
             "complexity": 0.95, "stakes": "high", "domain": "compliance"},
        ]

    def classify_task(self, task):
        """Route a single task to the appropriate collaboration band."""
        if task["complexity"] <= 0.65:
            return "autonomous"
        elif task["complexity"] > 0.85 and task["stakes"] == "high":
            return "escalated"
        else:
            return "collaborative"

    def classify_tasks(self):
        """Classify all tasks and return results with routing reasoning."""
        results = {"autonomous": [], "collaborative": [], "escalated": []}

        for task in self.tasks:
            band = self.classify_task(task)
            task_result = {**task, "band": band, "band_desc": self.ROUTING_BANDS[band]}
            results[band].append(task_result)

        # Summary logging
        ColorLogger.section("Collaboration Spectrum — Task Routing")
        for band, tasks in results.items():
            color_fn = (ColorLogger.success if band == "autonomous"
                       else ColorLogger.info if band == "collaborative"
                       else ColorLogger.error)
            for t in tasks:
                color_fn(f"[{band.upper()}] {t['id']}: {t['desc']} "
                        f"(complexity={t['complexity']:.2f}, stakes={t['stakes']})")

        ColorLogger.simulation(
            f"Routing complete: {len(results['autonomous'])} autonomous, "
            f"{len(results['collaborative'])} collaborative, "
            f"{len(results['escalated'])} escalated"
        )
        return results

    def compute_efficiency_metrics(self):
        """
        Compute Quandri-inspired performance metrics.
        Ref: Ch.17, p.7, 'Creating organizational value'
        """
        results = self.classify_tasks()
        total = len(self.tasks)
        auto_count = len(results["autonomous"])

        metrics = {
            "total_tasks": total,
            "autonomous_count": auto_count,
            "autonomous_pct": round(auto_count / total * 100, 1),
            "simulated_accuracy": 99.9,  # From Quandri case study
            "avg_processing_time_min": 12,  # Under 15 min target
            "estimated_monthly_value_usd": 30000,  # From text
            "efficiency_gain_pct": round(auto_count / total * 100, 1),
        }

        ColorLogger.success(
            f"Efficiency metrics (Quandri model): {metrics['autonomous_pct']}% autonomous, "
            f"{metrics['simulated_accuracy']}% accuracy, "
            f"~${metrics['estimated_monthly_value_usd']:,}/month value"
        )
        return metrics

    def generate_roadmap_assessment(self):
        """
        Assess organizational maturity on the crawl-walk-run model.
        Ref: Ch.17, p.6, 'Building agent capability roadmaps'
        """
        results = self.classify_tasks()
        auto_pct = len(results["autonomous"]) / len(self.tasks)

        if auto_pct < 0.3:
            phase = "Crawl"
            recommendation = ("Focus on automating well-understood, high-volume tasks. "
                            "Build observability pipelines and evaluation frameworks.")
        elif auto_pct < 0.7:
            phase = "Walk"
            recommendation = ("Introduce planning agents for complex multi-step workflows. "
                            "Expand governance processes and fairness monitoring.")
        else:
            phase = "Run"
            recommendation = ("Ready for learning agents and multi-agent coordination. "
                            "Implement continuous improvement velocity tracking.")

        assessment = {
            "current_phase": phase,
            "autonomous_ratio": round(auto_pct, 2),
            "recommendation": recommendation,
        }

        ColorLogger.simulation(
            f"Roadmap assessment: Organization is in '{phase}' phase "
            f"(autonomous ratio: {auto_pct:.0%}). {recommendation}"
        )
        return assessment
