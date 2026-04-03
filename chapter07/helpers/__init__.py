# =============================================================================
# helpers/__init__.py
# Chapter 7: Tool Manipulation and Orchestration Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026 — B34135)
#
# Package exports for the helpers module. This allows the notebook to import
# all shared infrastructure with a single line:
#   from helpers import log_info, graceful_fallback, MockLLM
# =============================================================================

# --- Color-Coded Logger (Section 7.3 — Comprehensive Logging) ---
from helpers.color_logger import (
    log_info,
    log_success,
    log_error,
    log_warning,
    log_mock,
    log_step,
    SHOW_TIMESTAMPS,
    ENABLE_COLOR,
)

# --- Resilience Layer (Section 7.3 — Safe Invocation Wrappers) ---
from helpers.resilience import (
    graceful_fallback,
    safe_invoke,
)

# --- Mock LLM (Sections 7.5, 7.6, 7.7, 7.7b — Simulation Mode) ---
from helpers.mock_llm import MockLLM

__all__ = [
    # Logger
    "log_info",
    "log_success",
    "log_error",
    "log_warning",
    "log_mock",
    "log_step",
    "SHOW_TIMESTAMPS",
    "ENABLE_COLOR",
    # Resilience
    "graceful_fallback",
    "safe_invoke",
    # Mock
    "MockLLM",
]
