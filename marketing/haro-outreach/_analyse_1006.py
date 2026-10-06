import json, re
from pathlib import Path
from datetime import date, datetime, timezone

D = Path('/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach')
TODAY = '2026-10-06'

prev = json.loads((D / 'digest-2026-10-05.json').read_text())
ver = json.loads((D / 'verified-requests.json').read_text())
led = json.loads((D / 'pitch-ledger.json').read_text())
win = json.loads((D / '_window_1006.json').read_text())
feed = set(json.loads((D / 'ai-topic-feed.json').read_text())['slugs'])

sitemap = (D / '_sitemap_1006.xml').read_text()
sm = set(re.findall(r'<loc>[^<]*?/journo-request/([a-z0-9\-]+)</loc>', sitemap))
print('sitemap slugs:', len(sm), '| AI feed slugs:', len(feed))

pitched = set(led.get('pitched', {}))
skipped = set(led.get('skipped', {}))

rows = []
for o in prev['opportunities']:
    u = o['url']
    sl = u.rstrip('/').split('/journo-request/')[-1]
    v = ver.get(sl) or {}
    rows.append({
        'slug': sl, 'url': u, 'rel': o.get('relevance'),
        'days': v.get('days_old'), 'live': v.get('live'), 'http': v.get('http'),
        'badge': v.get('badge'), 'feed': sl in feed, 'sitemap': sl in sm,
        'checked': v.get('checked'), 'emails': v.get('emails_on_page'),
        'hints': v.get('reply_hints'), 'links': v.get('published_links'),
        'redacted': v.get('email_redacted'), 'deadline': (o.get('deadline') or '')[:120],
    })

print('\ntracked rows (from 2026-10-05 digest):', len(rows))
print('checked today:', sum(1 for r in rows if r['checked'] == TODAY))
print('live:', sum(1 for r in rows if r['live']))
print('in sitemap:', sum(1 for r in rows if r['sitemap']))
print('in AI topic feed:', sum(1 for r in rows if r['feed']))
print('NOT in sitemap (dropped):', [r['slug'] for r in rows if not r['sitemap']])
print('pitched:', len(pitched), '| skipped:', len(skipped))

unp = [r for r in rows if r['url'] not in pitched and r['url'] not in skipped]
print('\nunpitched:', len(unp), '| live unpitched:', sum(1 for r in unp if r['live']))
cold = [r for r in unp if r['live'] and (r['days'] is None or r['days'] > 10)]
warm = [r for r in unp if r['live'] and r['days'] is not None and r['days'] <= 10]
print('live unpitched cold (>10d):', len(cold), '| live unpitched warm (<=10d):', len(warm))

print('\n--- live unpitched, sorted oldest -> newest ---')
for r in sorted(unp, key=lambda x: -(x['days'] or 0)):
    print(f"  {str(r['days']):>5}d  {r['rel']:<12} feed={'Y' if r['feed'] else 'n'} "
          f"email={r['emails'] or '-'} hints={r['hints']} :: {r['slug'][:62]}")
