import json, re, glob, os
D = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
bodies = json.load(open(f"{D}/_bodies_0915.json"))
scan = json.load(open(f"{D}/_scan_0915.json"))

withtok = {k:v for k,v in bodies.items() if v.get("spend_tokens",0) > 0}
strong = {k:v for k,v in bodies.items() if v.get("strong")}
print("bodies fetched:", len(bodies), "| missing headline:", sum(1 for v in bodies.values() if not v.get("headline")))
print("with ANY spend token:", len(withtok))
print("with STRONG spend signal:", len(strong))
for k,v in sorted(strong.items(), key=lambda x: x[1]["datePublished"]):
    print("  ", v["datePublished"], "|", v["headline"], "|", v["spend_hits"])

# AI-token slugs newly indexed since the 2026-09-14T09:00 run marker
tight = {k:v for k,v in scan["ai"].items() if v >= "2026-09-14T09:00:00"}
print("\nAI-token slugs new since 09-14T09:00:", len(tight))
for k in sorted(tight, key=lambda k: tight[k], reverse=True):
    b = bodies.get(k, {})
    print("  ", tight[k], k, "| strong:", b.get("strong"), "| tok:", b.get("spend_tokens"))

# digest appearance counts (excluding today)
digests = sorted(glob.glob(f"{D}/digest-*.json"))
print("\ndigest files:", [os.path.basename(d) for d in digests][-6:])
