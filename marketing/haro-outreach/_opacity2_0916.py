import json, re
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
snaps = json.loads((S / "data/pricing_snapshots.json").read_text())["snapshots"]
srcs = {x["slug"]: x for x in json.loads((S / "data/tool_sources.json").read_text())["tools"]}

# A tool counts as "no published price for the paid tier" only if its own snapshot says the
# vendor's official source does not publish a price. Excludes cases where a paid self-serve
# price IS published and only the top enterprise tier is sales-led (chatgpt, make, slack-ai).
STATEMENTS = [
    (r"does not publish a self-serve", "no self-serve price list"),
    (r"did not publish a self-serve", "no self-serve price list"),
    (r"No official USD seat price is reported", "no official seat price"),
    (r"No official USD seat or credit price is reported", "no official seat/credit price"),
    (r"No official paid consumer", "no official paid consumer schedule"),
    (r"no public pricing page", "no public pricing page"),
    (r"do not publish the subscription plan names, prices, or limits", "no published plan names/prices/limits"),
    (r"do not publish\b", "states it does not publish"),
    (r"not publish a self-serve consumer price list", "no self-serve consumer price list"),
]

rows = []
for k, v in snaps.items():
    txt = " ".join((v.get("digest") or "").split())
    src = " ".join((srcs.get(k, {}).get("pricing_summary") or "").split())
    why = [label for pat, label in STATEMENTS if re.search(pat, txt, re.I)]
    if why:
        rows.append((k, v["date"], sorted(set(why)), txt))

print(f"tools whose own snapshot states the paid price is not published: {len(rows)}\n")
for k, dt, why, txt in sorted(rows):
    print(f"{k:<16} checked {dt}  :: {why}")
print()
print("NAMES:", sorted(r[0] for r in rows))

# sanity: the three that only have sales-led ENTERPRISE tiers, with self-serve published
print()
for k in ("chatgpt", "make", "slack-ai"):
    print(f"{k} (excluded): {' '.join(snaps[k]['digest'].split())[:190]}")
