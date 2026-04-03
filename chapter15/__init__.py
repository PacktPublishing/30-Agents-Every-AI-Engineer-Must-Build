# ===========================================================================
# utils/__init__.py — Package Exports
# Chapter 15: Education and Knowledge Agents
# Book: 30 Agents Every AI Engineer Must Build (Packt Publishing)
# Author: Imran Ahmad
#
# Exports cross-cutting infrastructure for the notebook:
#   - MockLLM: Simulation-mode LLM with section-mapped response registry
#   - ColorLogger: ANSI color-coded execution tracing
#   - LogLevel: Enum for log levels (INFO, SUCCESS, WARN, ERROR)
#   - graceful_fallback: Decorator for fault-tolerant LLM/IO calls
# ===========================================================================

from utils.resilience import ColorLogger, LogLevel, graceful_fallback
from utils.mock_llm import MockLLM

__all__ = [
    "MockLLM",
    "ColorLogger",
    "LogLevel",
    "graceful_fallback",
]
