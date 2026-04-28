"""
Configuration constants for the GitHub Profile README generator.
"""

CITIES = {
    "Europe": {
        "London":    {"lat": 51.51, "lon": -0.13, "flag": "🇬🇧"},
        "Paris":     {"lat": 48.86, "lon": 2.35, "flag": "🇫🇷"},
        "Milan":     {"lat": 45.46, "lon": 9.19, "flag": "🇮🇹"},
        "Berlin":    {"lat": 52.52, "lon": 13.41, "flag": "🇩🇪"},
        "Moscow":    {"lat": 55.75, "lon": 37.62, "flag": "🇷🇺"},
        "Amsterdam": {"lat": 52.37, "lon": 4.89, "flag": "🇳🇱"},
    },
    "Asia": {
        "Beijing":   {"lat": 39.90, "lon": 116.40, "flag": "🇨🇳"},
        "Tokyo":     {"lat": 35.68, "lon": 139.69, "flag": "🇯🇵"},
        "Dubai":     {"lat": 25.20, "lon": 55.27, "flag": "🇦🇪"},
        "Hong Kong": {"lat": 22.30, "lon": 114.18, "flag": "🇭🇰"},
        "Singapore": {"lat": 1.35, "lon": 103.82, "flag": "🇸🇬"},
        "Bangkok":   {"lat": 13.73, "lon": 100.49, "flag": "🇹🇭"},
        "Seoul":     {"lat": 37.57, "lon": 126.98, "flag": "🇰🇷"},
    },
    "North America": {
        "New York":  {"lat": 40.71, "lon": -74.01, "flag": "🇺🇸"},
        "Los Angeles": {"lat": 34.05, "lon": -118.24, "flag": "🇺🇸"},
        "Toronto":   {"lat": 43.65, "lon": -79.38, "flag": "🇨🇦"},
        "Mexico City": {"lat": 19.43, "lon": -99.13, "flag": "🇲🇽"},
    },
    "South America": {
        "São Paulo": {"lat": -23.55, "lon": -46.63, "flag": "🇧🇷"},
        "Buenos Aires": {"lat": -34.60, "lon": -58.38, "flag": "🇦🇷"},
        "Lima":      {"lat": -12.05, "lon": -77.04, "flag": "🇵🇪"},
    },
    "Africa": {
        "Cape Town": {"lat": -33.93, "lon": 18.42, "flag": "🇿🇦"},
        "Cairo":     {"lat": 30.04, "lon": 31.24, "flag": "🇪🇬"},
        "Lagos":     {"lat": 6.52, "lon": 3.36, "flag": "🇳🇬"},
    },
    "Oceania": {
        "Sydney":    {"lat": -33.87, "lon": 151.21, "flag": "🇦🇺"},
        "Melbourne": {"lat": -37.81, "lon": 144.96, "flag": "🇦🇺"},
        "Auckland":  {"lat": -37.01, "lon": 174.77, "flag": "🇳🇿"},
    },
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
