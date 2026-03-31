# ──────────────────────────────────────────────────────────────
# utils/color_logger.py — Color-Coded Visual Logging
# Chapter 8: Data Analysis and Reasoning Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Ref: Strategy §4.2
# ──────────────────────────────────────────────────────────────
# info(msg)    → Blue   \033[94m  [INFO HH:MM:SS]
# success(msg) → Green  \033[92m  [SUCCESS HH:MM:SS]
# error(msg)   → Red    \033[91m  [HANDLED ERROR HH:MM:SS]
#
# Set CH08_NO_COLOR=1 to strip ANSI codes (plain-text loggers).
# ──────────────────────────────────────────────────────────────

from __future__ import annotations

import os
from datetime import datetime

# ── ANSI codes ───────────────────────────────────────────────
_BLUE = "\033[94m"
_GREEN = "\033[92m"
_RED = "\033[91m"
_RESET = "\033[0m"

_NO_COLOR = os.getenv("CH08_NO_COLOR", "").strip() in ("1", "true", "yes")


def _timestamp() -> str:
    """Return current time as HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")


def info(msg: str, section: str = "") -> None:
    """Log an informational message in Blue.

    Parameters
    ----------
    msg : str
        The message to display.
    section : str, optional
        Chapter section reference (e.g., "8.1.1").
    """
    sec = f" §{section}" if section else ""
    prefix = f"[INFO {_timestamp()}{sec}]"
    if _NO_COLOR:
        print(f"{prefix} {msg}")
    else:
        print(f"{_BLUE}{prefix}{_RESET} {msg}")


def success(msg: str, section: str = "") -> None:
    """Log a success message in Green.

    Parameters
    ----------
    msg : str
        The message to display.
    section : str, optional
        Chapter section reference (e.g., "8.4").
    """
    sec = f" §{section}" if section else ""
    prefix = f"[SUCCESS {_timestamp()}{sec}]"
    if _NO_COLOR:
        print(f"{prefix} {msg}")
    else:
        print(f"{_GREEN}{prefix}{_RESET} {msg}")


def error(msg: str, section: str = "") -> None:
    """Log a handled error message in Red.

    Parameters
    ----------
    msg : str
        The message to display.
    section : str, optional
        Chapter section reference (e.g., "8.2.5").
    """
    sec = f" §{section}" if section else ""
    prefix = f"[HANDLED ERROR {_timestamp()}{sec}]"
    if _NO_COLOR:
        print(f"{prefix} {msg}")
    else:
        print(f"{_RED}{prefix}{_RESET} {msg}")
