#!/usr/bin/env python3
"""Fetch every candidate slug from today's window and print its rendered body + route facts.

Reads _window_1001.json, fetches the AI-token and spend-token slugs, and writes
_candidates_1001.json with headline/datePublished/days_old/emails/links/reply_hints so the
judgement is made against the page, not against the slug text.
"""
import json
import re
import subprocess
import time
from datetime import date, datetime, timezone
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
CHROME = ("sourcee.app", "vercel", "sentry", "nextjs.org", "schema.org", "w3.org", "gstatic",
          "google.com/s2", "supabase.co", "redditstatic", "preview.redd.it",
          "linkedin.com/in/andrewsmith313", "x.com/andy_cb_smith")


def curl(url, timeout=40):
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
    try:
        return (datetime.now(timezone.utc) - datetime.fromisoformat(stamp.replace("Z", "+00:00"))).days
    except ValueError:
        pass
    m = re.match(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})", stamp)
    if not m:
        return None
    try:
        return (datetime.now(timezone.utc)
                - datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}+00:00")).days
    except ValueError:
        return None


def visible(raw):
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    return m.group(1).strip() if m else ""


win = json.loads((D / "_window_1001.json").read_text())
slugs = [s for s, _ in win["ai"]] + [s for s, _ in win["spend_any"]]
slugs = list(dict.fromkeys(slugs))
print(f"fetching {len(slugs)} candidates")

out = {}
for s in slugs:
    url = f"https://www.sourcee.app/journo-request/{s}"
    code, raw = curl(url)
    core = visible(raw)
    dp = field(raw, "datePublished")
    links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,180}", raw)))
             if not any(c in u for c in CHROME)]
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core)
                        if "sourcee" not in e.lower()))
    rec = {
        "slug": s, "url": url, "http": code, "live": code == "200" and bool(core),
        "headline": field(raw, "headline"), "domain": field(raw, "domain"),
        "datePublished": dp, "days_old": age_days(dp),
        "body": core[:2600],
        "email_redacted": bool(re.search(r"email redacted", core, re.I)),
        "emails_on_page": emails, "published_links": links[:6],
        "reply_hints": sorted({h for h in ("DM me", "DM or email", "reply to this thread", "Comment",
                                           "schedule time", "email me", "shoot me a DM", "Signal",
                                           "drop me")
                               if h.lower() in core.lower()}),
    }
    out[s] = rec
    print(f"{rec['http']} {rec['days_old']}d {s}")
    print(f"    head: {rec['headline']}")
    print(f"    body: {rec['body'][:300]}")
    print(f"    mails={emails} links={links[:3]} hints={rec['reply_hints']}")
    time.sleep(1)

(D / "_candidates_1001.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote _candidates_1001.json ({len(out)})")
