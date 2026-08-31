#!/usr/bin/env python3
"""Generator-driven static comparison pages from tools.json/tool_sources.json."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://aitoolsessentials.com'
EMAIL = 'contact@aitoolsessentials.com'

TOOLS = {t['slug']: t for t in json.loads((ROOT / 'data/tools.json').read_text())}
SOURCES = {x['slug']: x for x in json.loads((ROOT / 'data/tool_sources.json').read_text()).get('tools', [])}
try:
    BENCH = json.loads((ROOT / 'data/benchmarks.json').read_text())
except Exception:
    BENCH = {}
try:
    LINEUPS = json.loads((ROOT / 'data/model_lineups.json').read_text())
except Exception:
    LINEUPS = {}


def _e(x):
    return re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9a-fA-F]+;)', '&amp;', str(x)).replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def _source_card(slug, name):
    src = SOURCES.get(slug)
    if not src:
        return ''
    links = ''.join(
        f'<a href="{_e(src[k])}" target="_blank" rel="external noopener">{label} ↗</a>'
        for k, label in [('pricing_url', 'Pricing'), ('docs_url', 'Docs'), ('privacy_url', 'Privacy'), ('rights_url', 'Rights')]
        if src.get(k)
    )
    unresolved = ''.join(f'<li>{_e(x)}</li>' for x in src.get('unresolved_claims', []))
    unresolved_html = f'<details><summary>Open verification questions</summary><ul>{unresolved}</ul></details>' if unresolved else ''
    return (
        f'<div><strong>{_e(name)}</strong>'
        f'<p>{_e(src.get("pricing_summary", ""))}</p>'
        f'<span>Official sources checked {_e(src.get("pricing_checked_date", ""))}</span>'
        f'<div class="official-source-links">{links}</div>'
        f'{unresolved_html}'
        f'<p class="source-notes">{_e(src.get("verification_notes", ""))}</p>'
        f'</div>'
    )


def _bench_section(slugs):
    lines = []
    for key in ['arena_text_snapshot', 'coding_agent_snapshot']:
        for entry in BENCH.get(key, []):
            if entry.get('tool_slug') in slugs:
                if key == 'arena_text_snapshot':
                    lines.append(
                        f"{entry['model']} — rank #{entry['rank']}, {entry['score']} ({entry.get('votes', 0):,} votes; snapshot {BENCH.get('snapshot_date', '')})."
                    )
                else:
                    lines.append(
                        f"{entry['benchmark']} · {entry.get('configuration', '')} — {entry['score']} over {entry.get('trials', 0)} trials (run {entry.get('run_date', '')})."
                    )
    if not lines:
        return ''
    lis = ''.join(f'<li>{_e(l)}</li>' for l in lines)
    return (
        '<h3>External benchmark context</h3><ul>' + lis + '</ul>'
        '<p class="benchmark-caveat">Benchmark records apply only to the exact model/configuration shown—not the whole product. '
        'Independent same-task hands-on comparison: <strong>not yet published</strong>. '
        '<a href="/legal/testing-protocol.html">See the testing protocol</a>.</p>'
    )


def _lineup_section(slug, name):
    tools_lineups = LINEUPS.get('tools', {})
    data = tools_lineups.get(slug)
    if not data:
        return ''
    checked = data.get('checked_date', '')
    rows = []
    for model in data.get('models', [])[:6]:
        rows.append(
            '<tr>'
            f'<td><strong>{_e(model.get("name", ""))}</strong></td>'
            f'<td>{_e(model.get("role", ""))}</td>'
            f'<td>{_e(model.get("context", ""))}</td>'
            f'<td>{_e(model.get("pricing", ""))}</td>'
            '</tr>'
        )
    if not rows:
        return ''
    tbody = ''.join(rows)
    return (
        '<section class="comparison-evidence"><h2>Current model lineup</h2>'
        f'<p>Version names and prices move fast. This panel tracks what {_e(name)} actually ships today, with checked dates — so the comparison stays about real models, not marketing names.</p>'
        '<div class="decision-grid"><div>'
        f'<strong>{_e(name)} — current lineup ({_e(checked)})</strong>'
        '<div class="table-wrap"><table><thead><tr><th>Model</th><th>Role</th><th>Context</th><th>Pricing</th></tr></thead><tbody>'
        f'{tbody}'
        '</tbody></table></div>'
        '<ul class="lineup-notes"><li>Verify current names at the official site — vendors iterate point releases frequently.</li></ul>'
        '</div></div></section>'
    )


def _decision_brief_link(slugs):
    return f'<p style="text-align:center;margin-top:14px"><a class="button button-ghost-dark" href="/decision-brief.html?vs={",".join(slugs)}">Get a shareable decision brief for this matchup →</a></p>'


def _premium_module():
    return (
        '<section class="newsletter-panel premium-conversion-panel"><div><span>Premium research layer</span>'
        '<h2>Want the member-only decision archive?</h2>'
        '<p>Premium adds monthly research briefs, stack-audit templates, weekly checklists, tool-change alerts, hands-on protocols, ROI calculators, and member-requested deep dives through Whop.</p>'
        '<p class="affiliate-inline">7-day free trial · then $12/month · code LAUNCH50 for 50% off first paid month · Whop handles billing and access · research and strategy only.</p>'
        '</div><div class="newsletter-actions">'
        '<a class="button button-blue" href="https://whop.com/checkout/ch_DKm5yxA1OBXoDru/" rel="external noopener">Subscribe on Whop</a>'
        '<a class="button button-dark" href="/premium/">See Premium library</a>'
        '<a class="button button-dark" href="/premium/faq.html">FAQ</a>'
        '</div></section>'
    )


def generate_best_ai_tools(root: Path):
    tools = sorted(TOOLS.values(), key=lambda x: (-x.get('rating', 0), _e(x.get('name', ''))))
    by_cat = {}
    for t in tools:
        by_cat.setdefault(t.get('category', 'Other'), []).append(t)
    cat_rows = []
    for cat, items in sorted(by_cat.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        rows = []
        for t in items[:8]:
            rows.append(
                '<tr>'
                f'<td><a href="../tools/{t["slug"]}/">{_e(t["name"])}</a></td>'
                f'<td>{_e(t.get("category", ""))}</td>'
                f'<td>{_e(t.get("best_for", t.get("summary", "")))}</td>'
                f'<td>{_e(str(t.get("rating", "")))}/5</td>'
                '</tr>'
            )
        cat_rows.append(f'<h2>{_e(cat)}</h2><div class="table-wrap"><table><thead><tr><th>Tool</th><th>Category</th><th>Best for</th><th>Score</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

    cards = ''.join(
        '<article class="directory-card" style="min-height:260px">'
        f'<div><span class="category-pill">{i} · {t.get("rating", "")}/5</span>'
        f'<h3><a href="../tools/{t["slug"]}/">{_e(t["name"])}</a></h3>'
        f'<p>{_e(t.get("best_for", t.get("summary", "")))}</p>'
        '</div></article>'
        for i, t in enumerate(tools[:20], start=1)
    )
    body = (
        '<section class="scene scene-dark hero compact-hero"><div class="hero-copy">'
        '<p class="kicker">Best AI tools</p>'
        f'<h1>The practical AI shortlist for 2026.</h1>'
        f'<p class="subhead">A revenue-ready comparison page covering {len(tools)} important AI products across assistants, search, creative, coding, automation, meetings, and productivity.</p>'
        '</div></section>'
        '<section class="scene scene-light comparison-section"><div class="article-shell wide">'
        '<h2>Best AI tools by category</h2>'
        '<p>This is a living shortlist, not a claim that the AI market is finite. AIToolsEssentials will keep expanding and pruning tools based on adoption, buyer intent, practical usefulness, and monetization fit.</p>'
        f'{"".join(cat_rows)}'
        '</div></section>'
        '<section class="scene scene-light comparison-section"><div class="article-shell wide"><h2>Top 20 tools</h2><div class="directory-grid" style="max-width:980px">'
        f'{cards}'
        '</div></div></section>'
    )
    page = _wrap('Best AI Tools — AIToolsEssentials', 'The best AI tools organized by category, workflow fit, and practical use case.', 'Best AI tools', body, 'best-ai-tools.html')
    (root / 'comparisons' / 'best-ai-tools.html').write_text(page)
    return 'best-ai-tools.html'


def generate_versus(root: Path, fname: str, a: str, b: str, c: str = ''):
    slugs = [s for s in [a, b, c] if s]
    names = [TOOLS[s]['name'] for s in slugs]
    title = fname.replace('.html', '').replace('-', ' ').title().replace('Vs', 'vs').replace('N8N', 'n8n')
    kicker = 'Versus comparison'
    if any(x in TOOLS[s].get('category', '') for s in slugs for x in ['Video', 'Creative']):
        kicker = 'Video comparison' if any('Video' in TOOLS[s].get('category', '') for s in slugs) else 'Design comparison'
    if any('Coding' in TOOLS[s].get('category', '') for s in slugs):
        kicker = 'Coding comparison'
    if any('Automation' in TOOLS[s].get('category', '') for s in slugs):
        kicker = 'Automation comparison'
    if any('Productivity' in TOOLS[s].get('category', '') for s in slugs):
        kicker = 'Productivity comparison'
    if any('Research' in TOOLS[s].get('category', '') for s in slugs):
        kicker = 'Research comparison'
    if any('Marketing' in TOOLS[s].get('category', '') for s in slugs):
        kicker = 'Marketing comparison'
    if any('Meetings' in TOOLS[s].get('category', '') for s in slugs):
        kicker = 'Meetings comparison'
    if any('Audio' in TOOLS[s].get('category', '') for s in slugs):
        kicker = 'Audio comparison'
    subhead = ' · '.join(TOOLS[s].get('best_for', '') for s in slugs)

    header_cells = ''.join(f'<th>{_e(n)}</th>' for n in names)
    rows = (
        '<tr><th>Best for</th>' + ''.join(f'<td>{_e(TOOLS[s].get("best_for",""))}</td>' for s in slugs) + '</tr>'
        '<tr><th>Category</th>' + ''.join(f'<td>{_e(TOOLS[s].get("category",""))}</td>' for s in slugs) + '</tr>'
        '<tr><th>Price</th>' + ''.join(f'<td>{_e(TOOLS[s].get("price","Free + paid plans"))}</td>' for s in slugs) + '</tr>'
        '<tr><th>AIToolsEssentials score</th>' + ''.join(f'<td>{_e(str(TOOLS[s].get("rating","")))}/5</td>' for s in slugs) + '</tr>'
    )
    cards = ''.join(_source_card(s, TOOLS[s]['name']) for s in slugs)
    review_links = ' '.join(f'<a class="button button-blue" href="../tools/{s}/">Read {_e(TOOLS[s]["name"])} review</a>' for s in slugs)
    bench = _bench_section(set(slugs))
    lineup = ''.join(_lineup_section(s, TOOLS[s]['name']) for s in slugs)

    body = (
        f'<section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">{_e(kicker)}</p>'
        f'<h1>{_e(title)}</h1><p class="subhead">{_e(subhead)}</p></div></section>'
        '<section class="scene scene-light comparison-section"><div class="article-shell wide">'
        '<div class="table-wrap"><table><thead><tr><th>Decision point</th>' + header_cells + '</tr></thead><tbody>' + rows + '</tbody></table></div>'
        '<section class="comparison-evidence"><h2>Evidence status</h2><div class="decision-grid">' + cards + '</div>' + bench + '</section>'
        f'{lineup}'
        '<h2>How to decide</h2>'
        '<p>Match each platform to your actual workflow constraints. Run one real workflow in each finalist before paying.</p>'
        '<h2>Quick recommendation</h2>'
        '<p>Use the trial checklist on each review page and the free scorecard to record time-to-result, corrections needed, and monthly cost at your expected volume before committing to a plan.</p>'
        f'<p>{review_links} <a class="button button-dark" href="../downloads/ai-tool-evaluation-scorecard.html">Open scorecard</a></p>'
        '</div></section>'
        '<section class="newsletter-panel"><div><span>AI Tool Evaluation Scorecard</span>'
        '<h2>Use the AI Tool Evaluation Scorecard</h2>'
        '<p>Compare AI tools by workflow fit, quality, review time, privacy, collaboration, cost, and ROI before paying for another subscription.</p>'
        '<p class="affiliate-inline">Official product links remain in place until an affiliate program is approved. The scorecard requires no email signup.</p>'
        '</div><div class="newsletter-actions">'
        '<a class="button button-blue" href="../downloads/ai-tool-evaluation-scorecard.html">Open scorecard</a>'
        '<a class="button button-dark" href="../benchmarks/">Open benchmarks</a>'
        '<a class="button button-dark" href="../categories/">Browse categories</a>'
        '</div></section>'
        f'{_decision_brief_link(slugs)}'
        '<section class="score-card related-next-steps"><span>Related next steps</span><h2>Turn this page into a decision.</h2>'
        '<p><a class="button button-blue" href="/stack-builder.html">Generate stack</a>'
        '<a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a>'
        '<a class="button button-blue" href="/compare-shortlist.html" style="margin-left:8px">Compare shortlist</a></p></section>'
        '<section class="score-card related-next-steps"><span>Related</span><h3>Next reads</h3>'
        '<p><a href="/pricing-watch/">Pricing Watch</a> · <a href="/change-radar/">Change Radar</a> · <a href="/premium/">Premium</a> · <a href="/newsletter/">Newsletter</a></p></section>'
        f'{_premium_module()}'
    )
    page = _wrap(f'{title} — AIToolsEssentials', subhead, kicker, body, fname)
    (root / 'comparisons' / fname).write_text(page)
    return fname


def _wrap(title, description, kicker, body, canonical_name):
    schema = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'Article',
        'name': title,
        'description': description,
        'url': f'{DOMAIN}/comparisons/{canonical_name}',
        'isPartOf': {'@type': 'WebSite', 'name': 'AIToolsEssentials', 'url': DOMAIN},
        'publisher': {'@type': 'Organization', 'name': 'AIToolsEssentials', 'url': DOMAIN},
        'headline': title,
        'author': {'@type': 'Organization', 'name': 'AIToolsEssentials'}
    })
    faq_schema = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': 'How were these recommendations verified?',
                'acceptedAnswer': {'@type': 'Answer', 'text': 'Pricing and claims trace to each vendor\'s official page with a checked date; editorial scores are independent of sponsorships and affiliate relationships.'}
            },
            {
                '@type': 'Question',
                'name': 'Are the affiliate links on this page paid placements?',
                'acceptedAnswer': {'@type': 'Answer', 'text': 'Some outbound tool links are affiliate links. They never change rankings or scores, and every page carries an FTC-compliant disclosure.'}
            }
        ]
    })
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{_e(description)}">
<title>{_e(title)}</title>
<link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css">
<link rel="canonical" href="{DOMAIN}/comparisons/{canonical_name}">
<meta property="og:site_name" content="AIToolsEssentials">
<meta property="og:type" content="article">
<meta property="og:title" content="{_e(title)}">
<meta property="og:description" content="{_e(description)}">
<meta property="og:url" content="{DOMAIN}/comparisons/{canonical_name}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{_e(title)}">
<meta name="twitter:description" content="{_e(description)}">
<script type="application/ld+json">{faq_schema}</script>
<script type="application/ld+json">{schema}</script>
<!-- AIT STRUCTURED DATA START -->
<script type="application/ld+json">{{"@context":"https://***@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"Comparisons","item":"{DOMAIN}/comparisons/"}},{{"@type":"ListItem","position":3,"name":"{_e(kicker)}","item":"{DOMAIN}/comparisons/{canonical_name}"}}]}}</script>
<!-- AIT STRUCTURED DATA END -->
<!-- AIT DISCOVERY LINKS --><link rel="manifest" href="/site.webmanifest"><link rel="alternate" type="application/rss+xml" title="AIToolsEssentials updates" href="/feed.xml"><link rel="search" type="application/opensearchdescription+xml" title="AIToolsEssentials" href="/opensearch.xml"><meta name="theme-color" content="#5e6ad2"><script src="/js/discovery.js" defer></script>
<!-- AIT KNOWLEDGE SCHEMA START -->
<script type="application/ld+json">{{"@context":"https://***@graph":[{{"@type":"Organization","@id":"{DOMAIN}/#organization","name":"AIToolsEssentials","url":"{DOMAIN}","email":"{EMAIL}","logo":"{DOMAIN}/assets/aitools-bot-mark.svg"}},{{"@type":"WebSite","@id":"{DOMAIN}/#website","url":"{DOMAIN}","name":"AIToolsEssentials","publisher":{{"@id":"{DOMAIN}/#organization"}},"potentialAction":{{"@type":"SearchAction","target":"{DOMAIN}/tools/index.html?q={{search_term_string}}","query-input":"required name=search_term_string"}}}}]}}</script>
<!-- AIT KNOWLEDGE SCHEMA END -->
</head><body>
<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>
<nav class="nav-links"><a href="../tools/index.html">Tools</a><a href="../comparisons/best-ai-tools.html">Best AI tools</a><a href="../categories/index.html">Categories</a><a href="../articles/index.html">Guides</a><a href="../benchmarks/">Benchmarks</a>
<a href="../articles/learn.html">Learn</a><a href="../guides/switch-guides/">Switching</a></nav>
<a class="nav-cta" href="../legal/affiliate-disclosure.html">Disclosure</a></header>
<main>
{body}
</main>
<div id="share-row" hidden></div>
<footer class="footer">
<span>© 2026 AIToolsEssentials</span>
<a href="../advertise/index.html" rel="nofollow">Advertise</a>
<a href="../submit-tool.html" rel="nofollow">Submit a tool</a>
<a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
<a href="mailto:{EMAIL}">Contact</a>
<a href="../legal/about.html">About</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a><a href="../legal/corrections.html">Corrections</a>
</footer>
<script src="../js/site.js" defer></script>
<script src="../js/analytics.js" defer></script>
</body></html>'''


def generate_all(root: Path):
    made = []
    made.append(generate_best_ai_tools(root))
    versus = {
        'chatgpt-vs-claude.html': ('chatgpt', 'claude'),
        'chatgpt-vs-grok.html': ('chatgpt', 'grok'),
        'chatgpt-vs-perplexity.html': ('chatgpt', 'perplexity'),
        'claude-vs-cursor.html': ('claude', 'cursor'),
        'claude-vs-grok.html': ('claude', 'grok'),
        'grok-vs-chatgpt.html': ('grok', 'chatgpt'),
        'jasper-vs-copy-ai.html': ('jasper', 'copy-ai'),
        'midjourney-vs-canva-ai.html': ('midjourney', 'canva-ai'),
        'perplexity-vs-chatgpt.html': ('perplexity', 'chatgpt'),
        'perplexity-vs-gemini.html': ('perplexity', 'gemini'),
        'runway-vs-pika.html': ('runway', 'pika'),
        'gemini-vs-grok.html': ('gemini', 'grok'),
        'grok-vs-deepseek.html': ('grok', 'deepseek'),
        'claude-vs-deepseek.html': ('claude', 'deepseek'),
        'v0-vs-lovable.html': ('v0', 'lovable'),
        'bolt-new-vs-lovable.html': ('bolt-new', 'lovable'),
        'v0-vs-bolt-new.html': ('v0', 'bolt-new'),
        'fathom-vs-otter-ai.html': ('fathom', 'otter-ai'),
        'midjourney-vs-ideogram.html': ('midjourney', 'ideogram'),
        'descript-vs-riverside-fm.html': ('descript', 'riverside-fm'),
        'perplexity-vs-notebooklm.html': ('perplexity', 'notebooklm'),
        'ollama-vs-lm-studio.html': ('ollama', 'lm-studio'),
        'suno-vs-udio.html': ('suno', 'udio'),
    }
    for fname, (a, b) in versus.items():
        if a in TOOLS and b in TOOLS:
            made.append(generate_versus(root, fname, a, b))
    return made


if __name__ == '__main__':
    print('Generated static comparisons:', generate_all(ROOT))
