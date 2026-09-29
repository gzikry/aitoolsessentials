#!/usr/bin/env python3
"""Step 2b: refresh the page-verified facts for all 47 tracked requests (today's run).

Writes verified-requests.json for every tracked slug, so build_pitch_queue.py's age comes off
today's page read rather than a stale cache. Then prints the live/cold split.
"""
import json, re, subprocess, sys, time
from datetime import date
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

rows = json.loads((D / "_reverify_0929.json").read_text())
cache = json.loads((D / "verified-requests.json").read_text())

FEED = json.loads((D / "ai-topic-feed.json").read_text()) if (D / "ai-topic-feed.json").exists() else {}


def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def field(raw, key):
    for pat in (r'"' + key + r'":\s*"((?:[^"\\]|\\.)*?)"',
                r'\\+"' + key + r'\\+":\\+"((?:[^"\\]|\\.)*?)\\+"'):
        m = re.search(pat, raw)
        if m:
            v = m.group(1)
            for _ in range(3):
                n = v.replace("\\n", " ").replace("\\u0026", "&").replace("\\/", "/")
                n = re.sub(r'\\(.)', r'\1', n)
                if n == v:
                    break
                v = n
            return v.strip()
    return None


def age_days(stamp):
    if not stamp:
        return None
    from datetime import datetime, timezone
    try:
        return (datetime.now(timezone.utc) - datetime.fromisoformat(stamp.replace("Z", "+00:00"))).days
    except ValueError:
        pass
    m = re.match(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})", stamp)
    if not m:
        return None
    from datetime import datetime, timezone
    return (datetime.now(timezone.utc)
            - datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}+00:00")).days


CHROME = ("sourcee.app", "vercel", "sentry", "nextjs.org", "schema.org", "w3.org", "gstatic",
          "google.com/s2", "supabase.co", "redditstatic", "preview.redd.it",
          # Sourcee's OWN social accounts appear on every request page. The 2026-09-29 run's
          # refresh script dropped these two from the list, which populated `published_links` on
          # a comment-only Forbes request and made the queue's `_sendable()` count it as having a
          # usable route. Kept here so a page's own chrome can never read as a reply route.
          "linkedin.com/in/andrewsmith313", "x.com/andy_cb_smith")

out = {}
for r in rows:
    url = r["url"]
    code, raw = curl(url)
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial(.*?)Brought to you by Sourcee", txt, re.S)
    core = (m.group(1).strip() if m else "")
    dp = field(raw, "datePublished")
    badge = re.search(r"(Posted (?:in last 7 days|today|yesterday|\d+ (?:days?|hours?) ago))", core)
    slug = url.rstrip("/").split("/journo-request/")[-1]
    links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,160}", raw)))
             if not any(c in u for c in CHROME)]
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core)
                        if "sourcee" not in e.lower()))
    out[slug] = {
        "url": url, "slug": slug, "http": code,
        "live": code == "200" and bool(core),
        "headline": field(raw, "headline"),
        "datePublished": dp, "days_old": age_days(dp),
        "badge": badge.group(1) if badge else None,
        "domain": field(raw, "domain"),
        "in_ai_topic_feed": slug in set(FEED.get("slugs") or []),
        "email_redacted": bool(re.search(r"email redacted", core, re.I)),
        "emails_on_page": emails,
        "published_links": links[:6],
        "reply_hints": sorted({h for h in ("DM me", "DM or email", "reply to this thread", "Comment",
                                           "schedule time", "email me", "shoot me a DM", "Signal")
                               if h.lower() in core.lower()}),
        "checked": date.today().isoformat(),
    }
    print(f"{slug[:60]:<62} {code} {str(out[slug]['days_old']):>4}d "
          f"badge={str(out[slug]['badge']):<20} dp={dp}", file=sys.stderr)
    time.sleep(0.4)

cache.update(out)
for k in [k for k in cache if k.startswith("http")]:
    v = cache.pop(k)
    cache[v.get("slug") or k] = v
(D / "verified-requests.json").write_text(json.dumps(cache, indent=1))
print(json.dumps({"cached": len(cache), "refreshed": len(out),
                  "non200": [r["url"] for r in out.values() if r["http"] != "200"],
                  "not_live": [r["url"] for r in out.values() if not r["live"]]}, indent=1))
