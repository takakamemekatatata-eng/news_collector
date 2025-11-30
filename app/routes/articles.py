# app/routes/articles.py

from flask import Blueprint, render_template, request, jsonify
from app.services.article_service import get_sorted_articles
from app.services.feed_service import get_feeds
from database.connection import get_db


bp = Blueprint("articles", __name__)


@bp.route("/")
def index():
    q = request.args.get("q", "")
    sort = request.args.get("sort", "new")
    feeds = request.args.getlist("feed")
    feeds = [int(f) for f in feeds if f.isdigit()]

    # お気に入りのみ表示するかどうか
    fav = request.args.get("fav", "0") == "1"

    articles = get_sorted_articles(q, sort, feeds=feeds, fav=fav)
    feeds_list = get_feeds()

    return render_template(
        "index.html",
        articles=articles,
        q=q,
        sort=sort,
        feeds=feeds,
        feeds_list=feeds_list,
        fav=fav,
    )


@bp.route("/favorite/<int:article_id>", methods=["POST"])
def toggle_favorite(article_id):
    """記事のお気に入り状態をトグルする API"""
    db = get_db()
    cur = db.cursor()

    # 現在の値を取得（列名は favorite）
    cur.execute(
        "SELECT favorite FROM article_status WHERE article_id = ?",
        (article_id,),
    )
    row = cur.fetchone()

    # 無ければ新規作成 → お気に入り ON (1)
    if not row:
        cur.execute(
            """
            INSERT INTO article_status (article_id, read, favorite, updated_at)
            VALUES (?, ?, ?, datetime('now'))
            """,
            (article_id, 0, 1),
        )
        db.commit()
        return jsonify({"success": True, "favorite": 1})

    # 既にある場合はトグル
    current_value = row[0]
    new_value = 0 if current_value else 1

    cur.execute(
        """
        UPDATE article_status
        SET favorite = ?, updated_at = datetime('now')
        WHERE article_id = ?
        """,
        (new_value, article_id),
    )

    db.commit()

    return jsonify({"success": True, "favorite": new_value})


@bp.route("/read/<int:article_id>", methods=["POST"])
def mark_as_read(article_id):
    """記事を既読にする API"""
    db = get_db()
    cur = db.cursor()

    # レコードが無ければ新規作成
    cur.execute(
        "SELECT read FROM article_status WHERE article_id = ?",
        (article_id,),
    )
    row = cur.fetchone()

    if not row:
        cur.execute(
            """
            INSERT INTO article_status (article_id, read, favorite, updated_at)
            VALUES (?, 1, 0, datetime('now'))
            """,
            (article_id,),
        )
    else:
        cur.execute(
            """
            UPDATE article_status
            SET read = 1, updated_at = datetime('now')
            WHERE article_id = ?
            """,
            (article_id,),
        )

    db.commit()
    return jsonify({"success": True, "read": 1})
