# =============================================================================
# helpers/color_logger.py
# Chapter 7: Tool Manipulation and Orchestration Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026 — B34135)
# Ref: Section 7.3 — Comprehensive Logging and Telemetry
#
# Provides color-coded visual logging for all agent actions.
# Every agent, tool, and orchestrator in the notebook uses these functions
# to produce a clear, pedagogical trail of execution.
# =============================================================================

from datetime import datetime

# ---------------------------------------------------------------------------
# Module-Level Flags
# ---------------------------------------------------------------------------

SHOW_TIMESTAMPS: bool = False
"""Prepend ISO timestamp to each log line. Set True for debugging."""

ENABLE_COLOR: bool = True
"""Set False for non-ANSI terminals (e.g., legacy cmd.exe on Windows)."""

# ---------------------------------------------------------------------------
# ANSI Color Codes
# ---------------------------------------------------------------------------

_BLUE = "\033[94m"
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_RESET = "\033[0m"
_BOLD = "\033[1m"


# ---------------------------------------------------------------------------
# Internal Helper
# ---------------------------------------------------------------------------

def _format(color: str, badge: str, message: str) -> str:
    """Build a formatted log line with optional timestamp and color."""
    timestamp = ""
    if SHOW_TIMESTAMPS:
        timestamp = f"{datetime.now().isoformat(timespec='seconds')} "

    if ENABLE_COLOR:
        return f"{color}{_BOLD}{timestamp}{badge}{_RESET}{color} {message}{_RESET}"
    return f"{timestamp}{badge} {message}"


# ---------------------------------------------------------------------------
# Public Logging Functions
# ---------------------------------------------------------------------------

def log_info(message: str) -> None:
    """Blue [INFO] — General informational messages about agent operations."""
    print(_format(_BLUE, "[INFO]", message))


def log_success(message: str) -> None:
    """Green [SUCCESS] — Tool or agent step completed successfully."""
    print(_format(_GREEN, "[SUCCESS]", message))


def log_error(message: str) -> None:
    """Red [ERROR] — Exception caught, fallback activated."""
    print(_format(_RED, "[ERROR]", message))


def log_warning(message: str) -> None:
    """Yellow [WARNING] — Threshold breached or escalation triggered."""
    print(_format(_YELLOW, "[WARNING]", message))


def log_mock(message: str) -> None:
    """Cyan [MOCK] — Simulation Mode data returned instead of live API call."""
    print(_format(_CYAN, "[MOCK]", message))


def log_step(section: str, step: int, description: str) -> None:
    """Blue [Section X | Step N] — Pedagogical step marker combining section
    reference with step numbering for a clear execution trail.

    Parameters
    ----------
    section : str
        Chapter section reference, e.g. "7.1".
    step : int
        Step number within the current section workflow.
    description : str
        Human-readable description of what this step does.
    """
    badge = f"[Section {section} | Step {step}]"
    print(_format(_BLUE, badge, description))
