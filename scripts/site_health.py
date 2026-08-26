#!/usr/bin/env python3
"""Fast, dependency-free operational health check for AIToolsEssentials.

This is intentionally read-only unless --json/--markdown output paths are supplied.
It complements validate_site.py with operational checks useful in CI and scheduled runs.
"""
from __future__ import annotations
import argparse, json, re, sys
from datetime import date, datetime
from pathlib import Path

REQUIRED = [
    "fit-interview", "confidence-check", "change-radar", "evidence", "methodology",
    "pricing-watch", "guides/switch-guides", "decision-brief.html", "stack-builder.html",
    "cost-calculator.html", "compare-shortlist.html",
]
SECRET_PATTERNS = [
    re.compile(r"(?:sk|rk|pk)-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"xai-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AIza[A-Za-z0-9_-]{30,}"),
]

def load_json(path: Path):
    return json.loads(path.read_text())

def iso(s):
    try: return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception: return None

def run(root: Path) -> dict:
    tools=load_json(root/"data/tools.json")
    source_data=load_json(root/"data/tool_sources.json")
    sources={x["slug"]:x for x in source_data["tools"]}
    today=date.today()
    html=list(root.rglob("*.html"))
    reviews=list((root/"tools").glob("*/index.html"))
    missing=[p for p in REQUIRED if not (root/p if p.endswith('.html') else root/p/"index.html").exists()]
    slugs={t.get("slug") for t in tools}
    review_slugs={p.parent.name for p in reviews}
    pricing_dates=[iso(x.get("pricing_checked_date","")) for x in sources.values()]
    pricing_dates=[x for x in pricing_dates if x]
    latest=max(pricing_dates, default=None)
    stale=[]
    if latest:
        for x in sources.values():
            checked=iso(x.get("pricing_checked_date",""))
            if checked and checked < latest:
                stale.append(x["slug"])
        stale.sort()
    secret_hits=[]
    for p in root.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.suffix in {".png",".jpg",".jpeg",".gif",".pdf",".woff",".woff2"}: continue
        try: text=p.read_text(errors="ignore")
        except Exception: continue
        if any(rx.search(text) for rx in SECRET_PATTERNS): secret_hits.append(str(p.relative_to(root)))
    checks={
      "required_pages": {"ok": not missing, "missing": missing},
      "coverage": {"ok": slugs==review_slugs, "tools":len(slugs), "reviews":len(review_slugs), "missing_reviews":sorted(slugs-review_slugs), "orphan_reviews":sorted(review_slugs-slugs)},
      "pricing_freshness": {"ok": True, "latest_recorded_date": latest.isoformat() if latest else None, "older_than_latest": stale},
      "secrets_scan": {"ok": not secret_hits, "hits": secret_hits},
      "generated_output": {"html_pages":len(html), "fit_interview":(root/"fit-interview/index.html").exists(), "change_radar_rows":(root/"change-radar/index.html").read_text().count('class="radar-row"') if (root/"change-radar/index.html").exists() else 0},
    }
    ok=all(v.get("ok",True) for v in checks.values())
    return {"status":"pass" if ok else "fail", "checked_at":datetime.now().isoformat(timespec="seconds"), "checks":checks}

def markdown(report):
    c=report["checks"]
    lines=[f"# AIToolsEssentials automation health: {report['status'].upper()}","",f"Checked: {report['checked_at']}","",f"- HTML pages: {c['generated_output']['html_pages']}",f"- Tools/reviews: {c['coverage']['tools']}/{c['coverage']['reviews']}",f"- Latest recorded pricing date: {c['pricing_freshness']['latest_recorded_date']}",f"- Change Radar rows: {c['generated_output']['change_radar_rows']}",""]
    if c['required_pages']['missing']: lines += ["## Missing pages", *[f"- `{x}`" for x in c['required_pages']['missing']], ""]
    if c['coverage']['missing_reviews']: lines += ["## Missing reviews", *[f"- `{x}`" for x in c['coverage']['missing_reviews']], ""]
    if c['pricing_freshness']['older_than_latest']: lines += ["## Older pricing records", *[f"- `{x}`" for x in c['pricing_freshness']['older_than_latest']], ""]
    if c['secrets_scan']['hits']: lines += ["## Potential secret hits", *[f"- `{x}`" for x in c['secrets_scan']['hits']], ""]
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument("--json",type=Path); ap.add_argument("--markdown",type=Path); args=ap.parse_args()
    report=run(args.root); print(json.dumps(report,indent=2))
    if args.json: args.json.write_text(json.dumps(report,indent=2)+"\n")
    if args.markdown: args.markdown.write_text(markdown(report))
    sys.exit(0 if report["status"]=="pass" else 1)
if __name__=="__main__": main()
