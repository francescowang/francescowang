#!/usr/bin/env python3
"""
Update only the Hacker News section in README.

Runs every 12 hours via GitHub Actions.
Inherits from UpdateScriptBase for common functionality.
"""

import logging

from .update_base import UpdateScriptBase
from .update_patterns import HACKERNEWS_SECTION_HEADER, HACKERNEWS_SECTION_END, HACKERNEWS_TIMESTAMP
from providers.hackernews import get_hackernews_top10


class HackerNewsUpdateScript(UpdateScriptBase):
    """Update script for Hacker News section."""

    SECTION_HEADER_PATTERN = HACKERNEWS_SECTION_HEADER
    SECTION_END_PATTERN = HACKERNEWS_SECTION_END
    TIMESTAMP_PATTERN = HACKERNEWS_TIMESTAMP

    def fetch_data(self) -> str:
        """Fetch top 10 Hacker News stories."""
        return get_hackernews_top10()

    def get_section_name(self) -> str:
        """Return the section name for logging."""
        return "hackernews"


def main():
    """Run the Hacker News update script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    script = HackerNewsUpdateScript()
    script.run()


if __name__ == "__main__":
    main()
