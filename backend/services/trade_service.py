from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.trade import Trade
from backend.schemas.trade import TradeCreate
from backend.services.alert_service import create_alert
from backend.services.risk_service import estimate_trade_risk, validate_trade_limits


async def create_trade(session: AsyncSession, payload: TradeCreate) -> Trade:
    risk = await validate_trade_limits(session=session, entry_price=payload.entry_price, quantity=payload.quantity, exit_price=payload.exit_price)
    if not risk.passed:
        await create_alert(session, symbol=payload.symbol, alert_type="risk", message="; ".join(risk.violations))

    pnl = 0.0
    if payload.exit_price is not None:
        pnl = (payload.exit_price - payload.entry_price) * payload.quantity

    trade_risk = estimate_trade_risk(payload.entry_price, payload.quantity, payload.exit_price)
    r_multiple = (pnl / trade_risk) if trade_risk else 0.0

    trade = Trade(
        symbol=payload.symbol,
        instrument_type=payload.instrument_type,
        entry_price=payload.entry_price,
        exit_price=payload.exit_price,
        quantity=payload.quantity,
        entry_time=payload.entry_time,
        exit_time=payload.exit_time,
        strategy=payload.strategy,
        pnl=pnl,
        r_multiple=r_multiple,
        notes=payload.notes,
    )
    session.add(trade)
    await session.commit()
    await session.refresh(trade)
    return trade


async def list_trades(session: AsyncSession, limit: int = 200) -> list[Trade]:
    stmt = select(Trade).order_by(Trade.entry_time.desc()).limit(limit)
    return list((await session.execute(stmt)).scalars().all())
