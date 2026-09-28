#!/usr/bin/env python3
"""Fetch and read the 2026-09-28 candidate slugs in full (2 AI-token + 3 spend-any)."""
import json, re, subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

CANDIDATES = [
    "instinct-employees-and-ai-founders-user-growth-analysis",
    "firms-implementing-ai-apprenticeship-replacement-training-playbook",
    "homeowners-facing-mortgage-repayment-pressure-rate-hike-impact",
    "ottawa-community-resource-users-stories-about-lowcost-initiatives",
    "retirees-55-in-us-affordable-retirement-picks-and-pitfalls",
]

def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)

out = {}
for slug in CANDIDATES:
    url = f"https://www.sourcee.app/journo-request/{slug}"
    code, raw = curl(url)
    # body text
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    badge = re.search(r"Posted\s+(?:in the last|in last|)\s*([0-9]+|a few|several)?\s*(?:days?|hours?|weeks?|minutes?)\s*ago", txt, re.I)
    pub = re.search(r"datePublished\"?\s*[:=]\s*\"([^\"]+)\"", raw)
    author = re.search(r'datePublished', raw)
    out[slug] = {"url": url, "http": code, "bytes": len(raw),
                 "badge": (badge.group(0) if badge else None),
                 "datePublished": (pub.group(1) if pub else None),
                 "text": txt[:2600]}
    print("=" * 100)
    print(slug, "| HTTP", code, "|", len(raw), "bytes")
    print("BADGE:", out[slug]["badge"], "| datePublished:", out[slug]["datePublished"])
    print(txt[:1800])

(D / "_candidates_0928.json").write_text(json.dumps(out, indent=1))
