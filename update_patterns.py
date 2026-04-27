"""
Regex patterns for README section updates.

Each pattern is designed to match a specific section in the README
for surgical updates without affecting other content.
"""

# WEATHER SECTION PATTERNS
WEATHER_SECTION_HEADER = r"<tr><th>🏙️ City</th>.*?</tr>"
WEATHER_SECTION_END = r"</table>\s*\n\n<sub>🕐 Last weather update:"
WEATHER_TIMESTAMP = r"<sub>🕐 Last weather update: <b>.*?</b></sub>"

# STOCKS SECTION PATTERNS
STOCKS_SECTION_HEADER = r"<tr><th>📊 Ticker</th>.*?</tr>"
STOCKS_SECTION_END = r"</table>\s*\n\n<sub>🕐 Last market update:"
STOCKS_TIMESTAMP = r"<sub>🕐 Last market update: <b>.*?</b>"

# HACKER NEWS SECTION PATTERNS
HACKERNEWS_SECTION_HEADER = r"<tr><th>📌 Rank</th>.*?</tr>"
HACKERNEWS_SECTION_END = r"</table>\s*\n\n<sub>🕐 Last HN update:"
HACKERNEWS_TIMESTAMP = r"<sub>🕐 Last HN update: <b>.*?</b></sub>"
