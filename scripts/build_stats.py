#!/usr/bin/env python3
"""GitHub API에서 통계를 읽어 assets/stats-*.svg, assets/langs-*.svg를 만든다.

    GITHUB_TOKEN=$(gh auth token) python3 scripts/build_stats.py

GitHub Action(.github/workflows/stats.yml)이 매주 실행해 자동으로 갱신한다.

전체 기간의 커밋을 세기 위해 커밋 검색 API(author:LOGIN)를 쓴다. GraphQL의
contributionsCollection / repositoriesContributedTo는 최근 1년만 세기 때문이다.
비공개 저장소도 센다. 토큰이 볼 수 있는 범위만 집계되므로, Action에서는 repo 권한이
있는 PAT(secret STATS_TOKEN)를 써야 공개 전용 숫자로 덮어쓰지 않는다.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_svgs import OUT, THEMES, eyebrow, svg, text  # noqa: E402

LOGIN = "hs03290811"
API = "https://api.github.com"

# 프로젝트 코드가 아닌 부수 파일 언어. 비율 계산에서 뺀다.
LANG_IGNORE = {"Mako", "Roff", "M4", "Makefile", "Shell", "Dockerfile", "Wolfram Language",
               "Assembly", "Awk", "Lex", "Yacc", "Perl", "SmPL", "Linker Script", "XS", "sed",
               "Gherkin", "Clojure", "UnrealScript", "Ruby", "Kotlin", "Objective-C", "Swift"}


def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not t:
        sys.exit("GITHUB_TOKEN이 필요합니다")
    return t


def get(path, **params):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"bearer {token()}",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def search_all(path, q):
    items, page = [], 1
    while True:
        data = get(path, q=q, per_page=100, page=page)
        items += data["items"]
        if len(items) >= data["total_count"] or not data["items"] or page >= 10:
            return items
        page += 1


def fetch():
    commits = search_all("/search/commits", f"author:{LOGIN}")
    # 저장소별 커밋 수 (토큰이 볼 수 있는 비공개 저장소 포함)
    per_repo = {}
    for c in commits:
        name = c["repository"]["full_name"]
        per_repo[name] = per_repo.get(name, 0) + 1
    prs = get("/search/issues", q=f"author:{LOGIN} is:pr", per_page=1)["total_count"]
    own = [r for r in get(f"/users/{LOGIN}/repos", per_page=100, type="owner") if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in own)
    repos = set(per_repo) | {r["full_name"] for r in own}
    langs_by_repo = {name: get(f"/repos/{name}/languages") for name in sorted(repos)}
    return dict(per_repo=per_repo, prs=prs, stars=stars, langs_by_repo=langs_by_repo)


def summarize(d):
    contributed = [r for r in d["per_repo"] if not r.startswith(f"{LOGIN}/")]
    # 저장소마다 언어 비율을 1로 정규화한 뒤 합친다. 바이트로 합치면 커널 소스가
    # 통째로 들어 있는 저장소 하나가 C 99%를 만들어 버린다.
    langs = {}
    for name, by_lang in d["langs_by_repo"].items():
        by_lang = {k: v for k, v in by_lang.items() if k not in LANG_IGNORE}
        repo_total = sum(by_lang.values()) or 1
        for k, v in by_lang.items():
            langs[k] = langs.get(k, 0) + v / repo_total
    total = sum(langs.values()) or 1
    top = [(k, v / total) for k, v in sorted(langs.items(), key=lambda kv: -kv[1])]
    top = [(k, s) for k, s in top if s >= 0.01][:6]
    return {
        "commits": sum(d["per_repo"].values()),
        "prs": d["prs"],
        "contributed_to": len(contributed),
        "stars": d["stars"],
        "langs": top,
    }


def card_frame(t, w=407, h=160):
    return f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>\n'


def stats_card(s, t):
    w, h = 407, 160
    b = card_frame(t) + eyebrow(28, 40, "GitHub", t)
    cells = [
        (s["commits"], "commits"), (s["prs"], "pull requests"),
        (s["contributed_to"], "repos contributed to"), (s["stars"], "stars"),
    ]
    for i, (n, label) in enumerate(cells):
        x = 28 + (i % 2) * 190
        y = 88 + (i // 2) * 48
        num = f"{n:,}"
        b += text(x, y, num, 26, t["fg"], 600, spacing=-0.5)
        b += text(x + len(num) * 15.5 + 8, y, label, 12, t["sub"], 500)
    return svg(w, h, b, t)


def langs_card(s, t):
    w, h = 407, 160
    b = card_frame(t) + eyebrow(28, 40, "Languages", t)
    # 막대 하나. 비율이 큰 언어부터 진한 색 → 옅은 색.
    bx, by, bw, bh = 28, 54, w - 56, 8
    n = len(s["langs"]) or 1
    b += f'<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4"/></clipPath>\n'
    b += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4" fill="{t["line"]}"/>\n'
    x = bx
    for i, (name, share) in enumerate(s["langs"]):
        seg = bw * share
        op = 1 - i * (0.75 / n)
        b += (f'<rect x="{x:.1f}" y="{by}" width="{seg:.1f}" height="{bh}" fill="{t["fg"]}" '
              f'fill-opacity="{op:.2f}" clip-path="url(#bar)"/>\n')
        x += seg
    # 범례 2열 3행
    for i, (name, share) in enumerate(s["langs"]):
        cx = 28 + (i % 2) * 190
        cy = 88 + (i // 2) * 24
        op = 1 - i * (0.75 / n)
        b += f'<circle cx="{cx + 4}" cy="{cy - 4}" r="4" fill="{t["fg"]}" fill-opacity="{op:.2f}"/>\n'
        b += text(cx + 16, cy, name, 13, t["fg"], 500)
        b += text(cx + 16 + len(name) * 7.8 + 6, cy, f"{share*100:.0f}%", 12, t["sub"])
    return svg(w, h, b, t)


def main():
    s = summarize(fetch())
    print(json.dumps(s, ensure_ascii=False))
    for name, t in THEMES.items():
        (OUT / f"stats-{name}.svg").write_text(stats_card(s, t))
        (OUT / f"langs-{name}.svg").write_text(langs_card(s, t))
    print("wrote stats/langs svgs")


if __name__ == "__main__":
    main()
