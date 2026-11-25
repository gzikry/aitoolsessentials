#!/usr/bin/env python3
"""Site cleanup P2: retired bands stay gone, scores stay hidden, folded pages redirect."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from legacy_redirects import CONSOLIDATED  # noqa: E402
from simplify_pages import RETIRED_BLOCKS, simplify  # noqa: E402

SCORE_TELLS = (
    'class="score-meter"',
    "/5 editorial",
    "<th>AIToolsEssentials editorial score</th>",
    "Choose with evidence, not hype.",
    '<section class="newsletter-panel"><div><span>AI Tool Evaluation Scorecard</span>',
)


def main() -> None:
    errors: list[str] = []
    marker = re.compile(r"<!-- AIT (" + "|".join(map(re.escape, RETIRED_BLOCKS)) + r") START -->")
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("admin/", "drafts/", "templates/", ".")) or "/node_modules/" in rel:
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in html:
            continue
        m = marker.search(html)
        if m:
            errors.append(f"{rel} still carries {m.group(1)}")
        for tell in SCORE_TELLS:
            if tell in html:
                errors.append(f"{rel} shows {tell!r}")
    for loser, winner, _title in CONSOLIDATED:
        html = (ROOT / loser).read_text(encoding="utf-8")
        if 'http-equiv="refresh"' not in html or f"/{winner}" not in html:
            errors.append(f"{loser} must redirect to /{winner}")

    sample = ('<!-- AIT VERDICT BAR START --><div>x</div><!-- AIT VERDICT BAR END -->'
              '<table><tr><th>Tool</th><th>Score</th></tr><tr><td>A</td><td>4.1/5</td></tr></table>')
    out = simplify(sample)
    if "VERDICT" in out or "4.1/5" in out or "<th>Score</th>" in out:
        errors.append("simplify() left a band or score column")
    if simplify(out) != out:
        errors.append("simplify() is not idempotent")

    if errors:
        raise SystemExit("\n".join(errors[:40]))
    print("simplified pages ok")


if __name__ == "__main__":
    main()
