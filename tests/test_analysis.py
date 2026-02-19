from analysis import build_stock_summary, compute_day_change_pct, moving_average_signal


def test_compute_day_change_pct():
    assert round(compute_day_change_pct(110.0, 100.0), 2) == 10.00


def test_moving_average_signal_bullish():
    closes = [float(i) for i in range(1, 70)]
    assert moving_average_signal(closes) == "Bullish"


def test_build_stock_summary_defaults():
    quote = {"regularMarketPrice": 11.0}
    summary = build_stock_summary("msft", quote, [10.0, 11.0])

    assert summary.ticker == "MSFT"
    assert summary.company_name == "MSFT"
    assert summary.current_price == 11.0
