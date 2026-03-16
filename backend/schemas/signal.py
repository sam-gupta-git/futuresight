from datetime import datetime

from pydantic import BaseModel, Field


class SignalCreate(BaseModel):
    symbol: str
    signal_type: str
    price: float
    confidence: float = Field(ge=0, le=1)


class SignalRead(SignalCreate):
    id: str
    created_at: datetime
