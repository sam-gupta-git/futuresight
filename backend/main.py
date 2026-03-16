from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import init_models
from backend.routes.alerts import router as alerts_router
from backend.routes.analytics import router as analytics_router
from backend.routes.news import router as news_router
from backend.routes.trades import router as trades_router
from backend.routes.market_quotes import router as market_quotes_router
from backend.routes.watchlist import router as watchlist_router

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await init_models()
    yield


app = FastAPI(title="FutureSight API", version="1.0.0", lifespan=lifespan)
app.include_router(watchlist_router)
app.include_router(alerts_router)
app.include_router(trades_router)
app.include_router(analytics_router)
app.include_router(news_router)
app.include_router(market_quotes_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
