from langgraph.graph import StateGraph, START, END
from components.state import WeatherAgentState
from components.nodes import (
    fetch_location_data,
    fetch_weather_data, 
    generate_weather_info
)

builder = StateGraph(WeatherAgentState)

# Add nodes
builder.add_node("fetch_location_data", fetch_location_data)
builder.add_node("fetch_weather_data", fetch_weather_data)
builder.add_node("generate_weather_info", generate_weather_info)

# Add edges - sequential linear flow
builder.add_edge(START, "fetch_location_data")
builder.add_edge("fetch_location_data", "fetch_weather_data")
builder.add_edge("fetch_weather_data", "generate_weather_info")
builder.add_edge("generate_weather_info", END)

# Compile the graph into an executable runnable
weather_agent = builder.compile()
