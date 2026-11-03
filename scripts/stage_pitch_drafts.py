#!/usr/bin/env python3
"""Stage a run's email pitches as Gmail drafts — never sends, and refuses to stage a stale figure.

Why this exists: every run since 2026-10-22 ended with paste-ready drafts and zero sends, and the
2026-10-28 run noted that a staged Gmail draft is "the one artefact no script re-reads" — drafts
48/49/50 sat in the mailbox for six days carrying the 99-tool / median $17.50 figures after the
dataset had moved to 105 tools / median $16.50, i.e. one click from sending a wrong number to a
journalist. Hand-copying the blockquote into `himalaya message save` each run is what let them drift.

This script reads the drafts straight out of `marketing/haro-outreach/pitch-drafts-<date>.md`:

  * the body is the `>` blockquote verbatim (no re-typing),
  * the recipient comes from the draft's own "Reply route" line,
  * the subject comes from the draft's own "**Subject:**" line,
  * and it REFUSES to stage anything whose text quotes a tool count or median that disagrees with
    `data/tools.json` / `data/pricing_snapshots.json` today.

Usage:
    python3 scripts/stage_pitch_drafts.py marketing/haro-outreach/pitch-drafts-2026-11-03.md
    python3 scripts/stage_pitch_drafts.py <file> --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
FROM = "AIToolsEssentials <aitoolsessentials@gmail.com>"
MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)


def figures() -> dict:
    snaps = json.loads((SITE_ROOT / "data/pricing_snapshots.json").read_text())
    tools = json.loads((SITE_ROOT / "data/tools.json").read_text())
    paid = {}
    for k, v in (snaps.get("snapshots") or {}).items():
        vals = [float(x) for x in MONTH.findall(v.get("digest") or "") if float(x) > 0]
        if vals:
            paid[k] = min(vals)
    return {"n_tools": len(tools), "n_paid": len(paid),
            "median": statistics.median(paid.values()) if paid else None,
            "updated": snaps.get("updated")}


def sections(md: str) -> list[dict]:
    """Split the drafts file into ## sections carrying a Subject, a Reply route and a quote block."""
    out = []
    for chunk in re.split(r"\n## ", md)[1:]:
        title = chunk.splitlines()[0].strip()
        subj = re.search(r"\*\*Subject[^*]*\*\*\s*`?([^`\n]+)`?", chunk)
        route = re.search(r"\*\*Reply route:\*\*\s*\*\*([^*]+)\*\*", chunk)
        body_lines, in_body = [], False
        for line in chunk.splitlines():
            if line.startswith("> "):
                in_body = True
                body_lines.append(line[2:])
            elif line.strip() == ">":
                in_body = True
                body_lines.append("")
            elif in_body:
                break
        if not (subj and route and body_lines):
            continue
        email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", route.group(1))
        out.append({"title": title, "subject": subj.group(1).strip(),
                    "to": email.group(0) if email else None,
                    "body": "\n".join(body_lines).strip()})
    return out


def stale_figure(d: dict, f: dict) -> str | None:
    """A draft that quotes today's tool count or median must quote today's numbers."""
    m = re.search(r"of the (\d{2,3}) AI tools", d["body"])
    if m and int(m.group(1)) != f["n_tools"]:
        return f"quotes {m.group(1)} tools, dataset holds {f['n_tools']}"
    m = re.search(r"median[^$]{0,40}\$(\d+(?:\.\d+)?)", d["body"])
    if m and f["median"] is not None and abs(float(m.group(1)) - f["median"]) > 0.005:
        return f"quotes median ${m.group(1)}, dataset yields ${f['median']:.2f}"
    return None


def save(d: dict) -> str:
    raw = (f"From: {FROM}\r\nTo: {d['to']}\r\nSubject: {d['subject']}\r\n"
           f"MIME-Version: 1.0\r\nContent-Type: text/plain; charset=\"utf-8\"\r\n"
           f"Content-Transfer-Encoding: 8bit\r\n\r\n{d['body']}\r\n")
    r = subprocess.run(["himalaya", "message", "save", "--account", "aitools",
                        "-f", "[Gmail]/Drafts"], input=raw, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"himalaya save failed: {r.stderr[-400:]}")
    return "saved"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    f = figures()
    ds = [d for d in sections(Path(a.file).read_text()) if d["to"]]
    if not ds:
        raise SystemExit("no draft with a published email address in that file — nothing to stage")

    bad = [(d["title"], why) for d in ds if (why := stale_figure(d, f))]
    if bad:
        for title, why in bad:
            print(f"REFUSED {title}: {why}")
        raise SystemExit("draft text disagrees with today's dataset — fix the draft, do not stage it")

    for d in ds:
        print(f"{a.file}: {d['title'][:60]} -> {d['to']} | {len(d['body'].split())} words")
        if a.dry_run:
            continue
        print("  ", save(d))
    print(f"\nfigures checked: {f['n_paid']} of {f['n_tools']} monthly-priced, median ${f['median']:.2f}, "
          f"snapshot {f['updated']} (nothing was sent — drafts only)")


if __name__ == "__main__":
    main()
