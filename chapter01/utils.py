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
    banner = "=" * 60
    print(f"\n{GREEN}{BOLD}{banner}")
    print("   LIVE MODE ACTIVE")
    print("   Connected to OpenAI API.")
    print(f"{banner}{RESET}\n")


# ============================================================
# API Key Detection — Three-Tier Cascade
# Ref: Strategy §2.3 — API Key Detection Flow
# Flow: .env (dotenv) → os.getenv → getpass → SIMULATION
# ============================================================

def detect_api_key():
    """Detect an OpenAI API key using a three-tier fallback cascade.

    Tier 1: Load from .env file via python-dotenv.
    Tier 2: Check os.getenv("OPENAI_API_KEY").
    Tier 3: Prompt via getpass (interactive environments only).
    Fallback: Return (None, "SIMULATION") if all tiers fail.

    Returns:
        tuple: (api_key_or_None, mode_string)
            mode_string is either "LIVE" or "SIMULATION".

    Author: Imran Ahmad
    """
    # Tier 1: Attempt to load from .env via python-dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
        log_info("Loaded .env file via python-dotenv.")
    except ImportError:
        log_warning("python-dotenv not installed. Skipping .env file loading.")
    except Exception:
        log_warning("Could not load .env file. Continuing with fallback detection.")

    # Tier 2: Check environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.strip():
        # Skip placeholder values from .env templates
        if "your-key" in api_key or "your_key" in api_key:
            log_warning("Placeholder API key detected. Skipping.")
        else:
            log_info("API key detected from environment variable.")
            return api_key.strip(), "LIVE"

    # Tier 3: Interactive prompt via getpass (only in interactive terminals)
    if sys.stdin and sys.stdin.isatty():
        try:
            import getpass
            api_key = getpass.getpass(
                "Enter your OpenAI API key (or press Enter for Simulation Mode): "
            )
            if api_key and api_key.strip():
                log_info("API key provided via interactive prompt.")
                return api_key.strip(), "LIVE"
        except (EOFError, OSError):
            pass

    # Fallback: Simulation Mode
    log_info("No API key detected. Activating Simulation Mode.")
    return None, "SIMULATION"


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
