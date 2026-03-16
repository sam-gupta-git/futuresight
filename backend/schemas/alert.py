from datetime import datetime

from pydantic import BaseModel


class AlertRead(BaseModel):
    id: str
    symbol: str
    alert_type: str
    message: str
    timestamp: datetime
