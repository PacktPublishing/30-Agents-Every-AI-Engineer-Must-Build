"""
agent_logger.py — Color-Coded Logging Utility & Resilience Decorator
=====================================================================
Book:    30 Agents Every AI Engineer Must Build
Author:  Imran Ahmad
Chapter: 11 — Multi-Modal Perception Agents
Ref:     Cross-cutting utility used by all three agent domains

Provides:
    - AgentLogger: Color-coded console logger (BLUE info, GREEN success, RED error)
    - graceful_fallback: Decorator that catches exceptions, logs RED errors,
      and returns a safe fallback value so notebooks never crash.
"""

from __future__ import annotations

import functools
import sys
from datetime import datetime
from typing import Any, Callable


class AgentLogger:
    """Color-coded logger for multi-modal agent output.

    Ref: Cross-cutting — used in all chapter sections.
    Author: Imran Ahmad

    Color schema:
        .info()    → BLUE   — Informational / status messages
        .success() → GREEN  — Successful operation completion
        .error()   → RED    — Errors, failures, critical alerts
    """

    # ANSI escape codes
    _BLUE = "\033[94m"
    _GREEN = "\033[92m"
    _RED = "\033[91m"
    _BOLD = "\033[1m"
    _RESET = "\033[0m"

    # Set to False if your terminal does not render ANSI codes.
    # See troubleshooting.md — Issue 7.
    USE_ANSI: bool = True

    def __init__(self, name: str = "Agent") -> None:
        self.name = name

    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _format(self, level: str, color: str, message: str) -> str:
        ts = self._timestamp()
        if self.USE_ANSI:
            return (
                f"{color}{self._BOLD}[{ts}] [{level}] "
                f"[{self.name}]{self._RESET} {color}{message}{self._RESET}"
            )
        return f"[{ts}] [{level}] [{self.name}] {message}"

    def info(self, message: str) -> None:
        """Log an informational message in BLUE."""
        print(self._format("INFO", self._BLUE, message))

    def success(self, message: str) -> None:
        """Log a success message in GREEN."""
        print(self._format("SUCCESS", self._GREEN, message))

    def error(self, message: str) -> None:
        """Log an error message in RED."""
        print(self._format("ERROR", self._RED, message))


def graceful_fallback(
    fallback_value: Any = None,
    chapter_ref: str = "",
) -> Callable:
    """Decorator: catch exceptions, log RED error, return fallback value.

    Ref: Cross-cutting resilience pattern.
    Author: Imran Ahmad

    Usage::

        @graceful_fallback(fallback_value="N/A", chapter_ref="Building a Vision QA Agent")
        def answer_question(self, image, question):
            ...

    Args:
        fallback_value: Value returned when the wrapped function raises.
        chapter_ref:    Chapter section cited in the error log.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Attempt to find an AgentLogger on the instance (first arg = self)
            logger = None
            if args and hasattr(args[0], "logger"):
                logger = args[0].logger
            if logger is None:
                logger = AgentLogger(name=func.__qualname__)

            try:
                return func(*args, **kwargs)
            except Exception as exc:
                ref_tag = f" [Ref: {chapter_ref}]" if chapter_ref else ""
                logger.error(
                    f"{func.__name__} failed: {type(exc).__name__}: {exc}. "
                    f"Falling back to {fallback_value!r}.{ref_tag}"
                )
                return fallback_value

        return wrapper

    return decorator
