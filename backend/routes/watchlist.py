from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas.signal import SignalRead
from backend.services.market_service import get_watchlist_signals

router = APIRouter(tags=["watchlist"])


@router.get("/watchlist", response_model=list[SignalRead])
async def get_watchlist(session: AsyncSession = Depends(get_db)) -> list[SignalRead]:
    signals = await get_watchlist_signals(session)
    return [SignalRead(id=str(s.id), symbol=s.symbol, signal_type=s.signal_type, price=s.price, confidence=s.confidence, created_at=s.created_at) for s in signals]
