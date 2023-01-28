from flask import current_app, redirect, url_for

from src.blueprints import feed


@feed.get("/feed.json")
def json():

    return "feed/feed.json"


@feed.get("feed.xml")
def rss():

    return "feed/feed.xml"
