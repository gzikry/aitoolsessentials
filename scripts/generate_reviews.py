#!/usr/bin/env python3
"""Enriched tool review page generator for AIToolsEssentials.
Called from daily_content_update.py. Expects `root`, `today`, `tools` in caller scope
when run as a function; can also run standalone."""
import json
import re
from pathlib import Path

DOMAIN = 'https://aitoolsessentials.com'
EMAIL = 'contact@aitoolsessentials.com'

from affiliate_util import approved_programs, public_affiliate_href, NOUS_OFFER


def _source_record(root: Path, slug: str):
    path = root / 'data/tool_sources.json'
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return next((x for x in data.get('tools', []) if x.get('slug') == slug), None)


def _official_source_html(record) -> str:
    if not record:
        return '<div class="official-source-card pending"><span>Source status</span><strong>Official verification pending</strong><p>Verify the vendor pricing and policy pages before purchasing.</p></div>'
    labels = [('Official pricing', 'pricing_url'), ('Product documentation', 'docs_url'), ('Privacy / data use', 'privacy_url'), ('Rights / terms', 'rights_url')]
    links = ''.join(
        f'<a href="{record[key]}" target="_blank" rel="external noopener">{label} ↗</a>'
        for label, key in labels if record.get(key)
    )
    unresolved = ''.join(f'<li>{x}</li>' for x in record.get('unresolved_claims', []))
    unresolved_html = f'<details><summary>Open verification questions</summary><ul>{unresolved}</ul></details>' if unresolved else ''
    notes = record.get('verification_notes') or ''
    return f'''<div class="official-source-card"><span>Official sources checked {record.get('pricing_checked_date', '')}</span><p><strong>Current official summary:</strong> {record.get('pricing_summary') or 'No stable public pricing was verified.'}</p><div class="official-source-links">{links}</div>{unresolved_html}<p class="source-notes">{notes}</p></div>'''


def _price_rows(tool):
    detail = tool.get('pricing_detail')
    if detail:
        return [(r[0], f"{r[1]} — {r[2]}" if len(r) > 2 else r[1]) for r in detail]
    price = tool.get('price', '')
    rows = [('Entry price', price)]
    if 'free' in price.lower():
        rows.insert(0, ('Free tier', 'Yes'))
    else:
        rows.append(('Free tier', 'Not advertised — check current offers'))
    return rows


def _who_for(tool):
    cat = tool.get('category', '')
    best = tool.get('best_for', '')
    return (f"{tool['name']} is aimed at teams and individuals who need {best.lower().rstrip('.')}. "
            f"It is designed for {cat.lower()} workflows where output quality, adoption effort, and operating cost all matter. "
            f"Compare alternatives first if you require self-hosting, unusually deep customization, or tighter policy controls than the official plan provides.")


def _benchmark_html(root: Path, slug: str, category: str) -> str:
    path = root / 'data/benchmarks.json'
    if not path.exists():
        return ''
    data = json.loads(path.read_text())
    sources = {x['id']: x for x in data.get('sources', [])}
    snapshot = next((x for x in data.get('arena_text_snapshot', []) if x['tool_slug'] == slug), None)
    if snapshot:
        source = sources[snapshot['source_id']]
        return f'''<div class="review-benchmark">
<div class="review-benchmark-head"><div><span class="evidence-label">External benchmark snapshot</span><h3>Arena Text · {snapshot['model']}</h3><span class="benchmark-meta">Snapshot {data['snapshot_date']} · {snapshot['votes']:,} preference votes · exact model version shown</span></div><div class="review-benchmark-score"><strong>#{snapshot['rank']}</strong><small>Arena rank</small><span>{snapshot['score']}</span><em>rating ± 95% confidence interval</em></div></div>
<p>{snapshot['note']} This is supporting context—not the AIToolsEssentials product score. <a href="{source['url']}" target="_blank" rel="external noopener">Source [{source['id']}] ↗</a></p>
</div>'''
    coding_snapshot = next((x for x in data.get('coding_agent_snapshot', []) if x['tool_slug'] == slug), None)
    if coding_snapshot:
        source = sources[coding_snapshot['source_id']]
        return f'''<div class="review-benchmark">
<div class="review-benchmark-head"><div><span class="evidence-label">Verified agent configuration</span><h3>{coding_snapshot['benchmark']} · {coding_snapshot['configuration']}</h3><span class="benchmark-meta">Run {coding_snapshot['run_date']} · {coding_snapshot['trials']} trials · exact agent/model/effort shown</span></div><div class="review-benchmark-score">{coding_snapshot['score']}</div></div>
<p>{coding_snapshot['note']} Reward-hack disqualifications: {coding_snapshot['reward_hack_disqualification']}. <a href="{source['url']}" target="_blank" rel="external noopener">Source [{source['id']}] ↗</a></p>
</div>'''
    unavailable = next((x for x in data.get('benchmark_unavailable', []) if x['tool_slug'] == slug), None)
    if unavailable:
        links = ' · '.join(
            f'<a href="{sources[i]["url"]}" target="_blank" rel="external noopener">Evaluation framework [{i}] ↗</a>'
            for i in unavailable.get('method_source_ids', []) if i in sources
        )
        return f'''<div class="review-benchmark"><span class="evidence-label">Benchmark unavailable</span><h3>No trustworthy comparable product score</h3><p>{unavailable['reason']} We therefore do not publish a numeric benchmark for this product.</p><p>{links} · <a href="../../benchmarks/">See benchmark policy →</a></p></div>'''
    source_ids = data.get('coverage', {}).get(category, [])
    if not source_ids:
        return ''
    links = ' · '.join(
        f'<a href="{sources[i]["url"]}" target="_blank" rel="external noopener">{sources[i]["name"]} [{i}] ↗</a>'
        for i in source_ids if i in sources
    )
    arena_definition = "Arena Text is a human-preference leaderboard from anonymous pairwise battles. Its rank is the model's position; its rating is the statistical preference score; and any ± value is a confidence interval, not a guarantee of quality. " if 1 in source_ids else "Benchmark numbers are evidence for a specific task and configuration, not a universal product score. "
    return f'''<div class="review-benchmark"><span class="evidence-label">Relevant benchmark coverage</span><h3>Use category-specific evidence</h3><p>{links}</p><p>{arena_definition}<a href="../../benchmarks/">See benchmark policy →</a></p></div>'''


def generate_review_page(root: Path, tool: dict, tools: list, today: str) -> None:
    slug = tool['slug']
    name = tool.get('name', '')
    rating = tool.get('rating', 4)
    official = tool.get('official', '')
    summary = tool.get('summary', '')
    category = tool.get('category', '')
    source_record = _source_record(root, slug)
    official_source_html = _official_source_html(source_record)
    benchmark_html = _benchmark_html(root, slug, category)

    same_cat = [t for t in tools if t['slug'] != slug and category in t.get('category', '')]
    others = [t for t in tools if t['slug'] != slug and t not in same_cat]
    related = (same_cat + others)[:3]

    comp_dir = root / 'comparisons'
    comp_links = []
    if comp_dir.exists():
        name_key = name.lower().replace(' ', '-')
        for c in sorted(comp_dir.glob('*.html')):
            parts = re.split('-vs-', c.stem)
            if any(p == slug or p == name_key or p in name_key for p in parts):
                comp_links.append((c.name, c.stem.replace('-', ' ').title()))
    comp_links = comp_links[:5]

    # Find related articles (worth-it guides, deep comparisons, audience guides)
    article_links = []
    articles_dir = root / 'articles'
    if articles_dir.exists():
        name_key = name.lower().replace(' ', '-')
        for a in sorted(articles_dir.glob('*.html')):
            a_html = a.read_text()
            if f'/tools/{slug}/' in a_html or f'/{slug}' in a_html:
                title_match = re.search(r'<title>(.*?)</title>', a_html)
                title = title_match.group(1).replace(' | AIToolsEssentials', '') if title_match else a.stem.replace('-', ' ').title()
                article_links.append((a.name, title))
    article_links = article_links[:5]

    related_html = ''
    for r in related:
        related_html += (f'<li><a href="../{r["slug"]}/">{r["name"]}</a>'
                         f'<span style="color:#6e6e73;font-size:13px"> · {r.get("category","")}</span></li>\n')

    comp_html = ''
    for fname, label in comp_links:
        comp_html += f'<a class="text-link" href="../../comparisons/{fname}">{label}</a><br>\n'
    if not comp_html:
        comp_html = '<a class="text-link" href="../../comparisons/best-ai-tools.html">All AI tool comparisons</a>\n'

    article_aside_html = ''
    if article_links:
        items = ''.join(f'<li><a href="../../articles/{fname}">{title[:80]}</a></li>' for fname, title in article_links)
        article_aside_html = f'<div class="score-card"><span>Guides &amp; deep dives</span><ul style="margin:0;padding-left:0;list-style:none;display:grid;gap:10px">{items}</ul></div>'

    if source_record:
        price_html = official_source_html
    else:
        price_rows = _price_rows(tool)
        price_html = '<table class="price-table"><tbody>\n'
        for k, v in price_rows:
            price_html += f'<tr><th>{k}</th><td>{v}</td></tr>\n'
        price_html += '</tbody></table>\n'

    who_for = _who_for(tool)
    score_percent = max(0, min(100, rating / 5 * 100))

    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Review",
        "itemReviewed": {"@type": "SoftwareApplication", "name": name,
                          "applicationCategory": category, "url": official},
        "reviewRating": {"@type": "Rating", "ratingValue": str(rating), "bestRating": "5"},
        "reviewBody": summary,
        "dateModified": today,
        "positiveNotes": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": note}
            for i, note in enumerate(tool.get('pros', []))
        ]},
        "negativeNotes": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": note}
            for i, note in enumerate(tool.get('cons', []))
        ]},
        "author": {"@type": "Organization", "name": "AIToolsEssentials"},
        "publisher": {"@type": "Organization", "name": "AIToolsEssentials"},
        "url": f"{DOMAIN}/tools/{slug}/"
    })

    features_html = ''.join(f'<li>{f}</li>\n' for f in tool.get('key_features', []))
    trial_checklist = tool.get('trial_checklist', '')
    best_plan = tool.get('best_plan', '')
    faq = tool.get('faq', [])
    faq_html = ''
    for q, a in faq:
        faq_html += f'<details><summary>{q}</summary><p>{a}</p></details>\n'

    # FAQPage JSON-LD schema for rich results
    faq_schema = ''
    if faq:
        faq_entities = []
        for q, a in faq:
            import html as _html
            faq_entities.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": _html.unescape(re.sub(r'<[^>]+>', '', a))
                }
            })
        faq_schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        })
    same_cat_n = len([x for x in tools if x['slug'] != slug and category in x.get('category', '')])
    compare_names = ', '.join(r['name'] for r in related[:3])
    compare_para = (
        f"Within {category.lower()}, {name} goes up against {compare_names}"
        f"{f' and {same_cat_n - 3} others' if same_cat_n > 3 else ''}. "
        f"Its edge is {tool.get('pros', ['its core workflow'])[0].lower().rstrip('.')}. "
        f"Weigh that against the cons above — especially: {tool.get('cons', ['pricing'])[0].lower().rstrip('.')} — "
        f"then check our side-by-side comparisons for task-level results before you commit."
    )

    best_plan_html = ''
    if best_plan:
        best_plan_html = f'<div class="best-plan-card"><span>Our recommendation</span><strong>{best_plan}</strong></div>\n'
    buying_decision_html = (
        f'<div class="decision-grid">'
        f'<div><strong>Choose {name} when</strong><p>{tool.get("best_for", "its core workflow")} is the repeated job you need to improve.</p></div>'
        f'<div><strong>Compare first when</strong><p>{tool.get("cons", ["The trade-offs affect your workflow"])[0]}.</p></div>'
        f'<div><strong>Before paying</strong><p>Run the trial checklist above and verify the current plan limit on the official pricing page.</p></div>'
        f'</div>'
    )

    pro1 = tool.get('pros', ['It delivers on its core promise'])[0]
    con1 = tool.get('cons', ['Costs can grow with usage'])[0].lower().rstrip('.')

    automation_decoder_categories = {'Automation', 'Browser Automation', 'Productivity', 'AI Agents'}
    automation_decoder_block = ''
    if category in automation_decoder_categories:
        automation_decoder_block = f'''<section class="score-card"><span>Automation billing decoder</span><h2>Translate this workflow into billing units.</h2><p>Estimate Zapier tasks, Make credits, and n8n executions for the same monthly run volume before comparing plan prices.</p><p><a class="button button-blue" href="/automation-cost-decoder/">Open the free decoder</a></p></section>\n'''

    visit_href = official
    visit_rel = 'sponsored noopener nofollow'
    visit_target = ' target="_blank"'
    visit_label = f'Visit {name}'
    visit_note = 'Affiliate link — supports editorial maintenance at no cost to you.'
    visit_offer = ''
    visit_fineprint = ''
    try:
        prog = approved_programs(root).get(slug)
    except Exception:
        prog = None
    if prog:
        visit_href = public_affiliate_href(prog)
        is_internal = visit_href.startswith('/')
        visit_rel = 'sponsored nofollow' if is_internal else 'sponsored noopener nofollow'
        visit_target = '' if is_internal else ' target="_blank"'
        offer = prog.get('offer_copy') or (NOUS_OFFER if slug == 'hermes-agent' else '')
        if offer:
            visit_label = prog.get('cta_label') or 'Claim the $15 first-month referral'
            visit_offer = f'<p class="affiliate-inline">{offer}</p>'
            visit_note = 'Affiliate / referral link — labeled because this is a partner offer.'
            visit_fineprint = '<p class="pricing-fineprint">Affiliate / referral link — we may earn a commission at no cost to you. See our <a href="../../legal/affiliate-disclosure.html">disclosure</a>.</p>'
        else:
            visit_note = 'Affiliate link — supports editorial maintenance at no cost to you.'
            visit_fineprint = '<p class="pricing-fineprint">Affiliate link — we may earn a commission at no cost to you. See our <a href="../../legal/affiliate-disclosure.html">disclosure</a>.</p>'

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{summary}">
<title>{name}: AI Tool Review — AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/tools/{slug}/">
<link rel="stylesheet" href="../css/styles.css">
<script type="application/ld+json">{schema}</script>
{f'<script type="application/ld+json">{faq_schema}</script>' if faq_schema else ''}
</head>
<body>
<header class="global-nav">
<a class="brand" href="../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>
<nav class="nav-links">
<a href="../tools/index.html">Tools</a>
<a href="../../fit-interview/">Fit interview</a>
<a href="../../confidence-check/">Confidence check</a>
<a href="../comparisons/best-ai-tools.html">Best AI tools</a>
<a href="../categories/index.html">Categories</a>
<a href="../articles/index.html">Guides</a>
</nav>
<a class="nav-cta" href="../legal/affiliate-disclosure.html">Disclosure</a>
</header>

<section class="review-hero scene scene-light">
<p class="kicker light">{category}</p>
<h1>{name} review</h1>
<p>{summary}</p>
<p class="last-updated">Editorial review · Updated {today} · <a href="../../legal/testing-protocol.html">Hands-on result not yet published</a></p>
</section>

<div class="review-layout">
<article class="review-content">
<h2>Overview</h2>
<p>{summary}</p>

<h2>Key features</h2>
<ul>
{features_html}</ul>

<h2>Trial checklist</h2>
<p>{trial_checklist}</p>
{benchmark_html}

<h2>Pricing</h2>
{price_html}
<p class="affiliate-inline">Pricing changes often — verify current plans on the official site before buying. Dated snapshots: <a href="../../pricing-watch/">Pricing Watch</a>.</p>

<h2>Use cases</h2>
<ul>
'''
    for u in tool.get('use_cases', []):
        html += f'<li>{u}</li>\n'
    html += '</ul>\n<h2>Pros</h2>\n<ul>\n'
    for pr in tool.get('pros', []):
        html += f'<li>{pr}</li>\n'
    html += '</ul>\n<h2>Cons</h2>\n<ul>\n'
    for co in tool.get('cons', []):
        html += f'<li>{co}</li>\n'

    html += f'''</ul>
<h2>Who {name} is for</h2>
<p>{who_for}</p>

<h2>Buying decision</h2>
{buying_decision_html}

<h2>Verdict</h2>
<p><strong>Bottom line:</strong> {name} has an AIToolsEssentials editorial score of {rating}/5. {pro1}. The main trade-off to weigh: {con1}.</p>
<p>Test it against one real task from your workflow this week — that tells you more than any review.</p>
<h2>How {name} compares</h2>
<p>{compare_para}</p>
<h2>How we evaluated</h2>
<p>The AIToolsEssentials rating is an editorial score—not an external benchmark. It summarizes job fit, likely output quality, ease of adoption, and operational cost using published product information, benchmark context where the exact model is identifiable, and the repeatable trial checklist above. Benchmarks never determine the final product rating by themselves. See our <a href="../../methodology/">editorial methodology</a>, <a href="../../evidence/">evidence ledger</a>, and <a href="../../benchmarks/">benchmark evidence policy</a>.</p>
{best_plan_html}<h2>Frequently asked questions</h2>
<div class="faq-list">
{faq_html}</div>
</article>

<aside class="review-aside">
<div class="score-card">
<span>AIToolsEssentials editorial score</span>
<strong>{rating}<small style="font-size:20px;color:#6e6e73">/5</small></strong>
<div class="score-meter" aria-label="Editorial score {rating} out of 5"><i style="width:{score_percent}%"></i></div>
<span>Evidence: editorial assessment + sourced benchmarks where the exact model is identifiable.</span>
<a class="button button-blue small" style="margin-top:8px" href="{visit_href}" rel="{visit_rel}"{visit_target}>{visit_label}</a>{visit_fineprint}
{visit_offer}<span>{visit_note}</span>
</div>
<div class="score-card">
<span>Related tools</span>
<ul style="margin:0;padding-left:0;list-style:none;display:grid;gap:10px">
{related_html}</ul>
</div>
<div class="score-card">
<span>Comparisons</span>
{comp_html}
</div>
{article_aside_html}
</aside>
</div>

<section class="newsletter-cta"><div class="cta-grid"><div class="cta-content"><h3>Choose with evidence, not hype.</h3><p>Use the free scorecard for your own trial, then check the benchmark hub for versioned external evidence.</p><div class="cta-actions"><a class="cta-button" href="../../downloads/ai-tool-evaluation-scorecard.html">Download the free scorecard</a><a class="cta-secondary" href="../../benchmarks/">Open benchmarks</a></div></div><div class="cta-actions" style="margin-top:12px"><a class="cta-button" href="../../newsletter/">Read Keep/Cut Weekly</a><a class="cta-secondary" href="../../premium/">Premium research membership</a><a class="cta-secondary" href="../../press/">Press / cite us</a></div></div></section>

{automation_decoder_block}
</main>
<footer class="footer">
<span>© 2026 AIToolsEssentials</span>
<a href="../advertise/index.html" rel="nofollow">Advertise</a>
<a href="../submit-tool.html" rel="nofollow">Submit a tool</a>
<a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
<a href="mailto:{EMAIL}">Contact</a>
</footer>
<script src="../js/site.js" defer></script>
<script src="../js/analytics.js" defer></script>
</body>
</html>'''

    out = root / 'tools' / slug / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return out


def generate_all(root: Path, tools: list, today: str) -> int:
    n = 0
    for tool in tools:
        generate_review_page(root, tool, tools, today)
        print(f'Generated review: {tool["slug"]}')
        n += 1
    return n


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    from datetime import datetime
    tools = json.loads((root / 'data/tools.json').read_text())
    generate_all(root, tools, datetime.today().strftime('%Y-%m-%d'))
