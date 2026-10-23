from typing import Optional, Dict, Any, TypedDict

class StockAgentState(TypedDict):
    """
    State schema for the Stock Market Analysis Agent.

    Fields:
        ticker (str): Input stock ticker symbol (e.g., 'AAPL', 'MSFT').
        stock_data (dict | None): Historical OHLCV summary and price series extracted via yfinance.
        indicators (dict | None): Calculated technical indicators (SMA-10, SMA-20, RSI-14, trend metrics).
        recommendation (dict | None): Recommendation action ('BUY', 'HOLD', 'SELL') and supporting reasons.
        analysis_report (str | None): Formatted final analysis report for display.
        error (str | None): Error message if data retrieval or validation fails.
    """
    ticker: str
    stock_data: Optional[Dict[str, Any]]
    indicators: Optional[Dict[str, Any]]
    recommendation: Optional[Dict[str, Any]]
    analysis_report: Optional[str]
    error: Optional[str]
