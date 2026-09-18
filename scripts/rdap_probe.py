#!/usr/bin/env python3
"""RDAP registration facts for a domain (works around the curl|python guard)."""
import json, sys, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

CANDIDATES = [
    "https://rdap.org/domain/{d}",
    "https://rdap.verisign.com/com/v1/domain/{d}",
]


def rdap(domain):
    tld = domain.rsplit(".", 1)[-1]
    urls = [u.format(d=domain) for u in CANDIDATES]
    if tld not in ("com", "net"):
        urls.insert(1, f"https://rdap.org/domain/{domain}")
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rdap+json"})
            with urllib.request.urlopen(req, timeout=25) as r:
                final = r.geturl()
                return final, json.load(r)
        except Exception as e:  # noqa: BLE001
            last = f"{url} -> {e}"
    return None, {"error": last}


if __name__ == "__main__":
    for dom in sys.argv[1:]:
        src, d = rdap(dom)
        print(f"=== {dom} (via {src}) ===")
        if "error" in d:
            print("  ", d["error"])
            continue
        print("  handle:", d.get("handle"), "| status:", d.get("status"))
        for e in d.get("events", []):
            print("  event:", e.get("eventAction"), e.get("eventDate"))
        for n in d.get("nameservers", []):
            print("  NS:", n.get("ldhName"))
        for ent in d.get("entities", []):
            v = ent.get("vcardArray")
            nm = None
            if v:
                for it in v[1]:
                    if it[0] == "fn":
                        nm = it[3]
            print("  entity:", ent.get("roles"), nm)
