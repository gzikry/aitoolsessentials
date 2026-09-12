#!/usr/bin/env python3
"""Sourcee sitemap scan for journo requests matching the AIToolsEssentials beat."""
import re, json, subprocess, sys, os

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/_scan.json"

BROAD = ["ai-", "ai-", "artificial-intelligence", "ai", "tool", "software", "saas",
         "budget", "agent", "tech", "subscri", "app", "startup", "subscription"]
STRICT = ["pricing", "cost", "price", "subscription", "subscri", "spend", "spending",
          "credit", "renewal", "overlap", "consolidat", "finops", "budget", "expense", "bill"]


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True)
    return r.stdout


def main():
    raw = curl("https://www.sourcee.app/sitemap-journo-requests.xml", 90)
    pairs = re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", raw)
    print("total sitemap URLs:", len(pairs))
    if not pairs:
        print("SITEMAP FETCH FAILED. first 300 chars:", raw[:300])
        sys.exit(1)
    pairs.sort(key=lambda p: p[1], reverse=True)
    print("newest lastmod:", pairs[0][1], "| oldest:", pairs[-1][1])

    cutoff = sys.argv[1] if len(sys.argv) > 1 else "2026-09-02"
    recent = [p for p in pairs if p[1] >= cutoff]
    print(f"requests with lastmod >= {cutoff}:", len(recent))

    broad, strict = [], []
    for url, lm in recent:
        u = url.lower()
        hits = [k for k in BROAD if k in u]
        shits = [k for k in STRICT if k in u]
        if hits:
            broad.append({"url": url, "lastmod": lm, "kw": hits, "strict": shits})
        if shits:
            strict.append({"url": url, "lastmod": lm, "kw": shits})

    print("broad matches:", len(broad), "| strict matches:", len(strict))
    with open(OUT, "w") as f:
        json.dump({"cutoff": cutoff, "total": len(pairs), "recent": len(recent),
                   "broad": broad, "strict": strict}, f, indent=1)

    print("\n--- STRICT (ranked, most recent first) ---")
    for i, b in enumerate(strict[:45], 1):
        print(f"{i}. [{b['lastmod']}] {b['url'].split('/journo-request/')[-1][:95]} | {','.join(b['kw'])}")


main()
