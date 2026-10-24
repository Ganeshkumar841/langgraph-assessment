from typing import Optional, Dict, Any, TypedDict


class StockAgentState(TypedDict):
    """State dictionary passed across stock analysis nodes."""

    ticker: str
    stock_data: Optional[Dict[str, Any]]
    indicators: Optional[Dict[str, Any]]
    recommendation: Optional[Dict[str, Any]]
    analysis_report: Optional[str]
    error: Optional[str]
