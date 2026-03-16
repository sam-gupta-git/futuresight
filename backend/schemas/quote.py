from pydantic import BaseModel


class QuoteData(BaseModel):
    symbol: str
    price: float
    change_pct: float
    sparkline: list[float]  # last 7 daily closes
