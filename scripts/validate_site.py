#!/usr/bin/env python3
"""Validate AIToolsEssentials static site quality gates."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urldefrag
import json
import re
import sys
from datetime import date

from enhance_structured_data import is_hands_on_published, valid_rating_value

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


def iter_jsonld_nodes(obj):
    if isinstance(obj, dict):
        yield obj
        for key, value in obj.items():
            if key == '@context':
                continue
            yield from iter_jsonld_nodes(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_jsonld_nodes(item)


def schema_types(node):
    raw = node.get('@type') if isinstance(node, dict) else None
    if isinstance(raw, str):
        return {raw}
    if isinstance(raw, list):
        return {str(x) for x in raw}
    return set()


def author_names(node):
    author = node.get('author')
    authors = author if isinstance(author, list) else [author]
    names = []
    for item in authors:
        if isinstance(item, dict) and item.get('name'):
            names.append(str(item['name']))
        elif isinstance(item, str) and item.strip():
            names.append(item)
    return names


def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        return f'{path.relative_to(ROOT)} JSON parse failed: {exc}'


def main():
    errors = []
    for rel in ['data/tools.json','data/tool_sources.json','data/test_cases.json','data/affiliate_programs.json','data/sponsors.json','data/revenue_targets.json','data/sponsor_inventory.json','data/benchmarks.json','data/integrations.json','data/pricing_snapshots.json','data/stack_audit_rules.json','data/stack_audit_catalog.json']:
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
            rel = review.relative_to(ROOT)
            raw_html = review.read_text()
            snippet_items = []
            has_software_application = False
            for raw_schema in re.findall(
                r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                raw_html,
                flags=re.S | re.I,
            ):
                try:
                    data = json.loads(raw_schema)
                except Exception:
                    continue
                for node in iter_jsonld_nodes(data):
                    types = schema_types(node)
                    if 'SoftwareApplication' in types or 'Product' in types:
                        has_software_application = True
                    if 'Review' in types:
                        snippet_items.append(('Review', node))
                    if 'AggregateRating' in types:
                        snippet_items.append(('AggregateRating', node))
                    if node.get('ratingValue') is not None:
                        try:
                            rating_value = float(node['ratingValue'])
                        except (TypeError, ValueError):
                            errors.append(f'{rel} JSON-LD ratingValue is not numeric: {node.get("ratingValue")}')
                            continue
                        if rating_value <= 0 or rating_value > 5:
                            errors.append(f'{rel} JSON-LD ratingValue out of range: {node.get("ratingValue")}')
            if not has_software_application:
                errors.append(f'{rel} missing SoftwareApplication JSON-LD')
            if not is_hands_on_published(tool):
                for kind, _node in snippet_items:
                    errors.append(
                        f'{rel} emits {kind} JSON-LD without a published hands-on result'
                    )
            if len(snippet_items) > 1:
                kinds = ', '.join(kind for kind, _node in snippet_items)
                errors.append(
                    f'{rel} has {len(snippet_items)} Review snippet items ({kinds}); '
                    'do not combine Review and AggregateRating'
                )
            for kind, node in snippet_items:
                if kind == 'Review':
                    names = author_names(node)
                    if not names:
                        errors.append(f'{rel} Review JSON-LD missing author name')
                    if any('george' in name.lower() for name in names):
                        errors.append(f'{rel} Review JSON-LD must not name a person on public pages')
                    review_rating = node.get('reviewRating') if isinstance(node.get('reviewRating'), dict) else {}
                    if review_rating.get('ratingValue') in (None, '', '0'):
                        errors.append(f'{rel} Review JSON-LD missing valid reviewRating.ratingValue')
                elif kind == 'AggregateRating':
                    if not (node.get('reviewCount') or node.get('ratingCount')):
                        errors.append(f'{rel} AggregateRating JSON-LD missing reviewCount/ratingCount')
                    if valid_rating_value(tool) is None:
                        errors.append(f'{rel} AggregateRating JSON-LD without a valid tool rating')
    
    # Check for key viral pages
    key_pages = ['leaderboard.html','submit-tool.html','downloads/ai-tool-evaluation-scorecard.html',
                 'legal/privacy.html','legal/terms.html','legal/about.html','legal/corrections.html',
                 'legal/testing-protocol.html','downloads/ai-tool-test-log.csv',
                 'benchmarks/index.html','research/ai-tool-pricing-2026.html',
                 'automation-cost-decoder/index.html','stack-audit.html']
    missing_keys = [p for p in key_pages if not (ROOT / p).exists()]
    if missing_keys:
        errors.append(f'Missing key pages: {missing_keys}')
    for rel in ['js/stack-audit.js', 'css/stack-audit.css']:
        if not (ROOT / rel).exists():
            errors.append(f'Missing Stack Audit asset: {rel}')
    catalog_path = ROOT / 'data/stack_audit_catalog.json'
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_text())
        catalog_slugs = {item.get('slug') for item in catalog.get('tools', [])}
        if catalog_slugs != tool_slugs:
            errors.append('Stack Audit catalog slugs do not match tools.json')
        for item in catalog.get('tools', []):
            if item.get('numeric_list_price_usd') not in (None,):
                errors.append(f'Stack Audit catalog invented a numeric price for {item.get("slug")}')
            if '20' == str(item.get('numeric_list_price_usd')) or item.get('numeric_list_price_usd') == 35:
                errors.append(f'Stack Audit catalog reused viral heuristic for {item.get("slug")}')
        page = (ROOT / 'stack-audit.html').read_text() if (ROOT / 'stack-audit.html').exists() else ''
        if 'sa-premium-upsell' not in page:
            errors.append('Stack Audit page missing Premium upsell section')
        if 'keep/cut pack' not in page.lower() and 'written reply' not in page.lower():
            errors.append('Stack Audit page missing Path A keep/cut pack upgrade')
        if '?promo=LAUNCH50' not in page:
            errors.append('Stack Audit upgrade CTA must use the LAUNCH50 checkout')
        if 'You could save' in page:
            errors.append('Stack Audit must not invent savings in the Premium CTA')
        if 'Never changes' not in page and 'never changes' not in page:
            errors.append('Stack Audit page missing affiliate/sponsor editorial policy')
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
        if '</html>' not in raw.lower():
            errors.append(f'{rel} is truncated (missing </html>)')
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

    home_html = (ROOT / 'index.html').read_text()
    subscribe_match = re.search(r'<section[^>]*id="subscribe"[^>]*>.*?</section>', home_html, flags=re.S)
    if not subscribe_match:
        errors.append('Homepage missing #subscribe Keep/Cut Weekly panel')
    else:
        subscribe_block = subscribe_match.group(0)
        if 'whop.com/checkout' in subscribe_block.lower():
            errors.append('Homepage #subscribe must not be the Whop Premium checkout')
        if '/subscribe/' not in subscribe_block:
            errors.append('Homepage #subscribe must link to /subscribe/')
        if 'Beehiiv form' in subscribe_block or re.search(
            r'<a[^>]+href="https?://[^"]*beehiiv\.com/subscribe"', subscribe_block, flags=re.I
        ):
            errors.append('Homepage #subscribe must not add a second Beehiiv form button')
        if len(re.findall(r'<a\b[^>]*\bbutton\b', subscribe_block)) != 1:
            errors.append('Homepage #subscribe must have exactly one button CTA')
        if 'keep/cut' not in subscribe_block.lower() and 'weekly' not in subscribe_block.lower():
            errors.append('Homepage #subscribe must be labeled as the free Keep/Cut Weekly email')
        if 'join premium on whop' in subscribe_block.lower() or 'start 7-day' in subscribe_block.lower():
            errors.append('Homepage #subscribe must not look like the paid Premium CTA')
    if 'Join Premium on Whop — 7-day trial · LAUNCH50' not in home_html:
        errors.append('Homepage must keep a labeled LAUNCH50 upgrade CTA (not as the hero primary)')
    if 'https://whop.com/checkout/ch_DKm5yxA1OBXoDru/?promo=LAUNCH50' not in home_html:
        errors.append('Homepage upgrade checkout must use the LAUNCH50 promo URL')
    hero_html = home_html[home_html.find('class="hero '): home_html.find('hero-device')] if 'class="hero ' in home_html and 'hero-device' in home_html else ''
    if 'href="/stack-audit.html">Free Stack Audit' not in hero_html:
        errors.append('Homepage hero primary CTA must be Free Stack Audit')
    if 'Join Premium' in hero_html:
        errors.append('Homepage hero must not lead with Join Premium')
    if '/stack-audit.html' not in home_html:
        errors.append('Homepage must link the free Stack Audit')
    home_head = home_html.split('</head>', 1)[0]
    if 'operationalize' in home_html.lower():
        errors.append('Homepage still says operationalize (meta/OG/Twitter/JSON-LD must use second-person voice)')
    if 'The essential AI tools directory' in home_html:
        errors.append('Homepage still uses The essential AI tools directory')
    if 'Stop paying for tools you do not use' not in home_head:
        errors.append('Homepage head missing second-person title')
    if 'See which subscriptions you should keep' not in home_head:
        errors.append('Homepage head missing second-person description')
    for needle, label in (
        ('property="og:title" content="AIToolsEssentials — Stop paying for tools you do not use"', 'og:title'),
        ('property="og:description" content="See which subscriptions you should keep, which you can cancel, and what to test this week."', 'og:description'),
        ('name="twitter:title" content="AIToolsEssentials — Stop paying for tools you do not use"', 'twitter:title'),
        ('name="twitter:description" content="See which subscriptions you should keep, which you can cancel, and what to test this week."', 'twitter:description'),
        ('"name": "AIToolsEssentials — Stop paying for tools you do not use"', 'JSON-LD name'),
        ('"description": "See which subscriptions you should keep, which you can cancel, and what to test this week."', 'JSON-LD description'),
    ):
        if needle not in home_head:
            errors.append(f'Homepage head missing {label} second-person voice')
    for p in ROOT.rglob('*.html'):
        rel = p.relative_to(ROOT)
        if 'admin' in rel.parts or any(part.startswith('.') for part in rel.parts) or 'go' in rel.parts:
            continue
        if 'operationalize' in p.read_text().lower():
            errors.append(f'{rel} still says operationalize')
    checkout_html = (ROOT / 'checkout/complete/index.html').read_text()
    if 'Payment confirmed' in checkout_html:
        errors.append('checkout/complete must not claim Payment confirmed from a client query')
    if '/premium/welcome/' not in checkout_html:
        errors.append('checkout/complete must redirect to /premium/welcome/')
    if 'http-equiv="refresh"' not in checkout_html:
        errors.append('checkout/complete must use a JS-free meta refresh')
    if 'cannot verify a charge' not in checkout_html.lower() and 'If Whop shows payment succeeded' not in checkout_html:
        errors.append('checkout/complete must be honest that Whop is the source of truth')
    if "You're in" in checkout_html:
        errors.append('checkout/complete must not use confirmation tone')
    welcome_html = (ROOT / 'premium/welcome/index.html').read_text()
    if 'https://whop.com/joined/aitoolsessentials-premium/' not in welcome_html:
        errors.append('premium/welcome must use the product hub deep link')
    if 'https://whop.com/hub"' in welcome_html or "https://whop.com/hub'" in welcome_html:
        errors.append('premium/welcome still uses generic whop.com/hub')
    pricing_html = (ROOT / 'pricing/index.html').read_text()
    if '/stack-audit.html' not in pricing_html:
        errors.append('Pricing page must link the free Stack Audit')
    if 'Join Premium on Whop — 7-day trial · LAUNCH50' not in pricing_html:
        errors.append('Pricing page must label the Whop CTA with trial + LAUNCH50')
    if 'https://whop.com/checkout/ch_DKm5yxA1OBXoDru/?promo=LAUNCH50' not in pricing_html:
        errors.append('Pricing page primary checkout must use the LAUNCH50 promo URL')
    if 'second product' not in pricing_html.lower() and 'not a second' not in pricing_html.lower():
        errors.append('Pricing page must say the human audit is not a second paid product')
    services_audit = ROOT / 'services/ai-stack-audit.html'
    if services_audit.exists():
        services_html = services_audit.read_text()
        if '/stack-audit.html' not in services_html:
            errors.append('services/ai-stack-audit.html must distinguish the free instant Stack Audit')
    library_hub = ROOT / 'premium/library/index.html'
    if not library_hub.exists():
        errors.append('Missing premium/library/index.html preview hub')
    else:
        library_html = library_hub.read_text()
        preview_ok = any(
            phrase in library_html.lower()
            for phrase in ('public preview', 'not gated', 'no server-side gate', 'not a login wall', 'cannot hide')
        )
        if not preview_ok:
            errors.append('Premium library hub must say the pages are a public preview and not gated')
        if 'whop.com/checkout/ch_DKm5yxA1OBXoDru' not in library_html:
            errors.append('Premium library hub must keep the existing Whop Premium checkout URL')
        if 'public premium preview' not in library_html.lower():
            errors.append('Premium library hub must be labeled Public Premium preview')
        if '?promo=LAUNCH50' not in library_html:
            errors.append('Premium library hub primary checkout must use LAUNCH50')
    conversion_hits = list((ROOT).glob('tools/*/index.html'))[:3]
    for sample in conversion_hits:
        text = sample.read_text()
        if 'premium-conversion-panel' in text and 'Subscribe on Whop' in text:
            errors.append(f'{sample.relative_to(ROOT)} Premium CTA still says Subscribe on Whop')
    header = home_html.split('</header>', 1)[0]
    if '/subscribe/' not in header and 'href="subscribe/"' not in header:
        errors.append('Homepage nav must include Subscribe → /subscribe/')
    if '/stack-audit.html' not in header:
        errors.append('Homepage nav must include Stack Audit')
    if '/premium/' not in header and 'href="premium/"' not in header:
        errors.append('Homepage nav must include Premium')
    if '/tools/' not in header:
        errors.append('Homepage nav must include Tools')
    for junk in ('Cost calc', 'Shortlist', 'Coding quiz', 'Best AI tools', 'Switching'):
        if junk in header:
            errors.append(f'Homepage nav still has fat-nav junk: {junk}')
    main_html = home_html[home_html.find('<main>'): home_html.find('</main>')] if '<main>' in home_html and '</main>' in home_html else ''
    if 'Three paths' in main_html:
        errors.append('Homepage still has the Three paths section')
    if 'Essential categories' in main_html:
        errors.append('Homepage still has the Essential categories grid')
    if 'Do not buy a tool because the demo looked clever' in main_html:
        errors.append('Homepage still has the how-to-choose workflow section')
    if 'State of AI Tool Pricing' in main_html:
        errors.append('Homepage still has the State of AI Pricing deep section')
    if 'AIT LEAD MAGNET' in home_html or 'Print this before you buy another subscription' in main_html:
        errors.append('Homepage still has the PDF checklist / lead magnet')
    if 'AIT HOMEPAGE JOB TILES' in home_html:
        errors.append('Homepage still has the three-paths job tiles')
    if 'AIT HOMEPAGE CITE STRIP' in home_html:
        errors.append('Homepage still has the cite-strip mega CTA row')
    if 'AIT WORKFLOW LIBRARY PROMO' in home_html:
        errors.append('Homepage still has the workflow library promo')
    if 'AIT PREMIUM MODULE' in home_html:
        errors.append('Homepage still has a duplicate Premium closer module')
    if 'If you sell a tool, submit evidence' in main_html:
        errors.append('Homepage still has the vendor submit pitch')
    if home_html.count('AIT HOMEPAGE PREMIUM BAND START') != 1:
        errors.append('Homepage must have exactly one Premium band')
    stack_audit_buttons = home_html.count('href="/stack-audit.html">Free Stack Audit')
    if stack_audit_buttons > 2:
        errors.append(f'Homepage repeats Free Stack Audit too many times ({stack_audit_buttons})')
    if 'Find overlapping AI subscriptions' not in hero_html and 'what to cancel' not in hero_html.lower():
        errors.append('Homepage H1 must be about overlapping subscriptions / what to cancel')
    if 'pay $12 to stop paying' in home_html.lower():
        errors.append('Homepage still says pay $12 to stop paying for AI')
    footer = home_html[home_html.find('<footer'): home_html.find('</footer>')] if '<footer' in home_html else ''
    if '/pricing-watch/' not in footer:
        errors.append('Homepage footer must link Pricing Watch')
    if '/tools/' not in footer:
        errors.append('Homepage footer must link the Tools directory')
    subscribe_page = ROOT / 'subscribe/index.html'
    if subscribe_page.exists():
        subscribe_html = subscribe_page.read_text()
        if 'aitoolsessentials.beehiiv.com/subscribe' not in subscribe_html:
            errors.append('Subscribe page missing Beehiiv signup URL')
        if 'id="digest-form"' in subscribe_html or 'formsubmit.co/ajax' in subscribe_html:
            errors.append('Subscribe page must not wire FormSubmit to the newsletter')
    else:
        errors.append('Missing subscribe/index.html')
    issue1 = ROOT / 'newsletter/2026-w35.html'
    if issue1.exists():
        issue_html = issue1.read_text()
        if 'The AI bill you forgot to cancel' not in issue_html:
            errors.append('Issue 1 public copy must use the newsletter subject')
        if 'Sir, you appear' in issue_html or 'J. —' in issue_html or 'Good evening. I have reviewed' in issue_html:
            errors.append('Issue 1 public copy still has butler/J teaser language')
        if 'AIToolsEssentials' not in issue_html:
            errors.append('Issue 1 public copy missing AIToolsEssentials sign-off')
        if 'newsletter-sheet' not in issue_html or 'newsletter-masthead' not in issue_html:
            errors.append('Issue 1 public page must use newsletter composition, not a generic article shell')
        if 'class="scene scene-dark"' in issue_html:
            errors.append('Issue 1 public page still uses the dark article hero shell')
        if 'Morning.' not in issue_html:
            errors.append('Issue 1 public copy missing Morning. opening')
    else:
        errors.append('Missing newsletter/2026-w35.html')
    newsletter_hub = ROOT / 'newsletter/index.html'
    if newsletter_hub.exists() and 'Sir, you appear' in newsletter_hub.read_text():
        errors.append('Newsletter index still uses the butler Issue 1 teaser')

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
