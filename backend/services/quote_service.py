import asyncio
import random
import time
from datetime import datetime, timedelta, timezone

import httpx

from backend.config import settings
from backend.schemas.quote import QuoteData

# In-memory cache: key -> (quotes, expiry_timestamp)
_cache: dict[str, tuple[list[QuoteData], float]] = {}
_CACHE_TTL = 120.0


async def fetch_quotes(symbols: list[str]) -> list[QuoteData]:
    if not symbols:
        return []

    cache_key = "|".join(sorted(symbols))
    cached = _cache.get(cache_key)
    if cached and time.monotonic() < cached[1]:
        return cached[0]

    if not settings.massive_api_key:
        quotes = _mock_quotes(symbols)
    else:
        quotes = await _fetch_from_massive(symbols)

    _cache[cache_key] = (quotes, time.monotonic() + _CACHE_TTL)
    return quotes


async def _fetch_from_massive(symbols: list[str]) -> list[QuoteData]:
    today = datetime.now(timezone.utc).date()
    date_from = (today - timedelta(days=14)).strftime("%Y-%m-%d")
    date_to = today.strftime("%Y-%m-%d")

    async def fetch_one(symbol: str) -> QuoteData | None:
        url = (
            f"https://api.massive.com/v2/aggs/ticker/{symbol}"
            f"/range/1/day/{date_from}/{date_to}"
            f"?apiKey={settings.massive_api_key}"
        )
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            results = response.json().get("results", [])

        if len(results) < 2:
            return None

        closes = [r["c"] for r in results]
        sparkline = closes[-7:] if len(closes) >= 7 else closes
        price = closes[-1]
        prev = closes[-2]
        change_pct = round(((price - prev) / prev) * 100, 2)

        return QuoteData(
            symbol=symbol,
            price=round(price, 2),
            change_pct=change_pct,
            sparkline=[round(v, 2) for v in sparkline],
        )

    results = await asyncio.gather(
        *[fetch_one(s) for s in symbols], return_exceptions=True
    )
    return [r for r in results if isinstance(r, QuoteData)]


def _mock_quotes(symbols: list[str]) -> list[QuoteData]:
    mock_data: dict[str, tuple[float, float]] = {
        "NG": (2.85, 1.42),
        "CL": (78.52, -0.67),
        "BZ": (82.10, -0.43),
        "FCX": (45.23, 2.15),
        "NEM": (38.90, -1.08),
        "BHP": (58.44, 0.76),
        "AAPL": (178.50, 0.32),
        "MSFT": (415.20, -0.18),
        "NVDA": (890.30, 1.85),
        "SPY": (520.15, 0.45),
        "QQQ": (445.80, 0.62),
    }
    quotes: list[QuoteData] = []
    for sym in symbols:
        base_price, change = mock_data.get(sym, (100.0 + random.uniform(-20, 20), round(random.uniform(-3, 3), 2)))
        sparkline = [round(base_price * (1 + random.uniform(-0.02, 0.02)), 2) for _ in range(7)]
        sparkline[-1] = round(base_price, 2)
        quotes.append(QuoteData(
            symbol=sym,
            price=round(base_price, 2),
            change_pct=change,
            sparkline=sparkline,
        ))
    return quotes
