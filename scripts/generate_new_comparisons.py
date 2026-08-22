#!/usr/bin/env python3
"""Generate additional high-value comparison pages from verified source data."""
import html as H
import json
from pathlib import Path

NEW_COMPARISONS = {
    'cursor-vs-github-copilot.html': {
        'kicker': 'Coding comparison',
        'a': 'cursor', 'b': 'github-copilot',
        'subhead': 'An AI-first editor against the assistant built into every major IDE.',
        'bench_keys': ['coding_agent_snapshot'],
    },
    'zapier-vs-make-vs-n8n.html': {
        'kicker': 'Automation comparison',
        'a': 'zapier-ai', 'b': 'make', 'c': 'n8n',
        'subhead': 'Three automation platforms compared on pricing models, AI features, and self-hosting.',
        'bench_keys': [],
    },
    'chatgpt-vs-gemini.html': {
        'kicker': 'Versus comparison',
        'a': 'chatgpt', 'b': 'gemini',
        'subhead': 'The ecosystem-agnostic assistant against the one wired into Google Workspace and Android.',
        'bench_keys': ['arena_text_snapshot'],
    },
    'claude-vs-perplexity.html': {
        'kicker': 'Versus comparison',
        'a': 'claude', 'b': 'perplexity',
        'subhead': 'Deep document analysis and writing against source-backed web research.',
        'bench_keys': ['arena_text_snapshot'],
    },
    'chatgpt-vs-deepseek.html': {
        'kicker': 'Versus comparison',
        'a': 'chatgpt', 'b': 'deepseek',
        'subhead': 'The polished commercial default against the open-source value option.',
        'bench_keys': ['arena_text_snapshot'],
    },
    'heygen-vs-synthesia.html': {
        'kicker': 'Video comparison',
        'a': 'heygen', 'b': 'synthesia',
        'subhead': 'Two avatar-video leaders compared on plans, credits, consent rules, and output rights.',
        'bench_keys': [],
    },
    'elevenlabs-vs-descript.html': {
        'kicker': 'Audio & video comparison',
        'a': 'elevenlabs', 'b': 'descript',
        'subhead': 'Best-in-class voice generation against transcript-based editing — where they overlap and where they do not.',
        'bench_keys': [],
    },
    'notion-ai-vs-microsoft-copilot.html': {
        'kicker': 'Productivity comparison',
        'a': 'notion-ai', 'b': 'microsoft-copilot',
        'subhead': 'AI inside your docs workspace against AI across the Microsoft 365 estate.',
        'bench_keys': [],
    },
    'midjourney-vs-leonardo-ai.html': {
        'kicker': 'Image comparison',
        'a': 'midjourney', 'b': 'leonardo-ai',
        'subhead': 'Aesthetic quality leader against a controllable, credit-based production alternative.',
        'bench_keys': [],
    },
    'fireflies-vs-otter-ai.html': {
        'kicker': 'Meetings comparison',
        'a': 'fireflies', 'b': 'otter-ai',
        'subhead': 'Two meeting recorders compared on free-tier limits, storage, and team features.',
        'bench_keys': [],
    },
    'gamma-vs-canva-ai.html': {
        'kicker': 'Presentations comparison',
        'a': 'gamma', 'b': 'canva-ai',
        'subhead': 'Narrative-first deck generation against a full design suite with AI features.',
        'bench_keys': [],
    },
    'perplexity-vs-you-com.html': {
        'kicker': 'Research comparison',
        'a': 'perplexity', 'b': 'you-com',
        'subhead': 'Cited-answer search engines compared on focus, models available, and pricing.',
        'bench_keys': [],
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


def source_card(src, name):
    links = ''.join(
        f'<a href="{_e(src[k])}" target="_blank" rel="external noopener">{label} ↗</a>'
        for k, label in [('pricing_url','Pricing'),('docs_url','Docs'),('privacy_url','Privacy'),('rights_url','Rights')]
        if src.get(k))
    return (f'<div><strong>{_e(name)}</strong>'
            f'<p>{_e(src["pricing_summary"])}</p>'
            f'<span>Official sources checked {src["pricing_checked_date"]}</span>'
            f'<div class="official-source-links">{links}</div></div>')


def bench_section(bench, keys, slugs):
    lines = []
    for key in keys:
        for entry in bench.get(key, []):
            if entry.get('tool_slug') in slugs:
                if key == 'arena_text_snapshot':
                    lines.append(f"{entry['model']} — rank #{entry['rank']}, {entry['score']} ({entry['votes']:,} votes; snapshot {bench['snapshot_date']}).")
                else:
                    lines.append(f"{entry['benchmark']} · {entry.get('configuration','')} — {entry['score']} over {entry['trials']} trials (run {entry['run_date']}).")
    if not lines:
        return ''
    lis = ''.join(f'<li>{_e(l)}</li>' for l in lines)
    return (f'<h3>External benchmark context</h3><ul>{lis}</ul>'
            f'<p class="benchmark-caveat">Benchmark records apply only to the exact model/configuration shown—not the whole product. '
            f'Independent same-task hands-on comparison: <strong>not yet published</strong>. '
            f'<a href="../legal/testing-protocol.html">See the testing protocol</a>.</p>')


def generate(root: Path) -> int:
    tools = {t['slug']: t for t in json.loads((root/'data/tools.json').read_text())}
    srcs = {x['slug']: x for x in json.loads((root/'data/tool_sources.json').read_text())['tools']}
    bench = json.loads((root/'data/benchmarks.json').read_text())
    made = 0
    for fname, spec in NEW_COMPARISONS.items():
        slugs = [spec['a']] + ([spec['c']] if spec.get('c') else [])
        names = [tools[s]['name'] for s in slugs]
        title = fname.replace('.html','').replace('-', ' ').title().replace('Vs','vs').replace('N8N','n8n')
        rows = ''
        labels = ['Best for'] + ['Category']
        header_cells = ''.join(f'<th>{_e(n)}</th>' for n in names)
        best_cells = ''.join(f'<td>{_e(tools[s].get("best_for",""))}</td>' for s in slugs)
        cat_cells = ''.join(f'<td>{_e(tools[s].get("category",""))}</td>' for s in slugs)
        price_cells = ''.join(f'<td>See evidence below — official sources checked {srcs[s]["pricing_checked_date"]}</td>' for s in slugs)
        score_cells = ''.join(f'<td>{tools[s].get("rating","—")}/5</td>' if tools[s].get('rating') else '<td>Editorial score in review</td>' for s in slugs)
        rows = (f'<tr><th>Best for</th>{best_cells}</tr>'
                f'<tr><th>Category</th>{cat_cells}</tr>'
                f'<tr><th>Price</th>{price_cells}</tr>'
                f'<tr><th>AIToolsEssentials score</th>{score_cells}</tr>')
        cards = ''.join(source_card(srcs[s], tools[s]['name']) for s in slugs)
        review_links = ' '.join(f'<a class="button button-blue" href="../tools/{s}/">Read {_e(tools[s]["name"])} review</a>' for s in slugs)
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{_e(title)}: compare use cases, verified pricing, policy terms, and workflow fit."><title>{_e(title)} — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css"><!-- AIT SEO START -->
  <link rel="canonical" href="https://aitoolsessentials.com/comparisons/{fname}">
  <meta property="og:site_name" content="AIToolsEssentials">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{_e(title)} — AIToolsEssentials">
  <meta property="og:description" content="{_e(spec['subhead'])}">
  <meta property="og:url" content="https://aitoolsessentials.com/comparisons/{fname}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "Article", "name": "{_e(title)} — AIToolsEssentials", "url": "https://aitoolsessentials.com/comparisons/{fname}", "publisher": {{"@type": "Organization", "name": "AIToolsEssentials"}}}}</script>
  <!-- AIT SEO END -->

  <!-- AIT FAVICON START -->
  <link rel="icon" href="../assets/aitools-bot-mark.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../assets/aitools-bot-logo-256.png">
  <!-- AIT FAVICON END -->
</head><body>{HEADER}<main><section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">{_e(spec['kicker'])}</p><h1>{_e(title)}</h1><p class="subhead">{_e(spec['subhead'])}</p></div></section><section class="scene scene-light comparison-section"><div class="article-shell wide"><div class="table-wrap"><table><thead><tr><th>Decision point</th>{header_cells}</tr></thead><tbody>{rows}</tbody></table></div><!-- AIT COMPARISON EVIDENCE START --><section class="comparison-evidence"><h2>Evidence status</h2><div class="decision-grid">{cards}</div>{bench_section(bench, spec['bench_keys'], set(slugs))}</section><!-- AIT COMPARISON EVIDENCE END --><h2>How to decide</h2><p>Match each platform to your actual workflow constraints: editor preference and model access for coding tools; task-based versus credit-based versus execution-based pricing, self-hosting needs, and technical depth for automation. Run one real workflow in each finalist before paying.</p><h2>Quick recommendation</h2><p>Use the trial checklist on each review page and the free scorecard to record time-to-result, corrections needed, and monthly cost at your expected volume before committing to a plan.</p><p>{review_links} <a class="button button-dark" href="../downloads/ai-tool-evaluation-scorecard.html">Open scorecard</a></p></div></section><section class="newsletter-panel"><div><span>AI Tool Evaluation Scorecard</span><h2>Use the AI Tool Evaluation Scorecard</h2><p>Compare AI tools by workflow fit, quality, review time, privacy, collaboration, cost, and ROI before paying for another subscription.</p><p class="affiliate-inline">Official product links remain in place until an affiliate program is approved. The scorecard requires no email signup.</p></div><div class="newsletter-actions"><a class="button button-blue" href="../downloads/ai-tool-evaluation-scorecard.html">Open scorecard</a><a class="button button-dark" href="../benchmarks/">Open benchmarks</a></div></section>

</main><div id="share-row" hidden></div>
  {FOOTER}</body></html>'''
        (root/'comparisons'/fname).write_text(page)
        made += 1
    return made


if __name__ == '__main__':
    print(generate(Path(__file__).resolve().parent.parent))
