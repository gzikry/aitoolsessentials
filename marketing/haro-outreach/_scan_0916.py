import re, json, os

D = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
s = open("/tmp/sitemap_0916.xml", errors="ignore").read()
print("sitemap bytes", len(s))

pairs = re.findall(r'<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>', s)
print("loc/lastmod pairs", len(pairs))
slugs = {}
for loc, lm in pairs:
    m = re.search(r'/journo-request/([a-z0-9\-]{5,160})', loc)
    if m:
        sl = m.group(1)
        if sl not in slugs or lm > slugs[sl]:
            slugs[sl] = lm
print("unique slugs", len(slugs))
lms = sorted(slugs.values())
print("newest lastmod", lms[-1], "oldest", lms[0])

SINCE = "2026-09-02"
recent = {k: v for k, v in slugs.items() if v >= SINCE}
print("slugs lastmod >=", SINCE, len(recent))
# Since yesterday's run marker (2026-09-15T09:00 PDT = 16:00Z)
tight = {k: v for k, v in slugs.items() if v >= "2026-09-15T16:00:00"}
print("slugs lastmod >= 2026-09-15T16:00Z (since last run)", len(tight))

AI_TOKENS = {"ai","a-i","artificial","llm","llms","gpt","chatgpt","claude","copilot","gemini","openai","anthropic","agent","agents","agentic","machine","automation","automate","saas","software","tool","tools","tech","technology","chatbot","model","models","genai"}
STRICT = {"pricing","price","prices","cost","costs","budget","budgets","subscription","subscriptions","spend","spending","credit","credits","billing","invoice","invoices","renewal","renewals","overlap","overlapping","consolidat","consolidation","finops","seat","seats","license","licenses","licence","licences","expense","expenses","fees","rate","rates","cheaper","expensive"}
THIRD = {"pay","paying","paid","cancel","cancelling","canceled","stack","sprawl","waste","wasted","tooling","duplicate","duplicates","redundant","procurement","cfo","audit","audits","tco","roi"}


def tokens(sl):
    return set(sl.lower().split("-"))


ai = {k: v for k, v in recent.items() if tokens(k) & AI_TOKENS}
strict = {k: v for k, v in recent.items() if tokens(k) & STRICT}
strict_ai = {k: v for k, v in strict.items() if tokens(k) & AI_TOKENS}
third = {k: v for k, v in recent.items() if tokens(k) & THIRD}
third_ai = {k: v for k, v in third.items() if tokens(k) & AI_TOKENS}

print("broad AI-token matches", len(ai))
print("strict pricing/cost matches", len(strict), "of which AI co-occur", len(strict_ai))
print("third tier matches", len(third), "of which AI co-occur", len(third_ai))

json.dump({"sitemap_bytes": len(s), "pairs": len(pairs), "unique_slugs": len(slugs),
           "newest": lms[-1], "since_0902": len(recent), "tight_since_0915": len(tight),
           "ai": ai, "strict": strict, "strict_ai": strict_ai, "third_ai": third_ai},
          open(f"{D}/_scan_0916.json", "w"), indent=1)

print("\n--- NEW since last run marker (tight) ---")
for k in sorted(tight, key=lambda k: tight[k], reverse=True):
    print(tight[k], k, "|AI" if tokens(k) & AI_TOKENS else "", "|STRICT" if tokens(k) & STRICT else "", "|3rd" if tokens(k) & THIRD else "")

print("\n--- STRICT x AI (whole window) ---")
for k in sorted(strict_ai, key=lambda k: strict_ai[k], reverse=True):
    print(strict_ai[k], k)
print("\n--- THIRD x AI (whole window) ---")
for k in sorted(third_ai, key=lambda k: third_ai[k], reverse=True):
    print(third_ai[k], k)
