#!/usr/bin/env python3
"""Sitemap-based candidate scan for 2026-09-18.

Reads /tmp/sitemap_journo_0918.xml (sitemap-index child; the old /sitemap.xml now returns
only an index of 8 children, so pointing the scan at it produced 0 pairs and silently zeroed
every downstream signal - the 2026-09-18 run is the first to read sitemap-journo-requests.xml
directly).
"""
import json
import re
import sys
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
XML = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sitemap_journo_0918.xml"
SINCE = "2026-09-11"

raw = Path(XML).read_text(errors="ignore")
pairs = re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", raw)
slugs: dict[str, str] = {}
for loc, lm in pairs:
    m = re.search(r"/journo-request/([a-z0-9\-]{5,160})", loc)
    if m:
        if m.group(1) not in slugs or lm > slugs[m.group(1)]:
            slugs[m.group(1)] = lm
Path("/tmp/slugs_0918.json").write_text(json.dumps(slugs))
print("pairs", len(pairs), "unique slugs", len(slugs), "newest", max(slugs.values()) if slugs else "-")

AI_TOKENS = {"ai", "a-i", "artificial", "llm", "llms", "gpt", "chatgpt", "claude", "copilot", "gemini",
             "openai", "anthropic", "agent", "agents", "agentic", "machine", "automation", "automate",
             "saas", "software", "tool", "tools", "tech", "technology", "chatbot", "model", "models", "genai"}
STRICT = {"pricing", "price", "prices", "cost", "costs", "budget", "budgets", "subscription",
          "subscriptions", "spend", "spending", "credit", "credits", "billing", "invoice", "invoices",
          "renewal", "renewals", "overlap", "overlapping", "consolidat", "consolidation", "finops",
          "seat", "seats", "license", "licenses", "licence", "licences", "expense", "expenses",
          "fees", "rate", "rates", "cheaper", "expensive"}
THIRD = {"pay", "paying", "paid", "stack", "sprawl", "waste", "wasted", "tooling", "duplicate",
         "duplicates", "redundant", "procurement", "cfo", "audit", "audits", "tco", "roi"}


def tok(s: str) -> set:
    return set(s.lower().split("-"))


recent = {k: v for k, v in slugs.items() if v >= SINCE}
ai = {k: v for k, v in recent.items() if tok(k) & AI_TOKENS}
strict = {k: v for k, v in recent.items() if tok(k) & STRICT}
sai = {k: v for k, v in strict.items() if tok(k) & AI_TOKENS}
tai = {k: v for k, v in recent.items() if (tok(k) & THIRD) and (tok(k) & AI_TOKENS)}
print("slugs lastmod >=", SINCE, len(recent))
print("AI:", len(ai), "STRICT:", len(strict), "STRICTxAI:", len(sai), "THIRDxAI:", len(tai))
for k in sorted(ai, key=lambda k: ai[k], reverse=True):
    print(" AI ", ai[k][:10], k)
print("--- strict x ai ---")
for k in sorted(sai, key=lambda k: sai[k], reverse=True):
    print("   ", sai[k][:10], k)
print("--- third x ai ---")
for k in sorted(tai, key=lambda k: tai[k], reverse=True):
    print("   ", tai[k][:10], k)
(D / "_scan_0918.json").write_text(json.dumps(
    {"recent": recent, "ai": ai, "strict": strict, "strict_ai": sai, "third_ai": tai}, indent=1))
