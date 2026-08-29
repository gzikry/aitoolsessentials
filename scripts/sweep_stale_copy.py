#!/usr/bin/env python3
"""Sweep public HTML for stale inventory copy and refresh new category tool lists."""
from pathlib import Path
import json, re, html as H

ROOT = Path('.')
TOOLS = json.loads((ROOT / 'data/tools.json').read_text())
COUNT = len(TOOLS)

# 1. Stale inventory replacements for public HTML only.
replacements = {
    '39 AI tools': f'{COUNT} AI tools',
    '39 AI tools reviewed': f'{COUNT} AI tools reviewed',
    '40 AI tools': f'{COUNT} AI tools',
    '40 AI tools reviewed': f'{COUNT} AI tools reviewed',
    '45 AI tools': f'{COUNT} AI tools',
    '45 AI tools reviewed': f'{COUNT} AI tools reviewed',
    '61 AI tools': f'{COUNT} AI tools',
    '69 AI tools': f'{COUNT} AI tools',
    'planned Premium': 'Premium',
    '$497': '$12/month',
}
skip_dirs = {'.git', '.hermes', 'admin', 'scripts', 'content_briefs', 'audit_reports'}

html_files = []
for p in ROOT.rglob('*.html'):
    if any(s in p.parts for s in skip_dirs):
        continue
    html_files.append(p)

print(f'Scanning {len(html_files)} public HTML files for stale copy...')
changed = 0
for p in html_files:
    try:
        text = p.read_text()
    except Exception:
        continue
    new = text
    for old, repl in replacements.items():
        if old in new:
            new = new.replace(old, repl)
    if new != text:
        p.write_text(new)
        changed += 1
print(f'Refreshed stale inventory copy in {changed} public HTML files.')

# 2. Refresh new category pages with all tools in that category.
new_categories = {'Email AI', 'Browser Automation', 'Research'}
for cat in new_categories:
    cat_tools = sorted([t for t in TOOLS if t.get('category') == cat], key=lambda x: -x.get('rating', 0))
    cat_dir = ROOT / 'categories' / cat
    index = cat_dir / 'index.html'
    if not index.exists():
        print(f'Missing category page: {index}')
        continue
    txt = index.read_text()
    # Replace the product-grid / directory-grid section with all tools for this category.
    # Strategy: find the existing grid container and rebuild its inner cards.
    # Pattern: <div class="directory-grid" ...> ... </div>
    grid_start = txt.find('<div class="directory-grid"')
    grid_end = txt.find('</div>', grid_start) + 6 if grid_start != -1 else -1
    if grid_start == -1 or grid_end == -1:
        print(f'Could not locate grid in {index}')
        continue
    cards = []
    for i, t in enumerate(cat_tools[:12], start=1):
        stars = '★' * int(round(t.get('rating', 0)))
        score_label = f"{t['rating']}/5" if t.get('rating') else 'Editorial score in review'
        best = t.get('best_for', t.get('summary', ''))
        best = best[:110].rstrip()
        cards.append(f'''<article class="directory-card" style="min-height:260px">
          <div>
            <span class="category-pill">#{i} · {score_label}</span>
            <h3><a href="../../tools/{t['slug']}/">{H.escape(t['name'])}</a></h3>
            <p>{H.escape(best)}</p>
            <span style="color:#f5a623;letter-spacing:2px">{stars}</span>
          </div>
          <div class="card-actions">
            <a class="text-link" href="../../tools/{t['slug']}/">Read review</a>
            <a class="button button-blue small" href="{H.escape(t.get('official',''))}" rel="sponsored noopener nofollow" target="_blank">Visit site</a>
          </div>
        </article>''')
    new_grid = '<div class="directory-grid" style="max-width:760px">\n' + '\n'.join(cards) + '\n</div>'
    new_txt = txt[:grid_start] + new_grid + txt[grid_end:]
    if new_txt != txt:
        index.write_text(new_txt)
        print(f'Refreshed {index} with {len(cat_tools)} tools')
    else:
        print(f'No change needed for {index}')
