from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.signal import Signal


async def create_signal(session: AsyncSession, symbol: str, signal_type: str, price: float, confidence: float) -> Signal:
    signal = Signal(
        symbol=symbol,
        signal_type=signal_type,
        price=price,
        confidence=confidence,
        created_at=datetime.now(timezone.utc),
    )
    session.add(signal)
    await session.commit()
    await session.refresh(signal)
    return signal


async def list_signals(session: AsyncSession, limit: int = 200) -> list[Signal]:
    stmt = select(Signal).order_by(Signal.created_at.desc()).limit(limit)
    return list((await session.execute(stmt)).scalars().all())
