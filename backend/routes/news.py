from fastapi import APIRouter, Query

from backend.config import settings
from backend.schemas.news import NewsItem
from backend.services.news_service import fetch_news

router = APIRouter(tags=["news"])


@router.get("/news", response_model=list[NewsItem])
async def get_news(
    symbols: str = Query(default=""),
    topics: str = Query(default=""),
) -> list[NewsItem]:
    sym_list = [s.strip() for s in symbols.split(",") if s.strip()] if symbols else []
    topic_list = [t.strip() for t in topics.split(",") if t.strip()] if topics else []

    if not sym_list:
        sym_list = [s.strip() for s in settings.scanner_equity_symbols.split(",") if s.strip()]

    return await fetch_news(sym_list, topic_list)
