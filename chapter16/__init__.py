# src/__init__.py
# Author: Imran Ahmad
# Ref: Chapter 16 — Embodied and Physical World Agents
#
# Package init for the chapter16-embodied-agents support library.
# Exports the core utilities needed by the notebook:
#   - get_llm:          LLM factory (MockChatOpenAI or ChatOpenAI)
#   - ColorLogger:      ANSI-colored logger class
#   - fail_gracefully:  Resilience decorator factory
#   - logger:           Pre-instantiated ColorLogger singleton
#   - SIMULATION_MODE:  Module-level flag detected at import time

import os
import sys

from resilience import ColorLogger, fail_gracefully, logger
from mock_layer import get_llm

# ---------------------------------------------------------------------------
# SIMULATION_MODE detection
# ---------------------------------------------------------------------------
# Cascading fallback: .env → environment variable → Simulation Mode
# Ref: Strategy §1.3 Data Flow — Simulation Mode vs. Live Mode
#
# This flag is set at import time. The notebook reads it to decide
# whether to call get_llm(True) or get_llm(False).
# ---------------------------------------------------------------------------

def _detect_simulation_mode() -> bool:
    """Detect whether to run in Simulation Mode.

    Returns True (simulation) if no valid OPENAI_API_KEY is available.
    The notebook may override this after a getpass prompt.
    """
    # Attempt to load .env if python-dotenv is available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    key = os.environ.get("OPENAI_API_KEY", "")
    if key and key != "your-openai-api-key-here" and key.startswith("sk-"):
        return False
    return True


SIMULATION_MODE: bool = _detect_simulation_mode()

__all__ = [
    "get_llm",
    "ColorLogger",
    "fail_gracefully",
    "logger",
    "SIMULATION_MODE",
]
