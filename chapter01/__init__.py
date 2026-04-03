"""
Chapter 1: Foundations of Agent Engineering
Book: "AI Agents" by Imran Ahmad (Packt, 2026)
"""

__version__ = "1.0.0"
__author__ = "Imran Ahmad"
__book__ = "AI Agents"
__chapter__ = "1 - Foundations of Agent Engineering"

from .mock_llm import MockLLM, MockResponse
from .utils import (
    log_info, log_success, log_error, log_warning,
    graceful_fallback, detect_api_key, simulation_mode_banner
)
