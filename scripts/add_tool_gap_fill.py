#!/usr/bin/env python3
"""Add 6 high-intent software-only tools and sync minimal required records."""
from pathlib import Path
import json

ROOT = Path('.')

tools_path = ROOT / 'data/tools.json'
tools = json.loads(tools_path.read_text())
existing_tools = {t['slug'] for t in tools}

additions = [
  {
    "slug": "shortwave",
    "name": "Shortwave",
    "category": "Email AI",
    "best_for": "AI email triage, summaries, and scheduled send in Gmail",
    "price": "Free + paid plans",
    "rating": 4.5,
    "official": "https://www.shortwave.com/",
    "summary": "An AI email client that adds triage, summaries, reminders, and scheduled send to Gmail.",
    "use_cases": ["Inbox triage", "Long email summaries", "Reminders and scheduled send", "Bulk cleanup", "Reading time estimates"],
    "pros": ["Works inside Gmail", "Fast AI summaries", "Clear free tier"],
    "cons": ["Mobile experience differs from desktop", "Some users prefer vanilla Gmail"],
    "key_features": ["AI thread summaries", "Smart triage with custom rules", "Scheduled send and reminders", "Reading time estimates", "Bulk cleanup and mute"],
    "faq": [
      ["Is Shortwave free?", "See the official pricing summary and source links above."],
      ["Shortwave vs Superhuman?", "Shortwave adds AI triage and summaries on top of Gmail; Superhuman is a separate fast-mailbox experience. See our email AI tools guide."]
    ],
    "trial_checklist": "Use a real work week with real threads. Verify whether summaries and triage rules cut read/sort time. Track volume of messages moved without review. Compare feel against vanilla Gmail and at least one alternative before renewing.",
    "hands_on_status": "protocol_ready_not_published",
    "hands_on_priority": "standard"
  },
  {
    "slug": "browse-ai",
    "name": "Browse AI",
    "category": "Browser Automation",
    "best_for": "Visual web scraping and no-code browser automation",
    "price": "Free + paid plans",
    "rating": 4.3,
    "official": "https://www.browse.ai/",
    "summary": "A visual web automation platform that turns site monitoring and extraction into repeatable robots.",
    "use_cases": ["Price monitoring", "Competitor tracking", "Lead list extraction", "Form submission automation"],
    "pros": ["Visual setup", "Handles auth and pagination", "APIs and integrations"],
    "cons": ["Site changes can break robots", "Volume pricing grows quickly"],
    "key_features": ["Visual robot recorder", "Scheduled monitoring", "API and webhooks", "Prebuilt robots for popular sites", "Rotating proxies"],
    "faq": [
      ["Is Browse AI free?", "See the official pricing summary and source links above."],
      ["Browse AI vs Make/Zapier/n8n?", "Browse AI is specialized for visual web tasks; Make/Zapier/n8n are general automation layers. Use the automation cost decoder to compare units for your workflow."]
    ],
    "trial_checklist": "Run one real extraction against live pages and one monitoring task. Verify whether retries and proxy behavior recover from a real page change. Compare cost and maintenance against a Make/Zapier/n8n equivalent before deciding.",
    "hands_on_status": "protocol_ready_not_published",
    "hands_on_priority": "standard"
  },
  {
    "slug": "rows",
    "name": "Rows",
    "category": "Productivity",
    "best_for": "AI-native spreadsheet with integrated data connections",
    "price": "Free + paid plans",
    "rating": 4.4,
    "official": "https://rows.com/",
    "summary": "A spreadsheet built for teams that want AI transformations and direct integrations inside the grid.",
    "use_cases": ["Data-enriched planning", "Integrated reporting", "Marketing and finance ops", "Client-facing dashboards"],
    "pros": ["Built-in integrations", "AI transforms in cells", "Clean sharing model"],
    "cons": ["Smaller ecosystem than Excel/Sheets", "Advanced formulas differ from Excel"],
    "key_features": ["AI cell transforms", "Native integrations", "Publish and share dashboards", "Python and JS cells", "Team workspace controls"],
    "faq": [
      ["Is Rows free?", "See the official pricing summary and source links above."],
      ["Rows vs Airtable AI?", "Rows is spreadsheet-first with live integrations; Airtable is database-first with AI fields. See our productivity tools guide."]
    ],
    "trial_checklist": "Use one real planning/reporting workbook with live integrations. Verify whether cell-level AI transforms actually shorten prep time. Share a published dashboard and check access/update behavior. Repeat the same workflow in Airtable AI or Notion AI before deciding.",
    "hands_on_status": "protocol_ready_not_published",
    "hands_on_priority": "standard"
  },
  {
    "slug": "notebooklm",
    "name": "NotebookLM",
    "category": "Research",
    "best_for": "Document QDA, study guides, and audio overviews from uploaded sources",
    "price": "Free",
    "rating": 4.5,
    "official": "https://notebooklm.google.com/",
    "summary": "Google's document research tool that grounds answers in uploaded files and produces audio overviews.",
    "use_cases": ["Research synthesis", "Study guide generation", "Audio briefings", "Source-grounded Q&A"],
    "pros": ["Free to use", "Grounded in your sources", "Audio overviews"],
    "cons": ["Data usage governed by Google's privacy terms", "Upload limits apply"],
    "key_features": ["Source-grounded answers", "Audio overview generator", "Study guide and briefing exports", "Multi-source notebooks", "Inline citations from sources"],
    "faq": [
      ["Is NotebookLM free?", "Google currently offers NotebookLM for free. See the official source link above for current availability and limits."],
      ["NotebookLM vs Perplexity?", "NotebookLM answers from your uploaded files; Perplexity searches the open web. Use both when you need private source review plus public research."]
    ],
    "trial_checklist": "Use one real document set with proprietary or time-sensitive content. Verify whether answers stay grounded in your sources rather than hallucinating from general knowledge. Check export quality for study guides and audio overviews. Compare against at least one alternative before relying on it for regular research.",
    "hands_on_status": "protocol_ready_not_published",
    "hands_on_priority": "standard"
  },
  {
    "slug": "typingmind",
    "name": "TypingMind",
    "category": "AI Agents",
    "best_for": "Self-hosted multi-model chat with unified prompts and model routing",
    "price": "Free + paid plans",
    "rating": 4.4,
    "official": "https://www.typingmind.com/",
    "summary": "A self-hostable chat interface that unifies multiple LLM providers under one prompt library and usage dashboard.",
    "use_cases": ["Multi-model comparison", "Prompt library management", "Private self-hosted chat", "Team access controls"],
    "pros": ["Self-hosted option", "Multi-provider", "Prompt library"],
    "cons": ["Setup complexity for self-hosting", "UI is functional rather than polished"],
    "key_features": ["Bring-your-own API keys", "Self-hosted deployment", "Prompt library and tags", "Usage and cost tracking", "Model routing and fallbacks"],
    "faq": [
      ["Is TypingMind free?", "See the official pricing summary and source links above. Self-hosted and cloud plan limits can change."],
      ["TypingMind vs Poe?", "TypingMind focuses on self-hosted multi-model control with prompt libraries; Poe is a consumer bot platform with shared subscriptions. See our AI chat tools guide."]
    ],
    "trial_checklist": "Use at least two real provider keys on the same prompt. Verify whether cost tracking and routing actually match your bill. If self-hosting, confirm update path and access controls. Repeat the same prompts in Poe and at least one direct model UI before deciding.",
    "hands_on_status": "protocol_ready_not_published",
    "hands_on_priority": "standard"
  },
  {
    "slug": "speechify",
    "name": "Speechify",
    "category": "Audio Production",
    "best_for": "Text-to-speech reading assistant for documents, web, and learning",
    "price": "Free + paid plans",
    "rating": 4.2,
    "official": "https://speechify.com/",
    "summary": "A text-to-speech reading assistant that turns documents, web pages, and PDFs into listenable audio.",
    "use_cases": ["Audiobook-style reading", "PDF and document listening", "Reading speed adjustment", "Learning and accessibility"],
    "pros": ["Wide format support", "Natural reader voices", "Accessibility focus"],
    "cons": ["Best voices require paid plans", "Background noise handling is limited"],
    "key_features": ["Document and PDF reader", "Web page reader extension", "Speed and voice controls", "Offline listening", "Accessibility-focused design"],
    "faq": [
      ["Is Speechify free?", "See the official pricing summary and source links above. Plan limits and voice access can change."],
      ["Speechify vs ElevenLabs?", "Speechify is a reading assistant focused on document and web listening; ElevenLabs is a voice creation platform for narration and dubbing. See our AI voice tools guide."]
    ],
    "trial_checklist": "Use one real long document and one web reading session. Verify voice quality, speed control, and offline behavior. Compare cost and output quality against ElevenLabs or Murf for any narration use case. Repeat the same task in at least one alternative before deciding.",
    "hands_on_status": "protocol_ready_not_published",
    "hands_on_priority": "standard"
  }
]

for item in additions:
    if item['slug'] in existing_tools:
        raise SystemExit(f'{item["slug"]} already exists in tools.json')
    tools.append(item)

tools_path.write_text(json.dumps(tools, indent=2) + '\n')
print(f'Updated tools.json with {len(additions)} new tools, total={len(tools)}')

# Minimal tool_sources.json additions
src_path = ROOT / 'data/tool_sources.json'
src_obj = json.loads(src_path.read_text())
if not isinstance(src_obj, dict) or 'tools' not in src_obj or not isinstance(src_obj['tools'], list):
    raise SystemExit('tool_sources.json has unexpected shape')
existing_src = {x.get('slug') for x in src_obj['tools']}
for item in additions:
    if item['slug'] in existing_src:
        continue
    src_obj['tools'].append({
        "slug": item['slug'],
        "pricing_checked_date": "2026-08-29",
        "pricing_summary": item.get('price', 'Free + paid plans') + " — official pricing page should be verified before publication.",
        "pricing_url": item.get('official', ''),
        "docs_url": item.get('official', '') + "/docs/",
        "privacy_url": item.get('official', '') + "/privacy/",
        "rights_url": item.get('official', '') + "/terms/",
        "verification_notes": "No official source verification has been performed for this record yet. Do not publish unverified pricing or rights claims.",
        "unresolved_claims": [
            "Official pricing, rights, and privacy statements have not been verified.",
            "Affiliate program status and revenue terms are unknown until checked against official sources."
        ]
    })
src_path.write_text(json.dumps(src_obj, indent=2) + '\n')
print('Updated tool_sources.json minimal records.')

# Minimal revenue_targets.json additions
rev_path = ROOT / 'data/revenue_targets.json'
rev_obj = json.loads(rev_path.read_text()) if rev_path.exists() else []
existing_rev = {x.get('tool_slug') for x in rev_obj}
for item in additions:
    if item['slug'] in existing_rev:
        continue
    rev_obj.append({
        "tool_slug": item['slug'],
        "tool_name": item.get('name', item['slug']),
        "priority": "medium",
        "category": item.get('category', 'General AI Assistant'),
        "recommended_networks_to_check": [],
        "search_queries": [],
        "target_pages": [],
        "best_audiences": ["AI tool buyers", "workflow-specific buyers"],
        "status": "not_started",
        "next_action": "Check direct affiliate/partner page and major networks; update data/affiliate_programs.json only after approval.",
        "notes": "Do not invent affiliate URLs. Use official URL until approved."
    })
rev_path.write_text(json.dumps(rev_obj, indent=2) + '\n')
print('Updated revenue_targets.json minimal records.')

# Minimal pricing_snapshots.json additions
prices_path = ROOT / 'data/pricing_snapshots.json'
prices_obj = json.loads(prices_path.read_text())
if not isinstance(prices_obj, dict) or 'snapshots' not in prices_obj or not isinstance(prices_obj['snapshots'], dict):
    raise SystemExit('pricing_snapshots.json has unexpected shape')
for item in additions:
    if item['slug'] in prices_obj['snapshots']:
        continue
    prices_obj['snapshots'][item['slug']] = {
        "date": "2026-08-29",
        "digest": item.get('price', 'Free + paid plans') + " — official pricing digest should be verified before publication."
    }
prices_path.write_text(json.dumps(prices_obj, indent=2) + '\n')
print('Updated pricing_snapshots.json minimal records.')
