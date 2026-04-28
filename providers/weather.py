"""
Weather provider — Open-Meteo API (free, no key required).
https://open-meteo.com/
Cities are fetched concurrently to reduce total latency.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import CITIES, WEATHER_EMOJI, WEATHER_DESC
from providers.utils import fetch_json


def _fetch_city_weather(city: str, info: dict) -> str:
    """Fetch weather for a single city and return a formatted HTML table row."""
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
        return (
            f"<tr>"
            f"<td>{info['flag']} <b>{city}</b></td>"
            f"<td>{temp}°C</td>"
            f"<td>{humidity}%</td>"
            f"<td>{wind} km/h</td>"
            f"<td>{emoji} {desc}</td>"
            f"</tr>"
        )
    return (
        f"<tr>"
        f"<td>{info['flag']} <b>{city}</b></td>"
        f"<td colspan='4'>Data unavailable</td>"
        f"</tr>"
    )


def get_weather() -> str:
    """Fetch current weather for all cities concurrently from Open-Meteo, organized by continent."""
    # Flatten all cities and fetch concurrently
    all_cities = {}
    continent_cities = {}
    
    for continent, cities in CITIES.items():
        continent_cities[continent] = {}
        for city, info in cities.items():
            all_cities[(continent, city)] = info
    
    city_rows = {}
    with ThreadPoolExecutor(max_workers=len(all_cities)) as executor:
        future_to_key = {
            executor.submit(_fetch_city_weather, city, info): (continent, city)
            for (continent, city), info in all_cities.items()
        }
        for future in as_completed(future_to_key):
            continent, city = future_to_key[future]
            city_rows[(continent, city)] = future.result()

    # Build HTML output organized by continent
    result_html = ""
    for continent in CITIES.keys():
        result_html += f"<details open>\n<summary><b>{continent}</b></summary>\n\n<table>\n"
        result_html += "<tr>\n<th>🏙️ City</th>\n<th>🌡️ Temp</th>\n<th>💧 Humidity</th>\n<th>🌬️ Wind</th>\n<th>☁️ Conditions</th>\n</tr>\n"
        
        # Add rows for this continent
        for city in CITIES[continent].keys():
            if (continent, city) in city_rows:
                result_html += city_rows[(continent, city)] + "\n"
        
        result_html += "</table>\n\n</details>\n\n"
    
    return result_html.rstrip()
