#!/usr/bin/env python3
"""Generate the public Premium member library from dated directory data.

These pages are intentionally not login-gated: the site is static. Copy must
say that Whop handles billing/access and that this library is the worksheets
members pay $12/month for. No invented savings, case studies, or prices.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"


def esc(s: Any) -> str:
    return (
        str(s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_whop(root: Path) -> dict[str, Any]:
    cfg = json.loads((root / "data" / "integrations.json").read_text()).get("whop") or {}
    return {
        "checkout_url": cfg.get("checkout_url") or "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/",
        "checkout_promo_url": cfg.get("checkout_promo_url")
        or "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/?promo=LAUNCH50",
        "product_url": cfg.get("product_url")
        or "https://whop.com/aitoolsessentials/aitoolsessentials-premium/",
        "plan_id": cfg.get("plan_id") or "plan_FNXWs3suBFwDN",
        "promo_code": cfg.get("promo_code") or "LAUNCH50",
        "trial_period_days": int(cfg.get("trial_period_days") or 7),
        "price_usd_month": int(cfg.get("price_usd_month") or 12),
        "hub_url": "https://whop.com/hub",
    }


def header() -> str:
    return (
        '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span>'
        "<span>AIToolsEssentials</span></a><nav class=\"nav-links\">"
        '<a href="/tools/index.html">Tools</a>'
        '<a href="/stack-audit.html">Free Stack Audit</a>'
        '<a href="/newsletter/">Keep/Cut Weekly</a>'
        '<a href="/premium/">Premium</a>'
        '<a href="/premium/library/">Member library</a>'
        "</nav>"
        '<a class="nav-cta" href="/pricing/">Paid Premium $12/mo</a></header>'
    )


def footer() -> str:
    return (
        '<footer class="footer"><span>© 2026 AIToolsEssentials</span>'
        '<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>'
        f'<a href="mailto:{EMAIL}">Contact</a>'
        '<a href="/legal/about.html">About</a>'
        '<a href="/legal/privacy.html">Privacy</a>'
        '<a href="/legal/terms.html">Terms</a></footer>'
    )


def head(title: str, desc: str, canonical: str) -> str:
    return (
        "<head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f'<meta name="description" content="{esc(desc)}"><title>{esc(title)}</title>'
        f'<link rel="canonical" href="{canonical}">'
        f'<meta property="og:title" content="{esc(title)}">'
        f'<meta property="og:description" content="{esc(desc)}">'
        f'<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<link rel="stylesheet" href="/css/styles.css">'
        '<link rel="stylesheet" href="/css/share.css"></head>'
    )


def scripts() -> str:
    return '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def access_note(whop: dict[str, Any]) -> str:
    return (
        '<section class="score-card"><span>How access works</span>'
        "<h2>Whop bills the membership. This static site is not a login wall.</h2>"
        f"<p>AIToolsEssentials Premium is the paid membership: "
        f"{whop['trial_period_days']}-day free trial, then ${whop['price_usd_month']}/month via Whop. "
        f"Code <strong>{esc(whop['promo_code'])}</strong> is 50% off the first paid month for new users. "
        "Open the <a href=\"https://whop.com/hub\" rel=\"external noopener\">Whop member hub</a> "
        "with the email you used at checkout. These pages are readable here — this static site "
        "cannot hide them behind a login. Affiliate or sponsor status never "
        "changes keep/cut advice.</p>"
        f'<p><a class="button button-blue" href="{esc(whop["checkout_url"])}" rel="external noopener">'
        f'Join Premium on Whop (${whop["price_usd_month"]}/mo)</a>'
        f'<a class="button button-dark" href="{esc(whop["checkout_promo_url"])}" rel="external noopener" style="margin-left:8px">'
        f'Use code {esc(whop["promo_code"])}</a>'
        '<a class="button button-dark" href="/subscribe/" style="margin-left:8px">Free Keep/Cut Weekly</a>'
        '<a class="button button-dark" href="/stack-audit.html" style="margin-left:8px">Free Stack Audit</a></p>'
        "</section>"
    )


def lanes_note() -> str:
    return (
        '<p class="affiliate-inline">Three different things: '
        "<strong>Keep/Cut Weekly</strong> is the free Beehiiv email. "
        "<strong>Stack Audit</strong> is the free, no-login scorecard. "
        "<strong>Premium</strong> is the paid Whop membership.</p>"
    )


def write_csv(path: Path, headers: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(headers)
        w.writerows(rows)


def tools_list(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(tools, key=lambda t: (str(t.get("category") or ""), str(t.get("name") or "")))


def digest_alerts(root: Path) -> list[dict[str, str]]:
    path = root / "data" / "monthly_digests.json"
    if not path.exists():
        return []
    alerts: list[dict[str, str]] = []
    for digest in json.loads(path.read_text()):
        month = str(digest.get("month_label") or digest.get("slug") or "")
        checked = str(digest.get("checked_at") or "")
        for item in digest.get("new_listings") or []:
            alerts.append({
                "date": str(item.get("checked_at") or checked),
                "month": month,
                "tool": str(item.get("name") or ""),
                "kind": "New listing",
                "summary": str(item.get("note") or ""),
                "source": str(item.get("source_url") or "/updates/"),
            })
        for item in digest.get("vendor_launches") or []:
            alerts.append({
                "date": str(item.get("checked_at") or checked),
                "month": month,
                "tool": str(item.get("name") or ""),
                "kind": "Vendor launch",
                "summary": str(item.get("note") or ""),
                "source": str(item.get("source_url") or "/change-radar/"),
            })
        for item in digest.get("watch_list") or []:
            alerts.append({
                "date": str(item.get("checked_at") or checked),
                "month": month,
                "tool": str(item.get("name") or ""),
                "kind": "Watch / re-check",
                "summary": str(item.get("note") or ""),
                "source": str(item.get("source_url") or "/change-radar/"),
            })
    alerts.sort(key=lambda a: a.get("date") or "", reverse=True)
    return alerts


def overlap_pairs(tools: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any], str]]:
    by_slug = {str(t.get("slug")): t for t in tools}
    pairs = [
        ("chatgpt", "claude", "General writing / research assistants"),
        ("cursor", "github-copilot", "Coding assistants"),
        ("zapier-ai", "make", "Automation platforms"),
        ("fireflies", "otter-ai", "Meeting notes"),
        ("heygen", "synthesia", "Avatar / video generation"),
    ]
    out = []
    for a, b, job in pairs:
        if a in by_slug and b in by_slug:
            out.append((by_slug[a], by_slug[b], job))
    return out


def generate_hub(root: Path, tools: list[dict[str, Any]], today: str, whop: dict[str, Any]) -> None:
    out = root / "premium" / "library"
    out.mkdir(parents=True, exist_ok=True)
    n = len(tools)
    cards = [
        ("Research brief", "Dated keep/cut notes from the recorded September and August 2026 directory checks — official prices only.", "research-brief.html"),
        ("Decision matrix", f"All {n} tracked tools with official pricing labels, category, and best-for notes. CSV download included.", "decision-matrix.html"),
        ("Stack-audit template", "The paid worksheet that sits on top of the free instant scorecard: inventory, overlap, and a strategy-reply format.", "stack-audit-template.html"),
        ("Weekly checklist", "A 15-minute weekly rhythm so Premium is used, not collected.", "weekly-checklist.html"),
        ("Tool-change alerts", "Member-format feed built from the dated monthly digest — no invented launches.", "tool-change-alerts.html"),
        ("ROI worksheet", "Fill in your own hours and bills. The page does not invent savings.", "roi-worksheet.html"),
        ("How to access", "Whop hub, checkout, promo code, and what stays free.", "how-to-access.html"),
    ]
    grid = "".join(
        f'<article class="content-hub-card"><span>Member library</span><h3><a href="{href}">{esc(title)}</a></h3><p>{esc(text)}</p></article>'
        for title, text, href in cards
    )
    desc = (
        f"Public Premium member library: dated research brief, {n}-tool decision matrix, "
        "stack-audit template, weekly checklist, tool-change alerts, and ROI worksheet. "
        f"${whop['price_usd_month']}/month via Whop. Free Keep/Cut Weekly and free Stack Audit stay free."
    )
    page = f'''<!doctype html><html lang="en">{head("Premium member library", desc, DOMAIN + "/premium/library/")}
<body>{header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Paid Premium · member library</p>
<h1>Research you can run this week.</h1>
<p class="subhead">This is the $12/month Whop membership library — not the free newsletter and not the free instant Stack Audit. Open a brief, fill a worksheet, or download the matrix. Whop handles billing. This site does not pretend to check your login.</p>
{lanes_note()}
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
{access_note(whop)}
<h2>Library contents · generated {esc(today)}</h2>
<div class="content-hub-grid">{grid}</div>
<section class="score-card"><span>Editorial independence</span>
<h2>Paying never buys a ranking.</h2>
<p>Affiliate links, sponsor labels, and Premium membership do not change public scores, inclusion, or keep/cut advice. Research and strategy only — no implementation, credentials, or account access.</p>
</section>
</div></section>
</main>{footer()}{scripts()}</body></html>'''
    (out / "index.html").write_text(page)


def generate_research_brief(root: Path, tools: list[dict[str, Any]], today: str, whop: dict[str, Any]) -> None:
    digests = []
    digest_path = root / "data" / "monthly_digests.json"
    if digest_path.exists():
        digests = json.loads(digest_path.read_text())
    digest_blocks = []
    for digest in digests:
        listings = "".join(
            f"<li><strong>{esc(item.get('name'))}</strong> — {esc(item.get('note'))}</li>"
            for item in (digest.get("new_listings") or [])
        )
        launches = "".join(
            f"<li><strong>{esc(item.get('name'))}</strong> — {esc(item.get('note'))}</li>"
            for item in (digest.get("vendor_launches") or [])
        )
        watches = "".join(
            f"<li><strong>{esc(item.get('name'))}</strong> — {esc(item.get('note'))}</li>"
            for item in (digest.get("watch_list") or [])
        )
        digest_blocks.append(
            f'<article class="score-card"><span>{esc(digest.get("month_label"))} · checked {esc(digest.get("checked_at"))}</span>'
            f'<h3>{esc(digest.get("title"))}</h3><p>{esc(digest.get("summary"))}</p>'
            + (f"<h4>New listings</h4><ul>{listings}</ul>" if listings else "")
            + (f"<h4>Vendor launches</h4><ul>{launches}</ul>" if launches else "")
            + (f"<h4>Watch list</h4><ul>{watches}</ul>" if watches else "")
            + f"<p><strong>Keep/cut rule:</strong> {esc(digest.get('keep_cut_rule'))}</p></article>"
        )
    pair_rows = []
    for a, b, job in overlap_pairs(tools):
        pair_rows.append(
            f"<tr><td>{esc(job)}</td>"
            f'<td><a href="/tools/{esc(a.get("slug"))}/">{esc(a.get("name"))}</a><br><span class="muted">{esc(a.get("price"))}</span></td>'
            f'<td><a href="/tools/{esc(b.get("slug"))}/">{esc(b.get("name"))}</a><br><span class="muted">{esc(b.get("price"))}</span></td>'
            f"<td>Run one real weekly task in both. Keep the one you actually finish in. Official prices are labels, not your bill.</td></tr>"
        )
    pairs_table = (
        '<div class="table-wrap"><table><thead><tr><th>Weekly job</th><th>Tool A · official price label</th>'
        "<th>Tool B · official price label</th><th>Member action</th></tr></thead><tbody>"
        + "".join(pair_rows)
        + "</tbody></table></div>"
    )
    desc = (
        "September 2026 Premium research brief: dated directory checks, official price labels "
        "for common overlap pairs, and keep/cut rules. No invented savings."
    )
    page = f'''<!doctype html><html lang="en">{head("Premium research brief — September 2026", desc, DOMAIN + "/premium/library/research-brief.html")}
<body>{header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Member research brief · generated {esc(today)}</p>
<h1>What changed, and which overlap to test.</h1>
<p class="subhead">Built from the recorded monthly digests and official price labels already on this site. No case studies. No invented dollar savings. If a launch has no public price, it is not a buy decision.</p>
{lanes_note()}
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
{access_note(whop)}
<h2>Recorded month notes</h2>
{''.join(digest_blocks) or "<p>No monthly digest records were found.</p>"}
<h2>Common overlap pairs — official labels only</h2>
<p>These pairs share a weekly job in the directory. The action is a real-task test, not a ranking. Confirm the current official page before you renew.</p>
{pairs_table}
<section class="score-card"><span>What this brief will not do</span>
<p>It will not invent how much you will save. It will not tell you a tool is cheaper than your actual invoice. It will not change because a vendor is an affiliate.</p>
<p><a href="/premium/library/decision-matrix.html">Open the full decision matrix</a> · <a href="/premium/library/tool-change-alerts.html">Open the alert feed</a> · <a href="/updates/">Public monthly digest</a></p>
</section>
</div></section>
</main>{footer()}{scripts()}</body></html>'''
    (root / "premium" / "library" / "research-brief.html").write_text(page)


def generate_decision_matrix(root: Path, tools: list[dict[str, Any]], today: str, whop: dict[str, Any]) -> None:
    rows_html = []
    csv_rows = []
    for t in tools_list(tools):
        price = t.get("price") or ""
        pressure = (
            "free-first" if "free" in str(price).lower()
            else "paid-only" if "paid" in str(price).lower()
            else "verify official page"
        )
        rows_html.append(
            f'<tr><td><a href="/tools/{esc(t.get("slug"))}/">{esc(t.get("name"))}</a></td>'
            f'<td>{esc(t.get("category"))}</td><td>{esc(price)}</td>'
            f'<td>{esc(t.get("best_for"))}</td><td>{esc(pressure)}</td>'
            f'<td>{esc(t.get("rating"))}</td></tr>'
        )
        csv_rows.append([
            t.get("name"), t.get("slug"), t.get("category"), price,
            t.get("rating"), pressure, t.get("best_for"), t.get("summary"),
        ])
    public_csv = root / "downloads" / "premium" / f"premium-tool-decision-matrix-{today[:7]}.csv"
    write_csv(
        public_csv,
        ["name", "slug", "category", "pricing", "editorial_score", "pricing_pressure", "best_for", "summary"],
        csv_rows,
    )
    desc = (
        f"Premium decision matrix for {len(tools)} tracked AI tools. Official pricing labels, "
        "category, and best-for notes from the directory. Refreshed from data/tools.json."
    )
    page = f'''<!doctype html><html lang="en">{head("Premium decision matrix", desc, DOMAIN + "/premium/library/decision-matrix.html")}
<body>{header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Member decision matrix · {esc(today)}</p>
<h1>{len(tools)} tools. Official labels. Sort before you renew.</h1>
<p class="subhead">This is the monthly Premium matrix as an HTML table plus CSV. Editorial scores are not benchmarks. Pricing text is the directory label — confirm the vendor page before you pay.</p>
{lanes_note()}
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
{access_note(whop)}
<p><a class="button button-blue" href="/downloads/premium/{esc(public_csv.name)}">Download CSV</a>
<a class="button button-dark" href="/pricing-watch/" style="margin-left:8px">Public Pricing Watch</a></p>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Category</th><th>Official price label</th><th>Best for</th><th>Pricing pressure</th><th>Editorial score</th></tr></thead><tbody>{''.join(rows_html)}</tbody></table></div>
</div></section>
</main>{footer()}{scripts()}</body></html>'''
    (root / "premium" / "library" / "decision-matrix.html").write_text(page)


def generate_stack_audit_template(root: Path, today: str, whop: dict[str, Any]) -> None:
    fields = [
        ("Role / team size", "e.g. solo consultant, 5-person agency"),
        ("Known monthly AI spend", "Sum only bills you can see. Leave unknown spend blank."),
        ("Tool name", "One row per paid or weekly tool"),
        ("What you pay", "Your invoice, not the directory sticker"),
        ("Hours used last week", "Honest number, including zero"),
        ("Weekly job it owns", "One sentence"),
        ("Could another tool you already pay for do this job?", "Name it or write no"),
        ("Biggest overlap", "Which two tools share a weekly job?"),
        ("Most expensive rarely used tool", "Cancel candidate"),
        ("Privacy / data constraint", "Client data, NDA, health, legal"),
        ("Renewal dates you know", "Leave blank if unknown — do not guess"),
    ]
    field_rows = "".join(
        f'<tr><th>{esc(label)}</th><td><input class="sa-search" type="text" aria-label="{esc(label)}" placeholder="{esc(hint)}"></td></tr>'
        for label, hint in fields
    )
    desc = (
        "Premium stack-audit template: inventory, overlap, and strategy-reply format. "
        "The free instant Stack Audit stays free at /stack-audit.html."
    )
    page = f'''<!doctype html><html lang="en">{head("Premium stack-audit template", desc, DOMAIN + "/premium/library/stack-audit-template.html")}
<body>{header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Member stack-audit template · {esc(today)}</p>
<h1>Free scorecard first. Premium worksheet second.</h1>
<p class="subhead">The free <a href="/stack-audit.html">Stack Audit</a> is an instant, no-login scorecard. This Premium template is the deeper inventory you send for a strategy-only keep/cut/trial reply. It is not a second paid product.</p>
{lanes_note()}
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
{access_note(whop)}
<div class="score-card"><span>What stays free</span>
<ul>
<li><strong>Free Stack Audit</strong> — instant keep/cut/overlap score on your device. No account.</li>
<li><strong>Free Keep/Cut Weekly</strong> — one Beehiiv email a week.</li>
<li><strong>Paid Premium</strong> — this worksheet, the matrix, alerts, and a written strategy reply after you send the completed inventory. Research only. No logins taken.</li>
</ul>
<p><a class="button button-dark" href="/stack-audit.html">Run the free instant audit</a></p>
</div>
<h2>Fill this on the page, then print or copy</h2>
<p>Nothing is submitted to AIToolsEssentials from this form. Print it, or paste answers into a Whop reply / email to {esc(EMAIL)} with subject “Premium stack audit”.</p>
<div class="table-wrap"><table><thead><tr><th>Field</th><th>Your answer</th></tr></thead><tbody>{field_rows}</tbody></table></div>
<p style="margin-top:18px"><button class="button button-blue" type="button" onclick="window.print()">Print / PDF</button></p>
<section class="score-card"><span>Strategy reply format</span>
<h3>What a Premium reply looks like</h3>
<p>Keep / cut / trial / do-not-start per named tool. Official price labels cited when used. Unknown spend stays unknown. No fabricated savings. No implementation. Reply target is 48 hours after a complete inventory arrives — that is an editorial SLA, not a login into your accounts.</p>
</section>
</div></section>
</main>{footer()}{scripts()}</body></html>'''
    (root / "premium" / "library" / "stack-audit-template.html").write_text(page)


def generate_weekly_checklist(root: Path, today: str, whop: dict[str, Any]) -> None:
    days = [
        ("Mon", "Read the tool-change alert feed for tools you already pay for", "Catch a plan-name or price-label change before renewal."),
        ("Mon", "Skim Pricing Watch only for tools on your inventory", "Public dated snapshots. Do not treat directory labels as invoices."),
        ("Tue", "Run one real task in your primary assistant", "Notice limit hits and edit burden. Do not start a second assistant today."),
        ("Wed", "Mark overlap: two tools, one weekly job", "If both are paid, schedule a real-task bake-off, not a demo."),
        ("Thu", "Test one candidate replacement on the same real task", "Keep notes. Affiliate status must not decide the winner."),
        ("Fri", "Log friction, unused seats, and unknown spend", "Unknown stays unknown. Do not invent a monthly total."),
        ("Sun", "Decide one cancel, one keep, or one trial for next week", "Act on the log. If nothing changed, write that down too."),
    ]
    rows = "".join(
        f"<tr><td>{esc(day)}</td><td>{esc(task)}</td><td>{esc(why)}</td><td><input type=\"checkbox\" aria-label=\"Done {esc(day)}\"></td></tr>"
        for day, task, why in days
    )
    desc = "Premium weekly AI stack checklist: 15-minute keep/cut rhythm. Free newsletter and free Stack Audit stay free."
    page = f'''<!doctype html><html lang="en">{head("Premium weekly stack checklist", desc, DOMAIN + "/premium/library/weekly-checklist.html")}
<body>{header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Member weekly checklist · {esc(today)}</p>
<h1>Fifteen minutes. One decision.</h1>
<p class="subhead">Print this. Check boxes locally. Nothing is uploaded. Premium is an operating rhythm, not a PDF collection.</p>
{lanes_note()}
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
{access_note(whop)}
<div class="table-wrap"><table><thead><tr><th>Day</th><th>Task</th><th>Why</th><th>Done</th></tr></thead><tbody>{rows}</tbody></table></div>
<p style="margin-top:18px"><button class="button button-blue" type="button" onclick="window.print()">Print / PDF</button>
<a class="button button-dark" href="/premium/library/tool-change-alerts.html" style="margin-left:8px">This week’s alert format</a></p>
</div></section>
</main>{footer()}{scripts()}</body></html>'''
    (root / "premium" / "library" / "weekly-checklist.html").write_text(page)


def generate_alerts(root: Path, today: str, whop: dict[str, Any]) -> None:
    alerts = digest_alerts(root)
    rows = []
    csv_rows = []
    for item in alerts:
        src = item["source"]
        src_html = (
            f'<a href="{esc(src)}" rel="external noopener">{esc(src)}</a>'
            if src.startswith("http")
            else f'<a href="{esc(src)}">{esc(src)}</a>'
        )
        rows.append(
            f'<tr><td>{esc(item["date"])}</td><td>{esc(item["tool"])}</td>'
            f'<td>{esc(item["kind"])}</td><td>{esc(item["summary"])}</td><td>{src_html}</td></tr>'
        )
        csv_rows.append([item["date"], item["tool"], item["kind"], item["summary"], item["source"], item["month"]])
    write_csv(
        root / "downloads" / "premium" / f"tool-change-alerts-{today[:7]}.csv",
        ["date", "tool", "kind", "summary", "source", "month"],
        csv_rows,
    )
    desc = (
        "Premium tool-change alert feed formatted from dated monthly digests. "
        "No invented launches or prices."
    )
    page = f'''<!doctype html><html lang="en">{head("Premium tool-change alerts", desc, DOMAIN + "/premium/library/tool-change-alerts.html")}
<body>{header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Member alert feed · {esc(today)}</p>
<h1>Recorded changes, member format.</h1>
<p class="subhead">{len(alerts)} dated rows from the public monthly digest. This page is the Premium layout — same facts, sorted for people who already pay for a stack. If a source is missing a dollar price, this feed will not invent one.</p>
{lanes_note()}
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
{access_note(whop)}
<p><a class="button button-blue" href="/downloads/premium/tool-change-alerts-{esc(today[:7])}.csv">Download CSV</a>
<a class="button button-dark" href="/change-radar/" style="margin-left:8px">Public change radar</a>
<a class="button button-dark" href="/updates/" style="margin-left:8px">Public monthly digest</a></p>
<div class="table-wrap"><table><thead><tr><th>Date</th><th>Tool</th><th>Kind</th><th>Recorded note</th><th>Source</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</div></section>
</main>{footer()}{scripts()}</body></html>'''
    (root / "premium" / "library" / "tool-change-alerts.html").write_text(page)


def generate_roi(root: Path, today: str, whop: dict[str, Any]) -> None:
    desc = (
        "Premium ROI worksheet. Enter your own hours and invoices. "
        "The page does not invent time saved or dollar payback."
    )
    page = f'''<!doctype html><html lang="en">{head("Premium ROI worksheet", desc, DOMAIN + "/premium/library/roi-worksheet.html")}
<body>{header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Member ROI worksheet · {esc(today)}</p>
<h1>Your numbers. Not ours.</h1>
<p class="subhead">Fill the fields. Arithmetic stays in your browser. This worksheet will not claim that Premium saved you money. Premium costs ${whop["price_usd_month"]}/month after the trial. If your own cancelled seats exceed that, you can write it down.</p>
{lanes_note()}
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
{access_note(whop)}
<div class="score-card" id="roi-sheet">
<label class="sa-field" for="roi-spend">Known monthly AI spend (USD)</label>
<input class="sa-search" id="roi-spend" type="number" min="0" step="0.01" inputmode="decimal">
<label class="sa-field" for="roi-hours">Hours you believe you saved last week (your estimate)</label>
<input class="sa-search" id="roi-hours" type="number" min="0" step="0.1" inputmode="decimal">
<label class="sa-field" for="roi-rate">Your hourly rate (USD, optional)</label>
<input class="sa-search" id="roi-rate" type="number" min="0" step="0.01" inputmode="decimal">
<label class="sa-field" for="roi-overlap">Known overlap spend you may cut (USD, only if you have the invoices)</label>
<input class="sa-search" id="roi-overlap" type="number" min="0" step="0.01" inputmode="decimal">
<p id="roi-out" class="sa-note">Enter known figures. Empty fields stay empty — they are not treated as zero savings.</p>
</div>
<section class="score-card"><span>How to read the math</span>
<ul>
<li>Monthly time value = hours/week × 4.3 × hourly rate — only if you typed both hours and rate.</li>
<li>Net vs tool spend = time value − known monthly spend — only if both sides exist.</li>
<li>Premium itself is ${whop["price_usd_month"]}/month after the {whop["trial_period_days"]}-day trial. That is a cost, not a saving.</li>
<li>Do not treat directory stickers as invoices. Do not treat this as financial advice.</li>
</ul>
</section>
</div></section>
</main>{footer()}
<script>
(function () {{
  function num(id) {{
    var el = document.getElementById(id);
    if (!el || el.value === "") return null;
    var n = Number(el.value);
    return Number.isFinite(n) ? n : null;
  }}
  function money(n) {{ return "$" + n.toFixed(2); }}
  function render() {{
    var spend = num("roi-spend");
    var hours = num("roi-hours");
    var rate = num("roi-rate");
    var overlap = num("roi-overlap");
    var bits = [];
    if (hours !== null && rate !== null) {{
      var value = hours * 4.3 * rate;
      bits.push("Your estimated monthly time value from the hours and rate you typed: " + money(value) + ".");
      if (spend !== null) {{
        bits.push("Time value minus known spend: " + money(value - spend) + ". This is your arithmetic, not a claim by AIToolsEssentials.");
      }}
    }} else {{
      bits.push("Time value is blank until you enter both hours and an hourly rate.");
    }}
    if (spend === null) bits.push("Known monthly spend is blank.");
    if (overlap !== null) {{
      bits.push("Known overlap you may cut: " + money(overlap) + ". Compare that yourself to Premium at ${whop["price_usd_month"]}/month. No payback is assumed.");
    }}
    document.getElementById("roi-out").textContent = bits.join(" ");
  }}
  ["roi-spend", "roi-hours", "roi-rate", "roi-overlap"].forEach(function (id) {{
    var el = document.getElementById(id);
    if (el) el.addEventListener("input", render);
  }});
}})();
</script>
{scripts()}</body></html>'''
    (root / "premium" / "library" / "roi-worksheet.html").write_text(page)


def generate_access(root: Path, today: str, whop: dict[str, Any]) -> None:
    desc = (
        "How to join AIToolsEssentials Premium on Whop, open the member hub, "
        "and keep the free newsletter and free Stack Audit separate."
    )
    page = f'''<!doctype html><html lang="en">{head("How to access Premium", desc, DOMAIN + "/premium/library/how-to-access.html")}
<body>{header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Paid Premium · access</p>
<h1>Whop is checkout. These pages are the library.</h1>
<p class="subhead">Use the existing Premium checkout. Do not pay for the free newsletter or the free Stack Audit — those stay free.</p>
{lanes_note()}
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
<div class="content-hub-grid">
<article class="content-hub-card"><span>Free</span><h3>Keep/Cut Weekly</h3><p>Beehiiv email. No Whop charge.</p><p><a href="/subscribe/">Subscribe free</a></p></article>
<article class="content-hub-card"><span>Free</span><h3>Stack Audit</h3><p>Instant scorecard. Stays on your device.</p><p><a href="/stack-audit.html">Run it free</a></p></article>
<article class="content-hub-card"><span>Paid</span><h3>Premium membership</h3><p>{whop["trial_period_days"]}-day trial, then ${whop["price_usd_month"]}/month. Code {esc(whop["promo_code"])} for 50% off the first paid month (new users).</p><p><a href="{esc(whop["checkout_url"])}" rel="external noopener">Join Premium on Whop (${whop["price_usd_month"]}/mo)</a></p></article>
</div>
<ol>
<li>Open the Whop checkout for <strong>AIToolsEssentials Premium</strong>. Product page: <a href="{esc(whop["product_url"])}" rel="external noopener">{esc(whop["product_url"])}</a>.</li>
<li>Complete the {whop["trial_period_days"]}-day trial or apply <strong>{esc(whop["promo_code"])}</strong> on the first paid month if you are a new user.</li>
<li>Open <a href="{esc(whop["hub_url"])}" rel="external noopener">whop.com/hub</a> with that email. Posts and upload-pack CSVs live there when George has published them.</li>
<li>Use this public library for the dated HTML and CSV files. There is no login cookie on aitoolsessentials.com that unlocks extra HTML.</li>
<li>Cancel from your Whop account. All sales are final — no refunds. Research and strategy only.</li>
</ol>
<p>Return URL after checkout: <a href="/checkout/complete/">/checkout/complete/</a>. That page cannot verify a charge by itself. Trust the Whop receipt.</p>
<p>Generated {esc(today)}. Plan id used on site buttons: <code>{esc(whop["plan_id"])}</code> (existing, not newly invented).</p>
</div></section>
</main>{footer()}{scripts()}</body></html>'''
    (root / "premium" / "library" / "how-to-access.html").write_text(page)


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    tools_list_data = tools if tools is not None else json.loads((root / "data" / "tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    whop = load_whop(root)
    (root / "premium" / "library").mkdir(parents=True, exist_ok=True)
    (root / "downloads" / "premium").mkdir(parents=True, exist_ok=True)
    generate_hub(root, tools_list_data, today, whop)
    generate_research_brief(root, tools_list_data, today, whop)
    generate_decision_matrix(root, tools_list_data, today, whop)
    generate_stack_audit_template(root, today, whop)
    generate_weekly_checklist(root, today, whop)
    generate_alerts(root, today, whop)
    generate_roi(root, today, whop)
    generate_access(root, today, whop)
    return 8


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    print("premium library pages:", generate(root))
