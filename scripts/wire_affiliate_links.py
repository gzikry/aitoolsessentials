#!/usr/bin/env python3
"""Point approved-partner CTAs at /go/<slug>/.

Evidence links (pricing, docs, privacy, terms) stay on the vendor URL.
Visit / Try / homepage buttons, and any anchor already using a partner URL,
become the hop. The hop page holds the partner URL.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from affiliate_util import approved_programs, inject_product_links_module

MARK_S = "<!-- AIT PARTNER HOPS START -->"
MARK_E = "<!-- AIT PARTNER HOPS END -->"
_A_TAG = re.compile(r"<a\b([^>]*?)>(.*?)</a>", re.I | re.S)
_HREF = re.compile(r'\bhref="([^"]*)"')
_REL = re.compile(r'\brel="([^"]*)"')
_TARGET = re.compile(r'\s*target="[^"]*"')
PARTNER_REL = "sponsored nofollow noopener"
DISCLOSURE = (
    '<p class="ledger-disclosure">Some outbound links may earn a partner commission '
    'at no cost to you. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>'
)
_DISCLOSURE_SPAN = (
    '<span class="ledger-disclosure">Some outbound links may earn a partner commission '
    'at no cost to you. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</span>'
)
# Product names, not the verb "make" or the word "description".
_NAME_PATTERNS = {
    "elevenlabs": re.compile(r"ElevenLabs|\belevenlabs\b", re.I),
    "make": re.compile(r"\bMake\b|make\.com"),
    "gamma": re.compile(r"\bGamma\b"),
    "descript": re.compile(r"\bDescript\b"),
    "aidetector-cx": re.compile(r"AIDetector|aidetector", re.I),
    "sonaopus": re.compile(r"Sonaopus|sonaopus", re.I),
    "hermes-agent": re.compile(r"Hermes Agent|hermes-agent", re.I),
}
_APP_BUILDER_LINKS = (
    ('/go/v0/', "Try v0"),
    ("/go/bolt-new/", "Try Bolt.new"),
    ("/go/lovable/", "Try Lovable"),
    ("/go/replit-ai/", "Try Replit"),
)
_COST_VERDICT_S = "<!-- AIT COST VERDICTS START -->"
_COST_VERDICT_E = "<!-- AIT COST VERDICTS END -->"
_CITE_LABEL = re.compile(
    r"^(official pricing|product documentation|privacy(?:\s*/\s*data use)?|"
    r"rights(?:\s*/\s*terms)?|pricing|docs|privacy|terms|rights|help|legal|"
    r"trust|security|documentation)\b",
    re.I,
)
_CITATION = (
    "/pricing",
    "/privacy",
    "/terms",
    "/help",
    "/docs",
    "/legal",
    "/trust",
    "/security",
    "/blog",
    "/documentation",
    "/policies",
)


def _host(url: str) -> str:
    host = (urlsplit(url).hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def _path(url: str) -> str:
    return urlsplit(url).path.rstrip("/").lower()


def _scope(root: Path, path: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    if rel.startswith(("admin/", "marketing/", "go/", "newsletter/", "legal/", "scripts/")):
        return False
    if rel.startswith(("tools/", "comparisons/", "guides/switch-guides/", "articles/", "compare/")):
        return True
    return rel in {"index.html", "stack-audit.html", "cost-calculator.html"}


def _partners(root: Path) -> list[dict]:
    tools = {
        tool["slug"]: tool
        for tool in json.loads((root / "data" / "tools.json").read_text(encoding="utf-8"))
    }
    rows = []
    for slug, prog in approved_programs(root).items():
        tool = tools.get(slug) or {}
        official = (tool.get("official") or "").strip()
        affiliate = (prog.get("affiliate_url") or prog.get("approved_tracking_url") or "").strip()
        public = (prog.get("public_href") or f"/go/{slug}/").strip()
        if not public.endswith("/"):
            public += "/"
        rows.append({
            "slug": slug,
            "name": tool.get("name") or slug.replace("-", " "),
            "official": official,
            "affiliate": affiliate,
            "public": public,
        })
    return rows


def _is_partner_cta(href: str, partner: dict) -> bool:
    if href.startswith("/"):
        return href.rstrip("/") + "/" == partner["public"]
    affiliate = partner["affiliate"]
    if affiliate and (href == affiliate or href.startswith(affiliate.split("?", 1)[0])):
        bare = affiliate.split("?", 1)[0].rstrip("/")
        if href.split("?", 1)[0].rstrip("/") == bare or href.startswith(affiliate):
            return True
    official = partner["official"]
    if not official or _host(href) != _host(official):
        return False
    path = _path(href)
    official_path = _path(official)
    # The official homepage is the CTA even when that URL lives under /docs.
    # Citation labels are restored earlier and never reach this check.
    if path == official_path or path in {"", "/register", "/signup", "/en/register", "/ai", "/en"}:
        return True
    if any(bit in path for bit in _CITATION):
        return False
    return False


def _retarget(attrs: str, public: str) -> str:
    if _HREF.search(attrs):
        attrs = _HREF.sub(f'href="{public}"', attrs, count=1)
    else:
        attrs += f' href="{public}"'
    if _REL.search(attrs):
        attrs = _REL.sub(f'rel="{PARTNER_REL}"', attrs, count=1)
    else:
        attrs += f' rel="{PARTNER_REL}"'
    attrs = _TARGET.sub("", attrs)
    return attrs


def _citation_label(inner: str) -> bool:
    plain = re.sub(r"<[^>]+>", "", inner)
    plain = plain.replace("↗", " ").strip()
    return bool(_CITE_LABEL.match(plain))


def _restore_citation(attrs: str, inner: str, partners: list[dict]) -> str | None:
    """Evidence labels stay on the official URL, even if an earlier pass hopped them."""
    href_match = _HREF.search(attrs)
    if not href_match:
        return None
    href = href_match.group(1)
    for partner in partners:
        affiliate = partner["affiliate"]
        hopped = href.rstrip("/") + "/" == partner["public"] or (
            bool(affiliate) and (href == affiliate or href.startswith(affiliate))
        )
        if not hopped:
            continue
        official = partner["official"]
        if not official:
            return None
        if _HREF.search(attrs):
            attrs = _HREF.sub(f'href="{official}"', attrs, count=1)
        if _REL.search(attrs):
            attrs = _REL.sub('rel="external noopener"', attrs, count=1)
        else:
            attrs += ' rel="external noopener"'
        if "target=" not in attrs:
            attrs += ' target="_blank"'
        return "<a" + attrs + ">" + inner + "</a>"
    return None


def _rewrite_tags(html: str, partners: list[dict]) -> str:
    def repl(match: re.Match[str]) -> str:
        attrs = match.group(1)
        inner = match.group(2)
        if _citation_label(inner):
            restored = _restore_citation(attrs, inner, partners)
            return restored if restored is not None else match.group(0)
        href_match = _HREF.search(attrs)
        if not href_match:
            return match.group(0)
        href = href_match.group(1)
        for partner in partners:
            if not _is_partner_cta(href, partner):
                continue
            rel_match = _REL.search(attrs)
            already = href.rstrip("/") + "/" == partner["public"] and rel_match and rel_match.group(1) == PARTNER_REL
            if already:
                return match.group(0)
            return "<a" + _retarget(attrs, partner["public"]) + ">" + inner + "</a>"
        return match.group(0)

    return _A_TAG.sub(repl, html)


def _name_mentioned(html: str, partner: dict) -> bool:
    pattern = _NAME_PATTERNS.get(partner["slug"])
    return bool(pattern and pattern.search(html))


def _mentioned(html: str, rel: str, partner: dict) -> bool:
    slug = partner["slug"]
    if f"/tools/{slug}/" in html:
        return True
    if re.search(
        rf"(^|[^a-z0-9]){re.escape(slug)}([^a-z0-9]|$)",
        Path(rel).name,
    ):
        return True
    # Hubs and the cost calculator name a partner without linking /tools/<slug>/.
    if rel.startswith(("comparisons/", "guides/switch-guides/")) or rel == "cost-calculator.html":
        return _name_mentioned(html, partner)
    return False


def _hop_block(partners: list[dict]) -> str:
    links = "".join(
        f'<a href="{partner["public"]}" rel="{PARTNER_REL}">Try {partner["name"]}</a> '
        for partner in partners
    )
    return (
        f"{MARK_S}<p class=\"ledger-disclosure\">Some outbound links may earn a partner commission "
        f'at no cost to you. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>'
        f"<p>{links}</p>{MARK_E}"
    )


def _inject(html: str, block: str) -> str:
    pattern = re.compile(re.escape(MARK_S) + r".*?" + re.escape(MARK_E), re.S)
    if MARK_S in html:
        return pattern.sub(lambda _m: block, html, count=1)
    if "</main>" not in html:
        return html
    return html.replace("</main>", block + "\n</main>", 1)


def _app_builder_paragraph() -> str:
    links = " · ".join(
        f'<a href="{href}" rel="external noopener">{label}</a>'
        for href, label in _APP_BUILDER_LINKS
    )
    return f"<p>{links}</p>{DISCLOSURE}"


def _wire_app_builder_links(html: str) -> str:
    """The four builder hops are campaign tags, not approved partner programs."""
    wanted = _app_builder_paragraph()
    if wanted in html:
        return html
    pattern = re.compile(r"<p>(?:(?!</p>).)*href=\"/go/v0/\"(?:(?!</p>).)*</p>", re.S)
    match = pattern.search(html)
    if not match:
        return html
    end = match.end()
    if html.startswith(DISCLOSURE, end):
        end += len(DISCLOSURE)
    return html[: match.start()] + wanted + html[end:]


_COST_VERDICT_JS = r"""
(function () {
  var partners = {
    elevenlabs: "/go/elevenlabs/",
    make: "/go/make/",
    gamma: "/go/gamma/",
    descript: "/go/descript/",
    "aidetector-cx": "/go/aidetector-cx/",
    sonaopus: "/go/sonaopus/",
    "hermes-agent": "/go/nous/"
  };
  var disclosure = '<span class="ledger-disclosure">Some outbound links may earn a partner commission at no cost to you. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</span>';
  function esc(value) {
    return String(value || "").replace(/[&<>"]/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch];
    });
  }
  function estimate(tool) {
    var price = (tool.price || "").toLowerCase();
    if (price.indexOf("free self-hosted") !== -1) return 0;
    if (price.indexOf("free") !== -1) return 20;
    return 35;
  }
  var box = document.getElementById("cost-verdicts");
  var idle = box ? box.innerHTML : "";
  function render() {
    if (!box || typeof COST_TOOLS === "undefined") return;
    var selected = [];
    var boxes = document.querySelectorAll("[data-cost]:checked");
    for (var i = 0; i < boxes.length; i++) {
      for (var j = 0; j < COST_TOOLS.length; j++) {
        if (COST_TOOLS[j].slug === boxes[i].value) selected.push(COST_TOOLS[j]);
      }
    }
    if (!selected.length) {
      box.innerHTML = idle;
      return;
    }
    var costs = selected.map(estimate);
    var cheapest = costs[0];
    for (var k = 1; k < costs.length; k++) if (costs[k] < cheapest) cheapest = costs[k];
    var html = "<h3>Keep / Switch</h3>";
    for (var n = 0; n < selected.length; n++) {
      var tool = selected[n];
      var verdict = costs[n] === cheapest ? "Keep" : "Switch";
      var hop = partners[tool.slug] || ("/go/" + tool.slug + "/");
      var partner = Object.prototype.hasOwnProperty.call(partners, tool.slug);
      var rel = partner ? "sponsored nofollow noopener" : "external noopener";
      html += '<p><span class="ledger-stamp">' + verdict + "</span> " + esc(tool.name) +
        ' <a href="' + hop + '" rel="' + rel + '">Open</a>';
      if (partner) html += " " + disclosure;
      html += "</p>";
    }
    box.innerHTML = html;
  }
  document.addEventListener("change", function (event) {
    var target = event.target;
    if (!target) return;
    if (target.matches && (target.matches("[data-cost]") || target.id === "teamSize")) render();
  });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", render);
  else render();
})();
"""


def _partner_open_links() -> str:
    rows = []
    catalog = (
        ("elevenlabs", "/go/elevenlabs/", "ElevenLabs"),
        ("make", "/go/make/", "Make"),
        ("gamma", "/go/gamma/", "Gamma"),
        ("descript", "/go/descript/", "Descript"),
        ("aidetector-cx", "/go/aidetector-cx/", "AIDetector.cx"),
        ("sonaopus", "/go/sonaopus/", "Sonaopus"),
        ("hermes-agent", "/go/nous/", "Hermes Agent"),
    )
    for _slug, href, name in catalog:
        rows.append(
            f'<p><a href="{href}" rel="{PARTNER_REL}">Open {name}</a> {_DISCLOSURE_SPAN}</p>'
        )
    return (
        "<h3>Keep / Switch</h3>"
        "<p>Select seats above. The lowest planning estimate stays Keep. A dearer selected seat is Switch.</p>"
        + "".join(rows)
    )


def _inject_cost_verdicts(html: str) -> str:
    block = (
        f'{_COST_VERDICT_S}<div id="cost-verdicts" aria-live="polite">'
        f"{_partner_open_links()}</div><script>{_COST_VERDICT_JS}</script>{_COST_VERDICT_E}"
    )
    pattern = re.compile(re.escape(_COST_VERDICT_S) + r".*?" + re.escape(_COST_VERDICT_E), re.S)
    if _COST_VERDICT_S in html:
        return pattern.sub(lambda _m: block, html, count=1)
    summary = re.search(r'<div id="costSummary"[^>]*>.*?</div>', html, re.S)
    if not summary:
        return html
    return html[: summary.end()] + "\n" + block + html[summary.end() :]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    partners = _partners(root)
    approved = approved_programs(root)
    changed = 0
    hops = 0
    from affiliate_util import write_hop_pages

    hops = write_hop_pages(root)
    for path in root.rglob("*.html"):
        if not _scope(root, path):
            continue
        original = path.read_text(encoding="utf-8", errors="ignore")
        updated = _rewrite_tags(original, partners)
        rel = path.relative_to(root).as_posix()
        if rel == "compare/ai-app-builders/index.html":
            updated = _wire_app_builder_links(updated)
        featured = [partner for partner in partners if _mentioned(updated, rel, partner)]
        if featured and not rel.startswith("tools/") and rel != "index.html" and "</main>" in updated:
            missing = [partner for partner in featured if partner["public"] not in updated]
            if missing or MARK_S in updated:
                updated = _inject(updated, _hop_block(featured))
        if rel == "cost-calculator.html":
            updated = _inject_cost_verdicts(updated)
        if rel.startswith("tools/") and rel.count("/") == 2:
            slug = rel.split("/")[1]
            prog = approved.get(slug)
            if prog:
                updated = inject_product_links_module(updated, prog)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"affiliate wiring: {changed} pages updated; hops={hops}")


if __name__ == "__main__":
    main()
