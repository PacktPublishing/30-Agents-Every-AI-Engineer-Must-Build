"""
Chapter 05 — Foundational Cognitive Architectures
Book: 30 Agents Every AI Engineer Must Build
Author: Imran Ahmad
Publisher: Packt Publishing

Resilience utilities: the @fail_gracefully decorator wraps agent
tool calls in defensive error handling with exponential-backoff
retries and fallback values.

Ref: Engineering Best Practices — Robustness (p. 32)
"Design your systems with clear fallbacks and escalation paths
for undecidable or unsafe conditions."
"""

import functools
import time

from color_logger import log_error, log_success, log_warn


def fail_gracefully(
    fallback_value=None,
    max_retries: int = 1,
    chapter_ref: str = "",
):
    """Decorator that ensures agent tool calls never crash the system.

    Wraps the decorated function in try/except, retries on failure
    with exponential backoff (2^attempt seconds), and returns a
    fallback value if all attempts fail. Execution always continues.

    Args:
        fallback_value: Value returned when all retries are exhausted.
        max_retries: Number of retry attempts (default 1, meaning
            up to 2 total executions: initial + 1 retry).
        chapter_ref: Book reference string for log traceability
            (e.g., "Section 5.1, p. 14").

    Returns:
        Decorated function that never raises exceptions.

    Chapter Reference:
        Engineering Best Practices — Robustness (p. 32)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ref_tag = f" (ref: {chapter_ref})" if chapter_ref else ""
            attempts = max_retries + 1  # initial attempt + retries

            for attempt in range(attempts):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        log_success(
                            f"{func.__name__} succeeded on retry "
                            f"{attempt}{ref_tag}"
                        )
                    return result
                except Exception as exc:
                    remaining = attempts - attempt - 1
                    log_error(
                        f"{func.__name__} failed: {exc}{ref_tag}"
                    )

                    if remaining > 0:
                        wait = 2 ** attempt
                        log_warn(
                            f"Retrying {func.__name__} in {wait}s "
                            f"({remaining} retries left){ref_tag}"
                        )
                        time.sleep(wait)
                    else:
                        log_error(
                            f"All retries exhausted for "
                            f"{func.__name__}. Returning fallback "
                            f"value: {fallback_value!r}{ref_tag}"
                        )
                        return fallback_value

            return fallback_value  # safety net (should not reach here)

        return wrapper

    return decorator
