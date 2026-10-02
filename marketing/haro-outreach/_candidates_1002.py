#!/usr/bin/env python3
"""Read today's window candidates in full: each new AI-token slug, plus any spend-token slug."""
import json
import re
import subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
CHROME = ("sourcee.app", "vercel", "sentry", "nextjs.org", "schema.org", "w3.org", "gstatic",
          "google.com/s2", "supabase.co", "redditstatic", "preview.redd.it",
          "linkedin.com/in/andrewsmith313", "x.com/andy_cb_smith")

win = json.loads((D / "_window_1002.json").read_text())
slugs = [s for s, _ in win["ai"]] + [s for s, _ in win["spend_any"]]
seen = []
for s in slugs:
    if s not in seen:
        seen.append(s)


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


out = []
for s in seen:
    url = f"https://www.sourcee.app/journo-request/{s}"
    code, raw = curl(url)
    core = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", core)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    body = (m.group(1).strip() if m else "")
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", txt)
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", txt)
                        if "sourcee" not in e.lower()))
    links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,160}", raw)))
             if not any(c in u for c in CHROME)]
    out.append({"slug": s, "http": code, "bytes": len(raw), "headline": field(raw, "headline"),
                "domain": field(raw, "domain"), "datePublished": field(raw, "datePublished"),
                "badge": badge.group(1) if badge else None,
                "email_redacted": bool(re.search(r"email redacted", txt, re.I)),
                "emails_on_page": emails, "published_links": links[:6],
                "reply_hints": sorted({h for h in ("DM me", "DM or email", "reply to this thread",
                                                   "Comment", "schedule time", "email me",
                                                   "shoot me a DM", "Signal")
                                       if h.lower() in txt.lower()}),
                "body": body})
    print("=" * 100)
    print(f"{code} {len(raw):>8} {s}")
    print(f"  headline: {out[-1]['headline']}")
    print(f"  domain: {out[-1]['domain']}  date: {out[-1]['datePublished']}  badge: {out[-1]['badge']}")
    print(f"  emails={emails} redacted={out[-1]['email_redacted']} hints={out[-1]['reply_hints']}")
    print(f"  links={links[:4]}")
    print(f"  BODY: {body[:1200]}")
    print()

(D / "_candidates_1002.json").write_text(json.dumps(out, indent=1))
print("wrote _candidates_1002.json", len(out), "candidates")
