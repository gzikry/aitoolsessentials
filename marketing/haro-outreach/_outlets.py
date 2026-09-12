#!/usr/bin/env python3
"""Fetch Sourcee outlet pages (Forbes, FT, TechCrunch, etc.) via JSON-LD + flight strings."""
import subprocess, re, json, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

OUTLETS = sys.argv[1:] or ["forbes", "financial-times", "techcrunch", "business-insider",
                           "the-guardian", "wall-street-journal", "fast-company", "wired"]

for o in OUTLETS:
    url = f"https://www.sourcee.app/media-outlets/{o}/journo-requests"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    # titles appear as escaped JSON strings in the flight payload
    titles = re.findall(r'\\"(?:title|headline)\\":\\"((?:[^"\\]|\\.){10,200}?)\\"', raw)
    slugs = sorted(set(re.findall(r'/journo-request/([a-z0-9\-]{8,120})', raw)))
    print(f"=== {o} | html {len(raw)} | titles {len(titles)} | slugs {len(slugs)}")
    for t in titles[:20]:
        print("   T:", t[:150])
    for s in slugs[:25]:
        print("   S:", s)
    print()
