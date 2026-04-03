"""
Agent Utilities — Chapter 4: Agent Deployment and Responsible Development
From "Agents" by Imran Ahmad (Packt, 2026)

Provides shared infrastructure for the Chapter 4 companion notebook:
  - AgentLogger      : Color-coded ANSI logging for Jupyter environments
  - @fail_gracefully : Resilience decorator (Ref: Section 4.3, Table 4.1)
  - CostTracker      : Per-call cost accounting with budget enforcement
                       (Ref: Section 4.2, Figure 4.2, pp. 7–9)
  - CircuitBreaker   : State-machine circuit breaker extending the book's
                       tenacity-based pattern (Ref: Section 4.3, pp. 14–15)
  - InputValidator   : Prompt sanitization and threat-pattern detection
                       (Ref: Section 4.5, Tables 4.3a/b, pp. 18–19)
  - format_table()   : ASCII table renderer for notebook output

Author: Imran Ahmad
"""

from __future__ import annotations

import functools
import re
import time
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# AgentLogger — Color-coded notebook logging
# Ref: Strategy §3.6, all notebook sections
# ---------------------------------------------------------------------------

class AgentLogger:
    """Color-coded logger optimised for Jupyter notebook output.

    Color schema (ANSI):
        Blue  — [INFO] / [DEBUG]
        Green — [SUCCESS]
        Red   — [HANDLED ERROR]
        Bold  — section headers

    Author: Imran Ahmad
    Ref: Chapter 4, all sections
    """

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def __init__(self, verbose: bool = False, html_mode: bool = False) -> None:
        """Initialise logger with optional verbose and HTML modes.

        Author: Imran Ahmad
        """
        self.verbose = verbose
        self.html_mode = html_mode

    # -- internal helpers ---------------------------------------------------

    def _emit(self, color: str, tag: str, msg: str) -> None:
        """Print a formatted log line with ANSI colour or HTML.

        Author: Imran Ahmad
        """
        if self.html_mode:
            color_map = {
                self.BLUE: "#3B82F6",
                self.GREEN: "#22C55E",
                self.RED: "#EF4444",
                self.BOLD: "#1E293B",
            }
            hex_color = color_map.get(color, "#1E293B")
            from IPython.display import display, HTML
            display(HTML(
                f'<span style="color:{hex_color};font-weight:600;">'
                f'[{tag}]</span> {msg}'
            ))
        else:
            print(f"{color}[{tag}]{self.RESET} {msg}")

    # -- public API ---------------------------------------------------------

    def info(self, msg: str) -> None:
        """Log an informational message (Blue). Author: Imran Ahmad"""
        self._emit(self.BLUE, "INFO", msg)

    def success(self, msg: str) -> None:
        """Log a success message (Green). Author: Imran Ahmad"""
        self._emit(self.GREEN, "SUCCESS", msg)

    def error(self, msg: str) -> None:
        """Log a handled-error message (Red). Author: Imran Ahmad"""
        self._emit(self.RED, "HANDLED ERROR", msg)

    def debug(self, msg: str) -> None:
        """Log a debug message (Blue). Only visible when verbose=True. Author: Imran Ahmad"""
        if self.verbose:
            self._emit(self.BLUE, "DEBUG", msg)

    def section_header(self, num: str, title: str) -> None:
        """Print a bold section divider for notebook cells. Author: Imran Ahmad"""
        line = f"{'═' * 3} Section {num}: {title} {'═' * 3}"
        if self.html_mode:
            from IPython.display import display, HTML
            display(HTML(
                f'<h3 style="color:#1E293B;">{"═" * 3} Section {num}: '
                f'{title} {"═" * 3}</h3>'
            ))
        else:
            print(f"\n{self.BOLD}{line}{self.RESET}\n")


# Module-level default logger instance
logger = AgentLogger()


# ---------------------------------------------------------------------------
# @fail_gracefully — Resilience decorator
# Ref: Section 4.3, Table 4.1 (Failover Models row), pp. 11–12
# ---------------------------------------------------------------------------

def fail_gracefully(
    fallback_value: Any = None,
    section_ref: str = "",
) -> Callable:
    """Decorator that ensures a function never crashes the notebook.

    On success  → logs GREEN via AgentLogger.
    On exception → logs RED with *section_ref*, returns *fallback_value*.

    Usage::

        @fail_gracefully(fallback_value={"status": "unavailable"}, section_ref="4.3")
        def call_external_tool(endpoint):
            ...

    Author: Imran Ahmad
    Ref: Section 4.3, Table 4.1 — Failover Models
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                logger.success(
                    f"{func.__name__}() completed successfully."
                )
                return result
            except Exception as exc:
                ref_str = f" (Section {section_ref})" if section_ref else ""
                logger.error(
                    f"{type(exc).__name__} in {func.__name__}(){ref_str}: "
                    f"{exc}. Returning fallback."
                )
                return fallback_value
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# CostTracker — Per-call cost accounting with budget enforcement
# Ref: Section 4.2, Figure 4.2 (Cost Optimization hub), pp. 7–9
# ---------------------------------------------------------------------------

class CostTracker:
    """Tracks simulated inference costs and enforces a budget ceiling.

    When cumulative cost exceeds *budget_ceiling*, ``check_budget()``
    returns ``"degraded"`` — modelling the graceful-degradation strategy
    described in Section 4.2 (p. 8).

    Author: Imran Ahmad
    Ref: Section 4.2, Figure 4.2, pp. 7–9
    """

    def __init__(self, budget_ceiling: float = 1.00) -> None:
        """Initialise with a budget ceiling for degradation. Author: Imran Ahmad"""
        self.budget_ceiling = budget_ceiling
        self._records: List[Dict[str, Any]] = []
        self._total_cost: float = 0.0
        self._total_tokens: int = 0

    # -- recording ----------------------------------------------------------

    def record(self, model: str, tokens: int, cost: float) -> None:
        """Log a single inference cost event.

        Author: Imran Ahmad
        Ref: Section 4.2 — Monitoring & Iterative Optimization, p. 8
        """
        self._records.append({
            "model": model,
            "tokens": tokens,
            "cost": cost,
            "timestamp": time.time(),
        })
        self._total_cost += cost
        self._total_tokens += tokens

    # -- budget check -------------------------------------------------------

    def check_budget(self) -> str:
        """Return ``'ok'`` or ``'degraded'`` based on cumulative spend.

        Author: Imran Ahmad
        Ref: Section 4.2 — Cost-Aware Routing & Budget Enforcement, p. 8
        """
        if self._total_cost >= self.budget_ceiling:
            logger.error(
                f"Budget ceiling ${self.budget_ceiling:.2f} reached "
                f"(spent ${self._total_cost:.4f}). Entering degraded mode."
            )
            return "degraded"
        return "ok"

    # -- reporting ----------------------------------------------------------

    def summary(self) -> str:
        """Return a formatted cost dashboard string.

        Includes per-model and per-tier breakdown, mirroring the token cost
        dashboards described in Section 4.2 (p. 8).

        Author: Imran Ahmad
        Ref: Section 4.2 — Monitoring & Iterative Optimization
        """
        if not self._records:
            return "No cost records logged yet."

        by_model: Dict[str, Dict[str, float]] = defaultdict(
            lambda: {"calls": 0, "tokens": 0, "cost": 0.0}
        )
        for rec in self._records:
            entry = by_model[rec["model"]]
            entry["calls"] += 1
            entry["tokens"] += rec["tokens"]
            entry["cost"] += rec["cost"]

        headers = ["Model", "Calls", "Tokens", "Cost ($)"]
        rows = []
        for model, stats in sorted(by_model.items()):
            rows.append([
                model,
                str(int(stats["calls"])),
                str(int(stats["tokens"])),
                f"{stats['cost']:.4f}",
            ])
        rows.append([
            "TOTAL",
            str(len(self._records)),
            str(self._total_tokens),
            f"{self._total_cost:.4f}",
        ])

        table_str = format_table(headers, rows)
        budget_status = self.check_budget()
        header = (
            f"Cost Dashboard  |  "
            f"Budget: ${self.budget_ceiling:.2f}  |  "
            f"Status: {budget_status.upper()}"
        )
        return f"{header}\n{table_str}"

    # -- reset --------------------------------------------------------------

    def reset(self) -> None:
        """Clear all records (useful between demo sections).

        Author: Imran Ahmad
        """
        self._records.clear()
        self._total_cost = 0.0
        self._total_tokens = 0


# ---------------------------------------------------------------------------
# CircuitBreaker — State-machine extending book code pp. 14–15
# Ref: Section 4.3, Table 4.1 (Circuit Breakers row), pp. 14–15
# ---------------------------------------------------------------------------

class CircuitBreaker:
    """Circuit breaker with closed → open → half_open state transitions.

    Extends the ``tenacity``-based pattern from the book (pp. 14–15) by
    adding a *half_open* probe state and color-coded logging.

    States
    ------
    - **closed** : Normal operation. Failures are counted.
    - **open**   : All calls blocked immediately; fallback returned.
    - **half_open** : A single probe call is permitted. Success resets
      the breaker to closed; failure reopens it.

    Parameters
    ----------
    failure_threshold : int
        Consecutive failures before opening (book default: 3, p. 14).
    recovery_timeout : float
        Seconds before transitioning from open → half_open.

    Author: Imran Ahmad
    Ref: Section 4.3, Table 4.1, pp. 14–15
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 5.0,
    ) -> None:
        """Initialise breaker with configurable threshold and timeout. Author: Imran Ahmad"""
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failure_count: int = 0
        self._state: str = "closed"
        self._last_failure_time: float = 0.0

    # -- properties ---------------------------------------------------------

    @property
    def state(self) -> str:
        """Current breaker state: ``'closed'``, ``'open'``, or ``'half_open'``.

        Author: Imran Ahmad
        Ref: Section 4.3, pp. 14–15
        """
        if self._state == "open":
            elapsed = time.time() - self._last_failure_time
            if elapsed >= self.recovery_timeout:
                self._state = "half_open"
                logger.info(
                    f"CircuitBreaker → half_open (recovery timeout "
                    f"{self.recovery_timeout}s elapsed)."
                )
        return self._state

    # -- call wrapper -------------------------------------------------------

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute *func* through the circuit breaker.

        If the circuit is **open**, the call is blocked immediately and
        ``{"status": "unavailable", "fallback": True}`` is returned —
        matching the fallback dict on p. 15 of the book.

        Author: Imran Ahmad
        Ref: Section 4.3, pp. 14–15
        """
        current_state = self.state  # triggers open→half_open check

        if current_state == "open":
            logger.error(
                "Circuit OPEN — call blocked. Returning fallback."
            )
            return {"status": "unavailable", "fallback": True}

        try:
            result = func(*args, **kwargs)
            # Success path
            if current_state == "half_open":
                logger.success(
                    "CircuitBreaker probe succeeded → closed."
                )
            self._failure_count = 0
            self._state = "closed"
            return result

        except Exception as exc:
            self._failure_count += 1
            self._last_failure_time = time.time()
            logger.error(
                f"CircuitBreaker failure {self._failure_count}/"
                f"{self.failure_threshold}: {type(exc).__name__}: {exc}"
            )

            if self._failure_count >= self.failure_threshold:
                self._state = "open"
                logger.error(
                    f"Circuit breaker TRIPPED → open after "
                    f"{self.failure_threshold} consecutive failures."
                )

            return {"status": "unavailable", "fallback": True}

    # -- reset --------------------------------------------------------------

    def reset(self) -> None:
        """Reset the breaker to closed state (for demo re-runs).

        Author: Imran Ahmad
        """
        self._failure_count = 0
        self._state = "closed"
        self._last_failure_time = 0.0
        logger.info("CircuitBreaker reset → closed.")


# ---------------------------------------------------------------------------
# InputValidator — Prompt sanitisation and threat-pattern detection
# Ref: Section 4.5, Tables 4.3a/b (pp. 18–19), defense-in-depth (p. 21)
# ---------------------------------------------------------------------------

# Patterns sourced from Table 4.3b threat descriptions (pp. 18–19)
_INJECTION_PATTERNS: List[Tuple[str, str]] = [
    # (compiled-ready regex source, threat label)
    (r"(?i)ignore\s+(all\s+)?previous\s+instructions", "prompt_injection"),
    (r"(?i)you\s+are\s+now\s+(an?\s+)?admin", "identity_spoofing"),
    (r"(?i)system:\s*override", "prompt_injection"),
    (r"(?i)act\s+as\s+(root|admin|superuser)", "identity_spoofing"),
    (r"(?i)<script[^>]*>", "indirect_prompting"),
    (r"(?i)\{\{.*?\}\}", "indirect_prompting"),
    (r"(?i)forget\s+(everything|all|your)\s+(instructions|rules|guidelines)",
     "prompt_injection"),
    (r"(?i)execute\s+(shell|cmd|command|bash)", "tool_hijacking"),
    (r"(?i)curl\s+https?://", "tool_hijacking"),
    (r"(?i)rm\s+-rf\s+/", "tool_hijacking"),
]


class InputValidator:
    """Prompt sanitiser and threat-pattern scanner.

    Implements the defense-in-depth input-validation layer described in
    Section 4.5 (p. 21): strip malicious tokens, enforce structured
    prompts, and isolate user input from system commands.

    Author: Imran Ahmad
    Ref: Section 4.5, Tables 4.3a/b (pp. 18–19), p. 21
    """

    def __init__(self) -> None:
        """Initialise with compiled threat patterns from Table 4.3b. Author: Imran Ahmad"""
        self._compiled = [
            (re.compile(pat), label)
            for pat, label in _INJECTION_PATTERNS
        ]
        self._rate_limits: Dict[str, List[float]] = defaultdict(list)
        self._rate_window: float = 60.0   # seconds
        self._rate_max: int = 10          # max requests per window

    # -- sanitise -----------------------------------------------------------

    def sanitize(self, prompt: str) -> Dict[str, Any]:
        """Scan *prompt* for known attack vectors from Table 4.3b.

        Returns a dict with ``'clean_text'``, ``'threats_found'``, and
        ``'risk_level'``.

        Author: Imran Ahmad
        Ref: Section 4.5, Table 4.3b, pp. 18–19
        """
        threats: List[str] = []
        sanitized = prompt

        for pattern, label in self._compiled:
            if pattern.search(prompt):
                threats.append(label)
                sanitized = pattern.sub("[BLOCKED]", sanitized)

        risk = "low"
        if threats:
            risk = "high" if any(
                t in ("prompt_injection", "identity_spoofing", "tool_hijacking")
                for t in threats
            ) else "medium"

        return {
            "clean_text": sanitized.strip(),
            "threats_found": list(set(threats)),
            "risk_level": risk,
            "passed_validation": len(threats) == 0,
        }

    # -- schema enforcement -------------------------------------------------

    def enforce_schema(
        self,
        input_dict: Dict[str, Any],
        schema: Dict[str, type],
    ) -> Dict[str, Any]:
        """Validate *input_dict* against a typed *schema*.

        Returns ``{"valid": True/False, "errors": [...]}``.

        Author: Imran Ahmad
        Ref: Section 4.5, p. 21 — Prompt schema enforcement
        """
        errors: List[str] = []
        for key, expected_type in schema.items():
            if key not in input_dict:
                errors.append(f"Missing required field: '{key}'")
            elif not isinstance(input_dict[key], expected_type):
                errors.append(
                    f"Field '{key}': expected {expected_type.__name__}, "
                    f"got {type(input_dict[key]).__name__}"
                )
        return {"valid": len(errors) == 0, "errors": errors}

    # -- rate limiting ------------------------------------------------------

    def check_rate_limit(self, user_id: str) -> Dict[str, Any]:
        """Basic sliding-window rate limiter.

        Returns ``{"allowed": True/False, "remaining": int}``.

        Author: Imran Ahmad
        Ref: Section 4.5, p. 21 — Interface hardening (rate-limiting)
        """
        now = time.time()
        window = [
            ts for ts in self._rate_limits[user_id]
            if now - ts < self._rate_window
        ]
        self._rate_limits[user_id] = window

        if len(window) >= self._rate_max:
            return {"allowed": False, "remaining": 0}

        window.append(now)
        self._rate_limits[user_id] = window
        return {"allowed": True, "remaining": self._rate_max - len(window)}


# ---------------------------------------------------------------------------
# format_table — ASCII table renderer
# Ref: Used to display Tables 4.1–4.5 in notebook cells
# ---------------------------------------------------------------------------

def format_table(headers: List[str], rows: List[List[str]]) -> str:
    """Render a clean ASCII table for notebook display.

    Parameters
    ----------
    headers : list[str]
        Column header labels.
    rows : list[list[str]]
        Row data (each inner list must match *headers* length).

    Returns
    -------
    str
        Formatted table string ready for ``print()``.

    Author: Imran Ahmad
    """
    all_rows = [headers] + rows
    col_widths = [
        max(len(str(cell)) for cell in col) + 2
        for col in zip(*all_rows)
    ]

    def _format_row(cells: List[str]) -> str:
        return "│".join(
            str(cell).center(w) for cell, w in zip(cells, col_widths)
        )

    separator = "┼".join("─" * w for w in col_widths)
    lines = [_format_row(headers), separator]
    for row in rows:
        lines.append(_format_row(row))

    return "\n".join(lines)
