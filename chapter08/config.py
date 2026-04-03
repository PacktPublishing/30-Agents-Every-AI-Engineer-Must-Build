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


def load_api_key() -> tuple[str | None, bool]:
    """Resolve the OpenAI API key through a three-tier cascade.

    Returns
    -------
    tuple[str | None, bool]
        (api_key, simulation_mode) — If no valid key is found,
        simulation_mode is True and api_key is None.

    Ref: Strategy §4.1 — Zero-Hardcode Policy.
    """
    # ── Tier 1: .env file via python-dotenv ──────────────────
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv not installed; fall through

    # ── Tier 2: Environment variable ─────────────────────────
    key = os.getenv("OPENAI_API_KEY")
    if key and key.strip() and key.strip() != "your-key-here":
        return key.strip(), False

    # ── Tier 3: Interactive prompt (skipped in non-TTY) ──────
    try:
        if sys.stdin and sys.stdin.isatty():
            import getpass
            key = getpass.getpass(
                "Enter OpenAI API key (or press Enter for Simulation Mode): "
            )
            if key and key.strip():
                return key.strip(), False
    except (EOFError, OSError, KeyboardInterrupt):
        pass  # Non-interactive environment; fall through

    # ── No key found → Simulation Mode ───────────────────────
    return None, True
