from typing import List, Literal
from pydantic import BaseModel, Field


class TechnicalIndicators(BaseModel):
    current_price: float = Field(..., description="Latest closing price")
    previous_close: float = Field(..., description="Previous trading day closing price")
    daily_change_pct: float = Field(..., description="1-day percentage change")
    period_change_pct: float = Field(..., description="60-day percentage change")
    period_high: float = Field(..., description="60-day highest price")
    period_low: float = Field(..., description="60-day lowest price")
    avg_volume: int = Field(..., description="60-day average trading volume")
    sma_10: float = Field(..., description="10-day Simple Moving Average")
    sma_20: float = Field(..., description="20-day Simple Moving Average")
    rsi_14: float = Field(..., description="14-day Relative Strength Index")


class RecommendationResult(BaseModel):
    action: Literal["BUY", "HOLD", "SELL"] = Field(..., description="Recommended trading action")
    confidence: str = Field(..., description="Signal strength")
    trend_signal: str = Field(..., description="SMA crossover signal")
    momentum_signal: str = Field(..., description="RSI signal")
    reasons: List[str] = Field(..., description="Reasons for the recommendation")
