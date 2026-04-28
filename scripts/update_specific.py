#!/usr/bin/env python3
"""
Update a single README section from the command line.

Consolidates update_weather_only.py, update_stocks_only.py, and
update_hackernews_only.py into one entry point so you don't need
three separate files for the same pattern.

Usage
-----
    python -m scripts.update_specific weather
    python -m scripts.update_specific stocks
    python -m scripts.update_specific hackernews

GitHub Actions can call this instead of the individual scripts:

    - run: python -m scripts.update_specific weather
"""

import logging
import sys

from .update_weather_only import WeatherUpdateScript
from .update_stocks_only import StocksUpdateScript
from .update_hackernews_only import HackerNewsUpdateScript

SECTION_MAP: dict[str, type] = {
    "weather": WeatherUpdateScript,
    "stocks": StocksUpdateScript,
    "hackernews": HackerNewsUpdateScript,
}


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    if len(sys.argv) != 2 or sys.argv[1] not in SECTION_MAP:
        valid = ", ".join(SECTION_MAP)
        print(f"Usage: python -m scripts.update_specific <section>")
        print(f"Valid sections: {valid}")
        sys.exit(1)

    section = sys.argv[1]
    SECTION_MAP[section]().run()


if __name__ == "__main__":
    main()
