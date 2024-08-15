"""
This module is responsible for getting the news from the FFXIV news feed 
and return the news for today.
"""
import os
import datetime
import feedparser
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.local', override=True)
load_dotenv(dotenv_path='.env', override=False)

NEWS_URL = os.environ.get('FFXIV_NEWS_FEED')

@staticmethod
async def get_news_from_xml():
    """Get the news from the FFXIV news feed and return the news for today."""
    feed = feedparser.parse(NEWS_URL)

    #only get the news if the match the date and hour of today
    today = datetime.datetime.now()
    today = today.strftime('%Y-%m-%dT%H:%M')

    # #FOR TESTING PURPOSES
    # today = '2024-05-14T08:45'

    today_news = None
    # Loop through each entry in the feed
    for entry in feed.entries:
        if today not in entry.published:
            continue
        today_news = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "content": entry.content[0].value
        }

    if today_news:
        return today_news
    return None
