# LangGraph Assessment

This repository contains the completed solutions for the **LangGraph Final Assessment**, consisting of two modular AI agent assignments:

1. **Assignment 1 (`assignment_1/`)**: Debugging and fixing a broken LangGraph Weather Agent, complete with unit tests, multi-scenario simulations, error-handling tests, and detailed bug documentation in `weather_agent_debug.ipynb`.
2. **Assignment 2 (`assignment_2/`)**: Building a Stock Market Analysis Agent from scratch using LangGraph and `yfinance` that fetches 60 days of historical stock data, calculates 10-day & 20-day Simple Moving Averages (SMA) and 14-day Relative Strength Index (RSI), and generates a formatted `BUY` / `HOLD` / `SELL` analysis report, demonstrated in `stock_analysis_agent.ipynb`.

---

## Repository Structure

```text
langgraph-assessment/
├── .gitignore
├── README.md
├── assignment_1/
│   ├── README.md
│   ├── weather_agent_debug.ipynb
│   └── weather_agent/
│       ├── main.py
│       ├── graph.py
│       ├── requirements.txt
│       └── components/
│           ├── __init__.py
│           ├── config.py
│           ├── helper_functions.py
│           ├── nodes.py
│           ├── schema.py
│           └── state.py
└── assignment_2/
    ├── README.md
    ├── stock_analysis_agent.ipynb
    └── stock_agent/
        ├── main.py
        ├── graph.py
        ├── requirements.txt
        └── components/
            ├── __init__.py
            ├── config.py
            ├── helper_functions.py
            ├── nodes.py
            ├── schema.py
            └── state.py
```

---

## Quick Start

### 1. Create and Activate a Virtual Environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 2. Run Assignment 1 (Weather Agent)

```bash
cd assignment_1/weather_agent
pip install -r requirements.txt
python main.py
```

Or open `assignment_1/weather_agent_debug.ipynb` in Jupyter Notebook / VS Code.

### 3. Run Assignment 2 (Stock Market Analysis Agent)

```bash
cd assignment_2/stock_agent
pip install -r requirements.txt
python main.py
```

Or open `assignment_2/stock_analysis_agent.ipynb` in Jupyter Notebook / VS Code.
