from langgraph.graph import StateGraph, START, END
from components.state import StockAgentState
from components.nodes import (
    fetch_stock_data,
    calculate_indicators,
    generate_recommendation
)

builder = StateGraph(StockAgentState)

# Add nodes
builder.add_node("fetch_stock_data", fetch_stock_data)
builder.add_node("calculate_indicators", calculate_indicators)
builder.add_node("generate_recommendation", generate_recommendation)

# Add sequential edges
builder.add_edge(START, "fetch_stock_data")
builder.add_edge("fetch_stock_data", "calculate_indicators")
builder.add_edge("calculate_indicators", "generate_recommendation")
builder.add_edge("generate_recommendation", END)

# Compile the graph
stock_agent = builder.compile()
