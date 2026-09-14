#!/usr/bin/env python3
"""Sourcee sitemap scan for journo requests matching the AIToolsEssentials beat."""
import re, json, subprocess, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/_scan2.json"

BROAD = ["ai", "tool", "software", "saas", "budget", "agent", "tech",
         "subscri", "startup", "app"]
STRICT = ["pricing", "cost", "price", "subscription", "subscri", "spend",
          "spending", "credit", "renewal", "overlap", "consolidat", "finops",
          "budget", "expense", "bill", "invoice"]


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True)
    return r.stdout


def main():
    raw = curl("https://www.sourcee.app/sitemap-journo-requests.xml", 120)
    pairs = re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", raw)
    print("total sitemap URLs:", len(pairs))
    if not pairs:
        print("SITEMAP FETCH FAILED. first 300 chars:", raw[:300])
        sys.exit(1)
    pairs.sort(key=lambda p: p[1], reverse=True)
    print("newest lastmod:", pairs[0][1], "| oldest:", pairs[-1][1])

    # dedupe by slug
    seen, dedup = set(), []
    for u, lm in pairs:
        slug = u.rstrip("/").split("/journo-request/")[-1]
        if slug and slug not in seen:
            seen.add(slug)
            dedup.append((u, lm))
    print("unique slugs:", len(dedup))

    cutoff = sys.argv[1] if len(sys.argv) > 1 else "2026-09-02"
    recent = [p for p in dedup if p[1] >= cutoff]
    print(f"requests with lastmod >= {cutoff}:", len(recent))

    broad, strict = [], []
    for url, lm in recent:
        u = url.lower()
        hits = sorted({k for k in BROAD if k in u})
        shits = sorted({k for k in STRICT if k in u})
        if hits:
            broad.append({"url": url, "lastmod": lm, "kw": hits, "strict": shits})
        if shits:
            strict.append({"url": url, "lastmod": lm, "kw": shits})

    print("broad matches:", len(broad), "| strict matches:", len(strict))
    with open(OUT, "w") as f:
        json.dump({"cutoff": cutoff, "total": len(pairs), "unique": len(dedup),
                   "recent": len(recent), "broad": broad, "strict": strict}, f, indent=1)

    print("\n--- STRICT (newest first) ---")
    for i, b in enumerate(strict, 1):
        print(f"{i}. [{b['lastmod']}] {b['url'].split('/journo-request/')[-1][:100]} | {','.join(b['kw'])}")

    print("\n--- BROAD not already in strict (newest first) ---")
    sset = {b["url"] for b in strict}
    n = 0
    for b in broad:
        if b["url"] in sset:
            continue
        n += 1
        if n > 70:
            break
        print(f"{n}. [{b['lastmod']}] {b['url'].split('/journo-request/')[-1][:100]}")


main()
