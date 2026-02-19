# Stock Analysis App

A lightweight Python stock analysis app that fetches details for any ticker you enter.

## What it provides
- Company name and current price
- Previous close and daily percentage change
- 52-week high/low range
- Average volume (3 month)
- Market cap and trailing P/E ratio
- Basic trend signal using 20-day vs 50-day moving averages

## Run

```bash
python stock_app.py
```

Then input a ticker like `AAPL`, `MSFT`, or `TSLA`.

## Test

```bash
pytest -q
```
