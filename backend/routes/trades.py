from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas.trade import TradeCreate, TradeRead
from backend.services.trade_service import create_trade, list_trades

router = APIRouter(tags=["trades"])


@router.post("/trade", response_model=TradeRead, status_code=status.HTTP_201_CREATED)
async def post_trade(payload: TradeCreate, session: AsyncSession = Depends(get_db)) -> TradeRead:
    trade = await create_trade(session, payload)
    return TradeRead(
        id=str(trade.id), symbol=trade.symbol, instrument_type=trade.instrument_type,
        entry_price=trade.entry_price, exit_price=trade.exit_price, quantity=trade.quantity,
        entry_time=trade.entry_time, exit_time=trade.exit_time, strategy=trade.strategy,
        pnl=trade.pnl, r_multiple=trade.r_multiple, notes=trade.notes,
    )


@router.get("/trades", response_model=list[TradeRead])
async def get_trades(session: AsyncSession = Depends(get_db)) -> list[TradeRead]:
    rows = await list_trades(session)
    return [
        TradeRead(
            id=str(t.id), symbol=t.symbol, instrument_type=t.instrument_type,
            entry_price=t.entry_price, exit_price=t.exit_price, quantity=t.quantity,
            entry_time=t.entry_time, exit_time=t.exit_time, strategy=t.strategy,
            pnl=t.pnl, r_multiple=t.r_multiple, notes=t.notes,
        )
        for t in rows
    ]
