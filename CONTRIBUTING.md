# Contributing Guide

This project auto-generates a GitHub profile README from live APIs. Below is everything you need to make a change.

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the full README update
python -m scripts.update_readme

# Update only one section
python -m scripts.update_specific weather
python -m scripts.update_specific stocks
python -m scripts.update_specific hackernews
```

## Running Tests

```bash
PYTHONPATH=. python -m pytest tests/ -v
```

All tests are offline — every network call is mocked. A passing test run requires **zero** internet access.

---

## Adding a City

Edit `providers/config.py` and add an entry to the relevant continent:

```python
CITIES = {
    "Europe": {
        "Rome": {"lat": 41.90, "lon": 12.50, "flag": "🇮🇹"},
        # ↑ city name   lat/lon (decimal degrees)  country flag emoji
    },
}
```

Lat/lon can be found on [latlong.net](https://www.latlong.net/). The `flag` field is a country-flag emoji.  
No code changes are required — the weather provider reads `CITIES` on every run.

## Adding an ETF / Stock

Edit the `ETFS` list in `providers/config.py`:

```python
ETFS = ["VUAG.L", "VWRL.L", "SPY", "QQQ", "ARKK", "VTI", "IWDA.AS"]
#                                                              ↑ new ticker
```

Use any ticker symbol recognised by Yahoo Finance.

---

## Adding a New Provider

All providers follow the same interface. Copy this skeleton:

```python
# providers/my_provider.py
import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_my_data() -> str:
    """Fetch data and return HTML <tr> rows (or other formatted string).

    Returns:
        HTML string ready to be injected into the README template.
        Must never raise — return a fallback string on any error.
    """
    try:
        # ... fetch from API ...
        return "<tr><td>...</td></tr>"
    except Exception as exc:
        logger.warning("Failed to fetch my data: %s", exc)
        return "<tr><td>Data unavailable</td></tr>"
```

Then:
1. Call your function in `scripts/update_readme.py` (inside the `ThreadPoolExecutor` block).
2. Pass the result to the Jinja2 context dict.
3. Add the placeholder `{{ my_data_rows }}` to `TEMPLATE.md`.
4. Write tests in `tests/test_providers.py` — mock all network calls.

---

## Provider Interface Contract

| Rule | Reason |
|------|--------|
| Return a `str` | Template expects a string |
| Never raise | A single failure must not crash the whole README update |
| Mock-friendly | All HTTP calls should be injectable for tests |
| Fallback content | Always return a meaningful fallback on API failure |

---

## Regex Pattern Updates

If you change the README structure (add/remove columns, rename sections), you may need to update the regex patterns in `scripts/update_patterns.py`. See the detailed comments at the top of that file for how each pattern works and what it must match.

Run `pytest tests/test_patterns.py -v` after any pattern change to verify correctness.

---

## Project Layout

```
providers/
  config.py           — Centralized config (CITIES, ETFS, etc.)
  weather.py          — Open-Meteo weather fetcher
  stocks.py           — Yahoo Finance ETF fetcher
  hackernews.py       — Hacker News top-10 fetcher
  daily_content.py    — Quote, fact, word, history, moon phase
  utils.py            — Shared HTTP + daily-seed utilities

scripts/
  update_readme.py    — Full README regeneration (daily cron)
  update_specific.py  — Single-section CLI update
  update_weather_only.py   — Individual section scripts
  update_stocks_only.py    —   (kept for backward compatibility)
  update_hackernews_only.py —  (kept for backward compatibility)
  update_base.py      — Abstract base for section updates
  update_patterns.py  — Regex patterns for section replacement

tests/
  conftest.py         — Shared fixtures (sample README, temp file)
  test_providers.py   — Provider unit tests
  test_patterns.py    — Regex pattern tests
  test_update_base.py — UpdateScriptBase tests

TEMPLATE.md           — Jinja2 template; edit this to change README layout
```
