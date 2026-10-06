import json, os, glob

os.chdir('/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach')

def show(name):
    print('=' * 70)
    print(name)
    try:
        d = json.load(open(name))
    except Exception as e:
        print('ERR', e)
        return
    print(type(d).__name__)
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, list):
                print(' key:', k, 'LIST len', len(v))
                if v and isinstance(v[0], dict):
                    print('   sample keys:', list(v[0].keys()))
            elif isinstance(v, dict):
                print(' key:', k, 'DICT keys', list(v.keys())[:20])
            else:
                print(' key:', k, repr(v)[:200])
    elif isinstance(d, list):
        print(' len', len(d))
        if d and isinstance(d[0], dict):
            print(' sample keys:', list(d[0].keys()))
            print(' sample:', json.dumps(d[0], indent=1)[:1200])

show('digest-2026-10-05.json')
show('pitch-ledger.json')
show('ai-topic-feed.json')
