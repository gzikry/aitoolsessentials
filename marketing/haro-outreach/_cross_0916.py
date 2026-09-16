import json, re, subprocess, time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
feed = json.loads((D / "_feed_0916.json").read_text())
meta = json.loads((D / "_meta_0916.json").read_text())

feed_slugs = set(feed)
print("live AI topic feed slugs:", len(feed_slugs))
print()
print("=== Is each queued/carried slug in the CURRENT AI topic feed? ===")
for sl, rec in sorted(meta.items()):
    inn = "IN-FEED" if sl in feed_slugs else "NOT-IN-FEED"
    print(f"{inn:<12} pub={str(rec['datePublished'])[:10]}  {sl}")
print()
# Which feed slugs carry any AI-spend signal at all
print("=== feed slugs with 1+ spend token ===")
for sl, r in feed.items():
    if r["spend_tokens"]:
        print(f"  tok={len(r['spend_tokens'])} {sl[:70]} {r['spend_tokens']}")
