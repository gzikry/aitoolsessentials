#!/usr/bin/env python3
"""Paper ledger chrome and calculator callouts for tool and comparison pages.

Generators rewrite <body> on every pass. This runs after them, and before the
asset hash stamp, so the class and the callout survive a second pipeline run.
The homepage stays off body.ledger-page. Utility pages, including premium,
the voice calculator, and the articles index, get the class and no callout.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

MARK_S = "<!-- AIT CALCULATOR CALLOUT START -->"
MARK_E = "<!-- AIT CALCULATOR CALLOUT END -->"
BLOCK_RE = re.compile(re.escape(MARK_S) + r".*?" + re.escape(MARK_E), re.S)
BODY_RE = re.compile(r"<body([^>]*)>", re.I)
THEME_RE = re.compile(r'(<meta name="theme-color" content=")#5e6ad2(")', re.I)
HERO_RE = re.compile(
    r'<section\b[^>]*class="[^"]*(?:review-hero|scene-dark)[^"]*"[^>]*>.*?</section>',
    re.S | re.I,
)
MAIN_RE = re.compile(r"<main[^>]*>", re.I)
PHRASE = "Run the numbers in the interactive calculator →"
CREDIT = "/pricing-watch/credit-traps/"
AUDIT = "/stack-audit.html"

HUBS = {
    "coding": ("/compare/ai-coding-assistants/", "AI coding assistant cost ledger"),
    "apps": ("/compare/ai-app-builders/", "AI app-builder credit burn ledger"),
    "voice": ("/compare/ai-video-avatar-cost/", "voice and video minute cost ledger"),
    "auto": ("/compare/automation-task-calculator/", "automation task burn ledger"),
    "deck": ("/compare/ai-presentation-cost/", "presentation and deck cost ledger"),
}
SLUG_HUB = {
    "cursor": "coding",
    "github-copilot": "coding",
    "claude-command-center": "coding",
    "v0": "apps",
    "bolt-new": "apps",
    "lovable": "apps",
    "replit-ai": "apps",
    "gamma": "deck",
    "canva-ai": "deck",
    "htmlslides": "deck",
    "microsoft-copilot": "deck",
    "make": "auto",
    "n8n": "auto",
    "zapier-ai": "auto",
    "browse-ai": "auto",
    "whop-cli": "auto",
    "elevenlabs": "voice",
    "descript": "voice",
    "heygen": "voice",
    "synthesia": "voice",
    "runway": "voice",
    "midjourney": "voice",
}
CATEGORY_HUB = {
    "Automation": "auto",
    "Video": "voice",
    "Audio & Video": "voice",
}
ALIASES = {"zapier": "zapier-ai", "otter": "otter-ai", "copilot": "github-copilot"}
UTILITY_PAGES = frozenset({
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
    "articles/index.html",
    "compare/ai-video-avatar-cost/index.html",
})
DARK_INLINE = re.compile(r"(background(?:-color)?\s*:\s*)#000(?:000)?\b", re.I)


def _catalog(root: Path) -> dict[str, dict]:
    tools = json.loads((root / "data" / "tools.json").read_text(encoding="utf-8"))
    return {tool["slug"]: tool for tool in tools}


def _hub_key(slug: str, by_slug: dict[str, dict]) -> str | None:
    slug = ALIASES.get(slug, slug)
    if slug in SLUG_HUB:
        return SLUG_HUB[slug]
    tool = by_slug.get(slug)
    if not tool:
        return None
    return CATEGORY_HUB.get(tool.get("category"))


def _links(*hrefs: str) -> str:
    credit = f'<a href="{CREDIT}">credit expiry and locks</a>'
    audit = f'<a href="{AUDIT}">free stack audit</a>'
    return credit, audit


def _aside(primary: str, sentence: str, extra: str = "") -> str:
    extra_block = f"\n{extra}" if extra else ""
    return (
        f"{MARK_S}\n"
        '<aside class="ledger-calc-callout">\n'
        '<p class="ledger-kicker">Interactive ledger</p>\n'
        f'<p><a href="{primary}">{PHRASE}</a></p>\n'
        f"<p>{sentence}</p>{extra_block}\n"
        "</aside>\n"
        f"{MARK_E}"
    )


def _directory_callout() -> str:
    items = "\n".join(
        f'<li><a href="{href}">{label}</a></li>' for href, label in HUBS.values()
    )
    credit, audit = _links()
    return _aside(
        CREDIT,
        "Seat math on this page depends on the job. Open the calculator that matches it, "
        f"then read {credit} and run the {audit}.",
        f'<ul class="ledger-calc-links">\n{items}\n</ul>',
    )


def _hub_sentence(key: str, others: list[str]) -> str:
    _href, label = HUBS[key]
    credit, audit = _links()
    crossed = ""
    if others:
        bits = ", ".join(f'<a href="{HUBS[item][0]}">{HUBS[item][1]}</a>' for item in others)
        crossed = f" This page also crosses {bits}."
    return f"The {label} uses the checked prices.{crossed} Also see {credit} and run the {audit}."


def _fallback_sentence(kind: str) -> str:
    credit, audit = _links()
    subject = "this tool" if kind == "tool" else "this matchup"
    return (
        f"Checked prices for {subject} are on the credit-trap ledger. "
        f"See {credit} and run the {audit}."
    )


def _callout(kind: str, path: Path, by_slug: dict[str, dict]) -> str | None:
    if kind in {"guide", "category", "tool-index", "utility"}:
        return None
    if kind == "comparison-index" or path.name == "best-ai-tools.html":
        return _directory_callout()
    if kind == "tool":
        key = _hub_key(path.parent.name, by_slug)
        if not key:
            return _aside(CREDIT, _fallback_sentence("tool"))
        return _aside(HUBS[key][0], _hub_sentence(key, []))
    if kind != "comparison":
        return None
    keys: list[str] = []
    for part in path.stem.split("-vs-"):
        key = _hub_key(part, by_slug)
        if key and key not in keys:
            keys.append(key)
    if not keys:
        return _aside(CREDIT, _fallback_sentence("comparison"))
    return _aside(HUBS[keys[0]][0], _hub_sentence(keys[0], keys[1:]))


def _kind(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root).as_posix()
    if rel == "tools/index.html":
        return "tool-index"
    if rel.startswith("tools/") and rel.endswith("/index.html") and path.parent.parent == root / "tools":
        return "tool"
    if rel.startswith("comparisons/") and path.parent == root / "comparisons" and path.suffix == ".html":
        return "comparison-index" if path.name == "index.html" else "comparison"
    if rel.startswith("guides/") and path.suffix == ".html":
        return "guide"
    if rel.startswith("categories/") and path.name == "index.html":
        return "category"
    if rel in UTILITY_PAGES:
        return "utility"
    return None


def _add_class(text: str) -> str:
    def repl(match: re.Match) -> str:
        attrs = match.group(1)
        class_match = re.search(r'class="([^"]*)"', attrs)
        if not class_match:
            return f'<body{attrs} class="ledger-page">'
        classes = class_match.group(1).split()
        if "ledger-page" not in classes:
            classes.append("ledger-page")
        attrs = attrs[: class_match.start()] + f'class="{" ".join(classes)}"' + attrs[class_match.end() :]
        return f"<body{attrs}>"

    return BODY_RE.sub(repl, text, count=1)


def _insert(text: str, block: str) -> str:
    text = re.sub(
        r"\n*" + re.escape(MARK_S) + r".*?" + re.escape(MARK_E) + r"\n*",
        "",
        text,
        flags=re.S,
    )
    hero = HERO_RE.search(text)
    if hero:
        at = hero.end()
    else:
        main = MAIN_RE.search(text)
        at = main.end() if main else None
    if at is None:
        return text + "\n" + block + "\n"
    rest = re.sub(r"^\n+", "", text[at:])
    return text[:at] + "\n" + block + "\n" + rest


def inject(root: Path) -> int:
    by_slug = _catalog(root)
    changed = 0
    for path in sorted(root.rglob("*.html")):
        if any(part in {".git", "content_briefs", "admin", "go"} for part in path.parts):
            continue
        kind = _kind(path, root)
        if not kind:
            continue
        text = path.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text:
            continue
        updated = _add_class(text)
        updated = THEME_RE.sub(r"\1#FAF8F5\2", updated)
        updated = updated.replace("\u2726", "")
        updated = DARK_INLINE.sub(r"\1#FAF8F5", updated)
        block = _callout(kind, path, by_slug)
        if block:
            updated = _insert(updated, block)
        else:
            updated = BLOCK_RE.sub("", updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(inject(Path(__file__).resolve().parents[1]))
