#!/usr/bin/env python3
"""Apply approved affiliate tracking URLs to CTAs. Runs LAST in the pipeline so regeneration can't wipe them."""
import json, re
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent
    try:
        d = json.loads((root/'data/affiliate_programs.json').read_text())
    except Exception as e:
        print(f'affiliate wiring skipped: {e}')
        return
    approved = {}
    for prog in d.get('affiliate_programs', []):
        slug = prog.get('tool_slug')
        url = prog.get('affiliate_url') or prog.get('approved_tracking_url')
        if slug and url and prog.get('application_status') == 'approved':
            approved[slug] = url
    if not approved:
        print('affiliate wiring: no approved programs')
        return
    tools = json.loads((root/'data/tools.json').read_text())
    changed = 0
    disclosure = '<p class="pricing-fineprint">Affiliate link — we may earn a commission at no cost to you. See our <a href="../../legal/affiliate-disclosure.html">disclosure</a>.</p>'
    for t in tools:
        slug = t['slug']
        if slug not in approved:
            continue
        base = re.sub(r'/$', '', t['official'])
        url = approved[slug]
        targets = [root/'tools'/slug/'index.html'] + list((root/'articles').glob('*.html')) + list((root/'comparisons').glob('*.html'))
        pat = re.compile(r'href="' + re.escape(base) + r'/?(" rel="[^"]*sponsored[^"]*")')
        for p in targets:
            s = p.read_text()
            new = s.replace(f'href="{base}/" rel="sponsored noopener nofollow"', f'href="{url}" rel="sponsored noopener nofollow"')
            new = pat.sub('href="' + url + '"\\1', new)
            if new != s and 'sponsored' in new:
                # add disclosure on review page CTA
                if p == root/'tools'/slug/'index.html' and 'pricing-fineprint">Affiliate link' not in new:
                    j = new.find(url)
                    if j > -1:
                        k = new.find('</a>', j)
                        new = new[:k+4] + disclosure + new[k+4:]
                p.write_text(new)
                changed += 1
    print(f'affiliate wiring: {changed} pages updated')

if __name__ == '__main__':
    main()
