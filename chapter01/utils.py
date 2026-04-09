"""
Utility functions for Chapter 1: Foundations of Agent Engineering.
Book: "AI Agents" by Imran Ahmad (Packt, 2026)

Provides:
    - ANSI color-coded logging (log_info, log_success, log_error, log_warning)
    - Mode banners (simulation_mode_banner, live_mode_banner)
    - Three-tier API key detection (detect_api_key)
    - Resilience decorator (@graceful_fallback)
"""

import os
import sys
import functools

# ============================================================
# ANSI Color Constants
# Ref: Strategy §3.2 — Visual Logging Schema
# ============================================================

BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ============================================================
# Color-Coded Logging Functions
# ============================================================

def log_info(message):
    """Print a blue [INFO] message. Used before any agent operation.

    Author: Imran Ahmad
    """
    print(f"{BLUE}[INFO]{RESET} {message}")


def log_success(message):
    """Print a green bold [SUCCESS] message. Used after successful operations.

    Author: Imran Ahmad
    """
    print(f"{GREEN}{BOLD}[SUCCESS]{RESET} {message}")


def log_error(message):
    """Print a red bold [HANDLED ERROR] message. Used when exceptions are caught.

    Author: Imran Ahmad
    """
    print(f"{RED}{BOLD}[HANDLED ERROR]{RESET} {message}")


def log_warning(message):
    """Print a yellow [WARNING] message. Used for non-critical issues.

    Author: Imran Ahmad
    """
    print(f"{YELLOW}[WARNING]{RESET} {message}")


# ============================================================
# Mode Banners
# Ref: Strategy §3.2 — 60-char banners
# ============================================================

def simulation_mode_banner():
    """Display a yellow banner announcing Simulation Mode.

    Author: Imran Ahmad
    """
    banner = "=" * 60
    print(f"\n{YELLOW}{BOLD}{banner}")
    print("   SIMULATION MODE ACTIVE")
    print("   Using MockLLM with chapter-derived responses.")
    print("   No API key required.")
    print(f"{banner}{RESET}\n")


def live_mode_banner():
    """Display a green banner announcing Live API Mode.

    Author: Imran Ahmad
    """
    provider = get_provider()
    provider_label = {
        "openai": "OpenAI API",
        "anthropic": "Anthropic API (Claude)",
        "google": "Google Gemini API",
    }.get(provider, "API")
    banner = "=" * 60
    print(f"\n{GREEN}{BOLD}{banner}")
    print(f"   LIVE MODE ACTIVE")
    print(f"   Connected to {provider_label}.")
    print(f"{banner}{RESET}\n")


# ============================================================
# API Key Detection — Three-Tier Cascade
# Ref: Strategy §2.3 — API Key Detection Flow
# Flow: .env (dotenv) → os.getenv → getpass → SIMULATION
# ============================================================

_LLM_PROVIDER = None


def detect_api_key():
    """Detect an API key using a multi-provider fallback cascade.

    Supports OpenAI, Anthropic, and Google Gemini. The provider is selected
    by LLM_PROVIDER env var, or auto-detected from available keys.

    Tier 1: Load from .env file via python-dotenv.
    Tier 2: Multi-provider detection (OpenAI → Anthropic → Google).
    Tier 3: Prompt via getpass (interactive environments only).
    Fallback: Return (None, "SIMULATION") if all tiers fail.

    Returns:
        tuple: (api_key_or_None, mode_string)
            mode_string is either "LIVE" or "SIMULATION".

    Author: Imran Ahmad
    """
    global _LLM_PROVIDER

    # Tier 1: Attempt to load from .env via python-dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
        log_info("Loaded .env file via python-dotenv.")
    except ImportError:
        log_warning("python-dotenv not installed. Skipping .env file loading.")
    except Exception:
        log_warning("Could not load .env file. Continuing with fallback detection.")

    # Tier 2: Multi-provider detection via shared utility
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from supporting.llm_provider import detect_provider
        provider, key, mode = detect_provider()
        _LLM_PROVIDER = provider
        if mode == "LIVE":
            log_info(f"API key detected — provider: {provider}")
            return key, "LIVE"
    except ImportError:
        pass  # Fall through to legacy detection

    # Legacy: Check OPENAI_API_KEY environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.strip():
        if "your-key" in api_key or "your_key" in api_key:
            log_warning("Placeholder API key detected. Skipping.")
        else:
            log_info("API key detected from environment variable.")
            _LLM_PROVIDER = "openai"
            return api_key.strip(), "LIVE"

    # Tier 3: Interactive prompt via getpass (only in interactive terminals)
    if sys.stdin and sys.stdin.isatty():
        try:
            import getpass
            api_key = getpass.getpass(
                "Enter API key (OpenAI/Anthropic/Google) or press Enter for Simulation: "
            )
            if api_key and api_key.strip():
                log_info("API key provided via interactive prompt.")
                _LLM_PROVIDER = "openai"  # default assumption
                return api_key.strip(), "LIVE"
        except (EOFError, OSError):
            pass

    # Fallback: Simulation Mode
    log_info("No API key detected. Activating Simulation Mode.")
    _LLM_PROVIDER = "simulation"
    return None, "SIMULATION"


def get_provider():
    """Return the detected LLM provider name.

    Returns:
        str: "openai", "anthropic", "google", or "simulation"
    """
    global _LLM_PROVIDER
    return _LLM_PROVIDER or "simulation"


def get_client(api_key=None):
    """Return a raw API client for the detected provider.

    For direct API usage (not LangChain). Falls back to OpenAI.

    Args:
        api_key: API key override.

    Returns:
        Provider-specific client object.
    """
    provider = get_provider()
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from supporting.llm_provider import get_client as _get_client
        return _get_client(provider=provider, api_key=api_key)
    except ImportError:
        from openai import OpenAI
        return OpenAI(api_key=api_key)


def chat_completion(client, messages, model=None, temperature=0):
    """Send a chat completion and return the response text.

    Normalizes response format across OpenAI, Anthropic, and Google.

    Args:
        client: Provider client from get_client().
        messages: List of {"role": ..., "content": ...} dicts.
        model: Model name override.
        temperature: Model temperature.

    Returns:
        str: The assistant's response text.
    """
    provider = get_provider()
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from supporting.llm_provider import chat_completion as _chat_completion
        return _chat_completion(client, provider, messages, model=model, temperature=temperature)
    except ImportError:
        # Fallback: assume OpenAI
        response = client.chat.completions.create(
            model=model or "gpt-4o",
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content


# ============================================================
# @graceful_fallback Decorator
# Ref: Strategy §5 — Resilience Contract
# ============================================================

def graceful_fallback(fallback_value, section_ref=""):
    """Decorator factory that wraps a function in try-except resilience.

    On success:
        1. Logs [INFO] before execution.
        2. Logs [SUCCESS] after execution.
        3. Returns the function's actual result.

    On exception:
        1. Logs [INFO] before execution.
        2. Logs [HANDLED ERROR] with the exception details and section reference.
        3. Returns the fallback_value instead of raising.

    Args:
        fallback_value: The value to return when the wrapped function raises.
        section_ref (str): Chapter section reference for error traceability
            (e.g., "§1.2.1 Perception").

    Returns:
        Decorator that wraps the target function.

    Author: Imran Ahmad
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            log_info(f"Executing {func_name}() — {section_ref}")
            try:
                result = func(*args, **kwargs)
                log_success(f"{func_name}() completed successfully.")
                return result
            except Exception as e:
                log_error(
                    f"{func_name}() failed: {type(e).__name__}: {e}. "
                    f"Falling back to default for {section_ref}."
                )
                return fallback_value
        return wrapper
    return decorator
