import asyncio
import time
from datetime import datetime, timezone

import httpx

from backend.config import settings
from backend.schemas.news import NewsItem

# In-memory cache: key -> (articles, expiry_timestamp)
_cache: dict[str, tuple[list[NewsItem], float]] = {}
_CACHE_TTL = 120.0


async def fetch_news(symbols: list[str], topics: list[str]) -> list[NewsItem]:
    cache_key = "|".join(sorted(symbols)) + "||" + "|".join(sorted(topics))
    cached = _cache.get(cache_key)
    if cached and time.monotonic() < cached[1]:
        return cached[0]

    if not settings.massive_api_key:
        articles = _mock_news(symbols)
    else:
        articles = await _fetch_from_massive(symbols)

    if topics:
        lower_topics = [t.lower() for t in topics]
        articles = [
            a for a in articles
            if any(kw in a.title.lower() or kw in a.summary.lower() for kw in lower_topics)
        ]

    _cache[cache_key] = (articles, time.monotonic() + _CACHE_TTL)
    return articles


async def _fetch_from_massive(symbols: list[str]) -> list[NewsItem]:
    async def fetch_one(symbol: str) -> list[NewsItem]:
        url = (
            f"https://api.massive.com/v2/reference/news"
            f"?ticker={symbol}&limit=10&apiKey={settings.massive_api_key}"
        )
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            results = response.json().get("results", [])

        items = []
        for r in results:
            items.append(NewsItem(
                title=r.get("title", ""),
                source=r.get("author", "Unknown"),
                summary=r.get("description", ""),
                url=r.get("article_url", ""),
                published_at=datetime.fromisoformat(r["published_utc"].replace("Z", "+00:00")),
                symbols=r.get("tickers", []),
            ))
        return items

    nested = await asyncio.gather(*[fetch_one(s) for s in symbols], return_exceptions=True)
    seen: set[str] = set()
    articles: list[NewsItem] = []
    for batch in nested:
        if isinstance(batch, Exception):
            continue
        for item in batch:
            if item.url not in seen:
                seen.add(item.url)
                articles.append(item)
    articles.sort(key=lambda a: a.published_at, reverse=True)
    return articles


def _mock_news(symbols: list[str]) -> list[NewsItem]:
    now = datetime.now(timezone.utc)
    sym = symbols[0] if symbols else "AAPL"
    return [
        NewsItem(
            title=f"{sym} Surges on Strong Earnings Beat",
            source="Market Watch",
            summary=f"{sym} reported quarterly earnings well above analyst expectations, driven by robust demand across all segments. The stock climbed sharply in pre-market trading.",
            url=f"https://example.com/news/{sym.lower()}-earnings",
            published_at=now,
            symbols=[sym],
        ),
        NewsItem(
            title="Options Volume Spikes Ahead of Fed Decision",
            source="Reuters",
            summary="Options traders are positioning aggressively ahead of the Federal Reserve's interest rate decision, with implied volatility rising across major indices including SPY and QQQ.",
            url="https://example.com/news/options-fed",
            published_at=now,
            symbols=["SPY", "QQQ"],
        ),
        NewsItem(
            title="Futures Markets Signal Cautious Optimism",
            source="Bloomberg",
            summary="ES and NQ futures pointed higher overnight as global markets digested softer-than-expected inflation data from Europe, supporting risk appetite heading into the US open.",
            url="https://example.com/news/futures-overnight",
            published_at=now,
            symbols=["ESM6", "NQM6"],
        ),
        NewsItem(
            title="NVDA Breaks Out to New All-Time High",
            source="Barron's",
            summary="NVIDIA shares broke through resistance on record volume following an analyst upgrade citing AI data center demand as a multi-year tailwind for the chipmaker.",
            url="https://example.com/news/nvda-breakout",
            published_at=now,
            symbols=["NVDA"],
        ),
        NewsItem(
            title="Volatility Index Climbs as Macro Risks Mount",
            source="CNBC",
            summary="The VIX rose sharply as traders grew cautious about geopolitical developments and upcoming economic data releases, prompting a rotation into defensive equities.",
            url="https://example.com/news/vix-macro",
            published_at=now,
            symbols=["SPY", "AAPL", "MSFT"],
        ),
    ]
