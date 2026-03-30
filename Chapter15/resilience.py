# =============================================================================
# utils/resilience.py — Color-Coded Logging & Graceful Fallback Decorator
# Chapter 15: Education and Knowledge Agents
# Book: 30 Agents Every AI Engineer Must Build (Packt Publishing)
# Author: Imran Ahmad
#
# Cross-cutting infrastructure for:
#   1. ColorLogger — Visual execution tracing (§4, pp. 2–25, 25–39)
#   2. @graceful_fallback — Exception-safe decorator with mock routing (§5)
#
# Visual Logging Schema:
#   Blue   [INFO]           — Agent initializing, tool invoked, state read
#   Green  [SUCCESS]        — Step complete, valid output returned
#   Yellow [WARN]           — Degraded result, low confidence
#   Red    [HANDLED ERROR]  — Exception caught, fallback activated
# =============================================================================

import functools
import traceback
from enum import Enum
from datetime import datetime


# ── LogLevel Enum (§4) ──────────────────────────────────────────────────────

class LogLevel(Enum):
    """ANSI color-coded log levels for agent execution tracing.

    Each member stores a (label, ansi_code) tuple used by ColorLogger
    to format console output with visual differentiation.

    Schema (Ch.15 Repository Standard):
        INFO    — \033[94m (Blue)   — Initialization, tool calls, state reads
        SUCCESS — \033[92m (Green)  — Completed steps, valid outputs
        WARN    — \033[93m (Yellow) — Degraded results, low confidence
        ERROR   — \033[91m (Red)    — Caught exceptions, fallback activation
    """
    INFO = ("INFO", "\033[94m")
    SUCCESS = ("SUCCESS", "\033[92m")
    WARN = ("WARN", "\033[93m")
    ERROR = ("HANDLED ERROR", "\033[91m")


# ── ColorLogger (§4, pp. 2–39) ─────────────────────────────────────────────

class ColorLogger:
    """Color-coded logger for agent execution tracing.

    Provides four convenience methods (info, success, warn, error) that
    emit timestamped, color-coded, component-tagged messages to stdout.

    Visual Logging Schema (Ch.15 Repository Standard):
        Blue   [INFO]           — Agent initializing, tool invoked, state read
        Green  [SUCCESS]        — Step complete, valid output returned
        Yellow [WARN]           — Degraded result, low confidence
        Red    [HANDLED ERROR]  — Exception caught, fallback activated

    Args:
        component: Identifier for the source module/class (e.g., 'CurriculumPlanner').

    Example:
        >>> logger = ColorLogger("StudentModel")
        >>> logger.info("Initializing mastery state for student 'alex_001'")
        [14:22:01] [INFO] [StudentModel] Initializing mastery state for student 'alex_001'
    """

    def __init__(self, component: str = "Agent"):
        self.component = component

    def _log(self, level: LogLevel, message: str) -> None:
        """Emit a single color-coded log line to stdout.

        Args:
            level: LogLevel enum member controlling color and label prefix.
            message: Free-form message string.
        """
        label, color = level.value
        reset = "\033[0m"
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] [{label}] [{self.component}] {message}{reset}")

    def info(self, msg: str) -> None:
        """Log an informational message (Blue)."""
        self._log(LogLevel.INFO, msg)

    def success(self, msg: str) -> None:
        """Log a success message (Green)."""
        self._log(LogLevel.SUCCESS, msg)

    def warn(self, msg: str) -> None:
        """Log a warning message (Yellow)."""
        self._log(LogLevel.WARN, msg)

    def error(self, msg: str) -> None:
        """Log a handled-error message (Red)."""
        self._log(LogLevel.ERROR, msg)


# ── @graceful_fallback Decorator (§5, Decorator Application Map) ───────────

def graceful_fallback(fallback_value=None, component: str = "Agent", mock_fn=None):
    """Decorator: wraps callable in try/except, logs errors, returns fallback.

    This is the key resilience primitive for the Chapter 15 repository.
    Every external or fragile call (LLM API, network I/O) is wrapped so
    that the notebook never crashes — even if the API key is invalid,
    the network is down, or a rate limit is hit.

    Priority: mock_fn > fallback_value.

    Args:
        fallback_value: Static value to return on failure (used if mock_fn is None).
        component: Name for ColorLogger context (e.g., 'FeedbackGenerator').
        mock_fn: Optional callable invoked with (*args, **kwargs) to generate
                 a context-aware fallback. Takes priority over fallback_value.

    Decorator Application Map (§5):
        FeedbackGenerator.generate_feedback()   — pp. 22–24
        CollaborativeAgent.propose_solution()    — pp. 27–28
        CollaborativeAgent.evaluate_proposal()   — pp. 28–29
        ConsensusEngine._synthesize()            — pp. 33–34
        misconceptions.detect_llm()              — pp. 22, 24
        AdaptivePlacementTest.run()              — pp. 11–13
        KnowledgeGraph initialization            — pp. 6, 8

    Example:
        >>> @graceful_fallback(fallback_value="default", component="MyAgent")
        ... def risky_call():
        ...     raise ConnectionError("API down")
        >>> risky_call()  # Returns "default", logs red error, notebook continues
        'default'
    """
    logger = ColorLogger(component)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                logger.success(f"{func.__name__}() completed successfully.")
                return result
            except Exception as e:
                logger.error(
                    f"{func.__name__}() failed: {type(e).__name__}: {e}. "
                    f"Falling back to {'mock_fn' if mock_fn else 'static fallback'}."
                )
                if mock_fn is not None:
                    try:
                        fallback = mock_fn(*args, **kwargs)
                        logger.warn(
                            "Mock response returned — fidelity is illustrative, "
                            "not generative."
                        )
                        return fallback
                    except Exception as inner_e:
                        logger.error(f"Mock fallback also failed: {inner_e}")
                        return fallback_value
                return fallback_value
        return wrapper
    return decorator
