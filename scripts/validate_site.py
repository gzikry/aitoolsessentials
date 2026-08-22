#!/usr/bin/env python3
"""Validate AIToolsEssentials static site quality gates."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urldefrag
import json
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
    for rel in ['data/tools.json','data/affiliate_programs.json','data/sponsors.json','data/newsletter.json','data/revenue_targets.json','data/sponsor_inventory.json','data/benchmarks.json']:
        result = load_json(ROOT / rel)
        if isinstance(result, str):
            errors.append(result)

    tools = json.loads((ROOT/'data/tools.json').read_text())
    tool_slugs = {t['slug'] for t in tools}
    revenue_targets = json.loads((ROOT/'data/revenue_targets.json').read_text())
    target_slugs = {r.get('tool_slug') for r in revenue_targets}
    tool_slugs_for_targets = {t['slug'] for t in tools}
    if target_slugs != tool_slugs_for_targets:
        errors.append('Revenue targets do not match tools.json slugs')
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
    for tool in tools:
        review = ROOT/'tools'/tool['slug']/'index.html'
        if review.exists():
            text = review.read_text().lower()
            for phrase in unsupported_claim_patterns:
                if phrase in text:
                    errors.append(f"{review.relative_to(ROOT)} contains unsupported testing claim: {phrase}")
            for required in ['Trial checklist', 'How we evaluated', 'editorial score']:
                if required.lower() not in text:
                    errors.append(f"{review.relative_to(ROOT)} missing review evidence label: {required}")
    
    # Check for key viral pages
    key_pages = ['leaderboard.html','submit-tool.html','downloads/ai-tool-evaluation-scorecard.html']
    missing_keys = [p for p in key_pages if not (ROOT / p).exists()]
    if missing_keys:
        errors.append(f'Missing key pages: {missing_keys}')

    parsers = {}
    for f in ROOT.rglob('*.html'):
        p = Parser(); p.feed(f.read_text()); parsers[f.resolve()] = p
    for f,p in parsers.items():
        page_text = ' '.join(p.text).lower()
        if any(part in f.parts for part in ['articles','comparisons','tools']):
            if 'disclosure' not in page_text and 'affiliate' not in page_text:
                errors.append(f'{f.relative_to(ROOT)} missing disclosure language')
        for tag, href in p.refs:
            if href.startswith(('http://','https://','mailto:')):
                continue
            from urllib.parse import unquote
            href_dec = unquote(href)
            url, frag = urldefrag(href_dec)
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

    sitemap = ROOT/'sitemap.xml'
    if sitemap.exists():
        html_count = len([p for p in ROOT.rglob('*.html') if 'admin' not in str(p.relative_to(ROOT))])
        url_count = sitemap.read_text().count('<url>')
        if html_count != url_count:
            errors.append(f'Sitemap URL count {url_count} != HTML count {html_count}')
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
