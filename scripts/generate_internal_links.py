#!/usr/bin/env python3
"""Link public pages from the matching category page, tool page, and article.

Redirect stubs and the two deliberate exceptions stay unlinked. /404.html is
the error page. /shortlist.html is opened by js/site.js only after a reader
saves a tool. Moved URLs are noindex refresh stubs; indexable pages must not
point at them. Everything else gets a stable href the internal-link audit can
see (literal spaces and ampersands, not percent-encoding).

The block is a pure function of the catalog, so a second generator pass
reprints it.
"""
from __future__ import annotations

import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from consolidate_duplicates import is_redirect_stub
from internal_link_audit import (
    build_link_graph,
    classify_orphans,
    extract_links,
    find_html_files,
    find_orphan_pages,
    get_page_url,
)

START = "<!-- AIT RELATED READING START -->"
END = "<!-- AIT RELATED READING END -->"
_BLOCK = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
_TITLE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
_SLUG = re.compile(r"/tools/([a-z0-9-]+)/")

# Hops that are not catalog tools, and the public pages that should carry them.
EXTRA_HOPS = {
    "claude-code": ("Claude Code", ("tools/claude/index.html", "categories/Development/index.html")),
}

# Sitewide pages linked from the category hub and the tool directory.
HUB_LINKS = (
    ("/pricing-index/", "AI tool pricing index"),
    ("/start-here/", "Start here"),
    ("/site-map/", "Site map"),
    ("/community/reports.html", "Community test reports"),
    ("/premium/archive.html", "Premium research archive"),
    ("/submit/", "Submit an AI tool"),
    ("/services/sample-audit.html", "Sample AI stack audit"),
    ("/services/audit-standard.html", "AI stack audit delivery standard"),
    ("/services/intake-received.html", "Audit intake received"),
)

ARTICLE_EXTRAS = {
    "learn.html": (
        ("/start-here/", "Start here"),
        ("/site-map/", "Site map"),
        ("/community/reports.html", "Community test reports"),
        ("/submit/", "Submit an AI tool"),
    ),
    "monthly-ai-cost-review.html": (("/pricing-index/", "AI tool pricing index"),),
    "monthly-vs-annual-ai-plans.html": (("/pricing-index/", "AI tool pricing index"),),
    "what-are-ai-credits.html": (("/pricing-index/", "AI tool pricing index"),),
    "is-an-ai-tool-membership-worth-it.html": (
        ("/premium/archive.html", "Premium research archive"),
        ("/services/sample-audit.html", "Sample AI stack audit"),
        ("/services/audit-standard.html", "AI stack audit delivery standard"),
        ("/services/intake-received.html", "Audit intake received"),
    ),
    "best-ai-tools-for-customer-support.html": (
        ("/embed/customer-support-cost.html", "Customer support cost embed"),
    ),
    "grok-alternatives.html": (("/xai-bot-guides/", "Grok bot guides"),),
    "grok-vs-chatgpt.html": (("/xai-bot-guides/", "Grok bot guides"),),
    "is-grok-worth-it.html": (("/xai-bot-guides/", "Grok bot guides"),),
}


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _title(page_html: str, fallback: str) -> str:
    match = _TITLE.search(page_html)
    if not match:
        return fallback
    text = re.sub(r"\s+", " ", match.group(1)).strip()
    text = re.sub(r"\s+(\||—|-)\s+AIToolsEssentials.*$", "", text)
    text = text.replace(" (moved)", "")
    return text or fallback


def _dedupe(links: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[str] = set()
    ordered: list[tuple[str, str]] = []
    for href, label in links:
        if href in seen:
            continue
        seen.add(href)
        ordered.append((href, label))
    return ordered


def _block(links: list[tuple[str, str]], *, heading: bool) -> str:
    items = "".join(f"<li><a href=\"{href}\">{_esc(label)}</a></li>" for href, label in links)
    title = "<h2>Related reading</h2>" if heading else ""
    return f"{START}\n<section class=\"score-card related-reading\">{title}<ul>{items}</ul></section>\n{END}\n"


def _upsert(page_html: str, block: str, *, heading_outside: bool) -> str:
    if START in page_html:
        return _BLOCK.sub(block, page_html, count=1)
    if heading_outside and "<h2>Related reading</h2>" in page_html:
        return page_html.replace("<h2>Related reading</h2>", "<h2>Related reading</h2>\n" + block, 1)
    if "</main>" in page_html:
        return page_html.replace("</main>", block + "</main>", 1)
    if "<footer" in page_html:
        return page_html.replace("<footer", block + "<footer", 1)
    return page_html


def _visible_links(page_html: str, page_url: str) -> set[str]:
    outside = _BLOCK.sub("", page_html)
    return set(extract_links(outside, page_url))


def _write_links(path: Path, links: list[tuple[str, str]], *, article: bool) -> bool:
    page_html = path.read_text(encoding="utf-8", errors="ignore")
    outside = _BLOCK.sub("", page_html)
    page_url = get_page_url(path)
    already = _visible_links(page_html, page_url)
    kept = [(href, label) for href, label in _dedupe(links) if href != page_url and href not in already]
    if not kept:
        if START not in page_html:
            return False
        path.write_text(_BLOCK.sub("", page_html), encoding="utf-8")
        return True
    heading_outside = article and "<h2>Related reading</h2>" in outside
    block = _block(kept, heading=not heading_outside)
    updated = _upsert(page_html, block, heading_outside=heading_outside)
    if updated == page_html:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def _hop_exists(root: Path, slug: str) -> bool:
    return (root / "go" / slug / "index.html").is_file()


def _article_slugs(stem: str, page_html: str, by_slug: dict) -> Counter:
    """Count catalog tools named in the copy, with a boost when the filename names one."""
    counts: Counter = Counter(slug for slug in _SLUG.findall(page_html) if slug in by_slug)
    tokens = stem.split("-")
    for slug, parts in ((slug, slug.split("-")) for slug in by_slug):
        width = len(parts)
        if any(tokens[i : i + width] == parts for i in range(len(tokens) - width + 1)):
            counts[slug] += 5
    return counts


def apply(root: Path) -> str:
    tools = json.loads((root / "data" / "tools.json").read_text(encoding="utf-8"))
    by_slug = {tool["slug"]: tool for tool in tools}
    by_category: dict[str, list[dict]] = defaultdict(list)
    for tool in tools:
        by_category[tool.get("category") or "Uncategorized"].append(tool)
    for rows in by_category.values():
        rows.sort(key=lambda tool: tool.get("name") or tool["slug"])

    planned: dict[Path, list[tuple[str, str]]] = defaultdict(list)

    def add(rel: str, href: str, label: str) -> None:
        path = root / rel
        if path.is_file():
            planned[path].append((href, label))

    for slug, tool in sorted(by_slug.items()):
        category = tool.get("category") or "Uncategorized"
        name = tool.get("name") or slug
        add(f"tools/{slug}/index.html", f"/categories/{category}/", f"{category} category")
        add(f"tools/{slug}/index.html", "/pricing-index/", "AI tool pricing index")
        if _hop_exists(root, slug):
            hop = (f"/go/{slug}/", f"{name} site hop")
            add(f"tools/{slug}/index.html", *hop)
            add(f"categories/{category}/index.html", *hop)
        if slug in {"customgpt", "robylon"}:
            add(
                f"tools/{slug}/index.html",
                "/embed/customer-support-cost.html",
                "Customer support cost embed",
            )
        if slug == "grok":
            add(f"tools/{slug}/index.html", "/xai-bot-guides/", "Grok bot guides")

    for category in sorted(by_category):
        add(f"categories/{category}/index.html", "/pricing-index/", "AI tool pricing index")
    add(
        "categories/AI Agents/index.html",
        "/embed/customer-support-cost.html",
        "Customer support cost embed",
    )
    add("categories/General AI Assistant/index.html", "/xai-bot-guides/", "Grok bot guides")

    for slug, (label, homes) in EXTRA_HOPS.items():
        if not _hop_exists(root, slug):
            continue
        for rel in homes:
            add(rel, f"/go/{slug}/", f"{label} site hop")
        add("tools/index.html", f"/go/{slug}/", f"{label} site hop")
        add("categories/index.html", f"/go/{slug}/", f"{label} site hop")

    for hop in sorted((root / "go").glob("*/index.html")):
        slug = hop.parent.name
        if slug in by_slug or slug in EXTRA_HOPS:
            continue
        label = _title(hop.read_text(encoding="utf-8", errors="ignore"), slug)
        label = label.removeprefix("Continuing to ").strip() or slug
        add("tools/index.html", f"/go/{slug}/", f"{label} site hop")
        add("categories/index.html", f"/go/{slug}/", f"{label} site hop")

    for href, label in HUB_LINKS:
        add("categories/index.html", href, label)
        add("tools/index.html", href, label)
    add("community/test-report.html", "/community/reports.html", "Community test reports")

    drafts = sorted((root / "admin" / "newsletter").glob("*-draft.html"))
    for draft in drafts:
        add("admin/index.html", f"/admin/newsletter/{draft.name}", f"Held draft {draft.stem.removesuffix('-draft')}")

    articles_dir = root / "articles"
    article_pages = []
    for path in sorted(articles_dir.glob("*.html")):
        page_html = path.read_text(encoding="utf-8", errors="ignore")
        if path.name == "index.html" or is_redirect_stub(page_html):
            continue
        counts = _article_slugs(path.stem, page_html, by_slug)
        article_pages.append((path, page_html, counts))

    for path, page_html, counts in article_pages:
        links: list[tuple[str, str]] = []
        floor = 2 if len(counts) >= 3 else 1
        scored = []
        for other, other_html, other_counts in article_pages:
            if other == path:
                continue
            shared = len(counts.keys() & other_counts.keys())
            if shared:
                scored.append((shared, other.name, other, other_html))
        strong = [row for row in scored if row[0] >= floor] or scored
        for _shared, _name, _other, other_html in sorted(strong, key=lambda item: (-item[0], item[1]))[:4]:
            links.append((f"/articles/{_name}", _title(other_html, _name.replace("-", " ").removesuffix(".html"))))
        if counts:
            primary = counts.most_common(1)[0][0]
            tool = by_slug[primary]
            category = tool.get("category") or "Uncategorized"
            links.append((f"/categories/{category}/", f"{category} category"))
            if _hop_exists(root, primary):
                links.append((f"/go/{primary}/", f"{tool.get('name') or primary} site hop"))
        links.extend(ARTICLE_EXTRAS.get(path.name, ()))
        if len(_dedupe(links)) < 3:
            links.append(("/articles/", "All guides"))
            links.append(("/categories/", "All categories"))
            links.append(("/start-here/", "Start here"))
        planned[path].extend(links)

    # The guides hub is generated and is not a single-tool article.
    add("articles/index.html", "/start-here/", "Start here")
    add("articles/index.html", "/pricing-index/", "AI tool pricing index")
    add("articles/index.html", "/site-map/", "Site map")

    written = 0
    for path, links in sorted(planned.items(), key=lambda item: item[0].as_posix()):
        article = path.parent.name == "articles" and path.suffix == ".html"
        if _write_links(path, links, article=article):
            written += 1

    pages = find_html_files()
    _graph, reverse = build_link_graph(pages)
    unexpected, intentional = classify_orphans(pages, find_orphan_pages(pages, reverse))
    if unexpected:
        raise RuntimeError("unexpected orphans remain: " + ", ".join(unexpected))
    return f"updated {written} pages; unexpected orphans 0; intentional {len(intentional)}"


if __name__ == "__main__":
    print(apply(Path(__file__).resolve().parents[1]))
