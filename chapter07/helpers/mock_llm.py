# =============================================================================
# helpers/mock_llm.py
# Chapter 7: Tool Manipulation and Orchestration Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026 — B34135)
# Ref: Sections 7.5, 7.6, 7.7, 7.7b
#
# Context-aware MockLLM class that enables Simulation Mode. When no OpenAI
# API key is detected, the notebook uses this class instead of making live
# API calls. Every mock response is derived directly from the chapter's own
# code examples and data, ensuring pedagogical consistency.
#
# Routing Table:
#   R1 — Standard risk assessment      (Section 7.7)
#   R2 — High-risk assessment           (Section 7.7)
#   R3 — Market intelligence report     (Section 7.6)
#   R4 — Sentiment analysis             (Section 7.5)
#   R5 — Insurance claim (low risk)     (Section 7.7b)
#   R6 — Insurance claim (high risk)    (Section 7.7b)
#   DEFAULT — Generic fallback
# =============================================================================

import json
import time

from helpers.color_logger import log_mock, log_warning

# ---------------------------------------------------------------------------
# Mock Response Data — drawn directly from chapter code listings
# ---------------------------------------------------------------------------

# Section 7.7 — E-Commerce Risk Assessment (pp. 28-30)
# Standard order: moderate risk flag for orders exceeding typical range
_R1_RESPONSE = {
    "risk_level": "medium",
    "reason": "Order total exceeds typical range for this customer segment.",
}

# Section 7.7 — High-risk order with address mismatch (p. 29)
_R2_RESPONSE = {
    "risk_level": "high",
    "reason": "Shipping/billing address mismatch combined with high order value.",
}

# Section 7.6 — Market Intelligence Synthesized Report (pp. 21-27)
# Values match FinancialAgent and SentimentAgent mock data from chapter code
_R3_RESPONSE = (
    "Market Intelligence Report for TechCorp\n"
    "=========================================\n"
    "Recent news: TechCorp Q3 earnings beat analyst estimates by 8%; "
    "TechCorp announces expansion into cloud infrastructure.\n"
    "Financial indicators: P/E ratio 24.5, revenue growth 12%, "
    "debt-to-equity 0.38, last close $142.73.\n"
    "Sentiment: Score 0.72 (positive). Investor confidence remains high "
    "and social media tone is broadly favorable this week.\n\n"
    "**Alignment Confirmed (Score: 0.12):** Public perception and market "
    "performance are well-aligned. No material discrepancy detected "
    "between sentiment signals and financial indicators."
)

# Section 7.5 — Sentiment Analysis (pp. 22)
_R4_RESPONSE = {
    "score": 0.72,
    "label": "positive",
    "evidence": [
        "Investor confidence in TechCorp remains high.",
        "Social media tone broadly favorable this week.",
    ],
}

# Section 7.7b — Insurance Claim Classification, low risk (p. 33)
# Matches CLM-4821 walkthrough: confidence 0.91, auto-approved
_R5_RESPONSE = {
    "confidence_score": 0.91,
    "risk": "low",
    "claim_type": "water_damage",
}

# Section 7.7b — Insurance Claim Classification, high risk (p. 33)
# Matches CLM-5099 escalation scenario: confidence 0.79, escalated
_R6_RESPONSE = {
    "confidence_score": 0.79,
    "risk": "high",
    "claim_type": "fire_damage",
}

# Default — No context matched
_DEFAULT_RESPONSE = {
    "response": "Mock LLM: No specific context matched for this prompt.",
    "status": "ok",
}


class MockLLM:
    """Context-aware mock LLM that routes prompts to chapter-derived responses.

    This class replaces live OpenAI API calls when no API key is present.
    It inspects the incoming prompt for keywords and returns the appropriate
    mock structure, ensuring that all downstream code (JSON parsing, field
    access, conditional branching) works identically in Simulation Mode.

    Parameters
    ----------
    verbose : bool
        If True, log each mock call with the detected route via log_mock().
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self._call_count = 0

    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------

    def generate(
        self,
        prompt: str,
        simulate_timeout: bool = False,
        **kwargs,
    ) -> str:
        """Route a prompt to the appropriate mock response.

        Parameters
        ----------
        prompt : str
            The prompt text that would normally be sent to an LLM.
        simulate_timeout : bool
            If True, sleep for 5 seconds then raise TimeoutError.
            Used in Section 7.3 failure demonstrations.

        Returns
        -------
        str
            JSON string (for structured routes) or plain text (for R3).
        """
        self._call_count += 1

        # --- Timeout simulation for Section 7.3 failure demos ---
        if simulate_timeout:
            if self.verbose:
                log_warning(
                    f"MockLLM call #{self._call_count}: "
                    "Simulating API timeout (5s delay)..."
                )
            time.sleep(5)
            raise TimeoutError("MockLLM: Simulated API timeout.")

        # --- Route detection and response ---
        route = self._detect_route(prompt)
        response = self._get_response(route, prompt)

        if self.verbose:
            log_mock(
                f"MockLLM call #{self._call_count}: "
                f"Route {route} matched. Returning chapter-derived data."
            )

        return response

    # ------------------------------------------------------------------
    # Internal Routing
    # ------------------------------------------------------------------

    def _detect_route(self, prompt: str) -> str:
        """Classify a prompt into a route ID based on keyword matching.

        The routing priority is ordered from most specific to least specific
        to avoid false matches. Routes R2 and R6 are checked before R1 and
        R5 respectively because they require additional qualifier keywords.
        """
        p = prompt.lower()

        # --- R6: High-risk insurance claim (before R5) — Section 7.7b ---
        if ("claim" in p or "insurance" in p) and (
            "high_risk" in p or "high risk" in p or "fire" in p
        ):
            return "R6"

        # --- R5: Standard insurance claim — Section 7.7b ---
        if ("claim" in p or "insurance" in p) and (
            "classify" in p or "assess" in p or "water" in p
        ):
            return "R5"

        # --- R2: High-risk order (before R1) — Section 7.7 ---
        if ("risk" in p or "fraud" in p) and (
            "high_value" in p or "mismatch" in p or "high value" in p
        ):
            return "R2"

        # --- R1: Standard risk assessment — Section 7.7 ---
        if "risk" in p or "fraud" in p or "order" in p:
            return "R1"

        # --- R3: Market intelligence report — Section 7.6 ---
        if any(kw in p for kw in ("market", "intelligence", "report", "synthesize")):
            return "R3"

        # --- R4: Sentiment analysis — Section 7.5 ---
        if "sentiment" in p or "analyze" in p:
            return "R4"

        # --- DEFAULT ---
        return "DEFAULT"

    def _get_response(self, route: str, prompt: str) -> str:
        """Return the mock data for a given route.

        Structured routes (R1, R2, R4, R5, R6, DEFAULT) return JSON strings.
        R3 returns plain prose text (the synthesized market report).
        """
        route_map = {
            "R1": _R1_RESPONSE,
            "R2": _R2_RESPONSE,
            "R3": _R3_RESPONSE,  # Plain text, not dict
            "R4": _R4_RESPONSE,
            "R5": _R5_RESPONSE,
            "R6": _R6_RESPONSE,
            "DEFAULT": _DEFAULT_RESPONSE,
        }

        data = route_map.get(route, _DEFAULT_RESPONSE)

        # R3 is already a string (prose report)
        if isinstance(data, str):
            return data

        return json.dumps(data)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @property
    def call_count(self) -> int:
        """Total number of generate() calls made on this instance."""
        return self._call_count

    def __repr__(self) -> str:
        return f"MockLLM(verbose={self.verbose}, calls={self._call_count})"
