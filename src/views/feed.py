from datetime import datetime, timezone
from json import dumps

from flask import Response, url_for

from src.blueprints import feed
from src.core.api import v2
from src.core.filters.date import format_date_pretty
from src.core.helpers import get_static_url


@feed.get("/feed.json")
def json():
    prompt = v2.get("prompts/")[0]
    icon = (
        f"{url_for('root.index', _external=True).removesuffix('/')}{get_static_url('favicon.png')}"
    )
    data = {
        "version": "https://www.jsonfeed.org/version/1.1/",
        "title": "#vss365 today",
        "home_page_url": url_for("root.index", _external=True),
        "feed_url": url_for("feed.json", _external=True),
        "description": "Get the latest #vss365 Prompt.",
        "language": "en",
        "icon": icon,
        "favicon": icon,
        "authors": [
            {
                "name": prompt["host"]["handle"],
                "url": prompt["host"]["url"],
            }
        ],
        "items": [
            {
                "id": str(prompt["_id"]),
                "url": url_for("root.view_date", d=prompt["date"], _external=True),
                "external_url": prompt["url"],
                "title": format_date_pretty(prompt["date"]),
                "content_text": prompt["content"],
                "summary": prompt["word"],
                "date_published": (
                    datetime.fromisoformat(prompt["date_added"])
                    .replace(tzinfo=timezone.utc)
                    .isoformat()
                ),
            }
        ],
    }

    return Response(dumps(data), mimetype="application/feed+json")


# @feed.get("feed.xml")
# def rss():
#     return "feed/feed.xml"
