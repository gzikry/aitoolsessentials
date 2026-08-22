#!/usr/bin/env python3
"""Generate a non-implementation AI Stack Audit report from an intake JSON file.

Usage:
  python3 scripts/generate_ai_stack_audit.py intakes/sample-small-business.json

The report is strategy-only: recommendations, workflow opportunities, risks,
and a 30-day roadmap. It does not perform setup or implementation.
"""
from __future__ import annotations

from pathlib import Path
from datetime import date
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLS = json.loads((ROOT / 'data' / 'tools.json').read_text())
TOOL_BY_SLUG = {tool['slug']: tool for tool in TOOLS}

CATEGORY_KEYWORDS = {
    'writing': ['chatgpt', 'claude', 'grammarly', 'jasper', 'copy-ai'],
    'content': ['chatgpt', 'claude', 'jasper', 'copy-ai', 'canva-ai', 'gamma'],
    'marketing': ['jasper', 'copy-ai', 'canva-ai', 'grammarly', 'gamma', 'chatgpt'],
    'sales': ['perplexity', 'fathom', 'fireflies', 'zapier-ai', 'copy-ai', 'chatgpt'],
    'meeting': ['fathom', 'otter-ai', 'fireflies', 'microsoft-copilot', 'notion-ai'],
    'research': ['perplexity', 'chatgpt', 'claude', 'gemini', 'grok', 'you-com'],
    'automation': ['zapier-ai', 'make', 'n8n', 'airtable-ai', 'notion-ai', 'slack-ai'],
    'video': ['descript', 'runway', 'heygen', 'synthesia', 'elevenlabs', 'canva-ai'],
    'audio': ['elevenlabs', 'descript', 'heygen'],
    'design': ['canva-ai', 'midjourney', 'adobe-firefly', 'leonardo-ai'],
    'image': ['midjourney', 'adobe-firefly', 'canva-ai', 'leonardo-ai'],
    'coding': ['cursor', 'github-copilot', 'replit-ai', 'v0', 'bolt-new', 'lovable'],
    'productivity': ['microsoft-copilot', 'notion-ai', 'slack-ai', 'airtable-ai', 'grammarly'],
    'real estate': ['chatgpt', 'canva-ai', 'grammarly', 'zapier-ai', 'perplexity', 'gamma'],
    'creator': ['chatgpt', 'midjourney', 'descript', 'elevenlabs', 'runway', 'canva-ai'],
    'student': ['chatgpt', 'perplexity', 'claude', 'grammarly', 'gamma', 'notion-ai'],
}

DEFAULT_STACK = ['chatgpt', 'claude', 'perplexity', 'canva-ai', 'zapier-ai', 'grammarly']


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-') or 'client'


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [line.strip('-• ').strip() for line in str(value).splitlines() if line.strip()]


def collect_keywords(intake: dict) -> str:
    parts = []
    for key in ['business_type', 'role', 'industry', 'desired_outcome', 'biggest_bottleneck']:
        if intake.get(key):
            parts.append(str(intake[key]))
    parts.extend(as_list(intake.get('top_workflows')))
    parts.extend(as_list(intake.get('outputs_needed')))
    parts.extend(as_list(intake.get('tools_considered')))
    return ' '.join(parts).lower()


def recommend_tools(intake: dict) -> list[str]:
    text = collect_keywords(intake)
    scores = {}
    for keyword, slugs in CATEGORY_KEYWORDS.items():
        if keyword in text:
            for weight, slug in enumerate(slugs[::-1], start=1):
                scores[slug] = scores.get(slug, 0) + weight
    for tool_name in as_list(intake.get('tools_considered')):
        normalized = tool_name.lower()
        for slug, tool in TOOL_BY_SLUG.items():
            if normalized in (slug.lower(), tool['name'].lower()):
                scores[slug] = scores.get(slug, 0) + 8
    if not scores:
        for slug in DEFAULT_STACK:
            scores[slug] = 1
    # Always include a general assistant and a research option unless contraindicated.
    for slug in ['chatgpt', 'claude', 'perplexity']:
        scores[slug] = scores.get(slug, 0) + 1
    ranked = sorted(scores, key=lambda slug: (-scores[slug], -TOOL_BY_SLUG.get(slug, {}).get('rating', 0), slug))
    return [slug for slug in ranked if slug in TOOL_BY_SLUG][:8]


def tools_to_delay(recommended: list[str], intake: dict) -> list[tuple[str, str]]:
    text = collect_keywords(intake)
    delays = []
    for slug in ['heygen', 'synthesia', 'runway', 'n8n', 'airtable-ai', 'jasper']:
        if slug not in recommended:
            tool = TOOL_BY_SLUG[slug]
            if slug in ['heygen', 'synthesia', 'runway'] and not any(k in text for k in ['video', 'training', 'avatar', 'youtube']):
                delays.append((tool['name'], 'Delay until video or avatar content becomes a repeated workflow.'))
            elif slug == 'n8n' and 'technical' not in text and 'developer' not in text:
                delays.append((tool['name'], 'Powerful but technical; start with simpler automation unless technical ownership exists.'))
            elif slug == 'airtable-ai' and 'database' not in text and 'operations' not in text:
                delays.append((tool['name'], 'Best when structured operational data already lives in Airtable.'))
            elif slug == 'jasper' and 'marketing' not in text and 'content' not in text:
                delays.append((tool['name'], 'Best for active marketing teams; may be unnecessary for occasional writing.'))
    return delays[:4]


def workflow_opportunities(intake: dict, recommended: list[str]) -> list[dict]:
    workflows = as_list(intake.get('top_workflows'))[:5]
    if not workflows:
        workflows = ['Weekly research and planning', 'Content drafting and editing', 'Admin follow-up and task routing']
    opportunities = []
    for i, workflow in enumerate(workflows[:5], start=1):
        lower = workflow.lower()
        if any(k in lower for k in ['research', 'market', 'competitor']):
            tools = [s for s in ['perplexity', 'chatgpt', 'claude'] if s in recommended or s in TOOL_BY_SLUG]
            review = 'Verify every source and keep citations attached to claims.'
        elif any(k in lower for k in ['meeting', 'call', 'sales call']):
            tools = [s for s in ['fathom', 'fireflies', 'otter-ai', 'chatgpt'] if s in TOOL_BY_SLUG]
            review = 'Confirm consent/recording policy and check summaries before sending follow-ups.'
        elif any(k in lower for k in ['content', 'blog', 'email', 'copy', 'social']):
            tools = [s for s in ['chatgpt', 'claude', 'grammarly', 'canva-ai'] if s in TOOL_BY_SLUG]
            review = 'Human edit for accuracy, brand voice, claims, and final publishing quality.'
        elif any(k in lower for k in ['lead', 'crm', 'automation', 'follow']):
            tools = [s for s in ['zapier-ai', 'make', 'airtable-ai', 'chatgpt'] if s in TOOL_BY_SLUG]
            review = 'Keep approval checkpoints before customer-facing messages or CRM overwrites.'
        else:
            tools = recommended[:3]
            review = 'Use AI for the first draft or analysis, then apply human review before use.'
        opportunities.append({
            'name': workflow,
            'tools': tools[:4],
            'new_process': f'Use AI to create a first-pass output for “{workflow}”, then review and finalize manually.',
            'review': review,
            'benefit': 'Reduce blank-page time, standardize the process, and make the workflow easier to repeat.'
        })
    return opportunities


def risk_notes(intake: dict) -> list[str]:
    notes = []
    privacy = str(intake.get('privacy_constraints', '')).strip()
    if privacy:
        privacy_clean = privacy.rstrip('. ')
        notes.append(f'Privacy constraint noted: {privacy_clean}. Avoid uploading sensitive records unless the selected plan and policy permit it.')
    if intake.get('team_size'):
        notes.append('If multiple people will use the stack, prioritize admin controls, shared workspaces, and documented review rules.')
    notes.append('Do not treat AI output as final for factual, legal, financial, medical, or customer-sensitive claims.')
    notes.append('Review paid subscriptions after 30 days and cancel tools that do not own a repeated workflow.')
    return notes


def render_report(intake: dict) -> str:
    client = intake.get('client_name') or intake.get('business_name') or 'Client'
    recommended = recommend_tools(intake)
    delays = tools_to_delay(recommended, intake)
    opportunities = workflow_opportunities(intake, recommended)
    risks = risk_notes(intake)
    budget = intake.get('monthly_budget', 'Not specified')
    constraints = intake.get('privacy_constraints', 'None specified')

    lines = []
    lines.append(f'# AI Stack Audit Report — {client}')
    lines.append('')
    lines.append(f'**Date:** {date.today().isoformat()}')
    lines.append('')
    lines.append('> Strategy and recommendation report only. This does not include implementation, setup, account configuration, integrations, password/API-key handling, or ongoing support.')
    lines.append('')
    lines.append('## Client Summary')
    lines.append('')
    for label, key in [('Business type','business_type'),('Team size','team_size'),('Website','website'),('Monthly budget','monthly_budget'),('Desired outcome','desired_outcome'),('Timeline','timeline')]:
        lines.append(f'- **{label}:** {intake.get(key, "Not specified")}')
    lines.append(f'- **Privacy / constraints:** {constraints}')
    lines.append('')
    lines.append('## Executive Recommendation')
    lines.append('')
    top_names = ', '.join(TOOL_BY_SLUG[s]['name'] for s in recommended[:5])
    lines.append(f'Start with a focused stack of {top_names}. The goal is not to buy the most tools; it is to assign each tool a clear repeated workflow, test it for 30 days, and cancel anything that does not reduce review-adjusted work time.')
    lines.append('')
    lines.append('## Recommended AI Stack')
    lines.append('')
    lines.append('| Tool | Role | Why it fits | Pricing note | Risk / review need |')
    lines.append('|---|---|---|---|---|')
    for slug in recommended:
        tool = TOOL_BY_SLUG[slug]
        lines.append(f'| {tool["name"]} | {tool["category"]} | {tool["best_for"]} | {tool["price"]} | {tool["cons"][0] if tool.get("cons") else "Human review required."} |')
    lines.append('')
    lines.append('## Tools to Avoid or Delay')
    lines.append('')
    if delays:
        lines.append('| Tool/category | Reason to avoid/delay |')
        lines.append('|---|---|')
        for name, reason in delays:
            lines.append(f'| {name} | {reason} |')
    else:
        lines.append('No specific tools need to be avoided based on the intake, but avoid adding any paid subscription until it is tied to a repeated workflow.')
    lines.append('')
    lines.append('## Workflow Opportunity Map')
    lines.append('')
    for i, opp in enumerate(opportunities, start=1):
        tool_names = ', '.join(TOOL_BY_SLUG[s]['name'] for s in opp['tools'] if s in TOOL_BY_SLUG)
        lines.append(f'### Workflow {i}: {opp["name"]}')
        lines.append('')
        lines.append(f'- **Recommended tool(s):** {tool_names}')
        lines.append(f'- **New process:** {opp["new_process"]}')
        lines.append(f'- **Human review point:** {opp["review"]}')
        lines.append(f'- **Expected benefit:** {opp["benefit"]}')
        lines.append('')
    lines.append('## 30-Day Adoption Roadmap')
    lines.append('')
    lines.append('### Week 1: Choose and test')
    lines.append('- Pick the top 2–3 tools from the recommended stack.')
    lines.append('- Run one real task through each tool.')
    lines.append('- Score each tool with the AI Tool Evaluation Scorecard.')
    lines.append('')
    lines.append('### Week 2: Document workflows')
    lines.append('- Write the winning process as a checklist.')
    lines.append('- Define where human review happens.')
    lines.append('- Save reusable prompts or templates.')
    lines.append('')
    lines.append('### Week 3: Train users and compare outputs')
    lines.append('- Have each user run the same workflow.')
    lines.append('- Compare quality, review time, and friction.')
    lines.append('- Decide whether the tool needs team controls or a paid plan.')
    lines.append('')
    lines.append('### Week 4: Decide what to keep/cancel')
    lines.append('- Keep tools with clear workflow ownership.')
    lines.append('- Cancel or delay overlapping tools.')
    lines.append(f'- Keep total monthly spend within the stated budget: {budget}.')
    lines.append('')
    lines.append('## Risks and Guardrails')
    lines.append('')
    for note in risks:
        lines.append(f'- {note}')
    lines.append('')
    lines.append('## Not Included')
    lines.append('')
    lines.append('This report does not include implementation, setup, integrations, account configuration, password/API-key handling, legal/compliance advice, or ongoing support.')
    lines.append('')
    return '\n'.join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('Usage: python3 scripts/generate_ai_stack_audit.py path/to/intake.json')
        return 2
    intake_path = Path(argv[1])
    if not intake_path.is_absolute():
        intake_path = ROOT / intake_path
    intake = json.loads(intake_path.read_text())
    report = render_report(intake)
    client = intake.get('client_name') or intake.get('business_name') or intake_path.stem
    out_dir = ROOT / 'audit_reports'
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f'{date.today().isoformat()}-{slugify(client)}-ai-stack-audit.md'
    out_path.write_text(report)
    print(out_path.relative_to(ROOT))
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
