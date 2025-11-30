# app/__init__.py

from flask import Flask

from database.schema import create_tables, seed_feeds
from database.connection import DB_PATH, init_app as init_db
from app.filters.date_filters import format_date
from app.routes import register_routes


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # DB の場所を Flask 設定にも共有しておく
    app.config["DB_PATH"] = str(DB_PATH)

    # DB 初期化（テーブル作成・初期データ投入）
    create_tables()
    seed_feeds()

    # Flask のアプリコンテキスト終了時に DB を閉じる
    init_db(app)

    # Jinja2 のテンプレートフィルタ登録
    app.add_template_filter(format_date, "format_date")

    # Blueprint 登録
    register_routes(app)

    return app
