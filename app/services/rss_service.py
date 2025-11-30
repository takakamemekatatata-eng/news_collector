"""
    app/services/rss_service.py
    RSSフィードから記事を取得するサービス層。
"""

import feedparser
from datetime import datetime, timezone
from app.utils.date_utils import parse_date_safe
from app.utils.text_utils import strip_html_tags

# 指定されたフィードリストから記事を取得するジェネレータ
def fetch_rss(feeds):
    for feed_id, name, url in feeds:
        parsed = feedparser.parse(url)

        status = getattr(parsed, "status", None)
        if status is not None and status >= 400:
            print(f"[WARN] Failed to fetch feed ({status}): {url}")
            continue

        for entry in parsed.entries:
            article = extract_article(entry, feed_id)
            if article:
                yield article

# エントリから記事情報を抽出して辞書で返す
def extract_article(entry, feed_id):
    title = entry.get("title", "").strip()
    link = entry.get("link")

    if not link:
        return None  # 保存しても意味ない

    description = entry.get("description", "") or entry.get("summary", "")
    description = strip_html_tags(description)

    content = None
    if "content" in entry and entry.content:
        try:
            content = entry.content[0].get("value", None)
        except Exception:
            content = None

    dt = normalize_published_date(entry)

    return {
        "feed_id": feed_id,
        "title": title,
        "link": link,
        "description": description,
        "content": content,
        "published_at": dt.isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

# published_at を正規化して datetime オブジェクトで返す
def normalize_published_date(entry):
    raw = (
        entry.get("published")
        or entry.get("updated")
        or entry.get("pubDate")
        or entry.get("date")
    )

    if raw:
        dt = parse_date_safe(raw)
        if dt:
            return dt

    # パース不可または空 → 今のUTC
    return datetime.now(timezone.utc)
