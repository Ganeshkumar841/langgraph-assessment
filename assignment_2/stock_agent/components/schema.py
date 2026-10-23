from typing import List, Literal
from pydantic import BaseModel, Field

class TechnicalIndicators(BaseModel):
    """Calculated technical indicators for a stock"""
    current_price: float = Field(..., description="Latest closing price")
    previous_close: float = Field(..., description="Previous trading day closing price")
    daily_change_pct: float = Field(..., description="1-day percentage change")
    period_change_pct: float = Field(..., description="60-day percentage change")
    period_high: float = Field(..., description="60-day highest price")
    period_low: float = Field(..., description="60-day lowest price")
    avg_volume: int = Field(..., description="60-day average trading volume")
    sma_10: float = Field(..., description="10-day Simple Moving Average")
    sma_20: float = Field(..., description="20-day Simple Moving Average")
    rsi_14: float = Field(..., description="14-day Relative Strength Index (0-100)")

class RecommendationResult(BaseModel):
    """Stock recommendation output"""
    action: Literal["BUY", "HOLD", "SELL"] = Field(..., description="Recommended trading action")
    confidence: str = Field(..., description="Signal strength (Strong / Moderate / Neutral)")
    trend_signal: str = Field(..., description="SMA crossover signal summary")
    momentum_signal: str = Field(..., description="RSI momentum signal summary")
    reasons: List[str] = Field(..., description="Detailed bullet points explaining the recommendation")
