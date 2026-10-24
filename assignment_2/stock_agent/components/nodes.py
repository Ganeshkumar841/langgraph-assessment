import pandas as pd
from components.state import StockAgentState
from components.config import config
from components.helper_functions import (
    calculate_sma,
    calculate_rsi,
    evaluate_recommendation,
)

try:
    import yfinance as yf
except ImportError:
    yf = None


def fetch_stock_data(state: StockAgentState) -> StockAgentState:
    """Download 60 days of daily stock history from Yahoo Finance."""
    raw_ticker = (state.get("ticker") or "").strip().upper()
    if not raw_ticker:
        state["error"] = "Invalid ticker symbol: Ticker cannot be empty."
        return state

    state["ticker"] = raw_ticker

    if yf is None:
        state["error"] = "yfinance library is not installed. Run `pip install yfinance`."
        return state

    try:
        ticker_obj = yf.Ticker(raw_ticker)
        hist = ticker_obj.history(period=config.HISTORY_PERIOD, interval=config.HISTORY_INTERVAL)

        if hist is None or hist.empty:
            state["error"] = f"No historical stock data found for ticker '{raw_ticker}'."
            return state

        if "Close" not in hist.columns:
            state["error"] = f"Historical data for '{raw_ticker}' is missing 'Close' prices."
            return state

        close_series = hist["Close"].dropna()
        if len(close_series) < config.MIN_REQUIRED_DAYS:
            state["error"] = (
                f"Insufficient historical data for '{raw_ticker}': found {len(close_series)} days, "
                f"need at least {config.MIN_REQUIRED_DAYS}."
            )
            return state

        dates = [str(idx.date()) if hasattr(idx, "date") else str(idx) for idx in close_series.index]
        volumes = hist["Volume"].dropna().tolist() if "Volume" in hist.columns else []
        highs = hist["High"].dropna().tolist() if "High" in hist.columns else close_series.tolist()
        lows = hist["Low"].dropna().tolist() if "Low" in hist.columns else close_series.tolist()

        state["stock_data"] = {
            "ticker": raw_ticker,
            "trading_days": len(close_series),
            "start_date": dates[0],
            "end_date": dates[-1],
            "dates": dates,
            "close_prices": [round(float(x), 4) for x in close_series.tolist()],
            "high_prices": [round(float(x), 4) for x in highs],
            "low_prices": [round(float(x), 4) for x in lows],
            "volumes": [int(v) for v in volumes] if volumes else [],
        }
        state["error"] = None

    except Exception as e:
        state["error"] = f"Failed to fetch stock data for '{raw_ticker}': {e}"

    return state


def calculate_indicators(state: StockAgentState) -> StockAgentState:
    """Compute SMA-10, SMA-20, RSI-14, and basic price stats."""
    if state.get("error"):
        return state

    stock_data = state.get("stock_data")
    if not stock_data or not stock_data.get("close_prices"):
        state["error"] = "Stock data is unavailable for indicator calculation."
        return state

    try:
        close_series = pd.Series(stock_data["close_prices"], dtype="float64")
        high_series = pd.Series(stock_data.get("high_prices", stock_data["close_prices"]), dtype="float64")
        low_series = pd.Series(stock_data.get("low_prices", stock_data["close_prices"]), dtype="float64")
        volumes = stock_data.get("volumes", [])

        current_price = round(float(close_series.iloc[-1]), 2)
        previous_close = round(float(close_series.iloc[-2]), 2) if len(close_series) >= 2 else current_price
        first_close = float(close_series.iloc[0])

        daily_change_pct = round(((current_price - previous_close) / previous_close) * 100.0, 2) if previous_close else 0.0
        period_change_pct = round(((current_price - first_close) / first_close) * 100.0, 2) if first_close else 0.0
        period_high = round(float(high_series.max()), 2)
        period_low = round(float(low_series.min()), 2)
        avg_volume = int(sum(volumes) / len(volumes)) if volumes else 0

        sma_10 = calculate_sma(close_series, config.SMA_SHORT_WINDOW)
        sma_20 = calculate_sma(close_series, config.SMA_LONG_WINDOW)
        rsi_14 = calculate_rsi(close_series, config.RSI_PERIOD)

        state["indicators"] = {
            "current_price": current_price,
            "previous_close": previous_close,
            "daily_change_pct": daily_change_pct,
            "period_change_pct": period_change_pct,
            "period_high": period_high,
            "period_low": period_low,
            "avg_volume": avg_volume,
            "sma_10": sma_10,
            "sma_20": sma_20,
            "rsi_14": rsi_14,
        }

    except Exception as e:
        state["error"] = f"Error calculating technical indicators: {e}"

    return state


def generate_recommendation(state: StockAgentState) -> StockAgentState:
    """Build the final recommendation and text report."""
    if state.get("error"):
        state["analysis_report"] = "\n".join([
            f"Stock Analysis Report: {state.get('ticker') or 'N/A'}",
            "Status: Error",
            f"Details: {state['error']}",
        ])
        return state

    stock_data = state["stock_data"]
    ind = state["indicators"]

    try:
        rec = evaluate_recommendation(
            current_price=ind["current_price"],
            sma_10=ind["sma_10"],
            sma_20=ind["sma_20"],
            rsi_14=ind["rsi_14"],
        )
        state["recommendation"] = rec

        reasons_formatted = "\n".join(f"- {r}" for r in rec["reasons"])
        report_lines = [
            f"Stock Analysis Report: {stock_data['ticker']}",
            f"Period: {stock_data['start_date']} to {stock_data['end_date']} ({stock_data['trading_days']} trading days)",
            "",
            "Price Summary:",
            f"- Current Price: ${ind['current_price']:.2f} ({ind['daily_change_pct']:+.2f}% today)",
            f"- 60-Day Change: {ind['period_change_pct']:+.2f}%",
            f"- 60-Day Range: ${ind['period_low']:.2f} to ${ind['period_high']:.2f}",
            f"- Avg Daily Volume: {ind['avg_volume']:,}",
            "",
            "Technical Indicators:",
            f"- 10-Day SMA: ${ind['sma_10']:.2f}",
            f"- 20-Day SMA: ${ind['sma_20']:.2f}",
            f"- 14-Day RSI: {ind['rsi_14']:.2f}",
            f"- Trend Signal: {rec['trend_signal']}",
            f"- Momentum Signal: {rec['momentum_signal']}",
            "",
            f"Recommendation: {rec['action']} (Confidence: {rec['confidence']})",
            "",
            "Notes:",
            reasons_formatted,
        ]
        state["analysis_report"] = "\n".join(report_lines)

    except Exception as e:
        state["error"] = f"Error generating recommendation report: {e}"

    return state
