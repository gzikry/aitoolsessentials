#!/usr/bin/env python3
"""Site cleanup P3: banned-phrase lint for visible copy on every public page."""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from plain_copy import BANNED, plain_body, visible_text  # noqa: E402
from site_scope import is_public_rel  # noqa: E402


def main() -> None:
    hits: Counter[str] = Counter()
    where: dict[str, str] = {}
    pages = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if not is_public_rel(rel):
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in html:
            continue
        pages += 1
        text = visible_text(html)
        for phrase in BANNED:
            if phrase in text:
                hits[phrase] += 1
                where.setdefault(phrase, rel.as_posix())
    sample = '<body><p>Fast — and cheap</p><pre>a — b</pre><a>Guide — AIToolsEssentials</a></body>'
    out = plain_body(sample)
    errors = [f"{p!r} on {n} pages, e.g. {where[p]}" for p, n in hits.most_common()]
    if out != '<body><p>Fast, and cheap</p><pre>a — b</pre><a>Guide</a></body>':
        errors.append(f"plain_body() gave {out!r}")
    if plain_body(out) != out:
        errors.append("plain_body() is not idempotent")
    if errors:
        raise SystemExit("banned copy found:\n" + "\n".join(errors))
    print(f"plain copy ok: {pages} pages")


if __name__ == "__main__":
    main()
