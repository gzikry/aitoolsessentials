#!/usr/bin/env python3
"""Seed minimal source and revenue target records for tools that are missing them."""
from pathlib import Path
import json

ROOT = Path('.')
tools = json.loads((ROOT / 'data/tools.json').read_text())

# tool_sources.json must be a dict with key 'tools'
src_path = ROOT / 'data/tool_sources.json'
src_obj = json.loads(src_path.read_text()) if src_path.exists() else {'checked_at': '2026-08-29', 'source_policy': 'Official vendor sources only. Missing values remain null or unresolved; no inference.', 'tools': []}
existing_src = {x.get('slug') for x in src_obj.get('tools', [])}
for t in tools:
    if t['slug'] in existing_src:
        continue
    src_obj['tools'].append({
        "slug": t['slug'],
        "pricing_checked_date": "2026-08-29",
        "pricing_summary": t.get('price', 'Free + paid plans') + " — official pricing page should be verified before publication.",
        "pricing_url": t.get('official', ''),
        "docs_url": t.get('official', '') + "/docs/",
        "privacy_url": t.get('official', '') + "/privacy/",
        "rights_url": t.get('official', '') + "/terms/",
        "verification_notes": "No official source verification has been performed for this record yet. Do not publish unverified pricing or rights claims.",
        "unresolved_claims": [
            "Official pricing, rights, and privacy statements have not been verified.",
            "Affiliate program status and revenue terms are unknown until checked against official sources."
        ]
    })
src_path.write_text(json.dumps(src_obj, indent=2) + '\n')
print(f'Seeded missing tool_sources.json entries; total={len(src_obj.get("tools", []))}')

# revenue_targets.json must be a list of dicts with tool_slug
rev_path = ROOT / 'data/revenue_targets.json'
rev_obj = json.loads(rev_path.read_text()) if rev_path.exists() else []
existing_rev = {x.get('tool_slug') for x in rev_obj}
for t in tools:
    if t['slug'] in existing_rev:
        continue
    rev_obj.append({
        "tool_slug": t['slug'],
        "tool_name": t.get('name', t['slug']),
        "priority": "medium",
        "category": t.get('category', 'General AI Assistant'),
        "recommended_networks_to_check": [f"Direct {t.get('name', t['slug'])} partner program search"],
        "search_queries": [
            f"{t.get('name', t['slug'])} affiliate program",
            f"{t.get('name', t['slug'])} partner program",
            f"{t.get('name', t['slug'])} referral program"
        ],
        "target_pages": [
            f"tools/{t['slug']}.html",
            "comparisons/best-ai-tools.html",
            "articles/index.html"
        ],
        "best_audiences": ["AI tool buyers", "workflow-specific buyers"],
        "status": "not_started",
        "next_action": "Check direct affiliate/partner page and major networks; update data/affiliate_programs.json only after approval.",
        "notes": "Do not invent affiliate URLs. Use official URL until approved."
    })
rev_path.write_text(json.dumps(rev_obj, indent=2) + '\n')
print(f'Seeded missing revenue_targets.json entries; total={len(rev_obj)}')
