#!/usr/bin/env python3
"""
Update only the weather section in README.

Runs every 3 hours via GitHub Actions.
Inherits from UpdateScriptBase for common functionality.
"""

import logging

from .update_base import UpdateScriptBase
from .update_patterns import WEATHER_SECTION_HEADER, WEATHER_SECTION_END, WEATHER_TIMESTAMP
from providers.weather import get_weather


class WeatherUpdateScript(UpdateScriptBase):
    """Update script for weather section."""

    SECTION_HEADER_PATTERN = WEATHER_SECTION_HEADER
    SECTION_END_PATTERN = WEATHER_SECTION_END
    TIMESTAMP_PATTERN = WEATHER_TIMESTAMP

    def fetch_data(self) -> str:
        """Fetch current weather data for all cities."""
        return get_weather()

    def get_section_name(self) -> str:
        """Return the section name for logging."""
        return "weather"


def main():
    """Run the weather update script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    script = WeatherUpdateScript()
    script.run()


if __name__ == "__main__":
    main()
