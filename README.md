# LangGraph Assessment

Solutions for the two LangGraph assignments:

- `assignment_1/`: Debugged weather agent that fetches location by IP and current weather from Open-Meteo.
- `assignment_2/`: Stock market analysis agent using `yfinance` to compute 10-day SMA, 20-day SMA, and 14-day RSI and output a BUY, HOLD, or SELL recommendation.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
```

## Running Assignment 1

```bash
cd assignment_1/weather_agent
pip install -r requirements.txt
python main.py
```

Notebook: `assignment_1/weather_agent_debug.ipynb`

## Running Assignment 2

```bash
cd assignment_2/stock_agent
pip install -r requirements.txt
python main.py
```

Notebook: `assignment_2/stock_analysis_agent.ipynb`
