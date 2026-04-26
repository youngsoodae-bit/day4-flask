import sqlite3
from datetime import datetime
from crawler import fetch_rss, parse_items

DB = 'blog.db'

RSS_SOURCES = [
    "https://feeds.feedburner.com/yonhapnews/all",
    "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko",
]


def _to_created_at(published: str) -> str:
    """'2026-04-26 02:47' → 'Apr 26, 2026'"""
    try:
        return datetime.strptime(published, "%Y-%m-%d %H:%M").strftime("%b %d, %Y")
    except ValueError:
        return datetime.now().strftime("%b %d, %Y")


def seed():
    items = []
    for url in RSS_SOURCES:
        try:
            xml = fetch_rss(url)
            items = parse_items(xml, limit=10)
            if items:
                break
        except Exception as e:
            print(f"[seed] RSS 실패 ({url}): {e}")

    if not items:
        print("[seed] 가져올 뉴스가 없습니다.")
        return

    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    added = 0
    for item in items:
        exists = conn.execute(
            'SELECT 1 FROM post WHERE title = ?', (item['title'],)
        ).fetchone()
        if exists:
            continue
        content = item['summary'] or item['title']
        if item['link']:
            content += f"\n\n원문: {item['link']}"
        conn.execute(
            'INSERT INTO post (title, content, created_at) VALUES (?, ?, ?)',
            (item['title'], content, _to_created_at(item['published']))
        )
        added += 1

    conn.commit()
    conn.close()
    print(f"[seed] {added}건 추가됨 (중복 {len(items) - added}건 건너뜀)")


if __name__ == '__main__':
    seed()
