#!/usr/bin/env python3
"""Post-refresh sanity read: cached count, the Forbes row's route fields, and checked dates."""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
d = json.loads((D / "verified-requests.json").read_text())
print("cached", len(d))
k = "founders-cutting-ai-use-eliminating-or-reducing-ai-in-business"
print(k, "| links:", d[k]["published_links"], "| emails:", d[k]["emails_on_page"],
      "| redacted:", d[k]["email_redacted"], "| checked:", d[k]["checked"])
print("checked dates across cache:", sorted({v.get("checked") for v in d.values()}))
