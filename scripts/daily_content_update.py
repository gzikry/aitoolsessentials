#!/usr/bin/env python3
"""Daily content maintenance for AIToolsEssentials.

Runs once per day to:
- Regenerate tool review pages from tools.json
- Regenerate category pages
- Regenerate sitemap.xml
- Write a content brief to content_briefs/YYYY-MM-DD-daily-content-brief.md
"""
from pathlib import Path
from datetime import datetime
import json
import re

root = Path(__file__).resolve().parents[1]
today = datetime.today().strftime('%Y-%m-%d')
brief_file = root / 'content_briefs' / f'{today}-daily-content-brief.md'
brief_file.parent.mkdir(exist_ok=True)

# Load tools and benchmark evidence status
tools = json.loads((root / 'data/tools.json').read_text())
benchmark_data = json.loads((root / 'data/benchmarks.json').read_text())
tool_source_data = json.loads((root / 'data/tool_sources.json').read_text())
benchmark_age = (datetime.today().date() - datetime.fromisoformat(benchmark_data['snapshot_date']).date()).days
tool_source_age = (datetime.today().date() - datetime.fromisoformat(tool_source_data['checked_at']).date()).days
print(f'Loaded {len(tools)} tools')


def _sitemap_priority_changefreq(rel_path: str) -> tuple[str, str]:
    """Return (priority, changefreq) for a sitemap URL based on page type."""
    if rel_path in ('/', 'index.html'):
        return '1.0', 'daily'
    if rel_path.startswith('tools/') and rel_path != 'tools/index.html':
        return '0.9', 'weekly'
    if rel_path.startswith('comparisons/') and rel_path != 'comparisons/index.html':
        return '0.9', 'weekly'
    if rel_path.startswith('categories/') and rel_path != 'categories/index.html':
        return '0.8', 'weekly'
    if rel_path.startswith('articles/') and rel_path != 'articles/index.html':
        return '0.7', 'weekly'
    if rel_path.endswith('index.html'):
        return '0.8', 'weekly'
    return '0.5', 'monthly'


def refresh_sitemap(root: Path) -> list[str]:
    sitemap_urls = []
    for p in sorted(root.rglob('*.html')):
        if '.hermes' in p.parts:
            continue
        rel = p.relative_to(root)
        html_text = p.read_text()
        # Exclude internal, error, checkout-return, redirect, and noindex pages.
        if 'admin' in rel.parts or p.name == '404.html' or 'name="robots" content="noindex' in html_text:
            continue
        if p.name == 'index.html':
            url = f'/{rel.parent}/'
        else:
            url = f'/{rel}'
        sitemap_urls.append(url)

    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'''
    for url in sitemap_urls:
        priority, changefreq = _sitemap_priority_changefreq(url.lstrip('/'))
        sitemap += f'  <url><loc>https://aitoolsessentials.com{url}</loc><lastmod>{today}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>\n'
    sitemap += '</urlset>\n'
    (root / 'sitemap.xml').write_text(sitemap)
    return sitemap_urls


from generate_fit_interview import generate as generate_fit_interview
generate_fit_interview(root, today)
print('Generated AI Tool Fit Interview')

from generate_confidence_check import generate as generate_confidence_check
generate_confidence_check(root, today)
print('Generated decision confidence check')

from generate_methodology import generate as generate_methodology
generate_methodology(root, today)
print('Generated editorial methodology page')

from generate_evidence_ledger import generate as generate_evidence_ledger
generate_evidence_ledger(root, today)
print('Generated public evidence ledger')

# Generate enriched tool review pages
from generate_reviews import generate_all
generate_all(root, tools, today)

# Generate polished category buyer guides
from generate_categories import generate_all as generate_categories_all
generate_categories_all(root, tools, today)

# Generate benchmark evidence hub
from generate_benchmarks import generate as generate_benchmarks_page
generate_benchmarks_page(root)
print('Generated benchmark evidence hub')

# Generate honest community shortlist (never fabricated votes/traffic)
from generate_community import generate as generate_community_page
generate_community_page(root, tools, today)
print('Generated community shortlist')

# Add official-source and benchmark context to major comparison pages.
from enhance_comparisons import generate as enhance_comparison_pages
enhance_comparison_pages(root)

from enhance_guides import generate as enhance_buyer_guides
enhance_buyer_guides(root)

from generate_new_comparisons import generate as generate_new_comparison_pages
from generate_static_comparisons import generate_all as generate_static_comparisons
from generate_comparison_hub import generate as generate_comparison_hub
generate_new_comparison_pages(root)
print('Generated static comparisons:', generate_static_comparisons(root))
generate_comparison_hub(root)

from generate_audience_guides import generate as generate_audience_guide_pages
generate_audience_guide_pages(root)

from enhance_faq_schema import generate as enhance_faq_schema
enhance_faq_schema(root)

from generate_faq_articles import generate as generate_faq_articles
generate_faq_articles(root)

from generate_learn_hub import generate as generate_learn_hub
generate_learn_hub(root)
from generate_growth_hubs import generate as generate_growth_hubs
generate_growth_hubs(root)

from generate_article_hub import generate as generate_article_hub
generate_article_hub(root)

from generate_deep_comparisons import generate as generate_deep_comparisons, cross_link_comparisons as cross_link_deep_comparisons
generate_deep_comparisons(root)
cross_link_deep_comparisons(root)

from generate_worth_it_articles import generate as generate_worth_it_articles
generate_worth_it_articles(root)
generate_article_hub(root)
print('Generated deep comparison editorials, worth-it articles, and refreshed article hub')

from generate_viral_growth import generate as generate_viral_growth
generate_viral_growth(root, tools, today)
print('Generated viral growth utilities')

from generate_conversion_growth import generate as generate_conversion_growth
generate_conversion_growth(root, tools, today)
print('Generated conversion growth utilities')

from generate_workflow_pages import generate as generate_workflow_pages
print('Generated workflow SEO pages:', generate_workflow_pages(root))

from generate_knowledge_growth import generate as generate_knowledge_growth
generate_knowledge_growth(root, tools, today)
print('Generated knowledge growth utilities')

from generate_resource_library import generate as generate_resource_library
generate_resource_library(root, tools, today)
print('Generated resource library')

from generate_premium_membership import generate as generate_premium_membership
generate_premium_membership(root, tools, today)
print('Generated premium membership pages and Whop pack')

from generate_decision_brief import generate as generate_decision_brief
generate_decision_brief(root, tools, today)
print('Generated decision brief generator')

from generate_switch_guides import generate as generate_switch_guides
generate_switch_guides(root, tools, today)
print('Generated switch-from migration guides')

from generate_pricing_watch import generate as generate_pricing_watch
generate_pricing_watch(root, tools, today)
print('Generated pricing watch page')

from generate_pricing_research import generate as generate_pricing_research
generate_pricing_research(root, tools, today)
print('Generated current pricing research')

from generate_automation_cost_decoder import generate as generate_automation_cost_decoder
generate_automation_cost_decoder(root, tools, today)
print('Generated automation billing decoder')

from generate_change_radar import generate as generate_change_radar
print('Generated change radar:', generate_change_radar(root))

from generate_monthly_digest import generate as generate_monthly_digest
print('Generated monthly digests:', generate_monthly_digest(root))

from generate_subscribe import generate as generate_subscribe
print('Generated subscribe page:', generate_subscribe(root))

from generate_weekly_newsletter import generate as generate_weekly_newsletter
print('Generated weekly newsletter:', generate_weekly_newsletter(root))

from generate_how_tos import generate as generate_how_tos
print('Generated how-to library:', generate_how_tos(root))

from generate_hardware import generate as generate_hardware
print('Generated hardware guide:', generate_hardware(root))

from generate_local_ai_planner import generate as generate_local_ai_planner
generate_local_ai_planner(root)
print('Generated local AI planner')

from generate_bestfor_and_report import generate_best_for, generate_pricing_report
generate_best_for(root)
generate_pricing_report(root, today)
print('Generated best-for hub and pricing report')

from generate_verified_deals import generate as generate_verified_deals
generate_verified_deals(root)
print('Generated verified deals section')


from generate_site_discovery import generate as generate_site_discovery
generate_site_discovery(root, tools, today)
print('Generated site discovery utilities')

from generate_affiliate_tracker import generate as generate_affiliate_tracker
generate_affiliate_tracker(root)
print('Generated verified affiliate tracker')

from generate_press import generate as generate_press
generate_press(root)
print('Generated press / cite-us page')

# Generate sitemap
sitemap_urls = refresh_sitemap(root)
print(f'Generated sitemap with {len(sitemap_urls)} URLs')

# Write daily brief
brief = f'''# Daily Content Brief — {today}

## Summary
- Tools reviewed: {len(tools)}
- Category buyer guides: {len(set(t['category'] for t in tools))}
- Total HTML pages: {len(sitemap_urls)}
- Sitemap URLs: {len(sitemap_urls)}
- Benchmark snapshot: {benchmark_data['snapshot_date']} ({benchmark_age} days old)
- Benchmark refresh due: {'YES' if benchmark_age > benchmark_data.get('policy', {}).get('staleness_days', 30) else 'No'}
- Official tool sources: {tool_source_data['checked_at']} ({tool_source_age} days old)
- Official source refresh due: {'YES' if tool_source_age > 30 else 'No'}

## Revenue Status
- Affiliate programs: Check `data/affiliate_programs.json` for application status.
- Sponsored placements: Check `data/sponsors.json` for inventory.

## Actions
- Refresh `data/benchmarks.json` from its source registry when the snapshot is over 30 days old.
- Do not copy a benchmark score unless the exact model/version and harness are known.
- Review tools with `program_status: not_applied` in `data/affiliate_programs.json`.
- Submit affiliate applications for high-priority tools.
- Draft sponsored placement offers for partners.

## Notes
- All tool review pages regenerated from `data/tools.json`.
- All category buyer guides regenerated.
- Sitemap updated.
'''
brief_file.write_text(brief)
print(f'Wrote daily brief: {brief_file}')

print('Daily content maintenance complete:', today)

from generate_media_kit import generate as generate_media_kit
generate_media_kit(root)

# Run post-generation cleanup (idempotent: fixes paths, structure, share rows, emails)
import subprocess
r = subprocess.run(['python3', 'scripts/cleanup_html.py'], capture_output=True, text=True, cwd=str(root))
print(r.stdout.strip() or r.stderr.strip())

# Inject/enhance Article schema on all article pages (idempotent)
from inject_article_schema import enhance_article_schema
enhance_article_schema(root)

def ping_indexnow(root):
    """Ping IndexNow with the full sitemap URL set after each successful deploy."""
    import json as _json, subprocess
    try:
        key = _json.loads((root / 'data' / 'integrations.json').read_text())['bing']['indexnow_key']
        sm = (root / 'sitemap.xml').read_text()
        urls = [u.strip() for u in __import__('re').findall(r'<loc>(https://aitoolsessentials\.com[^<]+)</loc>', sm)]
        if not urls:
            return
        body = _json.dumps({"host": "aitoolsessentials.com", "key": key, "urlList": urls[:10000]})
        r = subprocess.run(['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code}',
                            '-X', 'POST', 'https://api.indexnow.org/indexnow',
                            '-H', 'Content-Type: application/json; charset=utf-8', '-d', body],
                           capture_output=True, text=True, timeout=60)
        print(f'IndexNow ping: {r.stdout} ({len(urls)} URLs)')
    except Exception as e:
        print(f'IndexNow ping skipped: {e}')

# Auto-ping IndexNow with the fresh sitemap so search engines index new pages same-day
ping_indexnow(root)

subprocess.run(['python3', str(root / 'scripts' / 'enhance_structured_data.py')], check=False, capture_output=True, text=True)
# Apply approved affiliate tracking URLs last so regeneration cannot wipe them
import subprocess as _sp
_r=_sp.run(['python3','scripts/wire_affiliate_links.py'],capture_output=True,text=True,cwd=str(root))
print(_r.stdout.strip() or _r.stderr.strip())

# Final viral review modules must run after cleanup/affiliate post-passes so they persist.
from generate_viral_growth import inject_review_stack_modules as _inject_review_stack_modules
_inject_review_stack_modules(root, tools)
print('Injected review-page stack modules')

from generate_conversion_growth import postprocess as _conversion_postprocess
_conversion_postprocess(root, tools)
print('Injected conversion growth post-process modules')

from generate_site_discovery import postprocess as _site_discovery_postprocess
_site_discovery_postprocess(root, tools, today)
print('Injected site discovery head/status modules')

from generate_knowledge_growth import postprocess as _knowledge_postprocess
_knowledge_postprocess(root, tools, today)
print('Injected knowledge schema modules')

from generate_decision_brief import postprocess as _decision_brief_postprocess
_decision_brief_postprocess(root, tools, today)
print('Injected decision brief entry links')


from generate_premium_membership import postprocess as _premium_postprocess
_premium_postprocess(root, tools, today)
print('Injected premium conversion modules')

from generate_switch_guides import postprocess as _switch_postprocess
_switch_postprocess(root, tools, today)
print('Re-injected switch guide modules')

from generate_pricing_watch import postprocess as _pricing_watch_postprocess
_pricing_watch_postprocess(root, tools, today)
print('Re-injected pricing watch links')

from generate_model_lineups import generate as generate_model_lineups
generate_model_lineups(root)
print('Injected model lineup panels')

from generate_lineup_hub import generate as generate_lineup_hub
print('Generated model lineups hub:', generate_lineup_hub(root))

from generate_seo_monetization_sweep import postprocess as _sweep_postprocess
print('SEO/monetization sweep:', _sweep_postprocess(root, tools, today))

from generate_evidence_ledger import postprocess_reviews as _evidence_review_postprocess
print('Injected exact evidence links:', _evidence_review_postprocess(root))

from generate_exit_plan import postprocess as _exit_plan_postprocess
print('Injected exit plans:', _exit_plan_postprocess(root, tools))

from generate_test_protocol import postprocess as _test_protocol_postprocess
print('Injected test protocols:', _test_protocol_postprocess(root, tools))

from generate_bestfor_and_report import postprocess_refresh as _bestfor_refresh
print('Best-for deals strip refreshed:', _bestfor_refresh(root))

# Keep inventory claims accurate after adding or removing tools. Historical pricing
# research retains its original 40-tool snapshot language; current-directory copy is dynamic.
_current_count = len(tools)
_inventory_replacements = {
    '39 AI tools': f'{_current_count} AI tools',
    '39 AI tools reviewed': f'{_current_count} AI tools reviewed',
    '40 tools. Pricing verified': f'{_current_count} tools. Pricing verified',
    '45 AI tools': f'{_current_count} AI tools',
    '45 AI tools organized by real workflows': f'{_current_count} AI tools organized by real workflows',
    'for all 40 tools': 'for the 40-tool pricing snapshot',
    'across all 40 tools': 'across the 40-tool pricing snapshot',
    'across 40 tools': 'across the 40-tool pricing snapshot',
    "can't personally test all 40 tools": f"can't personally test all {_current_count} tools",
    'verified snapshots for the 40-tool pricing snapshot': f'verified snapshots for {_current_count} tools',
}
for _path in root.rglob('*'):
    if not _path.is_file() or _path.suffix not in {'.html', '.txt', '.md', '.xml'}:
        continue
    if '.git' in _path.parts or '.hermes' in _path.parts:
        continue
    try:
        _text = _path.read_text()
        _new = _text
        for _old, _replacement in _inventory_replacements.items():
            _new = _new.replace(_old, _replacement)
        if _path.suffix == '.html':
            _new = re.sub(
                r'href="(?:/|(?:\.\./)*)index\.html([#?][^"]*)?"',
                lambda m: 'href="/' + (m.group(1) or '') + '"',
                _new,
            )
        if _new != _text:
            _path.write_text(_new)
    except (UnicodeDecodeError, OSError):
        continue
print(f'Refreshed inventory copy for {_current_count} tools')

# Final metadata pass: downstream generators can rewrite head sections, so restore
# structured data, discovery links, and knowledge schema after every other pass.
subprocess.run(['python3', str(root / 'scripts' / 'enhance_structured_data.py')], check=True)
_site_discovery_postprocess(root, tools, today)
_knowledge_postprocess(root, tools, today)

# Final postprocessors can rewrite status and discovery pages after the cleanup pass.
# Normalize homepage links once more so analytics and crawl signals stay on `/`.
for _html_path in root.rglob('*.html'):
    _html = _html_path.read_text()
    _normalized = re.sub(
        r'href="(?:/|(?:\.\./)*)index\.html([#?][^"]*)?"',
        lambda m: 'href="/' + (m.group(1) or '') + '"',
        _html,
    )
    if _normalized != _html:
        _html_path.write_text(_normalized)

_expected_count = len(tools)
_metadata_targets = {
    root / 'change-radar/index.html': ('<article class="radar-row"', 'radar rows'),
    root / 'confidence-check/index.html': ('<article class="confidence-card"', 'confidence cards'),
    root / 'evidence/index.html': ('<tr id="evidence-', 'evidence rows'),
}
for _page, (_needle, _label) in _metadata_targets.items():
    _html = _page.read_text()
    _actual = _html.count(_needle)
    if _actual != _expected_count:
        raise RuntimeError(f'{_page}: expected {_expected_count} {_label}, found {_actual}')
    for _start, _end in [('AIT STRUCTURED DATA START', 'AIT STRUCTURED DATA END'), ('AIT KNOWLEDGE SCHEMA START', 'AIT KNOWLEDGE SCHEMA END')]:
        if _html.count(_start) != 1 or _html.count(_end) != 1:
            raise RuntimeError(f'{_page}: metadata marker pair is not exactly once')
    if _html.count('AIT DISCOVERY LINKS') != 1:
        raise RuntimeError(f'{_page}: discovery metadata marker is not exactly once')
if f'Search {_expected_count} tools' not in (root / 'confidence-check/index.html').read_text():
    raise RuntimeError('confidence-check: current tool-count search prompt missing')
print(f'Verified dynamic metadata coverage for {_expected_count} tools')
_sitemap_urls_final = refresh_sitemap(root)
print(f'Refreshed final sitemap with {len(_sitemap_urls_final)} URLs')
print('Re-injected final metadata layers')
