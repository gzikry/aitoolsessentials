import subprocess, re, json
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")


def get(url, headers=False):
    args = ["curl", "-sL", "-m", "30", "-A", UA]
    if headers:
        args += ["-D", "/tmp/hdr.txt"]
    args.append(url)
    r = subprocess.run(args, capture_output=True, text=True)
    hdr = ""
    if headers:
        try:
            hdr = Path("/tmp/hdr.txt").read_text(errors="ignore")
        except OSError:
            pass
    return r.stdout, hdr


res = {}

# 1. Where do the two lnkd.in links land?
for name, link in (("value_creation", "https://lnkd.in/eZkcsHTQ"),
                   ("ukraine", "https://lnkd.in/gZAm7f6d")):
    body, hdr = get(link, headers=True)
    loc = re.findall(r"(?im)^location:\s*(\S+)", hdr)
    res[name] = {"link": link, "location": loc, "bytes": len(body),
                 "calendly": sorted(set(re.findall(r"calendly\.com/[A-Za-z0-9_\-/]+", body)))[:4],
                 "title": (re.search(r"<title>(.*?)</title>", body, re.S).group(1).strip()[:120]
                           if re.search(r"<title>(.*?)</title>", body, re.S) else None)}
    print(name, "->", loc, res[name]["calendly"], "|", res[name]["title"])

# 2. marketintelligencetools contact page — the Amplemarket author's own reply route
for path in ("/contact", "/", "/about"):
    body, _ = get("https://marketintelligencetools.com" + path)
    es = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", body)
                    if not e.endswith((".png", ".jpg", ".svg", ".webp"))))
    li = sorted(set(re.findall(r"linkedin\.com/(?:in|company)/[A-Za-z0-9_\-]+", body)))
    res["mit" + path] = {"emails": es, "linkedin": li, "bytes": len(body)}
    print("MIT", path, "->", es[:5], li[:3])
    if path == "/contact":
        txt = re.sub(r"<script.*?</script>", " ", body, flags=re.S | re.I)
        txt = re.sub(r"<[^>]+>", " ", txt)
        txt = re.sub(r"\s+", " ", txt)
        m = re.search(r"(contact.{0,700})", txt, re.S | re.I)
        if m:
            res["mit_contact_text"] = m.group(1)[:700]
            print("   ", m.group(1)[:400])

Path("/tmp/route_res.json").write_text(json.dumps(res, indent=1))
