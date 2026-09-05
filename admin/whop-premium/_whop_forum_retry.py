#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, subprocess, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path("/Users/georgezikry/aitoolessentials/site/admin/whop-premium")
FILES = ROOT / "files"
WHOP = "/Users/georgezikry/.local/bin/whop"
NODE = "/Users/georgezikry/.local/bin/node"
EXP = "exp_h66R9eZyc2jI4D"
API = "https://api.whop.com/api/v1"
TOKEN_PATH = Path("/tmp/whop-oauth-token-cache")
OUT = ROOT / "whop-created-forum-posts-2026-09-04-retry.json"
os.environ["PATH"] = "/Users/georgezikry/.local/bin:/opt/homebrew/bin:/usr/bin:/bin"

# Remaining posts to create: (md file, heading prefix match, csv list)
TODO = [
    ("whop-posts-2026-09.md", "2 — September brief", ["premium-tool-decision-matrix-2026-09.csv"]),
    ("whop-posts-2026-11.md", "N2 —", ["ai-stack-audit-template.csv", "ai-roi-calculator-template.csv", "premium-tool-decision-matrix-2026-11.csv"]),
    ("whop-posts-2026-11.md", "N3 —", ["weekly-ai-stack-checklist.csv"]),
    ("whop-posts-2026-11.md", "N4 —", ["tool-change-alert-feed-2026-11.csv"]),
    ("whop-posts-2026-11.md", "N5 —", ["assistant-hands-on-comparison-2026-11.csv"]),
    ("whop-posts-2026-11.md", "N6 —", []),
]

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def get_token():
    js = r'''
import { createRequire } from "node:module";
import { writeFileSync, chmodSync } from "node:fs";
const require = createRequire("/Users/georgezikry/.local/lib/node_modules/@whop/cli/dist/index.js");
const { Entry } = require("@napi-rs/keyring");
const secret = JSON.parse(new Entry("whop-cli", "georgezikry").getPassword());
writeFileSync("/tmp/whop-oauth-token-cache", secret.accessToken, { mode: 0o600 });
chmodSync("/tmp/whop-oauth-token-cache", 0o600);
process.stdout.write("ok");
'''
    r = run([NODE, "--input-type=module", "-e", js])
    if r.returncode != 0:
        raise SystemExit(f"KEYCHAIN_FAIL: {r.stderr or r.stdout}")
    return TOKEN_PATH.read_text().strip()

def clear_token():
    try:
        TOKEN_PATH.unlink(missing_ok=True)
    except Exception:
        pass

def api(method, path, token, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(API + path, data=data, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            j = json.loads(raw)
        except Exception:
            j = {"raw": raw[:500]}
        return e.code, j

def upload_file(path: Path):
    r = run([WHOP, "files", "create", "--filename", path.name, "--visibility", "private", "--format", "json", "--full-output"])
    d = json.loads(r.stdout)["data"]
    req = urllib.request.Request(d["upload_url"], data=path.read_bytes(), method="PUT")
    for k, v in (d.get("upload_headers") or {"Content-Type": "application/octet-stream"}).items():
        req.add_header(k, v)
    urllib.request.urlopen(req)
    for _ in range(25):
        meta = json.loads(run([WHOP, "files", "get", d["id"], "--format", "json"]).stdout)
        if "data" in meta:
            meta = meta["data"]
        if meta.get("upload_status") == "ready":
            return d["id"]
        time.sleep(0.5)
    return d["id"]

def parse_post(md_path: Path, prefix: str):
    text = md_path.read_text()
    chunks = re.split(r"\n## POST ", text)
    for chunk in chunks[1:]:
        lines = chunk.strip().splitlines()
        heading = lines[0].strip()
        if heading.startswith(prefix) or prefix in heading[:len(prefix)+5]:
            return heading, "\n".join(lines[1:]).strip()
    raise KeyError(prefix)

def main():
    print("sleeping 45s for rate limit…")
    time.sleep(45)
    token = get_token()
    created = []
    try:
        for md_name, prefix, csvs in TODO:
            title, content = parse_post(ROOT / md_name, prefix)
            atts = []
            for name in csvs:
                fid = upload_file(FILES / name)
                atts.append({"id": fid})
                print(f"fresh {name} -> {fid}")
                time.sleep(1)
            body = {
                "experience_id": EXP,
                "title": title[:200],
                "content": content,
                "visibility": "members_only",
            }
            if atts:
                body["attachments"] = atts
            # retry on rate limit
            for attempt in range(6):
                status, data = api("POST", "/forum_posts", token, body)
                if status == 400 and "rate limit" in json.dumps(data).lower():
                    wait = 30 * (attempt + 1)
                    print(f"rate limit on {title[:40]} wait {wait}s")
                    time.sleep(wait)
                    continue
                break
            post_id = None
            if status in (200, 201):
                post_id = (data.get("data") or data).get("id") or data.get("id")
            rec = {"title": title, "http": status, "id": post_id, "attachments": [a["id"] for a in atts], "error": None if status in (200, 201) else data}
            created.append(rec)
            print(f"POST {status} {title[:70]} id={post_id}")
            time.sleep(3)

        # pin November N1
        st, listing = api("GET", f"/forum_posts?experience_id={EXP}&first=50", token)
        posts = listing.get("data") or []
        nov = next((p for p in posts if "updated for November" in (p.get("title") or "") or (p.get("title") or "").startswith("N1")), None)
        if nov:
            pid = nov.get("id")
            st2, _ = api("PATCH", f"/forum_posts/{pid}", token, {"is_pinned": True})
            print(f"PIN_NOV {st2} {pid} title={nov.get('title')}")
            created.append({"action": "pin_nov", "id": pid, "http": st2})
        st3, listing2 = api("GET", f"/forum_posts?experience_id={EXP}&first=50", token)
        print(f"forum_count {len(listing2.get('data') or [])}")
        OUT.write_text(json.dumps({"created": created, "forum_count": len(listing2.get("data") or [])}, indent=2))
        print(f"wrote {OUT}")
    finally:
        clear_token()
        print("token_cleared")

if __name__ == "__main__":
    main()
