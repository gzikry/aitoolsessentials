#!/usr/bin/env python3
"""Generate audience-based buyer guides (freelancers, students, agencies, developers, small business)."""
import html as H
import json
from datetime import datetime
from pathlib import Path

GUIDES = {
    'best-ai-tools-for-freelancers.html': {
        'kicker': 'Audience guide', 'audience': 'freelancers',
        'title': 'Best AI tools for freelancers',
        'subhead': 'A lean AI stack for solo operators: one assistant, one writing tool, one automation platform — chosen by cost per delivered project.',
        'slugs': ['chatgpt','claude','canva-ai','zapier-ai','notion-ai','grammarly'],
        'angle': ('Freelancers feel every subscription personally, so the stack has to earn its keep '
                  'monthly. The pattern that works: one general assistant for drafting and analysis, '
                  'one client-facing production tool, and one automation to kill repetitive admin. '
                  'Start free-tier everywhere; only upgrade the single tool that saves you hours weekly.'),
    },
    'best-ai-tools-for-students.html': {
        'kicker': 'Audience guide', 'audience': 'students',
        'title': 'Best AI tools for students',
        'subhead': 'Free-first AI tools for research, writing, notes, and presentations — with academic-integrity guardrails.',
        'slugs': ['perplexity','chatgpt','gamma','otter-ai','notion-ai'],
        'angle': ('Students rarely need paid plans. The free tiers of Perplexity, ChatGPT, Gamma, and '
                  'Otter cover research, drafting, slides, and lecture capture. Two rules: verify every '
                  'citation against the actual source before it goes in your work, and check your '
                  'institution\'s AI policy per course — disclosure rules differ widely.'),
    },
    'best-ai-tools-for-agencies.html': {
        'kicker': 'Audience guide', 'audience': 'agencies',
        'title': 'Best AI tools for agencies',
        'subhead': 'Team-plan decisions for content production, design, meetings, and client reporting — evaluated on seats, permissions, and margin.',
        'slugs':['claude','jasper','copy-ai','adobe-firefly','heygen','fireflies'],
        'angle': ('Agencies buy seats, not subscriptions. The evaluation axis is different from solo use: '
                  'team workspaces, permission controls, brand-voice consistency, output rights you can '
                  'transfer to clients, and per-seat cost against billable value. Consumer plans usually '
                  'break here — check commercial-use terms before client delivery.'),
    },
    'best-ai-tools-for-developers.html': {
        'kicker': 'Audience guide', 'audience': 'developers',
        'title': 'Best AI tools for developers',
        'subhead': 'Coding assistants, app builders, and automation for engineering teams — with training-policy and code-ownership notes.',
        'slugs':['cursor','github-copilot','v0','bolt-new','replit-ai','n8n'],
        'angle': ('Developer tooling decisions hinge on two things beyond raw quality: whether your code '
                  'trains vendor models (Cursor: no unless opted in; check each vendor\'s current policy) '
                  'and where suggestions run (local context vs cloud). Prototype builders like v0 and '
                  'Bolt are for scaffolding, not production paths.'),
    },
    'best-ai-tools-for-consultants.html': {
        'kicker': 'Audience guide', 'audience': 'consultants',
        'title': 'Best AI tools for consultants',
        'subhead': 'Research, deck production, meeting capture, and analysis for client work — with confidentiality as a first-class constraint.',
        'slugs':['claude','perplexity','gamma','fireflies','microsoft-copilot'],
        'angle': ('Consultants trade on trust, so data-handling terms matter as much as capability. Before '
                  'putting client material into any tool, read its training policy: Claude consumer chats '
                  'may be used for training unless opted out; business tiers differ. Prefer tools with '
                  'explicit no-training commitments on your plan tier.'),
    },
    'best-ai-tools-for-healthcare-admin.html': {
        'kicker': 'Audience guide', 'audience': 'healthcare administrators and medical professionals',
        'title': 'Best AI tools for healthcare admin',
        'subhead': 'Documentation drafts, literature lookup, and practice-admin workflows for medical teams — with no implied HIPAA, FDA, or clinical-decision certification.',
        'slugs':['heidi-health','openevidence','dragon-copilot','microsoft-copilot','perplexity','otter-ai'],
        'angle': ('Healthcare buyers need a different filter than consumer AI shoppers. Separate '
                  'administrative drafting from anything that touches identifiable patient data, billing, '
                  'or the signed medical record. Heidi Health is the public self-serve documentation '
                  'starting point; OpenEvidence is official-homepage-free literature lookup for healthcare '
                  'professionals; Dragon Copilot is Microsoft quote-based enterprise documentation. '
                  'Vendor HIPAA marks are claims to verify in contract review, not certifications by this site. '
                  'Do not paste PHI into a general tool during a trial.'),
    },
    'best-ai-tools-for-lawyers.html': {
        'kicker': 'Audience guide', 'audience': 'lawyers and in-house counsel',
        'title': 'Best AI tools for lawyers',
        'subhead': 'Confidentiality-first tools for legal research, contract review, and drafting — with no implied privilege, bar, or legal-advice certification.',
        'slugs':['harvey','spellbook','cocounsel','claude','perplexity','microsoft-copilot'],
        'angle': ('Legal buyers start with privilege, not features. Harvey is the quote-based enterprise '
                  'platform for firms and in-house teams. Spellbook is Word-native contract review and drafting. '
                  'CoCounsel Legal is Thomson Reuters’ Westlaw- and Practical Law-grounded assistant; the only '
                  'official dollar figure recorded here is Westlaw Advantage with CoCounsel Essentials starting '
                  'at $415.35/month. Consumer chat tiers are the wrong place for client-identifiable files. '
                  'Verify every citation in a primary research product before advice or filing.'),
    },
    'best-ai-tools-for-teachers.html': {
        'kicker': 'Audience guide', 'audience': 'teachers and instructional coaches',
        'title': 'Best AI tools for teachers',
        'subhead': 'Free-first tools for lesson plans, rubrics, slides, and family emails — with no implied FERPA, grading, or student-data certification.',
        'slugs':['magicschool','khanmigo','canva-ai','gamma','chatgpt','perplexity'],
        'angle': ('Teachers should start on official free education tiers, not a $20 chatbot, unless a general '
                  'assistant already owns a weekly task. MagicSchool publishes a $0 individual teacher plan and '
                  'Plus at $12.99/month or $8.33/month billed annually. Khanmigo’s official teacher page states '
                  'teacher tools are free; learner and family plans are $4/month or $44/year, and classroom student '
                  'access is a district implementation, not a teacher-account toggle. Vendor FERPA/COPPA marks are '
                  'claims to verify with your school. Do not paste identifiable student records into a personal chat.'),
    },
    'best-ai-tools-for-nonprofits.html': {
        'kicker': 'Audience guide', 'audience': 'nonprofit staff and grant writers',
        'title': 'Best AI tools for nonprofits',
        'subhead': 'Grant-writing and development tools with published free or trial paths — and no implied fundraising, tax, or award certification.',
        'slugs':['grantable','instrumentl','chatgpt','claude','notion-ai','canva-ai'],
        'angle': ('Small nonprofits should not start on a $299/month grant database. Grantable publishes a real '
                  'free plan (5 messages/day) plus Starter at $50/month and Pro at $150/month, with a one-year 50% '
                  'discount to $25/$75 for qualifying 501(c)(3)s under about $500K. Instrumentl is the paid discovery '
                  'and lifecycle platform: official Discover is $299/month billed annually or $349 monthly, with a '
                  '14-day free trial. Vendor win-rate and revenue-uplift claims are marketing. Keep eligibility, '
                  'budgets, and authorized submissions with a human grant lead.'),
    },
    'best-ai-tools-for-podcasters.html': {
        'kicker': 'Audience guide', 'audience': 'podcasters and show producers',
        'title': 'Best AI tools for podcasters',
        'subhead': 'Record, enhance, edit, clip, and voice a weekly show — with published free or trial paths and no implied music-rights or likeness certification.',
        'slugs':['riverside','adobe-podcast','descript','elevenlabs','canva-ai','chatgpt'],
        'angle': ('Start on official free recording and cleanup tiers before stacking Descript plus a voice lab. '
                  'Riverside publishes Free at $0 with a 2-hour one-off multi-track allowance, then Pro at $24/month '
                  'billed annually or $29 monthly. Adobe Podcast publishes Free Enhance Speech and Studio limits and '
                  'a 30-day Premium trial, but no official USD Premium price on the plans page. Descript and ElevenLabs '
                  'stay in the stack for transcript editing and voiceover. Check guest consent, voice-clone rights, '
                  'and watermarks before you publish.'),
    },
}

HEADER = '<header class="global-nav"><a class="brand" href="../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="../tools/index.html">Tools</a><a href="../comparisons/best-ai-tools.html">Best AI tools</a><a href="../categories/index.html">Categories</a><a href="../articles/index.html">Guides</a><a href="../benchmarks/">Benchmarks</a>\n</nav><a class="nav-cta" href="../legal/affiliate-disclosure.html">Disclosure</a></header>'

FOOTER = '''<footer class="footer">
    <span>© 2026 AIToolsEssentials</span>
    <a href="../advertise/index.html" rel="nofollow">Advertise</a>
    <a href="../submit-tool.html" rel="nofollow">Submit a tool</a>
    <a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
    <a href="mailto:contact@aitoolsessentials.com">Contact</a>
  <a href="../legal/about.html">About</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a><a href="../legal/corrections.html">Corrections</a></footer><script src="../js/site.js" defer></script>
<script src="../js/analytics.js" defer></script>'''


def _e(x): return H.escape(str(x))


def generate(root: Path) -> int:
    tools = {t['slug']: t for t in json.loads((root/'data/tools.json').read_text())}
    srcs = {x['slug']: x for x in json.loads((root/'data/tool_sources.json').read_text())['tools']}
    today = datetime.today().strftime('%B %d, %Y')
    made = 0
    articles_dir = root/'articles'
    for fname, spec in GUIDES.items():
        cards = ''
        picks = []
        for s in spec['slugs']:
            t = tools[s]
            checked = srcs[s].get('pricing_checked_date', '')
            cards += (f'<article class="tool-pick"><div class="pick-head"><h3>{_e(t["name"])}</h3>'
                      f'<span class="pick-score">{t.get("rating","—")}/5 editorial</span></div>'
                      f'<p>{_e(t.get("summary",""))}</p>'
                      f'<p class="pick-meta">Category: {_e(t["category"])} · Pricing verified {_e(checked)}</p>'
                      f'<div class="pick-actions"><a class="button button-blue" href="../tools/{s}/">Read review</a>'
                      f'<a class="text-link" href="../legal/testing-protocol.html">How we test</a></div></article>')
            picks.append(t['name'])
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{_e(spec['title'])}: {_e(spec['subhead'])}"><title>{_e(spec['title'])} — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css"><!-- AIT SEO START -->
  <link rel="canonical" href="https://aitoolsessentials.com/articles/{fname}">
  <meta property="og:site_name" content="AIToolsEssentials"><meta property="og:type" content="article">
  <meta property="og:title" content="{_e(spec['title'])} — AIToolsEssentials">
  <meta property="og:description" content="{_e(spec['subhead'])}">
  <meta property="og:url" content="https://aitoolsessentials.com/articles/{fname}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "Article", "name": "{_e(spec['title'])}", "headline": "{_e(spec['title'])}", "description": "{_e(spec['subhead'])}", "url": "https://aitoolsessentials.com/articles/{fname}", "author": {{"@type": "Organization", "name": "AIToolsEssentials"}}, "publisher": {{"@type": "Organization", "name": "AIToolsEssentials"}}}}</script>
  <!-- AIT SEO END -->

  <!-- AIT FAVICON START -->
  <link rel="icon" href="../assets/aitools-bot-mark.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../assets/aitools-bot-logo-256.png">
  <!-- AIT FAVICON END -->
</head><body>{HEADER}<main><section class="scene scene-light article-hero"><p class="kicker light">{_e(spec['kicker'])}</p><h1>{_e(spec['title'])}</h1><p>{_e(spec['subhead'])}</p><p class="last-updated">Official sources checked {today} · Editorial scores are AIToolsEssentials ratings, not benchmarks · Independent hands-on results not yet published</p><div class="actions"><a class="button button-blue" href="../tools/index.html">Browse all tools</a><a class="button button-dark" href="../downloads/premium/aitools-premium-comparison-archive-2026-09.csv">Download comparison archive</a></div></section>
<section class="scene scene-light"><article class="article-shell">
<h2>How this stack is chosen</h2><p>{_e(spec['angle'])}</p>
<h2>The shortlist</h2>
{cards}
<h2>Before you pay for anything</h2>
<p>Run each finalist's trial checklist on one real task. Record time-to-result, corrections needed, and what the plan actually costs at your volume — then decide. Our <a href="../downloads/ai-tool-evaluation-scorecard.html">free scorecard</a> gives you the template.</p>
<p class="monetization-note">Official product links remain in place until affiliate programs are approved and verified.</p>
</article></section>
<section class="newsletter-panel"><div><span>AI Tool Evaluation Scorecard</span><h2>Decide with evidence, not demos</h2><p>Compare candidates on workflow fit, quality, review time, privacy, collaboration, cost, and ROI.</p><p class="affiliate-inline">No email required. No newsletter signup.</p></div><div class="newsletter-actions"><a class="button button-blue" href="../downloads/ai-tool-evaluation-scorecard.html">Open scorecard</a><a class="button button-dark" href="../benchmarks/">See benchmark evidence</a></div></section>

</main><div id="share-row" hidden></div>
  {FOOTER}</body></html>'''
        (articles_dir/fname).write_text(page)
        made += 1
    return made


if __name__ == '__main__':
    print(generate(Path(__file__).resolve().parent.parent))
