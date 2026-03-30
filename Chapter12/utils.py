"""
Utility module: Color-coded logging, resilience decorators, and mode detection.

Author: Imran Ahmad
Book: 30 Agents Every AI Engineer Must Build, Chapter 12
Section Reference: Tech Requirements (p.2), Resilience Layer (p.35)
"""

import os
import functools
import getpass
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Section 5.1 — Color-Coded Logging Schema (p.2, p.35)
# Blue=[INFO], Green=[SUCCESS], Red=[HANDLED ERROR], Yellow=[DEBUG]
# ---------------------------------------------------------------------------

class ColorLogger:
    """
    Color-coded logger for notebook and terminal output.
    Uses ANSI escape codes as specified in Chapter 12 resilience layer.

    Color map (Section 5.1):
        DEBUG        -> Yellow  (\\033[93m)
        INFO         -> Blue    (\\033[94m)
        SUCCESS      -> Green   (\\033[92m)
        HANDLED ERROR -> Red    (\\033[91m)
    """

    RESET = "\033[0m"
    COLORS = {
        "DEBUG":         "\033[93m",   # Yellow
        "INFO":          "\033[94m",   # Blue
        "SUCCESS":       "\033[92m",   # Green
        "HANDLED ERROR": "\033[91m",   # Red
    }

    def __init__(self, name: str = "Chapter12"):
        self.name = name

    def _emit(self, level: str, message: str) -> None:
        color = self.COLORS.get(level, self.RESET)
        tag = f"[{level}]"
        formatted = f"{color}{tag} [{self.name}] {message}{self.RESET}"
        print(formatted)  # Notebook-compatible output

    def debug(self, message: str) -> None:
        """Yellow — internal diagnostics."""
        self._emit("DEBUG", message)

    def info(self, message: str) -> None:
        """Blue — informational banners, mode announcements."""
        self._emit("INFO", message)

    def success(self, message: str) -> None:
        """Green — step completion, passing checks."""
        self._emit("SUCCESS", message)

    def error(self, message: str) -> None:
        """Red — handled errors and fallback activations."""
        self._emit("HANDLED ERROR", message)


# Singleton logger for module-level convenience
logger = ColorLogger()


# ---------------------------------------------------------------------------
# Section 5.2 — @graceful_fallback Decorator (p.35)
# Catches all exceptions, logs failure in red, returns fallback value.
# ---------------------------------------------------------------------------

def graceful_fallback(fallback_value=None, section_ref: str = ""):
    """
    Decorator that wraps any function in a try/except block.

    On exception:
      1. Logs a [HANDLED ERROR] with the section reference.
      2. Returns the fallback_value (callable → called, else returned as-is).

    Args:
        fallback_value: Static value or callable producing the fallback.
        section_ref: Chapter section string for traceability (e.g.,
                     "Section 12 - Bias Detection (p.16)").

    Usage:
        @graceful_fallback(
            fallback_value={"score": 0.0, "source": "fallback"},
            section_ref="Section 12 - Resume Scoring (p.20)"
        )
        def score_resume(candidate):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                ref_tag = f" | Ref: {section_ref}" if section_ref else ""
                logger.error(
                    f"{func.__qualname__}() failed: {type(exc).__name__}: {exc}{ref_tag}. "
                    f"Falling back to safe default."
                )
                if callable(fallback_value):
                    return fallback_value()
                return fallback_value
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Mode Detection — resolve_api_key() and get_mode() (p.2)
# Flow: .env → getpass → Simulation Mode
# ---------------------------------------------------------------------------

_SIMULATION_MODE = None  # Cached after first resolution


def resolve_api_key(interactive: bool = True) -> str:
    """
    Three-tier API key resolution (Section 1.3 — Mode Detection Flow):
      1. Load from .env file via python-dotenv.
      2. If empty and interactive=True, prompt via getpass.
      3. If still empty, return empty string (triggers Simulation Mode).

    Returns:
        The resolved API key string (may be empty).
    """
    global _SIMULATION_MODE

    load_dotenv()
    key = os.getenv("OPENAI_API_KEY", "").strip()

    if not key and interactive:
        try:
            key = getpass.getpass(
                "[INFO] No API key in .env. Enter OpenAI key (or press Enter for Simulation Mode): "
            ).strip()
            if key:
                os.environ["OPENAI_API_KEY"] = key
        except Exception:
            # Handles EOFError, StdinNotImplementedError, etc.
            key = ""

    if key:
        _SIMULATION_MODE = False
        logger.success("API key detected. Running in Live Mode.")
    else:
        _SIMULATION_MODE = True
        logger.info(
            "No API key detected. Running in Simulation Mode with "
            "chapter-derived mock data. All outputs are synthetic. "
            "Supply an OpenAI API key via .env for live mode."
        )

    return key


def get_mode() -> str:
    """
    Return the current operating mode.

    Returns:
        'live' if a valid API key was resolved, 'simulation' otherwise.
    """
    global _SIMULATION_MODE
    if _SIMULATION_MODE is None:
        # First call — attempt non-interactive resolution
        resolve_api_key(interactive=False)
    return "simulation" if _SIMULATION_MODE else "live"


def is_simulation() -> bool:
    """Convenience check for Simulation Mode."""
    return get_mode() == "simulation"


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    log = ColorLogger(name="SelfTest")
    log.debug("Testing Yellow — [DEBUG] level.")
    log.info("Testing Blue — [INFO] level.")
    log.success("Testing Green — [SUCCESS] level.")
    log.error("Testing Red — [HANDLED ERROR] level.")

    # Test graceful_fallback
    @graceful_fallback(
        fallback_value={"result": "safe_default"},
        section_ref="Section 12 - Self-Test (p.0)"
    )
    def risky_function():
        raise RuntimeError("Simulated failure")

    result = risky_function()
    log.success(f"Fallback returned: {result}")

    # Test mode detection (non-interactive for self-test)
    mode = get_mode()
    log.info(f"Detected mode: {mode}")
    log.success("All self-tests passed.")
