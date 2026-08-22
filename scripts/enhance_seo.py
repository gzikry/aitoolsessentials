#!/usr/bin/env python3
"""Inject sitewide canonical, Open Graph, Twitter, and JSON-LD metadata.

Safe/idempotent: removes previous AIToolsEssentials SEO block before inserting.
"""
from pathlib import Path
from html.parser import HTMLParser
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://aitoolsessentials.com'
SITE_NAME = 'AIToolsEssentials'
MARKER_START = '<!-- AIT SEO START -->'
MARKER_END = '<!-- AIT SEO END -->'

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.description = ''
        self.h1 = ''
        self._in_title = False
        self._in_h1 = False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'title':
            self._in_title = True
        if tag == 'h1' and not self.h1:
            self._in_h1 = True
        if tag == 'meta' and d.get('name') == 'description':
            self.description = d.get('content', '')
    def handle_endtag(self, tag):
        if tag == 'title': self._in_title = False
        if tag == 'h1': self._in_h1 = False
    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        if self._in_h1 and not self.h1:
            self.h1 += data.strip()

def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == 'index.html':
        return BASE_URL + '/'
    if rel.endswith('/index.html'):
        return BASE_URL + '/' + rel[:-10]
    return BASE_URL + '/' + rel

def page_type(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    if 'tools' in parts and path.name != 'index.html': return 'SoftwareApplication'
    if 'articles' in parts: return 'Article'
    if 'comparisons' in parts: return 'Article'
    if 'services' in parts: return 'Service'
    return 'WebPage'

def json_ld(path: Path, title: str, desc: str, url: str):
    typ = page_type(path)
    data = {
        '@context': 'https://schema.org',
        '@type': typ,
        'name': title,
        'description': desc,
        'url': url,
        'isPartOf': {'@type': 'WebSite', 'name': SITE_NAME, 'url': BASE_URL + '/'},
        'publisher': {'@type': 'Organization', 'name': SITE_NAME, 'url': BASE_URL + '/'}
    }
    if typ == 'Article':
        data['headline'] = title
        data['author'] = {'@type': 'Organization', 'name': SITE_NAME}
    if typ == 'SoftwareApplication':
        data['applicationCategory'] = 'AI tool'
        data['operatingSystem'] = 'Web'
    if typ == 'Service':
        data['serviceType'] = 'AI Stack Audit strategy report'
        data['provider'] = {'@type': 'Organization', 'name': SITE_NAME}
    return json.dumps(data, ensure_ascii=False)

def strip_existing(content: str) -> str:
    pattern = re.compile(r'\n?\s*' + re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END) + r'\s*\n?', re.S)
    return pattern.sub('\n', content)

def enhance(path: Path):
    content = strip_existing(path.read_text())
    parser = MetaParser(); parser.feed(content)
    title = parser.title or parser.h1 or SITE_NAME
    desc = parser.description or 'AIToolsEssentials helps readers compare AI tools by workflow fit, pricing, and practical business value.'
    url = url_for(path)
    block = f'''\n  {MARKER_START}
  <link rel="canonical" href="{html.escape(url, quote=True)}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:type" content="{'article' if page_type(path) == 'Article' else 'website'}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(desc, quote=True)}">
  <meta property="og:url" content="{html.escape(url, quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(desc, quote=True)}">
  <script type="application/ld+json">{json_ld(path, title, desc, url)}</script>
  {MARKER_END}'''
    if '</head>' not in content:
        return False
    content = content.replace('</head>', block + '\n</head>', 1)
    path.write_text(content)
    return True

def main():
    changed = 0
    for path in ROOT.rglob('*.html'):
        if '.hermes' in path.parts:
            continue
        if enhance(path):
            changed += 1
    print(f'Enhanced SEO metadata on {changed} HTML pages')

if __name__ == '__main__':
    main()
