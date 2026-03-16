from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas.alert import AlertRead
from backend.services.alert_service import list_alerts

router = APIRouter(tags=["alerts"])


@router.get("/alerts", response_model=list[AlertRead])
async def get_alerts(session: AsyncSession = Depends(get_db)) -> list[AlertRead]:
    alerts = await list_alerts(session)
    return [AlertRead(id=str(a.id), symbol=a.symbol, alert_type=a.alert_type, message=a.message, timestamp=a.timestamp) for a in alerts]
