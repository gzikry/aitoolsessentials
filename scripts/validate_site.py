#!/usr/bin/env python3
"""Validate AIToolsEssentials static site quality gates."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urldefrag
import json
import re
import sys
from datetime import date

ROOT = Path(__file__).resolve().parents[1]

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()
        self.outbound_ctas = []
        self.text = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.add(d['id'])
        if tag == 'a' and d.get('href'):
            self.refs.append(('a', d['href']))
            if d['href'].startswith(('http://','https://')):
                self.outbound_ctas.append(d)
        if tag == 'link' and d.get('href'):
            self.refs.append(('link', d['href']))
        if tag == 'script' and d.get('src'):
            self.refs.append(('script', d['src']))
    def handle_data(self, data):
        self.text.append(data)


def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        return f'{path.relative_to(ROOT)} JSON parse failed: {exc}'


def main():
    errors = []
    for rel in ['data/tools.json','data/tool_sources.json','data/test_cases.json','data/affiliate_programs.json','data/sponsors.json','data/revenue_targets.json','data/sponsor_inventory.json','data/benchmarks.json','data/integrations.json','data/pricing_snapshots.json']:
        result = load_json(ROOT / rel)
        if isinstance(result, str):
            errors.append(result)

    tools = json.loads((ROOT/'data/tools.json').read_text())
    tool_slugs = {t['slug'] for t in tools}
    tool_sources = json.loads((ROOT/'data/tool_sources.json').read_text())
    source_records = {x.get('slug'): x for x in tool_sources.get('tools', [])}
    if set(source_records) != tool_slugs:
        errors.append('Official tool-source registry does not match tools.json slugs')
    try:
        source_age = (date.today() - date.fromisoformat(tool_sources['checked_at'])).days
        if source_age > 30:
            errors.append(f'Official tool-source registry is stale: {source_age} days old')
    except Exception as exc:
        errors.append(f'Official tool-source checked date invalid: {exc}')
    for slug, record in source_records.items():
        if not record.get('pricing_checked_date'):
            errors.append(f'Official source record missing checked date: {slug}')
        if not record.get('pricing_summary'):
            errors.append(f'Official source record missing pricing summary: {slug}')
        if not any(record.get(k) for k in ['pricing_url','docs_url','privacy_url','rights_url']):
            errors.append(f'Official source record has no source URLs: {slug}')
    revenue_targets = json.loads((ROOT/'data/revenue_targets.json').read_text())
    affiliate_data = json.loads((ROOT/'data/affiliate_programs.json').read_text())
    affiliate_records = affiliate_data.get('affiliate_programs', [])
    unknown_affiliate_tools = sorted({x.get('tool_slug') for x in affiliate_records} - tool_slugs)
    if unknown_affiliate_tools:
        errors.append(f'Affiliate registry references unknown tools: {unknown_affiliate_tools}')
    try:
        affiliate_age = (date.today() - date.fromisoformat(affiliate_data['checked_at'])).days
        if affiliate_age > 30:
            errors.append(f'Affiliate program registry is stale: {affiliate_age} days old')
    except Exception as exc:
        errors.append(f'Affiliate checked date invalid: {exc}')
    for record in affiliate_records:
        if not record.get('official_program_url'):
            errors.append(f"Affiliate record missing official URL: {record.get('tool_slug')}")
        if record.get('application_status') == 'approved' and not record.get('affiliate_url'):
            errors.append(f"Approved affiliate record missing tracking URL: {record.get('tool_slug')}")
    target_slugs = {r.get('tool_slug') for r in revenue_targets}
    tool_slugs_for_targets = {t['slug'] for t in tools}
    if target_slugs != tool_slugs_for_targets:
        errors.append('Revenue targets do not match tools.json slugs')
    pricing_data = json.loads((ROOT/'data/pricing_snapshots.json').read_text())
    pricing_slugs = set(pricing_data.get('snapshots', {}))
    if pricing_slugs != tool_slugs:
        errors.append('Pricing snapshots do not match tools.json slugs')
    sponsor_inv = json.loads((ROOT/'data/sponsor_inventory.json').read_text())
    if not isinstance(sponsor_inv, dict) or 'placements' not in sponsor_inv or len(sponsor_inv.get('placements', [])) == 0:
        errors.append('Sponsor inventory is empty')
    review_pages = {p.stem for p in (ROOT/'tools').glob('*.html') if p.name != 'index.html'}
    review_pages |= {d.name for d in (ROOT/'tools').iterdir() if d.is_dir() and (d/'index.html').exists()}
    missing_reviews = sorted(tool_slugs - review_pages)
    extra_reviews = sorted(review_pages - tool_slugs)
    if missing_reviews:
        errors.append(f'Missing review pages: {missing_reviews}')
    if extra_reviews:
        errors.append(f'Extra reviews without tool records: {extra_reviews}')

    # Benchmark evidence integrity and review provenance gates.
    benchmark_data = json.loads((ROOT/'data/benchmarks.json').read_text())
    source_ids = {s['id'] for s in benchmark_data.get('sources', [])}
    for row in benchmark_data.get('arena_text_snapshot', []) + benchmark_data.get('coding_agent_snapshot', []):
        if row.get('source_id') not in source_ids:
            errors.append(f"Benchmark row {row.get('model', row.get('configuration'))} has unknown source_id")
        if row.get('tool_slug') not in tool_slugs:
            errors.append(f"Benchmark row references unknown tool: {row.get('tool_slug')}")
    for row in benchmark_data.get('benchmark_unavailable', []):
        if row.get('tool_slug') not in tool_slugs:
            errors.append(f"Benchmark unavailable record references unknown tool: {row.get('tool_slug')}")
        for source_id in row.get('method_source_ids', []):
            if source_id not in source_ids:
                errors.append(f"Benchmark unavailable record {row.get('tool_slug')} has unknown source_id {source_id}")
    try:
        snapshot_age = (date.today() - date.fromisoformat(benchmark_data['snapshot_date'])).days
        if snapshot_age > benchmark_data.get('policy', {}).get('staleness_days', 30):
            errors.append(f'Benchmark snapshot is stale: {snapshot_age} days old')
    except Exception as exc:
        errors.append(f'Benchmark snapshot date invalid: {exc}')
    unsupported_claim_patterns = ['our test tasks', 'in testing', 'we tested', 'blind tests', 'our testers']
    fabricated_growth_patterns = ['2,847 submissions', '156,234 upvotes', '892,415 clicks', '10k+ weekly visitors', '20k+ weekly visitors', 'guaranteed #1', 'guaranteed rankings']
    for tool in tools:
        review = ROOT/'tools'/tool['slug']/'index.html'
        if review.exists():
            text = review.read_text().lower()
            for phrase in unsupported_claim_patterns:
                if phrase in text:
                    errors.append(f"{review.relative_to(ROOT)} contains unsupported testing claim: {phrase}")
            for required in ['Trial checklist', 'How we evaluated', 'editorial score', 'Official sources checked', 'Hands-on result not yet published']:
                if required.lower() not in text:
                    errors.append(f"{review.relative_to(ROOT)} missing review evidence label: {required}")
    
    # Check for key viral pages
    key_pages = ['leaderboard.html','submit-tool.html','downloads/ai-tool-evaluation-scorecard.html',
                 'legal/privacy.html','legal/terms.html','legal/about.html','legal/corrections.html',
                 'legal/testing-protocol.html','downloads/ai-tool-test-log.csv',
                 'benchmarks/index.html','research/ai-tool-pricing-2026.html',
                 'automation-cost-decoder/index.html']
    missing_keys = [p for p in key_pages if not (ROOT / p).exists()]
    if missing_keys:
        errors.append(f'Missing key pages: {missing_keys}')
    comparison_hub = ROOT/'comparisons/index.html'
    comparison_pages = {
        p.name for p in (ROOT/'comparisons').glob('*.html')
        if p.name != 'index.html'
    }
    if comparison_hub.exists():
        hub_text = comparison_hub.read_text()
        hub_links = set(re.findall(r'href=["\']([^"\']+\.html)', hub_text))
        hub_link_names = {Path(link).name for link in hub_links}
        missing_from_hub = sorted(comparison_pages - hub_link_names)
        if missing_from_hub:
            errors.append(f'Comparison pages missing from comparison hub: {missing_from_hub}')
        expected_comparison_count = f'Showing all {len(comparison_pages)} comparisons.'
        if expected_comparison_count not in hub_text:
            errors.append(f'Comparison hub count is stale; expected {len(comparison_pages)}')
    else:
        errors.append('Missing comparison hub')
    article_hub = ROOT/'articles/index.html'
    article_pages = {
        p.name for p in (ROOT/'articles').glob('*.html')
        if p.name != 'index.html'
    }
    if article_hub.exists():
        article_hub_text = article_hub.read_text()
        article_hub_links = set(re.findall(r'href=["\']([^"\']+\.html)', article_hub_text))
        article_hub_link_names = {Path(link).name for link in article_hub_links}
        missing_articles = sorted(article_pages - article_hub_link_names)
        if missing_articles:
            errors.append(f'Article pages missing from article hub: {missing_articles}')
        expected_article_count = f'Showing all {len(article_pages)} guides.'
        if expected_article_count not in article_hub_text:
            errors.append(f'Article hub count is stale; expected {len(article_pages)}')
    else:
        errors.append('Missing article hub')
    duplicate_home_links = []
    for page in ROOT.rglob('*.html'):
        if re.search(r'href="(?:/|(?:\.\./)*)index\.html(?:[#?][^"]*)?"', page.read_text()):
            duplicate_home_links.append(str(page.relative_to(ROOT)))
    if duplicate_home_links:
        errors.append(f'Pages link to duplicate homepage path /index.html: {duplicate_home_links[:10]}')
    analytics_text = (ROOT/'js/analytics.js').read_text()
    if 'window.plausibleQueue.add(n)' in analytics_text or '(function sendQueue()' in analytics_text:
        errors.append('Analytics pre-fires conversion events without a user click')
    decoder_targets = [
        ROOT/'tools/zapier-ai/index.html', ROOT/'tools/make/index.html', ROOT/'tools/n8n/index.html',
        ROOT/'comparisons/zapier-vs-make-vs-n8n.html', ROOT/'categories/Automation/index.html',
        ROOT/'articles/make-vs-zapier-which-to-pay-for.html', ROOT/'workflows/client-onboarding-automation.html',
    ]
    for target in decoder_targets:
        if target.exists() and target.read_text().count('AIT AUTOMATION DECODER START') != 1:
            errors.append(f'{target.relative_to(ROOT)} missing automation decoder cross-link')
    pricing_research = ROOT/'research/ai-tool-pricing-2026.html'
    if pricing_research.exists():
        pricing_text = pricing_research.read_text()
        expected_title = f'{len(tools)} Tools Tracked'
        if expected_title not in pricing_text:
            errors.append(f'Pricing research inventory claim is stale; expected {expected_title}')
        if pricing_text.count('<tbody>') != 1 or pricing_text.count('<tr>') - 1 != len(tools):
            errors.append('Pricing research table does not match current tool inventory')

    parsers = {}
    for f in ROOT.rglob('*.html'):
        raw_html = f.read_text()
        p = Parser(); p.feed(raw_html); parsers[f.resolve()] = p
        for raw_schema in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', raw_html, flags=re.S | re.I):
            try:
                json.loads(raw_schema)
            except Exception as exc:
                errors.append(f'{f.relative_to(ROOT)} JSON-LD parse failed: {exc}')
        if 'admin' not in f.relative_to(ROOT).parts and '<main' in raw_html and '<footer' in raw_html:
            main_close = raw_html.find('</main>')
            footer_open = raw_html.find('<footer')
            footer_close = raw_html.find('</footer>')
            if not (main_close >= 0 and footer_open > main_close and footer_close > footer_open):
                errors.append(f'{f.relative_to(ROOT)} has malformed main/footer order')
    for f,p in parsers.items():
        page_text = ' '.join(p.text).lower()
        if 'admin' not in f.parts:
            for phrase in fabricated_growth_patterns:
                if phrase in page_text:
                    errors.append(f'{f.relative_to(ROOT)} contains unsupported growth claim: {phrase}')
        if any(part in f.parts for part in ['articles','comparisons','tools']):
            if 'disclosure' not in page_text and 'affiliate' not in page_text:
                errors.append(f'{f.relative_to(ROOT)} missing disclosure language')
        for tag, href in p.refs:
            if href.startswith(('http://','https://','mailto:')):
                continue
            from urllib.parse import unquote
            href_dec = unquote(href)
            url, frag = urldefrag(href_dec)
            # Query strings are valid on static pages (e.g., ?vs=slug1,slug2); strip before resolving.
            if '?' in url:
                url = url.split('?', 1)[0]
            if href.startswith('/'):
                target = ROOT / url.lstrip('/')
            else:
                target = f if not url else (f.parent / url).resolve()
            if target.exists() and target.is_dir():
                target = target / 'index.html'
            if not target.exists():
                errors.append(f'{f.relative_to(ROOT)} missing {tag} {href}')
            elif frag and target.suffix == '.html' and target in parsers and frag not in parsers[target].ids:
                errors.append(f'{f.relative_to(ROOT)} bad fragment {href}')
        for a in p.outbound_ctas:
            if 'admin' in f.parts:
                continue
            href = a.get('href','')
            rel = a.get('rel','')
            # Exclude social sharing links (twitter.com, facebook.com, linkedin.com/share)
            if any(domain in href.lower() for domain in ['twitter.com', 'facebook.com', 'facebook.com/sharer', 'linkedin.com/share']):
                continue
            # Editorial/benchmark citations are non-commercial references.
            if 'external' in rel:
                continue
            if 'sponsored' not in rel or 'nofollow' not in rel:
                errors.append(f'{f.relative_to(ROOT)} outbound link missing sponsored nofollow: {a.get("href")}')

    old_slugs = ('/riverside', '/adobe-podcast', '/categories/Podcast', '/best-ai-tools-for-podcasters')
    for html_path in ROOT.rglob('*.html'):
        rel = html_path.relative_to(ROOT)
        if 'admin' in rel.parts:
            continue
        raw = html_path.read_text()
        if '.html.html' in raw:
            errors.append(f'{rel} still contains doubled .html.html URL')
        canons = re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', raw, flags=re.I)
        canons += re.findall(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', raw, flags=re.I)
        for href in canons:
            if href.endswith('.html.html'):
                errors.append(f'{rel} canonical is doubled: {href}')
        for raw_schema in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', raw, flags=re.S | re.I):
            try:
                schema = json.loads(raw_schema)
            except Exception:
                continue
            schemas = schema if isinstance(schema, list) else [schema]
            for item in schemas:
                if not isinstance(item, dict):
                    continue
                if str(rel).startswith('hardware/') and rel.name != 'index.html' and item.get('@type') == 'Product':
                    if not item.get('image'):
                        errors.append(f'{rel} Product JSON-LD missing image')
                    if 'offers' in item:
                        errors.append(f'{rel} hardware Product schema must not include merchant Offer fields')
                if str(rel) == 'premium/faq.html' and item.get('@type') == 'Product':
                    if not item.get('image'):
                        errors.append('premium/faq.html Product JSON-LD missing image')
                    offer = item.get('offers') or {}
                    if not offer.get('hasMerchantReturnPolicy'):
                        errors.append('premium/faq.html Offer missing hasMerchantReturnPolicy')
                    shipping = offer.get('shippingDetails') or {}
                    if not shipping or not shipping.get('deliveryTime'):
                        errors.append('premium/faq.html Offer missing digital-goods shippingDetails')

    sitemap = ROOT/'sitemap.xml'
    if sitemap.exists():
        html_count = len([
            p for p in ROOT.rglob('*.html')
            if 'admin' not in p.relative_to(ROOT).parts
            and p.name != '404.html'
            and 'name="robots" content="noindex' not in p.read_text()
        ])
        sitemap_text = sitemap.read_text()
        url_count = sitemap_text.count('<url>')
        if html_count != url_count:
            errors.append(f'Sitemap URL count {url_count} != HTML count {html_count}')
        for slug in old_slugs:
            if f'https://aitoolsessentials.com{slug}' in sitemap_text and 'riverside-fm' not in slug:
                errors.append(f'Sitemap still lists retired path {slug}')
        retired_hits = re.findall(r'<loc>(https://aitoolsessentials\.com[^<]*(?:/riverside|/adobe-podcast|/categories/Podcast|/best-ai-tools-for-podcasters)[^<]*)</loc>', sitemap_text)
        retired_hits = [u for u in retired_hits if '/riverside-fm' not in u and '/adobe-enhance-speech' not in u and 'podcast-shows' not in u]
        if retired_hits:
            errors.append(f'Sitemap still lists retired paths: {retired_hits}')
    else:
        errors.append('Missing sitemap.xml')

    if errors:
        print('Validation failed')
        for err in errors:
            print('-', err)
        return 1
    print('Validation passed')
    print(f'Tools: {len(tools)}')
    print(f'HTML pages: {len(list(ROOT.rglob("*.html")))}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
