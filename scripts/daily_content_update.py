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

root = Path('/Users/georgezikry/aitoolessentials/site')
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
generate_new_comparison_pages(root)

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

from generate_viral_growth import generate as generate_viral_growth
generate_viral_growth(root, tools, today)
print('Generated viral growth utilities')

from generate_conversion_growth import generate as generate_conversion_growth
generate_conversion_growth(root, tools, today)
print('Generated conversion growth utilities')

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

from generate_verified_deals import generate as generate_verified_deals
generate_verified_deals(root)
print('Generated verified deals section')


from generate_site_discovery import generate as generate_site_discovery
generate_site_discovery(root, tools, today)
print('Generated site discovery utilities')

from generate_affiliate_tracker import generate as generate_affiliate_tracker
generate_affiliate_tracker(root)
print('Generated verified affiliate tracker')

# Generate sitemap
sitemap_urls = []
for p in sorted(root.rglob('*.html')):
    if '.hermes' in p.parts:
        continue
    rel = p.relative_to(root)
    html_text = p.read_text()
    # Exclude internal, error, checkout-return, redirect, and noindex pages.
    if 'admin' in str(rel) or p.name == '404.html' or 'name="robots" content="noindex' in html_text:
        continue
    if p.name == 'index.html':
        url = f'/{rel.parent}/'
    else:
        url = f'/{rel}'
    # Exclude admin pages from sitemap
    if 'admin' in str(rel):
        continue
    sitemap_urls.append(url)

sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
for url in sitemap_urls:
    sitemap += f'  <url><loc>https://aitoolsessentials.com{url}</loc></url>\n'
sitemap += '</urlset>\n'
(root / 'sitemap.xml').write_text(sitemap)
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
generate_media_kit(root)
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

from generate_seo_monetization_sweep import postprocess as _sweep_postprocess
print('SEO/monetization sweep:', _sweep_postprocess(root, tools, today))
