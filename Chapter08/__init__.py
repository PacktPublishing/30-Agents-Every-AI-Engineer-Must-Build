# ──────────────────────────────────────────────────────────────
# utils/__init__.py — Public API for Chapter 8 Utilities
# Chapter 8: Data Analysis and Reasoning Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# ──────────────────────────────────────────────────────────────

from utils.config import load_api_key                     # noqa: F401
from utils.color_logger import info, success, error       # noqa: F401
from utils import color_logger as log                     # noqa: F401
from utils.mock_llm import MockLLM, llm_call              # noqa: F401
from utils.mock_llm import fail_gracefully                # noqa: F401

__all__ = [
    "load_api_key",
    "log",
    "MockLLM",
    "llm_call",
    "fail_gracefully",
]
