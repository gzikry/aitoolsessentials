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

# Run post-generation cleanup (idempotent: fixes paths, structure, share rows, emails)
import subprocess
r = subprocess.run(['python3', 'scripts/cleanup_html.py'], capture_output=True, text=True, cwd=str(root))
print(r.stdout.strip() or r.stderr.strip())

def generate_media_kit(root)
ping_indexnow(root):
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
