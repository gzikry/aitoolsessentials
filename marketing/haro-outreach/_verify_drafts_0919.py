"""Assert every number quoted in pitch-drafts-2026-09-19.md against our own data files.

A pitch citing a wrong number is worse than no pitch: the 2026-09-15 send cited a count that had
drifted, and the 2026-09-18 Amplemarket send carried two opacity claims that were simply wrong and
had to be corrected in the reply. So nothing here is eyeballed — each claim is recomputed.
"""
import json
import re
import statistics
import sys
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
tools = json.loads((S / "data/tools.json").read_text())
snapf = json.loads((S / "data/pricing_snapshots.json").read_text())
snaps = snapf["snapshots"]
srcs = json.loads((S / "data/tool_sources.json").read_text())
ver = json.loads((S / "marketing/haro-outreach/verified-requests.json").read_text())
drafts = (S / "marketing/haro-outreach/pitch-drafts-2026-09-19.md").read_text()

ok = True


def check(label, cond, detail=""):
    global ok
    print(f"{'PASS' if cond else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))
    if not cond:
        ok = False


# 1. 76 tools tracked
check("76 tools tracked", len(tools) == 76, f"len={len(tools)}")

# 2. the affordability threshold quoted in drafts 1 and 3
MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {k: (min(float(x) for x in MONTH.findall(" ".join((v.get("digest") or "").split())) if float(x) > 0),
             v.get("date"))
        for k, v in snaps.items()
        if [float(x) for x in MONTH.findall(" ".join((v.get("digest") or "").split())) if float(x) > 0]}
check("40 of 76 publish a non-zero monthly price", len(paid) == 40, f"{len(paid)}")
under25 = {k: v for k, v in paid.items() if v[0] <= 25}
check("31 of those are at or under $25/month", len(under25) == 31, f"{len(under25)}")
med = statistics.median(v[0] for v in paid.values())
check("median cheapest paid monthly tier is $16.50", abs(med - 16.50) < 0.005, f"${med:.2f}")
lo = min(paid.values(), key=lambda x: x[0])
lokey = [k for k, v in paid.items() if v[0] == lo[0]]
check("lowest is $4 (Khanmigo)", lo[0] == 4.0 and lokey == ["khanmigo"], f"${lo[0]} {lokey}")
check("Khanmigo snapshot checked 2026-09-18", snaps["khanmigo"]["date"] == "2026-09-18", snaps["khanmigo"]["date"])

# 3. the same-tier monthly/annual range
PAIR = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(user|seat|member|person)?\s*/?\s*month[^.;$]{0,60}?"
                  r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(user|seat|member|person)?\s*/?\s*month\s*(?:billed\s+)?annual", re.I)
ratios = []
for k, v in snaps.items():
    for m in PAIR.finditer(" ".join((v.get("digest") or "").split())):
        mo, an = float(m.group(1)), float(m.group(3))
        if an > 0 and mo > an and (m.group(2) or "") == (m.group(4) or ""):
            ratios.append((round(mo / an, 2), k, mo, an, v.get("date")))
ratios.sort()
check("same-tier monthly/annual range is 1.21x-2.53x", ratios[0][0] == 1.21 and ratios[-1][0] == 2.53,
      f"{ratios[0][0]}-{ratios[-1][0]}")
check("widest pair is Browse AI $48 vs $19",
      ratios[-1][1] == "browse-ai" and ratios[-1][2] == 48.0 and ratios[-1][3] == 19.0, str(ratios[-1]))
check("narrowest pair is HeyGen $29 vs $24",
      ratios[0][1] == "heygen" and ratios[0][2] == 29.0 and ratios[0][3] == 24.0, str(ratios[0]))
check("both Browse AI figures checked 2026-09-18", snaps["browse-ai"]["date"] == "2026-09-18",
      snaps["browse-ai"]["date"])

# 4. Claude / Anthropic tier figures
cd = " ".join(snaps["claude"]["digest"].split())
check("Claude Pro $17 with $200 annual prepayment or $20 month-to-month",
      "$17" in cd and "$200" in cd and "$20" in cd, snaps["claude"]["date"])
check("Claude Max starts at $100/month", "Max starts at $100 per month" in cd)
ts = next((t for t in srcs["tools"] if t["slug"] == "claude"), None)
sd = " ".join(((ts or {}).get("pricing_summary") or "").split())
# The snapshot's digest field is capped at 200 chars and cuts off mid-sentence after the Standard
# seat price; the Premium seat price only exists in tool_sources. Assert each figure against the
# file that actually holds it, rather than assuming the two files agree.
check("claude snapshot holds Team Standard $20/seat", "$20 per seat per month" in cd)
check("claude tool_sources holds Team Standard $20 and Premium $100 per seat",
      "$20 per seat per month" in sd and "$100 per seat per month" in sd,
      f"pricing_checked_date={ (ts or {}).get('pricing_checked_date') }")
check("claude snapshot checked 2026-09-18", snaps["claude"]["date"] == "2026-09-18", snaps["claude"]["date"])
check("claude snapshot is verified against anthropic.com/pricing",
      "anthropic.com/pricing" in (snaps["claude"].get("verified_against") or ""),
      str(snaps["claude"].get("verified_against")))
check("tool_sources claude pricing_checked_date is 2026-09-18",
      (ts or {}).get("pricing_checked_date") == "2026-09-18", str((ts or {}).get("pricing_checked_date")))
check("the drafts disclose which file holds the Premium seat figure",
      "truncates mid-sentence" in drafts and "data/tool_sources.json" in drafts)

# 5. the routes the drafts depend on
check("draft 1 names the Raconteur byline route", "simon.chandler@raconteur.net" in drafts)
check("draft 1 names the obfuscation mechanism", "data-part1" in drafts and "scripts-last.min.js" in drafts)
check("draft 1 names the control author used to validate the pattern", "id@raconteur.net" in drafts)
check("draft 2 names the Signal handle", "hliwrites.99" in drafts)
check("draft 3 names the resolved editorial address", "holly.shackleton@artichokehq.com" in drafts)
check("draft 1 carries the no-personal-account disclosure",
      "can't give you a personal account" in drafts and "hold no personal account" in drafts)
check("draft 2 does not claim we reported a support failure",
      "I don't have a support failure to give you" in drafts)
check("draft 3 states we are not a food retailer",
      "I'm not a speciality food business" in drafts)
check("draft 3 avoids a £/$ conversion",
      not re.search(r"£\s?\d+(?:,\d{3})*(?:\.\d+)?\s*=|equals £|about £\d", drafts))
check("the drafts record that nothing was sent", "Nothing in this file has been sent" in drafts)

# 6. no draft names George as the sender
mentions = re.findall(r"(?i)george[^\s]*", drafts)
allowed = {"george's", "george)", "george."}
check("every 'George' mention is route-ownership or prose, never a sender",
      all(m.lower() in allowed for m in mentions), f"{sorted(set(m.lower() for m in mentions))}")
check("no draft signs off as George", not re.search(r"(?im)^>\s*(george|—\s*george)\s*$", drafts))
check("drafts signed AIToolsEssentials", drafts.count("AIToolsEssentials") >= 3,
      f"{drafts.count('AIToolsEssentials')}")

# 7. each draft body under 200 words, split on the signature line (draft 2 names the site mid-body)
blocks = re.findall(r"((?:^>[^\n]*\n|^>\s*\n)+)", drafts, re.M)
bodies = []
for b in blocks:
    if not re.search(r"(?m)^>\s*AIToolsEssentials\s*$", b):
        continue
    body = re.split(r"(?m)^>\s*AIToolsEssentials\s*$", b)[0]
    bodies.append((len(re.findall(r"[A-Za-z']+", body)), body.strip().split("\n")[0][:46]))
check("three draft bodies found", len(bodies) == 3, f"{len(bodies)}")
check("every draft body is under 200 words", all(c < 200 for c, _ in bodies), f"{ [c for c,_ in bodies] }")
check("all three draft bodies are non-trivial", all(c > 60 for c, _ in bodies), f"{[c for c, _ in bodies]}")

# 8. every request URL in the drafts is page-verified today, and none is an index page
draft_urls = set(re.findall(r"https://www\.sourcee\.app/journo-request/[a-z0-9\-]+", drafts))
check("no drafted URL is a browse/index page",
      not any("/topics/" in u or "/media-outlets/" in u for u in draft_urls), str(sorted(draft_urls)))
for u in sorted(draft_urls):
    slug = u.split("/journo-request/")[-1]
    v = ver.get(slug)
    check(f"{slug[:58]} page-verified live today",
          bool(v) and v.get("live") and v.get("checked") == "2026-09-19",
          f"live={bool(v) and v.get('live')} checked={v.get('checked') if v else None} days={v.get('days_old') if v else None}")

# 9. the ages stated in the drafts match the page-verified ages
for slug, stated in (("fulltime-employees-shadow-ai-use-and-paying-outofpocket", 2),
                     ("anthropic-users-and-business-owners-customer-service-experiences", 7),
                     ("speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech", 1)):
    got = ver[slug].get("days_old")
    check(f"{slug[:52]} draft states {stated}d and the page says {got}d", got == stated, str(got))

# 10. the FinOps draft is not re-drafted but is pointed at
check("drafts say the FinOps draft already exists and must not be re-drafted",
      "pitch-drafts-2026-09-17.md" in drafts and "do not re-draft" in drafts)

print()
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
