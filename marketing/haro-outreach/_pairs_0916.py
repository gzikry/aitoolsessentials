import json, re, subprocess
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
snaps = json.loads((S / "data/pricing_snapshots.json").read_text())["snapshots"]

# Find monthly vs annual pairs and quantify the gap, so any pitch figure is defensible.
PAIR = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*(?:/|per\s)?\s*(?:user|seat|member|person)?\s*/?\s*month\b"
                  r"[^.;]{0,60}?\$\s?(\d+(?:\.\d+)?)\s*(?:/|per\s)?\s*(?:user|seat|member|person)?\s*"
                  r"/?\s*month\s*(?:billed\s+)?annual", re.I)
ALT = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month\s*billed\s+annually", re.I)

rows = []
for k, v in snaps.items():
    d = " ".join(v.get("digest", "").split())
    for m in PAIR.finditer(d):
        mo, an = float(m.group(1)), float(m.group(2))
        if an > 0 and mo > an:
            rows.append((k, v["date"], mo, an, (mo / an - 1) * 100, m.group(0)[:110]))

print(f"{'tool':<16} {'checked':<11} {'monthly':>8} {'annual':>8} {'premium':>8}")
for k, dt, mo, an, pct, txt in sorted(rows, key=lambda r: -r[4]):
    print(f"{k:<16} {dt:<11} {mo:>8.2f} {an:>8.2f} {pct:>7.0f}%")
print()
print("pairs found:", len(rows))
if rows:
    print("max premium: %.0f%% (%s)" % (rows[0][4] if False else max(r[4] for r in rows),
                                        max(rows, key=lambda r: r[4])[0]))
print()
print("=== verify reply mailboxes ===")
for dom, addr in (("marketintelligencetools.com", "contact@marketintelligencetools.com"),
                  ("foxandspindle.com", "hello@foxandspindle.com")):
    r = subprocess.run(["dig", "+short", "MX", dom], capture_output=True, text=True)
    print(f"{addr:<42} MX: {r.stdout.strip().splitlines()[:2]}")
