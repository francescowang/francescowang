"""
Regex patterns for README section updates.

Each pattern is designed to match a specific section in the README
for surgical updates without affecting other content.
"""

# WEATHER SECTION PATTERNS
# Matches from first <details open> through all continent sections to the last </details>
# The header pattern matches the start, and matches everything until before the last closing details tag
WEATHER_SECTION_HEADER = r"<details open>"
# Match the last </details> before the timestamp line
WEATHER_SECTION_END = r"</details>"
WEATHER_TIMESTAMP = r"<sub>🕐 Last weather update: <b>.*?</b> · Data from OpenWeatherMap</sub>"

# STOCKS SECTION PATTERNS
STOCKS_SECTION_HEADER = r"<tr>\s*<th>📊 Ticker</th>.*?</tr>"
STOCKS_SECTION_END = r"</table>\s*\n\n<sub>🕐 Last market update:"
STOCKS_TIMESTAMP = r"<sub>🕐 Last market update: <b>.*?</b>"

# HACKER NEWS SECTION PATTERNS
HACKERNEWS_SECTION_HEADER = r"<tr>\s*<th>📌 Rank</th>.*?</tr>"
HACKERNEWS_SECTION_END = r"</table>\s*\n\n<sub>🕐 Last HN update:"
HACKERNEWS_TIMESTAMP = r"<sub>🕐 Last HN update: <b>.*?</b></sub>"
