#!/usr/bin/env python3
"""Re-verify Short.now's open verification items against their live pages.

Used with the held submission in admin/held-submissions.md (Short.now, held 2026-09-14).
Re-run this after any vendor reply instead of trusting the reply text: on 2026-09-14 the
vendor confirmed contact + authorisation while every one of the five substantive items was
still live on the site, unchanged.

Usage:  python3 scripts/verify_vendor_claims_shortnow.py
Exit code is always 0; read the output.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

PAGES = [
    "https://short.now/",
    "https://short.now/terms/",
    "https://short.now/privacy/",
    "https://short.now/llms.txt",
    "https://short.now/pricing/",
    "https://short.now/impressum/",
    "https://short.now/de/impressum/",
    "https://short.now/tools/",
    "https://short.now/tools/free-clipping/",
    "https://short.now/for/youtubers/",
    "https://short.now/compare/short-now-vs-opus-clip/",
    "https://short.now/compare/best-ai-video-clipping-tools/",
]

# Independent competitor facts we cite, re-checked each run (official page, not their copy).
COMPETITOR = "https://www.opus.pro/pricing"


def fetch(url: str) -> tuple[object, str]:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "text/html,text/plain,*/*", "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return f"ERR:{e}", ""


def text_of(html: str) -> str:
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&#39;", "'"), ("&#x27;", "'")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)


def probe(label: str, pat: str, body: str) -> None:
    hits: list[str] = []
    for m in re.finditer(pat, body, re.I):
        s = m.group(0).strip()[:180]
        if s not in hits:
            hits.append(s)
    print(f"  [{label}] " + ("  ||  ".join(hits[:3]) if hits else "-- none --"))


def main() -> None:
    bodies: dict[str, str] = {}
    print("=== LIVE PAGE STATUS / CONTENT")
    for url in PAGES:
        status, html = fetch(url)
        bodies[url] = text_of(html) if html else ""
        print(f"{url} -> {status} ({len(html)} bytes)")

    home = bodies["https://short.now/"]
    tools = bodies["https://short.now/tools/"]
    freeclip = bodies["https://short.now/tools/free-clipping/"]
    youtubers = bodies["https://short.now/for/youtubers/"]
    vsopus = bodies["https://short.now/compare/short-now-vs-opus-clip/"]
    best = bodies["https://short.now/compare/best-ai-video-clipping-tools/"]
    terms = bodies["https://short.now/terms/"]
    privacy = bodies["https://short.now/privacy/"]
    llms = bodies["https://short.now/llms.txt"]

    print("\n=== ITEM 1: entity / jurisdiction / legal pages")
    probe("ToS 13 governing law", r"governed by and construed[^.]{0,200}", terms)
    probe("impressum marker", r"(?:Impressum|Mentions l[ée]gales|Angaben gem)", home + terms)
    for p in ("/impressum/", "/de/impressum/"):
        print(f"  {p} present: {'yes' if bodies.get('https://short.now' + p) else 'NO (404)'}")

    print("\n=== ITEM 2: processors / training / retention clock")
    probe("privacy sharing", r"Service providers who help us operate[^.]{0,140}", privacy)
    probe("privacy retention", r"Uploaded video files are deleted[^.]{0,180}", privacy)
    probe("ToS 10 retention", r"On the free Starter plan, uploaded videos[^.]{0,180}", terms)
    probe("training mention", r"(?:train|training)[^.]{0,120}", privacy + terms)

    print("\n=== ITEM 3: free-plan allowance (weekly vs monthly)")
    probe("homepage card", r"3 videos to start[^.]{0,90}", home)
    probe("homepage faq", r"You get 3 videos to start[^.]{0,90}", home)
    for name, b in (("tools", tools), ("free-clipping", freeclip),
                    ("for/youtubers", youtubers), ("vs-opus", vsopus), ("best-clipping", best)):
        probe(f"{name} monthly claim", r"3 (?:free )?videos(?:/| every )\s*month[^.]{0,60}", b)
    probe("llms.txt free", r"\*\*Free\*\*[^\n]{0,160}", llms)

    print("\n=== ITEM 4: Starter price / plan names")
    probe("homepage card block", r"Monthly Annual[^\n]{0,700}", home)
    probe("homepage currencies", r"\$\s?\d+(?:\.\d+)?\s*/?\s*(?:mo|forever|yr)?", home)
    probe("llms.txt tiers", r"\*\*(?:Free|Starter|Creator|Pro|Agency)\*\*[^\n]{0,200}", llms)
    probe("vs-opus starter row", r"Starter paid plan \$12[^.]{0,80}", vsopus)
    probe("best-clipping starting price", r"Starting price \$12[^.]{0,80}", best)

    print("\n=== ITEM 5: competitor rows vs Opus Clip's own page")
    probe("their free-plan row", r"Very limited(?: credit allowance|\s*or none)", vsopus + best)
    status, html = fetch(COMPETITOR)
    ob = text_of(html) if html else ""
    print(f"  opus.pro/pricing -> {status}")
    probe("Opus free tier", r"Free \$0[^.]{0,120}", ob)
    probe("Opus paid tiers", r"\$\d+\s*(?:billed monthly|USD /mo)[^.]{0,80}", ob)

    print("\n=== MX (contact reachability)")
    status, raw = fetch("https://dns.google/resolve?name=short.now&type=MX")
    try:
        d = json.loads(raw)
        print("  " + ", ".join(a.get("data", "") for a in d.get("Answer", [])) or "  none")
    except Exception as e:  # noqa: BLE001
        print(f"  lookup failed: {e}")


if __name__ == "__main__":
    main()
