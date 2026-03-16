from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.analytics import Analytics
from backend.models.trade import Trade


async def compute_and_store_metrics(session: AsyncSession) -> list[Analytics]:
    total_pnl = float((await session.execute(select(func.coalesce(func.sum(Trade.pnl), 0.0)))).scalar_one())
    wins = int((await session.execute(select(func.count(Trade.id)).where(Trade.pnl > 0))).scalar_one())
    losses = int((await session.execute(select(func.count(Trade.id)).where(Trade.pnl < 0))).scalar_one())
    total = wins + losses
    win_rate = (wins / total * 100.0) if total else 0.0

    gross_profit = float((await session.execute(select(func.coalesce(func.sum(Trade.pnl), 0.0)).where(Trade.pnl > 0))).scalar_one())
    gross_loss = abs(float((await session.execute(select(func.coalesce(func.sum(Trade.pnl), 0.0)).where(Trade.pnl < 0))).scalar_one()))
    profit_factor = (gross_profit / gross_loss) if gross_loss else 0.0

    now = datetime.now(timezone.utc)
    rows = [
        Analytics(metric="cumulative_pnl", value=total_pnl, timestamp=now),
        Analytics(metric="win_rate", value=win_rate, timestamp=now),
        Analytics(metric="profit_factor", value=profit_factor, timestamp=now),
    ]
    session.add_all(rows)
    await session.commit()
    return rows


async def list_analytics(session: AsyncSession, limit: int = 100) -> list[Analytics]:
    stmt = select(Analytics).order_by(Analytics.timestamp.desc()).limit(limit)
    return list((await session.execute(stmt)).scalars().all())
