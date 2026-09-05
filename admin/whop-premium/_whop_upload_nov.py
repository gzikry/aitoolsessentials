#!/usr/bin/env python3
import json, urllib.request, subprocess, os
WHOP = "/Users/georgezikry/.local/bin/whop"
os.environ["PATH"] = "/Users/georgezikry/.local/bin:/opt/homebrew/bin:/usr/bin:/bin"
os.chdir("/Users/georgezikry/aitoolessentials/site/admin/whop-premium")
files = [
  ("whop-posts-2026-11.md", "whop-posts-2026-11.md"),
  ("files/premium-tool-decision-matrix-2026-11.csv", "premium-tool-decision-matrix-2026-11.csv"),
  ("files/tool-change-alert-feed-2026-11.csv", "tool-change-alert-feed-2026-11.csv"),
  ("files/ai-stack-audit-template.csv", "ai-stack-audit-template.csv"),
  ("files/weekly-ai-stack-checklist.csv", "weekly-ai-stack-checklist.csv"),
  ("files/assistant-hands-on-comparison-2026-11.csv", "assistant-hands-on-comparison-2026-11.csv"),
  ("files/ai-roi-calculator-template.csv", "ai-roi-calculator-template.csv"),
]
out_rows = []
for path, name in files:
    r = subprocess.run(
        [WHOP, "files", "create", "--filename", name, "--visibility", "private", "--format", "json", "--full-output"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("CREATE FAIL", name, r.stderr or r.stdout)
        continue
    d = json.loads(r.stdout)["data"]
    url = d["upload_url"]
    headers = d.get("upload_headers") or {"Content-Type": "application/octet-stream"}
    data = open(path, "rb").read()
    req = urllib.request.Request(url, data=data, method="PUT")
    for k, v in headers.items():
        req.add_header(k, v)
    resp = urllib.request.urlopen(req)
    print(d["id"], name, "PUT", resp.status, "bytes", len(data))
    out_rows.append((d["id"], name))
open("/tmp/whop-new-ids.txt", "w").write("\n".join(f"{i}\t{n}" for i, n in out_rows) + "\n")
if out_rows:
    args = [WHOP, "files", "list"]
    for i, _ in out_rows:
        args += ["--file_ids", i]
    args += ["--format", "json"]
    r = subprocess.run(args, capture_output=True, text=True)
    d = json.loads(r.stdout)
    for x in d.get("data", []):
        print("READY" if x.get("upload_status") == "ready" else x.get("upload_status"), x["id"], x["filename"])
