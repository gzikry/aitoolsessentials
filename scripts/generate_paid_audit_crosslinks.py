#!/usr/bin/env python3
"""Route existing traffic to the paid AI Stack Audit.

Why this exists
---------------
The paid audit was built, delivered, and then folded into the $12/mo Premium membership,
leaving it on zero public pages. Measured 2026-09-21: ~29 visits/month already reach offer
pages (/premium/, /stack-audit.html, /services/...) and were being offered a $12 subscription
instead of a $497 service. The traffic exists; the offer simply was not on it.

This module adds a marker-delimited block to those pages. Markers (not raw string replaces)
so the pass is idempotent and survives regeneration by other generators - the same discipline
used by the premium/affiliate modules.

Editorial discipline
--------------------
The paid audit is OUR product, not a third-party affiliate link, so `rel="sponsored"` would be
wrong here (sponsored declares paid placement by a third party). Internal product links use no
rel beyond noopener when opening a new tab. validate_site.py enforces the opposite direction
(affiliate hrefs MUST be sponsored), so these must not be added to the affiliate needle list.
"""
from __future__ import annotations

from pathlib import Path

MARK_S = "<!-- AIT PAID AUDIT CROSSLINK START -->"
MARK_E = "<!-- AIT PAID AUDIT CROSSLINK END -->"

AUDIT_HREF = "/services/paid-audit.html"
INTAKE_HREF = "/services/audit-intake.html"


def _block(context: str) -> str:
    """Context-specific pitch. One size does not fit all three lanes."""
    if context == "premium":
        body = (
            "Premium is built for the decision you make with a template. If your stack is larger, "
            "the bottleneck is unclear, or you want the answer priced against your own contracts, "
            "the written audit does that work with you."
        )
        cta = f'<a class="button button-ghost-dark" href="{AUDIT_HREF}">See the written audit</a>'
    elif context == "stack_audit":
        body = (
            "The scorecard tells you where the overlap is. It cannot tell you what the overlap "
            "costs, because it cannot see your invoices or renewal dates. The written audit can."
        )
        cta = f'<a class="button button-ghost-dark" href="{AUDIT_HREF}">What the written audit adds</a>'
    else:
        body = (
            "If you would rather have a written decision than a scorecard — keep/cut/defer priced "
            "against your actual subscriptions, with the bottleneck you ranked worked in depth."
        )
        cta = f'<a class="button button-ghost-dark" href="{AUDIT_HREF}">See the written audit</a>'
    return (
        f'{MARK_S}<section class="score-card"><span>If a scorecard is not enough</span>'
        f'<h2>Written AI Stack Audit — $497, one-time.</h2>'
        f'<p>{body}</p>'
        f'<p>{cta} <a class="text-link" href="{INTAKE_HREF}" style="margin-left:8px">Start the intake</a></p>'
        f'<p class="muted-small">Strategy and written recommendations only. No implementation, no '
        f'account access, no credentials or API keys. Not affiliated with any tool vendor.</p>'
        f'</section>{MARK_E}'
    )


def apply_crosslinks(root: Path) -> dict[str, int]:
    """Insert/replace the paid-audit block on the pages that already receive offer traffic."""
    targets: list[tuple[Path, str]] = [
        (root / "pricing" / "index.html", "pricing"),
        (root / "premium" / "index.html", "premium"),
        (root / "stack-audit.html", "stack_audit"),
        (root / "services" / "ai-stack-audit.html", "premium"),
        # The free/Premium intake and the $497 intake are two different forms. Without a link
        # across, someone who wanted the deeper service fills in the lighter questionnaire and
        # never learns the option exists — which reads as an upsell-by-omission once they do.
        (root / "services" / "intake-questionnaire.html", "premium"),
    ]
    stats = {"updated": 0, "skipped": 0}
    for path, context in targets:
        if not path.exists():
            stats["skipped"] += 1
            continue
        try:
            html = path.read_text()
        except (OSError, UnicodeDecodeError):
            stats["skipped"] += 1
            continue
        if MARK_S in html and MARK_E in html:
            # Replace in place so regeneration can never stack duplicates.
            start = html.index(MARK_S)
            end = html.index(MARK_E) + len(MARK_E)
            new_html = html[:start] + _block(context) + html[end:]
        else:
            # Prefer the end of <main>; fall back to before </body>.
            anchor = html.rfind("</main>")
            if anchor == -1:
                anchor = html.rfind("</body>")
            if anchor == -1:
                stats["skipped"] += 1
                continue
            new_html = html[:anchor] + _block(context) + "\n" + html[anchor:]
        if new_html != html:
            path.write_text(new_html)
            stats["updated"] += 1
    return stats


if __name__ == "__main__":
    import json
    root_path = Path(__file__).resolve().parents[1]
    print("crosslinks:", json.dumps(apply_crosslinks(root_path)))
