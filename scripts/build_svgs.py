#!/usr/bin/env python3
"""assets/ 아래 SVG를 전부 생성한다. 내용을 바꾸려면 이 파일의 DATA 부분을 고치고 다시 실행.

    python3 scripts/build_svgs.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

FONT = (
    '-apple-system, "SF Pro Display", "SF Pro Text", "Helvetica Neue", '
    '"Apple SD Gothic Neo", "Segoe UI", "Malgun Gothic", Arial, sans-serif'
)

# 배경은 투명. GitHub 테마(라이트 #fff, 다크 #0d1117, dimmed #22272e 등) 위에 그대로 얹힌다.
# 카드와 구분선은 반투명이라 어떤 배경 위에서도 애플의 회색 톤이 나온다.
THEMES = {
    "light": dict(fg="#1d1d1f", sub="#6e6e73", line="rgba(0,0,0,0.13)", card="rgba(0,0,0,0.035)"),
    "dark": dict(fg="#f5f5f7", sub="#a1a1a6", line="rgba(255,255,255,0.16)", card="rgba(255,255,255,0.06)"),
}

# ──────────────────────────────────────────────── DATA ──
NAME = "Adia"
AFFILIATION = "중앙대학교 소프트웨어학부"

# (파일명, 제목, 설명 줄들, 하단 메타)
MINE = [
    ("guardian", "Guardian Login System",
     ["키스트로크 다이내믹스와 위험 기반 인증을", "결합한 적응형 로그인 시스템"],
     "Python · FastAPI · Redis"),
    ("slope", "도로 경사도 API",
     ["전국 도로망과 DEM으로 경사도를 계산해", "PostGIS에 적재하고 FastAPI로 제공"],
     "Python · PostGIS · AWS"),
    ("netfilter", "netfilter 락 최적화",
     ["리눅스 커널 conntrack 해시 테이블의 전역 spinlock을", "per-bucket lock으로 바꿔 경합을 줄이는 실험"],
     "C · Linux kernel"),
]

WITH = [
    ("lectra", "Lectra BE",
     ["슬라이드·판서·음성을 슬라이드 단위로", "묶어주는 AI 강의노트 백엔드"],
     "36 commits · 21 PRs · Python"),
    ("yut", "윷놀이",
     ["4·5·6각형 판을 지원하는 윷놀이 게임.", "소프트웨어공학 팀 프로젝트"],
     "32 commits · 10 PRs · Java"),
    ("cvar", "CV_AR",
     ["실시간 장면 이해로 환경에 적응하는", "AR 아바타 행동 생성 연구"],
     "14 commits · 1 PR · Python · Unity"),
    ("ictcube", "ICT-CUBE FE",
     ["비공개 프로젝트의 프론트엔드"],
     "2 commits · 2 PRs · private"),
]

STACK = [
    ("Languages", ["C", "C++", "C#", "Java", "Python", "JavaScript", "TypeScript", "HTML", "CSS"]),
    ("Frameworks", ["Unity", "FastAPI", "React Native", "SQLAlchemy"]),
    ("Infra", ["PostgreSQL", "PostGIS", "Redis", "Docker", "AWS", "Linux"]),
    ("Tools", ["Git", "Notion"]),
    ("Setup", ["MacBook Pro 14"]),
]

MUSIC = [
    ("Nell", "band"),
    ("Radiohead", "band"),
    ("Nirvana", "band"),
    ("Oasis", "band"),
    ("Green Day", "band"),
    ("SHINee", "group"),
    ("G-Dragon", "solo"),
]
# ────────────────────────────────────────────────────────


def svg(w, h, body, t):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        f'<style>text{{font-family:{FONT};}}</style>\n'
        f'{body}</svg>\n'
    )


def text(x, y, s, size, fill, weight=400, anchor="start", spacing=0):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{spacing}">{s}</text>\n')


def eyebrow(x, y, s, t):
    return text(x, y, s, 13, t["sub"], 500)


def header(t):
    w, h = 830, 260
    b = text(w / 2, 140, NAME, 76, t["fg"], 600, "middle", -2)
    b += text(w / 2, 184, AFFILIATION, 17, t["sub"], 400, "middle")
    return svg(w, h, b, t)


def card(title, lines, meta, t, wide=False):
    w, h = (830 if wide else 407), 160
    r = 18
    b = f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="{t["card"]}" stroke="{t["line"]}"/>\n'
    b += text(28, 46, title, 20, t["fg"], 600, spacing=-0.3)
    y = 76
    for ln in lines:
        b += text(28, y, ln, 14, t["sub"])
        y += 22
    b += text(28, h - 28, meta, 12, t["sub"], 500)
    return svg(w, h, b, t)


def _tw(s, size):
    """대략적인 텍스트 폭. 한글/전각은 1em, 나머지는 0.56em."""
    return sum(size if ord(c) > 0x2E7F else size * 0.56 for c in s)


def stack(t):
    w = 830
    pad_l, label_w, y = 0, 120, 44
    b = eyebrow(pad_l, 20, "Stack", t)
    for label, items in STACK:
        b += text(pad_l, y + 18, label, 13, t["sub"], 500)
        x = pad_l + label_w
        for it in items:
            tw = _tw(it, 14)
            cw = tw + 28
            if x + cw > w:
                x = pad_l + label_w
                y += 40
            b += (f'<rect x="{x}" y="{y}" width="{cw:.0f}" height="30" rx="15" '
                  f'fill="none" stroke="{t["line"]}"/>\n')
            b += text(x + cw / 2, y + 19.5, it, 14, t["fg"], 400, "middle")
            x += cw + 8
        y += 48
    h = y - 4
    return svg(w, h, b, t)


def music(t):
    w = 830
    row = 48
    b = eyebrow(0, 20, "Playing", t)
    y = 40
    for i, (name, kind) in enumerate(MUSIC, 1):
        b += text(4, y + 31, f"{i}", 14, t["sub"], 400)
        b += text(40, y + 31, name, 17, t["fg"], 500)
        b += text(w - 4, y + 31, kind, 13, t["sub"], 400, "end")
        if i < len(MUSIC):
            b += f'<line x1="40" y1="{y + row}" x2="{w}" y2="{y + row}" stroke="{t["line"]}"/>\n'
        y += row
    h = y + 8
    return svg(w, h, b, t)


def main():
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t))
        (OUT / f"stack-{name}.svg").write_text(stack(t))
        (OUT / f"music-{name}.svg").write_text(music(t))
        for i, (slug, title, lines, meta) in enumerate(MINE):
            wide = (i == len(MINE) - 1 and len(MINE) % 2 == 1)
            (OUT / f"card-{slug}-{name}.svg").write_text(card(title, lines, meta, t, wide))
        for slug, title, lines, meta in WITH:
            (OUT / f"card-{slug}-{name}.svg").write_text(card(title, lines, meta, t))
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
