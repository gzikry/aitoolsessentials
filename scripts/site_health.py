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
    "pricing-watch", "guides/switch-guides", "model-lineups", "workflows", "decision-brief.html", "stack-builder.html",
    "cost-calculator.html", "compare-shortlist.html", "stack-audit.html",
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
    if not isinstance(s, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", s): return None
    try: return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception: return None

def run(root: Path) -> dict:
    tools=load_json(root/"data/tools.json")
    source_data=load_json(root/"data/tool_sources.json")
    if not isinstance(source_data, dict) or not isinstance(source_data.get("tools"), list):
        raise ValueError("data/tool_sources.json must contain a tools list")
    malformed_sources=[]
    valid_source_records=[]
    source_slugs=[]
    for i, item in enumerate(source_data["tools"]):
        if not isinstance(item, dict) or not isinstance(item.get("slug"), str) or not item.get("slug"):
            malformed_sources.append(i)
        else:
            valid_source_records.append(item)
            source_slugs.append(item["slug"])
    duplicate_source_slugs=sorted({slug for slug in source_slugs if source_slugs.count(slug) > 1})
    today=date.today()
    html=list(root.rglob("*.html"))
    reviews=list((root/"tools").glob("*/index.html"))
    missing=[p for p in REQUIRED if not (root/p if p.endswith('.html') else root/p/"index.html").exists()]
    slugs={t.get("slug") for t in tools}
    review_slugs={p.parent.name for p in reviews}
    pricing_dates=[iso(x.get("pricing_checked_date","")) for x in valid_source_records]
    pricing_dates=[x for x in pricing_dates if x]
    latest=max(pricing_dates, default=None)
    stale=[]
    future=[]
    invalid=[]
    for x in valid_source_records:
        raw=x.get("pricing_checked_date", "")
        if not raw or iso(raw) is None:
            invalid.append(x["slug"])
    invalid.sort()
    if latest:
        for x in valid_source_records:
            checked=iso(x.get("pricing_checked_date",""))
            if checked and checked < latest:
                stale.append(x["slug"])
            if checked and checked > today:
                future.append(x["slug"])
        stale.sort(); future.sort()
    secret_hits=[]
    for p in root.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.suffix in {".png",".jpg",".jpeg",".gif",".pdf",".woff",".woff2"}: continue
        try: text=p.read_text(errors="ignore")
        except Exception: continue
        if any(rx.search(text) for rx in SECRET_PATTERNS): secret_hits.append(str(p.relative_to(root)))
    checks={
      "required_pages": {"ok": not missing, "missing": missing},
      "coverage": {"ok": slugs==review_slugs, "tools":len(slugs), "reviews":len(review_slugs), "missing_reviews":sorted(slugs-review_slugs), "orphan_reviews":sorted(review_slugs-slugs)},
      "pricing_freshness": {"ok": not malformed_sources and not duplicate_source_slugs and not invalid and not future, "latest_recorded_date": latest.isoformat() if latest else None, "older_than_latest": stale, "undated_or_invalid": invalid, "future_dated": future, "malformed_records": malformed_sources, "duplicate_slugs": duplicate_source_slugs},
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
    if c['pricing_freshness']['undated_or_invalid'] or c['pricing_freshness']['future_dated'] or c['pricing_freshness']['malformed_records'] or c['pricing_freshness']['duplicate_slugs']:
        lines += ["## Pricing evidence anomalies", *[f"- Undated or invalid: `{x}`" for x in c['pricing_freshness']['undated_or_invalid']], *[f"- Future-dated: `{x}`" for x in c['pricing_freshness']['future_dated']], *[f"- Malformed record index: `{x}`" for x in c['pricing_freshness']['malformed_records']], *[f"- Duplicate slug: `{x}`" for x in c['pricing_freshness']['duplicate_slugs']], ""]
    if c['secrets_scan']['hits']: lines += ["## Potential secret hits", *[f"- `{x}`" for x in c['secrets_scan']['hits']], ""]
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument("--json",type=Path); ap.add_argument("--markdown",type=Path); args=ap.parse_args()
    report=run(args.root); print(json.dumps(report,indent=2))
    if args.json: args.json.write_text(json.dumps(report,indent=2)+"\n")
    if args.markdown: args.markdown.write_text(markdown(report))
    sys.exit(0 if report["status"]=="pass" else 1)
if __name__=="__main__": main()
