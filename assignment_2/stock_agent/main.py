from graph import stock_agent
from components.state import StockAgentState

def main():
    ticker = input("Enter stock ticker symbol (e.g., AAPL, MSFT): ").strip().upper()
    if not ticker:
        ticker = "AAPL"

    initial_state = StockAgentState(
        ticker=ticker,
        stock_data=None,
        indicators=None,
        recommendation=None,
        analysis_report=None,
        error=None
    )

    try:
        final_state = stock_agent.invoke(initial_state)
        print("\n" + (final_state.get("analysis_report") or "No report generated."))
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")

if __name__ == "__main__":
    main()
