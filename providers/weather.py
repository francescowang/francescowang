"""
Weather provider — Open-Meteo API (free, no key required).
https://open-meteo.com/
"""

from config import CITIES, WEATHER_EMOJI, WEATHER_DESC
from providers.utils import fetch_json


def get_weather() -> str:
    """Fetch current weather for all cities from Open-Meteo."""
    rows = []
    for city, info in CITIES.items():
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={info['lat']}&longitude={info['lon']}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            f"&temperature_unit=celsius&wind_speed_unit=kmh"
        )
        data = fetch_json(url)
        if data and "current" in data:
            cur = data["current"]
            code = cur.get("weather_code", 0)
            emoji = WEATHER_EMOJI.get(code, "?")
            desc = WEATHER_DESC.get(code, "Unknown")
            temp = cur.get("temperature_2m", "N/A")
            humidity = cur.get("relative_humidity_2m", "N/A")
            wind = cur.get("wind_speed_10m", "N/A")
            rows.append(
                f"<tr>"
                f"<td>{info['flag']} <b>{city}</b></td>"
                f"<td>{temp}°C</td>"
                f"<td>{humidity}%</td>"
                f"<td>{wind} km/h</td>"
                f"<td>{emoji} {desc}</td>"
                f"</tr>"
            )
        else:
            rows.append(
                f"<tr>"
                f"<td>{info['flag']} <b>{city}</b></td>"
                f"<td colspan='4'>Data unavailable</td>"
                f"</tr>"
            )
    return "\n".join(rows)
