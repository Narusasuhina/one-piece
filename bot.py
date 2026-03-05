import requests
import feedparser
import time
import os

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
RSS_FEED = "https://onepiece.fandom.com/wiki/Special:RecentChanges?feed=rss"
SEEN_FILE = "seen.txt"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        f.write("\n".join(seen))

def check_feed():
    seen = load_seen()
    feed = feedparser.parse(RSS_FEED)
    new_seen = set(seen)

    for entry in feed.entries[:5]:
        if entry.link not in seen:
            message = f"🏴‍☠️ **NEW ONE PIECE UPDATE!!!**\n{entry.title.upper()}\n{entry.link}\n⚓ THE GREAT ERA OF PIRATES CONTINUES!!"
            requests.post(WEBHOOK_URL, json={"content": message})
            new_seen.add(entry.link)
            time.sleep(2)

    save_seen(new_seen)

while True:
    check_feed()
    time.sleep(3600)
```

**Step 4:** Also create a file called `requirements.txt` with this inside:
```
requests
feedparser
