# ===========================================================================
# utils/resilience.py — ColorLogger & Graceful Fallback Decorator
# Chapter 15: Education and Knowledge Agents
# Book: 30 Agents Every AI Engineer Must Build (Packt Publishing)
# Author: Imran Ahmad
#
# Cross-cutting infrastructure for visual logging and fault tolerance.
# Ref: Strategy §4 (ColorLogger), §5 (@graceful_fallback)
# ===========================================================================

import functools
import traceback
from enum import Enum
from datetime import datetime


class LogLevel(Enum):
    """ANSI color-coded log levels for agent execution tracing.

    Visual Logging Schema (Ch.15 Repository Standard):
        Blue   [INFO]           — Agent initializing, tool invoked, state read
        Green  [SUCCESS]        — Step complete, valid output returned
        Yellow [WARN]           — Degraded result, low confidence
        Red    [HANDLED ERROR]  — Exception caught, fallback activated
    """
    INFO = ("INFO", "\033[94m")
    SUCCESS = ("SUCCESS", "\033[92m")
    WARN = ("WARN", "\033[93m")
    ERROR = ("HANDLED ERROR", "\033[91m")


class ColorLogger:
    """Color-coded logger for agent execution tracing.

    Provides four log levels with ANSI color output for clear visual
    feedback during notebook execution. Each message is timestamped
    and tagged with the component name.

    Ref: Strategy §4 — Visual Logging Schema
    """

    def __init__(self, component: str = "Agent") -> None:
        self.component = component

    def _log(self, level: LogLevel, message: str) -> None:
        """Emit a color-coded, timestamped log line."""
        label, color = level.value
        reset = "\033[0m"
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] [{label}] [{self.component}] {message}{reset}")

    def info(self, msg: str) -> None:
        """Blue — Agent initialization, tool invocation, state transitions."""
        self._log(LogLevel.INFO, msg)

    def success(self, msg: str) -> None:
        """Green — Completed steps, valid outputs, mastery threshold crossed."""
        self._log(LogLevel.SUCCESS, msg)

    def warn(self, msg: str) -> None:
        """Yellow — Degraded responses, low confidence, near-threshold values."""
        self._log(LogLevel.WARN, msg)

    def error(self, msg: str) -> None:
        """Red — API failures, timeout, fallback activation."""
        self._log(LogLevel.ERROR, msg)


def graceful_fallback(fallback_value=None, component="Agent", mock_fn=None):
    """Decorator: wraps callable in try/except, logs errors, returns fallback.

    Every external or fragile call in the notebook is wrapped with this
    decorator to ensure the system remains stable during failure-scenario
    demonstrations. When an exception occurs, the decorator:
      1. Logs the error in red via ColorLogger.
      2. Invokes mock_fn (if provided) for a context-aware fallback.
      3. Falls back to the static fallback_value as a last resort.

    Args:
        fallback_value: Static value to return on failure (used if mock_fn
                        is None or itself raises).
        component: Name for ColorLogger context (e.g., 'FeedbackGenerator').
        mock_fn: Optional callable invoked with (*args, **kwargs) to generate
                 a context-aware fallback. Takes priority over fallback_value.

    Ref: Strategy §5 — Graceful Fallback Decorator
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
                            "Mock response returned — fidelity is illustrative."
                        )
                        return fallback
                    except Exception as inner_e:
                        logger.error(f"Mock fallback also failed: {inner_e}")
                        return fallback_value
                return fallback_value
        return wrapper
    return decorator
