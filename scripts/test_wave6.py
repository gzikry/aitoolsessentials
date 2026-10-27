#!/usr/bin/env python3
"""Wave 6: Runway and Midjourney on the voice ledger, and paper utility pages."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UTILITY = (
    "submit-tool.html",
    "submit/index.html",
    "methodology/index.html",
    "pricing-watch/index.html",
    "legal/about.html",
    "advertise/index.html",
    "premium/index.html",
    "stack-audit.html",
    "newsletter/index.html",
    "price-changes/index.html",
    "categories/index.html",
    "tools/index.html",
    "comparisons/index.html",
    "articles/index.html",
    "guides/official/index.html",
    "compare/ai-video-avatar-cost/index.html",
)


def main() -> None:
    errors: list[str] = []
    proc = subprocess.run([sys.executable, "tests/test_price_voice.py"], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        errors.append(proc.stderr or proc.stdout or "priceVoice tests failed")

    cfg = json.loads((ROOT / "data" / "newsletter.json").read_text(encoding="utf-8"))
    if cfg.get("send_enabled") is not False:
        errors.append("send_enabled must stay false")

    home = (ROOT / "index.html").read_text(encoding="utf-8")
    if "ledger-page" in home:
        errors.append("homepage picked up ledger-page")

    voice = (ROOT / "compare" / "ai-video-avatar-cost" / "index.html").read_text(encoding="utf-8")
    for needle in (
        "Runway",
        "Midjourney",
        'id="voice-seconds"',
        "12 credits",
        "Stealth",
        'href="/go/runway/" rel="external noopener"',
        'href="/go/midjourney/" rel="external noopener"',
        "body class=\"ledger-page\"",
    ):
        if needle not in voice:
            errors.append(f"voice hub missing {needle}")
    if 'href="/go/runway/" rel="sponsored' in voice or 'href="/go/midjourney/" rel="sponsored' in voice:
        errors.append("runway or midjourney marked sponsored")
    if "\u2726" in voice:
        errors.append("voice hub still has a sparkle glyph")

    for rel in UTILITY:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing {rel}")
            continue
        html = path.read_text(encoding="utf-8")
        if "ledger-page" not in html:
            errors.append(f"{rel} missing ledger-page")
        if "\u2726" in html:
            errors.append(f"{rel} has a sparkle glyph")
        if "background:#000" in html.lower() or "background: #000" in html.lower():
            errors.append(f"{rel} has a #000 inline background")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"wave6 ok: {len(UTILITY)} utility pages")


if __name__ == "__main__":
    main()
