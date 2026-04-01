"""
Daily content providers — quotes, facts, word of the day, history, moon phase, countdowns.

All APIs are free and require no API keys:
  - ZenQuotes:        https://zenquotes.io/
  - Useless Facts:    https://uselessfacts.jsph.pl/
  - Free Dictionary:  https://dictionaryapi.dev/
  - Wikimedia:        https://api.wikimedia.org/wiki/Feed_API/Reference/On_this_day
"""

from datetime import datetime, timezone

from config import INTERESTING_WORDS, MOON_PHASES
from providers.utils import fetch_json, pick_daily


def get_philosopher_quote() -> dict:
    """Fetch quote of the day from ZenQuotes API (free, no key).

    API docs: https://zenquotes.io/
    Rate limit: 5 requests / 30 seconds (plenty for daily cron).
    """
    data = fetch_json("https://zenquotes.io/api/today")
    if data and isinstance(data, list) and len(data) > 0:
        q = data[0].get("q", "")
        a = data[0].get("a", "Unknown")
        if q and a != "zenquotes.io":
            return {"quote": q, "author": a}
    return {"quote": "The only true wisdom is in knowing you know nothing.", "author": "Socrates"}


def get_fun_fact() -> dict:
    """Fetch today's fun fact from Useless Facts API (free, no key).

    API docs: https://uselessfacts.jsph.pl/
    Endpoints: /api/v2/facts/today (daily) or /api/v2/facts/random
    """
    data = fetch_json("https://uselessfacts.jsph.pl/api/v2/facts/today")
    if data and "text" in data:
        return {"emoji": "🧠", "fact": data["text"]}
    data = fetch_json("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
    if data and "text" in data:
        return {"emoji": "🧠", "fact": data["text"]}
    return {"emoji": "🧠", "fact": "Honey never spoils — archaeologists found 3,000-year-old honey still edible."}


def get_word_of_the_day(now: datetime) -> dict:
    """Pick a daily word and fetch its definition from Free Dictionary API (free, no key).

    API docs: https://dictionaryapi.dev/
    Usage:    GET https://api.dictionaryapi.dev/api/v2/entries/en/{word}
    """
    word = pick_daily(INTERESTING_WORDS, now)
    data = fetch_json(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if data and isinstance(data, list) and len(data) > 0:
        entry = data[0]
        word_display = entry.get("word", word).capitalize()
        phonetic = entry.get("phonetic", "")
        if not phonetic:
            for p in entry.get("phonetics", []):
                if p.get("text"):
                    phonetic = p["text"]
                    break
        meanings = entry.get("meanings", [])
        if meanings:
            first = meanings[0]
            pos = first.get("partOfSpeech", "")
            defs = first.get("definitions", [])
            if defs:
                definition = defs[0].get("definition", "")
                example = defs[0].get("example", "")
                return {
                    "word": word_display,
                    "pronunciation": phonetic or "/…/",
                    "type": pos,
                    "meaning": definition,
                    "example": example or f"Today's word is '{word}' — try using it in conversation!",
                }
    return {
        "word": word.capitalize(),
        "pronunciation": "/…/",
        "type": "–",
        "meaning": "Definition temporarily unavailable.",
        "example": f"Look up '{word}' — it's a fascinating word!",
    }


def get_on_this_day(now: datetime) -> dict:
    """Fetch a historical event from Wikimedia On This Day API (free, no key).

    API docs: https://api.wikimedia.org/wiki/Feed_API/Reference/On_this_day
    Usage:    GET /feed/v1/wikipedia/en/onthisday/{type}/{MM}/{DD}
    Types:    selected, events, births, deaths, holidays
    """
    mm = now.strftime("%m")
    dd = now.strftime("%d")
    for endpoint in ("selected", "events"):
        url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/{endpoint}/{mm}/{dd}"
        data = fetch_json(url)
        key = endpoint if endpoint != "events" else "events"
        if data and key in data and len(data[key]) > 0:
            events = data[key]
            event = pick_daily(events, now)
            year = event.get("year", "?")
            text = event.get("text", "Something interesting happened on this day.")
            return {"year": str(year), "emoji": "📜", "event": text}
    return {"year": "?", "emoji": "📜", "event": "Check Wikipedia for events on this day!"}


def get_moon_phase(now: datetime) -> str:
    """Calculate the current moon phase (astronomical formula, not an API)."""
    diff = (now - datetime(2000, 1, 6, tzinfo=timezone.utc)).days
    cycle = 29.53058867
    phase_index = int((diff % cycle) / cycle * 8) % 8
    return MOON_PHASES[phase_index]


def get_days_until_events(now: datetime) -> str:
    """Calculate days until fun upcoming events."""
    year = now.year
    events = [
        (datetime(year, 12, 25, tzinfo=timezone.utc), "🎄 Christmas"),
        (datetime(year, 1, 1, tzinfo=timezone.utc), "🎆 New Year"),
        (datetime(year, 10, 31, tzinfo=timezone.utc), "🎃 Halloween"),
        (datetime(year, 3, 14, tzinfo=timezone.utc), "🥧 Pi Day"),
        (datetime(year, 5, 4, tzinfo=timezone.utc), "⚔️ Star Wars Day"),
        (datetime(year, 4, 22, tzinfo=timezone.utc), "🌍 Earth Day"),
    ]
    rows = []
    for event_date, label in events:
        delta = (event_date - now).days
        if delta < 0:
            event_date = event_date.replace(year=year + 1)
            delta = (event_date - now).days
        if delta == 0:
            rows.append(f"| {label} | **🎉 TODAY!** |")
        else:
            bar_len = max(1, min(20, 20 - int(delta / 18.25)))
            bar = "█" * bar_len + "░" * (20 - bar_len)
            rows.append(f"| {label} | `{bar}` **{delta}** days |")
    return "\n".join(rows)
