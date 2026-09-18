#!/usr/bin/env python3
"""MX + domain sanity check for an outreach recipient domain (no shell pipes)."""
import json, sys, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"


def dns(name, rtype):
    url = "https://dns.google/resolve?" + urllib.parse.urlencode({"name": name, "type": rtype})
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/dns-json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def report(domain):
    out = {"domain": domain}
    for rtype in ("MX", "A", "NS"):
        try:
            d = dns(domain, rtype)
            answers = d.get("Answer") or []
            if rtype == "MX":
                out["MX"] = sorted(a["data"] for a in answers)
            elif rtype == "A":
                out["A"] = sorted(a["data"] for a in answers)
            else:
                out["NS"] = sorted(a["data"] for a in answers)
        except Exception as e:  # noqa: BLE001
            out[rtype] = f"ERROR {e}"
    out["has_mx"] = bool(out.get("MX"))
    return out


if __name__ == "__main__":
    for dom in sys.argv[1:]:
        print(json.dumps(report(dom), indent=1))
