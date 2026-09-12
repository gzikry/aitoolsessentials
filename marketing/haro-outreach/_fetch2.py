#!/usr/bin/env python3
"""Sourcee fetcher v2 — parse the JSON-LD Article block (headline, description, date, author)."""
import subprocess, re, json, sys, os, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/_requests.json"


def get(url, timeout=30):
    raw = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                         capture_output=True, text=True).stdout
    return raw


def parse(raw):
    # JSON-LD Article fields
    def field(key):
        m = re.search(r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw)
        if not m:
            m = re.search(r'"' + key + r'":"((?:[^"\\]|\\.)*?)"', raw)
        if not m:
            return None
        return m.group(1).replace("\\\\n", "\n").replace("\\n", "\n").replace('\\"', '"').strip()

    headline = field("headline")
    desc = field("description")
    date = field("datePublished")
    author = field("name")
    if not headline:
        return {"status": "no_jsonld", "snippet": raw[:200]}
    return {"status": "ok", "headline": headline, "description": desc,
            "date_published": date, "author": author}


if __name__ == "__main__":
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    slugs = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    for slug in slugs:
        url = f"https://www.sourcee.app/journo-request/{slug}"
        raw = get(url)
        p = parse(raw)
        p["url"] = url
        res[slug] = p
        if p["status"] == "ok":
            print(f"=== {slug} [{p['date_published']}] by {p['author']}")
            print("HEADLINE:", p["headline"])
            print(p["description"])
        else:
            print(f"=== {slug} -> {p['status']}")
        print()
        time.sleep(1.2)
    json.dump(res, open(OUT, "w"), indent=1)
    print("saved", OUT)
