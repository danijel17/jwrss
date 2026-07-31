#!/usr/bin/env python3
"""Generate an unofficial RSS feed for the Croatian JW.org "Novo na stranici" page.

The page renders its list of items server-side inside <div class="whatsNewItems">.
Each item is a <div class="synopsis"> containing:
    <p class="meta pubDate">YYYY-MM-DD</p>
    <p class="contextTitle">CATEGORY</p>
    <h3><a href="...">Title</a></h3>

This is far more reliable than grabbing every <h3> on the page (which also picks
up navigation headings and misses the publish date / category).
"""

from datetime import datetime, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

URL = "https://www.jw.org/hr/sto-je-novo/"
OUTPUT = "jw_hr.xml"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "hr,en;q=0.8",
}


def clean(text):
    return " ".join(text.split()) if text else ""


def parse_items(html):
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one(".whatsNewItems")
    if container is None:
        return []

    items = []
    for syn in container.select("div.synopsis"):
        link_el = syn.select_one("h3 a[href]")
        if not link_el:
            continue

        title = clean(link_el.get_text(" ", strip=True))
        link = urljoin(URL, link_el["href"])

        date_el = syn.select_one(".pubDate")
        published = None
        if date_el:
            raw_date = clean(date_el.get_text())
            try:
                published = datetime.strptime(raw_date, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                published = None

        cat_el = syn.select_one(".contextTitle")
        category = clean(cat_el.get_text()) if cat_el else None

        items.append(
            {
                "title": title,
                "link": link,
                "category": category,
                "published": published,
            }
        )
    return items


def build_feed(items):
    fg = FeedGenerator()
    fg.title("JW.org Hrvatski - Novo na stranici")
    fg.link(href=URL, rel="alternate")
    fg.link(href=URL, rel="self")
    fg.description("Neslužbeni RSS feed za hrvatsku stranicu JW.org (Novo na stranici)")
    fg.language("hr")
    fg.lastBuildDate(datetime.now(timezone.utc))

    # feedgen prepends each entry, so add oldest first to keep newest at the top.
    for item in reversed(items):
        entry = fg.add_entry()
        entry.title(item["title"])
        entry.link(href=item["link"])
        entry.guid(item["link"], permalink=True)
        if item["category"]:
            entry.category(term=item["category"])
        if item["published"]:
            entry.pubDate(item["published"])

    return fg


def main():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or "utf-8"

    items = parse_items(response.text)
    if not items:
        raise SystemExit(
            "Nije pronađen nijedan članak. Struktura stranice se možda promijenila."
        )

    fg = build_feed(items)
    fg.rss_file(OUTPUT, pretty=True)
    print(f"RSS generiran: {OUTPUT} ({len(items)} članaka).")


if __name__ == "__main__":
    main()
