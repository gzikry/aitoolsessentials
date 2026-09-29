#!/usr/bin/env python3
"""Dig the four new AI-token candidates' raw pages for the request's original source URL and
any author handle — i.e. anything that resolves into an actual reply route."""
import json, re, subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
SLUGS = ["insurance-agents-ai-use-in-personal-lines",
         "b2b-marketing-leaders-hyperspecialization-to-outcompete-ai",
         "ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes",
         "data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity"]


def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


for slug in SLUGS:
    code, raw = curl(f"https://www.sourcee.app/journo-request/{slug}")
    print("=" * 100)
    print(slug, code, len(raw))
    for key in ("source", "sourceUrl", "url", "author", "authorUrl", "handle", "twitter",
                "linkedin", "postedBy", "contactMethod", "contact", "publication", "domain",
                "image", "deadline", "expires"):
        vals = sorted(set(re.findall(r'"' + key + r'":\s*"([^"]{1,200})"', raw)))
        vals = [v for v in vals if "sourcee.app" not in v or key in ("url", "source")]
        if vals:
            print(f"  {key}: {vals[:4]}")
    social = sorted(set(re.findall(r'https?://(?:www\.)?(?:x\.com|twitter\.com|linkedin\.com|instagram\.com|t\.co|bit\.ly)/[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{2,120}', raw)))
    print("  social/short links:", social[:10])
