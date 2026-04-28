"""
Tests for provider modules — focuses on fallback behaviour and data shaping.
All network calls are mocked so tests run offline and deterministically.
"""

import re
import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Hacker News provider
# ---------------------------------------------------------------------------

class TestHackerNewsProvider:
    def test_returns_fallback_on_connection_error(self):
        from providers.hackernews import get_hackernews_top10
        with patch("providers.hackernews.requests.get", side_effect=ConnectionError("down")):
            result = get_hackernews_top10()
        assert "Unable to fetch Hacker News stories" in result

    def test_fallback_is_valid_html_row(self):
        from providers.hackernews import get_hackernews_top10
        with patch("providers.hackernews.requests.get", side_effect=Exception("fail")):
            result = get_hackernews_top10()
        assert result.startswith("<tr>")

    def test_title_truncated_when_over_70_chars(self):
        from providers.hackernews import get_hackernews_top10

        long_title = "A" * 80

        mock_ids = MagicMock()
        mock_ids.json.return_value = [42]
        mock_ids.raise_for_status.return_value = None

        mock_story = MagicMock()
        mock_story.json.return_value = {
            "title": long_title,
            "score": 100,
            "descendants": 20,
            "url": "https://example.com",
        }
        mock_story.raise_for_status.return_value = None

        with patch("providers.hackernews.requests.get", side_effect=[mock_ids, mock_story]):
            result = get_hackernews_top10()

        assert "..." in result
        match = re.search(r"<a href='[^']+'>(.+?)</a>", result)
        assert match and len(match.group(1)) <= 70

    def test_title_not_truncated_when_under_70_chars(self):
        from providers.hackernews import get_hackernews_top10

        short_title = "Short title"

        mock_ids = MagicMock()
        mock_ids.json.return_value = [1]
        mock_ids.raise_for_status.return_value = None

        mock_story = MagicMock()
        mock_story.json.return_value = {
            "title": short_title,
            "score": 50,
            "descendants": 5,
            "url": "https://example.com",
        }
        mock_story.raise_for_status.return_value = None

        with patch("providers.hackernews.requests.get", side_effect=[mock_ids, mock_story]):
            result = get_hackernews_top10()

        assert "..." not in result
        assert short_title in result
        assert result.startswith("<tr>")

    def test_output_contains_score_and_comments(self):
        from providers.hackernews import get_hackernews_top10

        mock_ids = MagicMock()
        mock_ids.json.return_value = [7]
        mock_ids.raise_for_status.return_value = None

        mock_story = MagicMock()
        mock_story.json.return_value = {
            "title": "Test Story",
            "score": 999,
            "descendants": 42,
            "url": "https://example.com",
        }
        mock_story.raise_for_status.return_value = None

        with patch("providers.hackernews.requests.get", side_effect=[mock_ids, mock_story]):
            result = get_hackernews_top10()

        assert "999" in result
        assert "42" in result
        assert result.startswith("<tr>")


# ---------------------------------------------------------------------------
# Weather provider
# ---------------------------------------------------------------------------

class TestWeatherProvider:
    def test_returns_unavailable_row_on_fetch_failure(self):
        from providers.weather import get_weather
        with patch("providers.weather.fetch_json", return_value=None):
            result = get_weather()
        assert "Data unavailable" in result

    def test_result_contains_london_flag(self):
        from providers.weather import get_weather
        with patch("providers.weather.fetch_json", return_value=None):
            result = get_weather()
        assert "🇬🇧" in result  # London

    def test_result_contains_all_city_flags(self):
        """Test that result contains country flags for cities in all continents."""
        from providers.weather import get_weather
        with patch("providers.weather.fetch_json", return_value=None):
            result = get_weather()
        # Check that we have at least one city from major regions
        assert "London" in result
        assert "Beijing" in result
        assert "New York" in result
        assert "São Paulo" in result
        assert "Sydney" in result
        assert "Cape Town" in result
        # Verify we have multiple continent sections
        assert result.count("<details") >= 6

    def test_formats_temperature_when_data_available(self):
        from providers.weather import get_weather
        mock_data = {
            "current": {
                "temperature_2m": 18.5,
                "relative_humidity_2m": 75,
                "wind_speed_10m": 12.0,
                "weather_code": 0,
            }
        }
        with patch("providers.weather.fetch_json", return_value=mock_data):
            result = get_weather()
        assert "18.5°C" in result

    def test_result_is_html_table_rows(self):
        from providers.weather import get_weather
        with patch("providers.weather.fetch_json", return_value=None):
            result = get_weather()
        assert "<tr>" in result
        assert "</tr>" in result

    def test_result_organized_by_continents(self):
        """Weather data should be organized in continent sections."""
        from providers.weather import get_weather
        with patch("providers.weather.fetch_json", return_value=None):
            result = get_weather()
        expected_continents = ["Europe", "Asia", "North America", "South America", "Africa", "Oceania"]
        for continent in expected_continents:
            assert continent in result
        # Check for details/summary structure
        assert "<details" in result
        assert "<summary>" in result


# ---------------------------------------------------------------------------
# Daily content providers
# ---------------------------------------------------------------------------

class TestPhilosopherQuote:
    def test_returns_fallback_on_api_failure(self):
        from providers.daily_content import get_philosopher_quote
        with patch("providers.daily_content.fetch_json", return_value=None):
            result = get_philosopher_quote()
        assert "quote" in result
        assert "author" in result
        assert len(result["quote"]) > 0

    def test_returns_real_quote_on_success(self):
        from providers.daily_content import get_philosopher_quote
        mock_data = [{"q": "Know thyself.", "a": "Socrates"}]
        with patch("providers.daily_content.fetch_json", return_value=mock_data):
            result = get_philosopher_quote()
        assert result["quote"] == "Know thyself."
        assert result["author"] == "Socrates"

    def test_fallback_excludes_zenquotes_io_author(self):
        """The API sometimes returns 'zenquotes.io' as the author — must use fallback."""
        from providers.daily_content import get_philosopher_quote
        mock_data = [{"q": "Some quote", "a": "zenquotes.io"}]
        with patch("providers.daily_content.fetch_json", return_value=mock_data):
            result = get_philosopher_quote()
        assert result["author"] != "zenquotes.io"


class TestFunFact:
    def test_returns_fallback_on_api_failure(self):
        from providers.daily_content import get_fun_fact
        with patch("providers.daily_content.fetch_json", return_value=None):
            result = get_fun_fact()
        assert "fact" in result
        assert "emoji" in result
        assert len(result["fact"]) > 0

    def test_returns_real_fact_on_success(self):
        from providers.daily_content import get_fun_fact
        mock_data = {"text": "Bananas are berries, but strawberries are not."}
        with patch("providers.daily_content.fetch_json", return_value=mock_data):
            result = get_fun_fact()
        assert "Bananas" in result["fact"]


# ---------------------------------------------------------------------------
# Moon phase (pure computation — no mocking needed)
# ---------------------------------------------------------------------------

class TestMoonPhase:
    def test_returns_a_string(self):
        from providers.daily_content import get_moon_phase
        now = datetime(2025, 4, 27, tzinfo=timezone.utc)
        result = get_moon_phase(now)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_known_phase_emoji(self):
        from providers.daily_content import get_moon_phase
        from providers.config import MOON_PHASES
        now = datetime(2025, 4, 27, tzinfo=timezone.utc)
        result = get_moon_phase(now)
        assert result in MOON_PHASES


# ---------------------------------------------------------------------------
# Event countdown (pure computation — no mocking needed)
# ---------------------------------------------------------------------------

class TestEventCountdown:
    def test_returns_string(self):
        from providers.daily_content import get_days_until_events
        now = datetime(2025, 4, 27, tzinfo=timezone.utc)
        result = get_days_until_events(now)
        assert isinstance(result, str)

    def test_contains_pipe_rows(self):
        from providers.daily_content import get_days_until_events
        now = datetime(2025, 4, 27, tzinfo=timezone.utc)
        result = get_days_until_events(now)
        assert "|" in result

    def test_today_shows_today_label(self):
        from providers.daily_content import get_days_until_events
        # Christmas day
        now = datetime(2025, 12, 25, tzinfo=timezone.utc)
        result = get_days_until_events(now)
        assert "TODAY" in result


# ---------------------------------------------------------------------------
# Edge case tests — HN title length boundary
# ---------------------------------------------------------------------------

class TestHackerNewsTitleBoundary:
    """Verify the 70-char truncation boundary precisely."""

    def _mock_hn(self, title: str):
        """Helper: mock one HN story with the given title."""
        mock_ids = MagicMock()
        mock_ids.json.return_value = [99]
        mock_ids.raise_for_status.return_value = None

        mock_story = MagicMock()
        mock_story.json.return_value = {
            "title": title,
            "score": 1,
            "descendants": 0,
            "url": "https://example.com",
        }
        mock_story.raise_for_status.return_value = None
        return [mock_ids, mock_story]

    def test_title_at_exactly_70_chars_is_not_truncated(self):
        from providers.hackernews import get_hackernews_top10
        title = "X" * 70
        with patch("providers.hackernews.requests.get", side_effect=self._mock_hn(title)):
            result = get_hackernews_top10()
        assert "..." not in result
        assert title in result

    def test_title_at_71_chars_is_truncated(self):
        from providers.hackernews import get_hackernews_top10
        title = "X" * 71
        with patch("providers.hackernews.requests.get", side_effect=self._mock_hn(title)):
            result = get_hackernews_top10()
        assert "..." in result

    def test_title_with_unicode_is_handled(self):
        """Titles with non-ASCII characters should be truncated/kept correctly."""
        from providers.hackernews import get_hackernews_top10
        title = "こんにちは世界 " * 5  # well under 70 chars total
        with patch("providers.hackernews.requests.get", side_effect=self._mock_hn(title)):
            result = get_hackernews_top10()
        assert "<tr>" in result

    def test_individual_story_fetch_failure_is_skipped(self):
        """If a single story detail fetch raises, that story is omitted gracefully."""
        from providers.hackernews import get_hackernews_top10

        mock_ids = MagicMock()
        mock_ids.json.return_value = [1, 2]
        mock_ids.raise_for_status.return_value = None

        mock_good = MagicMock()
        mock_good.json.return_value = {
            "title": "Good Story",
            "score": 50,
            "descendants": 5,
            "url": "https://example.com",
        }
        mock_good.raise_for_status.return_value = None

        # Second story fetch raises
        mock_bad = MagicMock()
        mock_bad.raise_for_status.side_effect = Exception("network error")

        with patch("providers.hackernews.requests.get",
                   side_effect=[mock_ids, mock_good, mock_bad]):
            result = get_hackernews_top10()

        assert "Good Story" in result


# ---------------------------------------------------------------------------
# Edge case tests — weather provider partial data
# ---------------------------------------------------------------------------

class TestWeatherEdgeCases:
    def test_weather_with_missing_individual_fields_shows_na(self):
        """When 'current' exists but a field is missing, get() returns N/A."""
        from providers.weather import get_weather
        # 'current' key present but completely empty — all .get() calls return N/A
        mock_data = {"current": {}}
        with patch("providers.weather.fetch_json", return_value=mock_data):
            result = get_weather()
        assert "N/A" in result

    def test_weather_unicode_city_name_renders(self):
        """São Paulo (non-ASCII city name) must appear in the output."""
        from providers.weather import get_weather
        with patch("providers.weather.fetch_json", return_value=None):
            result = get_weather()
        assert "São Paulo" in result

    def test_weather_output_has_correct_continent_count(self):
        """Exactly 6 continents should be present in the output."""
        from providers.weather import get_weather
        with patch("providers.weather.fetch_json", return_value=None):
            result = get_weather()
        assert result.count("<details") == 6
        assert result.count("</details>") == 6


# ---------------------------------------------------------------------------
# Edge case tests — stocks fallback row count
# ---------------------------------------------------------------------------

class TestStocksEdgeCases:
    def test_fallback_returns_one_row_per_etf(self):
        """_stock_fallback must produce exactly one <tr> per ETF ticker."""
        from providers.stocks import _stock_fallback
        from providers.config import ETFS
        result = _stock_fallback()
        assert result.count("<tr>") == len(ETFS)

    def test_fallback_contains_all_ticker_symbols(self):
        from providers.stocks import _stock_fallback
        from providers.config import ETFS
        result = _stock_fallback()
        for ticker in ETFS:
            assert ticker in result

    def test_get_stocks_returns_fallback_when_yfinance_missing(self):
        """When HAS_YFINANCE is False, get_stocks() returns fallback content."""
        from providers import stocks as stocks_module
        original = stocks_module.HAS_YFINANCE
        try:
            stocks_module.HAS_YFINANCE = False
            result = stocks_module.get_stocks()
            assert "Market data temporarily unavailable" in result
        finally:
            stocks_module.HAS_YFINANCE = original


# ---------------------------------------------------------------------------
# Config validation tests
# ---------------------------------------------------------------------------

class TestConfigValidation:
    def test_valid_config_passes(self):
        """The real config must pass validation without raising."""
        from providers.config import validate_config
        validate_config()  # should not raise

    def test_missing_lat_raises(self):
        from providers.config import validate_config, CITIES
        import providers.config as cfg_module

        bad = {"Europe": {"FakeCity": {"lon": 0.0, "flag": "🏳️"}}}
        original = cfg_module.CITIES
        try:
            cfg_module.CITIES = bad
            with pytest.raises(ValueError, match="missing required fields"):
                validate_config()
        finally:
            cfg_module.CITIES = original

    def test_non_numeric_lat_raises(self):
        from providers.config import validate_config
        import providers.config as cfg_module

        bad = {"Europe": {"FakeCity": {"lat": "not-a-number", "lon": 0.0, "flag": "🏳️"}}}
        original = cfg_module.CITIES
        try:
            cfg_module.CITIES = bad
            with pytest.raises(ValueError, match="lat must be numeric"):
                validate_config()
        finally:
            cfg_module.CITIES = original

    def test_empty_etfs_raises(self):
        from providers.config import validate_config
        import providers.config as cfg_module

        original = cfg_module.ETFS
        try:
            cfg_module.ETFS = []
            with pytest.raises(ValueError, match="ETFS must be"):
                validate_config()
        finally:
            cfg_module.ETFS = original

    def test_empty_continent_raises(self):
        from providers.config import validate_config
        import providers.config as cfg_module

        original = cfg_module.CITIES
        try:
            cfg_module.CITIES = {"EmptyContinent": {}}
            with pytest.raises(ValueError, match="has no cities"):
                validate_config()
        finally:
            cfg_module.CITIES = original

