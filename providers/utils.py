"""
Shared utilities: HTTP fetching and deterministic daily selection.
"""

import json
import hashlib
import urllib.request
import urllib.error
from datetime import datetime


def fetch_json(url: str, timeout: int = 15) -> dict | None:
    """Fetch JSON from a URL, return None on failure."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GitHubProfileBot/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as exc:
        print(f"Failed to fetch {url}: {exc}")
        return None


def daily_seed(now: datetime) -> int:
    """Deterministic seed based on the date so everyone sees the same content."""
    return int(hashlib.md5(now.strftime("%Y-%m-%d").encode()).hexdigest(), 16)


def pick_daily(items: list, now: datetime):
    """Deterministically pick one item per day from a list."""
    seed = daily_seed(now)
    return items[seed % len(items)]
