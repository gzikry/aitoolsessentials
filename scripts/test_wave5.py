#!/usr/bin/env python3
"""Wave 5: paper ledger pages and calculator callouts on tools and comparisons."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHRASE = "Run the numbers in the interactive calculator →"
MARK = re.compile(
    r"<!-- AIT CALCULATOR CALLOUT START -->.*?<!-- AIT CALCULATOR CALLOUT END -->",
    re.S,
)
CREDIT = "/pricing-watch/credit-traps/"
AUDIT = "/stack-audit.html"
SEAT_HUBS = (
    "/compare/ai-coding-assistants/",
    "/compare/ai-app-builders/",
    "/compare/ai-video-avatar-cost/",
    "/compare/automation-task-calculator/",
    "/compare/ai-presentation-cost/",
)


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _block(html: str) -> str:
    match = MARK.search(html)
    return match.group(0) if match else ""


def _hrefs(block: str) -> list[str]:
    return re.findall(r'href="([^"]+)"', block)


def _live(paths) -> list[Path]:
    live = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text:
            continue
        live.append(path)
    return live


def main() -> None:
    errors: list[str] = []
    css = _read("css/styles.css")
    for needle in ("body.ledger-page", "#FAF8F5", "#111315", "#D8D2C5"):
        if needle not in css:
            errors.append(f"css missing {needle}")
    if ".scene-dark { background: var(--black); color: var(--white); }" not in css:
        errors.append("global scene-dark was restyled")

    cfg = json.loads(_read("data/newsletter.json"))
    if cfg.get("send_enabled") is not False:
        errors.append("send_enabled must stay false")

    home = _read("index.html")
    if "ledger-page" in home:
        errors.append("homepage picked up ledger-page")
    premium = re.search(r'<section class="([^"]*home-premium-band[^"]*)"', home)
    if not premium or "scene-dark" not in premium.group(1) or "scene-light" in premium.group(1):
        errors.append("homepage premium band must stay scene-dark")

    def expect(rel: str, first: str, also: tuple[str, ...] = (), banned: tuple[str, ...] = ()) -> None:
        html = _read(rel)
        if 'class="ledger-page"' not in html and "ledger-page" not in html.split(">", 1)[-1][:800]:
            if "<body class=\"ledger-page\">" not in html and 'class="ledger-page"' not in html:
                errors.append(f"{rel} missing ledger-page")
        if html.count(PHRASE) != 1:
            errors.append(f"{rel} phrase count {html.count(PHRASE)}")
        block = _block(html)
        if not block:
            errors.append(f"{rel} missing callout")
            return
        if "sponsored" in block:
            errors.append(f"{rel} callout is sponsored")
        hrefs = _hrefs(block)
        if not hrefs or hrefs[0] != first:
            errors.append(f"{rel} primary {hrefs[:1]} != {first}")
        for href in (CREDIT, AUDIT, *also):
            if href not in hrefs:
                errors.append(f"{rel} missing {href}")
        for href in banned:
            if href in hrefs:
                errors.append(f"{rel} should not link {href}")
        if 'content="#FAF8F5"' not in html:
            errors.append(f"{rel} theme-color")

    expect("tools/gamma/index.html", "/compare/ai-presentation-cost/")
    expect("tools/v0/index.html", "/compare/ai-app-builders/")
    expect("tools/cursor/index.html", "/compare/ai-coding-assistants/")
    expect("tools/midjourney/index.html", "/compare/ai-video-avatar-cost/")
    expect("tools/make/index.html", "/compare/automation-task-calculator/")
    expect("tools/pika/index.html", "/compare/ai-video-avatar-cost/")
    expect("tools/elevenlabs/index.html", "/compare/ai-video-avatar-cost/")
    expect(
        "tools/harvey/index.html",
        CREDIT,
        banned=SEAT_HUBS,
    )
    expect(
        "tools/hol-registry/index.html",
        CREDIT,
        banned=SEAT_HUBS,
    )
    expect(
        "tools/claude/index.html",
        CREDIT,
        banned=SEAT_HUBS,
    )
    expect(
        "tools/jasper/index.html",
        CREDIT,
        banned=SEAT_HUBS,
    )
    expect("comparisons/v0-vs-lovable.html", "/compare/ai-app-builders/")
    expect("comparisons/cursor-vs-github-copilot.html", "/compare/ai-coding-assistants/")
    expect(
        "comparisons/midjourney-vs-canva-ai.html",
        "/compare/ai-video-avatar-cost/",
        also=("/compare/ai-presentation-cost/",),
    )
    expect(
        "comparisons/chatgpt-vs-claude.html",
        CREDIT,
        banned=SEAT_HUBS,
    )
    expect("comparisons/best-ai-tools.html", CREDIT, also=SEAT_HUBS)

    tool_pages = _live((ROOT / "tools").glob("*/index.html"))
    if len(tool_pages) < 90:
        errors.append(f"only {len(tool_pages)} live tool pages")
    for path in tool_pages:
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding="utf-8")
        if "<body class=\"ledger-page\">" not in html and 'class="ledger-page"' not in html:
            errors.append(f"{rel} missing ledger-page")
        if html.count(PHRASE) != 1 or not _block(html):
            errors.append(f"{rel} callout")
        if html.count("AIT DISCOVERY LINKS") != 1:
            errors.append(f"{rel} discovery links {html.count('AIT DISCOVERY LINKS')}")
        elif "sponsored" in _block(html):
            errors.append(f"{rel} sponsored callout")

    comp_pages = _live((ROOT / "comparisons").glob("*.html"))
    if len(comp_pages) < 370:
        errors.append(f"only {len(comp_pages)} comparison pages")
    for path in comp_pages:
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding="utf-8")
        if "ledger-page" not in html or html.count(PHRASE) != 1:
            errors.append(f"{rel} ledger callout")
        if html.count("AIT DISCOVERY LINKS") != 1:
            errors.append(f"{rel} discovery links {html.count('AIT DISCOVERY LINKS')}")

    for path in _live((ROOT / "guides" / "switch-guides").glob("*.html")):
        html = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        if "ledger-page" not in html:
            errors.append(f"{rel} missing ledger-page")
        if MARK.search(html):
            errors.append(f"{rel} should not carry a calculator callout")

    category_pages = _live((ROOT / "categories").glob("**/index.html"))
    if len(category_pages) < 16:
        errors.append(f"only {len(category_pages)} category pages")
    for path in category_pages:
        html = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        if "ledger-page" not in html:
            errors.append(f"{rel} missing ledger-page")
        if MARK.search(html):
            errors.append(f"{rel} should not carry a calculator callout")

    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"wave5 ok: {len(tool_pages)} tools, {len(comp_pages)} comparisons, "
        f"{len(category_pages)} categories"
    )


if __name__ == "__main__":
    main()
