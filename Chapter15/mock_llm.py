# ===========================================================================
# utils/mock_llm.py — MockLLM Class & Section-Mapped Response Registry
# Chapter 15: Education and Knowledge Agents
# Book: 30 Agents Every AI Engineer Must Build (Packt Publishing)
# Author: Imran Ahmad
#
# Simulation-mode LLM that returns pre-authored, educationally accurate
# responses keyed to specific chapter sections. Enables full notebook
# execution without an OpenAI API key.
#
# Ref: Strategy §6 — MockLLM Class & Response Registry
# ===========================================================================

import re
from utils.resilience import ColorLogger

logger = ColorLogger("MockLLM")


class MockLLM:
    """Simulation-mode LLM that returns pre-authored, section-mapped responses.

    Design Philosophy (Strategy §6):
        This is a context-aware response registry, not a random text generator.
        Each response is mapped to a specific chapter section, educationally
        accurate, and structurally realistic. Prompt classification uses
        keyword matching against the first two keywords in each rule.

    Registry Keys (9 total):
        feedback_generator   — pp. 22–24  Pedagogical feedback with nudge
        misconception_detect — pp. 22, 24 JSON misconception diagnosis
        propose_pedagogy     — pp. 27–28  Process-oriented rubric proposal
        propose_domain       — pp. 27–28  Technical rigor rubric proposal
        propose_assessment   — pp. 27–28  Binary reliability rubric proposal
        evaluate_proposal    — pp. 28–29  Structured 4-dimension scoring
        adversarial_critic   — pp. 31–32  Harsh critique with recommendations
        synthesize_consensus — pp. 33–34  Hybrid rubric with provenance trail
        cross_pollination    — pp. 38–39  Novel diagnostic-trace criterion
    """

    def __init__(self) -> None:
        self._registry: dict[str, str] = self._build_registry()
        self._call_count: int = 0

    def generate(self, prompt: str, **kwargs) -> str:
        """Route prompt to the best matching mock response.

        Args:
            prompt: The LLM prompt string to classify and respond to.
            **kwargs: Ignored in mock mode (accepted for API compatibility).

        Returns:
            Pre-authored response string matched to the prompt pattern.
        """
        self._call_count += 1
        response_key = self._match_prompt(prompt)
        response = self._registry.get(
            response_key, self._default_response(prompt)
        )
        logger.info(
            f"Call #{self._call_count} routed to mock key '{response_key}' "
            f"(length={len(response)} chars)"
        )
        return response

    def _match_prompt(self, prompt: str) -> str:
        """Classify prompt to a registry key using keyword matching.

        Each rule is a tuple of (key, [keyword1, keyword2, ...]). A match
        requires all of the first two keywords to be present in the prompt.
        Rules are evaluated in order; first match wins.

        Returns:
            Registry key string, or 'default' if no rule matches.
        """
        prompt_lower = prompt.lower()
        rules = [
            ("feedback_generator",
             ["expert python tutor", "student is working on",
              "generate feedback"]),
            ("misconception_detect",
             ["misconception", "diagnose", "error pattern"]),
            ("propose_pedagogy",
             ["pedagogy specialist", "propose a solution", "scaffolding"]),
            ("propose_domain",
             ["domain expert", "algorithm correctness",
              "propose a solution"]),
            ("propose_assessment",
             ["assessment specialist", "rubric validity",
              "propose a solution"]),
            ("evaluate_proposal",
             ["evaluate", "proposal", "score each dimension"]),
            ("adversarial_critic",
             ["adversarial", "critic", "weaknesses"]),
            ("synthesize_consensus",
             ["synthesize", "consensus", "final"]),
            ("cross_pollination",
             ["strongest elements", "competing proposals",
              "novel combinations"]),
        ]
        for key, keywords in rules:
            if all(kw in prompt_lower for kw in keywords[:2]):
                return key
        return "default"

    def _default_response(self, prompt: str) -> str:
        """Fallback response when no registry key matches."""
        return (
            f"[MOCK] Simulated response for prompt pattern: "
            f"'{prompt[:60].strip()}...'\n"
            f"Note: Running in Simulation Mode. Connect an API key "
            f"for generative responses."
        )

    def _build_registry(self) -> dict[str, str]:
        """Build the full section-mapped response registry.

        Each response is 150–400 words, matching realistic LLM output length.
        Content is authored to be educationally accurate and aligned with the
        specific chapter sections referenced in each key.
        """

        # --- Key: feedback_generator (pp. 22–24) ---
        # FeedbackGenerator prompt: "You are an expert Python tutor..."
        # Response follows the 4-part pedagogical contract from p. 23:
        #   1. Acknowledge correct elements
        #   2. Localize error without revealing solution
        #   3. Ask guiding question
        #   4. Address underlying misconception
        feedback_generator = (
            "Great work on the overall structure of your solution! "
            "Your use of a for loop to iterate through the list is correct, "
            "and your conditional check for even numbers using the modulo "
            "operator is well-implemented. That shows solid understanding of "
            "both iteration and conditional filtering.\n\n"
            "However, there is an issue with how the early termination "
            "condition interacts with the accumulation logic. Look at where "
            "your `break` statement executes relative to the accumulation "
            "step. The order of operations inside the loop body matters: "
            "right now, the loop may exit before processing a value that "
            "should have been included, or it may include a value that "
            "should have triggered the exit.\n\n"
            "Here is a guiding question to help you find the fix: trace "
            "through your code with `nums = [2, 4, -1, 6]`. Write down the "
            "value of `total` after each iteration. At which iteration does "
            "the behavior diverge from what you expect? Does the break "
            "execute before or after the addition?\n\n"
            "This is a common misconception related to control flow ordering. "
            "When you have multiple conditions inside a loop body, the "
            "sequence in which you check and act on them determines the "
            "program's behavior. Think of the loop body as a decision "
            "pipeline: each statement executes in order, and a `break` "
            "immediately exits — it does not finish the remaining statements "
            "in the current iteration."
        )

        # --- Key: misconception_detect (pp. 22, 24) ---
        # Two-stage misconception detection: rule-based first, LLM fallback.
        # Returns structured JSON for downstream processing.
        misconception_detect = (
            '{"misconception_id": "ctrl_flow_break_placement", '
            '"confidence": 0.82, '
            '"description": "Student places the break condition after the '
            'accumulation step instead of before it, causing the loop to '
            'include a value that should trigger early termination or to '
            'skip the termination check on the triggering element.", '
            '"related_objectives": ["loop_termination", '
            '"control_flow_ordering"], '
            '"evidence": "break statement appears after total += x in '
            'the loop body; test case with negative value fails", '
            '"suggested_remediation": "trace_exercise", '
            '"remediation_detail": "Have student manually trace loop '
            'execution with nums = [2, 4, -1, 6], writing total and '
            'loop state at each step. Then ask: at which iteration does '
            'the break fire, and what is total at that point?"}'
        )

        # --- Key: propose_pedagogy (pp. 27–28, 36) ---
        # Pedagogy Agent rubric proposal: process-oriented, 40/30/30 split.
        propose_pedagogy = (
            "## Rubric Proposal: Process-Oriented Assessment\n\n"
            "**Perspective:** Pedagogy Specialist (scaffolding, cognitive "
            "load, formative feedback)\n\n"
            "### Proposed Rubric Structure\n\n"
            "The rubric should prioritize the learning process over pure "
            "output correctness. Students who demonstrate strong "
            "problem-solving strategies but arrive at partially correct "
            "solutions should receive meaningful credit.\n\n"
            "**Weight Distribution:**\n"
            "- Problem-Solving Strategy (40%): Evidence of planning, "
            "decomposition, and systematic approach. Did the student break "
            "the merge operation into subproblems? Did they consider edge "
            "cases before coding?\n"
            "- Correctness (30%): Functional correctness on standard and "
            "edge-case inputs. Partial credit for solutions that handle "
            "the main case but miss boundaries.\n"
            "- Code Readability (30%): Variable naming, comments, logical "
            "organization. Code should communicate intent to a reader.\n\n"
            "**Criteria (5 total):**\n"
            "1. Demonstrates a clear problem decomposition strategy\n"
            "2. Handles standard merge case (two non-empty sorted lists)\n"
            "3. Handles at least one edge case (empty list, duplicates)\n"
            "4. Code is readable with meaningful variable names\n"
            "5. Includes at least one explanatory comment or docstring\n\n"
            "**Confidence:** 0.75\n"
            "**Uncertainty:** Inter-rater reliability on criterion 1 "
            "(strategy assessment) is subjective and may vary across "
            "graders without calibration sessions."
        )

        # --- Key: propose_domain (pp. 27–28, 36) ---
        # Domain Expert rubric proposal: technical rigor, 50/30/20 split.
        propose_domain = (
            "## Rubric Proposal: Technical Rigor Assessment\n\n"
            "**Perspective:** Domain Expert (algorithm correctness, edge "
            "cases, code style)\n\n"
            "### Proposed Rubric Structure\n\n"
            "The rubric should center on algorithmic correctness and "
            "efficiency. The merge-two-sorted-lists problem has a clear "
            "optimal solution (O(n+m) two-pointer technique), and the "
            "rubric should reward students who achieve it.\n\n"
            "**Weight Distribution:**\n"
            "- Correctness (50%): Passes all test cases including edge "
            "cases. Specific point allocation: standard case (20%), empty "
            "lists (10%), duplicate values (10%), single-element lists "
            "(10%).\n"
            "- Efficiency (30%): Achieves O(n+m) time complexity. Does "
            "not use built-in sort (which would be O((n+m)log(n+m))). "
            "Single-pass solution preferred.\n"
            "- Style (20%): Follows PEP 8 conventions. Uses descriptive "
            "names. No dead code or debugging artifacts.\n\n"
            "**Criteria (7 total):**\n"
            "1. Correctly merges two non-empty sorted lists (4 pts)\n"
            "2. Handles empty input lists (2 pts)\n"
            "3. Handles duplicate values correctly (2 pts)\n"
            "4. Handles single-element lists (1 pt)\n"
            "5. Achieves O(n+m) time complexity (3 pts)\n"
            "6. Does not use built-in sort functions (2 pts)\n"
            "7. Follows PEP 8 and uses clear naming (1 pt)\n\n"
            "**Confidence:** 0.82\n"
            "**Uncertainty:** Partial credit rules for criterion 5 need "
            "clear definition — what score does an O(n*m) solution receive?"
        )

        # --- Key: propose_assessment (pp. 27–28, 36) ---
        # Assessment Agent rubric proposal: binary reliability, 5 pass/fail.
        propose_assessment = (
            "## Rubric Proposal: Binary Reliability Assessment\n\n"
            "**Perspective:** Assessment Specialist (rubric validity, "
            "inter-rater reliability, grade distribution)\n\n"
            "### Proposed Rubric Structure\n\n"
            "The rubric should maximize inter-rater reliability by using "
            "binary (pass/fail) criteria that leave no room for subjective "
            "interpretation. Each criterion is a concrete, observable "
            "condition that can be verified by automated testing.\n\n"
            "**Criteria (5 binary pass/fail):**\n"
            "1. Handles empty input: `merge([], [1,2])` returns `[1,2]` "
            "and `merge([1,2], [])` returns `[1,2]` — PASS/FAIL\n"
            "2. Preserves sort order: output is sorted for all test "
            "inputs — PASS/FAIL\n"
            "3. Achieves O(n+m) complexity: no nested loops over both "
            "lists, no calls to sort() — PASS/FAIL\n"
            "4. Uses no built-in sort: solution does not call sorted(), "
            ".sort(), or heapq.merge() — PASS/FAIL\n"
            "5. Includes docstring: function has a docstring describing "
            "inputs, outputs, and behavior — PASS/FAIL\n\n"
            "**Scoring:** Each criterion = 20%. Total = count of PASS "
            "criteria * 20.\n\n"
            "**Confidence:** 0.78\n"
            "**Uncertainty:** Binary scoring misses partial understanding. "
            "A student who handles most edge cases but misses one receives "
            "the same score as a student who handles none. This may "
            "compress the grade distribution and reduce diagnostic value."
        )

        # --- Key: evaluate_proposal (pp. 28–29) ---
        # Structured 4-dimension scoring per the evaluate_proposal() method.
        evaluate_proposal = (
            "## Proposal Evaluation\n\n"
            "### Scoring (0–10 per dimension)\n\n"
            "**Correctness: 7/10**\n"
            "The proposed rubric correctly identifies the key dimensions "
            "of the merge-sorted-lists problem. However, it does not "
            "explicitly address the case where both lists contain "
            "identical elements throughout, which can reveal subtle bugs "
            "in pointer advancement logic.\n\n"
            "**Completeness: 6/10**\n"
            "The criteria cover the main functional requirements but lack "
            "attention to error handling (e.g., what if inputs are not "
            "lists or contain non-comparable types). Process-oriented "
            "criteria are also absent — there is no way to assess whether "
            "the student approached the problem systematically.\n\n"
            "**Feasibility: 8/10**\n"
            "The rubric is straightforward to apply. Most criteria can be "
            "verified with automated test cases, reducing grading time. "
            "The one exception is style evaluation, which requires human "
            "judgment unless an automated linter is configured.\n\n"
            "**Risks / Gaps: 5/10**\n"
            "Primary risk: the rubric may penalize correct-but-suboptimal "
            "solutions too harshly. A student who uses concatenation + "
            "sort (O((n+m)log(n+m))) produces correct output but fails "
            "the efficiency criterion entirely. This creates a cliff "
            "effect that may not reflect actual understanding.\n\n"
            "**Overall: 6.5/10**"
        )

        # --- Key: adversarial_critic (pp. 31–32) ---
        # Deliberately harsh critique from the adversarial critic role.
        adversarial_critic = (
            "## Adversarial Critique\n\n"
            "### Weaknesses Identified\n\n"
            "**1. Unfalsifiable Strategy Criterion**\n"
            "The 'problem-solving strategy' criterion (40% weight) is "
            "unfalsifiable in practice. Without a mandatory planning "
            "artifact (pseudocode, diagram, or written decomposition), "
            "graders must infer strategy from the final code alone. This "
            "is circular: a correct solution is assumed to reflect good "
            "strategy, while an incorrect one is assumed to reflect poor "
            "strategy. Inter-rater agreement on this criterion will be "
            "unacceptably low.\n\n"
            "**2. Penalizing Correct-but-Suboptimal Solutions**\n"
            "The efficiency criterion creates a binary cliff: O(n+m) "
            "passes, anything else fails. A student who writes a correct "
            "O(n*m) solution demonstrates understanding of the merge "
            "concept but receives zero efficiency credit. This discourages "
            "incremental improvement and punishes students who solve the "
            "problem 'their way' before optimizing.\n\n"
            "**3. Binary Scoring Discards Signal**\n"
            "Pass/fail criteria cannot distinguish between 'almost got it' "
            "and 'completely wrong.' A student whose empty-list handling "
            "fails on one of two directions (e.g., handles `merge([], x)` "
            "but not `merge(x, [])`) receives the same score as a student "
            "who never considered the case. This compresses the grade "
            "distribution and reduces formative diagnostic value.\n\n"
            "### Recommendation\n"
            "Replace binary criteria with a 3-point scale: Absent (0), "
            "Partial (1), Complete (2). This preserves reliability while "
            "capturing partial understanding. Add a mandatory planning "
            "artifact to make strategy assessment observable.\n\n"
            "**Overall: 5.5/10** — The proposals have sound individual "
            "components but lack integration and produce avoidable "
            "grading artifacts."
        )

        # --- Key: synthesize_consensus (pp. 33–34) ---
        # Hybrid rubric merging all three proposals with provenance trail.
        synthesize_consensus = (
            "## Synthesized Rubric: Merge Two Sorted Lists\n\n"
            "### Final Rubric (5 Criteria x 3-Point Scale)\n\n"
            "| # | Criterion | Absent (0) | Partial (1) | Complete (2) "
            "| Provenance |\n"
            "|---|-----------|-----------|------------|-------------|"
            "------------|\n"
            "| 1 | Empty input handling | No handling | Handles one "
            "direction | Handles both directions | Assessment Agent |\n"
            "| 2 | Sort-order preservation | Output unsorted | Sorted on "
            "standard cases only | Sorted on all cases incl. duplicates "
            "| Domain Expert |\n"
            "| 3 | Algorithmic efficiency | Uses built-in sort or O(n*m) "
            "| O(n*m) with correct logic | O(n+m) two-pointer approach "
            "| Domain Expert |\n"
            "| 4 | Problem-solving evidence | No planning artifact | "
            "Comments describe approach | Pseudocode or docstring with "
            "explicit decomposition | Pedagogy Agent |\n"
            "| 5 | Code quality | No docstring, poor naming | Docstring "
            "present, some naming issues | Clear docstring, PEP 8, "
            "descriptive names | Adversarial calibration |\n\n"
            "### Scoring\n"
            "- Maximum: 10 points (5 criteria x 2 points)\n"
            "- Grade mapping: 9-10 = A, 7-8 = B, 5-6 = C, 3-4 = D, "
            "0-2 = F\n\n"
            "### Provenance Trail\n"
            "- **Criteria structure** (5 concrete dimensions): adapted "
            "from Assessment Agent's binary criteria\n"
            "- **3-point scale** (Absent/Partial/Complete): adopted from "
            "Pedagogy Agent's emphasis on partial credit, reinforced by "
            "Adversarial Critic's recommendation\n"
            "- **Edge-case specificity** (criteria 1–2): from Domain "
            "Expert's test-case coverage\n"
            "- **Process criterion** (criterion 4): from Pedagogy Agent, "
            "modified to require observable artifact per Adversarial "
            "Critic's falsifiability concern\n"
            "- **Calibration adjustments**: Adversarial Critic's cliff-"
            "effect warning resolved by Partial tier in criterion 3\n\n"
            "### Consensus Score: 7.8/10\n"
            "Convergence achieved in Round 2. All agents agree on the "
            "3-point scale structure. Remaining disagreement on the weight "
            "of criterion 4 (process vs. product) was resolved by "
            "compromise: evidence of planning is valued but weighted "
            "equally with other criteria rather than receiving the 40% "
            "share originally proposed."
        )

        # --- Key: cross_pollination (pp. 38–39) ---
        # Novel criterion emerging from cross-agent interaction.
        cross_pollination = (
            "## Cross-Pollination: Emergent Criterion\n\n"
            "### Novel Diagnostic-Trace Criterion\n\n"
            "By examining the strongest elements from competing proposals, "
            "a new criterion has emerged that none of the individual agents "
            "proposed independently.\n\n"
            "**Proposed Criterion: Diagnostic Trace Reasoning**\n\n"
            "This criterion combines the Domain Expert's emphasis on "
            "edge-case coverage with the Pedagogy Agent's process-oriented "
            "philosophy. Instead of simply checking whether edge cases "
            "pass, the criterion asks students to provide a written trace "
            "for one failing test case, demonstrating their ability to "
            "diagnose and reason about boundary behavior.\n\n"
            "**Scoring (3-point scale):**\n"
            "- Absent (0): No trace provided\n"
            "- Partial (1): Trace is provided but contains logical errors "
            "or skips steps\n"
            "- Complete (2): Trace correctly walks through the algorithm "
            "step-by-step for the edge case, identifying the exact point "
            "where special handling is needed\n\n"
            "**Why this is emergent:** The Domain Expert would not have "
            "proposed this because their framework focuses on output "
            "correctness, not process artifacts. The Pedagogy Agent would "
            "not have proposed this because their notion of 'strategy' was "
            "general, not tied to specific test cases. The combination of "
            "'trace a specific edge case' bridges both perspectives and "
            "produces a criterion that is simultaneously diagnostic "
            "(reveals misconceptions), observable (written artifact), and "
            "domain-specific (tied to algorithmic boundary behavior).\n\n"
            "**Confidence:** 0.71 (novel criterion — not yet validated "
            "with student cohort data)\n\n"
            "**Analogical Transfer Note:** This approach mirrors clinical "
            "diagnostic reasoning — listing candidate failure modes, "
            "ordering discriminating tests, and ruling out hypotheses — "
            "applied to programming assessment."
        )

        return {
            "feedback_generator": feedback_generator,
            "misconception_detect": misconception_detect,
            "propose_pedagogy": propose_pedagogy,
            "propose_domain": propose_domain,
            "propose_assessment": propose_assessment,
            "evaluate_proposal": evaluate_proposal,
            "adversarial_critic": adversarial_critic,
            "synthesize_consensus": synthesize_consensus,
            "cross_pollination": cross_pollination,
        }
