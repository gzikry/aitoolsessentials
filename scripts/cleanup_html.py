#!/usr/bin/env python3
"""Post-generation cleanup pass. Idempotent — safe to run after every regeneration.
Fixes: typo'd domain, injected share blocks, <main> balance, admin link leaks,
asset path depths, CTA labels/links, category slugs, share-row mount, contact email."""
import re
from pathlib import Path

ROOT = Path('/Users/georgezikry/aitoolessentials/site')
EMAIL = 'contact@aitoolsessentials.com'
SLUG_MAP = {'writing-productivity': 'Writing & Productivity', 'creative-marketing': 'Creative & Marketing',
            'audio-video': 'Audio & Video', 'general-ai-assistant': 'General AI Assistant'}
PUBLIC_PREFIXES = ('tools', 'categories', 'articles', 'comparisons', 'legal', 'services',
                   'advertise', 'downloads', 'benchmarks')


def fix_page(p: Path) -> bool:
    rel_parts = p.relative_to(ROOT).parts
    depth = len(rel_parts) - 1
    prefix = '../' * depth
    h = p.read_text()
    orig = h

    # 1. Domain typo
    h = h.replace('aitoolsessentials.com', 'aitoolsessentials.com')

    # 2. Remove injected social-sharing blocks (replaced by JS share row)
    h = re.sub(r'<section class="social-sharing".*?</section>\s*', '', h, flags=re.S)

    # 3. <main> balance
    if '<main' not in h and '</header>' in h:
        h = h.replace('</header>', '</header>\n<main>', 1)
    if '<main' in h:
        n = h.count('</main>')
        if n == 0:
            h = h.replace('</footer>', '</main>\n<footer>', 1) if '</footer>' in h \
                else h.replace('</body>', '</main>\n</body>', 1)
        elif n > 1:
            first = h.find('</main>')
            h = h[:first + 7] + h[first + 7:].replace('</main>', '')
    elif '</main>' in h:
        h = h.replace('</main>', '', 1)

    # 4. Admin/vendor link leaks on public pages
    if 'admin' not in rel_parts:
        h = re.sub(r'<a class="guide-pill" href="admin/[^"]*">[^<]*</a>\s*', '', h)
    h = re.sub(r'<a class="guide-pill" href="(?:\.\./)*vendors/submit-tool\.html">[^<]*</a>',
               '<a class="guide-pill" href="submit-tool.html">Submit a tool</a>', h)

    # 5. CTA label + dead links
    h = re.sub(r'>([^<]{2,40}):\s*Download scorecard</a>', '>Download the free scorecard</a>', h)
    h = h.replace('href="newsletter.html"', f'href="{prefix}index.html#subscribe"')
    h = h.replace('href="../newsletter.html"', f'href="{prefix}index.html#subscribe"')

    # 6. Category slugs
    def repl_slug(m):
        slug = m.group(1)
        if slug in SLUG_MAP:
            from urllib.parse import quote
            return f'href="categories/{quote(SLUG_MAP[slug])}/index.html"'
        return m.group(0)
    h = re.sub(r'href="categories/([a-z-]+)/index\.html"', repl_slug, h)

    # Canonical tool reviews use /tools/<slug>/, never stale flat .html files.
    def canonical_tool_link(m):
        lead, slug = m.group(1), m.group(2)
        if slug == 'index':
            return m.group(0)
        return f'href="{lead}tools/{slug}/"'
    h = re.sub(r'href="((?:\.\./)*)tools/([a-z0-9-]+)\.html"', canonical_tool_link, h)

    # 7. Asset + root-page paths by depth
    def fix_asset(m):
        stripped = re.sub(r'^(\.\./)+', '', m.group(2))
        return f'{m.group(1)}="{prefix}{stripped}"'
    h = re.sub(r'(href|src)="((?:\.\./)*(?:css|js|assets)/[^"]+)"', fix_asset, h)
    h = re.sub(r'href="(?:\.\./)+(index\.html)"', f'href="{prefix}\\1"', h)
    h = re.sub(
        r'href="(?:\.\./)+((?:' + '|'.join(PUBLIC_PREFIXES) + r')/[^"]*|leaderboard\.html|submit-tool\.html)"',
        lambda m: f'href="{prefix}{m.group(1)}"', h)

    # 7b. Keep benchmark evidence one click away from every primary nav.
    if '<nav class="nav-links">' in h and '>Benchmarks</a>' not in h:
        h = h.replace('</nav>', f'<a href="{prefix}benchmarks/">Benchmarks</a>\n</nav>', 1)

    # 8. Inject share.css + site.js + share-row mount
    if 'share.css' not in h:
        h = h.replace('</head>', f'<link rel="stylesheet" href="{prefix}css/share.css">\n</head>', 1)
    if 'site.js' not in h:
        h = h.replace('</body>', f'<script src="{prefix}js/site.js" defer></script>\n</body>')
    if 'id="share-row"' not in h and '<footer' in h:
        h = h.replace('<footer', '<div id="share-row" hidden></div>\n  <footer', 1)

    # 9. Canonical trust/legal links in every public footer.
    if '<footer' in h:
        footer_match = re.search(r'<footer[^>]*>.*?</footer>', h, re.S)
        if footer_match:
            footer = footer_match.group(0)
            additions = []
            if '>About</a>' not in footer:
                additions.append(f'<a href="{prefix}legal/about.html">About</a>')
            if '>Privacy</a>' not in footer:
                additions.append(f'<a href="{prefix}legal/privacy.html">Privacy</a>')
            if '>Terms</a>' not in footer:
                additions.append(f'<a href="{prefix}legal/terms.html">Terms</a>')
            if '>Corrections</a>' not in footer:
                additions.append(f'<a href="{prefix}legal/corrections.html">Corrections</a>')
            if f'mailto:{EMAIL}' not in footer:
                additions.append(f'<a href="mailto:{EMAIL}">Contact</a>')
            if additions:
                new_footer = footer.replace('</footer>', ''.join(additions) + '</footer>')
                h = h.replace(footer, new_footer, 1)

    if h != orig:
        p.write_text(h)
        return True
    return False


def main():
    changed = 0
    for p in ROOT.rglob('*.html'):
        if 'admin' in p.relative_to(ROOT).parts:
            continue
        if fix_page(p):
            changed += 1
    print(f'Cleanup pass: fixed {changed} pages')


if __name__ == '__main__':
    main()
