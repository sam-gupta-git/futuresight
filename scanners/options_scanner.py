from datetime import datetime, timezone


def scan_options(rows: list[dict]) -> list[dict]:
    signals: list[dict] = []
    for row in rows:
        iv_percentile = float(row.get("iv_percentile", 0.0))
        options_volume = float(row.get("options_volume", 0.0))
        avg_options_volume = float(row.get("avg_options_volume", 1.0))
        if iv_percentile > 70 and options_volume > (5 * avg_options_volume):
            signals.append({"symbol": str(row.get("symbol", "UNKNOWN")), "signal_type": "options_iv_volume", "price": float(row.get("price", 0.0)), "confidence": min(1.0, 0.6 + (iv_percentile - 70) / 100.0), "created_at": datetime.now(timezone.utc)})
    return signals
