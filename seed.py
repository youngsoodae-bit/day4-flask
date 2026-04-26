import sqlite3
from datetime import datetime
from crawler import fetch_rss, parse_items

DB = 'blog.db'

FIXED_POSTS = [
    {
        'title': '이순신은 울었다',
        'created_at': 'Apr 26, 2026',
        'content': """이순신은 울었다.

SNS를 열면 강한 남자들이 넘쳐난다. 완벽한 몸, 빠른 성공, 흔들리지 않는 표정. 세상이 정해놓은 강함의 조건이다. 16세에 그 화면을 보고 있으면, 하루에 한 번쯤은 자신이 얼마나 부족한가를 확인하는 시간이 된다.

그 이순신이.

---

이순신을 모르는 한국인은 없다. 명량해전, 23전 23승, 불패의 장군. 그런데 우리는 그의 일기를 잘 읽지 않는다.

1597년 4월 19일. 이순신은 옥에서 풀려나 백의종군 명령을 받은 직후 이렇게 썼다.

"어찌하랴 어찌하랴. 천지간에 나 같은 사정이 또 어디 있을 것이랴. 어서 죽는 것만 같지 못하구나."

이것이 우리가 알던 그 이순신이다.

그는 조정의 모함으로 장군 자리를 빼앗겼다. 감옥에 갇혔다. 죽음 직전까지 몰렸다. 백의종군을 떠나는 길, 어머니가 배를 타고 아들을 보러 오다 숨을 거뒀다. 이순신은 어머니의 임종도 지키지 못했다. 장례조차 치르지 못하고 그 길로 전장을 향해 걸었다.

강함이란 무엇인가? 무너지지 않는 것인가? 두려움을 느끼지 않는 것인가?

이순신은 무너졌다. 두려움도 느꼈다. 그럼에도 걸었다. 백성이 있었기 때문이다. 자신의 억울함보다 큰 것을, 나라와 백성으로 버텼다.

그해 9월, 이순신에게 남은 배는 13척이었다. 일본 수군은 수백 척을 이끌고 왔다. 부하들은 도망치자고 했다. 이순신은 말했다.

"죽고자 하면 살고, 살고자 하면 죽는다."

필사즉생(必死則生). 이것이 전략이 아니었다면, 차라리 신앙이었다. 두려움을 느끼면서도 나아가는 것. 그것이 진짜 용기의 정체다.

서양 심리학은 이것을 그릿이라 부른다. 하지만 이순신은 400년 전에 이미 알고 있었다.

이순신은 32세에 무과에 급제했다. 늦은 출발이다. 그는 서두르지 않았다. 아니, 서두를 수 없는 상황에서도 준비를 멈추지 않았다. 대기만성이란 말이 여기에 어울린다면, 그것은 늦게 핀 꽃이 아니라 오래 버틴 뿌리의 이야기다.

이순신은 지금 여기 없다. 그러나 그의 발소리는 여전히 16세를 향하고 있다.

---

지금 네가 보는 강함은 진짜가 아닐지도 모른다.

이순신도 무너졌다. 그럼에도 걸었다. 그 걸음의 이유는 자신이 아니었다. 자신보다 큰 무언가였다.

너의 고난은 낭비가 아니다.

버티는 동안, 뿌리가 깊어지고 있다.

고난과 장애를 만났을 때 버티면 너의 뿌리와 기초가 튼튼해진다.""",
    },
]

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


def seed_fixed():
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
    for post in FIXED_POSTS:
        exists = conn.execute(
            'SELECT 1 FROM post WHERE title = ?', (post['title'],)
        ).fetchone()
        if not exists:
            conn.execute(
                'INSERT INTO post (title, content, created_at) VALUES (?, ?, ?)',
                (post['title'], post['content'], post['created_at'])
            )
            added += 1
    conn.commit()
    conn.close()
    print(f"[seed_fixed] {added}건 추가됨")


def seed():
    seed_fixed()
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
