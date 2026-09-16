import json, re
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
snaps = json.loads((S / "data/pricing_snapshots.json").read_text())["snapshots"]
tools = json.loads((S / "data/tools.json").read_text())

print("=== monthly vs annual spread on the three Meeting notetakers ===")
for k in ("fathom", "fireflies", "otter-ai"):
    d = " ".join(snaps[k]["digest"].split())
    print(f"{k} (checked {snaps[k]['date']}):")
    print("   ", d[:420])
    print()

print("=== coding tools: category Development ===")
for t in tools:
    if t["category"] == "Development":
        sl = t["slug"]
        print(f"  {t['name']:<16} price='{t.get('price')}' snapshot_checked={snaps.get(sl,{}).get('date')}")
print()
print("=== the opacity figure ===")
NOPRICE = re.compile(r"(no public|not publish|does not publish|do not publish|no official published|"
                     r"custom quote|sales-assisted|sales-led|contact sales|sales-based|not disclosed|"
                     r"no official paid|no official public|Enterprise has custom|custom pricing)", re.I)
nop = sorted(k for k, v in snaps.items() if NOPRICE.search(v.get("digest", "")))
print(f"{len(nop)} of {len(snaps)} snapshots say the price is custom/sales-led/unpublished:")
print("  ", nop)
print()
BOTH = [k for k, v in snaps.items()
        if re.search(r"(monthly|/month|month-to-month)", v.get("digest", ""), re.I)
        and re.search(r"(annual|/year|yearly)", v.get("digest", ""), re.I)]
print(f"{len(BOTH)} of {len(snaps)} snapshots quote BOTH a monthly and an annual rate")
print()
print("pricing_snapshots 'updated':", json.loads((S / "data/pricing_snapshots.json").read_text()).get("updated"))
print("stack_audit_catalog generated_at:", json.loads((S / "data/stack_audit_catalog.json").read_text()).get("generated_at"))
