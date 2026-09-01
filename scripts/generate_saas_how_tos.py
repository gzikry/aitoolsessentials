#!/usr/bin/env python3
"""Generate setup guides for SaaS AI tools and the combined how-to hub."""
from pathlib import Path
from html import escape
import json

DOMAIN = 'https://aitoolsessentials.com'

GUIDES = [
    {
        'slug': 'get-started-with-shortwave',
        'title': 'How to get started with Shortwave for AI email',
        'summary': 'A practical Shortwave setup path: connect Gmail, configure AI triage, test search and scheduled send, then decide if the paid tier earns its seat.',
        'tool': 'Shortwave',
        'sources': [
            ('Shortwave', 'https://www.shortwave.com/'),
            ('Shortwave pricing', 'https://www.shortwave.com/pricing/'),
        ],
        'steps': [
            ('Connect your Gmail account', 'Sign in with Google and grant Shortwave access to your Gmail. Start with a personal or secondary email if you want to test before committing your primary inbox.'),
            ('Configure AI triage', 'Let Shortwave analyze your inbox and suggest triage rules. Review the suggestions and adjust what gets pinned, snoozed, or bundled.'),
            ('Test AI search', 'Try searching your email history using natural language. Compare results with Gmail native search to see if the AI search saves you time.'),
            ('Try scheduled send and reminders', 'Schedule an email to send later and set a reminder to follow up. Decide if these features justify a paid tier for your workflow.'),
            ('Decide on the paid tier', 'If you process 50+ emails daily and the free tier limits interrupt your workflow, compare Business $30/seat against your time savings.'),
        ],
        'check': [
            'Gmail connected',
            'AI triage configured',
            'AI search tested',
            'Scheduled send tested',
            'Paid tier decision made',
        ],
    },
    {
        'slug': 'get-started-with-browse-ai',
        'title': 'How to get started with Browse AI for web automation',
        'summary': 'A practical Browse AI setup path: build your first robot, train it on a website, schedule runs, and decide if the paid tier is worth it.',
        'tool': 'Browse AI',
        'sources': [
            ('Browse AI', 'https://www.browse.ai/'),
            ('Browse AI pricing', 'https://www.browse.ai/pricing'),
        ],
        'steps': [
            ('Create your first robot', 'Use the visual trainer to teach Browse AI to extract data from one website. Start with a simple page — pricing, headlines, or product listings.'),
            ('Test the extraction', 'Run the robot and verify the extracted data is accurate. Adjust the training if it misses fields or captures wrong elements.'),
            ('Schedule regular runs', 'Set up a schedule for the robot to run daily or weekly. Configure notifications so you know when data changes.'),
            ('Monitor usage', 'Track how many websites you are monitoring and how many runs you need. The free tier allows unlimited robots but only 2 websites.'),
            ('Decide on the paid tier', 'If you need more than 2 websites or faster run frequency, compare Personal $48/month against the value of the data you are extracting.'),
        ],
        'check': [
            'First robot created',
            'Extraction verified',
            'Schedule configured',
            'Usage monitored',
            'Paid tier decision made',
        ],
    },
    {
        'slug': 'get-started-with-rows',
        'title': 'How to get started with Rows for AI-native spreadsheets',
        'summary': 'A practical Rows setup path: import data, try AI transformations, connect integrations, and decide if the paid tier earns its seat.',
        'tool': 'Rows',
        'sources': [
            ('Rows', 'https://rows.com/'),
            ('Rows pricing', 'https://rows.com/pricing'),
        ],
        'steps': [
            ('Import your data', 'Start with a CSV import or connect an integration. The free tier offers manual data import and 10 integration accounts.'),
            ('Try AI transformations', 'Use AI to clean, categorize, or enrich your data. The free tier includes 5 AI tasks per month — test whether they save you time.'),
            ('Connect an integration', 'Pull data from an API or service directly into your spreadsheet. Test whether the integration works with your data source.'),
            ('Collaborate with teammates', 'Share your spreadsheet and test real-time collaboration. Decide if the free tier covers your team size.'),
            ('Decide on the paid tier', 'If you need more than 5 AI tasks/month or more integrations, compare paid tiers against your productivity gain.'),
        ],
        'check': [
            'Data imported',
            'AI transformations tested',
            'Integration connected',
            'Collaboration tested',
            'Paid tier decision made',
        ],
    },
    {
        'slug': 'get-started-with-speechify',
        'title': 'How to get started with Speechify for text-to-speech',
        'summary': 'A practical Speechify setup path: import documents, test voices and speed, try scanning, and decide if the premium tier earns its seat.',
        'tool': 'Speechify',
        'sources': [
            ('Speechify', 'https://speechify.com/'),
            ('Speechify pricing', 'https://speechify.com/pricing/'),
        ],
        'steps': [
            ('Import a document', 'Start with a PDF, article, or document you actually need to process. Test whether the import handles formatting correctly.'),
            ('Test voices and speed', 'Try different voices and speed settings. The free tier offers up to 1.5x speed and 10 voices — test whether they meet your needs.'),
            ('Try scanning and OCR', 'Use the camera to scan printed text and convert it to speech. Test accuracy with your typical documents.'),
            ('Test the browser extension', 'Install the extension and try listening to web pages. Decide if this is something you would use regularly.'),
            ('Decide on the premium tier', 'If you need natural voices, higher speed limits, or scanning regularly, compare Premium against the time saved.'),
        ],
        'check': [
            'Document imported',
            'Voices and speed tested',
            'Scanning tested',
            'Browser extension tested',
            'Premium tier decision made',
        ],
    },
]

def e(x): return escape(str(x), quote=True)

def page(g):
    steps = ''.join(f'<li><h2>{e(t)}</h2><p>{e(d)}</p></li>' for t, d in g['steps'])
    sources = ''.join(f'<li><a href="{e(u)}" target="_blank" rel="external noopener">{e(n)} ↗</a></li>' for n, u in g['sources'])
    checks = ''.join(f'<li>{e(x)}</li>' for x in g['check'])
    schema = json.dumps({'@context': 'https://schema.org', '@type': 'HowTo', 'name': g['title'], 'description': g['summary'], 'url': f'{DOMAIN}/how-to/{g["slug"]}.html', 'step': [{'@type': 'HowToStep', 'name': t, 'text': d} for t, d in g['steps']]}, separators=(',', ':'))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(g['summary'])}"><title>{e(g['title'])} | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/how-to/{g['slug']}.html"><link rel="stylesheet" href="../css/styles.css"><link rel="stylesheet" href="../css/share.css"><script type="application/ld+json">{schema}</script></head><body><header class="global-nav"><a class="brand" href="../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="../tools/index.html">Tools</a><a href="../fit-interview/">Fit interview</a><a href="../change-radar/">Change radar</a><a href="../articles/learn.html">Learn</a><a href="../pricing/">Premium</a></nav></header><main><section class="scene scene-dark"><div class="howto-hero"><p class="kicker">How-to · {e(g['tool'])}</p><h1>{e(g['title'])}</h1><p class="subhead">{e(g['summary'])}</p><p class="howto-disclaimer">Setup commands, limits, and security terms change. Follow the linked official documentation before running anything.</p><p><a class="button button-blue" href="/newsletter/" style="margin-left:8px">Keep/Cut Weekly</a></p></div></section><section class="scene scene-light"><article class="howto-article"><div class="howto-callout"><strong>Before you start</strong><p>Use a test profile, synthetic data, and no production credentials. This guide is strategy and evaluation guidance, not managed implementation or support.</p></div><ol class="howto-steps">{steps}</ol><section class="howto-check"><h2>Completion checklist</h2><ul>{checks}</ul></section><section class="howto-sources"><h2>Official sources</h2><ul>{sources}</ul></section><p class="howto-next"><a class="button button-blue" href="../tools/{e(g['tool'].lower().replace(' ', '-'))}/">Review tool →</a><a class="button button-dark" href="../decision-brief.html">Create a decision brief</a></p></article></section></main><footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="../methodology/">Methodology</a><a href="../legal/affiliate-disclosure.html">Affiliate disclosure</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a></footer></body></html>'''

def generate(root: Path):
    out = root / 'how-to'
    out.mkdir(exist_ok=True)
    written = 0
    for g in GUIDES:
        p = out / f'{g["slug"]}.html'
        if p.exists():
            continue
        p.write_text(page(g))
        written += 1
    
    # Regenerate the hub to include all how-to guides (local + SaaS)
    _rebuild_hub(out)
    
    if written:
        print(f'SaaS how-to guides: {written} written')
    return written

def _rebuild_hub(out: Path):
    """Rebuild how-to/index.html from all existing guide files."""
    import re
    cards = []
    for f in sorted(out.glob('*.html')):
        if f.name == 'index.html':
            continue
        html = f.read_text()
        title_match = re.search(r'<h1>([^<]*)</h1>', html)
        title = title_match.group(1) if title_match else f.stem.replace('-', ' ').title()
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
        desc = desc_match.group(1) if desc_match else title
        cards.append(f'<article class="content-hub-card"><span>How-to</span><h2><a href="{f.name}">{escape(title)}</a></h2><p>{escape(desc)}</p></article>')
    
    hub = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Evidence-first how-to guides for AI tools: setup, configuration, security, and workflow optimization."><title>AI Tool How-To Guides | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/how-to/"><link rel="stylesheet" href="../css/styles.css"><link rel="stylesheet" href="../css/share.css"></head><body><header class="global-nav"><a class="brand" href="../index.html">✦ AIToolsEssentials</a><nav class="nav-links"><a href="../tools/index.html">Tools</a><a href="../fit-interview/">Fit interview</a><a href="../change-radar/">Change radar</a><a href="../articles/learn.html">Learn</a></nav><a class="nav-cta" href="../pricing/">Premium</a></header><main><section class="scene scene-dark"><div class="howto-hero"><p class="kicker">Practical setup library</p><h1>How to set up, secure, and optimize AI tools.</h1><p class="subhead">Source-linked setup guides for runtimes, agent gateways, browsers, email, automation, and productivity tools.</p></div></section><section class="scene scene-light"><div class="content-hub-grid">{''.join(cards)}</div></section><p style="text-align:center;margin-top:14px"><a class="button button-blue" href="/newsletter/">Keep/Cut Weekly</a></p></main><footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="../methodology/">Methodology</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a></footer></body></html>'''
    (out / 'index.html').write_text(hub)

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    print(generate(root))