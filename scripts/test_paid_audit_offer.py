#!/usr/bin/env python3
"""Guard the paid AI Stack Audit offer.

Regression this exists to prevent: the $497 audit was built, delivered, then folded into the
$12/mo Premium membership (commit 5f0ca9c9), and ended up on ZERO public pages. Roughly 29
visits/month were reaching offer pages and being offered a $12 subscription instead of a $497
service. Nothing failed loudly - the offer simply disappeared from the site while the code that
delivered it stayed in the repo.

These assertions make that failure mode impossible to repeat silently.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRICE = "497"
PAGES = [
    "services/paid-audit.html",
    "services/audit-intake.html",
    "services/sample-audit.html",
    "services/audit-standard.html",
    "services/intake-received.html",
]
# Pages already receiving offer traffic. The paid audit must be reachable from each.
REACHABLE_FROM = [
    "pricing/index.html",
    "premium/index.html",
    "stack-audit.html",
    "services/ai-stack-audit.html",
]
ACTIVATED_ENDPOINT = "formsubmit.co/eb3d1bf5a35125c06383cafa247af931"


def main() -> None:
    errors: list[str] = []

    for rel in PAGES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing paid audit page: {rel}")
            continue
        html = path.read_text(errors="ignore")
        if "</html>" not in html.lower():
            errors.append(f"{rel} is truncated")
        if 'name="robots" content="noindex' in html:
            errors.append(f"{rel} is noindex — a purchasable offer must be indexable")
        if 'rel="canonical"' not in html:
            errors.append(f"{rel} missing canonical")

    # The price must be visible on the page that sells it.
    service = (ROOT / "services" / "paid-audit.html")
    if service.exists():
        text = service.read_text(errors="ignore")
        if f"${PRICE}" not in text:
            errors.append(f"services/paid-audit.html does not state ${PRICE}")
        # Discovery requirement must be stated, not just the deliverables.
        if "discovery" not in text.lower():
            errors.append("paid-audit.html must state the discovery requirement")

    # The intake must carry every required discovery field. These are exactly the blanks that
    # made the first audit useless to the client.
    intake = ROOT / "services" / "audit-intake.html"
    if intake.exists():
        html = intake.read_text(errors="ignore")
        if ACTIVATED_ENDPOINT not in html:
            errors.append("intake must post to the ACTIVATED formsubmit endpoint")
        # mail_triage routes "intake" + "paid"/"$497" to the paid queue; keep that contract.
        if "intake" not in html.lower():
            errors.append("intake page must keep 'intake' in the subject for mail routing")
        for field in ("systems", "owners", "costs", "workflows", "bottleneck", "current_answer"):
            if f'name="{field}"' not in html:
                errors.append(f"intake missing required discovery field: {field}")
            elif not re.search(rf'name="{field}"[^>]*required', html):
                errors.append(f"intake field not required: {field}")

    # Every page that already gets offer traffic must reach the paid audit.
    for rel in REACHABLE_FROM:
        path = ROOT / rel
        if not path.exists():
            continue
        html = path.read_text(errors="ignore")
        if "/services/paid-audit.html" not in html:
            errors.append(f"{rel} does not link to /services/paid-audit.html")

    # The crosslink block must appear exactly once per target (a doubled block means the pass
    # is not marker-idempotent).
    for rel in REACHABLE_FROM:
        path = ROOT / rel
        if not path.exists():
            continue
        n = path.read_text(errors="ignore").count("AIT PAID AUDIT CROSSLINK START")
        if n > 1:
            errors.append(f"{rel} has {n} paid-audit crosslink blocks (must be ≤1)")

    # The three-lane ladder must stay legible: someone must be able to tell the $497 audit from
    # the $12 membership from the free scorecard.
    if service.exists():
        text = service.read_text(errors="ignore")
        for lane in ("Free instant audit", "Premium keep/cut pack", "This written audit"):
            if lane not in text:
                errors.append(f"paid-audit.html missing the lane comparison entry: {lane}")

    # Scope boundary must be stated on the page that takes money.
    if service.exists():
        text = service.read_text(errors="ignore").lower()
        for phrase in ("no implementation", "no access"):
            if phrase not in text:
                errors.append(f"paid-audit.html must state the scope boundary ({phrase})")

    if errors:
        raise SystemExit("paid audit guard failures:\n- " + "\n- ".join(errors))
    print("paid audit guard ok")


if __name__ == "__main__":
    main()
