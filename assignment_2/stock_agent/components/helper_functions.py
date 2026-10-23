import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
from components.config import config

def calculate_sma(close_series: pd.Series, window: int) -> float:
    """
    Calculate the Simple Moving Average (SMA) over a specified window.

    Args:
        close_series: Pandas Series of closing prices
        window: Rolling window size in trading days

    Returns:
        Latest SMA value rounded to 2 decimal places
    """
    if len(close_series) < window:
        raise ValueError(f"Insufficient data points ({len(close_series)}) for {window}-day SMA")
    sma = close_series.rolling(window=window).mean().iloc[-1]
    return round(float(sma), 2)

def calculate_rsi(close_series: pd.Series, period: int = 14) -> float:
    """
    Calculate the 14-day Relative Strength Index (RSI).

    Uses Wilder's smoothing / rolling average of gains and losses over `period` days.

    Args:
        close_series: Pandas Series of closing prices
        period: Lookback window for RSI calculation (default: 14)

    Returns:
        Latest RSI value (0.0 to 100.0) rounded to 2 decimal places
    """
    if len(close_series) < period + 1:
        raise ValueError(f"Insufficient data points ({len(close_series)}) for {period}-day RSI")

    delta = close_series.diff()
    gains = delta.clip(lower=0.0)
    losses = -delta.clip(upper=0.0)

    avg_gain = gains.rolling(window=period, min_periods=period).mean()
    avg_loss = losses.rolling(window=period, min_periods=period).mean()

    last_gain = float(avg_gain.iloc[-1])
    last_loss = float(avg_loss.iloc[-1])

    if last_loss == 0.0:
        return 100.0
    if last_gain == 0.0:
        return 0.0

    rs = last_gain / last_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return round(float(rsi), 2)

def evaluate_recommendation(
    current_price: float,
    sma_10: float,
    sma_20: float,
    rsi_14: float
) -> Dict[str, Any]:
    """
    Determine BUY / HOLD / SELL recommendation based on SMA-10, SMA-20, and 14-day RSI.

    Decision Logic:
    1. Trend Analysis (SMA-10 vs SMA-20 & Current Price):
       - Bullish Crossover / Uptrend: SMA-10 > SMA-20
       - Bearish Crossover / Downtrend: SMA-10 < SMA-20
    2. Momentum Analysis (14-day RSI):
       - Oversold (< 30): Strong buying opportunity / rebound potential
       - Overbought (> 70): Pullback risk / profit-taking signal
       - Neutral (30 to 70): Healthy trend continuation zone
    3. Combined Action Rule:
       - BUY:
         * Bullish trend (SMA-10 > SMA-20) AND RSI is not overbought (RSI < 70), OR
         * Stock is deeply oversold (RSI < 30) with price stabilizing near/above SMA-20
       - SELL:
         * Bearish trend (SMA-10 < SMA-20) AND RSI is not oversold (RSI > 30), OR
         * Stock is overbought (RSI > 70) showing exhaustion
       - HOLD:
         * Conflicting signals (e.g., SMA-10 < SMA-20 but RSI < 30 oversold bounce watch,
           or flat moving averages where SMA-10 == SMA-20)
    """
    reasons: List[str] = []

    # Evaluate SMA trend
    sma_diff_pct = ((sma_10 - sma_20) / sma_20) * 100.0 if sma_20 else 0.0
    if sma_10 > sma_20:
        trend_signal = "Bullish (SMA-10 > SMA-20)"
        reasons.append(
            f"10-day SMA (${sma_10:.2f}) is above 20-day SMA (${sma_20:.2f}) by {sma_diff_pct:+.2f}%, indicating positive short-term upward momentum."
        )
    elif sma_10 < sma_20:
        trend_signal = "Bearish (SMA-10 < SMA-20)"
        reasons.append(
            f"10-day SMA (${sma_10:.2f}) is below 20-day SMA (${sma_20:.2f}) by {sma_diff_pct:.2f}%, signaling downward short-term trend pressure."
        )
    else:
        trend_signal = "Neutral (SMA-10 == SMA-20)"
        reasons.append(
            f"10-day SMA (${sma_10:.2f}) and 20-day SMA (${sma_20:.2f}) are converged, indicating sideways consolidation."
        )

    # Price relative to SMAs
    if current_price > sma_10 and current_price > sma_20:
        reasons.append(f"Current price (${current_price:.2f}) is trading above both the 10-day and 20-day moving averages.")
    elif current_price < sma_10 and current_price < sma_20:
        reasons.append(f"Current price (${current_price:.2f}) is trading below both the 10-day and 20-day moving averages.")
    else:
        reasons.append(f"Current price (${current_price:.2f}) is trading between the 10-day and 20-day moving averages.")

    # Evaluate RSI momentum
    if rsi_14 < config.RSI_OVERSOLD:
        momentum_signal = f"Oversold (RSI = {rsi_14:.2f} < {config.RSI_OVERSOLD:.0f})"
        reasons.append(f"14-day RSI ({rsi_14:.2f}) is in oversold territory (< 30), suggesting selling exhaustion and rebound potential.")
    elif rsi_14 > config.RSI_OVERBOUGHT:
        momentum_signal = f"Overbought (RSI = {rsi_14:.2f} > {config.RSI_OVERBOUGHT:.0f})"
        reasons.append(f"14-day RSI ({rsi_14:.2f}) is in overbought territory (> 70), indicating elevated pullback risk.")
    else:
        momentum_signal = f"Neutral (RSI = {rsi_14:.2f})"
        reasons.append(f"14-day RSI ({rsi_14:.2f}) is within the healthy neutral range (30–70) with room for trend continuation.")

    # Determine final BUY / HOLD / SELL action
    if rsi_14 > config.RSI_OVERBOUGHT:
        if sma_10 < sma_20:
            action = "SELL"
            confidence = "Strong"
        else:
            action = "HOLD"
            confidence = "Moderate"
            reasons.append("Although the moving average trend is bullish, the overbought RSI (> 70) warrants holding and waiting for a better entry point.")
    elif rsi_14 < config.RSI_OVERSOLD:
        if sma_10 >= sma_20 or current_price >= sma_10:
            action = "BUY"
            confidence = "Strong"
        else:
            action = "HOLD"
            confidence = "Moderate"
            reasons.append("Oversold RSI (< 30) suggests a potential bounce, but waiting for SMA stabilization reduces downside risk.")
    else:
        # Neutral RSI (30 <= RSI <= 70): governed by SMA crossover and price confirmation
        if sma_10 > sma_20 and current_price >= sma_10:
            action = "BUY"
            confidence = "Strong" if 45.0 <= rsi_14 <= 65.0 else "Moderate"
        elif sma_10 > sma_20 and current_price < sma_10:
            action = "HOLD"
            confidence = "Moderate"
            reasons.append("Bullish SMA crossover remains intact, but price dipped below the 10-day SMA; holding until short-term support holds.")
        elif sma_10 < sma_20 and current_price <= sma_10:
            action = "SELL"
            confidence = "Strong" if 35.0 <= rsi_14 <= 55.0 else "Moderate"
        else:
            action = "HOLD"
            confidence = "Neutral"

    return {
        "action": action,
        "confidence": confidence,
        "trend_signal": trend_signal,
        "momentum_signal": momentum_signal,
        "reasons": reasons
    }
