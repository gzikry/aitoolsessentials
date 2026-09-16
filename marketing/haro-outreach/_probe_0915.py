import subprocess, re, json, os

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"

def probe(url, timeout=30):
    r = subprocess.run(["curl","-sL","-m",str(timeout),"-o","/tmp/p_body","-w","%{http_code} %{size_download} %{url_effective}","-A",UA,url],
                       capture_output=True, text=True)
    code, size, eff = (r.stdout.split(" ",2) + ["","",""])[:3]
    body = ""
    try:
        body = open("/tmp/p_body","r",errors="ignore").read()
    except Exception:
        pass
    t = re.search(r"<title[^>]*>(.*?)</title>", body, re.S|re.I)
    title = (t.group(1).strip()[:140] if t else "")
    return {"url": url, "http": code, "bytes": size, "effective": eff, "title": title,
            "has_journo": "journo-request" in body.lower(), "sample": body[:300].replace("\n"," ")}

targets = [
    "https://www.helpareporter.com/",
    "https://www.helpareporter.com/view-queries",
    "https://www.connectively.us/",
    "https://www.connectively.us/queries",
    "https://app.qwoted.com/requests",
    "https://mentionmatch.com/",
    "https://www.mentionmatch.com/",
    "https://www.sourceofsources.com/",
    "https://www.sourceofsources.com/requests",
    "https://medialyst.ai/api/mcp",
]

out = {}
for t in targets:
    try:
        out[t] = probe(t)
    except Exception as e:
        out[t] = {"url": t, "error": str(e)}

json.dump(out, open("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/_probe_0915.json","w"), indent=1)
for k,v in out.items():
    print(k, "->", v.get("http"), v.get("bytes"), "|", v.get("title"), "| journo=", v.get("has_journo"))
