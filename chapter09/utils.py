# src/utils.py
# Chapter 9: Software Development Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Author: Imran Ahmad
#
# Cross-cutting utilities: environment management, color-coded logging,
# and the @fail_gracefully resilience decorator.
# Ref: Strategy §2.2 — shared infrastructure across all notebook sections.

import os
import sys
import time
import functools
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Environment & API Key Management
# ---------------------------------------------------------------------------

# Load .env from repository root (no-op if file absent)
load_dotenv()

_API_KEY = None
_SIMULATION_MODE = None
_LLM_PROVIDER = None


def get_api_key():
    """
    Zero-hardcode API key resolution chain:
      1. .env file (via python-dotenv)
      2. Environment variable OPENAI_API_KEY (or ANTHROPIC/GOOGLE via LLM_PROVIDER)
      3. Interactive getpass prompt (skipped in non-interactive envs)
      4. Simulation Mode fallback (returns None)

    Returns:
        str or None: The API key, or None to activate Simulation Mode.
    """
    global _API_KEY, _SIMULATION_MODE, _LLM_PROVIDER

    # Multi-provider: try shared provider detection first
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from supporting.llm_provider import detect_provider
        provider, key, mode = detect_provider()
        _LLM_PROVIDER = provider
        if mode == "LIVE":
            _API_KEY = key
            _SIMULATION_MODE = False
            ColorLog.success(f"API key loaded — provider: {provider}")
            return _API_KEY
    except ImportError:
        pass  # Fall through to legacy detection

    # Legacy: Check OPENAI_API_KEY environment variable
    key = os.getenv("OPENAI_API_KEY")
    if key and key.strip() and "your-key" not in key and "your_key" not in key:
        _API_KEY = key.strip()
        _SIMULATION_MODE = False
        _LLM_PROVIDER = "openai"
        ColorLog.success("API key loaded from environment.")
        return _API_KEY

    # Attempt interactive prompt (safe for non-interactive envs)
    if sys.stdin.isatty():
        try:
            import getpass
            key = getpass.getpass(
                "Enter API key (OpenAI/Anthropic/Google) or press Enter for Simulation: "
            )
            if key and key.strip():
                _API_KEY = key.strip()
                _SIMULATION_MODE = False
                _LLM_PROVIDER = "openai"  # default assumption
                ColorLog.success("API key entered manually.")
                return _API_KEY
        except (EOFError, OSError):
            pass

    # Fall through to Simulation Mode
    _API_KEY = None
    _SIMULATION_MODE = True
    _LLM_PROVIDER = "simulation"
    ColorLog.info(
        "No API key detected — activating Simulation Mode (MockLLM)."
    )
    return None


def is_simulation_mode():
    """
    Returns True if the system is operating in Simulation Mode.
    Must be called after get_api_key().
    """
    global _SIMULATION_MODE
    if _SIMULATION_MODE is None:
        get_api_key()
    return _SIMULATION_MODE


def get_provider():
    """Return the detected LLM provider name.

    Returns:
        str: "openai", "anthropic", "google", or "simulation"
    """
    global _LLM_PROVIDER
    if _LLM_PROVIDER is None:
        get_api_key()
    return _LLM_PROVIDER


def get_llm(model=None, temperature=0, **kwargs):
    """Return a LangChain-compatible chat model for the detected provider.

    Falls back to MockLLM if in Simulation Mode.

    Args:
        model: Model name override.
        temperature: Model temperature.

    Returns:
        A LangChain BaseChatModel or MockLLM instance.
    """
    if is_simulation_mode():
        from chapter09.mock_llm import MockLLM
        return MockLLM()

    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from supporting.llm_provider import get_llm as _get_llm
        return _get_llm(
            provider=get_provider(),
            model=model,
            api_key=_API_KEY,
            temperature=temperature,
            **kwargs,
        )
    except ImportError:
        # Fallback to OpenAI directly
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model or "gpt-4o",
            temperature=temperature,
            api_key=_API_KEY,
            **kwargs,
        )


# ---------------------------------------------------------------------------
# Color-Coded Logging — ColorLog
# ---------------------------------------------------------------------------

class ColorLog:
    """
    ANSI color-coded logging utility for pedagogical output.

    Blue  [INFO]           — informational messages, workflow progress
    Green [SUCCESS]        — successful completions, tests passing
    Red   [HANDLED ERROR]  — caught exceptions, graceful fallbacks

    Respects the NO_COLOR environment variable for terminals that
    do not support ANSI escape codes.
    """

    _BLUE = "\033[94m"
    _GREEN = "\033[92m"
    _RED = "\033[91m"
    _YELLOW = "\033[93m"
    _RESET = "\033[0m"
    _BOLD = "\033[1m"

    @classmethod
    def _use_color(cls):
        return os.getenv("NO_COLOR") is None

    @classmethod
    def info(cls, message):
        if cls._use_color():
            print(f"{cls._BLUE}[INFO]{cls._RESET} {message}")
        else:
            print(f"[INFO] {message}")

    @classmethod
    def success(cls, message):
        if cls._use_color():
            print(f"{cls._GREEN}[SUCCESS]{cls._RESET} {message}")
        else:
            print(f"[SUCCESS] {message}")

    @classmethod
    def error(cls, message):
        if cls._use_color():
            print(f"{cls._RED}[HANDLED ERROR]{cls._RESET} {message}")
        else:
            print(f"[HANDLED ERROR] {message}")

    @classmethod
    def warning(cls, message):
        if cls._use_color():
            print(f"{cls._YELLOW}[WARNING]{cls._RESET} {message}")
        else:
            print(f"[WARNING] {message}")

    @classmethod
    def header(cls, message):
        if cls._use_color():
            print(f"\n{cls._BOLD}{cls._BLUE}{'='*60}")
            print(f"  {message}")
            print(f"{'='*60}{cls._RESET}\n")
        else:
            print(f"\n{'='*60}")
            print(f"  {message}")
            print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# @fail_gracefully — Resilience Decorator
# ---------------------------------------------------------------------------

def fail_gracefully(fallback_return=None, max_retries=1, base_delay=0.5):
    """
    Decorator that wraps agent functions in try/except with:
      - Exponential backoff retries
      - Color-coded error logging
      - Graceful fallback return value

    This ensures the notebook remains stable during failure scenario
    demonstrations (§9.2 Stage 4–5, §9.3 remediation, §9.4 critic).

    Args:
        fallback_return: Value returned on exhausted retries.
        max_retries: Number of retry attempts (default 1).
        base_delay: Initial delay in seconds for exponential backoff.

    Returns:
        Decorated function with resilience wrapper.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt)
                        ColorLog.warning(
                            f"{func.__name__}: Attempt {attempt + 1} failed "
                            f"({type(e).__name__}: {e}). "
                            f"Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                    else:
                        ColorLog.error(
                            f"{func.__name__}: All {max_retries + 1} attempts "
                            f"exhausted. Error: {type(last_exception).__name__}: "
                            f"{last_exception}"
                        )
            # Return fallback if all retries exhausted
            if callable(fallback_return):
                return fallback_return()
            return fallback_return
        return wrapper
    return decorator
