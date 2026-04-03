"""
Chapter 05 — Foundational Cognitive Architectures
Book: 30 Agents Every AI Engineer Must Build
Author: Imran Ahmad
Publisher: Packt Publishing

Color-coded logging utilities for visual tracing of agent logic.
Provides timestamped, ANSI-colored console output compatible with
Jupyter Notebook, JupyterLab, VS Code, and standard terminals.

Ref: Engineering Best Practices — Observability (p. 31)
"Implement comprehensive logging at every stage of the agent's
decision loop, from initial perception and prompt formulation
to tool calls and final actions."
"""

from datetime import datetime


# ── ANSI escape codes ──────────────────────────────────────────────
_BLUE = "\033[94m"
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


def _timestamp() -> str:
    """Return current time as HH:MM:SS string."""
    return datetime.now().strftime("%H:%M:%S")


def log_info(message: str) -> None:
    """Log an informational message in blue.

    Use for: initialization, tool invocation, state changes,
    perception inputs, and general progress updates.

    Args:
        message: The message to display.

    Chapter Reference:
        Engineering Best Practices — Observability (p. 31)
    """
    print(f"{_BLUE}[INFO  {_timestamp()}]{_RESET} {message}")


def log_success(message: str) -> None:
    """Log a success message in green.

    Use for: completed steps, valid outputs, passed safety checks,
    and successful action executions.

    Args:
        message: The message to display.

    Chapter Reference:
        Engineering Best Practices — Observability (p. 31)
    """
    print(f"{_GREEN}[SUCCESS {_timestamp()}]{_RESET} {message}")


def log_error(message: str) -> None:
    """Log an error message in red.

    Use for: failures, fallback activations, handled exceptions,
    and safety violations.

    Args:
        message: The message to display.

    Chapter Reference:
        Engineering Best Practices — Robustness (p. 32)
    """
    print(f"{_RED}[ERROR {_timestamp()}]{_RESET} {message}")


def log_warn(message: str) -> None:
    """Log a warning message in yellow.

    Use for: mock mode notifications, non-critical warnings,
    low-confidence scores, and near-threshold conditions.

    Args:
        message: The message to display.

    Chapter Reference:
        Engineering Best Practices — Observability (p. 31)
    """
    print(f"{_YELLOW}[WARN  {_timestamp()}]{_RESET} {message}")


def log_section(title: str, chapter_ref: str = "") -> None:
    """Print a bold section divider with optional chapter reference.

    Use to visually separate major phases of agent execution
    (e.g., Perception, Cognition, Action, Learning).

    Args:
        title: Section heading text.
        chapter_ref: Optional chapter reference string
            (e.g., "Section 5.1, pp. 3-16").

    Chapter Reference:
        Engineering Best Practices — Observability (p. 31)
    """
    ref_str = f"  [{chapter_ref}]" if chapter_ref else ""
    divider = "─" * 60
    print(f"\n{_BOLD}{divider}")
    print(f"  {title}{ref_str}")
    print(f"{divider}{_RESET}\n")
