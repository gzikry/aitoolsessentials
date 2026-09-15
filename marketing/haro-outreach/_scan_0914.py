#!/usr/bin/env python3
"""Sourcee sitemap scan + token-based filtering for the 2026-09-14 HARO monitor run."""
import re, json, subprocess, urllib.request

OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# 1. pull sitemap
r = subprocess.run(["curl", "-sL", "-m", "120", "-A", UA,
                    "https://www.sourcee.app/sitemap-journo-requests.xml"],
                   capture_output=True, text=True)
s = r.stdout
print("sitemap bytes:", len(s))
open(f"{OUT}/_sitemap_0914.xml", "w").write(s)

pairs = re.findall(r'<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>', s)
print("loc/lastmod pairs:", len(pairs))
slugs = {}
for loc, lm in pairs:
    m = re.search(r'/journo-request/([a-z0-9\-]+)', loc)
    if m:
        sl = m.group(1)
        if sl not in slugs or lm > slugs[sl]:
            slugs[sl] = lm
print("unique slugs:", len(slugs))
allk = sorted(slugs.values())
print("newest lastmod:", allk[-1], "| oldest:", allk[0])

# 2. window: since 2026-09-02 (keeps a wide net around the beat)
recent = {k: v for k, v in slugs.items() if v >= "2026-09-02"}
print("slugs with lastmod >= 2026-09-02:", len(recent))

def toks(slug):
    return set(slug.lower().split("-"))

BROAD = {"ai", "tool", "tools", "software", "saas", "budget", "agent", "agents",
         "app", "apps", "tech", "platform", "subscription", "subscriptions"}
STRICT = {"pricing", "price", "prices", "cost", "costs", "subscription", "subscriptions",
          "spend", "spending", "credit", "credits", "renewal", "renewals", "overlap",
          "overlapping", "consolidat", "consolidation", "finops", "budget", "budgets"}
WIDE = {"cfo", "finance", "procurement", "licensing", "license", "seat", "seats",
        "audit", "audits", "invoice", "invoices", "billing", "expense", "expenses",
        "usage", "tco", "roi", "vendor", "vendors", "contract", "contracts"}

def match(slug, tier):
    t = toks(slug)
    return bool(t & tier)

broad_hits = {k: v for k, v in recent.items() if match(k, BROAD)}
strict_hits = {k: v for k, v in recent.items() if match(k, STRICT)}
wide_hits = {k: v for k, v in recent.items() if match(k, WIDE)}
ai_only = {k: v for k, v in recent.items() if "ai" in toks(k)}

strict_and_ai = {k: v for k, v in strict_hits.items() if "ai" in toks(k)}
wide_and_ai = {k: v for k, v in wide_hits.items() if "ai" in toks(k)}

print("\nBROAD hits:", len(broad_hits))
print("STRICT hits:", len(strict_hits), "| of which AI co-occur:", len(strict_and_ai))
print("WIDE hits:", len(wide_hits), "| of which AI co-occur:", len(wide_and_ai))
print("AI-token slugs:", len(ai_only))

# 3. what is genuinely NEW since the 2026-09-13 run (lastmod > 2026-09-12T23:59)
new_since = {k: v for k, v in slugs.items() if v > "2026-09-12T23:59:59"}
print("\nNEW since last run (lastmod > 2026-09-12T23:59:59):", len(new_since))
for k, v in sorted(new_since.items(), key=lambda x: x[1], reverse=True):
    print("  ", v, k)

# 4. top on-beat candidates to fetch bodies for
cands = sorted(set(list(strict_and_ai) + list(wide_and_ai) + list(ai_only)),
               key=lambda k: slugs[k], reverse=True)
print("\nCANDIDATE POOL (ai-token or strict+ai):", len(cands))
for c in cands:
    print("  ", slugs[c], c)

json.dump({
    "sitemap_bytes": len(s),
    "pairs": len(pairs),
    "unique_slugs": len(slugs),
    "newest_lastmod": allk[-1],
    "recent_window_count": len(recent),
    "broad": len(broad_hits), "strict": len(strict_hits),
    "strict_and_ai": len(strict_and_ai),
    "wide": len(wide_hits), "wide_and_ai": len(wide_and_ai),
    "ai_token_slugs": len(ai_only),
    "new_since_last_run": new_since,
    "candidate_pool": {c: slugs[c] for c in cands},
    "all_recent": recent,
}, open(f"{OUT}/_scan_0914.json", "w"), indent=2)
print("\nwrote _scan_0914.json")
