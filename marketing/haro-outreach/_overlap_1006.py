import json, glob, re
from pathlib import Path

D = Path('/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach')

win = json.loads((D / '_window_1006.json').read_text())
prev = json.loads((D / 'digest-2026-10-05.json').read_text())
tracked = {o['url'].rstrip('/').split('/journo-request/')[-1] for o in prev['opportunities']}
print('tracked from 2026-10-05 digest:', len(tracked))

ai = [s for s, _ in win['ai']]
print('\nAI-token window slugs today:', len(ai))
for s in ai:
    print(('  ALREADY-TRACKED' if s in tracked else '  NEW            '), s)

print('\nspend-any window slugs today:', len(win['spend_any']))
for s, lm in win['spend_any']:
    print(('  tracked' if s in tracked else '  new    '), s)

# all digests merged counts
urls = set()
for f in D.glob('digest-*.json'):
    try:
        d = json.loads(f.read_text())
    except Exception:
        continue
    for o in d.get('opportunities', []):
        urls.add(o['url'].rstrip('/').rstrip('/').split('/journo-request/')[-1])
print('\nunique slugs across all digests:', len(urls))

# index pages in digests?
idx = [u for u in urls if '/media-outlets/' in u or '/topics/' in u]
print('index pages in digests:', len(idx))

# how many of today's AI slugs are brand new to the whole digest history
print('\nnew to ALL digest history:')
for s in ai:
    if s not in urls:
        print('   NEW-TO-HISTORY', s)
