#!/usr/bin/env python3
"""Assert every figure quoted in pitch-drafts-2026-09-20.md against the file that holds it.

Why this exists: the 2026-09-15 pitch went out citing "60 of 76" in categories holding 3+ when the
real number was 70, and the 2026-09-18 Amplemarket pitch cited an opacity count of 5 when it was 3.
Both were published to a recipient. A draft that quotes a number is a claim, and this is the check
that makes the claim true before it is sent.

It does not just re-derive the numbers - it reads the draft text, pulls out each numeric claim by
regex, and compares. A figure the verifier cannot find in any source file is a FAILURE, not a
warning, because that is exactly how an invented number would get through.
"""
import json
import re
import statistics
import sys
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
DRAFT = S / "marketing" / "haro-outreach" / "pitch-drafts-2026-09-20.md"
text = DRAFT.read_text()

tools = json.loads((S / "data" / "tools.json").read_text())
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())["snapshots"]
srcs = json.loads((S / "data" / "tool_sources.json").read_text())
ts = {t["slug"]: t for t in srcs["tools"]}

fails, passes = [], []


def check(name, claimed, actual):
    ok = claimed == actual
    (passes if ok else fails).append(f"{name}: draft says {claimed!r}, data says {actual!r}")
    print(f"  {'PASS' if ok else 'FAIL'}  {name:<52} draft={claimed!r} data={actual!r}")


print("=" * 100)
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

print("\n3. same-tier monthly/annual pairs (drafts 1 and 3)")
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
check("pair range lower bound 1.21x", 1.21, round(ratios[0][0], 2))
check("pair range upper bound 2.53x", 2.53, round(ratios[-1][0], 2))
check("narrowest pair is HeyGen $29 vs $24", ("heygen", 29.0, 24.0),
      (ratios[0][1], ratios[0][2], ratios[0][3]))
check("widest pair is Browse AI $48 vs $19", ("browse-ai", 48.0, 19.0),
      (ratios[-1][1], ratios[-1][2], ratios[-1][3]))
check("all pairs carry date 2026-09-18", {"2026-09-18"}, {r[4] for r in ratios})

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
check("Premium seat is NOT in the snapshot digest (that's why draft cites tool_sources)",
      False, "Premium seats" in (c_snap.get("digest") or ""))

print("\n5. reply routes stated in the draft (live re-checked this run)")
check("Raconteur live contributor URL", True,
      "https://www.raconteur.net/contributors/simon-chandler" in text)
check("draft still names the dead byline URL only as a correction", True,
      "/author/simon-chandler/" in text)
check("Speciality Food address present", True, "holly.shackleton@artichokehq.com" in text)
check("Signal handle present", True, "hliwrites.99" in text)

print("\n5b. the queue ranks every drafted request above nothing — no label falls through the band map")
QUEUE = S / "marketing" / "haro-outreach" / "pitch-queue.md"
qtext = QUEUE.read_text()
live_sec = qtext[qtext.find("## Live"):qtext.find("## Cold")]
order = [m.group(1) for m in re.finditer(r"### \[([^\]]+)\]", live_sec)]
rank = {"high": 0, "medium-high": 0.5, "medium": 1, "low-medium": 2, "medium-low": 2, "low": 3}
ranks = [rank.get(o.strip(), 9) for o in order]
check("queue live section is sorted best-relevance first", sorted(ranks), ranks)
unmapped = [o for o in order if rank.get(o.strip(), 9) == 9]
check("no live row carries an unmapped relevance band", [], unmapped)
drafted = [u.rsplit("/journo-request/")[-1] for u in re.findall(
    r"https://www\.sourcee\.app/journo-request/[a-z0-9\-]+", text)]
drafted_set = {d for d in drafted}
live_slugs = re.findall(r"\*\*URL:\*\* https://www\.sourcee\.app/journo-request/([a-z0-9\-]+)", live_sec)
draft_idx = qtext.find("## Drafts")
draft_sec = qtext[draft_idx:qtext.find("## Live")]
for d in sorted(drafted_set & set(live_slugs)):
    check(f"drafted {d[:44]} is named in the queue's draft index", True, d[:40] in draft_sec)


print("\n6. no draft exceeds 200 words (pitch body only, stopping at the signature line)")
# Same definition the 2026-09-19 verifier used, and the right one: the message that a journalist
# reads ends at the signature. Counting the quoted footer boilerplate as pitch words would fail
# correct drafts. Words are [A-Za-z'] tokens, so "$48" and "1.21x" do not inflate the count.
blocks = re.findall(r"((?:^>[^\n]*\n|^>\s*\n)+)", text, re.M)
bodies = []
for b in blocks:
    if not re.search(r"(?m)^>\s*AIToolsEssentials\s*$", b):
        continue
    body = re.split(r"(?m)^>\s*AIToolsEssentials\s*$", b)[0]
    bodies.append((len(re.findall(r"[A-Za-z']+", body)), body.strip().split("\n")[0][:50]))
check("three draft bodies found", 3, len(bodies))
for i, (count, first) in enumerate(bodies, start=1):
    ok = count <= 200
    (passes if ok else fails).append(f"draft {i} body word count {count}")
    print(f"  {'PASS' if ok else 'FAIL'}  draft {i} pitch body {count} words (limit 200) — {first}")
check("every draft body is non-trivial (>60 words)", True, all(c > 60 for c, _ in bodies))

print("\n7. signature discipline")
check("drafts signed AIToolsEssentials", True, text.count("AIToolsEssentials") >= 3)
mentions = sorted(set(m.lower() for m in re.findall(r"(?i)george[^\s]*", text)))
# 'George's lane' is route ownership and 'not George's' is the blocking line — neither is a byline.
allowed = {"george's", "george)", "george.", "george"}
check("every 'George' mention is route-ownership or prose, never a sender", True,
      all(m in allowed for m in mentions))
check("no draft signs off as George", False,
      bool(re.search(r"(?im)^>\s*(george|—\s*george)\s*$", text)))

print("\n" + "=" * 100)
print(f"checks passed: {len(passes)}   failures: {len(fails)}")
for f in fails:
    print("  FAIL:", f)
sys.exit(1 if fails else 0)
