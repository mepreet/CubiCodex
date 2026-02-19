from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from analysis import build_stock_summary


def fetch_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_stock_payload(ticker: str) -> tuple[dict, list[float]]:
    quote_url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    chart_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1y&interval=1d"

    quote_data = fetch_json(quote_url)
    chart_data = fetch_json(chart_url)

    quotes = quote_data.get("quoteResponse", {}).get("result", [])
    if not quotes:
        raise ValueError(f"Ticker '{ticker}' not found.")

    close_list = (
        chart_data.get("chart", {})
        .get("result", [{}])[0]
        .get("indicators", {})
        .get("quote", [{}])[0]
        .get("close", [])
    )
    closes = [float(price) for price in close_list if isinstance(price, (int, float))]

    return quotes[0], closes


def format_money(value: float | int | None) -> str:
    if value is None:
        return "N/A"
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    return f"${value:,.2f}" if isinstance(value, float) else f"${value:,}"


def print_summary(ticker: str) -> None:
    quote, closes = fetch_stock_payload(ticker)
    summary = build_stock_summary(ticker, quote, closes)

    print(f"\n=== Stock Analysis: {summary.ticker} ===")
    print(f"Company: {summary.company_name}")
    print(f"Current Price: {format_money(summary.current_price)}")
    print(f"Previous Close: {format_money(summary.previous_close)}")
    print(f"Day Change: {summary.day_change_pct:.2f}%")
    print(f"Trend Signal (20/50 MA): {summary.trend_signal}")
    print(f"52W Range: {format_money(summary.low_52w)} - {format_money(summary.high_52w)}")
    print(f"Average Volume (3M): {summary.avg_volume:,}" if summary.avg_volume else "Average Volume (3M): N/A")
    print(f"Market Cap: {format_money(summary.market_cap)}")
    print(f"P/E Ratio: {summary.pe_ratio:.2f}" if summary.pe_ratio else "P/E Ratio: N/A")


if __name__ == "__main__":
    ticker = input("Enter a ticker (e.g., AAPL): ").strip().upper()
    if not ticker:
        print("Ticker is required.")
    else:
        try:
            print_summary(ticker)
        except ValueError as exc:
            print(str(exc))
        except (HTTPError, URLError):
            print("Network error: unable to reach Yahoo Finance from this environment.")
        except Exception as exc:
            print(f"Unexpected error: {exc}")
