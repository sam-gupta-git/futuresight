from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas.market import AnalyticsRead
from backend.services.analytics_service import list_analytics

router = APIRouter(tags=["analytics"])


@router.get("/analytics", response_model=list[AnalyticsRead])
async def get_analytics(session: AsyncSession = Depends(get_db)) -> list[AnalyticsRead]:
    rows = await list_analytics(session)
    return [AnalyticsRead(metric=r.metric, value=r.value, timestamp=r.timestamp) for r in rows]
