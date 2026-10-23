# Assignment 1: Weather Agent Debugging

## Overview
This folder contains the debugged and verified **LangGraph Weather Agent** (`weather_agent/`) and the accompanying interactive debugging & verification notebook (`weather_agent_debug.ipynb`).

## Summary of Bugs Identified & Fixed

1. **`components/config.py` (Duplicate `WEATHER_API_BASE_URL` Override)**: Removed the duplicate `WEATHER_API_BASE_URL: str = ""` on line 53 that overwrote the valid Open-Meteo URL (`https://api.open-meteo.com/v1/forecast`).
2. **`components/config.py` (Invalid `TEMP_MIN` Declaration)**: Removed `TEMP_MIN = str = "Needs Debugging"` on line 55.
3. **`components/helper_functions.py` (`classify_temperature` Always Returning `"Needs Debugging"`)**: Removed the faulty `if temp_celsius: return config.TEMP_MIN` branch so temperatures are properly classified against `TEMP_COLD` (10°C), `TEMP_COOL` (18°C), `TEMP_COMFORTABLE` (26°C), and `TEMP_WARM` (32°C).
4. **`components/nodes.py` (`fetch_location_data` Field Validation Mismatch)**: Updated `required_fields` to check `'country_name'` (matching `schema.py` and `generate_weather_info`) and added a safe fallback `location.get("country_name") or location.get("country")`.
5. **`components/nodes.py` (`state["location_data"] = {}` Data Loss)**: Fixed `state["location_data"] = location_data` so the parsed geolocation response is preserved in state instead of being overwritten with an empty dictionary.
6. **`components/nodes.py` (`wind_unit` Commented Out & Hardcoded Literal)**: Uncommented `wind_unit = units.get("windspeed", "km/h")` and interpolated `{wind_unit}` in `f"• Wind: {windspeed} {wind_unit}"`.
7. **`graph.py` (`fetch_weather_data` Node Disconnected)**: Added edges `fetch_location_data -> fetch_weather_data -> generate_weather_info` so weather data is fetched before report generation.
8. **`graph.py` (Uncompiled `StateGraph`)**: Changed `weather_agent = builder` to `weather_agent = builder.compile()` so `.invoke()` works.
9. **`main.py` (`__name__ == "_main_"` Entry Guard Typo)**: Fixed single underscores `"_main_"` to double underscores `"__main__"`.
10. **`components/schema.py` & `requirements.txt`**: Updated `CurrentWeather.is_day` to `int` (matching Open-Meteo's `0`/`1` integer output) and ensured `requests` and `python-dotenv` are listed in `requirements.txt`.
