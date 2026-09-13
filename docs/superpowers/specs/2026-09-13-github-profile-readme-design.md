# GitHub 프로필 README 설계

날짜: 2026-09-13
대상: `hs03290811/hs03290811` 프로필 저장소

## 목표

보안을 공부하는 대학생 Adia의 GitHub 프로필 첫 화면을 애플 제품 페이지 느낌의 흑백 디자인으로 꾸민다.
템플릿이나 AI가 만든 것처럼 보이는 요소(인사말, 이모지 남발, 상투적 문구)는 넣지 않는다.

## 내용

| 항목 | 값 |
|---|---|
| 닉네임 | Adia |
| 소속 | 중앙대학교 소프트웨어학부 (실명은 표시하지 않음) |
| 소개 문구 | "보안과 AR을 공부합니다. 귀여운 강아지 호두를 키우고 있으며 유기견 봉사가 취미입니다." |
| 언어 | C, C++, C#, Java, Python, JavaScript, TypeScript, HTML, CSS |
| 프레임워크 | Unity, FastAPI, React Native, SQLAlchemy |
| 인프라 | PostgreSQL, PostGIS, Redis, Docker, AWS, Linux |
| 도구 | Git, Notion |
| 기기 | MacBook Pro 14 |
| 음악 | Nell, Radiohead, Nirvana, Oasis, Green Day, SHINee, G-Dragon (덜 대중적인 순) |
| 연락처 | song2won@daum.net, peachee@cau.ac.kr |

### 프로젝트 목록

만든 것 (본인 저장소):

| 저장소 | 설명 | 언어 |
|---|---|---|
| hs03290811/capstone2 | Guardian Login System. 키스트로크 다이내믹스와 위험 기반 인증을 결합한 적응형 로그인 | Python |
| hs03290811/capstone | 전국 도로 경사도 API 서버. 도로망·DEM 데이터를 PostGIS에 적재하고 FastAPI로 제공 | Python |
| hs03290811/linux_Team3 | 리눅스 커널 netfilter conntrack 락 최적화 (dynamic spinlock, per-bucket lock) | C |

함께 만든 것 (남의 저장소, 커밋 검색 기준 2026-09-13):

| 저장소 | 설명 | 기여 | 공개 |
|---|---|---|---|
| CAULectra/lectra_BE | AI 강의노트 서비스 백엔드. 슬라이드·판서·음성을 슬라이드 단위로 통합 | 커밋 36, PR 21 | 공개 |
| yeonnnnni/CAU_SWE02_6 | 윷놀이. 4·5·6각형 판을 지원하는 OOAD 구조의 Java 게임 | 커밋 32, PR 10 | 공개 |
| 13131323/CV_AR | 실시간 장면 이해 기반 환경 적응형 AR 아바타 행동 생성 (Python + Unity) | 커밋 7 | 공개 |
| backtrap/CV-AR | 위 프로젝트의 비공개 저장소 | 커밋 7, PR 1 | 비공개, 링크 없음 |
| ICT-CUBE/FE | 프론트엔드 | 커밋 2, PR 2 | 비공개, 링크 없음 |

## 구조

```
hs03290811/
├── README.md
├── scripts/build_svgs.py      # assets/ 전체를 생성. 내용 수정은 이 파일에서
└── assets/
    ├── header-{light,dark}.svg
    ├── card-*-{light,dark}.svg  # 프로젝트 카드 하나당 SVG 하나 (클릭 가능하게 <a>로 감쌈)
    ├── stack-{light,dark}.svg
    ├── stats-{light,dark}.svg, langs-{light,dark}.svg  # build_stats.py가 생성
    └── music-{light,dark}.svg
```

모든 SVG는 라이트/다크 두 벌. README에서 `<picture>` + `prefers-color-scheme`로 전환.
프로젝트 카드는 SVG 하나에 여러 카드를 그리면 링크를 걸 수 없으므로 카드마다 SVG를 따로 만들고 `<a>`로 감싼다.
CV_AR은 공개 저장소(13131323)와 비공개 저장소(backtrap)가 같은 프로젝트이므로 카드 하나로 합치고 커밋 수를 합산한다.
배경은 투명(GitHub 테마 배경 위에 얹힘). 카드·구분선은 반투명 흑/백이라 어떤 테마에서도 회색 톤이 유지된다.
라이트: 본문 `#1d1d1f`, 보조 `#6e6e73`. 다크: 본문 `#f5f5f7`, 보조 `#a1a1a6`.

## README 순서

1. 헤더 SVG: "Adia" 크게, 아래 작은 회색 "중앙대학교 소프트웨어학부".
2. 한 줄 소개 (마크다운 텍스트, 한국어).
3. Projects: "만든 것", "함께 만든 것" 두 묶음. 카드 SVG 2열(홀수 개면 마지막은 전체 폭). 각 카드에 이름, 한 줄 설명, 언어 또는 기여량. 카드마다 `<a>`로 저장소 링크.
4. Stack: 텍스트 칩 한 줄 SVG.
5. Playing: 애플 뮤직 목록 스타일 SVG.
6. Stats: 직접 만든 카드 2개 (GitHub 통계, 언어 비율). github-readme-stats 공개 서버가 자주 멈춰(503) 쓰지 않는다. `scripts/build_stats.py`가 커밋 검색 API로 전체 기간·공개 저장소만 세고, GitHub Action이 매주 갱신한다. 언어 비율은 저장소별로 정규화해 합친다.
7. Contact: 이메일 두 개.
8. 마지막 줄: "가장 친한 친구였던 혜리를 기억하며." (작은 글씨)

## 타이포그래피

SVG에서 외부 폰트를 불러올 수 없으므로 시스템 폰트 스택 사용:
`-apple-system, "SF Pro Display", "SF Pro Text", "Helvetica Neue", "Apple SD Gothic Neo", "Segoe UI", "Malgun Gothic", Arial, sans-serif`.
Mac에서는 SF Pro와 Apple SD Gothic Neo로 렌더링된다.

## 검증

- SVG를 브라우저에서 라이트/다크로 렌더링해 사용자에게 보여주고 확인받는다.
- 저장소 생성과 푸시는 사용자 확인 후 진행한다.
- 푸시 후 실제 프로필 페이지에서 라이트/다크 모두 확인한다.

## 범위 밖

- 참여 저장소 카드 자동 갱신. 프로젝트가 추가되면 `scripts/build_svgs.py`의 DATA를 직접 수정한다. (통계 카드만 Action으로 갱신)
- 개별 저장소 README 정리.
