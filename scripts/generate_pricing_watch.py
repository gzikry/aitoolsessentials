#!/usr/bin/env python3
"""Generate the public AI Pricing Watch page — a verified pricing-snapshot tracker.

Honest by design: it shows each tool's last-verified official pricing snapshot with
its checked date, plus any promos/deadlines found in the evidence. It does NOT
fabricate price history — change log entries are added only when a re-check detects
a difference vs the stored snapshot. Premium members get alert-style monitoring.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from html import escape
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
SNAPSHOT_PATH = Path(__file__).resolve().parent.parent / "data" / "pricing_snapshots.json"


def _load(root: Path) -> dict[str, Any]:
    src = json.loads((root / "data/tool_sources.json").read_text())
    return src


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    tools_list: list[dict[str, Any]] = tools if tools is not None else json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    sources = _load(root)
    checked_at = sources.get("checked_at", today)
    records = {r["slug"]: r for r in sources.get("tools", []) if r.get("slug")}
    names = {t["slug"]: t.get("name", t["slug"]) for t in tools_list}

    # Build/merge snapshot store (only real evidence; changes appended on future diffs)
    store: dict[str, Any] = {}
    if SNAPSHOT_PATH.exists():
        try:
            store = json.loads(SNAPSHOT_PATH.read_text())
        except Exception:
            store = {}
    snapshots = store.setdefault("snapshots", {})
    changelog = store.setdefault("changes", [])
    for slug, rec in records.items():
        prev = snapshots.get(slug)
        cur_digest = (rec.get("pricing_summary") or "")[:200]
        if prev and prev.get("digest") != cur_digest and prev.get("date") != rec.get("pricing_checked_date"):
            changelog.append({
                "slug": slug,
                "detected": today,
                "previous_check": prev.get("date"),
                "new_check": rec.get("pricing_checked_date"),
                "note": f"{names.get(slug, slug)}: official pricing page changed since {prev.get('date')} check. Re-verified {rec.get('pricing_checked_date')}.",
            })
            snapshots[slug] = {"date": rec.get("pricing_checked_date"), "digest": cur_digest}
        elif not prev:
            snapshots[slug] = {"date": rec.get("pricing_checked_date"), "digest": cur_digest}
    store["updated"] = today
    SNAPSHOT_PATH.write_text(json.dumps(store, indent=2) + "\n")

    rows = ""
    for t in sorted(tools_list, key=lambda x: x.get("name", "")):
        slug = t["slug"]
        rec = records.get(slug, {})
        pdate = rec.get("pricing_checked_date") or "—"
        promo_hint = ""
        summary = rec.get("pricing_summary") or "See review for current verified pricing."
        low = summary.lower()
        if "promo" in low or "% off" in low or "promotion" in low:
            promo_hint = '<span class="pill pill-promo">Promo live</span>'
        url = rec.get("pricing_url") or "#"
        rows += (
            f'<tr><td><strong><a href="/tools/{slug}/">{names.get(slug, slug)}</a></strong></td>'
            f'<td>{pdate}</td><td>{promo_hint}</td>'
            f'<td style="max-width:520px"><span class="muted">{summary[:180]}{"…" if len(summary) > 180 else ""}</span></td>'
            f'<td><a href="{url}" rel="external nofollow" target="_blank">Official pricing ↗</a></td></tr>'
        )

    watch_html = ""
    watches_path = root / "data/vendor_watches.json"
    if watches_path.exists():
        try:
            watch_data = json.loads(watches_path.read_text())
        except Exception:
            watch_data = {}
        watch_items = []
        for w in watch_data.get("watches", []):
            src = w.get("source_url") or "#"
            note = escape((w.get("pricing_note") or w.get("summary") or "")[:220], quote=True)
            status = str(w.get("status") or "")
            pricing_status = str(w.get("pricing_status") or "")
            if w.get("status_label"):
                pill = str(w.get("status_label"))
            elif status == "open_source" or pricing_status == "open_source_no_sku":
                pill = "Open source · not a directory SKU"
            else:
                pill = "Early access · no public pricing"
            watch_items.append(
                f'<tr><td><strong>{escape(str(w.get("name") or ""), quote=True)}</strong></td>'
                f'<td>{escape(str(w.get("checked_at") or "—"), quote=True)}</td>'
                f'<td><span class="pill">{escape(pill, quote=True)}</span></td>'
                f'<td style="max-width:520px"><span class="muted">{note}</span></td>'
                f'<td><a href="{escape(src, quote=True)}" rel="external nofollow" target="_blank">Official source ↗</a></td></tr>'
            )
        if watch_items:
            watch_html = (
                '<section class="score-card" style="margin-top:28px;border-left:4px solid #d97706">'
                '<span>Unlisted launches</span>'
                '<h3>Watches without directory SKUs</h3>'
                '<p>These vendor launches were checked against official posts. They are not directory listings and have no invented SKU prices. Open-source engines can appear here without a paid plan.</p>'
                '<div class="table-wrap"><table><thead><tr><th>Launch</th><th>Checked</th><th>Status</th><th>Snapshot</th><th>Source</th></tr></thead>'
                f'<tbody>{"".join(watch_items)}</tbody></table></div></section>'
            )

    change_html = ""
    if changelog:
        items = "".join(
            f'<li><strong>{c["note"]}</strong> <span class="muted">(detected {c["detected"]})</span></li>'
            for c in reversed(changelog[-20:])
        )
        change_html = f'<section class="score-card" style="margin-top:28px;border-left:4px solid #d97706"><span>Change log</span><h3>Re-checks that detected differences</h3><ul style="padding-left:20px">{items}</ul></section>'
    else:
        change_html = ('<section class="score-card" style="margin-top:28px"><span>Change log</span>'
                       '<h3>No changes detected yet</h3>'
                       '<p>The first verification snapshot is the baseline above. Every future pipeline '
                       're-check compares against it; confirmed differences appear here with dates.</p></section>')

    html = f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Verified AI tool pricing snapshots with checked dates across {len(tools_list)} tools, a public change log of confirmed price-page changes, and Premium member price alerts.">
<title>AI Pricing Watch — Verified Price Snapshots &amp; Changes — AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/pricing-watch/">
<meta property="og:title" content="AI Pricing Watch — AIToolsEssentials"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","name":"AI Pricing Watch","description":"Verified AI tool pricing snapshots and public change log.","dateModified":"{today}","publisher":{{"@type":"Organization","name":"AIToolsEssentials"}}}}</script>
</head><body>
<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/alternatives/">Alternatives</a><a href="/guides/switch-guides/">Switching</a><a href="/pricing-index/">Pricing index</a><a href="/evidence/">Evidence ledger</a><a href="/resources/">Resources</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>
<main>
<section class="scene scene-dark"><div style="max-width:900px;margin:0 auto;padding:88px 28px 64px;text-align:center">
<p class="kicker">Pricing watch · Baseline verified {checked_at}</p>
<h1>Know when AI prices move.</h1>
<p class="subhead">Every AI tool's pricing below traces to its official vendor page with a checked date — no scraped guesses. Future re-checks that detect changes land in the public change log. Premium members get alerted first.</p>
<p><a class="button button-blue" href="/premium/">Get price alerts with Premium</a><a class="button button-ghost-dark" href="/newsletter/" style="margin-left:8px">Keep/Cut Weekly</a></p>
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
<div class="table-wrap"><table>
<thead><tr><th>Tool</th><th>Pricing verified</th><th>Status</th><th>Snapshot</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table></div>
{watch_html}
{change_html}
<p class="affiliate-inline" style="margin-top:16px">Methodology: snapshots come from each vendor's official pricing page on the date shown; we never infer or estimate missing values. This page is informational — always confirm final pricing with the vendor before purchasing.</p>
</div></section>
</main>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a><a href="/legal/corrections.html">Corrections</a><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>
<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>
</body></html>'''
    out = root / "pricing-watch"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html)
    return len(records)


if __name__ == "__main__":
    root0 = Path(__file__).resolve().parent.parent
    print(generate(root0))


def postprocess(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    """Re-inject Pricing Watch links into pricing-index and premium pages after regeneration."""
    n = 0
    pi = root / "pricing-index/index.html"
    if pi.exists():
        s = pi.read_text()
        if "/pricing-watch/" not in s:
            mod = ('<section class="score-card" style="margin:26px auto 0;max-width:880px"><span>Price monitoring</span>'
                   '<h3>AI Pricing Watch</h3><p>See each tool\'s last-verified pricing snapshot and every confirmed change.</p>'
                   '<p><a href="/pricing-watch/">Open Pricing Watch →</a></p></section>')
            i = s.rfind("</main>")
            pi.write_text(s[:i] + mod + "\n" + s[i:])
            n += 1
    pr = root / "premium/index.html"
    if pr.exists():
        s = pr.read_text()
        if "/pricing-watch/" not in s:
            mod = ('<section class="score-card" style="margin:26px auto 0;max-width:880px"><span>Member benefit</span>'
                   '<h3>Price-change alerts</h3><p>Premium members hear about confirmed official price changes first — before renewals hit. '
                   'Public baseline: <a href="/pricing-watch/">AI Pricing Watch</a>.</p></section>')
            i = s.rfind("</main>")
            pr.write_text(s[:i] + mod + "\n" + s[i:])
            n += 1
    return n


if __name__ == "__main__":
    root0 = Path(__file__).resolve().parent.parent
    print(generate(root0))
    print("postprocess:", postprocess(root0))
