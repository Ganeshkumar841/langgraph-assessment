from typing import Optional, Dict, Any, TypedDict


class WeatherAgentState(TypedDict):
    """State dictionary passed between weather agent nodes."""

    name: str
    location_data: Optional[Dict[str, Any]]
    weather_data: Optional[Dict[str, Any]]
    weather_info: Optional[str]
