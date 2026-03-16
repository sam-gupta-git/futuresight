import asyncio
import hashlib
import json
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.database import SessionLocal
from backend.models.signal import Signal
from backend.services.market_service import fetch_market_batch
from queue.redis_client import get_redis
from queue.stream_reader import StreamReader
from queue.stream_writer import StreamWriter
from scanners.equity_scanner import scan_equities
from scanners.futures_scanner import scan_futures
from scanners.options_scanner import scan_options

MARKET_STREAM = "market.ingestion"
GROUP = "scanner_group"
CONSUMER = "scanner_worker_1"
DEAD_LETTER_STREAM = "market.dead_letter"


async def fetch_market_data() -> list[dict]:
    equity_symbols = _parse_csv(settings.scanner_equity_symbols)
    options_symbols = _parse_csv(settings.scanner_options_symbols)
    futures_contracts = _parse_csv(settings.scanner_futures_contracts)
    return await fetch_market_batch(equity_symbols, options_symbols, futures_contracts)


async def write_signals_to_db(session: AsyncSession, signals: list[dict]) -> None:
    for row in signals:
        session.add(Signal(symbol=row["symbol"], signal_type=row["signal_type"], price=row["price"], confidence=row["confidence"], created_at=row["created_at"]))
    await session.commit()


async def run_all_scanners(rows: list[dict]) -> list[dict]:
    signals: list[dict] = []
    signals.extend(scan_equities([r for r in rows if "gap_percent" in r]))
    signals.extend(scan_options([r for r in rows if "iv_percentile" in r]))
    signals.extend(scan_futures([r for r in rows if "overnight_high" in r]))
    return signals


async def main() -> None:
    redis = get_redis()
    writer = StreamWriter(redis, MARKET_STREAM)
    dead_letter_writer = StreamWriter(redis, DEAD_LETTER_STREAM)
    reader = StreamReader(redis, MARKET_STREAM, GROUP, CONSUMER)
    await reader.ensure_group()
    seen_ids: dict[str, float] = {}
    backoff_seconds = 1

    while True:
        try:
            prices = await fetch_market_data()
            for payload in prices:
                await writer.write(payload)

            consumed = await reader.read(count=100, block_ms=1000)
            records = [payload for _, payload in consumed]
            if records:
                try:
                    filtered_records = _dedupe_records(records, seen_ids)
                    if filtered_records:
                        signals = await run_all_scanners(filtered_records)
                        if signals:
                            async with SessionLocal() as session:
                                await write_signals_to_db(session, signals)
                    for message_id, _ in consumed:
                        await reader.ack(message_id)
                except Exception as record_exc:
                    for message_id, payload in consumed:
                        await dead_letter_writer.write(
                            {
                                "source_stream": MARKET_STREAM,
                                "message_id": message_id,
                                "error": str(record_exc),
                                "payload": payload,
                                "failed_at": datetime.now(timezone.utc).isoformat(),
                            }
                        )
                        await reader.ack(message_id)

            backoff_seconds = 1
        except Exception as exc:
            print(f"scanner_worker error: {exc}")
            await asyncio.sleep(backoff_seconds)
            backoff_seconds = min(backoff_seconds * 2, 30)
            continue

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())


def _parse_csv(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def _record_fingerprint(record: dict) -> str:
    normalized = json.dumps(record, sort_keys=True, default=str)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _dedupe_records(records: list[dict], seen_ids: dict[str, float]) -> list[dict]:
    now_ts = datetime.now(timezone.utc).timestamp()
    ttl_seconds = 300
    expired = [key for key, ts in seen_ids.items() if (now_ts - ts) > ttl_seconds]
    for key in expired:
        seen_ids.pop(key, None)

    unique: list[dict] = []
    for record in records:
        fingerprint = _record_fingerprint(record)
        if fingerprint in seen_ids:
            continue
        seen_ids[fingerprint] = now_ts
        unique.append(record)
    return unique
