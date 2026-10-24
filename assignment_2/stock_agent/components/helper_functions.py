import pandas as pd
from components.config import config


def calculate_sma(close_series: pd.Series, window: int) -> float:
    if len(close_series) < window:
        raise ValueError(f"Not enough data ({len(close_series)} rows) for {window}-day SMA")
    sma = close_series.rolling(window=window).mean().iloc[-1]
    return round(float(sma), 2)


def calculate_rsi(close_series: pd.Series, period: int = 14) -> float:
    """Compute 14-day RSI from closing prices."""
    if len(close_series) < period + 1:
        raise ValueError(f"Not enough data ({len(close_series)} rows) for {period}-day RSI")

    delta = close_series.diff()
    gains = delta.clip(lower=0.0)
    losses = -delta.clip(upper=0.0)

    avg_gain = gains.rolling(window=period, min_periods=period).mean()
    avg_loss = losses.rolling(window=period, min_periods=period).mean()

    last_gain = float(avg_gain.iloc[-1])
    last_loss = float(avg_loss.iloc[-1])

    # avoid division by zero if all days moved in one direction
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
    rsi_14: float,
) -> dict:
    """Return BUY, HOLD, or SELL decision and short reasons based on SMA and RSI."""
    reasons = []
    sma_diff_pct = ((sma_10 - sma_20) / sma_20) * 100.0 if sma_20 else 0.0

    if sma_10 > sma_20:
        trend_signal = "Bullish (SMA-10 > SMA-20)"
        reasons.append(
            f"10-day SMA (${sma_10:.2f}) is above 20-day SMA (${sma_20:.2f}) by {sma_diff_pct:+.2f}%."
        )
    elif sma_10 < sma_20:
        trend_signal = "Bearish (SMA-10 < SMA-20)"
        reasons.append(
            f"10-day SMA (${sma_10:.2f}) is below 20-day SMA (${sma_20:.2f}) by {sma_diff_pct:.2f}%."
        )
    else:
        trend_signal = "Neutral (SMA-10 == SMA-20)"
        reasons.append(f"10-day SMA and 20-day SMA are both at ${sma_10:.2f}.")

    if current_price > sma_10 and current_price > sma_20:
        reasons.append(f"Current price (${current_price:.2f}) is above both moving averages.")
    elif current_price < sma_10 and current_price < sma_20:
        reasons.append(f"Current price (${current_price:.2f}) is below both moving averages.")
    else:
        reasons.append(f"Current price (${current_price:.2f}) is between the 10-day and 20-day SMAs.")

    if rsi_14 < config.RSI_OVERSOLD:
        momentum_signal = f"Oversold (RSI = {rsi_14:.2f})"
        reasons.append(f"14-day RSI ({rsi_14:.2f}) is below 30 (oversold).")
    elif rsi_14 > config.RSI_OVERBOUGHT:
        momentum_signal = f"Overbought (RSI = {rsi_14:.2f})"
        reasons.append(f"14-day RSI ({rsi_14:.2f}) is above 70 (overbought).")
    else:
        momentum_signal = f"Neutral (RSI = {rsi_14:.2f})"
        reasons.append(f"14-day RSI ({rsi_14:.2f}) is in the normal 30-70 range.")

    if rsi_14 > config.RSI_OVERBOUGHT:
        if sma_10 < sma_20:
            action = "SELL"
            confidence = "Strong"
        else:
            action = "HOLD"
            confidence = "Moderate"
            reasons.append("Trend is positive, but RSI is overbought so holding for now.")
    elif rsi_14 < config.RSI_OVERSOLD:
        if sma_10 >= sma_20 or current_price >= sma_10:
            action = "BUY"
            confidence = "Strong"
        else:
            action = "HOLD"
            confidence = "Moderate"
            reasons.append("RSI is oversold, but waiting for moving averages to stabilize.")
    else:
        if sma_10 > sma_20 and current_price >= sma_10:
            action = "BUY"
            confidence = "Strong" if 45.0 <= rsi_14 <= 65.0 else "Moderate"
        elif sma_10 > sma_20 and current_price < sma_10:
            action = "HOLD"
            confidence = "Moderate"
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
        "reasons": reasons,
    }
