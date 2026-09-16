#!/usr/bin/env python3
"""Re-verify carried requests by URL: HTTP status + the page's own freshness badge.

The badge is the authoritative signal. Sourcee renders one of:
  * "Posted in last 7 days"  (or "Posted today" / "Posted N days ago")  -> still live
  * "Posted N days ago" where N > 7                                     -> live but aging
  * no badge + a removal notice in the rendered body                    -> gone
A previous run read 'expired' out of the site's JS bundle and mis-called live pages dead,
so this looks only at the rendered badge and the visible body text.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")

DEFAULT = [
    "finops-professionals-agentic-ai-cost-overruns",
    "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "employees-hiding-knowledge-from-workplace-ai-want-pay-for-ai-data",
    "ai-startups-workplace-fraud-detection-expenses-time-theft",
    "scientists-phd-students-and-postdocs-paying-for-ai-subscriptions",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    "ceos-ai-impact-on-ops-culture-and-commercial-strategy",
    "enterprise-ai-leaders-value-creation-ownership-and-governance",
    "edtech-product-managers-lms-audit-does-product-manage-learning",
    "us-founders-calls-to-slow-ai-development-impact-on-companies",
    "ukraine-tech-builders-and-global-observers-commercial-tech-adaptation",
    "cybersecurity-companies-and-experts-ai-scams-and-consumer-safety",
]


def fetch(url: str) -> tuple[str, str]:
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    code = m.group(1) if m else "?"
    return code, raw[:raw.rfind("__HTTP__")] if m else raw


def visible(page: str) -> str:
    body = re.sub(r"<script.*?</script>", " ", page, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", txt).strip()


def parse(html: str) -> dict:
    badge = re.findall(r'rounded-full[^>]*>([^<]{0,40})</span>', html)
    badge = [b.strip() for b in badge if "posted" in b.lower()]
    vis = visible(html)
    removed = "has been removed or is no longer available" in vis
    # The removal notice appears in the JS payload of every page; only trust it if the
    # visible body is short (i.e. we actually got the error page, not a request).
    error_page = removed and len(vis) < 1500
    # The published reply route, from the rendered body only.
    emails = [e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", vis)
              if "sourcee" not in e.lower()]
    routes = []
    if re.search(r"email redacted", vis, re.I):
        routes.append("email withheld on page (platform redaction)")
    if emails:
        routes.append("email: " + ", ".join(sorted(set(emails))[:3]))
    for pat, label in ((r"lnkd\.in/\S+", "linkedin short link"),
                       (r"linkedin\.com/in/\S+", "LinkedIn profile"),
                       (r"calendly\.com/\S+", "calendly"),
                       (r"reply to this thread", "reply in thread"),
                       (r"\bDM me\b", "DM the author")):
        if re.search(pat, vis, re.I):
            routes.append(label)
    return {"badge": badge[0] if badge else None, "removed_notice": removed,
            "error_page": error_page, "reply_routes": routes, "visible_chars": len(vis)}


def main() -> None:
    slugs = sys.argv[1:] or DEFAULT
    out = {}
    for sl in slugs:
        url = f"https://www.sourcee.app/journo-request/{sl}"
        code, html = fetch(url)
        info = parse(html)
        rec = {"url": url, "http": code, "bytes": len(html), **info}
        out[sl] = rec
        verdict = "LIVE" if (code == "200" and not info["error_page"]) else "GONE"
        print(f"{verdict:<4} {code} badge={info['badge']!r:<26} routes={info['reply_routes']} {sl}", flush=True)
        time.sleep(1)
    (OUT / "_verify_0916.json").write_text(json.dumps(out, indent=1))
    live = [k for k, v in out.items() if v["http"] == "200" and not v["error_page"]]
    print(f"\nlive {len(live)}/{len(out)}")
    for k in live:
        print("  LIVE:", k, "|", out[k]["badge"])


if __name__ == "__main__":
    main()
