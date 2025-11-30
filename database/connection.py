# database/connection.py
import sqlite3
from pathlib import Path
from flask import g

# プロジェクトルート (news_collector) を基準に DB ファイルのパスを決定
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "rss.db"


def _ensure_db_dir() -> None:
    """DB ファイルを置くディレクトリがなければ作成する"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """生の sqlite3 コネクションを返す (Flask コンテキスト外でも利用可)"""
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db() -> sqlite3.Connection:
    """Flask の g にコネクションをキャッシュして返す"""
    if "db" not in g:
        g.db = get_connection()
    return g.db


def close_db(e=None) -> None:
    """Flask の teardown_appcontext で呼び出される"""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app) -> None:
    """Flask アプリに DB クローズ処理を登録する"""
    app.teardown_appcontext(close_db)
