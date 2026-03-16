from datetime import datetime

from pydantic import BaseModel


class TradeCreate(BaseModel):
    symbol: str
    instrument_type: str
    entry_price: float
    exit_price: float | None = None
    quantity: int
    entry_time: datetime
    exit_time: datetime | None = None
    strategy: str
    notes: str = ""


class TradeRead(BaseModel):
    id: str
    symbol: str
    instrument_type: str
    entry_price: float
    exit_price: float | None
    quantity: int
    entry_time: datetime
    exit_time: datetime | None
    strategy: str
    pnl: float
    r_multiple: float
    notes: str
