# Assignment 2: Stock Market Analysis Agent

## Overview
This folder contains a modular **LangGraph Stock Market Analysis Agent** (`stock_agent/`) and an interactive demonstration notebook (`stock_analysis_agent.ipynb`).

## Architecture & Workflow
The agent uses a `StateGraph(StockAgentState)` pipeline with three sequential nodes:
1. **`fetch_stock_data`**: Validates the input stock ticker symbol and retrieves 60 trading days of historical OHLCV data using `yfinance`. Handles invalid tickers, delisted symbols, and network errors gracefully.
2. **`calculate_indicators`**: Computes the 10-day Simple Moving Average (`SMA-10`), 20-day Simple Moving Average (`SMA-20`), 14-day Relative Strength Index (`RSI-14`), daily/60-day price change percentages, 60-day trading range, and average volume.
3. **`generate_recommendation`**: Evaluates trend crossover (`SMA-10` vs. `SMA-20`) and momentum oscillator (`RSI-14` relative to `< 30` oversold and `> 70` overbought thresholds) to produce a `BUY`, `HOLD`, or `SELL` recommendation and a formatted analysis report.
