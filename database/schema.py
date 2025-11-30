# database/schema.py

from database.connection import get_connection
from datetime import datetime

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # --- feeds table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            site TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_feeds_site ON feeds(site);
    """)


    # --- keywords table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE
        );
    """)

    # --- feed_keywords (many-to-many) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feed_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feed_id INTEGER NOT NULL,
            keyword_id INTEGER NOT NULL,
            FOREIGN KEY(feed_id) REFERENCES feeds(id),
            FOREIGN KEY(keyword_id) REFERENCES keywords(id)
        );
    """)

    # --- articles table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feed_id INTEGER NOT NULL,
            title TEXT,
            link TEXT UNIQUE,
            description TEXT,
            content TEXT,
            published_at TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(feed_id) REFERENCES feeds(id)
        );
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_articles_feed_id ON articles(feed_id);
    """)

    # --- article_status table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS article_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            read BOOLEAN DEFAULT 0,
            favorite BOOLEAN DEFAULT 0,
            last_viewed_at TEXT,
            comment TEXT,
            tags TEXT,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(article_id) REFERENCES articles(id)
        );
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_article_status_article_id ON article_status(article_id);
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_article_status_favorite ON article_status(favorite);
    """)

    conn.commit()
    conn.close()

def seed_feeds():
    feeds = [
        {"name": "NHKニュース（総合）", "url": "https://www3.nhk.or.jp/rss/", "site": "NHK"},
        {"name": "朝日新聞デジタル（総合）", "url": "https://www.asahi.com/rss/", "site": "Asahi"},
        {"name": "読売新聞（総合）", "url": "https://www.yomiuri.co.jp/feed/", "site": "Yomiuri"},
        {"name": "毎日新聞（総合）", "url": "https://mainichi.jp/rss/", "site": "Mainichi"},
        {"name": "産経ニュース（総合）", "url": "https://www.sankei.com/rss", "site": "Sankei"},
    
        {"name": "ITmedia（総合）", "url": "https://www.itmedia.co.jp/rss/", "site": "ITmedia"},
        {"name": "GIGAZINE（総合）", "url": "https://gigazine.net/news/rss_2.0/", "site": "GIGAZINE"},
        {"name": "TechCrunch Japan", "url": "https://jp.techcrunch.com/feed/", "site": "TechCrunchJP"},
        {"name": "Publickey", "url": "https://www.publickey1.jp/atom.xml", "site": "Publickey"},
        {"name": "ZDNet Japan", "url": "https://japan.zdnet.com/news/rss.xml", "site": "ZDNet"},
        {"name": "CNET Japan", "url": "https://japan.cnet.com/rss/all.rdf", "site": "CNETJapan"},
    
        {"name": "Qiita トレンド", "url": "https://qiita.com/popular-items/feed.atom", "site": "Qiita"},
        {"name": "Zenn（全体フィード）", "url": "https://zenn.dev/feed", "site": "Zenn"},
        {"name": "はてなブックマーク（IT）", "url": "https://b.hatena.ne.jp/entrylist/it.rdf", "site": "HatenaIT"},
    
        {"name": "Google Developers Japan", "url": "https://developers-jp.googleblog.com/feeds/posts/default", "site": "GoogleDevJP"},
        {"name": "AWS公式ブログ", "url": "https://aws.amazon.com/jp/blogs/news/feed/", "site": "AWSBlog"},
        {"name": "Microsoft Dev Blog", "url": "https://devblogs.microsoft.com/feed/", "site": "MSDevBlog"},
        {"name": "GitHub Blog", "url": "https://github.blog/news/feed/", "site": "GitHubBlog"},
    
        {"name": "ナショナルジオグラフィック日本版", "url": "https://natgeo.nikkeibp.co.jp/rss/index.rdf", "site": "NatGeoJP"},
        {"name": "WIRED.jp（Tech/Sci）", "url": "https://wired.jp/feed/", "site": "WIREDJP"},
        {"name": "Science Portal", "url": "https://scienceportal.jst.go.jp/feed/", "site": "SciencePortal"},
        {"name": "MIT Technology Review Japan", "url": "https://www.technologyreview.jp/feed/", "site": "MITTechReviewJP"},
    
        {"name": "東洋経済オンライン（総合）", "url": "https://toyokeizai.net/list/feed/rss", "site": "ToyoKeizai"},
        {"name": "NewsPicks（非公式）", "url": "https://newspicks.com/feed/", "site": "NewsPicks"},
        {"name": "GLOBIS 知見録", "url": "https://globis.jp/feed/", "site": "Globis"},
    
        {"name": "クラスメソッド（DevelopersIO）", "url": "https://dev.classmethod.jp/feed/", "site": "Classmethod"},
        {"name": "Notion Japan Blog", "url": "https://www.notion.so/ja-jp/blog/rss.xml", "site": "NotionJP"},
        {"name": "きしだのHatena Blog", "url": "https://nowokay.hatenablog.com/feed", "site": "KishidaBlog"},
        {"name": "Kraggle Tech Blog", "url": "https://blog.kragle.jp/feed", "site": "KraggleTech"},
        {"name": "Togetter 人気まとめ", "url": "https://togetter.com/rss/summary", "site": "TogetterHot"},
    
        {"name": "Engadget 日本版", "url": "https://japanese.engadget.com/rss.xml", "site": "EngadgetJP"},
        {"name": "ケータイWatch", "url": "https://k-tai.watch.impress.co.jp/rss/all.xml", "site": "KTaiWatch"},
        {"name": "ITmedia Mobile", "url": "https://www.itmedia.co.jp/mobile/subtop/rss.xml", "site": "ITmediaMobile"},
    
        {"name": "ねとらぼ", "url": "https://nlab.itmedia.co.jp/nl/subtop/rss2/", "site": "Netorabo"},
        {"name": "映画.com ニュース", "url": "https://eiga.com/rss/news/", "site": "EigaCom"},
        {"name": "IGN Japan", "url": "https://jp.ign.com/feed", "site": "IGNJapan"},
    ]


    conn = get_connection()
    cursor = conn.cursor()

    for feed in feeds:
        cursor.execute(
            """
            INSERT OR IGNORE INTO feeds (name, site, url, created_at)
            VALUES (?, ?, ?, ?)
            """,
        (feed["name"], feed["site"], feed["url"], datetime.now().isoformat())
    )


    conn.commit()
    conn.close()
    print("Feeds seeded ✔")

