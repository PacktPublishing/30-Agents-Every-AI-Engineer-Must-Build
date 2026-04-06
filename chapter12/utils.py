# src/utils.py
# Author: Imran Ahmad
# Book: 30 Agents Every AI Engineer Must Build, Chapter 12
# Ref: Technical Requirements (p.2), Production Failure Modes (p.35)
# Description: Shared utilities — color-coded logging, resilience decorator,
#              API key resolution, and mode detection.

import os
import sys
import time
import functools
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on os.environ directly


# ---------------------------------------------------------------------------
# §5.1  Color-Coded Logging Schema
# ---------------------------------------------------------------------------

class ColorLogger:
    """
    ANSI color-coded logger for notebook and terminal output.

    Levels:
        DEBUG   — Yellow  (\\033[93m) — Agent initialization, internal state
        INFO    — Blue    (\\033[94m) — Simulation Mode banners, progress
        SUCCESS — Green   (\\033[92m) — Step completions, passed checks
        ERROR   — Red     (\\033[91m) — Handled errors, fallback activations

    Ref: Strategy §5.1, Color-Coded Logging Schema
    """

    COLORS = {
        "DEBUG":   "\033[93m",   # Yellow
        "INFO":    "\033[94m",   # Blue
        "SUCCESS": "\033[92m",   # Green
        "ERROR":   "\033[91m",   # Red
    }
    RESET = "\033[0m"

    def __init__(self, name: str = "Chapter12"):
        self.name = name

    def _log(self, level: str, message: str) -> None:
        color = self.COLORS.get(level, self.RESET)
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{level}] {ts} | {self.name} | {message}{self.RESET}")

    def debug(self, message: str) -> None:
        """Yellow — internal state, initialization."""
        self._log("DEBUG", message)

    def info(self, message: str) -> None:
        """Blue — Simulation Mode banners, progress updates."""
        self._log("INFO", message)

    def success(self, message: str) -> None:
        """Green — step completions, checks passed."""
        self._log("SUCCESS", message)

    def error(self, message: str) -> None:
        """Red — handled errors, fallback activations."""
        self._log("ERROR", message)


# Module-level logger instance for convenience
logger = ColorLogger("Chapter12")


# ---------------------------------------------------------------------------
# §5.2  @graceful_fallback Decorator
# ---------------------------------------------------------------------------

def graceful_fallback(fallback_value=None, section_ref="Chapter 12", retries=3):
    """
    Decorator that catches exceptions, applies exponential backoff on
    retryable errors (HTTP 429), and returns a fallback value on failure.

    Applied to every method that: (a) calls an LLM, (b) calls an external
    API, or (c) performs computation that could raise (SHAP, LIME).

    Parameters
    ----------
    fallback_value : callable or static value
        If callable, invoked with (*args, **kwargs) to produce the fallback.
        If static, returned directly on failure.
    section_ref : str
        Chapter section reference for the error log message.
    retries : int
        Number of retry attempts with exponential backoff (2s, 4s, 8s).

    Ref: Strategy §5.2, Failure Mode Matrix §5.3
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    exc_name = type(exc).__name__
                    # Retryable: rate limits, timeouts
                    if _is_retryable(exc) and attempt < retries - 1:
                        wait = 2 ** (attempt + 1)
                        logger.error(
                            f"[Retry {attempt + 1}/{retries}] {exc_name} "
                            f"in {func.__name__}. Retrying in {wait}s. "
                            f"Ref: {section_ref}"
                        )
                        time.sleep(wait)
                        continue
                    # Non-retryable or final attempt: fall back
                    logger.error(
                        f"[HANDLED ERROR] {exc_name} in {func.__name__}. "
                        f"Falling back to mock logic. Ref: {section_ref}"
                    )
                    break

            # Return fallback value
            if callable(fallback_value):
                try:
                    return fallback_value(*args, **kwargs)
                except TypeError:
                    return fallback_value()
            return fallback_value

        return wrapper
    return decorator


def _is_retryable(exc: Exception) -> bool:
    """Check if an exception is retryable (rate limits, timeouts)."""
    exc_str = str(exc).lower()
    retryable_signals = ["429", "rate limit", "timeout", "timed out"]
    return any(signal in exc_str for signal in retryable_signals)


# ---------------------------------------------------------------------------
# API Key Resolution & Mode Detection
# Ref: Strategy §1.3 (Mode Detection Flow), Tech Requirements (p.2)
# ---------------------------------------------------------------------------

_CURRENT_MODE = None  # Cached after first resolution


def resolve_api_key() -> str:
    """
    Cascading API key resolution:
        1. os.environ / .env  →  OPENAI_API_KEY
        2. getpass prompt     →  (interactive terminals only)
        3. Empty string       →  triggers Simulation Mode

    Returns the resolved key (may be empty).
    Ref: Strategy §1.3, Mode Detection Flow
    """
    global _CURRENT_MODE

    # Step 1: Environment variable (includes .env via python-dotenv)
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key and "your-key" not in key and "your_key" not in key:
        _CURRENT_MODE = "live"
        logger.success("API key detected from environment. Live Mode enabled.")
        return key

    # Step 2: Interactive getpass (only if stdin is a terminal)
    if sys.stdin.isatty():
        try:
            import getpass
            key = getpass.getpass(
                "[Chapter 12] Enter OpenAI API key (or press Enter for Simulation Mode): "
            ).strip()
            if key:
                os.environ["OPENAI_API_KEY"] = key
                _CURRENT_MODE = "live"
                logger.success("API key entered via prompt. Live Mode enabled.")
                return key
        except (EOFError, OSError):
            pass  # Non-interactive environment; fall through

    # Step 3: No key → Simulation Mode
    _CURRENT_MODE = "simulation"
    logger.info(
        "No API key detected. Running in Simulation Mode with chapter-derived "
        "mock data. All outputs are synthetic. Supply an OpenAI API key via "
        ".env for live mode."
    )
    return ""


def get_mode() -> str:
    """
    Return the current operating mode: 'live' or 'simulation'.

    If resolve_api_key() has not been called yet, calls it to determine
    the mode.
    """
    global _CURRENT_MODE
    if _CURRENT_MODE is None:
        resolve_api_key()
    return _CURRENT_MODE


def is_simulation() -> bool:
    """Convenience check: True if running in Simulation Mode."""
    return get_mode() == "simulation"


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    log = ColorLogger("SelfTest")
    log.debug("Debug message — Yellow")
    log.info("Info message — Blue")
    log.success("Success message — Green")
    log.error("Error message — Red")

    print(f"\nMode: {get_mode()}")

    # Test @graceful_fallback
    @graceful_fallback(
        fallback_value={"status": "fallback_triggered"},
        section_ref="Self-test",
        retries=1,
    )
    def will_fail():
        raise ValueError("Intentional test failure")

    result = will_fail()
    print(f"Fallback result: {result}")
    log.success("Self-test complete.")
