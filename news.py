import os
import datetime
import feedparser
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.local', override=True)
load_dotenv(dotenv_path='.env', override=False)

news_url = os.environ.get('FFXIV_NEWS_FEED')

feed = feedparser.parse(news_url)

#only get the news if the match the date of today
today = datetime.datetime.now().date()
#change today to yesterday FOR TESTING PURPOSES
today = today - datetime.timedelta(days=1)
#format toda to match the format of the feed 2024-05-14T08:45:00Z
today = today.strftime("%Y-%m-%d")
today_news = None
# Loop through each entry in the feed
for entry in feed.entries:
    if today not in entry.published:
        continue
    print(entry.title)
    print(entry.link)
    print(entry.published)
    print(entry.content[0].value)
    print("\n")
    today_news = {
        "title": entry.title,
        "link": entry.link,
        "published": entry.published,
        "content": entry.content[0].value
    }

# if today_news:
#     return today_news