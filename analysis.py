from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StockSummary:
    ticker: str
    company_name: str
    current_price: float
    previous_close: float | None
    day_change_pct: float
    high_52w: float | None
    low_52w: float | None
    avg_volume: int | None
    market_cap: int | None
    pe_ratio: float | None
    trend_signal: str


def compute_day_change_pct(current_price: float, previous_close: float | None) -> float:
    if previous_close in (None, 0):
        return 0.0
    return ((current_price - previous_close) / previous_close) * 100


def moving_average(values: list[float], window: int) -> float | None:
    if len(values) < window:
        return None
    subset = values[-window:]
    return sum(subset) / window


def moving_average_signal(closes: list[float], short_window: int = 20, long_window: int = 50) -> str:
    short_ma = moving_average(closes, short_window)
    long_ma = moving_average(closes, long_window)

    if short_ma is None or long_ma is None:
        return "Not enough data"
    if short_ma > long_ma:
        return "Bullish"
    if short_ma < long_ma:
        return "Bearish"
    return "Neutral"


def build_stock_summary(ticker: str, quote: dict, closes: list[float]) -> StockSummary:
    current_price = float(quote.get("regularMarketPrice") or 0.0)
    previous_close = quote.get("regularMarketPreviousClose")
    prev_close_float = float(previous_close) if previous_close is not None else None

    return StockSummary(
        ticker=ticker.upper(),
        company_name=quote.get("longName") or quote.get("shortName") or ticker.upper(),
        current_price=current_price,
        previous_close=prev_close_float,
        day_change_pct=compute_day_change_pct(current_price, prev_close_float),
        high_52w=quote.get("fiftyTwoWeekHigh"),
        low_52w=quote.get("fiftyTwoWeekLow"),
        avg_volume=quote.get("averageDailyVolume3Month"),
        market_cap=quote.get("marketCap"),
        pe_ratio=quote.get("trailingPE"),
        trend_signal=moving_average_signal(closes),
    )
