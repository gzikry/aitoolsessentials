import json, os
OUT="/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
d=json.load(open(f"{OUT}/digest-2026-09-14.json"))
req=["date","platforms_checked","opportunities","previously_reported_still_relevant",
     "new_this_run","expired_this_run","summary","recommended_actions"]
print("required keys present:", all(k in d for k in req), "| missing:", [k for k in req if k not in d])
print("platforms checked:", len(d["platforms_checked"]), "->", [p["platform"] for p in d["platforms_checked"]])
print("opportunities:", len(d["opportunities"]), "->", [o.get("journalist_publication") for o in d["opportunities"]])
for o in d["opportunities"]:
    for f in ["query_text","journalist_publication","category","deadline","contact_method","relevance","suggested_pitch_template","url"]:
        assert o.get(f), (o["id"], f)
print("all opportunity fields populated: OK")
print("previously_reported:", len(d["previously_reported_still_relevant"]))
print("new_this_run items:", len(d["new_this_run"]))
print("expired:", len(d["expired_this_run"]))
print("recommended_actions:", len(d["recommended_actions"]))
print("monitor_health:", d["monitor_health"]["status"])
print("\nfile bytes:", os.path.getsize(f"{OUT}/digest-2026-09-14.json"))
print("carry counts (grep across digests):")
for s in ["anthropic-users","amplemarket","business-and-technology-leaders","ceos-ai-impact","edtech-product-managers"]:
    n=len(os.popen(f"grep -l {s} {OUT}/digest-*.json").read().split())
    print(f"   {s}: {n}")
