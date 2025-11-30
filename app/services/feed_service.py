# app/services/feed_service.py

from database.queries.feeds import get_all_feeds
from app.services.rss_service import fetch_rss
from app.services.article_service import save_article
from database.connection import get_db

def get_feeds(site=None):
    """
    feeds テーブルから一覧を取得する
    site が指定されている場合は絞り込み
    """
    db = get_db()
    cursor = db.cursor()

    if site:
        cursor.execute(
            "SELECT id, name, site, url FROM feeds WHERE site = ? ORDER BY name ASC",
            (site,)
        )
    else:
        cursor.execute(
            "SELECT id, name, site, url FROM feeds ORDER BY name ASC"
        )

    rows = cursor.fetchall()

    return [
        {"id": r[0], "name": r[1], "site": r[2], "url": r[3]}
        for r in rows
    ]

def fetch_and_store_all():
    """全フィードからRSSを取得し、記事を保存する。保存数を返す。"""
    feeds = get_all_feeds()
    count = 0

    for article in fetch_rss(feeds):
        save_article(article)
        count += 1

    return count
