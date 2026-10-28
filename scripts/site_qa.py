#!/usr/bin/env python3
"""Local QA entry for the calculator hubs, submit lanes, and the send hold."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []
    cfg = json.loads((ROOT / "data" / "newsletter.json").read_text(encoding="utf-8"))
    if cfg.get("send_enabled") is not False:
        errors.append("data/newsletter.json send_enabled must stay false")
    for script in (
        "scripts/test_app_builder_hub.py",
        "scripts/test_coding_assistant_hub.py",
        "scripts/test_submit_alias.py",
        "scripts/test_newsletter_archive.py",
        "scripts/test_wave4.py",
        "scripts/test_wave5.py",
        "scripts/test_wave6.py",
        "scripts/test_spend_calculators.py",
        "scripts/test_customer_support_calc.py",
    ):
        proc = subprocess.run([sys.executable, script], cwd=ROOT)
        if proc.returncode:
            errors.append(script)
    if errors:
        raise SystemExit("\n".join(errors))
    print("site qa ok")


if __name__ == "__main__":
    main()
