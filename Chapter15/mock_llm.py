# =============================================================================
# utils/mock_llm.py — Simulation-Mode LLM with Section-Mapped Response Registry
# Chapter 15: Education and Knowledge Agents
# Book: 30 Agents Every AI Engineer Must Build (Packt Publishing)
# Author: Imran Ahmad
#
# Design Philosophy (§6):
#   The MockLLM is a context-aware response registry — not a random text
#   generator. Each response is mapped to a specific chapter section,
#   educationally accurate, and structurally realistic.
#
# Registry Keys (9 total):
#   feedback_generator    — pp. 22–24  Tutor feedback with error localization
#   misconception_detect  — pp. 22, 24 JSON misconception diagnosis
#   propose_pedagogy      — pp. 27–28  Pedagogy specialist rubric proposal
#   propose_domain        — pp. 27–28  Domain expert rubric proposal
#   propose_assessment    — pp. 27–28  Assessment specialist rubric proposal
#   evaluate_proposal     — pp. 28–29  4-dimension structured scoring
#   adversarial_critic    — pp. 31–32  Deliberately harsh critique
#   synthesize_consensus  — pp. 33–34  Hybrid rubric with provenance trail
#   cross_pollination     — pp. 38–39  Novel criterion from combined proposals
# =============================================================================

import re
from utils.resilience import ColorLogger

logger = ColorLogger("MockLLM")


class MockLLM:
    """Simulation-mode LLM that returns pre-authored, section-mapped responses.

    Compatible interface: exposes .generate(prompt: str) -> str, matching
    the LiveLLM wrapper around OpenAI. This allows seamless swapping via
    the get_llm_client() factory (§9).

    Attributes:
        _registry: Dict mapping string keys to pre-authored response strings.
        _call_count: Running tally of generate() invocations for tracing.

    Example:
        >>> llm = MockLLM()
        >>> response = llm.generate("You are an expert Python tutor...")
        >>> assert "break" in response  # feedback_generator key matched
    """

    def __init__(self):
        self._registry: dict[str, str] = self._build_registry()
        self._call_count: int = 0

    def generate(self, prompt: str, **kwargs) -> str:
        """Route prompt to the best matching mock response.

        Args:
            prompt: The full prompt string (system + user content).
            **kwargs: Ignored in mock mode (temperature, max_tokens, etc.).

        Returns:
            Pre-authored response string matched by keyword classification.
        """
        self._call_count += 1
        response_key = self._match_prompt(prompt)
        response = self._registry.get(response_key, self._default_response(prompt))
        logger.info(
            f"Call #{self._call_count} routed to mock key '{response_key}' "
            f"(length={len(response)} chars)"
        )
        return response

    def _match_prompt(self, prompt: str) -> str:
        """Classify prompt to a registry key using keyword matching.

        Uses an ordered rule list where each rule requires at least the
        first 2 keywords to be present in the lowercased prompt. First
        match wins.

        Args:
            prompt: Raw prompt string.

        Returns:
            Registry key string, or 'default' if no rule matches.
        """
        prompt_lower = prompt.lower()
        rules = [
            ("feedback_generator",
             ["expert python tutor", "student is working on", "generate feedback"]),
            ("misconception_detect",
             ["misconception", "diagnose", "error pattern"]),
            ("propose_pedagogy",
             ["pedagogy specialist", "propose a solution", "scaffolding"]),
            ("propose_domain",
             ["domain expert", "algorithm correctness", "propose a solution"]),
            ("propose_assessment",
             ["assessment specialist", "rubric validity", "propose a solution"]),
            ("evaluate_proposal",
             ["evaluate", "proposal", "score each dimension"]),
            ("adversarial_critic",
             ["adversarial", "critic", "weaknesses"]),
            ("synthesize_consensus",
             ["synthesize", "consensus", "final"]),
            ("cross_pollination",
             ["strongest elements", "competing proposals", "novel combinations"]),
        ]
        for key, keywords in rules:
            if all(kw in prompt_lower for kw in keywords[:2]):
                return key
        return "default"

    def _default_response(self, prompt: str) -> str:
        """Fallback response when no registry key matches.

        Args:
            prompt: The unmatched prompt (first 60 chars shown in output).

        Returns:
            Informational mock response indicating simulation mode.
        """
        return (
            f"[MOCK] Simulated response for prompt pattern: "
            f"'{prompt[:60].strip()}...'\n"
            f"Note: Running in Simulation Mode. Connect an API key "
            f"for generative responses."
        )

    def _build_registry(self) -> dict[str, str]:
        """Build the complete section-mapped response registry.

        Returns:
            Dictionary with 9 keys, each containing a pre-authored,
            educationally accurate response string (150–400 words).

        Registry Reference (§6):
            Each response is authored to match the prompt patterns defined
            in _match_prompt(), be educationally accurate per the chapter
            content, and include correct structural elements (JSON for
            misconceptions, markdown for proposals, scoring for evaluations).
        """
        return {

            # ── pp. 22–24: FeedbackGenerator Tutor Response ─────────────
            "feedback_generator": (
                "Great effort on this exercise! You've correctly identified that "
                "you need to iterate through the list and accumulate a sum, which "
                "shows solid understanding of loop mechanics.\n\n"
                "However, look at where your `break` statement executes relative "
                "to the accumulation step. Right now, the `break` triggers before "
                "the current element is added to `total`, which means the last "
                "valid even number is skipped.\n\n"
                "Try tracing through this example: `nums = [2, 4, -1, 6]`\n"
                "- Iteration 1: num=2, even? Yes → total=2\n"
                "- Iteration 2: num=4, even? Yes → total=6\n"
                "- Iteration 3: num=-1, negative? Yes → break\n\n"
                "Question: What should `total` be at the end? And what does your "
                "current code produce instead?\n\n"
                "This is a common control-flow ordering misconception — the "
                "relative position of `break` vs. the accumulation statement "
                "matters. The fix involves reordering just two lines. Try moving "
                "the `break` check to execute after the accumulation, or guard "
                "the break with the negative check before processing.\n\n"
                "Misconception note: This relates to the 'control_flow_ordering' "
                "pattern — students often place early-exit logic before the "
                "operation they want to complete on the current iteration."
            ),

            # ── pp. 22, 24: Misconception Detection (JSON) ──────────────
            "misconception_detect": (
                '{"misconception_id": "ctrl_flow_break_placement", '
                '"confidence": 0.82, '
                '"description": "Student places break/continue before the '
                'operation that should execute on the current iteration, '
                'causing off-by-one or skipped-element errors.", '
                '"related_objectives": ["loop_termination", "control_flow_ordering"], '
                '"evidence": "break statement at line 4 precedes accumulation at line 5", '
                '"suggested_remediation": "trace_exercise", '
                '"remediation_detail": "Have student trace through [2, 4, -1, 6] '
                'step by step, writing total after each iteration. Compare '
                'expected vs. actual output to reveal the ordering issue."}'
            ),

            # ── pp. 27–28, 36: Pedagogy Specialist Proposal ─────────────
            "propose_pedagogy": (
                "## Rubric Proposal: Process-Oriented Assessment\n"
                "**Agent: Pedagogy Specialist**\n"
                "**Confidence: 0.75**\n\n"
                "### Weighting\n"
                "- Problem-Solving Strategy: 40%\n"
                "- Correctness: 30%\n"
                "- Code Readability & Style: 30%\n\n"
                "### Criteria (5 total)\n"
                "1. **Decomposition** — Student breaks problem into sub-problems "
                "before coding (10 pts)\n"
                "2. **Algorithm Selection** — Chosen approach is appropriate for "
                "the problem constraints (10 pts)\n"
                "3. **Correctness** — Code produces expected output for standard "
                "and edge cases (10 pts)\n"
                "4. **Readability** — Variable names are meaningful, logic is "
                "clearly structured (10 pts)\n"
                "5. **Self-Monitoring** — Student can explain their reasoning and "
                "identify potential failure points (10 pts)\n\n"
                "### Scaffolding Notes\n"
                "This rubric prioritizes the problem-solving process over pure "
                "output correctness. Research shows that process-oriented feedback "
                "produces deeper learning transfer than outcome-only grading "
                "(Black & Wiliam, 1998).\n\n"
                "### Uncertainty\n"
                "Inter-rater reliability on 'Decomposition' and 'Self-Monitoring' "
                "criteria may be low without detailed anchor descriptions. "
                "Recommend calibration sessions with sample student work."
            ),

            # ── pp. 27–28, 36: Domain Expert Proposal ───────────────────
            "propose_domain": (
                "## Rubric Proposal: Technical Rigor Assessment\n"
                "**Agent: Domain Expert (Algorithms & Data Structures)**\n"
                "**Confidence: 0.82**\n\n"
                "### Weighting\n"
                "- Correctness (incl. edge cases): 50%\n"
                "- Efficiency: 30%\n"
                "- Code Style: 20%\n\n"
                "### Criteria (7 total, 100 pts)\n"
                "1. **Functional Correctness** — Passes all standard test cases "
                "(20 pts)\n"
                "2. **Edge Case Handling** — Empty input, single element, "
                "duplicates, negative values (15 pts)\n"
                "3. **Time Complexity** — Meets O(n+m) merge requirement, no "
                "unnecessary nested loops (15 pts)\n"
                "4. **Space Complexity** — No wasteful auxiliary data structures "
                "(10 pts)\n"
                "5. **No Built-in Sort** — Solution implements merge logic "
                "manually (10 pts)\n"
                "6. **Variable Naming** — Descriptive names; no single-letter "
                "variables except loop counters (10 pts)\n"
                "7. **Documentation** — Docstring with parameters, return type, "
                "and complexity annotation (20 pts)\n\n"
                "### Partial Credit Rules\n"
                "- Criteria 1–2: Binary (pass/fail per test case)\n"
                "- Criteria 3–7: 3-point scale (0=absent, half=partial, full=complete)\n\n"
                "### Uncertainty\n"
                "Partial credit rules for criteria 3–5 are ambiguous. A student "
                "who uses `sorted()` as a fallback after attempting manual merge "
                "is hard to score fairly."
            ),

            # ── pp. 27–28, 36: Assessment Specialist Proposal ───────────
            "propose_assessment": (
                "## Rubric Proposal: Binary Reliability Assessment\n"
                "**Agent: Assessment Specialist**\n"
                "**Confidence: 0.78**\n\n"
                "### Design Principle\n"
                "Maximize inter-rater reliability by using binary (pass/fail) "
                "criteria only. Each criterion is unambiguously testable.\n\n"
                "### Criteria (5 total, pass/fail each)\n"
                "1. **Handles Empty Input** — `merge_sorted([], [1,2])` returns "
                "`[1,2]` without error (PASS/FAIL)\n"
                "2. **Maintains Sort Order** — Output is sorted for all provided "
                "test cases (PASS/FAIL)\n"
                "3. **Meets Complexity Target** — Runs in O(n+m) verified by "
                "step counter or analysis (PASS/FAIL)\n"
                "4. **No Built-in Sort Used** — Source code contains no calls to "
                "`sort()`, `sorted()`, or equivalent (PASS/FAIL)\n"
                "5. **Has Docstring** — Function includes a docstring with at "
                "least parameter descriptions (PASS/FAIL)\n\n"
                "### Scoring\n"
                "Total = count(PASS) / 5 × 100%\n\n"
                "### Uncertainty\n"
                "Binary scoring discards signal about partial understanding. A "
                "student who handles 3/4 edge cases gets the same score as one "
                "who handles 0/4. Consider a 3-point scale (Absent / Partial / "
                "Complete) as a middle ground."
            ),

            # ── pp. 28–29: Evaluation Scoring ───────────────────────────
            "evaluate_proposal": (
                "## Proposal Evaluation\n\n"
                "### Dimension Scores\n"
                "| Dimension     | Score | Rationale |\n"
                "|---------------|-------|-----------|\n"
                "| Correctness   | 7/10  | Covers core requirements but "
                "ambiguous on partial credit |\n"
                "| Completeness  | 6/10  | Missing explicit edge-case "
                "enumeration for boundary inputs |\n"
                "| Feasibility   | 8/10  | Straightforward to implement in "
                "existing LMS grading workflow |\n"
                "| Risks         | 5/10  | Inter-rater reliability untested; "
                "'strategy' criterion is subjective |\n\n"
                "### Overall Score: 6.5/10\n\n"
                "### Key Recommendation\n"
                "Add anchor examples for each criterion to reduce scoring "
                "variance between different graders. The 'Self-Monitoring' "
                "criterion needs an observable behavioral indicator (e.g., "
                "'student identifies at least one failure mode in written "
                "reflection')."
            ),

            # ── pp. 31–32: Adversarial Critic ───────────────────────────
            "adversarial_critic": (
                "## Adversarial Critique\n\n"
                "### Critical Weaknesses Identified\n\n"
                "**1. Unfalsifiable 'Strategy' Criterion**\n"
                "The 'Problem-Solving Strategy' criterion (40% weight in the "
                "Pedagogy proposal) has no observable anchor. Any student who "
                "writes working code can retroactively claim they 'decomposed' "
                "the problem. Without a required planning artifact (pseudocode, "
                "diagram), this criterion measures self-report, not skill.\n\n"
                "**2. Penalizing Correct-but-Suboptimal Solutions**\n"
                "The Domain Expert's O(n+m) requirement (criterion 3) fails "
                "students who produce correct O(n log n) solutions. In a "
                "learning context, correctness should dominate efficiency unless "
                "the exercise explicitly targets algorithmic complexity.\n\n"
                "**3. Binary Scoring Discards Signal**\n"
                "The Assessment Specialist's pass/fail model collapses a "
                "5-dimensional space into 5 bits. A student handling 3/4 edge "
                "cases is indistinguishable from one handling 0/4. This is "
                "acceptable for certification but destructive for formative "
                "assessment where the goal is to identify specific gaps.\n\n"
                "### Recommendation\n"
                "Adopt a **3-point scale** (Absent=0, Partial=1, Complete=2) "
                "across all criteria. This preserves inter-rater reliability "
                "while capturing partial understanding.\n\n"
                "### Overall Score: 5.5/10\n"
                "(Deliberately harsh — this is the adversarial critic's role.)"
            ),

            # ── pp. 33–34: Consensus Synthesis ──────────────────────────
            "synthesize_consensus": (
                "## Synthesized Consensus Rubric\n\n"
                "### Final Rubric: Hybrid Assessment (5 Criteria × 3-Point Scale)\n\n"
                "| # | Criterion | Absent (0) | Partial (1) | Complete (2) | Source |\n"
                "|---|-----------|------------|-------------|--------------|--------|\n"
                "| 1 | Functional Correctness | No output or crashes | Passes "
                "≥50% test cases | Passes all test cases incl. edge cases | "
                "Domain Expert §1–2 |\n"
                "| 2 | Algorithmic Approach | No discernible strategy | "
                "Reasonable approach, suboptimal complexity | O(n+m) merge "
                "implemented correctly | Domain Expert §3 + Pedagogy §1 |\n"
                "| 3 | Code Quality | No names, no structure | Partial naming, "
                "some structure | Meaningful names, clear logic, documented | "
                "Domain Expert §6–7 + Pedagogy §4 |\n"
                "| 4 | Edge Case Awareness | No edge cases considered | "
                "Handles empty input OR duplicates | Handles empty, single, "
                "duplicate, negative | Assessment §1 + Domain Expert §2 |\n"
                "| 5 | Self-Monitoring | No reflection | Identifies ≥1 "
                "limitation | Identifies limitations + proposes fixes | "
                "Pedagogy §5 + Adversarial feedback |\n\n"
                "### Scoring\n"
                "Total = sum(criteria) / 10 × 100%\n"
                "Mastery threshold: ≥70%\n\n"
                "### Provenance Trail\n"
                "- Criteria structure: Assessment Specialist (binary → expanded "
                "to 3-point per Adversarial recommendation)\n"
                "- Scale design: Pedagogy Specialist (process emphasis retained)\n"
                "- Technical rigor: Domain Expert (edge cases, complexity)\n"
                "- Calibration: Adversarial Critic (eliminated unfalsifiable "
                "criteria, added observable anchors)\n\n"
                "### Consensus Score: 7.8/10\n"
                "All three agents agree this hybrid addresses their core "
                "concerns. Remaining disagreement: weight of 'Self-Monitoring' "
                "(Pedagogy wants 25%, Domain Expert wants 10%)."
            ),

            # ── pp. 38–39: Cross-Pollination ────────────────────────────
            "cross_pollination": (
                "## Cross-Pollination: Novel Diagnostic-Trace Criterion\n\n"
                "### Synthesis\n"
                "By combining the Domain Expert's emphasis on edge-case coverage "
                "with the Pedagogy Specialist's process-oriented approach, a "
                "novel criterion emerges:\n\n"
                "**Diagnostic Trace** — Student demonstrates understanding by "
                "tracing their solution through a failing edge case step-by-step, "
                "identifying exactly where and why the output diverges from "
                "expectation.\n\n"
                "### Scoring Anchor\n"
                "- **Absent (0):** No trace provided or trace is incorrect\n"
                "- **Partial (1):** Trace is correct but stops before identifying "
                "the root cause\n"
                "- **Complete (2):** Trace correctly identifies the divergence "
                "point and proposes a fix\n\n"
                "### Why This Is Novel\n"
                "Neither the Domain Expert (who focuses on output correctness) "
                "nor the Pedagogy Specialist (who focuses on planning process) "
                "proposed a criterion that assesses debugging-as-understanding. "
                "This criterion bridges both perspectives: it requires technical "
                "precision (Domain) applied to a reflective exercise (Pedagogy).\n\n"
                "### TRIZ Connection (Ch.15, p. 39)\n"
                "This is an example of TRIZ-inspired constraint relaxation: "
                "instead of asking 'does the code work?' (product) or 'did the "
                "student plan?' (process), we ask 'can the student diagnose "
                "failure?' — which tests both simultaneously.\n\n"
                "### Confidence: 0.71\n"
                "(Novel criterion — untested in practice. Recommend piloting "
                "with 2–3 student submissions before full deployment.)"
            ),
        }
