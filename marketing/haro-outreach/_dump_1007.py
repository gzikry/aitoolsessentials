#!/usr/bin/env python3
import json, re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
b = json.loads((D / "_bodies_1007.json").read_text())
for sl, r in b.items():
    print("=" * 100)
    print("SLUG:", sl)
    print("http:", r["http"], "| badge:", r["badge"], "| datePublished:", r["datePublished"])
    print("headline:", r["headline"])
    print("author:", r["author"], "| domain:", r["domain"])
    print("emails_on_page:", r["emails_on_page"], "| email_redacted:", r["email_redacted"])
    print("published_links:", r["published_links"])
    core = re.sub(r"\s+", " ", r["core"])
    print("BODY:", core[:1400])
    print()
