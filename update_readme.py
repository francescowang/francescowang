#!/usr/bin/env python3
"""
Dynamic GitHub Profile README Generator.

Fetches live data from free APIs and renders the Jinja2 template into README.md.
All provider calls are executed concurrently to minimise total runtime.
Runs daily via GitHub Actions.

"""

import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader

from providers.weather import get_weather
from providers.stocks import get_stocks
from providers.hackernews import get_hackernews_top10
from providers.daily_content import (
    get_philosopher_quote,
    get_fun_fact,
    get_word_of_the_day,
    get_on_this_day,
    get_moon_phase,
    get_days_until_events,
)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(script_dir))
    template = env.get_template("TEMPLATE.md")
    output_path = os.path.join(script_dir, "README.md")

    now = datetime.now(timezone.utc)

    print("🚀 Fetching all provider data concurrently...")
    with ThreadPoolExecutor(max_workers=7) as executor:
        f_weather = executor.submit(get_weather)
        f_stocks = executor.submit(get_stocks)
        f_hackernews = executor.submit(get_hackernews_top10)
        f_quote = executor.submit(get_philosopher_quote)
        f_fact = executor.submit(get_fun_fact)
        f_word = executor.submit(get_word_of_the_day, now)
        f_history = executor.submit(get_on_this_day, now)

        weather_rows = f_weather.result()
        stock_rows = f_stocks.result()
        hackernews_rows = f_hackernews.result()
        quote = f_quote.result()
        fact = f_fact.result()
        word = f_word.result()
        history = f_history.result()

    # Local computations — no I/O, no need for threads
    moon = get_moon_phase(now)
    countdowns = get_days_until_events(now)

    context = {
        "date": now.strftime("%A, %d %B %Y"),
        "weather_rows": weather_rows,
        "weather_update_time": now.strftime("%d %b %Y, %H:%M UTC"),
        "stock_rows": stock_rows,
        "stock_update_time": now.strftime("%d %b %Y, %H:%M UTC"),
        "hackernews_rows": hackernews_rows,
        "hackernews_update_time": now.strftime("%d %b %Y, %H:%M UTC"),
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

    print("📝 Rendering README with Jinja2...")
    readme = template.render(context)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"✅ README.md updated at {now.strftime('%Y-%m-%d %H:%M UTC')}")


if __name__ == "__main__":
    main()
