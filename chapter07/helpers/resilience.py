# =============================================================================
# helpers/resilience.py
# Chapter 7: Tool Manipulation and Orchestration Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026 — B34135)
# Ref: Section 7.3 — Error Handling in Tool Integration
#
# Implements the Safe Invocation Wrappers and Separation of Decision and
# Execution patterns described in Section 7.3 (pp. 13-16). Every tool
# function and agent call in the notebook is wrapped with these primitives
# to ensure the system remains stable during failure-scenario demonstrations.
# =============================================================================

import functools
import time
from typing import Any, Callable, Optional, Tuple

from helpers.color_logger import log_success, log_error, log_warning

# ---------------------------------------------------------------------------
# Primitive 1: @graceful_fallback Decorator
# ---------------------------------------------------------------------------
# Implements the "Safe Invocation Wrappers" strategy from Section 7.3.
# On success:  log_success("func_name completed. [Section 7.x]")
# On failure:  log_error("func_name failed: {e}. Falling back. [Section 7.x]")
#              then return fallback_return. Execution CONTINUES.
# ---------------------------------------------------------------------------


def graceful_fallback(
    fallback_return: Any = None,
    section: str = "",
    max_retries: int = 1,
    on_failure: Optional[Callable] = None,
):
    """Decorator that wraps a function in try/except with retry logic,
    color-coded logging, and a graceful fallback return value.

    Parameters
    ----------
    fallback_return : Any
        The value returned when all retries are exhausted. Should match
        the function's normal return type so downstream code can handle
        it safely (e.g., ``pd.DataFrame()`` for data-loading tools).
    section : str
        Chapter section reference for the log message (e.g., "7.1").
    max_retries : int
        Number of attempts before falling back. Default is 1 (no retry).
    on_failure : callable or None
        Optional callback invoked on final failure — supports the
        Failure Memory pattern from Section 7.3.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            sec_tag = f" [Section {section}]" if section else ""
            last_exception = None

            for attempt in range(1, max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    log_success(f"{func.__name__} completed.{sec_tag}")
                    return result
                except Exception as exc:
                    last_exception = exc
                    if attempt < max_retries:
                        wait = 2 ** (attempt - 1)  # Exponential backoff
                        log_warning(
                            f"{func.__name__} attempt {attempt}/{max_retries} "
                            f"failed: {exc}. Retrying in {wait}s...{sec_tag}"
                        )
                        time.sleep(wait)
                    else:
                        log_error(
                            f"{func.__name__} failed: {exc}. "
                            f"Falling back.{sec_tag}"
                        )

            # All retries exhausted — invoke failure callback if provided
            if on_failure is not None:
                try:
                    on_failure(func.__name__, last_exception)
                except Exception:
                    pass  # Failure callback must not break the flow

            return fallback_return

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Primitive 2: safe_invoke() Function
# ---------------------------------------------------------------------------
# Returns a (success, result) tuple so the orchestrator can branch on
# success/failure without catching exceptions — matching the Separation
# of Decision and Execution pattern from Section 7.1.
# ---------------------------------------------------------------------------


def safe_invoke(
    tool_func: Callable,
    args: tuple = (),
    kwargs: dict | None = None,
    tool_name: str = "",
    section: str = "",
) -> Tuple[bool, Any]:
    """Invoke a tool function safely and return a status tuple.

    Parameters
    ----------
    tool_func : callable
        The tool function to invoke.
    args : tuple
        Positional arguments for the tool function.
    kwargs : dict or None
        Keyword arguments for the tool function.
    tool_name : str
        Display name for logging (defaults to function name).
    section : str
        Chapter section reference for log messages.

    Returns
    -------
    (bool, Any)
        ``(True, result)`` on success, ``(False, None)`` on failure.
    """
    if kwargs is None:
        kwargs = {}
    name = tool_name or getattr(tool_func, "__name__", "unknown_tool")
    sec_tag = f" [Section {section}]" if section else ""

    try:
        result = tool_func(*args, **kwargs)
        log_success(f"{name} invoked successfully.{sec_tag}")
        return (True, result)
    except Exception as exc:
        log_error(f"{name} invocation failed: {exc}.{sec_tag}")
        return (False, None)
