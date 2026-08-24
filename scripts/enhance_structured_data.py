#!/usr/bin/env python3
"""Add durable structured data enhancements to AIToolsEssentials pages.

Idempotent post-generation pass:
- BreadcrumbList schema for public HTML pages.
- ItemList schema for discovery/growth hubs that list tools.
- Standalone SoftwareApplication schema for tool reviews (in addition to Review schema).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path('/Users/georgezikry/aitoolessentials/site')
DOMAIN = 'https://aitoolsessentials.com'
MARKER_START = '<!-- AIT STRUCTURED DATA START -->'
MARKER_END = '<!-- AIT STRUCTURED DATA END -->'


def load_tools():
    tools = json.loads((ROOT / 'data/tools.json').read_text())
    return tools, {t['slug']: t for t in tools}


def public_pages():
    for p in ROOT.rglob('*.html'):
        rel = p.relative_to(ROOT)
        if 'admin' in rel.parts:
            continue
        yield p


def url_for_rel(rel: Path) -> str:
    if rel.name == 'index.html':
        if len(rel.parts) == 1:
            return f'{DOMAIN}/'
        return f'{DOMAIN}/' + '/'.join(rel.parts[:-1]) + '/'
    return f'{DOMAIN}/' + '/'.join(rel.parts)


def title_from_file(html: str, rel: Path) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S | re.I)
    if m:
        return re.sub(r'<.*?>', '', m.group(1)).strip()
    m = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
    if m:
        return re.sub(r'\s*[—|].*$', '', m.group(1)).strip()
    stem = rel.stem if rel.name != 'index.html' else (rel.parts[-2] if len(rel.parts) > 1 else 'Home')
    return stem.replace('-', ' ').title()


def breadcrumb_schema(rel: Path, html: str):
    if rel.name == 'index.html' and len(rel.parts) == 1:
        return None
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"}]
    parts = list(rel.parts)
    if parts[-1] == 'index.html':
        parts = parts[:-1]
    else:
        parts[-1] = rel.stem
    path_accum = []
    for part in parts:
        if part in ('tools', 'categories', 'articles', 'comparisons', 'legal', 'services', 'benchmarks', 'research', 'community', 'alternatives'):
            name = {
                'tools': 'Tools', 'categories': 'Categories', 'articles': 'Guides', 'comparisons': 'Comparisons',
                'legal': 'Legal', 'services': 'Services', 'benchmarks': 'Benchmarks', 'research': 'Research',
                'community': 'Community', 'alternatives': 'Alternatives'
            }.get(part, part.title())
        else:
            name = title_from_file(html, rel) if part == parts[-1] else part.replace('-', ' ').replace('%20', ' ').title()
        path_accum.append(part)
        item = f"{DOMAIN}/" + '/'.join(path_accum)
        if rel.name == 'index.html' or part != parts[-1]:
            item += '/'
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": name, "item": item})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}


def itemlist_for_page(rel: Path, tools: list, by_slug: dict):
    rel_s = str(rel)
    if rel_s == 'tools/index.html':
        items = tools
        name = 'AI Tools Directory'
    elif rel_s == 'free-ai-tools.html':
        items = [t for t in tools if 'free' in t.get('price', '').lower()]
        name = 'Best Free AI Tools'
    elif rel_s == 'tool-finder.html':
        items = sorted(tools, key=lambda t: float(t.get('rating', 0) or 0), reverse=True)[:20]
        name = 'AI Tool Finder Recommendations'
    elif rel_s == 'alternatives/index.html':
        slugs = ['claude','gemini','perplexity','grok','deepseek','meta-ai','copy-ai','chatgpt','grammarly','make','n8n','airtable-ai','leonardo-ai','adobe-firefly','canva-ai','descript','allvideoai','heygen','synthesia']
        items = [by_slug[s] for s in slugs if s in by_slug]
        name = 'AI Tool Alternatives'
    else:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "numberOfItems": len(items),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{DOMAIN}/tools/{t['slug']}/", "name": t['name']}
            for i, t in enumerate(items)
        ]
    }


def software_schema_for_tool(rel: Path, tool: dict):
    if len(rel.parts) == 3 and rel.parts[0] == 'tools' and rel.parts[2] == 'index.html':
        return {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": tool.get('name'),
            "applicationCategory": tool.get('category'),
            "description": tool.get('summary'),
            "url": f"{DOMAIN}/tools/{tool['slug']}/",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": tool.get('price', 'See official pricing')},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": str(tool.get('rating', 0)), "bestRating": "5", "ratingCount": "1"},
            "publisher": {"@type": "Organization", "name": "AIToolsEssentials", "url": f"{DOMAIN}/"}
        }
    return None


def inject(p: Path, schemas: list[dict[str, Any] | None]) -> bool:
    h = p.read_text()
    orig = h
    h = re.sub(r'\s*<!-- AIT STRUCTURED DATA START -->.*?<!-- AIT STRUCTURED DATA END -->\s*', '\n', h, flags=re.S)
    schemas = [s for s in schemas if s]
    if schemas:
        block = MARKER_START + '\n' + '\n'.join(
            '<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False, separators=(',', ':')) + '</script>'
            for s in schemas
        ) + '\n' + MARKER_END + '\n'
        h = h.replace('</head>', block + '</head>', 1)
    if h != orig:
        p.write_text(h)
        return True
    return False


def main():
    tools, by_slug = load_tools()
    changed = 0
    for p in public_pages():
        rel = p.relative_to(ROOT)
        html = p.read_text()
        schemas = [breadcrumb_schema(rel, html), itemlist_for_page(rel, tools, by_slug)]
        if len(rel.parts) == 3 and rel.parts[0] == 'tools' and rel.parts[2] == 'index.html':
            slug = rel.parts[1]
            if slug in by_slug:
                schemas.append(software_schema_for_tool(rel, by_slug[slug]))
        if inject(p, schemas):
            changed += 1
    print(f'Structured data enhanced on {changed} pages')


if __name__ == '__main__':
    main()
