import asyncio
from datetime import datetime, timezone

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.models.signal import Signal


async def fetch_equity_snapshot(symbol: str) -> dict[str, float | str]:
    if not settings.polygon_api_key:
        return _mock_equity_snapshot(symbol)

    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/{symbol}?apiKey={settings.polygon_api_key}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        payload = response.json().get("ticker", {})

    day = payload.get("day", {})
    prev_day = payload.get("prevDay", {})
    last_trade = payload.get("lastTrade", {})

    price = _to_float(last_trade.get("p", day.get("c", 0.0)))
    volume = _to_float(day.get("v", 0.0))
    avg_volume = max(_to_float(prev_day.get("v", 1.0)), 1.0)
    prev_close = _to_float(prev_day.get("c", 0.0))
    gap_percent = ((price - prev_close) / prev_close * 100.0) if prev_close else 0.0

    return {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "avg_volume": avg_volume,
        "gap_percent": gap_percent,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


async def fetch_options_snapshot(symbol: str) -> dict[str, float | str]:
    if not (settings.ibkr_api_key and settings.ibkr_base_url):
        return _mock_options_snapshot(symbol)

    url = f"{settings.ibkr_base_url}/marketdata/options/{symbol}"
    headers = {"Authorization": f"Bearer {settings.ibkr_api_key}"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        payload = response.json()

    return {
        "symbol": symbol,
        "price": _to_float(payload.get("underlying_price", 0.0)),
        "iv_percentile": _to_float(payload.get("iv_percentile", 0.0)),
        "options_volume": _to_float(payload.get("options_volume", 0.0)),
        "avg_options_volume": max(_to_float(payload.get("avg_options_volume", 1.0)), 1.0),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


async def fetch_futures_snapshot(contract: str) -> dict[str, float | str]:
    if not (settings.ibkr_api_key and settings.ibkr_base_url):
        return _mock_futures_snapshot(contract)

    url = f"{settings.ibkr_base_url}/marketdata/futures/{contract}"
    headers = {"Authorization": f"Bearer {settings.ibkr_api_key}"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        payload = response.json()

    return {
        "contract": contract,
        "price": _to_float(payload.get("price", 0.0)),
        "overnight_high": _to_float(payload.get("overnight_high", 0.0)),
        "volume": _to_float(payload.get("volume", 0.0)),
        "avg_volume": max(_to_float(payload.get("avg_volume", 1.0)), 1.0),
        "atr": _to_float(payload.get("atr", 0.0)),
        "atr_prev": max(_to_float(payload.get("atr_prev", 1.0)), 1.0),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


async def fetch_market_batch(
    equity_symbols: list[str],
    options_symbols: list[str],
    futures_contracts: list[str],
) -> list[dict[str, float | str]]:
    requests = [fetch_equity_snapshot(symbol) for symbol in equity_symbols]
    requests.extend(fetch_options_snapshot(symbol) for symbol in options_symbols)
    requests.extend(fetch_futures_snapshot(contract) for contract in futures_contracts)
    return list(await asyncio.gather(*requests))


async def get_watchlist_signals(session: AsyncSession, limit: int = 100) -> list[Signal]:
    stmt = select(Signal).order_by(Signal.created_at.desc()).limit(limit)
    rows = (await session.execute(stmt)).scalars().all()
    return list(rows)


def _to_float(value: float | int | str | None) -> float:
    try:
        return float(value) if value is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def _mock_equity_snapshot(symbol: str) -> dict[str, float | str]:
    return {
        "symbol": symbol,
        "price": 112.4,
        "volume": 2_000_000,
        "avg_volume": 550_000,
        "gap_percent": 4.2,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _mock_options_snapshot(symbol: str) -> dict[str, float | str]:
    return {
        "symbol": symbol,
        "price": 504.2,
        "iv_percentile": 76.0,
        "options_volume": 300_000.0,
        "avg_options_volume": 45_000.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _mock_futures_snapshot(contract: str) -> dict[str, float | str]:
    return {
        "contract": contract,
        "price": 5432.0,
        "overnight_high": 5418.0,
        "volume": 180_000.0,
        "avg_volume": 72_000.0,
        "atr": 58.0,
        "atr_prev": 42.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
