#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from send_keep_cut import FROM_ADDRESS
from validate_site import OLD_PUBLICATION_NAME, publication_name_errors

REPO = Path(__file__).resolve().parent.parent
NEW_NAME = "Keep, Test, Cut"
LIVE_FROM = "Keep, Test, Cut <weekly@news.aitoolsessentials.com>"


def main() -> None:
    errors: list[str] = []
    found = publication_name_errors(REPO)
    if found:
        errors.extend(found)
    cfg = json.loads((REPO / "data" / "newsletter.json").read_text(encoding="utf-8"))
    if cfg.get("publication_name") != NEW_NAME:
        errors.append("publication_name is not Keep, Test, Cut")
    if cfg.get("signup_url") != "/subscribe/":
        errors.append("signup_url changed")
    archive = (REPO / "newsletter" / "index.html").read_text(encoding="utf-8")
    if f'<p class="newsletter-name">{NEW_NAME}</p>' not in archive:
        errors.append("newsletter archive masthead is not Keep, Test, Cut")
    if 'href="https://aitoolsessentials.com/newsletter/"' not in archive:
        errors.append("newsletter archive path changed")
    issue = (REPO / "newsletter" / "2026-w35.html").read_text(encoding="utf-8")
    if f'<p class="newsletter-name">{NEW_NAME}</p>' not in issue:
        errors.append("issue masthead is not Keep, Test, Cut")
    if "The AI bill you forgot to cancel" not in issue:
        errors.append("issue 1 body was rewritten")
    if OLD_PUBLICATION_NAME in issue:
        errors.append("issue 1 still says the retired name")
    subscribe = (REPO / "subscribe" / "index.html").read_text(encoding="utf-8")
    if f"<h1>{NEW_NAME}.</h1>" not in subscribe and f"<title>Subscribe — {NEW_NAME}" not in subscribe:
        errors.append("subscribe page does not use Keep, Test, Cut")
    sponsor = (REPO / "sponsor" / "index.html").read_text(encoding="utf-8")
    if "Sponsored by" not in sponsor or NEW_NAME not in sponsor:
        errors.append("sponsor tier copy does not name Keep, Test, Cut")
    worker = (REPO / "workers" / "newsletter-subscribe" / "worker.js").read_text(encoding="utf-8")
    if 'subject: "Confirm Keep, Test, Cut"' not in worker:
        errors.append("confirm subject is not Confirm Keep, Test, Cut")
    if OLD_PUBLICATION_NAME in worker:
        errors.append("worker still says the retired name")
    if FROM_ADDRESS != LIVE_FROM:
        errors.append(f"sender display name is {FROM_ADDRESS}")
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
