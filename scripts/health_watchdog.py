#!/usr/bin/env python3
"""Silent health watchdog for the scheduled cron job.

Watchdog contract: print NOTHING when healthy, print the report when unhealthy. Cron delivers
stdout verbatim, so empty output means no message reaches George at all.

Why a watchdog instead of an agent job
-------------------------------------
The previous version ran `validate_site.py` (which CI already runs on every push) and then had an
LLM restate "OK: 76 tools, 745 pages". That produced 30 near-identical daily messages and caught
nothing in a month, because a check that only re-runs a CI step cannot fail on a day with no commit.

What actually goes stale overnight, and is therefore worth waking someone for:

- **Pricing freshness** — records age past the freshness window by the passage of time alone.
  This is the site's core differentiator, and it degrades with no commit to trigger CI.
- **Coverage drift** — a review without a matching tool, or the reverse.
- **Required pages missing** — a page vanishes with no commit.
- **Secrets scan hits** — the repo is PUBLIC, so a committed credential is an immediate exposure.
- **Malformed/future-dated/duplicate pricing records.**

All of those come from `site_health.py`, which is a superset of validate_site.py for this purpose.

Exit codes are preserved from site_health.py so the scheduler can also see failure directly.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Run the health check. Silent on pass; full report on fail or on error."""
    md_path = Path("/tmp/site-health.md")
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "site_health.py"), "--markdown", str(md_path)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        print("AIToolsEssentials health check TIMED OUT after 300s.")
        print("The scheduled job did not complete. Investigate before trusting the site state.")
        return 1
    except Exception as exc:  # noqa: BLE001 - a watchdog must never crash silently
        print("AIToolsEssentials health check could not run.")
        print(f"{type(exc).__name__}: {exc}")
        return 1

    if proc.returncode == 0:
        # Healthy: say nothing at all. This is the whole point of the job.
        return 0

    # Unhealthy: emit every failed check, exactly as the script reported it.
    print("AIToolsEssentials automation health: FAIL")
    print()
    if md_path.exists():
        print(md_path.read_text().strip())
    else:
        print("Markdown report was not written; raw output follows.")
        print((proc.stdout or "").strip())
    if proc.stderr.strip():
        print()
        print("stderr:")
        print(proc.stderr.strip())
    return 1


if __name__ == "__main__":
    sys.exit(main())
