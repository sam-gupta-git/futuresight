import asyncio

from backend.database import SessionLocal
from backend.services.analytics_service import compute_and_store_metrics


async def main() -> None:
    while True:
        try:
            async with SessionLocal() as session:
                await compute_and_store_metrics(session)
        except Exception as exc:
            print(f"analytics_worker error: {exc}")
            await asyncio.sleep(3)

        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
