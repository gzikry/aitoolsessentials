import json, re
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
snaps = json.loads((S / "data/pricing_snapshots.json").read_text())["snapshots"]

# Candidate explicit "we don't publish a price / go through sales" statements.
PATTERNS = {
    "no_selfserve": re.compile(r"(does not publish a self-serve|did not publish a self-serve|"
                               r"no self-serve|no public\b|does not publish|do not publish|"
                               r"not publish a self-serve|no official published)", re.I),
    "sales_led": re.compile(r"(sales-led|sales-assisted|sales-based|contact sales|Request a Demo|"
                            r"route to a Microsoft representative|primary CTA is)", re.I),
    "no_price_reported": re.compile(r"(No official USD seat price is reported|"
                                    r"No official USD seat or credit price is reported|"
                                    r"No official paid consumer|No official USD)", re.I),
}

hits = {}
for k, v in snaps.items():
    d = " ".join(v.get("digest", "").split())
    found = [name for name, p in PATTERNS.items() if p.search(d)]
    if found:
        hits[k] = (found, d)

print(f"snapshots matching any 'no published price / sales-led' pattern: {len(hits)}\n")
for k, (found, d) in sorted(hits.items()):
    print(f"--- {k} (checked {snaps[k]['date']}) :: {found}")
    for m in re.finditer(r"[^.]*(?:does not publish|did not publish|no self-serve|sales-led|"
                         r"sales-assisted|sales-based|contact sales|Request a Demo|"
                         r"No official USD|No official paid)[^.]*\.", d, re.I):
        print("      *", m.group(0).strip()[:190])
    print()

print("=" * 90)
strict = re.compile(r"(does not publish a self-serve|did not publish a self-serve|no self-serve|"
                    r"No official USD seat price is reported|No official paid consumer|"
                    r"does not publish a self-serve consumer price list)", re.I)
s = sorted(k for k, v in snaps.items() if strict.search(v.get("digest", "")))
print(f"STRICT 'publishes no self-serve price': {len(s)} -> {s}")
