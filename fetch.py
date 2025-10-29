import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import subprocess

ANNOUNCEMENTS_URL = "https://corsidilaurea.uniroma1.it/it/course/33516/announcements"
DATA_FILE = "data.json"
REPO = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def fetch_announcements():
    r = requests.get(ANNOUNCEMENTS_URL, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    announcements = []
    for panel in soup.select("div.panel.panel-default"):
        title_el = panel.select_one("h4.panel-title")
        link_el = panel.select_one("div.panel-heading a[href]")
        if not title_el or not link_el:
            continue

        title = title_el.get_text(strip=True)
        link = link_el["href"]
        if link.startswith("#"):
            link = ANNOUNCEMENTS_URL + link
        elif link.startswith("/"):
            link = "https://corsidilaurea.uniroma1.it" + link

        announcements.append({"title": title, "link": link})

    return announcements

def load_seen():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("announcements", [])

def save_seen(announcements):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"announcements": announcements}, f, indent=2, ensure_ascii=False)

def create_issue(new_items):
    if not new_items:
        return
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    title = f"[AUTO] {len(new_items)} new announcement(s)"
    body = f"Detected new announcement(s) at {timestamp}:\n\n"
    for a in new_items:
        body += f"- [{a['title']}]({a['link']})\n"

    subprocess.run([
        "gh", "issue", "create",
        "--title", title,
        "--body", body
    ], check=True)

def main():
    current = fetch_announcements()
    seen = load_seen()

    seen_links = {a["link"] for a in seen}
    new_items = [a for a in current if a["link"] not in seen_links]

    if new_items:
        print(f"Found {len(new_items)} new announcements.")
        save_seen(seen + new_items)
        create_issue(new_items)
    else:
        print("No new announcements.")

if __name__ == "__main__":
    main()
