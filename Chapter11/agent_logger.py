# agent_logger.py
# Chapter 11: Multi-Modal Perception Agents
# Book: 30 Agents Every AI Engineer Must Build
# Author: Imran Ahmad | Publisher: Packt Publishing
#
# Color-coded logging utility and resilience decorator used across
# all three agent domains (Vision-Language, Audio Processing,
# Physical World Sensing).
# Ref: Cross-cutting utility — all chapter sections

import functools
import time
import traceback


class AgentLogger:
    """
    Color-coded logger for multi-modal agent output.

    Color schema:
        BLUE  — informational messages (mode banners, initialization)
        GREEN — successful completions (agent actions, tool results)
        RED   — errors and failures (exceptions, fallback activations)

    Ref: Cross-cutting utility for Chapter 11 agent demonstrations.
    """

    # ANSI escape codes
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    # Set to False to disable ANSI codes (e.g., environments that
    # render raw escape sequences). See troubleshooting.md Issue 7.
    USE_ANSI = True

    @classmethod
    def _fmt(cls, color: str, prefix: str, message: str) -> str:
        if cls.USE_ANSI:
            return f"{color}{cls.BOLD}[{prefix}]{cls.RESET}{color} {message}{cls.RESET}"
        return f"[{prefix}] {message}"

    @classmethod
    def info(cls, message: str) -> None:
        """Blue informational message."""
        print(cls._fmt(cls.BLUE, "INFO", message))

    @classmethod
    def success(cls, message: str) -> None:
        """Green success message."""
        print(cls._fmt(cls.GREEN, "SUCCESS", message))

    @classmethod
    def error(cls, message: str) -> None:
        """Red error message."""
        print(cls._fmt(cls.RED, "ERROR", message))


def graceful_fallback(max_retries: int = 2, base_delay: float = 1.0):
    """
    Decorator that wraps agent inference methods with retry logic
    and structured error reporting.

    Implements exponential backoff: delay doubles after each attempt.
    On final failure, logs a RED error and returns a descriptive
    fallback dictionary rather than raising an unhandled exception.

    Args:
        max_retries: Maximum number of retry attempts before fallback.
        base_delay: Initial delay in seconds between retries.

    Returns:
        Decorated function with resilience guarantees.

    Ref: Cross-cutting resilience pattern for all Chapter 11 agents.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exception = None

            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    AgentLogger.error(
                        f"{func.__name__} attempt {attempt}/{max_retries} "
                        f"failed: {type(exc).__name__}: {exc}"
                    )
                    if attempt < max_retries:
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff

            # All retries exhausted — return structured fallback
            AgentLogger.error(
                f"{func.__name__} failed after {max_retries} attempts. "
                f"Returning fallback response."
            )
            return {
                "error": True,
                "function": func.__name__,
                "exception": str(last_exception),
                "exception_type": type(last_exception).__name__,
                "message": (
                    f"{func.__name__} failed: {type(last_exception).__name__}. "
                    f"Falling back."
                ),
            }
        return wrapper
    return decorator
