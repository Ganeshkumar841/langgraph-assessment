# Assignment 2: Stock Market Analysis Agent

## What it does
Takes a stock ticker symbol (like `AAPL` or `MSFT`), downloads 60 days of daily price data using `yfinance`, calculates the 10-day SMA, 20-day SMA, and 14-day RSI, and prints a `BUY`, `HOLD`, or `SELL` recommendation report.

## Recommendation rules
- `BUY`: `SMA_10 > SMA_20` with `RSI < 70` and price at or above `SMA_10`, or `RSI < 30` (oversold) with price stabilizing.
- `SELL`: `SMA_10 < SMA_20` with `RSI > 30` and price at or below `SMA_10`, or `RSI > 70` (overbought) while trend is bearish.
- `HOLD`: Mixed signals (for example, `SMA_10 > SMA_20` but `RSI > 70` overbought).

## How to run

```bash
cd stock_agent
pip install -r requirements.txt
python main.py
```
