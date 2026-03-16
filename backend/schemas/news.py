from datetime import datetime

from pydantic import BaseModel


class NewsItem(BaseModel):
    title: str
    source: str
    summary: str
    url: str
    published_at: datetime
    symbols: list[str]
