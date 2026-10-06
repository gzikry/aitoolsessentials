#!/usr/bin/env python3
"""Verify today's pitch drafts: paste-ready, signed AIToolsEssentials, <200 words, no George name,
and every cited figure present in our own data files."""
import json
import re
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach"
text = (D / "pitch-drafts-2026-10-06.md").read_text()

# Split on the three numbered drafts
parts = re.split(r"\n## ", text)
print("draft sections:", len(parts) - 1)

for p in parts[1:]:
    title = p.split("\n", 1)[0]
    # the paste-ready body = the blockquote lines
    body = "\n".join(l[2:] if l.startswith("> ") else ("\n" if l == ">" else l)
                     for l in p.splitlines() if l.startswith(">"))
    words = len(re.findall(r"[A-Za-z0-9$£][A-Za-z0-9$£'’.,/-]*", body))
    print("\n" + "=" * 90)
    print(title[:80])
    print("  words in paste-ready body:", words, "UNDER 200" if words < 200 else "*** OVER 200 ***")
    print("  signed AIToolsEssentials:", "AIToolsEssentials" in body)
    print("  George named anywhere in body:", bool(re.search(r"\bGeorge\b", body, re.I)))
    print("  has subject line:", "Subject:" in body)

# cited figures must exist in our data
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())
tools = json.loads((S / "data" / "tools.json").read_text())
pairs = json.loads((S / "data" / "monthly_annual_pairs.json").read_text())
month = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps["snapshots"].items():
    vals = [float(x) for x in month.findall(v.get("digest") or "") if float(x) > 0]
    if vals:
        paid[k] = min(vals)

print("\n" + "=" * 90)
print("FIGURES CHECK")
facts = {
    "76 tools": len(tools) == 76,
    "42 monthly-priced": len(paid) == 42,
    "33 at/under $25": sum(1 for v in paid.values() if v <= 25) == 33,
    "median $17.50": abs(__import__('statistics').median(paid.values()) - 17.50) < 0.005,
    "pair 1.11x-2.53x median 1.25x over 19": (pairs["range_low"], pairs["range_high"],
                                              pairs["median"], pairs["n"]) == (1.11, 2.53, 1.25, 19),
    "browse-ai $48 vs $19": "$48/month or $19/month billed annually" in snaps["snapshots"]["browse-ai"]["digest"],
    "khanmigo $4 checked 2026-09-18": "$4/month" in snaps["snapshots"]["khanmigo"]["digest"]
                                      and snaps["snapshots"]["khanmigo"]["date"] == "2026-09-18",
    "snapshots updated 2026-10-06": snaps.get("updated") == "2026-10-06",
    "pairs built 2026-10-06": pairs.get("built") == "2026-10-06",
}
for k, v in facts.items():
    print(f"  {'OK ' if v else 'BAD'}  {k}")

# figure strings actually present in the drafts
print("\nliteral figure strings appearing in the draft file:")
for pat in ("76 AI tools", "42 publish", "33 of those", "$25/month", "$17.50", "1.11x to 2.53x",
            "median 1.25x", "$48", "$19", "$4 (Khanmigo", "2026-10-06", "19 tiers"):
    print(f"  {'yes' if pat in text else 'NO '}  {pat!r}")

# no unsent-flag words and no George signature blocks
print("\nhygiene:")
print("  contains 'George':", "George" in text)
print("  contains the stale 1.21x/1.33x range:", bool(re.search(r"1\.21x|1\.33x", text)))
print("  contains the stale 40/31/$16.50 set:", bool(re.search(r"40 publishing|31 of|16\.50", text)))
