# FutureSight

trading analytics and scanning

## Run
- `uvicorn backend.main:app --reload`
- `python workers/scanner_worker.py`
- `python workers/analytics_worker.py`
- `cd frontend && npm run dev`

## Docker
- `docker compose -f infra/docker-compose.yml up --build`

## Ingestion and Queueing
- The scanner worker ingests equities from Massive.com and options/futures from an IBKR adapter endpoint.
- All market payloads are written to Redis stream `market.ingestion`.
- Scanner processing failures are routed to `market.dead_letter` for replay/debugging.

## Scanner Configuration
- `SCANNER_EQUITY_SYMBOLS` (csv)
- `SCANNER_OPTIONS_SYMBOLS` (csv)
- `SCANNER_FUTURES_CONTRACTS` (csv)
