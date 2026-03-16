import asyncio
from datetime import datetime, timedelta, timezone

from backend.database import SessionLocal
from backend.models.alert import Alert
from backend.models.analytics import Analytics
from backend.models.signal import Signal
from backend.models.trade import Trade


async def seed() -> None:
    now = datetime.now(timezone.utc)
    async with SessionLocal() as session:
        session.add_all([
            Signal(symbol="AAPL", signal_type="equity_gap_volume", price=112.4, confidence=0.82, created_at=now),
            Signal(symbol="SPY", signal_type="options_iv_volume", price=504.2, confidence=0.79, created_at=now),
            Alert(symbol="AAPL", alert_type="scanner", message="High-confidence setup", timestamp=now),
            Trade(symbol="AAPL", instrument_type="equity", entry_price=110.0, exit_price=113.2, quantity=20, entry_time=now - timedelta(hours=2), exit_time=now - timedelta(hours=1), strategy="gap-and-go", pnl=64.0, r_multiple=1.6, notes="Seed trade"),
            Analytics(metric="cumulative_pnl", value=64.0, timestamp=now),
            Analytics(metric="win_rate", value=100.0, timestamp=now),
            Analytics(metric="profit_factor", value=3.0, timestamp=now),
        ])
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
