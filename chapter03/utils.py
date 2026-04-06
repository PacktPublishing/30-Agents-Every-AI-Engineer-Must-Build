"""
Utility module for Chapter 3: The Art of Agent Prompting
Book: Agents by Imran Ahmad (Packt Publishing, 2026)
Author: Imran Ahmad

Provides:
    - ColorLogger: ANSI-colored logging for notebook visual feedback
    - graceful_fallback: Decorator for fail-gracefully LLM call handling
    - get_api_key: Secure API key detection with dotenv + getpass fallback
"""

import os
import getpass
import functools
from dotenv import load_dotenv


class ColorLogger:
    """
    Color-coded logger for notebook visual feedback.

    Blue  [INFO]           — Operation starting
    Green [SUCCESS]        — Operation completed successfully
    Red   [HANDLED ERROR]  — Error caught and handled gracefully

    Author: Imran Ahmad
    """

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def __init__(self, context: str = "Agent"):
        self.context = context

    def info(self, message: str) -> None:
        print(
            f"{self.BLUE}{self.BOLD}[INFO]{self.RESET}"
            f"{self.BLUE}           [{self.context}] {message}{self.RESET}"
        )

    def success(self, message: str) -> None:
        print(
            f"{self.GREEN}{self.BOLD}[SUCCESS]{self.RESET}"
            f"{self.GREEN}        [{self.context}] {message}{self.RESET}"
        )

    def error(self, message: str) -> None:
        print(
            f"{self.RED}{self.BOLD}[HANDLED ERROR]{self.RESET}"
            f"{self.RED}  [{self.context}] {message}{self.RESET}"
        )


def graceful_fallback(section_ref: str, fallback_value=None):
    """
    Decorator that wraps any LLM call or tool invocation in defensive logic.

    - Logs execution start (Blue) and completion (Green)
    - On exception: logs error (Red) and returns fallback instead of crashing
    - NEVER re-raises. NEVER terminates notebook execution.

    Args:
        section_ref: Chapter section reference (e.g., "Section 3.6 - ToT")
        fallback_value: Optional value to return on failure

    Author: Imran Ahmad
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = ColorLogger(context="Resilience")
            logger.info(f"Executing: {func.__name__} [{section_ref}]")
            try:
                result = func(*args, **kwargs)
                logger.success(f"Completed: {func.__name__}")
                return result
            except Exception as e:
                error_type = type(e).__name__
                logger.error(
                    f"HANDLED ERROR in {func.__name__} [{section_ref}]: "
                    f"{error_type}: {e}. Returning graceful fallback."
                )
                if fallback_value is not None:
                    return fallback_value
                return {
                    "status": "fallback",
                    "section": section_ref,
                    "error": str(e),
                    "message": (
                        f"[Simulation Mode] {func.__name__} encountered an error "
                        f"and returned a safe fallback. See log above for details."
                    ),
                }

        return wrapper

    return decorator


def get_api_key() -> str | None:
    """
    Secure API key retrieval chain: .env → getpass → None.

    1. Loads .env file via python-dotenv
    2. Checks OPENAI_API_KEY environment variable
    3. Validates key is non-empty and not the placeholder
    4. Falls back to interactive getpass input
    5. Returns None if no valid key found (triggers Simulation Mode)

    Author: Imran Ahmad
    """
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY")

    if key and key.strip() and "your-key" not in key and "your_key" not in key:
        return key.strip()

    try:
        key = getpass.getpass(
            "Enter your OpenAI API key (or press Enter for Simulation Mode): "
        )
        if key and key.strip():
            return key.strip()
    except (EOFError, OSError, Exception):
        # Catches StdinNotImplementedError in non-interactive Jupyter contexts,
        # EOFError in piped stdin, and OSError in other edge cases.
        pass

    return None
