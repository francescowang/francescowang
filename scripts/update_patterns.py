"""
Regex patterns for README section updates.

How section replacement works
-------------------------------
UpdateScriptBase.update_section() builds a pattern of the form:

    ({SECTION_HEADER_PATTERN}\\n)(.*?)(\\n{SECTION_END_PATTERN})

Using re.DOTALL so '.' matches newlines too. The replacement keeps group 1
(the header line) and group 3 (the closing marker) while swapping group 2
(the body) for fresh data.

Pattern design rules
---------------------
- HEADER patterns must be unique enough not to match other sections.
- END patterns are intentionally narrow — they include distinctive text from
  the timestamp line so a plain </table> or </details> in another section
  can't accidentally anchor the wrong replacement.
- TIMESTAMP patterns match the full inline tag that wraps the date so the
  whole tag (not just the date) gets swapped on each update.


WEATHER SECTION
---------------
Source structure in README (simplified):

    <details open>              ← HEADER matches here
    <summary><b>Europe</b>...
    ...continent table rows...
    </details>                  ← END matches here (last one before timestamp)

    <sub>🕐 Last weather update: <b>26 Apr 2025, 09:00 UTC</b> · Data from OpenWeatherMap</sub>
    ↑ TIMESTAMP pattern matches this whole tag


STOCKS SECTION
--------------
Source structure in README (simplified):

    <tr>
    <th>📊 Ticker</th>...       ← HEADER matches this multiline <tr>...</tr>
    </tr>
    <tr>...stock rows...</tr>
    </table>

    <sub>🕐 Last market update: <b>26 Apr 2025</b>...</sub>
    ↑ END matches '</table>\\n\\n<sub>🕐 Last market update:'
    ↑ TIMESTAMP matches '<sub>🕐 Last market update: <b>.*?</b>'


HACKER NEWS SECTION
-------------------
Source structure in README (simplified):

    <tr>
    <th>📌 Rank</th>...         ← HEADER matches this multiline <tr>...</tr>
    </tr>
    <tr>...story rows...</tr>
    </table>

    <sub>🕐 Last HN update: <b>26 Apr 2025</b></sub>
    ↑ END matches '</table>\\n\\n<sub>🕐 Last HN update:'
    ↑ TIMESTAMP matches '<sub>🕐 Last HN update: <b>.*?</b></sub>'
"""

# WEATHER SECTION PATTERNS
# Matches the opening <details open> tag that starts each continent block.
# re.DOTALL lets (.*?) in update_section span across all continent <details> blocks
# up to the FINAL </details> before the timestamp.
WEATHER_SECTION_HEADER = r"<details open>"
WEATHER_SECTION_END = r"</details>"
WEATHER_TIMESTAMP = r"<sub>🕐 Last weather update: <b>.*?</b> · Data from OpenWeatherMap</sub>"

# STOCKS SECTION PATTERNS
# Matches the multiline header row that contains the "📊 Ticker" column heading.
# .*? with re.DOTALL spans any extra <th> columns between Ticker and </tr>.
STOCKS_SECTION_HEADER = r"<tr>\s*<th>📊 Ticker</th>.*?</tr>"
# Includes the start of the timestamp sub-tag to prevent matching other </table> tags.
STOCKS_SECTION_END = r"</table>\s*\n\n<sub>🕐 Last market update:"
STOCKS_TIMESTAMP = r"<sub>🕐 Last market update: <b>.*?</b>"

# HACKER NEWS SECTION PATTERNS
# Matches the multiline header row that contains the "📌 Rank" column heading.
HACKERNEWS_SECTION_HEADER = r"<tr>\s*<th>📌 Rank</th>.*?</tr>"
# Includes the start of the timestamp sub-tag to prevent matching other </table> tags.
HACKERNEWS_SECTION_END = r"</table>\s*\n\n<sub>🕐 Last HN update:"
HACKERNEWS_TIMESTAMP = r"<sub>🕐 Last HN update: <b>.*?</b></sub>"
