from datetime import datetime, timezone


def scan_equities(rows: list[dict]) -> list[dict]:
    signals: list[dict] = []
    for row in rows:
        gap_percent = float(row.get("gap_percent", 0.0))
        volume = float(row.get("volume", 0.0))
        avg_volume = float(row.get("avg_volume", 1.0))
        price = float(row.get("price", 0.0))
        if gap_percent > 3 and volume > (3 * avg_volume) and price > 20:
            signals.append({"symbol": str(row.get("symbol", "UNKNOWN")), "signal_type": "equity_gap_volume", "price": price, "confidence": min(1.0, 0.5 + gap_percent / 10.0), "created_at": datetime.now(timezone.utc)})
    return signals
