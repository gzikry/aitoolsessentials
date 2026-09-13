#!/usr/bin/env python3
"""Approved affiliate/referral helpers. Public pages must use hop hrefs when set."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

NOUS_MARK_S = "<!-- AIT NOUS REFERRAL START -->"
NOUS_MARK_E = "<!-- AIT NOUS REFERRAL END -->"
PRODUCT_MARK_S = "<!-- AIT PRODUCT AFFILIATE START -->"
PRODUCT_MARK_E = "<!-- AIT PRODUCT AFFILIATE END -->"

NOUS_OFFER = (
    "Nous Research gives you $15 off your first month on the Nous API and Hermes Agent."
)


def load_affiliate_programs(root: Path) -> list[dict[str, Any]]:
    path = root / "data/affiliate_programs.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return data.get("affiliate_programs", [])


def approved_programs(root: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for prog in load_affiliate_programs(root):
        slug = prog.get("tool_slug")
        url = prog.get("affiliate_url") or prog.get("approved_tracking_url")
        if slug and url and prog.get("application_status") == "approved":
            out[slug] = prog
    return out


def public_affiliate_href(prog: dict[str, Any]) -> str:
    """Href for public HTML. Prefer the site hop so tracking slugs stay off public pages."""
    return prog.get("public_href") or prog.get("affiliate_url") or prog.get("approved_tracking_url") or ""


def tracking_destination(prog: dict[str, Any]) -> str:
    return prog.get("affiliate_url") or prog.get("approved_tracking_url") or ""


def product_links(prog: dict[str, Any] | None) -> list[dict[str, str]]:
    if not prog:
        return []
    out: list[dict[str, str]] = []
    for item in prog.get("product_links") or []:
        name = (item or {}).get("name") or ""
        url = (item or {}).get("url") or ""
        if name and url.startswith("http"):
            out.append({"name": name, "url": url})
    return out


def product_links_module(prog: dict[str, Any] | None, disclosure_href: str = "../../legal/affiliate-disclosure.html") -> str:
    """Disclosed per-product affiliate checkout list for a review pricing section."""
    items = product_links(prog)
    if not items:
        return ""
    lis = "".join(
        f'<li><a href="{item["url"]}" rel="sponsored noopener nofollow" target="_blank">{item["name"]}</a></li>'
        for item in items
    )
    return (
        f'{PRODUCT_MARK_S}<div class="official-source-links">'
        "<p><strong>Profession products</strong> (affiliate checkout):</p>"
        f"<ul>{lis}</ul>"
        '<p class="pricing-fineprint">Affiliate links — we may earn a commission at no cost to you. See our '
        f'<a href="{disclosure_href}">disclosure</a>.</p>'
        f"</div>{PRODUCT_MARK_E}"
    )


def inject_product_links_module(html: str, prog: dict[str, Any] | None) -> str:
    import re

    module = product_links_module(prog)
    pattern = re.compile(re.escape(PRODUCT_MARK_S) + r".*?" + re.escape(PRODUCT_MARK_E), re.S)
    if not module:
        return pattern.sub("", html) if PRODUCT_MARK_S in html else html
    if PRODUCT_MARK_S in html:
        return pattern.sub(lambda _m: module, html)
    anchor = html.find('<p class="affiliate-inline">Pricing changes often')
    if anchor == -1:
        return html
    return html[:anchor] + module + "\n" + html[anchor:]


def sponsored_href_needles(root: Path) -> tuple[str, ...]:
    """Distinctive href fragments that may legally carry rel=sponsored."""
    needles = [
        "make.com/en/register?pc=",
        "try.elevenlabs.io/",
        "/go/nous/",
        "portal.nousresearch.com/r/",
    ]
    for prog in approved_programs(root).values():
        for url in (
            public_affiliate_href(prog),
            tracking_destination(prog),
            *(item["url"] for item in product_links(prog)),
        ):
            if not url:
                continue
            stripped = url.replace("https://", "").replace("http://", "")
            if stripped and stripped not in needles:
                needles.append(stripped)
    return tuple(needles)


def nous_referral_module() -> str:
    """Modest labeled mention for AI Agents / start-here. Links to the hop, not the portal."""
    return (
        f'{NOUS_MARK_S}<section class="score-card" style="margin:26px auto 0;max-width:880px">'
        "<span>Affiliate / referral offer</span>"
        "<h3>Nous Research · Hermes Agent</h3>"
        f"<p>{NOUS_OFFER}</p>"
        '<p><a class="button button-blue small" href="/go/nous/" rel="sponsored nofollow">Claim the $15 first-month referral</a>'
        ' <a class="text-link" href="/tools/hermes-agent/" style="margin-left:8px">Read the Hermes Agent review</a>'
        ' · <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a></p>'
        f"</section>{NOUS_MARK_E}"
    )


def inject_nous_referral_module(html: str) -> str:
    import re

    module = nous_referral_module()
    pattern = re.compile(re.escape(NOUS_MARK_S) + r".*?" + re.escape(NOUS_MARK_E) + r"\n?", re.S)
    if NOUS_MARK_S in html:
        return pattern.sub(lambda _m: module, html)
    close = html.rfind("</main>")
    if close == -1:
        return html
    return html[:close] + module + "\n" + html[close:]


def hop_page_html(prog: dict[str, Any]) -> str:
    dest = tracking_destination(prog)
    title = prog.get("hop_title") or "Continuing to Nous Research"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="refresh" content="0;url={dest}">
<title>{title}</title>
<meta name="description" content="Affiliate / referral redirect to Nous Research.">
<link rel="stylesheet" href="/css/styles.css">
</head>
<body>
<p>Continuing to Nous Research…</p>
<p><a href="{dest}" rel="sponsored nofollow noopener">Continue to Nous Research</a> (affiliate / referral link)</p>
<noscript><p><a href="{dest}" rel="sponsored nofollow noopener">Continue to Nous Research</a></p></noscript>
</body>
</html>
'''


def write_hop_pages(root: Path) -> int:
    written = 0
    for prog in approved_programs(root).values():
        public = prog.get("public_href") or ""
        dest = tracking_destination(prog)
        if not public.startswith("/go/") or not dest.startswith("http"):
            continue
        rel = public.strip("/")
        if not rel.endswith("/") and not rel.endswith(".html"):
            rel = rel + "/"
        if rel.endswith("/"):
            out = root / rel / "index.html"
        else:
            out = root / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        html = hop_page_html(prog)
        if not out.exists() or out.read_text() != html:
            out.write_text(html)
        written += 1
    return written
