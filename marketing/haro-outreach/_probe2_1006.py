import json

D = '/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/'
d = json.load(open(D + 'digest-2026-10-05.json'))

print('SUMMARY:', d['summary'][:1500])
print()
print('HEALTH:', json.dumps(d['monitor_health'], indent=1))
print()
print('PLATFORMS:')
for p in d['platforms_checked']:
    print(' -', p['platform'], '|', p['status'], '|', p['notes'][:180])
print()
print('NEW THIS RUN:')
for x in d['new_this_run']:
    print(' -', json.dumps(x)[:300] if not isinstance(x, str) else x)
print()
print('EXPIRED THIS RUN:')
for x in d['expired_this_run']:
    print(' -', json.dumps(x)[:300] if not isinstance(x, str) else x)
print()
print('RECOMMENDED:')
for x in d['recommended_actions']:
    print(' -', x)
print()
print('DEFECTS FIXED:', json.dumps(d.get('monitor_defects_fixed_this_run'), indent=1))
