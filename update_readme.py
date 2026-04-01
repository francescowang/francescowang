#!/usr/bin/env python3
"""
Dynamic GitHub Profile README Generator.

Fetches live data from free APIs and renders the Mustache template into README.md.
Runs daily via GitHub Actions.

"""

import os
from datetime import datetime, timezone

from providers.weather import get_weather
from providers.stocks import get_stocks
from providers.daily_content import (
    get_philosopher_quote,
    get_fun_fact,
    get_word_of_the_day,
    get_on_this_day,
    get_moon_phase,
    get_days_until_events,
)


def render_template(template: str, context: dict[str, str]) -> str:
    """Simple Mustache-style {{variable}} replacement."""
    result = template
    for key, value in context.items():
        result = result.replace("{{" + key + "}}", value)
    return result


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "TEMPLATE.md")
    output_path = os.path.join(script_dir, "README.md")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    now = datetime.now(timezone.utc)

    print("🌤️  Fetching weather data...")
    weather_rows = get_weather()

    print("📈 Fetching stock data...")
    stock_rows = get_stocks()

    print("🧠 Generating daily content...")
    quote = get_philosopher_quote()
    fact = get_fun_fact()
    word = get_word_of_the_day(now)
    history = get_on_this_day(now)
    moon = get_moon_phase(now)
    countdowns = get_days_until_events(now)

    context = {
        "date": now.strftime("%A,_%d_%B_%Y").replace("_", " "),
        "weather_rows": weather_rows,
        "weather_update_time": now.strftime("%d %b %Y, %H:%M UTC"),
        "stock_rows": stock_rows,
        "stock_update_time": now.strftime("%d %b %Y, %H:%M UTC"),
        "philosopher_quote": quote["quote"],
        "philosopher_author": quote["author"],
        "fun_fact_emoji": fact["emoji"],
        "fun_fact": fact["fact"],
        "word": word["word"],
        "word_pronunciation": word["pronunciation"],
        "word_type": word["type"],
        "word_meaning": word["meaning"],
        "word_example": word["example"],
        "history_year": str(history["year"]),
        "history_emoji": history["emoji"],
        "history_event": history["event"],
        "today_month_day": now.strftime("%B %d"),
        "moon_phase": moon,
        "countdowns": countdowns,
    }

    print("📝 Rendering README...")
    readme = render_template(template, context)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"✅ README.md updated at {now.strftime('%Y-%m-%d %H:%M UTC')}")


if __name__ == "__main__":
    main()
