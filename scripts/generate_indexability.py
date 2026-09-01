#!/usr/bin/env python3
"""Durable indexability post-pass for leftover HTML the generators do not rewrite.

Fixes only verified crawl bugs:
- doubled .html.html canonicals / og:url
- leftover article titles that collide with comparison titles
- directory canonicals that still point at /index.html
- cite-strip injection on leftover hubs that high-visibility generators miss
"""
from __future__ import annotations

import re
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
CITE_START = "<!-- AIT SOURCE CITE START -->"
CITE_END = "<!-- AIT SOURCE CITE END -->"
CITE_MODULE = (
    f'{CITE_START}<section class="score-card related-next-steps"><span>Cite and verify</span>'
    "<h2>Source pages Google can quote.</h2>"
    '<p><a href="/pricing-watch/">Pricing Watch</a> · '
    '<a href="/newsletter/">Keep/Cut Weekly</a> · '
    '<a href="/press/">Press / cite us</a> · '
    '<a href="/evidence/">Evidence ledger</a> · '
    '<a href="/methodology/">Methodology</a></p>'
    f"</section>{CITE_END}"
)
CITE_TARGETS = (
    "categories/index.html",
    "articles/index.html",
    "comparisons/index.html",
    "tools/index.html",
    "best-for/index.html",
    "stacks/index.html",
    "glossary/index.html",
)
LEFTOVER_TITLE_SUFFIX = {
    "articles/claude-code-vs-copilot-vs-cursor.html": "Claude Code vs Copilot vs Cursor — same-task pick | AIToolsEssentials",
    "articles/ai-invoicing-admin-stack-solo-consultants.html": "AI invoicing stack for solo consultants — keep/cut | AIToolsEssentials",
}


def _public_html(root: Path):
    for p in root.rglob("*.html"):
        rel = p.relative_to(root)
        if "admin" in rel.parts or any(part.startswith(".") for part in rel.parts):
            continue
        yield p, rel


def _expected_url(rel: Path) -> str:
    if rel.name == "index.html":
        if len(rel.parts) == 1:
            return f"{DOMAIN}/"
        return f"{DOMAIN}/" + "/".join(rel.parts[:-1]) + "/"
    return f"{DOMAIN}/" + "/".join(rel.parts)


def _close_truncated_document(html: str) -> str:
    """Close leftover sitemap pages that were cut off mid-tag. Does not invent copy."""
    html = re.sub(r"<li>[^<]*\Z", "", html)
    html = re.sub(r"<se\Z", "", html)
    html = re.sub(r"<[a-zA-Z][^>]*\Z", "", html)
    for tag in ("ul", "ol", "article", "div", "section", "main"):
        opens = len(re.findall(rf"<{tag}(?:\s|>)", html, flags=re.I))
        closes = len(re.findall(rf"</{tag}>", html, flags=re.I))
        if opens > closes:
            html += "".join(f"</{tag}>" for _ in range(opens - closes))
    if not re.search(r"<footer\b", html, flags=re.I):
        html += (
            '<footer class="footer"><span>© 2026 AIToolsEssentials</span>'
            '<a href="/advertise/" rel="nofollow">Advertise</a>'
            '<a href="/submit-tool.html" rel="nofollow">Submit a tool</a>'
            '<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>'
            "</footer>"
        )
    if not re.search(r"</body\s*>", html, flags=re.I):
        html += '<script src="/js/site.js" defer></script></body>'
    if not re.search(r"</html\s*>", html, flags=re.I):
        html += "</html>"
    return html


def _set_title(html: str, title: str) -> str:
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S | re.I)
    html = re.sub(
        r'(<meta property="og:title" content=")[^"]*(")',
        lambda m: m.group(1) + title + m.group(2),
        html,
        count=1,
        flags=re.I,
    )
    return html


def fix_canonicals_and_titles(root: Path) -> dict[str, int]:
    stats = {"canonicals": 0, "titles": 0, "cite": 0}
    comparison_titles: dict[str, str] = {}
    for p in (root / "comparisons").glob("*.html"):
        if p.name == "index.html":
            continue
        m = re.search(r"<title>(.*?)</title>", p.read_text(), flags=re.S | re.I)
        if m:
            comparison_titles[p.stem] = re.sub(r"\s+", " ", m.group(1)).strip()

    for p, rel in _public_html(root):
        html = p.read_text()
        orig = html
        expected = _expected_url(rel)
        html = html.replace(".html.html", ".html")
        html = re.sub(
            r'(<link[^>]+rel=["\']canonical["\'][^>]+href=["\'])https://aitoolsessentials\.com/([^"\']+/)?index\.html(["\'])',
            lambda m: m.group(1) + expected + m.group(3)
            if str(rel).endswith("index.html")
            else m.group(0),
            html,
            flags=re.I,
        )
        if str(rel).endswith("index.html"):
            html = re.sub(
                r'(<link[^>]+rel=["\']canonical["\'][^>]+href=["\'])https://aitoolsessentials\.com/[^"\']+index\.html(["\'])',
                r"\1" + expected + r"\2",
                html,
                count=1,
                flags=re.I,
            )

        rel_s = str(rel)
        if rel_s in LEFTOVER_TITLE_SUFFIX:
            before_title = html
            html = _set_title(html, LEFTOVER_TITLE_SUFFIX[rel_s])
            if html != before_title:
                stats["titles"] += 1
        elif rel.parts[0] == "articles" and rel.stem in comparison_titles:
            current = re.search(r"<title>(.*?)</title>", html, flags=re.S | re.I)
            current_title = re.sub(r"\s+", " ", current.group(1)).strip() if current else ""
            if "same-task pick" not in current_title.lower():
                base = re.sub(r"\s+[—|-]\s+AIToolsEssentials.*$", "", current_title).strip()
                comp_base = re.sub(r"\s+[—|-]\s+AIToolsEssentials.*$", "", comparison_titles[rel.stem]).strip()
                comp_base = re.sub(r"\s+comparison$", "", comp_base, flags=re.I)
                if base.lower() == comp_base.lower() or current_title == comparison_titles[rel.stem]:
                    html = _set_title(html, f"{base} — same-task pick | AIToolsEssentials")
                    stats["titles"] += 1

        if rel_s in CITE_TARGETS and CITE_START not in html:
            if "</main>" in html:
                html = html.replace("</main>", CITE_MODULE + "\n</main>", 1)
                stats["cite"] += 1
            elif re.search(r"<footer\b", html, flags=re.I):
                html = re.sub(r"<footer\b", CITE_MODULE + r"\n<footer", html, count=1, flags=re.I)
                stats["cite"] += 1

        if not re.search(r"</html\s*>", html, flags=re.I):
            html = _close_truncated_document(html)
            stats["canonicals"] += 1

        if html != orig:
            p.write_text(html)
            if ".html.html" in orig or "index.html" in orig and expected not in orig:
                stats["canonicals"] += 1
    return stats


def generate(root: Path) -> dict[str, int]:
    return fix_canonicals_and_titles(root)


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
