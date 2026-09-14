#!/usr/bin/env python3
"""Refined AI/software slug filter + extractor verification."""
import re, json, subprocess, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
BASE = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/"


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True)
    return r.stdout


def field(raw, key):                       # escaped or plain JSON string
    m = re.search(r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) \
        or re.search(r'"' + key + r'":"((?:[^"\\]|\\.)*?)"', raw)
    return m.group(1).replace("\\n", "\n").replace('\\"', '"').strip() if m else None


# --- token-based AI/software filter -------------------------------------
TOKENS = ["ai", "artificial-intelligence", "saas", "software", "agent", "agents",
          "agentic", "llm", "chatgpt", "claude", "openai", "anthropic", "copilot",
          "cursor", "tool", "tools", "tech", "startup", "startups", "automation",
          "subscription", "subscriptions", "productivity", "finops", "data-center",
          "datacenter"]


def slug_hit(slug):
    parts = slug.split("-")
    hits = set()
    for i, p in enumerate(parts):
        if p in TOKENS:
            hits.add(p)
    # multi-word
    if "artificial" in parts and "intelligence" in parts:
        hits.add("artificial-intelligence")
    return sorted(hits)


def main():
    data = json.load(open(BASE + "_scan2.json"))
    print("scan cutoff:", data["cutoff"], "| recent:", data["recent"])

    # ---------- 0. extractor health check ----------
    probe_url = "https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns"
    raw = curl(probe_url)
    h, d, dp = field(raw, "headline"), field(raw, "description"), field(raw, "datePublished")
    print("\n=== EXTRACTOR HEALTH ===")
    print("bytes:", len(raw), "| headline:", (h or "NONE")[:80])
    print("datePublished:", dp, "| description chars:", len(d or ""))
    if not h or not d or len(d) < 100:
        print("!!! EXTRACTOR BROKEN - stopping")
        sys.exit(2)
    print("extractor OK")

    # ---------- 1. refined AI/software filter ----------
    seen, rows = set(), []
    for entry in data["broad"]:
        url, lm = entry["url"], entry["lastmod"]
        slug = url.rstrip("/").split("/journo-request/")[-1]
        if slug in seen:
            continue
        seen.add(slug)
        hits = slug_hit(slug)
        if hits:
            rows.append({"slug": slug, "lastmod": lm, "kw": hits, "url": url})
    rows.sort(key=lambda r: r["lastmod"], reverse=True)
    print(f"\n=== AI/SOFTWARE SLUG MATCHES (since {data['cutoff']}): {len(rows)} ===")
    for r in rows:
        print(f"[{r['lastmod'][:16]}] {r['slug'][:95]} | {','.join(r['kw'][:4])}")

    # ---------- 2. new since yesterday's run ----------
    NEW_CUT = "2026-09-12T09:00:00"
    new = [r for r in rows if r["lastmod"] > NEW_CUT]
    print(f"\n=== NEW SINCE 2026-09-12T09:00Z (last run): {len(new)} ===")
    for r in new:
        print(f"[{r['lastmod'][:16]}] {r['slug']}")

    json.dump(rows, open(BASE + "_ai_slugs2.json", "w"), indent=1)


main()
