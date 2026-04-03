# src/resilience.py
# Author: Imran Ahmad
# Ref: Chapter 16 — Embodied and Physical World Agents
# Visual Logging Schema specification + §Multi-rate perception-action integration
#
# Provides:
#   - ColorLogger: ANSI-colored log output for Jupyter notebooks
#   - fail_gracefully: Decorator factory with retry, backoff, and fallback
#   - logger: Pre-instantiated singleton for immediate use

import functools
import time
import traceback


class ColorLogger:
    """ANSI color-coded logger for Chapter 16 agent operations.

    Color schema (Visual Logging Schema specification):
        Blue   INFO       — Neutral operational messages
        Green  SUCCESS    — Completed operations, green-envelope confirmations
        Red    ERROR      — Constraint violations, safety failures, exceptions
        Yellow SIMULATION — Mock/simulation mode indicators, AMBER warnings

    Each log line optionally includes a bold section reference for traceability.
    ANSI escape codes render natively in Jupyter notebook output cells.
    """

    # ANSI escape codes
    _BLUE = "\033[94m"
    _GREEN = "\033[92m"
    _RED = "\033[91m"
    _YELLOW = "\033[93m"
    _BOLD = "\033[1m"
    _RESET = "\033[0m"

    def _format(self, color: str, tag: str, message: str,
                section_ref: str = "") -> str:
        """Build a formatted log line with optional bold section reference."""
        ref_part = ""
        if section_ref:
            ref_part = f" {self._BOLD}[{section_ref}]{self._RESET}"
        return f"{color}[{tag}]{self._RESET}{ref_part} {message}"

    def info(self, message: str, section_ref: str = "") -> None:
        """Blue INFO — neutral operational messages."""
        print(self._format(self._BLUE, "INFO", message, section_ref))

    def success(self, message: str, section_ref: str = "") -> None:
        """Green SUCCESS — completed operations, constraint satisfaction."""
        print(self._format(self._GREEN, "SUCCESS", message, section_ref))

    def error(self, message: str, section_ref: str = "") -> None:
        """Red ERROR — constraint violations, safety failures, exceptions."""
        print(self._format(self._RED, "ERROR", message, section_ref))

    def simulation(self, message: str, section_ref: str = "") -> None:
        """Yellow SIMULATION — mock mode indicators, AMBER warnings."""
        print(self._format(self._YELLOW, "SIMULATION", message, section_ref))

    def warning(self, message: str, section_ref: str = "") -> None:
        """Yellow WARNING — alias for non-simulation amber messages."""
        print(self._format(self._YELLOW, "WARNING", message, section_ref))

    def constraint(self, domain: str, met: bool,
                   detail: str = "", section_ref: str = "") -> None:
        """Log a constraint domain check result as GREEN or RED."""
        if met:
            status = f"{self._GREEN}GREEN{self._RESET}"
        else:
            status = f"{self._RED}RED{self._RESET}"
        msg = f"{domain}: {status}"
        if detail:
            msg += f" — {detail}"
        tag_color = self._GREEN if met else self._RED
        tag = "PASS" if met else "FAIL"
        print(self._format(tag_color, tag, msg, section_ref))


def fail_gracefully(fallback_value=None, section_ref="",
                    max_retries=1, backoff_base=1.0):
    """Decorator factory: wrap a function with retry, exponential backoff,
    and a fallback return value on exhausted retries.

    Ref: §Multi-rate perception-action integration — every agent tool must
    be wrapped to ensure the system remains stable during failure scenarios.

    Args:
        fallback_value: Value returned when all retries are exhausted.
        section_ref:    Chapter section reference for log traceability.
        max_retries:    Number of retry attempts (0 = no retries, just catch).
        backoff_base:   Base delay in seconds for exponential backoff.

    Usage (recommended pattern from Strategy §7.3):
        @tool
        def check_flight_safety(state_json: str) -> dict:
            '''Docstring for LangChain tool schema.'''
            return _check_flight_safety_impl(state_json)

        @fail_gracefully(fallback_value={}, section_ref="§Constraint formalization")
        def _check_flight_safety_impl(state_json: str) -> dict:
            # Actual implementation
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    if attempt < max_retries:
                        delay = backoff_base * (2 ** attempt)
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed "
                            f"for {func.__name__}: {exc}. "
                            f"Retrying in {delay:.1f}s...",
                            section_ref=section_ref,
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts exhausted for "
                            f"{func.__name__}: {exc}. "
                            f"Returning fallback value.",
                            section_ref=section_ref,
                        )
            # Return a copy of fallback_value if it's mutable
            if isinstance(fallback_value, dict):
                return dict(fallback_value)
            if isinstance(fallback_value, list):
                return list(fallback_value)
            return fallback_value
        return wrapper
    return decorator


# Pre-instantiated singleton — import as: from src.resilience import logger
logger = ColorLogger()
