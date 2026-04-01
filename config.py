"""
Configuration constants for the GitHub Profile README generator.
"""

CITIES = {
    "London":    {"lat": 51.51, "lon": -0.13, "flag": "🇬🇧"},
    "Beijing":   {"lat": 39.90, "lon": 116.40, "flag": "🇨🇳"},
    "New York":  {"lat": 40.71, "lon": -74.01, "flag": "🇺🇸"},
    "Paris":     {"lat": 48.86, "lon": 2.35, "flag": "🇫🇷"},
    "Milan":     {"lat": 45.46, "lon": 9.19, "flag": "🇮🇹"},
    "Cape Town": {"lat": -33.93, "lon": 18.42, "flag": "🇿🇦"},
    "Tokyo":     {"lat": 35.68, "lon": 139.69, "flag": "🇯🇵"},
    "Sydney":    {"lat": -33.87, "lon": 151.21, "flag": "🇦🇺"},
    "Dubai":     {"lat": 25.20, "lon": 55.27, "flag": "🇦🇪"},
    "São Paulo": {"lat": -23.55, "lon": -46.63, "flag": "🇧🇷"},
}

ETFS = ["VUAG.L", "VWRL.L", "SPY", "QQQ", "ARKK", "VTI"]

WEATHER_EMOJI = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️",
    51: "🌦️", 53: "🌦️", 55: "🌧️",
    56: "🌧️", 57: "🌧️",
    61: "🌧️", 63: "🌧️", 65: "🌧️",
    66: "🌧️", 67: "🌧️",
    71: "🌨️", 73: "🌨️", 75: "🌨️", 77: "🌨️",
    80: "🌧️", 81: "🌧️", 82: "🌧️",
    85: "🌨️", 86: "🌨️",
    95: "⛈️", 96: "⛈️", 99: "⛈️",
}

WEATHER_DESC = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Dense drizzle",
    56: "Freezing drizzle", 57: "Freezing drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    66: "Freezing rain", 67: "Freezing rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Light showers", 81: "Showers", 82: "Heavy showers",
    85: "Light snow showers", 86: "Snow showers",
    95: "Thunderstorm", 96: "Hail thunderstorm", 99: "Heavy hail thunderstorm",
}

# Curated vocabulary — definitions fetched from Free Dictionary API
INTERESTING_WORDS = [
    "ephemeral", "serendipity", "petrichor", "ineffable", "eloquent",
    "ubiquitous", "mellifluous", "resilience", "pragmatic", "loquacious",
    "quixotic", "sanguine", "idempotent", "zeitgeist", "catharsis",
    "luminous", "entropy", "verisimilitude", "schadenfreude", "epiphany",
    "mercurial", "halcyon", "perspicacious", "numinous", "defenestration",
    "wanderlust", "esoteric", "panacea", "sonder", "apocryphal",
    "tenacious", "vicissitude", "quintessential", "melancholy", "obfuscate",
    "symbiosis", "paradigm", "juxtaposition", "euphoria", "labyrinthine",
]

MOON_PHASES = [
    "🌑 New Moon",
    "🌒 Waxing Crescent",
    "🌓 First Quarter",
    "🌔 Waxing Gibbous",
    "🌕 Full Moon",
    "🌖 Waning Gibbous",
    "🌗 Last Quarter",
    "🌘 Waning Crescent",
]
