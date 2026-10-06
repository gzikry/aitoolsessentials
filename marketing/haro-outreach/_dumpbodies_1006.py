import json
D = '/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/'
b = json.load(open(D + '_bodies_1006.json'))
for sl, r in b.items():
    print('=' * 100)
    print(sl)
    print('  http', r['http'], '| badge', r['badge'], '| datePublished', r['datePublished'])
    print('  headline:', r['headline'])
    print('  author:', r['author'], '| domain:', r['domain'])
    print('  email_redacted:', r['email_redacted'], '| emails_on_page:', r['emails_on_page'])
    print('  published_links:', r['published_links'])
    print('  CORE:', r['core'][:1400].replace('\n', ' '))
    print()
