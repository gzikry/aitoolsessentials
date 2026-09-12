#!/usr/bin/env python3
"""New extractor: Sourcee now serves a Next.js RSC flight payload, not <main> HTML."""
import subprocess, re, html, json, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def flight(url, timeout=30):
    raw = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                         capture_output=True, text=True).stdout
    chunks = re.findall(r'self\.__next_f\.push\(\[1,\s*("(?:[^"\\]|\\.)*")\]\)', raw)
    payload = ""
    for c in chunks:
        try:
            payload += json.loads(c)
        except Exception:
            pass
    return raw, payload


def clean(s):
    s = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", "\n", s)
    s = html.unescape(s)
    s = re.sub(r"\\n", "\n", s)
    s = re.sub(r"\\u003c", "<", s)
    s = re.sub(r"\\u003e", ">", s)
    lines = [l.strip() for l in s.split("\n") if l.strip()]
    # drop noisy ui chrome
    drop = {"Sign up", "Log in", "Log in with", "All publications →", "Search", "Home"}
    out = [l for l in lines if l not in drop and not l.startswith("{\\")]
    return "\n".join(out)


if __name__ == "__main__":
    url = sys.argv[1]
    raw, payload = flight(url)
    print("raw:", len(raw), "flight:", len(payload))
    txt = clean(payload)
    print(txt[:3000])
