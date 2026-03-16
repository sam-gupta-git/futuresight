from scanners.equity_scanner import scan_equities
from scanners.futures_scanner import scan_futures
from scanners.options_scanner import scan_options


def test_equity_scanner_creates_signal() -> None:
    rows = [{"symbol": "AAPL", "gap_percent": 4.1, "volume": 4_000_000, "avg_volume": 1_000_000, "price": 25}]
    signals = scan_equities(rows)
    assert len(signals) == 1


def test_options_scanner_creates_signal() -> None:
    rows = [{"symbol": "SPY", "iv_percentile": 75, "options_volume": 600_000, "avg_options_volume": 60_000, "price": 500}]
    signals = scan_options(rows)
    assert len(signals) == 1


def test_futures_scanner_creates_signal() -> None:
    rows = [{"contract": "ES", "price": 5100, "overnight_high": 5090, "volume": 200_000, "avg_volume": 80_000, "atr": 30, "atr_prev": 20}]
    signals = scan_futures(rows)
    assert len(signals) == 1


