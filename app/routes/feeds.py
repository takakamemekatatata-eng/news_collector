# app/routes/feeds.py

from flask import Blueprint, render_template, request, redirect, url_for
from app.services.feed_service import get_feeds, fetch_and_store_all

bp = Blueprint("feeds", __name__, url_prefix="/feeds")

@bp.route("/", methods=["GET"])
def index():
    # フィードの絞り込み（例：?site=ITmedia）
    site = request.args.get("site")

    # feeds一覧を取得
    feeds = get_feeds(site=site)

    return render_template("feeds.html", feeds=feeds, site=site)


@bp.route("/fetch", methods=["POST"])
def fetch_and_save():
    fetch_and_store_all()

    # ソート・検索を維持して戻る
    sort = request.args.get("sort", "new")
    q = request.args.get("q", "")

    return redirect(url_for("articles.index", sort=sort, q=q))
