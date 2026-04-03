# ──────────────────────────────────────────────────────────────
# utils/mock_llm.py — MockLLM, Mock Registry, llm_call,
#                      @fail_gracefully Decorator
# Chapter 8: Data Analysis and Reasoning Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Ref: Strategy §4.3, Chapter Sections 8.1.1, 8.1.2, 8.4, 8.5
# ──────────────────────────────────────────────────────────────

from __future__ import annotations

import json
import functools
from typing import Any, Callable

from utils import color_logger as log

# ══════════════════════════════════════════════════════════════
# 4.3.1 — Mock Response Registry (7 entries)
# Every response is derived verbatim from Chapter 8 fallbacks.
# ══════════════════════════════════════════════════════════════

MOCK_REGISTRY: dict[str, dict[str, Any]] = {

    # ── Section 8.4: News Fact-Checker — Claim Extraction ────
    # Source: Chapter §8.4, regex-fallback expected output for
    # the Ottawa economy article.
    "claim_extraction": {
        "section": "8.4",
        "keywords": ["fact-check", "extract", "claims"],
        "response": {
            "claims": [
                {
                    "claim_text": "the city's unemployment rate fell by 5% last year",
                    "metric": "unemployment rate change",
                    "value": "5%",
                    "entity": "Ottawa",
                    "period": "2024",
                },
                {
                    "claim_text": "budget surplus of $12 million for the 2024 fiscal year",
                    "metric": "budget surplus",
                    "value": "12000000",
                    "entity": "Ottawa",
                    "period": "2024",
                },
            ]
        },
    },

    # ── Section 8.5: GPS — Decompose (Iteration 1, broad) ───
    # Source: Chapter §8.5, `fallback` list inside decompose()
    "gps_decompose_v1": {
        "section": "8.5",
        "keywords": ["decompos"],
        "response": [
            "What network topology properties correlate with cascading failure resistance?",
            "How does biodiversity contribute to ecosystem network resilience?",
            "What redundancy mechanisms exist in ecological vs. engineered networks?",
        ],
    },

    # ── Section 8.5: GPS — Decompose (Iteration 2, refined) ─
    # Source: Chapter §8.5, `fallback` list when refinement_hint
    # is present.
    "gps_decompose_v2": {
        "section": "8.5",
        "keywords": ["decompos"],
        "response": [
            (
                "Which graph-theoretic metrics (e.g., betweenness centrality, modularity)"
                " predict cascade size in both food webs and power grids?"
            ),
            "How do keystone species in ecology map to critical substations in grids?",
            "What quantitative thresholds for redundancy prevent cascading collapse?",
        ],
    },

    # ── Section 8.5: GPS — Analogy Search ────────────────────
    # Source: Chapter §8.5, `fallback` dict inside
    # search_analogies().
    "gps_analogies": {
        "section": "8.5",
        "keywords": ["analogy", "ecology"],
        "response": {
            "topology": (
                "Food webs with higher connectance absorb species loss "
                "without trophic cascades (Dunne et al., 2002)."
            ),
            "keystone": (
                "Removal of keystone species triggers disproportionate "
                "ecosystem collapse, analogous to hub failure in grids."
            ),
            "redundancy": (
                "Functional redundancy in ecosystems (multiple species "
                "filling the same niche) parallels N-1 contingency in grids."
            ),
        },
    },

    # ── Section 8.5: GPS — Hypothesis Synthesis ──────────────
    # Source: Chapter §8.5, `fallback` string inside
    # generate_hypothesis().
    "gps_hypothesis": {
        "section": "8.5",
        "keywords": ["hypothes", "synthesiz"],
        "response": (
            "Power grids whose substation connectivity graph exhibits "
            "modularity and functional redundancy scores above "
            "ecological resilience thresholds will contain cascading "
            "failures to fewer than 5% of nodes."
        ),
    },

    # ── Section 8.1.1: Visualization Recommendation ──────────
    # Source: Chapter §8.1.1, decision-tree logic from
    # recommend_visualization() and Figure 8.2.
    "viz_recommendation": {
        "section": "8.1.1",
        "keywords": ["visualization", "chart type"],
        "response": {
            "trend": "line",
            "compare": "bar",
            "relationship": "scatter",
            "default": "table",
        },
    },

    # ── Section 8.1.2: Statistical Interpretation ────────────
    # Source: Chapter §8.1.2, inline interpretation examples for
    # OLS regression and anomaly detection.
    "stats_interpretation": {
        "section": "8.1.2",
        "keywords": ["statistic", "interpret"],
        "response": (
            "Marketing spend explains approximately 62% of the variation "
            "in revenue, indicating a strong positive correlation. "
            "Sales in Q2 for Region East appear unusually high, possibly "
            "due to promotional pricing or data entry anomalies."
        ),
    },
}


# ══════════════════════════════════════════════════════════════
# 4.3.2 — MockLLM Class
# ══════════════════════════════════════════════════════════════

class MockLLM:
    """Deterministic LLM stand-in for Simulation Mode.

    Serves chapter-accurate responses from MOCK_REGISTRY.
    Never crashes; returns a JSON error string on no match.

    Ref: Strategy §4.3.2
    """

    def __init__(self) -> None:
        self._registry = MOCK_REGISTRY
        self._call_count = 0

    # ── Public API ───────────────────────────────────────────

    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        context_key: str = "",
    ) -> str:
        """Return a mock response for the given prompts.

        Parameters
        ----------
        system_prompt : str
            The system message (used for keyword inference).
        user_prompt : str
            The user message (used for keyword inference).
        context_key : str, optional
            Explicit registry key. If provided, skips inference.

        Returns
        -------
        str
            JSON-encoded or plain-text response.
        """
        self._call_count += 1

        # Explicit key → direct lookup
        if context_key and context_key in self._registry:
            entry = self._registry[context_key]
            log.info(
                f"MockLLM serving '{context_key}' (Section {entry['section']})",
                section=entry["section"],
            )
            return self._format(entry["response"])

        # No key → autonomous inference
        inferred = self._infer_key(system_prompt, user_prompt)
        if inferred:
            entry = self._registry[inferred]
            log.info(
                f"MockLLM inferred '{inferred}' (Section {entry['section']})",
                section=entry["section"],
            )
            return self._format(entry["response"])

        # No match → safe fallback (never crashes)
        log.info("MockLLM: no registry match; returning default response.")
        return json.dumps({"mock": True, "message": "No matching mock response found."})

    # ── Private helpers ──────────────────────────────────────

    def _infer_key(self, system: str, user: str) -> str | None:
        """Keyword scan over combined prompts. Returns best key."""
        combined = (system + " " + user).lower()
        best_key: str | None = None
        best_hits = 0
        for key, entry in self._registry.items():
            hits = sum(1 for kw in entry["keywords"] if kw in combined)
            if hits > best_hits:
                best_hits = hits
                best_key = key
        return best_key if best_hits > 0 else None

    def _format(self, response: Any) -> str:
        """str passthrough; dict/list → json.dumps()."""
        if isinstance(response, str):
            return response
        return json.dumps(response)


# ══════════════════════════════════════════════════════════════
# 4.3.3 — Unified llm_call() Wrapper
# ══════════════════════════════════════════════════════════════

# Module-level singleton — reused across all calls
_mock_llm = MockLLM()


def llm_call(
    system: str,
    user: str,
    context_key: str = "",
    simulation_mode: bool = False,
    client: Any = None,
) -> str:
    """Single entry point for ALL LLM calls in the notebook.

    Live path:  OpenAI API → success or fall through to mock.
    Simulation: Routes directly to MockLLM.

    Parameters
    ----------
    system : str
        System prompt.
    user : str
        User prompt.
    context_key : str, optional
        Explicit MockLLM registry key.
    simulation_mode : bool
        If True, skip the API entirely.
    client : openai.OpenAI | None
        Initialized OpenAI client (None in Simulation Mode).

    Returns
    -------
    str
        LLM response text.

    Ref: Strategy §4.3.3
    """
    # ── Live path ────────────────────────────────────────────
    if not simulation_mode and client is not None:
        try:
            resp = client.chat.completions.create(
                model="gpt-4o",
                temperature=0,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            result = resp.choices[0].message.content
            log.success("LLM call completed (live API).")
            return result
        except Exception as e:
            log.error(f"Live API call failed: {e} — falling back to MockLLM.")

    # ── Simulation / fallback path ───────────────────────────
    return _mock_llm.call(system, user, context_key=context_key)


# ══════════════════════════════════════════════════════════════
# 4.3.4 — @fail_gracefully Decorator
# ══════════════════════════════════════════════════════════════

def fail_gracefully(
    fallback_value: Any = None,
    section: str = "",
) -> Callable:
    """Wrap any function in try/except with color-coded logging.

    On success: log.info (entry) + log.success (exit).
    On failure: log.error (with section ref) + return fallback_value.

    Parameters
    ----------
    fallback_value : Any
        Value to return when the wrapped function raises.
    section : str
        Chapter section reference for error messages.

    Ref: Strategy §4.3.4

    Usage
    -----
    >>> @fail_gracefully(fallback_value="table", section="8.1.1")
    ... def recommend_visualization(df, query):
    ...     ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            fname = func.__name__
            log.info(f"Entering {fname}()", section=section)
            try:
                result = func(*args, **kwargs)
                log.success(f"{fname}() completed.", section=section)
                return result
            except Exception as e:
                log.error(
                    f"{fname}() failed: {e} — returning fallback.",
                    section=section,
                )
                return fallback_value
        return wrapper
    return decorator
