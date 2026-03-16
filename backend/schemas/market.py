from datetime import datetime

from pydantic import BaseModel


class MarketPriceRead(BaseModel):
    symbol: str
    price: float
    volume: float
    timestamp: datetime


class AnalyticsRead(BaseModel):
    metric: str
    value: float
    timestamp: datetime
