#!/usr/bin/env python3
"""Body-level scan of every slug in a run's Sourcee sitemap window.

Slug regexes cannot support a "clean window" claim: a request about Anthropic pricing carries no
AI token in its slug. This fetches every slug in the window, scans the rendered body with the shared
matchers (scripts/sourcee_terms.py) and writes _bodies_MMDD.json. Resumable — rows already carrying
a `core` are skipped.

Replaces the hand-copied _bodies_MMDD.py files (one per run for four consecutive runs).

Usage:
    python3 scripts/haro_bodies.py                 # today's window
    python3 scripts/haro_bodies.py --today 2026-10-18
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
D = SITE_ROOT / "marketing" / "haro-outreach"
sys.path.insert(0, str(SITE_ROOT / "scripts"))
from sourcee_terms import AI, SPEND, REAL_SPEND, prose_ai  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
CHROME = ("sourcee.app", "vercel", "sentry", "nextjs.org", "schema.org", "w3.org", "gstatic",
          "google.com/s2", "supabase.co", "redditstatic", "preview.redd.it")


def field(raw: str, key: str) -> str | None:
    for pat in (r'"' + key + r'":\s*"((?:[^"\\]|\\.)*?)"',
                r'\\+"' + key + r'\\+":\\+"((?:[^"\\]|\\.)*?)\\+"'):
        m = re.search(pat, raw)
        if m:
            v = m.group(1)
            for _ in range(3):
                n = v.replace("\\n", " ").replace("\\u0026", "&").replace("\\/", "/")
                n = re.sub(r"\\(.)", r"\1", n)
                if n == v:
                    break
                v = n
            return v.strip()
    return None


def curl(url: str) -> tuple[str, str]:
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=date.today().isoformat())
    a = ap.parse_args()
    mmdd = a.today.replace("-", "")[4:]
    win = json.loads((D / f"_window_{mmdd}.json").read_text())
    slugs = [s for s, _lm in win["window"]]
    out_path = D / f"_bodies_{mmdd}.json"
    bodies = json.loads(out_path.read_text()) if out_path.exists() else {}

    for i, sl in enumerate(slugs):
        if (bodies.get(sl) or {}).get("core"):
            continue
        url = f"https://www.sourcee.app/journo-request/{sl}"
        code, raw = curl(url)
        body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
        m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
        core = m.group(1).strip() if m else ""
        badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
        # Query strings are stripped before the prose scan: `\bai\b` matches the 'AI' inside a
        # YouTube share parameter (?si=AI-...), which scored a ghost story as an AI request.
        scan = re.sub(r"https?://\S+", " ", core)
        links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,160}", raw)))
                 if not any(c in u for c in CHROME)]
        rec = {"slug": sl, "url": url, "http": code, "headline": field(raw, "headline"),
               "datePublished": field(raw, "datePublished"),
               "badge": badge.group(1) if badge else None, "author": field(raw, "name"),
               "domain": field(raw, "domain"),
               "email_redacted": bool(re.search(r"email redacted", core, re.I)),
               "emails_on_page": sorted(set(e for e in re.findall(
                   r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core) if "sourcee" not in e.lower())),
               "published_links": links[:6],
               # `AI` is the SLUG matcher — it requires hyphen/edge delimiters and returns nothing
               # on prose. Using it here produced a body-level false zero for four runs; prose
               # tokens come from prose_ai(), and the slug tokens are recorded separately.
               "ai_tokens_in_body": prose_ai(scan),
               "ai_prose_in_body": prose_ai(scan),
               "ai_slug_tokens": sorted({mm.group(2).lower() for mm in AI.finditer(sl)}),
               "spend_tokens_in_body": sorted({mm.group(1).lower() for mm in SPEND.finditer(scan)}),
               "real_spend_in_body": bool(REAL_SPEND.search(scan)),
               "core": core[:4000]}
        bodies[sl] = rec
        out_path.write_text(json.dumps(bodies, indent=1))
        print(f"[{i}] {code} {str(rec['badge']):<21} mail={len(rec['emails_on_page'])} "
              f"ai={len(rec['ai_tokens_in_body'])} spend={len(rec['spend_tokens_in_body'])} "
              f"real={rec['real_spend_in_body']} {str(rec['headline'])[:60]}", flush=True)
        time.sleep(1)

    # Rescore every stored record from its own `core` before reporting, so a matcher fix applies to
    # rows fetched earlier in this same run instead of only to the next run's.
    for rec in bodies.values():
        scan = re.sub(r"https?://\S+", " ", rec.get("core") or "")
        rec["ai_tokens_in_body"] = prose_ai(scan)
        rec["ai_prose_in_body"] = prose_ai(scan)
        rec["ai_slug_tokens"] = sorted({mm.group(2).lower() for mm in AI.finditer(rec["slug"])})
        rec["spend_tokens_in_body"] = sorted({mm.group(1).lower() for mm in SPEND.finditer(scan)})
        rec["real_spend_in_body"] = bool(REAL_SPEND.search(scan))
    out_path.write_text(json.dumps(bodies, indent=1))

    print("\nfetched", len(bodies), "of", len(slugs))
    print("--- body-level AI hits ---")
    for sl, r in bodies.items():
        if r["ai_tokens_in_body"]:
            print(f"  {sl}: ai={r['ai_tokens_in_body'][:6]} spend={r['spend_tokens_in_body'][:6]} real={r['real_spend_in_body']}")
    print("--- body-level spend-only hits ---")
    for sl, r in bodies.items():
        if r["spend_tokens_in_body"] and not r["ai_tokens_in_body"]:
            print(f"  {sl}: spend={r['spend_tokens_in_body'][:6]} real={r['real_spend_in_body']}")


if __name__ == "__main__":
    main()
