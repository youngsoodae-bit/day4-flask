import sqlite3
from datetime import datetime, timedelta
import random

DB = 'blog.db'

titles = [
    "파이썬으로 배우는 웹 개발 기초",
    "Flask vs Django: 어떤 프레임워크를 선택할까?",
    "SQLite로 시작하는 데이터베이스 입문",
    "HTML과 CSS로 나만의 블로그 만들기",
    "JavaScript 비동기 프로그래밍 완전 정복",
    "Git으로 버전 관리 시작하기",
    "REST API 설계 원칙과 모범 사례",
    "도커로 개발 환경 통일하기",
    "클린 코드: 읽기 좋은 코드 작성법",
    "테스트 주도 개발(TDD) 실전 가이드",
    "알고리즘 문제 풀이: 정렬 편",
    "자료구조 한눈에 보기: 스택과 큐",
    "리액트 훅(Hooks) 완벽 이해하기",
    "타입스크립트로 안전한 코드 작성하기",
    "Node.js로 서버 구축하기",
    "PostgreSQL vs MySQL 비교 분석",
    "AWS 입문: EC2와 S3 기초",
    "리눅스 명령어 치트시트",
    "정규표현식 마스터하기",
    "함수형 프로그래밍 개념 정리",
    "객체지향 프로그래밍 4대 원칙",
    "디자인 패턴: 싱글톤과 팩토리",
    "웹 성능 최적화 10가지 방법",
    "OAuth2.0 인증 흐름 이해하기",
    "JWT 토큰 기반 인증 구현하기",
    "Redis 캐싱으로 성능 높이기",
    "Celery로 비동기 작업 처리하기",
    "CI/CD 파이프라인 구축하기",
    "코드 리뷰 잘 하는 방법",
    "프로그래머의 커리어 성장 전략",
    "스타트업 개발팀 문화 만들기",
    "오픈소스 기여 시작하기",
    "기술 블로그 운영 팁",
    "개발자를 위한 영어 공부법",
    "번아웃 예방과 업무 효율 높이기",
    "맥북 개발 환경 세팅 A to Z",
    "VSCode 필수 익스텐션 모음",
    "터미널 생산성 높이기: zsh와 oh-my-zsh",
    "깃허브 프로필 멋지게 꾸미기",
    "포트폴리오 사이트 만들기",
    "취업 준비생을 위한 코딩 테스트 전략",
    "면접에서 자주 나오는 CS 질문 모음",
    "신입 개발자가 알아야 할 것들",
    "애자일 스크럼 방법론 실전 적용",
    "프로젝트 문서화의 중요성",
    "API 문서 자동화: Swagger 활용",
    "마이크로서비스 아키텍처 입문",
    "GraphQL vs REST: 언제 무엇을 쓸까",
    "WebSocket으로 실시간 채팅 구현하기",
    "PWA(Progressive Web App) 만들기",
    "머신러닝 입문: 선형 회귀 이해하기",
    "딥러닝과 신경망 기초",
    "자연어 처리(NLP) 시작하기",
    "OpenAI API 활용하기",
    "데이터 시각화: matplotlib과 seaborn",
    "판다스로 데이터 분석 시작하기",
    "SQL 쿼리 최적화 기법",
    "인덱스 설계와 쿼리 성능 튜닝",
    "보안 코딩 기초: OWASP Top 10",
    "XSS와 CSRF 공격 막기",
    "HTTPS와 SSL/TLS 이해하기",
    "DNS 작동 원리 알아보기",
    "HTTP/2와 HTTP/3 차이점",
    "브라우저 동작 원리",
    "웹 접근성 A11y 가이드",
    "반응형 웹 디자인 핵심 개념",
    "CSS Grid와 Flexbox 비교",
    "Tailwind CSS 빠르게 시작하기",
    "Sass/SCSS 사용법",
    "웹 애니메이션 효과 만들기",
    "모바일 앱 개발: React Native 입문",
    "Flutter로 크로스플랫폼 앱 만들기",
    "앱 스토어 출시 가이드",
    "게임 개발 입문: Unity 기초",
    "블록체인 기술 이해하기",
    "스마트 컨트랙트 작성하기",
    "클라우드 네이티브 개발",
    "서버리스 아키텍처 활용하기",
    "쿠버네티스 입문 가이드",
    "모니터링과 로깅 시스템 구축",
    "개발자가 알아야 할 수학",
    "이산수학과 알고리즘의 관계",
    "암호학 기초: 해싱과 암호화",
    "컴파일러 원리 쉽게 이해하기",
    "운영체제 기초: 프로세스와 스레드",
    "메모리 관리와 가비지 컬렉션",
    "네트워크 소켓 프로그래밍",
    "파이썬 고급 기능: 데코레이터와 제너레이터",
    "파이썬 패키지 배포하기",
    "가상환경과 의존성 관리",
    "코드 품질 도구: lint와 formatter",
    "리팩토링 기법 실전 예제",
    "레거시 코드 다루기",
    "기술 부채 줄이는 방법",
    "스타트업에서 배운 것들",
    "개발자의 독서 습관",
    "내가 좋아하는 프로그래밍 도구들",
    "10년 차 개발자의 조언",
    "사이드 프로젝트 성공시키는 법",
]

contents = [
    "이 글에서는 기초부터 차근차근 알아보겠습니다. 처음 접하는 분들도 쉽게 따라올 수 있도록 예제 코드와 함께 설명합니다. 실습을 통해 개념을 익히는 것이 중요하니 직접 코드를 작성해보세요.",
    "개발을 처음 시작하면 수많은 선택지 앞에서 막막함을 느끼게 됩니다. 이번 포스트에서는 실제 경험을 바탕으로 어떤 기술 스택을 선택하면 좋을지 정리해봤습니다.",
    "오늘은 제가 실무에서 직접 사용하고 있는 방법들을 공유하려고 합니다. 이론보다는 실전 위주로 설명할 예정이며, 바로 프로젝트에 적용할 수 있는 내용들입니다.",
    "많은 개발자들이 어려워하는 개념 중 하나입니다. 쉬운 비유와 시각적인 자료를 통해 핵심 개념을 정리했습니다. 단계별로 따라오시면 분명히 이해할 수 있습니다.",
    "이 기술을 제대로 이해하면 개발 속도와 코드 품질이 크게 향상됩니다. 기본 개념부터 고급 활용까지, 실용적인 예제로 알아보겠습니다.",
    "실무에서 자주 마주치는 문제와 그 해결책을 담았습니다. 같은 실수를 반복하지 않도록 체크리스트 형식으로 정리해두었습니다.",
    "커리어를 쌓아가면서 깨달은 것들을 공유합니다. 기술적인 내용 외에도 팀워크와 커뮤니케이션에 대한 인사이트도 담겨있습니다.",
    "최근 트렌드를 반영한 최신 내용입니다. 변화하는 기술 환경에 적응하기 위해 꼭 알아두어야 할 사항들을 정리했습니다.",
    "처음에는 복잡해 보이지만 원리를 이해하면 간단합니다. 핵심 개념을 명확하게 파악하고 나면 응용 범위가 크게 넓어집니다.",
    "삽질을 줄이고 싶다면 이 글을 꼭 읽어보세요. 제가 직접 경험한 시행착오들을 솔직하게 공유합니다.",
]

def seed():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    conn.execute('''
        CREATE TABLE IF NOT EXISTS post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    base_date = datetime(2024, 1, 1)
    posts = []
    for i in range(120):
        title = titles[i % len(titles)]
        if i >= len(titles):
            title = f"{title} ({i // len(titles) + 1}편)"
        content = contents[i % len(contents)]
        days_offset = random.randint(0, 480)
        post_date = base_date + timedelta(days=days_offset)
        created_at = post_date.strftime('%b %d, %Y')
        posts.append((title, content, created_at))

    conn.executemany(
        'INSERT INTO post (title, content, created_at) VALUES (?, ?, ?)',
        posts
    )
    conn.commit()

    count = conn.execute('SELECT COUNT(*) FROM post').fetchone()[0]
    conn.close()
    print(f"완료! 현재 총 {count}개의 포스트가 있습니다.")

if __name__ == '__main__':
    seed()
