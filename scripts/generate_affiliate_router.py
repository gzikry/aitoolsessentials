#!/usr/bin/env python3
"""Write data/affiliate_links.json and /go/<slug>/ hop pages.

Approved programs redirect to the live partner URL. Every other catalog tool
redirects to its official URL with the site UTM tags. /go/nous/ stays owned by
the Nous hop writer so that referral slug is not reprinted here.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from affiliate_util import approved_programs

UTM = {
    "utm_source": "aitoolsessentials",
    "utm_medium": "calculator",
    "utm_campaign": "keep_test_cut",
}
EXTRAS = (
    {
        "slug": "windsurf",
        "name": "Windsurf",
        "official": "https://windsurf.com/pricing",
    },
    {
        "slug": "claude-code",
        "name": "Claude Code",
        "official": "https://www.anthropic.com/pricing",
    },
)


def _with_utm(url: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    for key, value in UTM.items():
        query.setdefault(key, value)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def build_links(root: Path) -> dict:
    tools = json.loads((root / "data" / "tools.json").read_text(encoding="utf-8"))
    approved = approved_programs(root)
    records = []
    seen = set()
    for tool in tools:
        records.append(tool)
        seen.add(tool["slug"])
    for extra in EXTRAS:
        if extra["slug"] not in seen:
            records.append(extra)
    links = {}
    for tool in records:
        slug = tool["slug"]
        official = (tool.get("official") or "").strip()
        if not official:
            continue
        program = approved.get(slug) or {}
        affiliate_url = (program.get("affiliate_url") or program.get("approved_tracking_url") or "").strip()
        public_href = (program.get("public_href") or f"/go/{slug}/").strip()
        if not public_href.endswith("/"):
            public_href += "/"
        partner = bool(affiliate_url)
        destination = affiliate_url if partner else _with_utm(official)
        links[slug] = {
            "name": tool.get("name") or slug,
            "slug": slug,
            "official": official,
            "destination": destination,
            "affiliate_url": affiliate_url,
            "public_href": public_href,
            "partner": partner,
        }
    return {"utm": UTM, "links": links}


def hop_html(item: dict) -> str:
    dest = item["destination"]
    name = html.escape(item["name"])
    partner = item["partner"]
    rel = "sponsored nofollow noopener" if partner else "external noopener"
    note = "Partner link. We may earn a commission at no cost to you." if partner else "Official site, with our campaign tag."
    desc = html.escape(f"Continue to {item['name']}. {note}")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="refresh" content="0;url={html.escape(dest, quote=True)}">
<title>Continuing to {name}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://aitoolsessentials.com{item['public_href']}">
<link rel="stylesheet" href="/css/styles.css">
</head>
<body>
<main><section class="scene scene-light"><div class="article-shell">
<p>Continuing to {name}.</p>
<p><a class="stub-fallback" href="{html.escape(dest, quote=True)}" rel="{rel}">Continue to {name}</a>. {html.escape(note)}</p>
</div></section></main>
</body>
</html>
"""


def generate(root: Path) -> Path:
    payload = build_links(root)
    path = root / "data" / "affiliate_links.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for item in payload["links"].values():
        public = item["public_href"]
        # /go/nous/ is written by the Nous hop helper and must keep that copy.
        if public.rstrip("/") == "/go/nous":
            continue
        rel = public.strip("/")
        out = root / rel / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(hop_html(item), encoding="utf-8")
    return path


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
