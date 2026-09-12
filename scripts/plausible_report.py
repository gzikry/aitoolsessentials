#!/usr/bin/env python3
"""Read real AIToolsEssentials traffic from the Plausible v2 API.

Token lives at ~/.hermes/profiles/aitools/plausible_token (chmod 600). The value is
never printed. Use v2 (/api/v2/query); v1 returns stale/zero-filled data for this site.

Usage:
    python3 scripts/plausible_report.py                 # 30d summary
    python3 scripts/plausible_report.py --period 7d
    python3 scripts/plausible_report.py --markdown out.md
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

TOKEN_PATH = Path.home() / ".hermes" / "profiles" / "aitools" / "plausible_token"
SITE = "aitoolsessentials.com"
API = "https://plausible.io/api/v2/query"


def query(metrics: list[str], period: str = "30d",
          dimensions: list[str] | None = None,
          filters: list | None = None) -> dict:
    token = TOKEN_PATH.read_text().strip()
    payload: dict = {"site_id": SITE, "metrics": metrics, "date_range": period}
    if dimensions:
        payload["dimensions"] = dimensions
    if filters:
        payload["filters"] = filters
    result = subprocess.run(
        ["curl", "-sS", "-X", "POST", API,
         "-H", f"Authorization: Bearer {token}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload)],
        capture_output=True, text=True, timeout=90,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout[:300]}


def rows(response: dict) -> list[dict]:
    return response.get("results", []) or []


def metrics_of(response: dict) -> list:
    r = rows(response)
    return (r[0].get("metrics") if r else []) or []


def build_report(period: str) -> list[str]:
    out: list[str] = []
    agg = metrics_of(query(["visitors", "pageviews", "bounce_rate", "visit_duration"], period))
    visitors, pageviews = (agg + [0, 0])[:2]
    out.append(f"## Traffic ({period})")
    out.append("")
    out.append(f"- Visitors: **{visitors}**")
    out.append(f"- Pageviews: **{pageviews}**")
    if len(agg) >= 4:
        out.append(f"- Bounce rate: {agg[2]}% · avg visit {agg[3]}s")
    out.append("")

    out.append("### Top pages")
    out.append("")
    for row in rows(query(["visitors", "pageviews"], period, ["event:page"]))[:10]:
        page = row["dimensions"][0]
        v, p = (row["metrics"] + [0, 0])[:2]
        out.append(f"- {v}v / {p}pv — `{page}`")
    out.append("")

    out.append("### Sources")
    out.append("")
    for row in rows(query(["visitors"], period, ["visit:source"]))[:8]:
        src = row["dimensions"][0] or "(direct / none)"
        out.append(f"- {row['metrics'][0]}v — {src}")
    out.append("")

    out.append("### Conversion goals")
    out.append("")
    goals = [r for r in rows(query(["events"], period, ["event:name"]))
             if r["dimensions"][0] != "pageview"]
    if not goals:
        out.append("- (none recorded)")
    for row in sorted(goals, key=lambda r: -r["metrics"][0]):
        out.append(f"- {row['metrics'][0]} — `{row['dimensions'][0]}`")
    out.append("")

    # Stack Audit is the locked front door; report its funnel explicitly.
    audit = metrics_of(query(["visitors", "pageviews", "bounce_rate", "visit_duration"],
                             period, None, [["is", "event:page", ["/stack-audit.html"]]]))
    if audit and audit[0]:
        started = metrics_of(query(["events"], period, None,
                                   [["is", "event:name", ["stack_audit_started"]]]))
        done = metrics_of(query(["events"], period, None,
                                [["is", "event:name", ["stack_audit_completed"]]]))
        s = started[0] if started else 0
        d = done[0] if done else 0
        out.append("### Stack Audit funnel")
        out.append("")
        out.append(f"- Visitors to page: {audit[0]}")
        out.append(f"- Started: {s}")
        out.append(f"- Completed: {d}")
        if audit[0]:
            out.append(f"- Start rate: {s / audit[0] * 100:.0f}% · completion rate: {d / audit[0] * 100:.0f}%")
        out.append("")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--period", default="30d")
    parser.add_argument("--markdown")
    args = parser.parse_args()

    if not TOKEN_PATH.exists():
        print(f"Missing Plausible token at {TOKEN_PATH}", file=sys.stderr)
        return 2

    lines = build_report(args.period)
    text = "\n".join(lines)
    print(text)
    if args.markdown:
        Path(args.markdown).write_text(text + "\n")
        print(f"\nWrote {args.markdown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
