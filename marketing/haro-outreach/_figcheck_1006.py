import json, re
from pathlib import Path
S = Path('/Users/georgezikry/aitoolessentials/site')
snapf = json.loads((S / 'data/pricing_snapshots.json').read_text())
snaps = snapf['snapshots']
print('updated:', snapf.get('updated'), '| n:', len(snaps))

for k in ('browse-ai', 'khanmigo', 'replit-ai', 'otter-ai', 'fireflies', 'synthesia'):
    v = snaps.get(k)
    if not v:
        print(k, 'MISSING'); continue
    print('---', k, '| date:', v.get('date'))
    print('   ', ' '.join((v.get('digest') or '').split())[:400])

print('\n--- tool_sources.json ---')
p = S / 'data/tool_sources.json'
print('exists:', p.exists())
if p.exists():
    ts = json.loads(p.read_text())
    print(type(ts).__name__, len(ts))
    print(str(ts)[:600])
