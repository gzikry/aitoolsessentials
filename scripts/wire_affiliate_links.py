#!/usr/bin/env python3
"""Apply approved affiliate tracking URLs to CTAs. Runs LAST in the pipeline so regeneration can't wipe them.

Public hrefs use public_href (site hop) when set so tracking slugs stay off public pages.
"""
import re
from pathlib import Path

from affiliate_util import approved_programs, public_affiliate_href, write_hop_pages


def main():
    root = Path(__file__).resolve().parent.parent
    try:
        approved = approved_programs(root)
    except Exception as e:
        print(f'affiliate wiring skipped: {e}')
        return
    hops = write_hop_pages(root)
    if not approved:
        print(f'affiliate wiring: no approved programs (hops={hops})')
        return
    tools = __import__('json').loads((root/'data/tools.json').read_text())
    changed = 0
    disclosure = '<p class="pricing-fineprint">Affiliate / referral link — we may earn a commission at no cost to you. See our <a href="../../legal/affiliate-disclosure.html">disclosure</a>.</p>'
    for t in tools:
        slug = t['slug']
        if slug not in approved:
            continue
        prog = approved[slug]
        base = re.sub(r'/$', '', t['official'])
        url = public_affiliate_href(prog)
        if not url:
            continue
        targets = [root/'tools'/slug/'index.html'] + list((root/'articles').glob('*.html')) + list((root/'comparisons').glob('*.html'))
        is_internal = url.startswith('/')
        rel_attr = 'sponsored nofollow' if is_internal else 'sponsored noopener nofollow'
        pat = re.compile(r'href="' + re.escape(base) + r'/?(" rel="[^"]*sponsored[^"]*")')
        for p in targets:
            if not p.exists():
                continue
            s = p.read_text()
            new = s.replace(f'href="{base}/" rel="sponsored noopener nofollow"', f'href="{url}" rel="{rel_attr}"')
            new = new.replace(f'href="{base}" rel="sponsored noopener nofollow"', f'href="{url}" rel="{rel_attr}"')
            new = pat.sub('href="' + url + '"\\1', new)
            if is_internal:
                new = new.replace(f'href="{url}" rel="sponsored noopener nofollow" target="_blank"', f'href="{url}" rel="{rel_attr}"')
                new = new.replace(f'href="{url}" rel="sponsored noopener nofollow"', f'href="{url}" rel="{rel_attr}"')
            if new != s and 'sponsored' in new:
                # add disclosure on review page CTA
                if p == root/'tools'/slug/'index.html' and 'pricing-fineprint">Affiliate' not in new:
                    j = new.find(url)
                    if j > -1:
                        k = new.find('</a>', j)
                        new = new[:k+4] + disclosure + new[k+4:]
                p.write_text(new)
                changed += 1
    print(f'affiliate wiring: {changed} pages updated; hops={hops}')

if __name__ == '__main__':
    main()
