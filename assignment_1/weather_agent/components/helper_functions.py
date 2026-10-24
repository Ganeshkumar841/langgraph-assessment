from datetime import datetime, timedelta
from components.config import config


def classify_temperature(temp_celsius: float) -> str:
    if temp_celsius < config.TEMP_COLD:
        return "cold"
    elif temp_celsius < config.TEMP_COOL:
        return "cool"
    elif temp_celsius < config.TEMP_COMFORTABLE:
        return "comfortable"
    elif temp_celsius < config.TEMP_WARM:
        return "warm"
    return "hot"


def get_weather_description(weather_code: int) -> str:
    return config.WEATHER_CODE_DESCRIPTIONS.get(weather_code, f"Weather code {weather_code}")


def get_greeting(is_day: int) -> str:
    return "Good morning" if is_day == 1 else "Good evening"


def parse_utc_offset(utc_offset_str: str) -> timedelta:
    """Convert offset string like +05:30 or +0530 into a timedelta."""
    try:
        offset_str = utc_offset_str.replace("+", "")
        sign = -1 if offset_str.startswith("-") else 1
        offset_str = offset_str.replace("-", "")

        if ":" in offset_str:
            hours, minutes = map(int, offset_str.split(":"))
        elif len(offset_str) == 4:
            # ipapi returns +0530 without a colon
            hours = int(offset_str[:2])
            minutes = int(offset_str[2:])
        else:
            hours = int(offset_str)
            minutes = 0

        return timedelta(hours=sign * hours, minutes=sign * minutes)
    except (ValueError, IndexError):
        return timedelta(0)


def format_local_time(utc_time_str: str, utc_offset_str: str) -> str:
    try:
        utc_time = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
        local_time = utc_time + parse_utc_offset(utc_offset_str)

        utc_formatted = utc_time.strftime("%H:%M UTC")
        local_formatted = local_time.strftime("%H:%M")

        return f"{utc_formatted} | {local_formatted} (UTC{utc_offset_str})"
    except Exception:
        return "Time unavailable"
