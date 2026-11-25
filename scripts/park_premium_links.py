#!/usr/bin/env python3
"""Premium is parked (Nov 24, 2026). Drop every link to a /premium/ page.

The /premium/ pages themselves are redirect stubs (see legacy_redirects.PREMIUM),
so an old bookmark still lands somewhere. This pass removes the buttons and
links that still pitch Premium on public pages. Redirect stubs are left alone.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_scope import is_public_rel

_LINK_RE = re.compile(
    r'\s*<a\b[^>]*\bhref="(?:https://aitoolsessentials\.com)?(?:/|(?:\.\./)+)?premium/[^"]*"[^>]*>.*?</a>(?:\s*[\u00b7|]\s*(?=<))?',
    re.S,
)
# The Premium Stripe checkout (premium_copy.STRIPE_PREMIUM_URL). The $497 audit checkout stays.
_CHECKOUT_RE = re.compile(
    r'\s*<a\b[^>]*\bhref="https://buy\.stripe\.com/bJe4gya2Bctf1lB02r0x203"[^>]*>.*?</a>',
    re.S,
)
# A list item or paragraph left empty once its only link is gone.
_EMPTY_RE = re.compile(r"<(li|p)\b[^>]*>\s*(?:[\u00b7|,]\s*)*</\1>")


def strip(text: str) -> str:
    updated = _CHECKOUT_RE.sub("", _LINK_RE.sub("", text))
    return _EMPTY_RE.sub("", updated)


def apply(root: Path) -> int:
    changed = 0
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not is_public_rel(rel) or rel.parts[0] == "premium":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in text or ("premium/" not in text and "bJe4gya2Bctf1lB02r0x203" not in text):
            continue
        updated = strip(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(apply(Path(__file__).resolve().parents[1]))
