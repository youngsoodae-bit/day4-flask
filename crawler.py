import sys
import io
import webbrowser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Windows 콘솔 한글 깨짐 방지
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

RSS_URL = "https://feeds.feedburner.com/yonhapnews/all"
FALLBACK_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RSSReader/1.0)"
}


def fetch_rss(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.content


def parse_items(xml_bytes, limit=10):
    soup = BeautifulSoup(xml_bytes, "xml")
    items = soup.find_all("item")[:limit]

    results = []
    for item in items:
        title = item.find("title")
        description = item.find("description")
        link = item.find("link")
        pub_date = item.find("pubDate")

        results.append({
            "title": title.get_text(strip=True) if title else "(제목 없음)",
            "summary": _clean_summary(description.get_text(strip=True) if description else ""),
            "link": link.get_text(strip=True) if link else "",
            "published": _format_date(pub_date.get_text(strip=True) if pub_date else ""),
        })

    return results


def _clean_summary(text):
    # HTML 태그 제거 후 100자로 자르기
    clean = BeautifulSoup(text, "html.parser").get_text(strip=True)
    return clean[:100] + "..." if len(clean) > 100 else clean


def _format_date(raw):
    if not raw:
        return "알 수 없음"
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"):
        try:
            dt = datetime.strptime(raw, fmt)
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            continue
    return raw


def print_news(items):
    sep = "─" * 70
    print(f"\n{'뉴스 RSS 크롤러':^70}")
    print(sep)
    for i, item in enumerate(items, 1):
        print(f"[{i:02d}] {item['title']}")
        print(f"     발행: {item['published']}")
        if item["summary"]:
            print(f"     요약: {item['summary']}")
        print(f"     링크: {item['link']}")
        print(sep)


def open_interactive(items):
    print("\n번호를 입력하면 브라우저로 열립니다. (0 또는 Enter → 종료)")
    while True:
        try:
            raw = input("열 기사 번호: ").strip()
            if raw == "" or raw == "0":
                break
            n = int(raw)
            if 1 <= n <= len(items):
                url = items[n - 1]["link"]
                print(f"  → 브라우저 열기: {items[n-1]['title']}")
                webbrowser.open(url)
            else:
                print(f"  1~{len(items)} 사이 번호를 입력하세요.")
        except ValueError:
            print("  숫자를 입력하세요.")
        except KeyboardInterrupt:
            break


def main():
    for url, name in [(RSS_URL, "연합뉴스"), (FALLBACK_URL, "구글 뉴스")]:
        try:
            print(f"{name} RSS 가져오는 중... ({url})")
            xml = fetch_rss(url)
            items = parse_items(xml, limit=10)
            if items:
                print(f"{name}에서 {len(items)}건 파싱 완료.")
                print_news(items)
                open_interactive(items)
                return
        except Exception as e:
            print(f"{name} 실패: {e}")

    print("모든 RSS 소스 접근 실패.")


if __name__ == "__main__":
    main()
