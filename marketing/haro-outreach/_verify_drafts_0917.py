"""Verify every number quoted in pitch-drafts-2026-09-17.md against the data files.

A pitch that cites a wrong number is worse than no pitch: the Amplemarket writer explicitly
re-checks figures against their source, and the 2026-09-15 send had to be corrected for exactly
this. So each claim is asserted here, not eyeballed.
"""
import json
import re
import sys
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
tools = json.loads((S / "data/tools.json").read_text())
snaps = json.loads((S / "data/pricing_snapshots.json").read_text())["snapshots"]
srcs = json.loads((S / "data/tool_sources.json").read_text())
drafts = (S / "marketing/haro-outreach/pitch-drafts-2026-09-17.md").read_text()

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
NOPRICE = re.compile(r"(does not publish a self-serve|did not publish a self-serve|"
                     r"No official USD seat price is reported|"
                     r"No official USD seat or credit price is reported|"
                     r"No official paid consumer|no public pricing page|"
                     r"do not publish)", re.I)
nop = sorted(k for k, v in snaps.items()
             if NOPRICE.search(v.get("digest", "")) and "free and unlimited" not in v.get("digest", ""))
check("7 of 76 have an unpublished paid-tier price", len(nop) == 7, f"{len(nop)}: {nop}")

# 5. the named opaque tools actually say so, with the check dates the draft implies
for slug, needle, dt in (("harvey", "does not publish", "2026-08-26"),
                         ("spellbook", "does not publish", "2026-08-26"),
                         ("dragon-copilot", "does not publish", "2026-08-26"),
                         ("pika", "did not publish", "2026-08-28")):
    d = snaps.get(slug, {}).get("digest", "")
    got = snaps.get(slug, {}).get("date")
    check(f"{slug} says it publishes no self-serve price", needle in d.lower(), f"checked {got}")
    check(f"{slug} check date is {dt}", got == dt, str(got))

# 6. the price pairs, exactly as quoted
PAIR_RE = (r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month"
           r"[^.;]{0,40}?\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month"
           r"\s*(?:billed\s+)?annual")
PAIRS = {"browse-ai": (48.00, 19.00, "2026-09-01"),
         "fathom": (20.00, 16.00, "2026-08-21"),
         "fireflies": (18.00, 10.00, "2026-08-21"),
         "otter-ai": (16.99, 8.33, "2026-08-21")}
for slug, (mo, an, dt) in PAIRS.items():
    d = " ".join(snaps[slug]["digest"].split())
    found = None
    for m in re.finditer(PAIR_RE, d, re.I):
        if abs(float(m.group(1)) - mo) < 0.005 and abs(float(m.group(2)) - an) < 0.005:
            found = (float(m.group(1)), float(m.group(2)))
    check(f"{slug}: ${mo} monthly vs ${an} annual appear as a quoted pair",
          found is not None, f"parsed={found} date={snaps[slug]['date']}")
    check(f"{slug}: check date {dt} matches the data", snaps[slug]["date"] == dt, snaps[slug]["date"])

# 7. "up to 2.5x" — the widest of the verified monthly/annual pairs
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

# 8. Meetings category membership — the three notetakers are the whole category
meet = sorted(t["name"] for t in tools if t["category"] == "Meetings")
check("Meetings holds exactly Fathom, Fireflies.ai, Otter.ai",
      meet == ["Fathom", "Fireflies.ai", "Otter.ai"], str(meet))

# 9. Claude figures, in both files, with the dates the draft states
CL = {"$17": True, "$200": True, "$100/seat/month": False}
cd = " ".join(snaps["claude"]["digest"].split())
check("claude snapshot says Pro $17 with a $200 annual prepayment or $20 month-to-month",
      "$17" in cd and "$200" in cd and "$20" in cd, snaps["claude"]["date"])
check("claude snapshot date is 2026-08-21", snaps["claude"]["date"] == "2026-08-21", snaps["claude"]["date"])
check("claude snapshot lists Max from $100/month", "Max starts at $100" in cd, "")
ts = next(t for t in srcs["tools"] if t["slug"] == "claude")
sd = " ".join((ts.get("pricing_summary") or "").split())
check("tool_sources lists Team Standard $20 and Premium $100 per seat",
      "$20 per seat per month" in sd and "$100 per seat per month" in sd, ts.get("pricing_checked_date"))
check("tool_sources claude check date is 2026-08-25",
      ts.get("pricing_checked_date") == "2026-08-25", str(ts.get("pricing_checked_date")))

# 10. the drafts do not name George, and are signed
check("drafts never present George's name as the sender",
      not re.search(r"(?i)\b(regards|thanks|best|from|sincerely)\s*,?\s*george\b", drafts),
      "no sign-off naming George")
# Every mention of George must be either the route-ownership note ("George's lane", "(George)")
# or the prose sentence "No draft names George." — never a sender identity.
mentions = re.findall(r"(?i)george[^\s]*", drafts)
allowed = {"george's", "george)", "george."}
check("every 'George' mention is a route-ownership note or prose, never a sender",
      all(m.lower() in allowed for m in mentions), f"{sorted(set(m.lower() for m in mentions))}")
check("no draft signs off as George",
      not re.search(r"(?im)^>\s*(george|—\s*george)\s*$", drafts))
check("drafts signed AIToolsEssentials", drafts.count("AIToolsEssentials") >= 3,
      f"{drafts.count('AIToolsEssentials')}")
check("draft 2 keeps the no-contract disclosure",
      "haven't signed" in drafts and "have not signed" in drafts)

# 11. each of the three draft bodies is under 200 words. A body is the contiguous run of `>`
# lines from the opener through the standing opt-out footer, less the signature block. The
# split must be on the signature LINE ("> AIToolsEssentials"), not on the string
# "AIToolsEssentials" — draft 2 names the site mid-sentence inside its body, and splitting on
# the bare string truncated that body to 38 words and hid its real length.
blocks = re.findall(r"((?:^>[^\n]*\n|^>\s*\n)+)", drafts, re.M)
bodies = []
for b in blocks:
    if not re.search(r"(?m)^>\s*AIToolsEssentials\s*$", b):
        continue
    body = re.split(r"(?m)^>\s*AIToolsEssentials\s*$", b)[0]
    bodies.append((len(re.findall(r"[A-Za-z']+", body)), body.strip().split("\n")[0][:46]))
check("three draft bodies found", len(bodies) == 3, f"{len(bodies)}")
check("every draft body is under 200 words", all(c < 200 for c, _ in bodies), f"{bodies}")
check("all three draft bodies are non-trivial", all(c > 60 for c, _ in bodies),
      f"{[c for c, _ in bodies]}")

# 12. every request URL in the drafts is page-verified, and none is an index page
verified = json.loads((S / "marketing/haro-outreach/verified-requests.json").read_text())
draft_urls = set(re.findall(r"https://www\.sourcee\.app/journo-request/[a-z0-9\-]+", drafts))
missing = {u for u in draft_urls
           if u.rstrip("/").split("/journo-request/")[-1] not in verified}
check("every drafted request URL is page-verified", not missing, str(missing))
check("no drafted URL is a browse/index page",
      not any("/topics/" in u or "/media-outlets/" in u for u in draft_urls), str(sorted(draft_urls)))
for u in sorted(draft_urls):
    slug = u.split("/journo-request/")[-1]
    v = verified[slug]
    check(f"{slug} verified live this run", v.get("live") and v.get("checked") == "2026-09-17",
          f"live={v.get('live')} checked={v.get('checked')} days={v.get('days_old')}")

# 13. the ages stated in the drafts match the page-verified ages
for slug, stated in (("finops-professionals-agentic-ai-cost-overruns", 10),
                     ("amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot", 10),
                     ("anthropic-users-and-business-owners-customer-service-experiences", 5)):
    got = verified[slug].get("days_old")
    check(f"{slug} draft states {stated}d and the page says {got}d", got == stated, str(got))

# 14. the published routes the drafts name
check("draft 1 names the LinkedIn route it depends on",
      "linkedin.com/in/niloy-ghosh" in drafts)
check("draft 2 names the verified email route", "contact@marketintelligencetools.com" in drafts)
check("draft 3 names the Signal handle", "hliwrites.99" in drafts)
check("draft 3 does not claim we reported a support failure",
      "I don't have a support failure to give you" in drafts)
check("the drafts record that nothing was sent",
      "None of these has been sent" in drafts)

print()
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
