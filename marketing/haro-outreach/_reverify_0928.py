#!/usr/bin/env python3
"""Step 2: re-verify every carried URL in the previous digest by fetching its page.

Records HTTP code, page bytes, the page's own 'Posted ... ago' badge, JSON-LD datePublished and
whether the request body is still served. Ages are read off the page, never off the digest text.
"""
import json, re, subprocess, sys
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

prev = json.loads((D / "digest-2026-09-27.json").read_text())
urls = [o["url"] for o in prev["opportunities"]]
print(f"carried URLs to re-verify: {len(urls)}", file=sys.stderr)

def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)

out = []
for i, url in enumerate(urls, 1):
    code, raw = curl(url)
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    b = re.search(r"Posted\s+(in the last 7 days|in last 7 days|in the last|today|yesterday|"
                  r"[0-9]+\s*(?:days?|hours?|weeks?|minutes?)\s*ago)", txt, re.I)
    pub = re.search(r'"datePublished"\s*:\s*"([^"]+)"', raw)
    expired = bool(re.search(r"expired|no longer accepting|closed|this request has been removed", txt, re.I))
    has_body = "Brought to you by Sourcee" in raw
    rec = {"url": url, "http": code, "bytes": len(raw),
           "badge": (b.group(1) if b else None),
           "datePublished": (pub.group(1) if pub else None),
           "body_served": has_body, "expiry_word_seen": expired}
    out.append(rec)
    print(f"{i:>2}/{len(urls)} {code} {len(raw):>7} {str(rec['badge']):<22} {url.split('/')[-1][:62]}", file=sys.stderr)

(D / "_reverify_0928.json").write_text(json.dumps(out, indent=1))
print(json.dumps({"checked": len(out),
                  "non200": [r["url"] for r in out if r["http"] != "200"],
                  "body_missing": [r["url"] for r in out if not r["body_served"]],
                  "expiry_words": [r["url"] for r in out if r["expiry_word_seen"]]}, indent=1))
