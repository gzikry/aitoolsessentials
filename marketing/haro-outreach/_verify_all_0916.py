"""Re-verify every URL the queue carries, by URL, and record the page's own post date.

Why this exists: build_pitch_queue.py derived age from the digest's `deadline` text, and when
that text contained no date it fell back to the digest's first-seen date. Several digests wrote
"Open (posted >1 month ago)" as the deadline, so a request posted 2026-03-10 was shown as 8 days
old. Three queue rows were overstated by 100-180 days. This reads datePublished off the page.
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
SITE = Path("/Users/georgezikry/aitoolessentials/site")

# every /journo-request/ URL named anywhere in the queue, the ledger, or the carried set
urls: set[str] = set()
for f in (D / "pitch-queue.md", *(D.glob("digest-*.json")), D / "pitch-ledger.json"):
    try:
        txt = f.read_text()
    except OSError:
        continue
    for m in re.findall(r"https?://(?:www\.)?sourcee\.app/journo-request/[a-z0-9\-]+", txt):
        urls.add(m)

# carried + today's candidates that the queue may not name
for extra in ("us-founders-calls-to-slow-ai-development-impact-on-companies",
              "ukraine-tech-builders-and-global-observers-commercial-tech-adaptation",
              "cybersecurity-companies-and-experts-ai-scams-and-consumer-safety",
              "individual-contributors-managing-ai-agents-without-title-or-pay"):
    urls.add(f"https://www.sourcee.app/journo-request/{extra}")

print("URLs to verify:", len(urls))
FEED = json.loads((D / "_feed_0916.json").read_text())
feed_slugs = set(FEED)

now = datetime.now(timezone.utc)
out: dict[str, dict] = {}
rows = []
for url in sorted(urls):
    sl = url.rstrip("/").split("/journo-request/")[1]
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url],
                         capture_output=True, text=True).stdout
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)

    def g(key):
        mm = (re.search(r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw)
              or re.search(r'"' + key + r'":"((?:[^"\\]|\\.)*?)"', raw))
        return mm.group(1).replace("\\u0026", "&").strip() if mm else None

    dp = g("datePublished")
    dom = g("domain")
    age = None
    if dp:
        try:
            age = (now - datetime.fromisoformat(dp.replace("Z", "+00:00"))).days
        except ValueError:
            age = None
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core)
                        if "sourcee" not in e.lower()))
    rec = {
        "slug": sl, "url": url, "http_ok": bool(core), "headline": g("headline"),
        "datePublished": dp, "days_old": age, "badge": badge.group(1) if badge else None,
        "domain": dom, "in_ai_topic_feed": sl in feed_slugs,
        "email_redacted": bool(re.search(r"email redacted", core, re.I)),
        "emails_on_page": emails,
        "linkedin_short": sorted(set(re.findall(r"lnkd\.in/[A-Za-z0-9]+", core))),
        "reply_hints": sorted({h for h in ("DM me", "reply to this thread", "Comment", "schedule",
                                           "email me", "DM or email") if h.lower() in core.lower()}),
        "body": core[:1400],
    }
    out[sl] = rec
    rows.append(rec)
    print(f"{str(age):>4}d  feed={'Y' if rec['in_ai_topic_feed'] else 'n'}  "
          f"badge={str(rec['badge']):<22} {sl[:62]}", flush=True)
    time.sleep(1)

(D / "_verified_0916.json").write_text(json.dumps(out, indent=1))
live = [r for r in rows if r["http_ok"] and r["days_old"] is not None and r["days_old"] <= 10]
print(f"\nverified {len(rows)} URLs | live-and-fresh (<=10d): {len(live)}")
for r in sorted(live, key=lambda x: x["days_old"]):
    print(f"  {r['days_old']:>3}d feed={'Y' if r['in_ai_topic_feed'] else 'n'} {r['headline']} | {r['slug']}")
