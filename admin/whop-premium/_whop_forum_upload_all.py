#!/usr/bin/env python3
"""Upload Sep/Oct/Nov Whop forum packs. Never prints tokens."""
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
OUT = ROOT / "whop-created-forum-posts-2026-09-04.json"
os.environ["PATH"] = "/Users/georgezikry/.local/bin:/opt/homebrew/bin:/usr/bin:/bin"

# Attachments expected per post (filename -> used in backticks)
PACKS = [
    ("whop-posts-2026-09.md", "September"),
    ("whop-posts-2026-10.md", "October"),
    ("whop-posts-2026-11.md", "November"),
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r

def get_token():
    js = r'''
import { createRequire } from "node:module";
import { writeFileSync, chmodSync } from "node:fs";
const require = createRequire("/Users/georgezikry/.local/lib/node_modules/@whop/cli/dist/index.js");
const { Entry } = require("@napi-rs/keyring");
const secret = JSON.parse(new Entry("whop-cli", "georgezikry").getPassword());
const p = "/tmp/whop-oauth-token-cache";
writeFileSync(p, secret.accessToken, { mode: 0o600 });
chmodSync(p, 0o600);
process.stdout.write("ok");
'''
    r = run([NODE, "--input-type=module", "-e", js])
    if r.returncode != 0:
        raise SystemExit(f"KEYCHAIN_FAIL: {r.stderr or r.stdout}")
    if not TOKEN_PATH.exists():
        raise SystemExit("KEYCHAIN_FAIL: token file missing")
    return TOKEN_PATH.read_text().strip()

def clear_token():
    try:
        TOKEN_PATH.unlink(missing_ok=True)
    except Exception:
        pass

def api(method, path, token, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
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
    name = path.name
    r = run([WHOP, "files", "create", "--filename", name, "--visibility", "private", "--format", "json", "--full-output"])
    if r.returncode != 0:
        raise RuntimeError(f"files create failed {name}: {r.stderr or r.stdout}")
    d = json.loads(r.stdout)["data"]
    url = d["upload_url"]
    headers = d.get("upload_headers") or {"Content-Type": "application/octet-stream"}
    data = path.read_bytes()
    req = urllib.request.Request(url, data=data, method="PUT")
    for k, v in headers.items():
        req.add_header(k, v)
    urllib.request.urlopen(req)
    # poll ready
    for _ in range(20):
        r2 = run([WHOP, "files", "get", d["id"], "--format", "json"])
        meta = json.loads(r2.stdout)
        if "data" in meta:
            meta = meta["data"]
        if meta.get("upload_status") == "ready":
            return d["id"]
        time.sleep(0.4)
    return d["id"]

def parse_posts(md_text: str):
    chunks = re.split(r"\n## POST ", md_text)
    posts = []
    for chunk in chunks[1:]:
        lines = chunk.strip().splitlines()
        heading = lines[0].strip()
        # title after em dash or hyphen
        if "—" in heading:
            code, title = heading.split("—", 1)
            title = title.strip()
            full_title = f"{code.strip()} — {title}" if False else title
            # Prefer human title without N1 prefix for display? Keep full heading as title.
            title = heading  # "N1 — Pinned: ..."
        elif " - " in heading:
            title = heading
        else:
            title = heading
        body = "\n".join(lines[1:]).strip()
        # strip leading blank
        # attachments from backticks ending in .csv
        atts = re.findall(r"`([^`]+\.csv)`", body)
        # also Attach: lines
        posts.append({"heading": heading, "title": title, "content": body, "csv_names": list(dict.fromkeys(atts))})
    return posts

def pin_title(title: str) -> bool:
    t = title.lower()
    return "pinned" in t or "start here" in t or "welcome to premium" in t

def main():
    # verify forum
    token = get_token()
    try:
        status, data = api("GET", f"/forum_posts?experience_id={EXP}&first=5", token)
        if status == 400:
            raise SystemExit(f"NOT_FORUM: {data}")
        if status != 200:
            raise SystemExit(f"FORUM_LIST_FAIL http={status} body={data}")
        print(f"forum_ok exp={EXP} sample_count={len(data.get('data') or [])}")

        # Upload all CSVs we might need (fresh IDs)
        needed = set()
        pack_posts = []
        for fname, label in PACKS:
            md = (ROOT / fname).read_text()
            posts = parse_posts(md)
            for p in posts:
                p["pack"] = label
                p["source"] = fname
                needed.update(p["csv_names"])
            pack_posts.extend(posts)
            print(f"parsed {label}: {len(posts)} posts")

        file_ids = {}
        for name in sorted(needed):
            path = FILES / name
            if not path.exists():
                print(f"MISSING_CSV {name}")
                continue
            fid = upload_file(path)
            file_ids[name] = fid
            print(f"uploaded {name} -> {fid}")

        created = []
        pin_id = None
        for p in pack_posts:
            atts = []
            for n in p["csv_names"]:
                if n in file_ids:
                    atts.append({"id": file_ids[n]})
            body = {
                "experience_id": EXP,
                "title": p["title"][:200],
                "content": p["content"],
                "visibility": "members_only",
            }
            if atts:
                body["attachments"] = atts
            status, data = api("POST", "/forum_posts", token, body)
            post_id = None
            if status in (200, 201):
                post_id = (data.get("data") or data).get("id") or data.get("id")
            rec = {
                "pack": p["pack"],
                "source": p["source"],
                "title": p["title"],
                "http": status,
                "id": post_id,
                "attachments": [a["id"] for a in atts],
                "error": None if status in (200, 201) else data,
            }
            created.append(rec)
            print(f"POST {status} {p['title'][:60]} id={post_id} atts={len(atts)}")
            if post_id and pin_title(p["title"]) and pin_id is None:
                pin_id = post_id

        if pin_id:
            st, pdata = api("PATCH", f"/forum_posts/{pin_id}", token, {"is_pinned": True})
            print(f"PIN {st} {pin_id}")
            created.append({"action": "pin", "id": pin_id, "http": st, "error": None if st in (200, 201) else pdata})

        # list final
        st, listing = api("GET", f"/forum_posts?experience_id={EXP}&first=50", token)
        count = len(listing.get("data") or [])
        print(f"forum_list http={st} count={count}")
        OUT.write_text(json.dumps({"created": created, "file_ids": file_ids, "forum_count": count}, indent=2))
        print(f"wrote {OUT}")
    finally:
        clear_token()
        print("token_cleared")

if __name__ == "__main__":
    main()
