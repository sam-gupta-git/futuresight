from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.trade import Trade

MAX_DAILY_LOSS = 600.0
MAX_TRADE_RISK = 300.0
MAX_POSITIONS = 5


@dataclass
class RiskResult:
    passed: bool
    violations: list[str]


def estimate_trade_risk(entry_price: float, quantity: int, exit_price: float | None) -> float:
    if exit_price is not None:
        return abs(entry_price - exit_price) * quantity
    return entry_price * quantity * 0.01


async def validate_trade_limits(session: AsyncSession, entry_price: float, quantity: int, exit_price: float | None) -> RiskResult:
    violations: list[str] = []

    trade_risk = estimate_trade_risk(entry_price, quantity, exit_price)
    if trade_risk > MAX_TRADE_RISK:
        violations.append(f"Trade risk {trade_risk:.2f} exceeds max_trade_risk={MAX_TRADE_RISK:.2f}")

    utc_now = datetime.now(timezone.utc)
    day_start = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
    daily_pnl_stmt = select(func.coalesce(func.sum(Trade.pnl), 0.0)).where(and_(Trade.entry_time >= day_start, Trade.entry_time <= utc_now))
    daily_pnl = float((await session.execute(daily_pnl_stmt)).scalar_one())
    if daily_pnl < -MAX_DAILY_LOSS:
        violations.append(f"Daily loss {daily_pnl:.2f} exceeds max_daily_loss={MAX_DAILY_LOSS:.2f}")

    open_pos_stmt = select(func.count(Trade.id)).where(Trade.exit_time.is_(None))
    open_positions = int((await session.execute(open_pos_stmt)).scalar_one())
    if open_positions >= MAX_POSITIONS:
        violations.append(f"Open positions {open_positions} exceeds max_positions={MAX_POSITIONS}")

    return RiskResult(passed=not violations, violations=violations)
