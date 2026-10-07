#!/usr/bin/env python3
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
d = json.loads((D / "pitch-ledger.json").read_text())
print("type", type(d))
if isinstance(d, dict):
    print("keys", list(d.keys())[:30])
    for k in list(d.keys())[:3]:
        print("---", k, "---")
        print(json.dumps(d[k], indent=1)[:1200])
elif isinstance(d, list):
    print("len", len(d))
    print(json.dumps(d[0], indent=1)[:1500])
