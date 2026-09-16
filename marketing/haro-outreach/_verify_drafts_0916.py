"""Verify every number quoted in pitch-drafts-2026-09-16.md against the data files.

A pitch that cites a wrong number is worse than no pitch: the Amplemarket writer explicitly
re-checks figures against their source, and yesterday's send had to be corrected for exactly
this. So each claim is asserted here, not eyeballed.
"""
import json, re, sys
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
tools = json.loads((S / "data/tools.json").read_text())
snaps = json.loads((S / "data/pricing_snapshots.json").read_text())["snapshots"]
drafts = (S / "marketing/haro-outreach/pitch-drafts-2026-09-16.md").read_text()

ok = True


def check(label, cond, detail=""):
    global ok
    print(f"{'PASS' if cond else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))
    if not cond:
        ok = False


# 1. "76 AI tools"
check("76 tools tracked", len(tools) == 76, f"len={len(tools)}")

# 2. "70 of the 76 sit in the 13 categories holding three or more"
cats: dict[str, int] = {}
for t in tools:
    cats[t["category"]] = cats.get(t["category"], 0) + 1
three_plus = {k: v for k, v in cats.items() if v >= 3}
check("13 categories hold >=3 tools", len(three_plus) == 13, f"{len(three_plus)}")
check("those hold 70 tools", sum(three_plus.values()) == 70, f"{sum(three_plus.values())}")

# 3. "29 of 76 publish both monthly and annual"
both = [k for k, v in snaps.items()
        if re.search(r"(monthly|/month|month-to-month)", v.get("digest", ""), re.I)
        and re.search(r"(annual|/year|yearly)", v.get("digest", ""), re.I)]
check("29 of 76 quote monthly + annual", len(both) == 29, f"{len(both)}")

# 4. "7 of 76 publish no price for the paid tier"
# Criterion: the vendor has a paid tier whose price its own sources do not publish. This excludes
# OpenEvidence ("free and unlimited for healthcare professionals" — there is no paid tier to
# price) and excludes tools that publish self-serve pricing and only leave the top enterprise
# tier sales-led (ChatGPT, Make, Slack AI).
NOPRICE = re.compile(r"(does not publish a self-serve|did not publish a self-serve|"
                     r"No official USD seat price is reported|"
                     r"No official USD seat or credit price is reported|"
                     r"No official paid consumer|no public pricing page|"
                     r"do not publish)", re.I)
nop = sorted(k for k, v in snaps.items()
             if NOPRICE.search(v.get("digest", "")) and "free and unlimited" not in v.get("digest", ""))
check("7 of 76 have an unpublished paid-tier price", len(nop) == 7, f"{len(nop)}: {nop}")
check("OpenEvidence is excluded as a free product, not a pricing-opacity case",
      "openevidence" not in nop and "free and unlimited" in snaps["openevidence"]["digest"])

# 5. the named opaque tools actually say so
for slug, needle in (("harvey", "does not publish"), ("spellbook", "does not publish"),
                     ("dragon-copilot", "does not publish"), ("pika", "did not publish")):
    d = snaps.get(slug, {}).get("digest", "")
    check(f"{slug} says it publishes no self-serve price", needle in d.lower(),
          f"checked {snaps.get(slug,{}).get('date')}")

# 6. the four price pairs, exactly as quoted (compare numerically, not as substrings)
PAIRS = {"browse-ai": (48.00, 19.00, "2026-09-01"),
         "fathom": (20.00, 16.00, "2026-08-21"),
         "fireflies": (18.00, 10.00, "2026-08-21"),
         "otter-ai": (16.99, 8.33, "2026-08-21")}
PAIR_RE = (r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month"
           r"[^.;]{0,40}?\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month"
           r"\s*(?:billed\s+)?annual")
for slug, (mo, an, dt) in PAIRS.items():
    d = " ".join(snaps[slug]["digest"].split())
    found = None
    for m in re.finditer(PAIR_RE, d, re.I):
        if abs(float(m.group(1)) - mo) < 0.005 and abs(float(m.group(2)) - an) < 0.005:
            found = (float(m.group(1)), float(m.group(2)))
    check(f"{slug}: ${mo} monthly vs ${an} annual appear as a quoted pair",
          found is not None, f"parsed={found} date={snaps[slug]['date']} (draft says {dt})")
    check(f"{slug}: check date {dt} matches the data", snaps[slug]["date"] == dt,
          snaps[slug]["date"])

# 7. "up to 2.5x" — the widest of the eight verified pairs
pairs = []
for k, v in snaps.items():
    d = " ".join(v.get("digest", "").split())
    for m in re.finditer(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month"
                         r"[^.;]{0,40}?\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month"
                         r"\s*billed annual", d, re.I):
        mo, an = float(m.group(1)), float(m.group(2))
        if an > 0 and mo > an:
            pairs.append((mo / an, k, mo, an))
widest = max(pairs)
check("widest monthly/annual premium is 2.5x on browse-ai",
      abs(widest[0] - 2.53) < 0.02 and widest[1] == "browse-ai",
      f"{widest[0]:.2f}x on {widest[1]} ({widest[2]}/{widest[3]})")

# 8. Meetings category membership
meet = sorted(t["name"] for t in tools if t["category"] == "Meetings")
check("Meetings holds Fathom, Fireflies.ai, Otter.ai",
      meet == ["Fathom", "Fireflies.ai", "Otter.ai"], str(meet))

# 9. the drafts do not name George, and are signed
check("drafts never present George's name as the sender",
      not re.search(r"(?i)\b(regards|thanks|best|from|sincerely|—|--)\s*,?\s*george\b", drafts),
      "no sign-off naming George")
check("drafts signed AIToolsEssentials",
      drafts.count("AIToolsEssentials") >= 3, f"{drafts.count('AIToolsEssentials')}")
check("no draft claims an Amplemarket contract was signed",
      "haven't signed" in drafts or "have not signed" in drafts)
# word count of each pitch body, excluding the signature and the standing opt-out footer
bodies = re.findall(r"(?:^> .*$\n?)+", drafts, re.M)
counts = []
for b in bodies:
    body = b.split("AIToolsEssentials\n")[0] if "AIToolsEssentials\n" in b else b
    counts.append(len(re.findall(r"[A-Za-z']+", body)))
check("every draft body is under 200 words", all(c < 200 for c in counts), f"counts={counts}")

# 10. every request URL in the drafts is in the verified set
verified = json.loads((S / "marketing/haro-outreach/verified-requests.json").read_text())
draft_urls = set(re.findall(r"https://www\.sourcee\.app/journo-request/[a-z0-9\-]+", drafts))
missing = {u for u in draft_urls
           if u.rstrip("/").split("/journo-request/")[-1] not in verified}
check("every drafted request URL is page-verified", not missing, str(missing))

print()
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
