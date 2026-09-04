#!/usr/bin/env python3
"""Post-generation cleanup pass. Idempotent — safe to run after every regeneration.
Fixes: typo'd domain, injected share blocks, <main> balance, admin link leaks,
asset path depths, CTA labels/links, category slugs, share-row mount, contact email."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMAIL = 'contact@aitoolsessentials.com'
SLUG_MAP = {'writing-productivity': 'Writing & Productivity', 'creative-marketing': 'Creative & Marketing',
            'audio-video': 'Audio & Video', 'general-ai-assistant': 'General AI Assistant'}
PUBLIC_PREFIXES = ('tools', 'categories', 'articles', 'comparisons', 'legal', 'services',
                   'advertise', 'downloads', 'benchmarks')


def normalize_home_links(html: str) -> str:
    """Point every homepage link at the canonical root URL."""
    html = re.sub(r'href="(?:/|(?:\.\./)*)index\.html([#?][^"]*)?"',
                  lambda m: 'href="/' + (m.group(1) or '') + '"', html)
    return html


def fix_page(p: Path) -> bool:
    rel_parts = p.relative_to(ROOT).parts
    depth = len(rel_parts) - 1
    prefix = '../' * depth
    h = p.read_text()
    orig = h

    # Canonical homepage path: avoid splitting analytics and crawl signals
    # between / and /index.html.
    h = normalize_home_links(h)

    # Leftover pick-one pages once appended ".html" onto filenames that already
    # included the suffix, producing crawl-breaking /page.html.html canonicals.
    h = h.replace(".html.html", ".html")

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
            # Close main before the footer opens, never inside the footer.
            if '<footer' in h:
                h = h.replace('<footer', '</main>\n<footer', 1)
            else:
                h = h.replace('</body>', '</main>\n</body>', 1)
        elif n > 1:
            first = h.find('</main>')
            h = h[:first + 7] + h[first + 7:].replace('</main>', '')
        # Repair legacy pages where </main> was inserted inside/after the footer.
        footer_open = h.find('<footer')
        main_close = h.find('</main>')
        if footer_open >= 0 and main_close > footer_open:
            h = h[:main_close] + h[main_close + len('</main>'):]
            footer_open = h.find('<footer')
            h = h[:footer_open] + '</main>\n' + h[footer_open:]
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

    # 7b. Keep benchmark evidence one click away from every primary nav
    # except the slim homepage header (hero already fronts Stack Audit).
    is_slim_home = rel_parts == ('index.html',) or 'data-nav="slim"' in h
    if not is_slim_home:
        if '<nav class="nav-links">' in h and '>Learn</a>' not in h:
            h = h.replace('</nav>', f'<a href="{prefix}articles/learn.html">Learn</a></nav>', 1)
        if '<nav class="nav-links">' in h and '>Benchmarks</a>' not in h:
            h = h.replace('</nav>', f'<a href="{prefix}benchmarks/">Benchmarks</a>\n</nav>', 1)

    # 8. Inject share.css + site.js + cookie-consent.js + share-row mount
    if 'share.css' not in h:
        h = h.replace('</head>', f'<link rel="stylesheet" href="{prefix}css/share.css">\n</head>', 1)
    if 'site.js' not in h:
        h = h.replace('</body>', f'<script src="{prefix}js/site.js" defer></script>\n</body>')
    if 'cookie-consent.js' not in h:
        h = h.replace('</body>', f'<script src="{prefix}js/cookie-consent.js" defer></script>\n</body>')
    if 'id="share-row"' not in h and '<footer' in h:
        h = h.replace('<footer', '<div id="share-row" hidden></div>\n  <footer', 1)

    # 9. Canonical trust/legal links in every public footer.
    # Slim homepage footer is owned by enhance_homepage — do not re-inflate it.
    if '<footer' in h and 'data-footer="slim"' not in h:
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

    # stray script-footer removal (legacy bug)
    h = __import__('re').sub(r'</footer>\s*</main>\s*<footer>(\s*<script)', '</footer></main>\n\\1', h)
    h = __import__('re').sub(r'(Contact</a>)</main>\s*<footer>\s*(<script)', r'\1</footer></main>\n\2', h)

    # Impact.com site verification on every page
    if "impact-site-verification" not in h:
        h = h.replace('<head>', '<head><meta name="impact-site-verification" content="972313e6-cecc-47f0-aea2-c99b4364ee09">', 1)

    # og-image-injection: social share image + twitter card everywhere
    if 'property="og:image"' not in h and '</head>' in h:
        h = h.replace('</head>', '<meta property="og:image" content="https://aitoolsessentials.com/assets/og-ai-tools.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://aitoolsessentials.com/assets/og-ai-tools.jpg"></head>', 1)

    # GSC verification on every page
    if '<meta name="google-site-verification"' not in h:
        h = h.replace('<head>', '<head><meta name="google-site-verification" content="OzzGs2QF4v6zSBd9uO95NGgSPH5B598E6DPtcjRNn_4">', 1)
    # Normalize trailing horizontal whitespace so generated diffs stay clean.
    h = re.sub(r'[ \t]+(?=\r?$)', '', h, flags=re.M)

    if h != orig:
        p.write_text(h)
        return True
    return False


def main():
    changed = 0
    for p in ROOT.rglob('*.html'):
        rel = p.relative_to(ROOT)
        if 'admin' in rel.parts or 'go' in rel.parts:
            continue
        if fix_page(p):
            changed += 1
    print(f'Cleanup pass: fixed {changed} pages')


if __name__ == '__main__':
    main()

