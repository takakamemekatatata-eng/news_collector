# database/queries/feeds.py
from database.connection import get_db

def get_all_feeds():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, url FROM feeds")
    rows = cursor.fetchall()
    conn.close()
    return rows
