import requests
from components.state import WeatherAgentState
from components.config import config
from components.helper_functions import (
    classify_temperature,
    get_weather_description,
    get_greeting,
    format_local_time,
)


def fetch_location_data(state: WeatherAgentState) -> WeatherAgentState:
    """Fetch user location from ipapi based on IP."""
    try:
        response = requests.get(
            config.LOCATION_API_URL,
            timeout=config.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        location_data = response.json()

        required_fields = [
            "city",
            "region",
            "country_name",
            "latitude",
            "longitude",
            "utc_offset",
            "timezone",
        ]
        for field in required_fields:
            if field not in location_data:
                raise ValueError(f"Missing required field: {field}")

        state["location_data"] = location_data

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch location data: {e}")
    except ValueError as e:
        raise Exception(f"Invalid location data received: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching location: {e}")

    return state


def fetch_weather_data(state: WeatherAgentState) -> WeatherAgentState:
    """Fetch current weather from Open-Meteo for the user coordinates."""
    if not state.get("location_data"):
        raise Exception("Location data not available for weather fetch")

    location = state["location_data"]

    try:
        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current_weather": "true",
        }

        response = requests.get(
            config.WEATHER_API_BASE_URL,
            params=params,
            timeout=config.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        weather_data = response.json()

        if "current_weather" not in weather_data:
            raise ValueError("Missing current_weather data in response")

        required_weather_fields = [
            "time",
            "temperature",
            "windspeed",
            "winddirection",
            "is_day",
            "weathercode",
        ]
        current_weather = weather_data["current_weather"]

        for field in required_weather_fields:
            if field not in current_weather:
                raise ValueError(f"Missing required weather field: {field}")

        state["weather_data"] = weather_data

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch weather data: {e}")
    except ValueError as e:
        raise Exception(f"Invalid weather data received: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching weather: {e}")

    return state


def generate_weather_info(state: WeatherAgentState) -> WeatherAgentState:
    """Format location and weather data into the final text output."""
    if not state.get("location_data") or not state.get("weather_data"):
        raise Exception("Location or weather data not available for info generation")

    location = state["location_data"]
    weather = state["weather_data"]["current_weather"]
    units = state["weather_data"].get("current_weather_units", {})

    try:
        name = state["name"]
        city = location["city"]
        region = location["region"]
        # fallback to country code if country_name is missing in custom payloads
        country = location.get("country_name") or location.get("country")
        utc_offset = location["utc_offset"]

        temperature = weather["temperature"]
        temp_unit = units.get("temperature", "°C")
        windspeed = weather["windspeed"]
        wind_unit = units.get("windspeed", "km/h")
        is_day = weather["is_day"]
        weather_code = weather["weathercode"]
        utc_time = weather["time"]

        greeting = get_greeting(is_day)
        temp_classification = classify_temperature(temperature)
        weather_description = get_weather_description(weather_code)
        time_info = format_local_time(utc_time, utc_offset)

        weather_info_parts = [
            f"Time: {time_info}",
            "",
            f"{greeting}, {name}!",
            "",
            f"Your current location: {city}, {region}, {country}",
            "",
            "Current weather conditions:",
            f"- {weather_description}",
            f"- Temperature: {temperature}{temp_unit} ({temp_classification})",
            f"- Wind: {windspeed} {wind_unit}",
        ]

        state["weather_info"] = "\n".join(weather_info_parts)

    except KeyError as e:
        raise Exception(f"Missing data field for weather info generation: {e}")
    except Exception as e:
        raise Exception(f"Error generating weather info: {e}")

    return state
