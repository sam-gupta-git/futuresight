from fastapi import APIRouter, Query

from backend.schemas.quote import QuoteData
from backend.services.quote_service import fetch_quotes

router = APIRouter(tags=["market"])


@router.get("/market/quotes", response_model=list[QuoteData])
async def get_market_quotes(
    symbols: str = Query(default=""),
) -> list[QuoteData]:
    sym_list = [s.strip() for s in symbols.split(",") if s.strip()] if symbols else []
    return await fetch_quotes(sym_list)
