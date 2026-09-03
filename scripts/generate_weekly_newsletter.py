#!/usr/bin/env python3
"""Weekly Keep/Cut newsletter: public archive + Beehiiv paste HTML."""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
LOGO = f"{DOMAIN}/assets/aitools-bot-logo-256.png"
HEADER = '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/newsletter/">Keep/Cut Weekly</a><a href="/subscribe/">Subscribe</a><a href="/premium/">Premium</a></nav><a class="nav-cta" href="/subscribe/">Subscribe</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/privacy.html">Privacy</a></footer>'


def esc(s: object) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def tool_href(slug: str) -> str:
    return f"{DOMAIN}/tools/{esc(slug)}/"


def listings_html(items: list, public: bool) -> str:
    bits = []
    for x in items:
        href = f"/tools/{esc(x['slug'])}/" if public else tool_href(x["slug"])
        bits.append(f"<li><a href=\"{href}\">{esc(x['name'])}</a> — {esc(x['note'])}</li>")
    return "<ul>" + "".join(bits) + "</ul>" if bits else "<p>None recorded this week. Extraordinary restraint.</p>"


def beehiiv_html(issue: dict, cfg: dict) -> str:
    logo = esc(cfg.get("logo_url") or LOGO)
    name = esc(cfg.get("publication_name") or "Keep/Cut Weekly")
    keep = issue.get("keep_one") or {}
    keep_url = keep.get("url") or ""
    if keep_url.startswith("/"):
        keep_url = DOMAIN + keep_url
    
    # Pricing changes section
    pricing_items = issue.get("pricing_changes") or []
    if pricing_items:
        pricing_rows = "\n".join(
            f'<tr><td style="padding:10px 12px;border-bottom:1px solid #1c1c1e;font-size:14px;color:#f5f5f7;"><a href="{DOMAIN}/tools/{esc(p.get("slug"))}/" style="color:#64b5ff;text-decoration:none;">{esc(p.get("name"))}</a></td><td style="padding:10px 12px;border-bottom:1px solid #1c1c1e;font-size:13px;color:#d2d2d7;">{esc(p.get("change"))}</td></tr>'
            for p in pricing_items
        )
        pricing_section = f'''<h2 style="margin:28px 0 10px;font-size:18px;color:#f5f5f7;">Pricing Watch — confirmed changes</h2>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#121214;border-radius:12px;overflow:hidden;margin-bottom:24px;">
<thead><tr style="background:#1c1c1e;"><th style="padding:10px 12px;text-align:left;font-size:13px;color:#8e8e93;font-weight:600;text-transform:uppercase;letter-spacing:.05em;">Tool</th><th style="padding:10px 12px;text-align:left;font-size:13px;color:#8e8e93;font-weight:600;text-transform:uppercase;letter-spacing:.05em;">What changed</th></tr></thead>
<tbody>{pricing_rows}</tbody>
</table>
<p style="margin:0 0 20px;font-size:13px;color:#8e8e93;">Verified from official pricing pages on {esc(issue.get("checked_at"))}. Full tracker: <a href="{DOMAIN}/pricing-watch/" style="color:#64b5ff;">AI Pricing Watch</a>. Premium members get alerts first.</p>'''
    else:
        pricing_section = ""
    
    return f'''<!doctype html>
<html><body style="margin:0;padding:0;background:#0b0b0c;color:#f5f5f7;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',Helvetica,Arial,sans-serif;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0b0b0c;"><tr><td align="center" style="padding:32px 16px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
<tr><td style="padding:0 0 24px;text-align:center;">
<img src="{logo}" width="72" height="72" alt="AIToolsEssentials" style="border-radius:18px;display:block;margin:0 auto 12px;">
<p style="margin:0;letter-spacing:.18em;text-transform:uppercase;font-size:11px;color:#8e8e93;">{name}</p>
<p style="margin:8px 0 0;font-size:13px;color:#8e8e93;">Issue {esc(issue.get("issue"))} · {esc(issue.get("week_label"))}</p>
</td></tr>
<tr><td style="background:#121214;border-radius:20px;padding:32px 32px 8px;">
<h1 style="margin:0 0 14px;font-size:28px;line-height:1.2;color:#f5f5f7;font-weight:700;">{esc(issue.get("subject_line"))}</h1>
<p style="margin:0 0 18px;font-size:16px;line-height:1.6;color:#d2d2d7;">{esc(issue.get("lede"))}</p>
{f'<p style="margin:0 0 18px;font-size:13px;line-height:1.55;color:#8e8e93;">{esc(issue.get("verification"))}</p>' if issue.get("verification") else ""}
<div style="background:#0d1b2a;border-left:3px solid #0071E3;border-radius:0 10px 10px 0;padding:14px 16px;margin-bottom:24px;">
<p style="margin:0;font-size:15px;line-height:1.55;color:#f5f5f7;"><strong style="color:#64b5ff;">Standing order.</strong> {esc(issue.get("keep_cut_rule"))}</p>
</div>
{pricing_section}
<h2 style="margin:28px 0 10px;font-size:18px;color:#f5f5f7;">New on the directory</h2>
{listings_html(issue.get("new_listings") or [], public=False)}
<h2 style="margin:28px 0 10px;font-size:18px;color:#f5f5f7;">Re-check before you renew</h2>
{listings_html(issue.get("watch_list") or [], public=False)}
<h2 style="margin:28px 0 10px;font-size:18px;color:#f5f5f7;">Keep-one of the week</h2>
<p style="margin:0 0 8px;font-size:16px;line-height:1.55;color:#d2d2d7;"><a href="{esc(keep_url)}" style="color:#64b5ff;text-decoration:none;">{esc(keep.get("title"))}</a>. {esc(keep.get("rule"))}</p>
<p style="margin:0 0 8px;font-size:15px;line-height:1.55;color:#d2d2d7;"><strong style="color:#f5f5f7;">Protocol.</strong> {esc(issue.get("protocol"))}</p>
<p style="margin:24px 0 8px;font-size:15px;line-height:1.55;color:#d2d2d7;">Public archive: <a href="{DOMAIN}/newsletter/" style="color:#64b5ff;">Newsletter archive</a>. Free tools stay free. <a href="{DOMAIN}/premium/" style="color:#64b5ff;">Premium</a> is a separate $12 research membership — 7-day trial, code LAUNCH50 — not this newsletter.</p>
<p style="margin:0 0 28px;font-size:15px;line-height:1.55;color:#d2d2d7;">{esc(issue.get("signoff"))}</p>
</td></tr>
<tr><td style="padding:24px 8px 0;text-align:center;font-size:12px;line-height:1.6;color:#8e8e93;border-top:1px solid #1c1c1e;">
One email a week. Not a drip. Not a vendor inbox. <a href="{DOMAIN}/legal/affiliate-disclosure.html" style="color:#8e8e93;">Affiliate disclosure</a>. Confirm prices on official pages before you pay.<br>
Beehiiv adds the unsubscribe link in the footer. We do not send daily mail. FormSubmit is not this list.
</td></tr>
</table>
</td></tr></table>
</body></html>
'''


def public_page(issue: dict, cfg: dict) -> str:
    keep = issue.get("keep_one") or {}
    logo = esc(cfg.get("logo_url") or "/assets/aitools-bot-logo-256.png")
    if logo.startswith("http"):
        logo_src = logo
    else:
        logo_src = logo
    desc = issue.get("preview") or issue.get("lede") or ""
    
    # Pricing changes section for public page
    pricing_items = issue.get("pricing_changes") or []
    if pricing_items:
        pricing_rows = "\n".join(
            f'<li><a href="/tools/{esc(p.get("slug"))}/">{esc(p.get("name"))}</a> — {esc(p.get("change"))}</li>'
            for p in pricing_items
        )
        pricing_section = f'<h2>Pricing Watch — confirmed changes</h2><ul>{pricing_rows}</ul><p style="color:#6e6e73;font-size:14px;">Verified from official pricing pages on {esc(issue.get("checked_at"))}. <a href="/pricing-watch/">Full tracker</a>. Premium members get alerts first.</p>'
    else:
        pricing_section = ""
    
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(issue.get("subject"))} | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/newsletter/{esc(issue["slug"])}.html"><link rel="stylesheet" href="/css/styles.css"></head><body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center">
<img src="{logo_src}" alt="AIToolsEssentials" width="72" height="72" style="border-radius:18px">
<p class="kicker light">Keep/Cut Weekly · Issue {esc(issue.get("issue"))} · checked {esc(issue.get("checked_at"))}</p>
<h1>{esc(issue.get("subject_line"))}</h1>
<p class="subhead">{esc(issue.get("lede"))}</p>
{f'<p class="affiliate-inline">{esc(issue.get("verification"))}</p>' if issue.get("verification") else ""}
<p><a class="button button-blue" href="/subscribe/">Get next week</a></p>
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
<div class="score-card"><span>Standing order</span><h2>{esc(issue.get("keep_cut_rule"))}</h2></div>
{pricing_section}
<h2>New on the directory</h2>{listings_html(issue.get("new_listings") or [], public=True)}
<h2>Re-check before you renew</h2>{listings_html(issue.get("watch_list") or [], public=True)}
<h2>Keep-one of the week</h2>
<p><a href="{esc(keep.get("url"))}">{esc(keep.get("title"))}</a>. {esc(keep.get("rule"))}</p>
<p><strong>Protocol.</strong> {esc(issue.get("protocol"))}</p>
<p>{esc(issue.get("signoff"))}</p>
<p>Related: <a href="/updates/2026-08.html">August digest</a> · <a href="/subscribe/">Subscribe (Beehiiv, weekly only)</a> · <a href="/premium/">Premium research membership</a></p>
</div></section>
</main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''


def generate(root: Path) -> int:
    issues = json.loads((root / "data/weekly_issues.json").read_text())
    cfg = json.loads((root / "data/newsletter.json").read_text())
    out = root / "newsletter"
    out.mkdir(exist_ok=True)
    pack = root / "admin/newsletter"
    pack.mkdir(parents=True, exist_ok=True)
    cards = []
    for issue in issues:
        slug = issue["slug"]
        (out / f"{slug}.html").write_text(public_page(issue, cfg))
        (pack / f"{slug}-beehiiv.html").write_text(beehiiv_html(issue, cfg))
        (pack / f"{slug}-subject.txt").write_text(
            f"{issue.get('subject')}\nPREVIEW: {issue.get('preview')}\n"
        )
        cards.append(
            f'<article class="content-hub-card"><span>Issue {esc(issue.get("issue"))}</span><h3><a href="/newsletter/{esc(slug)}.html">{esc(issue.get("week_label"))}</a></h3><p>{esc(issue.get("preview"))}</p></article>'
        )
    desc = cfg.get("description") or "Weekly keep/cut newsletter."
    logo = esc(cfg.get("logo_url") or "/assets/aitools-bot-logo-256.png")
    hub = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(desc)}"><title>Keep/Cut Weekly | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/newsletter/"><link rel="stylesheet" href="/css/styles.css"></head><body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center">
<img src="{logo}" alt="AIToolsEssentials" width="72" height="72" style="border-radius:18px">
<p class="kicker light">Weekly newsletter</p>
<h1>Keep/Cut Weekly.</h1>
<p class="subhead">{esc(desc)}</p>
<p><a class="button button-blue" href="/subscribe/">Subscribe on Beehiiv</a></p>
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{"".join(cards)}</div></div></section>
</main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
    (out / "index.html").write_text(hub)
    return len(issues) + 1


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parent.parent))
