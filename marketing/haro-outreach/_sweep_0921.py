#!/usr/bin/env python3
"""Broader candidate sweep for 2026-09-21.

The slug filter can only match tokens in the slug, so requests like the Raconteur shadow-AI one
(slug carries no 'ai') are invisible to it. This reads every slug from the last 3 days carrying any
spend token, plus every slug in the last 3 days carrying any AI token, and prints them ranked by
lastmod so a body that needs reading is visible.
"""
import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
sw = json.loads((D / "_sitemap_0921.json").read_text())
slugs = sw["pairs"]
cut = "2026-09-18T05:00:00"

AI = re.compile(r"(?<![a-z])(ai|llm|chatgpt|claude|copilot|agentic|artificial.intelligence|machine.learning|"
                r"generative|automation|robot)(?![a-z])", re.I)
SPEND = re.compile(r"(pricing|price|subscription|cost|costs|spend|budget|credit|seat|licen[cs]e|"
                   r"renewal|procurement|invoice|billing|expense|reimburse|vendor|monthly|overlap|"
                   r"consolidat|waste|stack|tier|fee|free|paid|saas|software|tech|tool)", re.I)

ai, sp, both = [], [], []
for s, lm in slugs:
    if lm < cut:
        continue
    t = s.replace("-", " ")
    a, p = bool(AI.search(t)), bool(SPEND.search(t))
    if a:
        ai.append((s, lm, p))
    if p:
        sp.append((s, lm, a))
    if a and p:
        both.append((s, lm))

print(f"window since {cut}: {len([1 for s,lm in slugs if lm>=cut])} slugs")
print(f"\n-- AI-token slugs ({len(ai)}) --")
for s, lm, p in ai:
    print(f"  {lm}  {'SPEND' if p else '     '}  {s}")
print(f"\n-- spend-token slugs ({len(sp)}) --")
for s, lm, a in sp:
    print(f"  {lm}  {'AI' if a else '  '}  {s}")
print(f"\n-- AI + spend in the same slug ({len(both)}) --")
for s, lm in both:
    print(f"  {lm}  {s}")
