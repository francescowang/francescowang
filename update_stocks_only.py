#!/usr/bin/env python3
"""
Update only the stocks section in README.

Runs every 6 hours via GitHub Actions.
Inherits from UpdateScriptBase for common functionality.
"""

from update_base import UpdateScriptBase
from update_patterns import STOCKS_SECTION_HEADER, STOCKS_SECTION_END, STOCKS_TIMESTAMP
from providers.stocks import get_stocks


class StocksUpdateScript(UpdateScriptBase):
    """Update script for stocks section."""

    SECTION_HEADER_PATTERN = STOCKS_SECTION_HEADER
    SECTION_END_PATTERN = STOCKS_SECTION_END
    TIMESTAMP_PATTERN = STOCKS_TIMESTAMP

    def fetch_data(self) -> str:
        """Fetch current stock/ETF data."""
        return get_stocks()

    def get_section_name(self) -> str:
        """Return the section name for logging."""
        return "stocks"


def main():
    """Run the stocks update script."""
    script = StocksUpdateScript()
    script.run()


if __name__ == "__main__":
    main()
