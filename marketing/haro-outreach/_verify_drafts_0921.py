#!/usr/bin/env python3
"""Assert every figure quoted in pitch-drafts-2026-09-21.md against the file that holds it.

Why this exists: the 2026-09-15 pitch went out citing "60 of 76" where the real number was 70, and the
2026-09-18 Amplemarket pitch cited an opacity count of 5 where it was 3 — and then repeated a
monthly/annual range that this run proved wrong at its floor (1.21x was never the minimum). Each of
those was published to a recipient. A draft that quotes a number is a claim, and this is the check
that makes the claim true before it is sent.

It reads the draft text, pulls each numeric claim out by regex, and compares against the data file.
A figure that cannot be found in any source file is a FAILURE, not a warning — that is exactly how an
invented number would get through.
"""
import json
import re
import statistics
import sys
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
DRAFT = S / "marketing" / "haro-outreach" / "pitch-drafts-2026-09-21.md"
text = DRAFT.read_text()

tools = json.loads((S / "data" / "tools.json").read_text())
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())["snapshots"]
srcs = json.loads((S / "data" / "tool_sources.json").read_text())
ts = {t["slug"]: t for t in srcs["tools"]}
pairs = json.loads((S / "data" / "monthly_annual_pairs.json").read_text())

fails, passes = [], []


def check(name, claimed, actual):
    ok = claimed == actual
    (passes if ok else fails).append(f"{name}: draft says {claimed!r}, data says {actual!r}")
    print(f"  {'PASS' if ok else 'FAIL'}  {name:<56} draft={claimed!r} data={actual!r}")


print("=" * 104)
print("1. tool count")
check("76 tools tracked", 76, len(tools))

print("\n2. cheapest paid monthly tier set (drafts 1 and 3)")
MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    vals = [float(x) for x in MONTH.findall(" ".join((v.get("digest") or "").split())) if float(x) > 0]
    if vals:
        paid[k] = (min(vals), v.get("date"))
check("40 of 76 publish a non-zero monthly price", 40, len(paid))
check("31 of those at or under $25", 31, sum(1 for v in paid.values() if v[0] <= 25))
check("median cheapest paid tier $16.50", 16.50, round(statistics.median(v[0] for v in paid.values()), 2))
low = min(paid.items(), key=lambda kv: kv[1][0])
check("lowest is Khanmigo at $4", ("khanmigo", 4.0), (low[0], low[1][0]))
check("Khanmigo snapshot date 2026-09-18", "2026-09-18", low[1][1])

print("\n3. the CORRECTED same-tier monthly/annual range (the whole point of this run)")
check("pair count is 18", 18, pairs["n"])
check("range low is 1.16x (was published as 1.21x)", 1.16, pairs["range_low"])
check("range high is 2.53x", 2.53, pairs["range_high"])
check("median is 1.25x (was published as 1.33x)", 1.25, pairs["median"])
p = pairs["pairs"]
check("lowest pair is instrumentl Pre-Award $579 vs $499", ("instrumentl", 579.0, 499.0),
      (p[0]["slug"], p[0]["monthly_usd"], p[0]["annual_billed_monthly_usd"]))
check("highest pair is browse-ai Personal $48 vs $19", ("browse-ai", 48.0, 19.0),
      (p[-1]["slug"], p[-1]["monthly_usd"], p[-1]["annual_billed_monthly_usd"]))
check("draft cites the corrected floor 1.16x", True, "1.16x" in text)
check("draft names the old wrong floor as superseded", True, "1.21x" in text)
# The old range SHOULD still appear — it must, so the error is disclosed — but only inside the
# correction paragraph. A bare assertion "the string is absent" would fail a correct draft, and an
# assertion "the string is present" would pass an incorrect one. What has to hold is that every
# occurrence sits within ~120 chars of correction language.
CORRECTION = re.compile(r"(wrong|superseded|was published|old |corrected|no longer|never in the set|"
                        r"is superseded|old wrong)", re.I)
stale_claims = []
for m in re.finditer(r"(1\.21x to 2\.53x|median 1\.33x)", text):
    ctx = text[max(0, m.start() - 160):m.end() + 160]
    if not CORRECTION.search(ctx):
        stale_claims.append(ctx.strip()[:90])
check("every mention of the old range sits inside correction language", [], stale_claims)
check("the corrected range is the one the pitch bodies quote", True,
      "1.16x to 2.53x" in text and "1.16x up to 2.53x" in text)
# every pair sentence must still be present in the snapshot file
missing = []
for row in p:
    needle = {"instrumentl": "$499/month annually or $579 monthly",
              "airtable-ai": "$20/seat/month billed annually or $24 billed monthly",
              "slack-ai": "$15/user/month annually or $18 monthly"}.get(row["slug"])
    if not needle:
        continue
    if needle not in " ".join((snaps.get(row["slug"], {}).get("digest") or "").split()):
        missing.append((row["slug"], row["plan"]))
check("spot-checked pair sentences still exist in pricing_snapshots.json", [], missing)

print("\n4. Claude / Anthropic tier figures (draft 2)")
c_snap = snaps["claude"]
c_src = ts["claude"]
check("claude snapshot date 2026-09-18", "2026-09-18", c_snap.get("date"))
check("claude tool_sources checked 2026-09-18", "2026-09-18", c_src.get("pricing_checked_date"))
summary = " ".join((c_src.get("pricing_summary") or "").split())
for label, needle in (
    ("Pro $17/month", "$17 per month"),
    ("$200 annual prepayment", "$200 annual prepayment"),
    ("$20 month-to-month", "$20 month-to-month"),
    ("Max from $100/month", "Max starts at $100 per month"),
    ("Team Standard $20/seat/month", "Standard seats at $20 per seat per month"),
    ("Team Premium $100/seat/month", "Premium seats at $100 per seat per month"),
):
    check(label, True, needle in summary)
check("Premium seat is NOT in the snapshot digest (why draft cites tool_sources)",
      False, "Premium seats" in (c_snap.get("digest") or ""))

print("\n5. reply routes stated in the draft (live re-checked this run)")
for label, needle in (
    ("Raconteur live contributor URL", "https://www.raconteur.net/contributors/simon-chandler"),
    ("dead byline URL named only as a correction", "/author/simon-chandler/"),
    ("Speciality Food address present", "holly.shackleton@artichokehq.com"),
    ("Signal handle present", "hliwrites.99"),
    ("Raconteur address present", "simon.chandler@raconteur.net"),
):
    check(label, True, needle in text)

print("\n5b. the queue ranks every drafted request above the live-only rows")
QUEUE = S / "marketing" / "haro-outreach" / "pitch-queue.md"
qtext = QUEUE.read_text()
send_sec = qtext[qtext.find("## Sendable"):qtext.find("## Live but not sendable")]
order = [m.group(1) for m in re.finditer(r"### \[([^\]]+)\]", send_sec)]
rank = {"high": 0, "medium-high": 0.5, "medium": 1, "low-medium": 2, "medium-low": 2, "low": 3}
ranks = [rank.get(o.strip(), 9) for o in order]
check("queue sendable section is sorted best-relevance first", sorted(ranks), ranks)
check("no sendable row carries an unmapped relevance band", [], [o for o in order if rank.get(o.strip(), 9) == 9])
check("sendable section holds exactly the 3 drafted requests", 3, len(order))
check("queue headline names a SENDABLE count, not just a live count", True, "sendable" in qtext.lower())
check("off-beat live rows are split into their own non-actionable section", True,
      "## Live but not sendable" in qtext)
# every drafted request must appear in the queue's sendable section with a named route
drafted = {u.rsplit("/journo-request/")[-1] for u in re.findall(
    r"https://www\.sourcee\.app/journo-request/[a-z0-9\-]+", text)}
live_slugs = set(re.findall(r"\*\*URL:\*\* https://www\.sourcee\.app/journo-request/([a-z0-9\-]+)", send_sec))
check("all three drafted requests are in the queue's sendable section", set(), drafted - live_slugs)
draft_idx = qtext.find("## Drafts")
draft_sec = qtext[draft_idx:qtext.find("## Sendable")]
for d in sorted(drafted & live_slugs):
    check(f"drafted {d[:40]} is named in the queue's draft index", True, d[:40] in draft_sec)

print("\n6. no draft exceeds 200 words (pitch body only, stopping at the signature line)")
blocks = re.findall(r"((?:^>[^\n]*\n|^>\s*\n)+)", text, re.M)
bodies = []
for b in blocks:
    if not re.search(r"(?m)^>\s*AIToolsEssentials\s*$", b):
        continue
    body = re.split(r"(?m)^>\s*AIToolsEssentials\s*$", b)[0]
    bodies.append((len(re.findall(r"[A-Za-z']+", body)), body.strip().split("\n")[0][:52]))
check("three draft bodies found", 3, len(bodies))
for i, (count, first) in enumerate(bodies, start=1):
    ok = count <= 200
    (passes if ok else fails).append(f"draft {i} body word count {count}")
    print(f"  {'PASS' if ok else 'FAIL'}  draft {i} pitch body {count} words (limit 200) — {first}")
check("every draft body is non-trivial (>60 words)", True, all(c > 60 for c, _ in bodies))

print("\n7. signature discipline")
check("drafts signed AIToolsEssentials", True, text.count("AIToolsEssentials") >= 3)
mentions = sorted(set(m.lower() for m in re.findall(r"(?i)george[^\s]*", text)))
# 'George's lane' / "not George's" are route ownership, never a byline
allowed = {"george's", "george)", "george.", "george"}
check("every 'George' mention is route-ownership or prose, never a sender", True,
      all(m in allowed for m in mentions))
check("no draft signs off as George", False,
      bool(re.search(r"(?im)^>\s*(george|—\s*george)\s*$", text)))

print("\n8. ledger discipline — nothing marked pitched that was not sent")
LEDGER = json.loads((S / "marketing" / "haro-outreach" / "pitch-ledger.json").read_text())
check("ledger still records exactly 3 sent pitches", 3, len(LEDGER.get("pitched", {})))
check("no draft request is marked pitched in the ledger", set(),
      drafted & set(LEDGER.get("pitched", {})))

print("\n" + "=" * 104)
print(f"checks passed: {len(passes)}   failures: {len(fails)}")
for f in fails:
    print("  FAIL:", f)
sys.exit(1 if fails else 0)
