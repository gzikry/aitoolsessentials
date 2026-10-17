#!/usr/bin/env python3
"""Content-hash cache busters on local stylesheets and shared scripts."""
from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))

from asset_rev import asset_link_errors, content_hash, stamp_html

ROOT = Path(__file__).resolve().parents[1]


def test_stamp_rewrites_local_assets_and_is_idempotent() -> None:
    with TemporaryDirectory() as raw:
        root = Path(raw)
        css = root / "css" / "styles.css"
        css.parent.mkdir()
        css.write_text("body{color:red}\n")
        script = root / "js" / "site.js"
        script.parent.mkdir()
        script.write_text("console.log(1)\n")
        page = root / "tools" / "index.html"
        page.parent.mkdir()
        page.write_text(
            '<link rel="stylesheet" href="../css/styles.css">'
            '<link rel="stylesheet" href="../css/styles.css?v=20260910a">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">'
            '<script src="/js/site.js" defer></script>'
            '<script src="https://example.com/app.js"></script>'
        )
        css_hash = content_hash(css)
        js_hash = content_hash(script)
        first = stamp_html(page.read_text(), page, root)
        second = stamp_html(first, page, root)
        if first != second:
            raise AssertionError("second stamp changed the page")
        page.write_text(first)
        expected_css = f'href="../css/styles.css?v={css_hash}"'
        if first.count(expected_css) != 2:
            raise AssertionError(first)
        if "v=20260910a" in first:
            raise AssertionError("stale query survived")
        if 'href="https://fonts.googleapis.com/css2?family=Inter"' not in first:
            raise AssertionError("external stylesheet was rewritten")
        if f'src="/js/site.js?v={js_hash}"' not in first:
            raise AssertionError(first)
        if 'src="https://example.com/app.js"' not in first:
            raise AssertionError("external script was rewritten")
        if asset_link_errors(root):
            raise AssertionError(asset_link_errors(root))
        doubled = (
            '<script src="/js/site.js?v=old" defer></script>'
            '<script src="/js/site.js" defer></script>'
        )
        once = stamp_html(doubled, page, root)
        again = stamp_html(once, page, root)
        if once != again:
            raise AssertionError("deduped stamp was not idempotent")
        if once.count("/js/site.js") != 1:
            raise AssertionError(once)


def test_public_assets_carry_the_current_hash() -> None:
    errors = asset_link_errors(ROOT)
    if errors:
        raise AssertionError("\n".join(errors))


def main() -> None:
    tests = (
        test_stamp_rewrites_local_assets_and_is_idempotent,
        test_public_assets_carry_the_current_hash,
    )
    errors: list[str] = []
    for test in tests:
        try:
            test()
        except Exception as exc:
            errors.append(test.__name__ + ": " + str(exc))
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
