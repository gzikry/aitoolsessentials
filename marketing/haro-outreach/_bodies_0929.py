#!/usr/bin/env python3
"""Read the full visible body of every live, unpitched tracked request, so the drafts for
today are written from the page text rather than from a carried summary."""
import json, re, subprocess, sys
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

rows = json.loads((D / "_reverify_0929.json").read_text())
led = json.loads((D / "pitch-ledger.json").read_text())
done = {u.rstrip("/").split("/journo-request/")[-1] for u in
        list(led.get("pitched", {})) + list(led.get("skipped", {}))}


def days(badge):
    if not badge:
        return None
    m = re.search(r"(\d+)\s*days?", badge)
    if m:
        return int(m.group(1))
    if "last 7 days" in badge:
        return 3
    return None


urls = [r["url"] for r in rows
        if days(r.get("badge")) is not None and days(r["badge"]) <= 10
        and r["url"].rstrip("/").split("/journo-request/")[-1] not in done]
print(f"live unpitched to read: {len(urls)}", file=sys.stderr)


def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


out = {}
for url in urls:
    code, raw = curl(url)
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial(.*?)Brought to you by Sourcee", txt, re.S)
    core = (m.group(1).strip() if m else txt)
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core)
                        if "sourcee" not in e.lower()))
    links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{12,140}", core)))]
    slug = url.rstrip("/").split("/journo-request/")[-1]
    out[slug] = {"url": url, "http": code, "bytes": len(raw), "body": core[:2000],
                 "emails": emails, "links": links}
    print("=" * 100)
    print(slug, "| HTTP", code, "|", len(raw), "bytes")
    print("EMAILS:", emails, "| LINKS:", links)
    print(core[:1100])

(D / "_bodies_0929.json").write_text(json.dumps(out, indent=1))
