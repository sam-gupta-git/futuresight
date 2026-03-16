from datetime import datetime, timezone


def scan_futures(rows: list[dict]) -> list[dict]:
    signals: list[dict] = []
    for row in rows:
        price = float(row.get("price", 0.0))
        overnight_high = float(row.get("overnight_high", 0.0))
        volume = float(row.get("volume", 0.0))
        avg_volume = float(row.get("avg_volume", 1.0))
        atr = float(row.get("atr", 0.0))
        atr_prev = float(row.get("atr_prev", 1.0))
        if price > overnight_high and volume > (2 * avg_volume) and atr > (1.2 * atr_prev):
            signals.append({"symbol": str(row.get("contract", row.get("symbol", "UNKNOWN"))), "signal_type": "futures_breakout", "price": price, "confidence": 0.75, "created_at": datetime.now(timezone.utc)})
    return signals
