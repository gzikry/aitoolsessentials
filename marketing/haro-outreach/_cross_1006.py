import json
from pathlib import Path
D = Path('/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach')
prev = json.loads((D / 'digest-2026-10-05.json').read_text())
ver = json.loads((D / 'verified-requests.json').read_text())
led = json.loads((D / 'pitch-ledger.json').read_text())
done = {u.rstrip('/').split('/journo-request/')[-1] for u in list(led.get('pitched', {})) + list(led.get('skipped', {}))}

prev_live, prev_cold = [], []
for o in prev['opportunities']:
    sl = o['url'].rstrip('/').split('/journo-request/')[-1]
    if sl in done:
        continue
    d = o.get('_days_old')
    (prev_live if (d is not None and d <= 10) else prev_cold).append((sl, d))
print('2026-10-05 digest: live_unp', len(prev_live), 'cold_unp', len(prev_cold))
print('  max live age yesterday:', max(d for _, d in prev_live))

now_live, now_cold = [], []
for o in prev['opportunities']:
    sl = o['url'].rstrip('/').split('/journo-request/')[-1]
    if sl in done:
        continue
    d = (ver.get(sl) or {}).get('days_old')
    (now_live if (d is not None and d <= 10) else now_cold).append((sl, d))
print('today: live_unp', len(now_live), 'cold_unp', len(now_cold))

crossed = [(sl, d) for sl, d in now_cold if sl in dict(prev_live)]
print('\nCROSSED live->cold since yesterday digest:', crossed)
print('\ntoday warm (<=10d) unpitched:', sorted(now_live, key=lambda x: -x[1]))
print('\ntoday 11-13d (freshly cold band):', sorted([(s, d) for s, d in now_cold if d and 10 < d <= 13], key=lambda x: -x[1]))

pitched = led.get('pitched', {})
print('\npitched rows and their page state today:')
for u in pitched:
    sl = u.rstrip('/').split('/journo-request/')[-1]
    v = ver.get(sl) or {}
    print('  ', sl[:60], '| days', v.get('days_old'), '| live', v.get('live'), '| pitched', pitched[u])
