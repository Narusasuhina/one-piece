import requests
import feedparser
import time
import os

# === CONFIG ===
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
RSS_FEED = "https://onepiece.fandom.com/wiki/Special:RecentChanges?feed=rss"
SEEN_FILE = "seen.txt"
CHECK_INTERVAL = 3600  # seconds between checks (1 hour)

# === LOAD AND SAVE SEEN LINKS ===
def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(seen))

# === CHECK RSS FEED AND POST EMBEDS ===
def check_feed():
    seen = load_seen()
    feed = feedparser.parse(RSS_FEED)
    new_seen = set(seen)

    for entry in feed.entries[:5]:  # Only check the latest 5 entries
        if entry.link not in seen:
            embed = {
                "title": entry.title.upper(),
                "url": entry.link,
                "description": "⚓ THE GREAT ERA OF PIRATES CONTINUES!!",
                "color": 0xFF0000,  # Red color for the embed
                "footer": {"text": "One Piece Wiki Updates 🏴‍☠️"}
            }
            payload = {"embeds": [embed]}

            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code != 204:
                    print(f"Failed to send webhook: {response.status_code} - {response.text}")
            except Exception as e:
                print("Error sending webhook:", e)

            new_seen.add(entry.link)
            time.sleep(2)  # avoid hitting rate limits

    save_seen(new_seen)

# === MAIN LOOP ===
if __name__ == "__main__":
    print("🚀 One Piece RSS Bot started!")
    while True:
        try:
            check_feed()
        except Exception as e:
            print("Error checking feed:", e)
        time.sleep(CHECK_INTERVAL)
