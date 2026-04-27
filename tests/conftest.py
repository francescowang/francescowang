"""
Shared pytest fixtures for all test modules.
"""

import pytest


# ---------------------------------------------------------------------------
# Sample README content that matches the real regex patterns
# ---------------------------------------------------------------------------

SAMPLE_README = """\
# Francesco Wang

## 🌤️ Live Weather

<table>
<tr><th>🏙️ City</th><th>🌡️ Temp</th><th>💧 Humidity</th><th>🌬️ Wind</th><th>🌤️ Conditions</th></tr>
<tr><td>🇬🇧 <b>London</b></td><td>15°C</td><td>80%</td><td>20 km/h</td><td>☀️ Clear sky</td></tr>
</table>

<sub>🕐 Last weather update: <b>26 Apr 2025, 09:00 UTC</b></sub>

## 📈 Live Markets

<table>
<tr><th>📊 Ticker</th><th>💵 Price</th><th>📈 Change</th><th>% Change</th><th>📅 Date</th></tr>
<tr><td><b>SPY</b></td><td>450.00</td><td>🟢 +1.00</td><td>+0.22%</td><td>26 Apr 2025</td></tr>
</table>

<sub>🕐 Last market update: <b>26 Apr 2025, 09:00 UTC</b>

## 📰 Hacker News Top 10

<table>
<tr><th>📌 Rank</th><th>📰 Story</th><th>⬆️ Score</th><th>💬 Comments</th></tr>
| 1. | [Old Story](https://example.com) | 50 👍 | 10 💬 |
</table>

<sub>🕐 Last HN update: <b>26 Apr 2025, 09:00 UTC</b></sub>
"""


@pytest.fixture
def sample_readme() -> str:
    return SAMPLE_README


@pytest.fixture
def temp_readme_path(tmp_path, sample_readme) -> str:
    """Write SAMPLE_README to a temp file and return its path."""
    readme_file = tmp_path / "README.md"
    readme_file.write_text(sample_readme, encoding="utf-8")
    return str(readme_file)
