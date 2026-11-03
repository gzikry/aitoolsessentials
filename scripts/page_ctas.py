#!/usr/bin/env python3
"""Free Stack Audit and Keep, Test, Cut blocks for generated pages.

Comparison generators and the article generators share templates/ so a rewrite
and this inject pass emit the same markup. The page-cta rules follow the
paper, ink, and flat button from the receipt redesign.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

AUDIT_S = "<!-- AIT FREE STACK AUDIT CTA START -->"
AUDIT_E = "<!-- AIT FREE STACK AUDIT CTA END -->"
SIGNUP_S = "<!-- AIT KEEPCUT SIGNUP START -->"
SIGNUP_E = "<!-- AIT KEEPCUT SIGNUP END -->"
RUN_S = "<!-- AIT RUN FREE AUDIT START -->"
RUN_E = "<!-- AIT RUN FREE AUDIT END -->"
_FORM = "<!-- FORM -->"


def _template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8").strip()


def free_stack_audit_cta() -> str:
    return _template("free-stack-audit-cta.html")


def run_free_audit_link() -> str:
    return _template("run-free-audit.html")


def keepcut_signup(root: Path | None = None) -> str:
    """Same workers.dev form as /subscribe/. A closed endpoint stays a mailto."""
    from newsletter_hold import subscribe_form

    root = root or ROOT
    endpoint = ""
    cfg = root / "data" / "newsletter.json"
    if cfg.is_file():
        endpoint = str(json.loads(cfg.read_text(encoding="utf-8")).get("subscribe_endpoint") or "")
    block = _template("keep-test-cut-signup.html")
    if _FORM not in block:
        raise ValueError("keep-test-cut-signup.html is missing the form placeholder")
    return block.replace(_FORM, subscribe_form(endpoint))


def _upsert(html: str, start: str, end: str, block: str) -> str:
    """Reprint the block immediately before </main>, after any related-reading list."""
    pattern = re.compile(r"\n?" + re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.S)
    html = pattern.sub("\n", html)
    if "</main>" not in html:
        return html
    return html.replace("</main>", block + "\n</main>", 1)


def _upsert_run(html: str, block: str) -> str:
    pattern = re.compile(re.escape(RUN_S) + r".*?" + re.escape(RUN_E), re.S)
    if pattern.search(html):
        return pattern.sub(lambda _match: block, html, count=1)
    subhead = re.search(r'<p class="subhead">.*?</p>', html, re.S)
    if subhead:
        return html[: subhead.end()] + "\n" + block + html[subhead.end() :]
    return _upsert(html, RUN_S, RUN_E, block)


def _live(html: str) -> bool:
    return 'http-equiv="refresh"' not in html and "</main>" in html


def inject(root: Path | None = None) -> dict[str, int]:
    """Put the audit CTA on every comparison page and the signup on every article."""
    root = Path(root or ROOT)
    audit = free_stack_audit_cta()
    signup = keepcut_signup(root)
    run = run_free_audit_link()
    stats = {
        "comparisons": 0,
        "articles": 0,
        "run_free_audit": 0,
        "comparison_pages": 0,
        "article_pages": 0,
    }
    for path in sorted((root / "comparisons").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if not _live(text):
            continue
        stats["comparison_pages"] += 1
        updated = _upsert(text, AUDIT_S, AUDIT_E, audit)
        if path.name == "best-ai-tools.html":
            updated = _upsert_run(updated, run)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            stats["comparisons"] += 1
            if path.name == "best-ai-tools.html":
                stats["run_free_audit"] = 1
    for path in sorted((root / "articles").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if not _live(text):
            continue
        stats["article_pages"] += 1
        updated = _upsert(text, SIGNUP_S, SIGNUP_E, signup)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            stats["articles"] += 1
    return stats


if __name__ == "__main__":
    print(inject())
