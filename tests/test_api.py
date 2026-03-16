import os
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_api.db"

from backend.database import Base, SessionLocal, engine
from backend.main import app
from backend.models.signal import Signal
from backend.services.signal_service import create_signal


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.mark.asyncio
async def test_get_watchlist() -> None:
    async with SessionLocal() as session:
        session.add(Signal(symbol="AAPL", signal_type="equity_gap_volume", price=120.0, confidence=0.9, created_at=datetime.now(timezone.utc)))
        await session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/watchlist")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_and_get_trade() -> None:
    payload = {
        "symbol": "AAPL",
        "instrument_type": "equity",
        "entry_price": 100.0,
        "exit_price": 103.0,
        "quantity": 10,
        "entry_time": datetime.now(timezone.utc).isoformat(),
        "exit_time": datetime.now(timezone.utc).isoformat(),
        "strategy": "breakout",
        "notes": "api test",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        post_resp = await client.post("/trade", json=payload)
        get_resp = await client.get("/trades")
    assert post_resp.status_code == 201
    assert get_resp.status_code == 200


@pytest.mark.asyncio
async def test_signal_service_creates_signal() -> None:
    async with SessionLocal() as session:
        signal = await create_signal(
            session=session,
            symbol="MSFT",
            signal_type="equity_gap_volume",
            price=420.0,
            confidence=0.88,
        )
    assert signal.symbol == "MSFT"


@pytest.mark.asyncio
async def test_get_news() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/news")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_news_with_filters() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/news?symbols=AAPL&topics=options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_market_quotes() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/market/quotes?symbols=AAPL,MSFT")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for q in data:
        assert "symbol" in q
        assert "price" in q
        assert "change_pct" in q
        assert "sparkline" in q
        assert isinstance(q["sparkline"], list)


@pytest.mark.asyncio
async def test_risk_violation_creates_alert() -> None:
    payload = {
        "symbol": "TSLA",
        "instrument_type": "equity",
        "entry_price": 100.0,
        "exit_price": None,
        "quantity": 1000,
        "entry_time": datetime.now(timezone.utc).isoformat(),
        "exit_time": None,
        "strategy": "risk-test",
        "notes": "should trigger alert",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        post_resp = await client.post("/trade", json=payload)
        alerts_resp = await client.get("/alerts")

    assert post_resp.status_code == 201
    assert alerts_resp.status_code == 200
    alerts = alerts_resp.json()
    assert any(a["alert_type"] == "risk" and a["symbol"] == "TSLA" for a in alerts)
