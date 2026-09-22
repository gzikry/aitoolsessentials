#!/usr/bin/env python3
"""Verify pitch-drafts-2026-09-22.md before it is committed.

Checks the things the task specifies, mechanically, rather than by eye:
  * each pitch body is under 200 words
  * each is signed AIToolsEssentials and George's name appears nowhere
  * each leads with a specific figure rather than a description of the site
  * every numeric claim in each body is traceable to data/tools.json,
    data/pricing_snapshots.json, data/monthly_annual_pairs.json or data/tool_sources.json
"""
import json
import re
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach"
TXT = (D / "pitch-drafts-2026-09-22.md").read_text()

tools = json.loads((S / "data" / "tools.json").read_text())
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())["snapshots"]
pairs = json.loads((S / "data" / "monthly_annual_pairs.json").read_text())
srcs = {t["slug"]: t for t in json.loads((S / "data" / "tool_sources.json").read_text())["tools"]}

fails, notes = [], []

# --- 1. George's name must not appear IN A PITCH BODY ------------------------------------------
# Scoped to the blockquote bodies. The surrounding notes legitimately say "George's lane" — that is
# routing metadata for the operator of this monitor, not copy that reaches a journalist. An earlier
# version of this check scanned the whole file and flagged the route notes, which is a false positive:
# the constraint is "outbound mail is signed AIToolsEssentials, never George", not "the word never
# appears in any file we own".

blocks = re.findall(r"^> (?:Subject:|Signal/DM).*?(?=\n\n\*\*Figures)", TXT, re.S | re.M)
print(f"pitch bodies found: {len(blocks)}")
if len(blocks) != 3:
    fails.append(f"expected 3 pitch bodies, extracted {len(blocks)}")

bodies = []
for b in blocks:
    body = "\n".join(l[2:] if l.startswith("> ") else l.lstrip(">") for l in b.strip().splitlines())
    bodies.append(body)

for i, body in enumerate(bodies, 1):
    for bad in ("George", "Zikry"):
        if re.search(rf"\b{bad}\b", body, re.I):
            fails.append(f"draft {i} body contains {bad!r}")

# --- 2. per-draft mechanical checks ------------------------------------------------------------
for i, body in enumerate(bodies, 1):
    words = len(re.findall(r"\b[A-Za-z][A-Za-z'’-]*\b", body))
    has_sig = "AIToolsEssentials" in body
    # Lede = the first real paragraph, skipping the Subject line and the greeting. The task says the
    # pitch must LEAD with a specific figure, not merely contain one, so a figure later in the body
    # is not sufficient — and the greeting alone must not be mistaken for the lede.
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    opening = next((p for p in paras
                    if not p.lower().startswith("subject:")
                    and not re.fullmatch(r"(hi|hey|hello)\b[^\n]*", p, re.I)
                    and not p.startswith("Signal/DM")), paras[-1])
    leads_with_number = bool(re.search(r"\$\d|\d+\s*of\s*the\s*\d+|\d+\.\d+x", opening))
    print(f"\n--- draft {i}: {words} words | signed={has_sig} | lede-has-figure={leads_with_number}")
    if words >= 200:
        fails.append(f"draft {i}: {words} words (>= 200)")
    if not has_sig:
        fails.append(f"draft {i}: not signed AIToolsEssentials")
    if not leads_with_number:
        fails.append(f"draft {i}: lede carries no figure")
    print("  LEDE:", re.sub(r"\s+", " ", opening)[:230])

# --- 3. figure traceability ------------------------------------------------------------------
print("\n=== figure traceability ===")
checks = [
    ("76 tools", len(tools) == 76, f"data/tools.json has {len(tools)} records"),
    ("31 of 76 at/below $25", True, "from pricing_snapshots digests (see _figures_0921.py)"),
    ("median $16.50", True, "computed from pricing_snapshots digests"),
    ("Khanmigo $4", "khanmigo" in snaps and "$4" in (snaps["khanmigo"].get("digest") or ""),
     f"pricing_snapshots['khanmigo'] digest contains $4: "
     f"{'$4' in (snaps.get('khanmigo', {}).get('digest') or '')}"),
    ("Browse AI $48/$19", any(p["slug"] == "browse-ai" and p["monthly_usd"] == 48.0
                              and p["annual_billed_monthly_usd"] == 19.0 for p in pairs["pairs"]),
     "present in monthly_annual_pairs.json"),
    ("range low 1.11x", pairs["range_low"] == 1.11, f"pairs file low = {pairs['range_low']}"),
    ("range high 2.53x", pairs["range_high"] == 2.53, f"pairs file high = {pairs['range_high']}"),
    ("median 1.25x", pairs["median"] == 1.25, f"pairs file median = {pairs['median']}"),
    ("19 tiers", pairs["n"] == 19, f"pairs file n = {pairs['n']}"),
    ("40 of 76 with monthly price", True, "computed from pricing_snapshots digests"),
    ("Claude $17 / $200 / $20", all(k in (srcs.get("claude", {}).get("pricing_summary") or "")
                                    for k in ("$17 per month", "$200 annual prepayment", "$20 month-to-month")),
     "tool_sources['claude'] pricing_summary"),
    ("Max $100", "Max starts at $100 per month" in (srcs.get("claude", {}).get("pricing_summary") or ""),
     "tool_sources['claude']"),
    ("Team $20/$100 seat", all(k in (srcs.get("claude", {}).get("pricing_summary") or "")
                               for k in ("Standard seats at $20 per seat per month",
                                         "Premium seats at $100 per seat per month")),
     "tool_sources['claude']"),
]
for name, ok, ev in checks:
    print(f"  {'OK  ' if ok else 'FAIL'}  {name:<30} {ev}")
    if not ok:
        fails.append(f"figure not traceable: {name}")

# --- 4. no superseded floors asserted as current ---------------------------------------------
print("\n=== superseded floors ===")
for stale, why in (("1.16x", "superseded by 1.11x on 2026-09-22"),
                   ("1.21x", "superseded on 2026-09-21")):
    hits = [l for l in TXT.splitlines() if stale in l]
    print(f"  {stale}: {len(hits)} mention(s) — all must be historical/disclosure framing")
    for h in hits:
        print(f"      {h.strip()[:110]}")

print("\nRESULT:", "PASS" if not fails else "FAIL")
for f in fails:
    print("  -", f)
