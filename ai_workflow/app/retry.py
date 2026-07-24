from __future__ import annotations

import asyncio
import re
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


class RetryExhaustedError(RuntimeError):
    def __init__(self, status_code: int, attempts: int) -> None:
        self.status_code = status_code
        self.attempts = attempts
        super().__init__(
            f"The Gemini service is temporarily unavailable (HTTP {status_code}) after "
            f"{attempts} attempts. Please wait and try again, or run the offline demo."
        )


def extract_status_code(error: BaseException) -> int | None:
    for attribute in ("status_code", "code"):
        value = getattr(error, attribute, None)
        if isinstance(value, int):
            return value
    match = re.search(r"\b(429|503)\b", str(error))
    return int(match.group(1)) if match else None


async def retry_async(
    operation: Callable[[], Awaitable[T]],
    *,
    attempts: int = 3,
    initial_delay: float = 1.0,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> T:
    """Retry only temporary Gemini capacity errors with exponential backoff."""

    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for attempt in range(1, attempts + 1):
        try:
            return await operation()
        except Exception as error:
            status_code = extract_status_code(error)
            if status_code not in {429, 503}:
                raise
            if attempt == attempts:
                raise RetryExhaustedError(status_code, attempts) from None
            await sleep(initial_delay * (2 ** (attempt - 1)))

    raise RuntimeError("unreachable")
