"""
Fetch top 10 stories from Hacker News.

Uses the official Hacker News API: https://github.com/HackerNews/API
Stories are fetched concurrently to reduce total latency from ~30s to ~3s.
"""

import json
import logging
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

logger = logging.getLogger(__name__)


def _fetch_story(story_id: int) -> Optional[dict]:
    """Fetch a single story's details from the Hacker News API."""
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        req = urllib.request.Request(story_url, headers={"User-Agent": "GitHubProfileBot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as e:
        logger.warning("Failed to fetch story %s: %s", story_id, e)
        return None


def get_hackernews_top10() -> str:
    """Fetch top 10 Hacker News stories concurrently and format as a table."""
    try:
        # Get top story IDs
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(url, headers={"User-Agent": "GitHubProfileBot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            top_story_ids = json.loads(resp.read().decode())[:10]

        # Fetch all story details concurrently instead of sequentially
        stories: dict[int, Optional[dict]] = {}
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_idx = {
                executor.submit(_fetch_story, sid): (i, sid)
                for i, sid in enumerate(top_story_ids, 1)
            }
            for future in as_completed(future_to_idx):
                idx, _sid = future_to_idx[future]
                try:
                    stories[idx] = future.result()
                except Exception:
                    stories[idx] = None

        rows = []
        for idx in sorted(stories.keys()):
            story = stories[idx]
            if not story:
                continue
            title = story.get("title", "Untitled")
            score = story.get("score", 0)
            comments = story.get("descendants", 0)
            story_id = top_story_ids[idx - 1]
            item_url = story.get("url", f"https://news.ycombinator.com/item?id={story_id}")

            # Shorten long titles
            if len(title) > 70:
                title = title[:67] + "..."

            rows.append(
                f"<tr>"
                f"<td>{idx}.</td>"
                f"<td><a href='{item_url}'>{title}</a></td>"
                f"<td>{score} 👍</td>"
                f"<td>{comments} 💬</td>"
                f"</tr>"
            )

        return "\n".join(rows)

    except Exception as e:
        logger.warning("Error fetching Hacker News: %s", e)
        return "<tr><td colspan='4'><em>Unable to fetch Hacker News stories</em></td></tr>"
