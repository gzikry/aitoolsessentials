#!/usr/bin/env python3
"""Read the new-window candidate pages for 2026-09-23 and dump their visible bodies."""
import json, re, subprocess, sys
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = Path(__file__).resolve().parent
BASE = "https://www.sourcee.app/journo-request/"


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "-w", "\n__HTTP__%{http_code}__", url], capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def body(raw):
    b = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", b)
    t = re.sub(r"\s+", " ", t).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", t, re.S)
    return (m.group(1).strip() if m else "")


def dp(raw):
    for pat in (r'"datePublished":\s*"([^"]+)"', r'\\+"datePublished\\+":\\+"([^"\\]+)'):
        m = re.search(pat, raw)
        if m:
            return m.group(1)
    return None


slugs = json.loads((OUT / "_window_0923.json").read_text())
res = {}
for s, lm in slugs["ai_only"]:
    code, raw = curl(BASE + s)
    b = body(raw)
    res[s] = {"http": code, "lastmod": lm, "datePublished": dp(raw), "len": len(b), "body": b[:2200]}
    print("=" * 100)
    print(f"{code} | {s} | lastmod {lm} | datePublished {res[s]['datePublished']} | {len(b)} chars")
    print(b[:1400])
    print()

(OUT / "_newbodies_0923.json").write_text(json.dumps(res, indent=1))
print("wrote _newbodies_0923.json")
