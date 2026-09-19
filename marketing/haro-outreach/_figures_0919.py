"""Recompute every figure the 2026-09-19 drafts will cite, from our own data files.

Nothing here is trusted from an earlier draft: the Amplemarket send used a count (60) that had
drifted to 70, and two opacity claims were flatly wrong. Every number below is recomputed against
data/tools.json, data/pricing_snapshots.json and data/tool_sources.json as they stand today.
"""
import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
tools = json.loads((S / "data/tools.json").read_text())
snapf = json.loads((S / "data/pricing_snapshots.json").read_text())
snaps = snapf["snapshots"]
srcs = json.loads((S / "data/tool_sources.json").read_text())

print("pricing_snapshots.updated:", snapf.get("updated"))
print("tools:", len(tools), "snapshots:", len(snaps))

# --- category concentration ---
cats = {}
for t in tools:
    cats[t["category"]] = cats.get(t["category"], 0) + 1
three_plus = {k: v for k, v in cats.items() if v >= 3}
print("\n[1] categories:", len(cats), "| holding >=3:", len(three_plus), "| tools in them:", sum(three_plus.values()))
print("    ", sorted(three_plus.items(), key=lambda x: -x[1]))

# --- cheapest paid monthly tier per tool ---
MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    d = " ".join((v.get("digest") or "").split())
    vals = [float(x) for x in MONTH.findall(d) if float(x) > 0]
    if vals:
        paid[k] = (min(vals), v.get("date"))
print(f"\n[2] tools quoting a non-zero monthly price: {len(paid)} of {len(tools)}")
print(f"    cheapest paid monthly tier <= $25: {sum(1 for v in paid.values() if v[0] <= 25)}")
print(f"    median cheapest paid monthly tier: ${statistics.median(v[0] for v in paid.values()):.2f}")
print(f"    min ${min(v[0] for v in paid.values()):.2f} ({[k for k,v in paid.items() if v[0]==min(x[0] for x in paid.values())]})")
print(f"    max ${max(v[0] for v in paid.values()):.2f}")
low = sorted((v[0], k, v[1]) for k, v in paid.items() if v[0] <= 25)
print("    the sub-$25 set:", [(f"${a:.2f}", b, c) for a, b, c in low])

# --- monthly vs annual ---
both = [k for k, v in snaps.items()
        if re.search(r"(monthly|/month|month-to-month)", v.get("digest", ""), re.I)
        and re.search(r"(annual|/year|yearly)", v.get("digest", ""), re.I)]
print(f"\n[3] tools quoting BOTH a monthly and an annual rate: {len(both)} of {len(tools)}")

# --- paired same-tier ratios, one tier per tool ---
PAIR = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(user|seat|member|person)?\s*/?\s*month[^.;$]{0,60}?"
                  r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(user|seat|member|person)?\s*/?\s*month\s*(?:billed\s+)?annual", re.I)
ratios = []
for k, v in snaps.items():
    d = " ".join((v.get("digest") or "").split())
    for m in PAIR.finditer(d):
        mo, an = float(m.group(1)), float(m.group(3))
        if an > 0 and mo > an and (m.group(2) or "") == (m.group(4) or ""):
            ratios.append((mo / an, k, mo, an, v.get("date")))
ratios.sort()
print(f"\n[4] same-tier monthly/annual pairs: {len(ratios)}")
for r in ratios:
    print(f"    {r[0]:.2f}x  {r[1]:<22} ${r[2]:g} vs ${r[3]:g}  ({r[4]})")
if ratios:
    print(f"    range {ratios[0][0]:.2f}x - {ratios[-1][0]:.2f}x, median {statistics.median(r[0] for r in ratios):.2f}x")

# --- tools with no published paid-tier price ---
NOPRICE = re.compile(r"(does not publish a self-serve|did not publish a self-serve|"
                     r"No official USD seat price is reported|No official USD seat or credit price is reported|"
                     r"No official paid consumer|no public pricing page|do not publish)", re.I)
nop = sorted((k, v.get("date")) for k, v in snaps.items()
             if NOPRICE.search(v.get("digest", "")) and "free and unlimited" not in v.get("digest", ""))
print(f"\n[5] tools publishing no paid-tier price: {len(nop)}")
for k, d in nop:
    print(f"    {k:<22} checked {d}")
    print("      ", " ".join(snaps[k]["digest"].split())[:150])

# --- Claude / assistant tier figures used in the support-value draft ---
print("\n[6] assistant tiers")
for k in ("claude", "gemini", "cursor", "chatgpt", "perplexity"):
    v = snaps.get(k, {})
    print(f"    {k:<12} checked {v.get('date')} | {' '.join((v.get('digest') or '').split())[:230]}")
ts = {t["slug"]: t for t in srcs["tools"]}
for k in ("claude",):
    t = ts.get(k)
    if t:
        print(f"    tool_sources[{k}] pricing_checked_date={t.get('pricing_checked_date')}")
        print("      ", " ".join((t.get("pricing_summary") or "").split())[:600])
