# Assignment 1: Weather Agent

## What it does
Fetches the user's location from `ipapi.co` and gets the current weather from the Open-Meteo API using a 3-node LangGraph workflow.

## Bugs fixed
1. `components/config.py`: Removed duplicate empty `WEATHER_API_BASE_URL` and the placeholder `TEMP_MIN` variable at the bottom of the class.
2. `components/helper_functions.py`: Removed `if temp_celsius: return config.TEMP_MIN` in `classify_temperature` since any non-zero float was returning `"Needs Debugging"`.
3. `components/nodes.py`: Fixed `state["location_data"] = {}` overwriting the API response, updated field check to `country_name`, and uncommented `wind_unit` so it displays the actual unit instead of the literal string `"wind_unit"`.
4. `graph.py`: Added the missing edge to `fetch_weather_data` and called `builder.compile()`.
5. `main.py`: Fixed `if __name__ == "_main_":` to `"__main__"`.
6. `components/schema.py` & `requirements.txt`: Changed `is_day` type to `int` and added `requests` and `python-dotenv` to requirements.

## How to run

```bash
cd weather_agent
pip install -r requirements.txt
python main.py
```
