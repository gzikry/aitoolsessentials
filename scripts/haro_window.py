#!/usr/bin/env python3
"""Sourcee sitemap window probe for the journo-request monitor.

Replaces the per-run `marketing/haro-outreach/_window_MMDD.py` copies (one hand-copied file per
run for twenty runs, each with TODAY/PREV typed in by hand — the same defect class the digests
keep logging: a value that must move daily maintained by copy-paste).

Usage:
    python3 scripts/haro_window.py                 # today's window, mark = newest lastmod of the
                                                   # most recent previous _window_*.json
    python3 scripts/haro_window.py --today 2026-10-18 --prev 2026-10-17

Writes _sitemap_MMDD.xml and _window_MMDD.json into marketing/haro-outreach/ and prints a
summary: window size, AI-token slugs, AI+spend slugs with matched tokens, spend-only slugs, and
one probe per platform.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
D = SITE_ROOT / "marketing" / "haro-outreach"
sys.path.insert(0, str(SITE_ROOT / "scripts"))
from sourcee_terms import AI, SPEND, REAL_SPEND  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
SITEMAP = "https://www.sourcee.app/sitemap-journo-requests.xml"
FEED = "https://www.sourcee.app/topics/ai/journo-requests"

PLATFORMS = [
    ("Sourcee (sourcee.app)", "https://www.sourcee.app/"),
    ("Sourcee AI topic feed", FEED),
    ("HARO (helpareporter.com)", "https://www.helpareporter.com/"),
    ("Connectively (connectively.us)", "https://www.connectively.us/"),
    ("Source of Sources (sourceofsources.com)", "https://sourceofsources.com/requests"),
    ("Qwoted (qwoted.com)", "https://app.qwoted.com/requests"),
    ("MentionMatch (mentionmatch.com)", "https://mentionmatch.com/"),
    ("Medialyst MCP (medialyst.ai/api/mcp)", "https://medialyst.ai/api/mcp"),
    ("ResponseSource (responsesource.com)", "https://www.responsesource.com/"),
]


def curl(url: str, timeout: int = 90) -> tuple[str, str]:
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "-w", "\n__HTTP__%{http_code}__", url], capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def prev_window(today: str) -> tuple[str, str]:
    """The most recent window file before `today`, and its newest lastmod (the window mark)."""
    files = sorted(p for p in D.glob("_window_*.json") if p.stem.split("_")[-1] < today.replace("-", "")[4:])
    if not files:
        raise SystemExit("no previous _window_*.json to take a mark from")
    p = files[-1]
    d = json.loads(p.read_text())
    stamp = p.stem.split("_")[-1]
    prev_day = f"{today[:4]}-{stamp[:2]}-{stamp[2:]}"
    return prev_day, d["newest"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=date.today().isoformat())
    ap.add_argument("--prev", default=None)
    a = ap.parse_args()

    today = a.today
    if a.prev:
        prev_day = a.prev
        mark = json.loads((D / f"_window_{prev_day.replace('-', '')[4:]}.json").read_text())["newest"]
    else:
        prev_day, mark = prev_window(today)
    print(f"today {today}; window mark from {prev_day} run: {mark}")

    code, xml = curl(SITEMAP)
    (D / f"_sitemap_{today.replace('-', '')[4:]}.xml").write_text(xml)
    pairs = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml)
    slugs = [(loc.rstrip("/").split("/journo-request/")[-1], lm)
             for loc, lm in pairs if "/journo-request/" in loc]
    if not slugs:
        raise SystemExit(f"sitemap parse produced 0 slugs (HTTP {code}, {len(xml)} bytes)")
    newest = max(lm for _, lm in slugs)
    window = [(s, lm) for s, lm in slugs if lm > mark]
    ai = [(s, lm) for s, lm in window if AI.search(s)]
    ai_strict = [(s, lm, [t for t in SPEND.findall(s)]) for s, lm in ai if SPEND.search(s)]
    spend_any = [(s, lm) for s, lm in window if SPEND.search(s)]
    fp = [(s, toks) for s, _lm, toks in ai_strict if not REAL_SPEND.search(s)]

    feed_code, feed_raw = curl(FEED)
    feed_slugs: list[str] = []
    for s in re.findall(r"/journo-request/([a-z0-9\-]{5,160})", feed_raw):
        if s not in feed_slugs:
            feed_slugs.append(s)
    win_set = {s for s, _ in window}

    out = {
        "today": today, "prev": prev_day,
        "sitemap_http": code, "bytes": len(xml), "count": len(slugs), "newest": newest, "mark": mark,
        "window": window, "ai": ai, "ai_strict": ai_strict, "spend_any": spend_any,
        "ai_strict_false_positives": fp,
        "feed_count": len(feed_slugs), "feed_http": feed_code, "feed_bytes": len(feed_raw),
        "feed_overlap_with_window": len([s for s in feed_slugs if s in win_set]),
        "feed_slugs": feed_slugs,
    }

    plats = []
    for name, url in PLATFORMS:
        pcode, raw = curl(url, 40)
        title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
        plats.append({"platform": name, "url": url, "http": pcode, "bytes": len(raw),
                      "title": (title.group(1).strip()[:120] if title else ""),
                      "checkpoint": "Vercel Security Checkpoint" in raw})
    out["platforms"] = plats

    (D / f"_window_{today.replace('-', '')[4:]}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: (len(v) if isinstance(v, list) and k not in ("feed_slugs",) else v)
                      for k, v in out.items() if k not in ("platforms", "feed_slugs")}, indent=1))
    print("--- AI-Token window slugs ---")
    for s, lm in ai:
        print(f"  {lm}  {s}")
    print("--- AI+spend (with matched tokens) ---")
    for s, lm, toks in ai_strict:
        print(f"  {lm}  {s}   tokens={toks}")
    print("--- strict hits judged false positives ---")
    for s, toks in fp:
        print(f"  {s}   tokens={toks}")
    print("--- spend-any window slugs ---")
    for s, lm in spend_any:
        print(f"  {s}   {lm}")
    print("--- platforms ---")
    for p in plats:
        print(f"  {p['http']:>4} {p['bytes']:>8} {p['platform']:<40} {p['title'][:60]}  ckpt={p['checkpoint']}")
    print("--- feed ---")
    print(f"  {len(feed_slugs)} slugs; overlap with window {out['feed_overlap_with_window']}")


if __name__ == "__main__":
    main()
