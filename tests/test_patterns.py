"""Tests for update_patterns.py — verifies every regex pattern matches
valid README content and does NOT over-match adjacent sections.
"""

import re
import pytest

from scripts.update_patterns import (
    WEATHER_SECTION_HEADER,
    WEATHER_SECTION_END,
    WEATHER_TIMESTAMP,
    STOCKS_SECTION_HEADER,
    STOCKS_SECTION_END,
    STOCKS_TIMESTAMP,
    HACKERNEWS_SECTION_HEADER,
    HACKERNEWS_SECTION_END,
    HACKERNEWS_TIMESTAMP,
)

FLAGS = re.DOTALL


# ---------------------------------------------------------------------------
# Weather patterns
# ---------------------------------------------------------------------------

class TestWeatherPatterns:
    def test_header_matches_full_row(self):
        html = "<!-- WEATHER START -->"
        assert re.search(WEATHER_SECTION_HEADER, html, FLAGS)

    def test_header_matches_minimal_row(self):
        html = "<!-- WEATHER START -->"
        assert re.search(WEATHER_SECTION_HEADER, html, FLAGS)

    def test_header_does_not_match_stocks_header(self):
        html = "<tr><th>📊 Ticker</th><th>💵 Price</th></tr>"
        assert not re.search(WEATHER_SECTION_HEADER, html, FLAGS)

    def test_end_matches_standard_closing(self):
        text = "</details>\n<!-- WEATHER END -->"
        assert re.search(WEATHER_SECTION_END, text, FLAGS)

    def test_end_does_not_match_stocks_closing(self):
        text = "</table>\n\n<sub>🕐 Last market update:"
        assert not re.search(WEATHER_SECTION_END, text, FLAGS)

    def test_timestamp_matches_full_tag(self):
        text = "<sub>🕐 Last weather update: <b>27 Apr 2025, 09:00 UTC</b> · Data from OpenWeatherMap</sub>"
        assert re.search(WEATHER_TIMESTAMP, text, FLAGS)

    def test_timestamp_does_not_match_stocks_timestamp(self):
        text = "<sub>🕐 Last market update: <b>27 Apr 2025, 09:00 UTC</b> · Data from Yahoo Finance</sub>"
        assert not re.search(WEATHER_TIMESTAMP, text, FLAGS)

    def test_timestamp_does_not_match_hn_timestamp(self):
        text = "<sub>🕐 Last news update: <b>27 Apr 2025, 09:00 UTC</b> · Data from Hacker News</sub>"
        assert not re.search(WEATHER_TIMESTAMP, text, FLAGS)


# ---------------------------------------------------------------------------
# Stocks patterns
# ---------------------------------------------------------------------------

class TestStocksPatterns:
    def test_header_matches_full_row(self):
        html = "<tr><th>📊 Ticker</th><th>💵 Price</th><th>📈 Change</th><th>% Change</th><th>📅 Date</th></tr>"
        assert re.search(STOCKS_SECTION_HEADER, html, FLAGS)

    def test_header_matches_minimal_row(self):
        html = "<tr><th>📊 Ticker</th></tr>"
        assert re.search(STOCKS_SECTION_HEADER, html, FLAGS)

    def test_header_matches_multiline_row(self):
        html = "<tr>\n<th>📊 Ticker</th>\n<th>💰 Price</th>\n</tr>"
        assert re.search(STOCKS_SECTION_HEADER, html, FLAGS)

    def test_header_does_not_match_weather_header(self):
        html = "<tr><th>🏙️ City</th><th>🌡️ Temp</th></tr>"
        assert not re.search(STOCKS_SECTION_HEADER, html, FLAGS)

    def test_end_matches_standard_closing(self):
        text = "</table>\n\n<sub>🕐 Last market update:"
        assert re.search(STOCKS_SECTION_END, text, FLAGS)

    def test_end_does_not_match_weather_closing(self):
        text = "</table>\n\n<sub>🕐 Last weather update:"
        assert not re.search(STOCKS_SECTION_END, text, FLAGS)

    def test_timestamp_matches_partial_tag(self):
        # Stocks timestamp intentionally lacks </sub> in the pattern
        text = "<sub>🕐 Last market update: <b>27 Apr 2025, 09:00 UTC</b>"
        assert re.search(STOCKS_TIMESTAMP, text, FLAGS)

    def test_timestamp_does_not_match_weather_timestamp(self):
        text = "<sub>🕐 Last weather update: <b>27 Apr 2025, 09:00 UTC</b></sub>"
        assert not re.search(STOCKS_TIMESTAMP, text, FLAGS)


# ---------------------------------------------------------------------------
# Hacker News patterns
# ---------------------------------------------------------------------------

class TestHackerNewsPatterns:
    def test_header_matches_full_row(self):
        html = "<tr><th>📌 Rank</th><th>📰 Story</th><th>⬆️ Score</th><th>💬 Comments</th></tr>"
        assert re.search(HACKERNEWS_SECTION_HEADER, html, FLAGS)

    def test_header_matches_minimal_row(self):
        html = "<tr><th>📌 Rank</th></tr>"
        assert re.search(HACKERNEWS_SECTION_HEADER, html, FLAGS)

    def test_header_matches_multiline_row(self):
        html = "<tr>\n<th>📌 Rank</th>\n<th>📖 Story</th>\n</tr>"
        assert re.search(HACKERNEWS_SECTION_HEADER, html, FLAGS)

    def test_header_does_not_match_weather_header(self):
        html = "<tr><th>🏙️ City</th><th>🌡️ Temp</th></tr>"
        assert not re.search(HACKERNEWS_SECTION_HEADER, html, FLAGS)

    def test_header_does_not_match_stocks_header(self):
        html = "<tr><th>📊 Ticker</th><th>💵 Price</th></tr>"
        assert not re.search(HACKERNEWS_SECTION_HEADER, html, FLAGS)

    def test_end_matches_standard_closing(self):
        text = "</table>\n\n<sub>🕐 Last news update:"
        assert re.search(HACKERNEWS_SECTION_END, text, FLAGS)

    def test_end_does_not_match_weather_closing(self):
        text = "</table>\n\n<sub>🕐 Last weather update:"
        assert not re.search(HACKERNEWS_SECTION_END, text, FLAGS)

    def test_timestamp_matches_full_tag(self):
        text = "<sub>🕐 Last news update: <b>27 Apr 2025, 09:00 UTC</b> · Data from Hacker News</sub>"
        assert re.search(HACKERNEWS_TIMESTAMP, text, FLAGS)

    def test_timestamp_does_not_match_weather_timestamp(self):
        text = "<sub>🕐 Last weather update: <b>27 Apr 2025, 09:00 UTC</b></sub>"
        assert not re.search(HACKERNEWS_TIMESTAMP, text, FLAGS)
