import json, re
from collections import Counter
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
tools = json.loads((S / "data/tools.json").read_text())
snaps = json.loads((S / "data/pricing_snapshots.json").read_text())["snapshots"]

print("=== tools.json ===")
print("tools tracked:", len(tools))
cats = Counter(t["category"] for t in tools)
print("categories:", len(cats))
three_plus = {k: v for k, v in cats.items() if v >= 3}
print("categories with >=3 tools:", len(three_plus), "holding", sum(three_plus.values()), "tools")
print("  ->", dict(sorted(three_plus.items(), key=lambda x: -x[1])))
print()
print("Meetings category members:", [t["name"] for t in tools if t["category"] == "Meetings"])
print("Development members:", [t["name"] for t in tools if t["category"] == "Development"])
print()
print("=== pricing_snapshots ===")
print("snapshots:", len(snaps))
# tools with no published public price anywhere in the snapshot
NOPRICE = re.compile(r"(no public|not publish|does not publish|do not publish|no official published|"
                     r"custom quote|sales-assisted|sales-led|contact sales|sales-based|not disclosed|"
                     r"no official paid|no official public)", re.I)
nop = [k for k, v in snaps.items() if NOPRICE.search(v.get("digest", ""))]
print("snapshots stating no published/custom/sales-led price:", len(nop))
print("  ->", nop)
print()
# monthly + annual both present
both = []
for k, v in snaps.items():
    d = v.get("digest", "")
    if re.search(r"(monthly|/month|month-to-month)", d, re.I) and re.search(r"(annual|/year|billed annual|yearly)", d, re.I):
        both.append(k)
print("snapshots quoting both a monthly and an annual rate:", len(both))
print("  ->", both[:30])
print()
# meeting notetaker verified prices
for k in ("fathom", "fireflies"):
    print(k, "| checked", snaps[k]["date"], "|", " ".join(snaps[k]["digest"].split())[:260])
print()
print("Otter in snapshots?", "otter" in snaps)
print()
print("=== the sent pitch claim ===")
print("sent email said: '60 sit in the 13 categories holding three or more'")
print("verified from tools.json:", sum(three_plus.values()), "across", len(three_plus), "categories")
