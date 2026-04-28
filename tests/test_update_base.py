"""
Tests for UpdateScriptBase — the abstract base class that drives all
section-specific README update scripts.
"""

import pytest
from datetime import datetime, timezone

from scripts.update_base import UpdateScriptBase
from scripts.update_patterns import (
    WEATHER_SECTION_HEADER,
    WEATHER_SECTION_END,
    WEATHER_TIMESTAMP,
    STOCKS_SECTION_HEADER,
    STOCKS_SECTION_END,
    STOCKS_TIMESTAMP,
)


# ---------------------------------------------------------------------------
# Concrete test double for UpdateScriptBase
# ---------------------------------------------------------------------------

# New weather row with continent structure
NEW_WEATHER_ROW = (
    "<details open>\n<summary><b>Europe</b></summary>\n\n<table>\n"
    "<tr>\n<th>🏙️ City</th>\n<th>🌡️ Temp</th>\n<th>💧 Humidity</th>\n<th>🌬️ Wind</th>\n<th>☁️ Conditions</th>\n</tr>\n"
    "<tr><td>🇬🇧 <b>London</b></td><td>25°C</td><td>60%</td><td>10 km/h</td><td>☀️ Sunny</td></tr>\n"
    "</table>\n\n</details>\n\n"
    "<details open>\n<summary><b>Asia</b></summary>\n\n<table>\n"
    "<tr>\n<th>🏙️ City</th>\n<th>🌡️ Temp</th>\n<th>💧 Humidity</th>\n<th>🌬️ Wind</th>\n<th>☁️ Conditions</th>\n</tr>\n"
    "<tr><td>🇨🇳 <b>Beijing</b></td><td>20°C</td><td>40%</td><td>8 km/h</td><td>☀️ Clear</td></tr>\n"
    "</table>\n\n</details>"
)

NEW_STOCKS_ROW = (
    "<tr><td><b>SPY</b></td><td>500.00</td>"
    "<td>🟢 +10.00</td><td>+2.04%</td><td>27 Apr 2025</td></tr>"
)


class ConcreteWeatherScript(UpdateScriptBase):
    SECTION_HEADER_PATTERN = WEATHER_SECTION_HEADER
    SECTION_END_PATTERN = WEATHER_SECTION_END
    TIMESTAMP_PATTERN = WEATHER_TIMESTAMP

    def fetch_data(self) -> str:
        return NEW_WEATHER_ROW

    def get_section_name(self) -> str:
        return "weather"


class ConcreteStocksScript(UpdateScriptBase):
    SECTION_HEADER_PATTERN = STOCKS_SECTION_HEADER
    SECTION_END_PATTERN = STOCKS_SECTION_END
    TIMESTAMP_PATTERN = STOCKS_TIMESTAMP

    def fetch_data(self) -> str:
        return NEW_STOCKS_ROW

    def get_section_name(self) -> str:
        return "stocks"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestReadWrite:
    def test_read_readme_returns_content(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        content = script.read_readme()
        assert "Francesco Wang" in content

    def test_read_readme_preserves_unicode(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        content = script.read_readme()
        assert "🇬🇧" in content

    def test_write_readme_overwrites_file(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        script.write_readme("New content")
        assert script.read_readme() == "New content"

    def test_write_readme_preserves_unicode(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        script.write_readme("☀️ 日本語")
        assert script.read_readme() == "☀️ 日本語"


class TestUpdateSection:
    def test_replaces_weather_row(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        readme = script.read_readme()
        updated = script.update_section(readme, NEW_WEATHER_ROW)
        assert "25°C" in updated

    def test_removes_old_weather_row(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        readme = script.read_readme()
        updated = script.update_section(readme, NEW_WEATHER_ROW)
        assert "15°C" not in updated

    def test_replaces_stocks_row(self, temp_readme_path):
        script = ConcreteStocksScript(readme_path=temp_readme_path)
        readme = script.read_readme()
        updated = script.update_section(readme, NEW_STOCKS_ROW)
        assert "500.00" in updated

    def test_removes_old_stocks_row(self, temp_readme_path):
        script = ConcreteStocksScript(readme_path=temp_readme_path)
        readme = script.read_readme()
        updated = script.update_section(readme, NEW_STOCKS_ROW)
        assert "450.00" not in updated

    def test_does_not_corrupt_other_sections(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        readme = script.read_readme()
        updated = script.update_section(readme, NEW_WEATHER_ROW)
        # Stocks section must be untouched
        assert "450.00" in updated

    def test_returns_original_when_no_match(self, temp_readme_path, capsys):
        """Warns and returns original content when the pattern finds nothing."""
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        updated = script.update_section("no matching content here", "new data")
        assert updated == "no matching content here"
        captured = capsys.readouterr()
        assert "Warning" in captured.out or "warning" in captured.out.lower()


class TestUpdateTimestamp:
    def test_replaces_weather_timestamp(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        readme = script.read_readme()
        updated = script.update_timestamp(readme)
        # Old weather timestamp tag should be replaced (other sections may still have the date)
        assert "Last weather update: <b>26 Apr 2025" not in updated

    def test_inserts_current_date_in_weather_timestamp(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        readme = script.read_readme()
        updated = script.update_timestamp(readme)
        expected_date = script.now.strftime("%d %b %Y")
        assert expected_date in updated

    def test_replaces_stocks_timestamp(self, temp_readme_path):
        script = ConcreteStocksScript(readme_path=temp_readme_path)
        readme = script.read_readme()
        updated = script.update_timestamp(readme)
        expected_date = script.now.strftime("%d %b %Y")
        assert expected_date in updated


class TestRun:
    def test_run_writes_new_content(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        script.run()
        result = script.read_readme()
        assert "25°C" in result

    def test_run_updates_timestamp(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        script.run()
        result = script.read_readme()
        expected_date = script.now.strftime("%d %b %Y")
        assert expected_date in result

    def test_run_preserves_unrelated_sections(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        script.run()
        result = script.read_readme()
        assert "Hacker News" in result


class TestSectionName:
    def test_weather_section_name(self, temp_readme_path):
        script = ConcreteWeatherScript(readme_path=temp_readme_path)
        assert script.get_section_name() == "weather"

    def test_stocks_section_name(self, temp_readme_path):
        script = ConcreteStocksScript(readme_path=temp_readme_path)
        assert script.get_section_name() == "stocks"
