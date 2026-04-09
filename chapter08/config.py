# ──────────────────────────────────────────────────────────────
# utils/config.py — Three-Tier API Key Resolution
# Chapter 8: Data Analysis and Reasoning Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Ref: Strategy §4.1
# ──────────────────────────────────────────────────────────────
# Tier 1: python-dotenv → load_dotenv() → reads .env
# Tier 2: os.getenv("OPENAI_API_KEY")
# Tier 3: getpass.getpass() with skip-for-simulation prompt
# Result: Returns (key: str | None, simulation_mode: bool)
# ──────────────────────────────────────────────────────────────

from __future__ import annotations

import os
import sys


_LLM_PROVIDER = None


def load_api_key() -> tuple[str | None, bool]:
    """Resolve an API key through a multi-provider cascade.

    Supports OpenAI, Anthropic, and Google Gemini via LLM_PROVIDER env var.

    Returns
    -------
    tuple[str | None, bool]
        (api_key, simulation_mode) — If no valid key is found,
        simulation_mode is True and api_key is None.

    Ref: Strategy §4.1 — Zero-Hardcode Policy.
    """
    global _LLM_PROVIDER

    # ── Tier 1: .env file via python-dotenv ──────────────────
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # ── Tier 2: Multi-provider detection ─────────────────────
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from supporting.llm_provider import detect_provider
        provider, key, mode = detect_provider()
        _LLM_PROVIDER = provider
        if mode == "LIVE":
            return key, False
    except ImportError:
        pass  # Fall through to legacy

    # ── Legacy: OPENAI_API_KEY environment variable ──────────
    key = os.getenv("OPENAI_API_KEY")
    if key and key.strip() and "your-key" not in key and "your_key" not in key:
        _LLM_PROVIDER = "openai"
        return key.strip(), False

    # ── Tier 3: Interactive prompt (skipped in non-TTY) ──────
    try:
        if sys.stdin and sys.stdin.isatty():
            import getpass
            key = getpass.getpass(
                "Enter API key (OpenAI/Anthropic/Google) or press Enter for Simulation: "
            )
            if key and key.strip():
                _LLM_PROVIDER = "openai"
                return key.strip(), False
    except (EOFError, OSError, KeyboardInterrupt):
        pass

    # ── No key found → Simulation Mode ───────────────────────
    _LLM_PROVIDER = "simulation"
    return None, True


def get_provider() -> str:
    """Return the detected LLM provider name."""
    global _LLM_PROVIDER
    return _LLM_PROVIDER or "simulation"
