"""
resilience.py — Fail-Gracefully Architecture for Chapter 17
Book: AI Agents by Imran Ahmad (Packt, 2025)
Chapter: 17 — Epilogue: The Future of Intelligent Agents

Provides:
  - ColorLogger: ANSI color-coded logging (Blue=INFO, Green=SUCCESS, Red=ERROR)
  - @fail_gracefully: Defensive decorator that catches exceptions and returns fallbacks
  - detect_api_mode(): Environment detection for Simulation vs. Live mode
"""

import os
import functools


class ColorLogger:
    """
    Visual logging with ANSI color codes for clear notebook output.
    Author: Imran Ahmad
    """
    BLUE  = "\033[94m"
    GREEN = "\033[92m"
    RED   = "\033[91m"
    BOLD  = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def info(msg):
        print(f"{ColorLogger.BLUE}[INFO]{ColorLogger.RESET} {msg}")

    @staticmethod
    def success(msg):
        print(f"{ColorLogger.GREEN}[SUCCESS]{ColorLogger.RESET} {msg}")

    @staticmethod
    def error(msg):
        print(f"{ColorLogger.RED}[HANDLED ERROR]{ColorLogger.RESET} {msg}")

    @staticmethod
    def simulation(msg):
        print(f"{ColorLogger.BOLD}[SIMULATION MODE]{ColorLogger.RESET} {msg}")

    @staticmethod
    def section(title):
        print(f"\n{'='*60}")
        print(f"{ColorLogger.BOLD}{title}{ColorLogger.RESET}")
        print(f"{'='*60}\n")


def fail_gracefully(fallback_return=None, context="Unknown"):
    """
    Wraps any function in defensive try/except logic.
    On exception: logs RED error, returns fallback, NEVER terminates execution.

    Args:
        fallback_return: Value to return on failure (or callable producing one).
        context: Human-readable label for log messages (e.g., "Architecture Search").
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                ColorLogger.error(
                    f"{context} — {type(e).__name__}: {e}. "
                    f"Falling back to mock/default result."
                )
                if callable(fallback_return):
                    return fallback_return()
                return fallback_return
        return wrapper
    return decorator


def detect_api_mode():
    """
    Detects whether a valid API key is available.
    Returns: tuple of (mode_string, api_key_or_None)

    Priority:
      1. OPENAI_API_KEY from environment / .env
      2. ANTHROPIC_API_KEY from environment / .env
      3. Fallback to Simulation Mode
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        ColorLogger.info("python-dotenv not installed. Checking env vars directly.")
    except Exception:
        ColorLogger.info("dotenv load failed. Checking env vars directly.")

    key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")

    if key and not key.startswith("<") and len(key) > 10:
        ColorLogger.success("Live API key detected. Running in LIVE MODE.")
        return "live", key
    else:
        ColorLogger.simulation(
            "No valid API key found. All outputs are synthetic. "
            "See .env.template to enable live mode."
        )
        return "simulation", None
