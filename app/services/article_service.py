# app/services/article_service.py

from database.connection import get_connection, get_db
from datetime import datetime, timezone
from app.utils.date_utils import parse_date_safe

def get_sorted_articles(q, sort, feeds=None, fav=False):
    db = get_db()
    cursor = db.cursor()

    base_query = """
        SELECT 
            articles.*,
            feeds.name AS feed_name,
            COALESCE(article_status.read, 0) AS is_read,
            COALESCE(article_status.favorite, 0) AS is_favorite
        FROM articles
        JOIN feeds ON articles.feed_id = feeds.id
        LEFT JOIN article_status ON articles.id = article_status.article_id
        WHERE 1=1
    """

    params = []

    # キーワード検索
    if q:
        base_query += " AND (articles.title LIKE ? OR articles.description LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]

    # feed 絞り込み
    if feeds:
        base_query += " AND feed_id IN ({})".format(",".join("?" * len(feeds)))
        params += feeds

    # ★ お気に入りフィルタ
    if fav:
        base_query += " AND article_status.favorite = 1"

    # ソート
    ORDER_BY_MAP = {
    "new": "published_at DESC",
    "old": "published_at ASC",
    "title": "title ASC",
    }
    base_query += f" ORDER BY {ORDER_BY_MAP.get(sort, 'published_at DESC')}"

    cursor.execute(base_query, params)
    return cursor.fetchall()

def save_article(article):
    """記事を articles テーブルに保存する"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO articles
        (feed_id, title, link, description, content, published_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        article["feed_id"],
        article["title"],
        article["link"],
        article["description"],
        article["content"],
        article["published_at"],
        article["created_at"],
    ))

    conn.commit()
    conn.close()
