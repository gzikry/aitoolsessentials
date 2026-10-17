#!/usr/bin/env python3
"""Send one approved Keep/Cut issue as a Resend broadcast. Off unless the hold opens."""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_hold import POSTAL_ADDRESS, SENDING_DOMAIN, UNSUBSCRIBE_HREF, Held, hold

FROM_ADDRESS = f"Keep, Test, Cut <weekly@{SENDING_DOMAIN}>"
_SIGN = "\u2014 AIToolsEssentials"
_UNSUBSCRIBE = "{{{RESEND_UNSUBSCRIBE_URL}}}"
Post = Callable[[dict, str], dict]


@dataclass(frozen=True)
class Refused:
    reason: Literal["personal_name", "missing_issue", "missing_footer"]


def approved_file(root: Path, slug: str) -> bool:
    path = root / "admin" / "newsletter" / f"{slug}.approved"
    if not path.is_file():
        return False
    return path.read_text(encoding="utf-8").strip() == "approved"


def email_html(draft: str) -> str:
    html = draft.replace(UNSUBSCRIBE_HREF, _UNSUBSCRIBE)
    if _UNSUBSCRIBE not in html or POSTAL_ADDRESS not in html or _SIGN not in html:
        raise ValueError("missing_footer")
    if "george" in html.casefold():
        raise ValueError("personal_name")
    return html


def subject_line(root: Path, slug: str, draft: str) -> str:
    subject_path = root / "admin" / "newsletter" / f"{slug}-subject.txt"
    if subject_path.is_file():
        line = subject_path.read_text(encoding="utf-8").splitlines()
        if line and line[0].strip():
            return line[0].strip()
    match_start = draft.find("<h1")
    if match_start >= 0:
        inner = draft[match_start:].split(">", 1)[1].split("</h1>", 1)[0]
        text = inner.strip()
        if text:
            return text
    raise ValueError("missing_issue")


def post_broadcast(payload: dict, api_key: str) -> dict:
    req = urllib.request.Request(
        "https://api.resend.com/broadcasts",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def send_issue(
    root: Path,
    slug: str,
    env: Mapping[str, str] | None = None,
    *,
    post: Post | None = None,
) -> Held | Refused | dict:
    source = os.environ if env is None else env
    held = hold(source, approved=approved_file(root, slug))
    if held.reason != "no_transport":
        return held
    key = str(source.get("RESEND_API_KEY", "")).strip()
    segment = str(source.get("RESEND_SEGMENT_ID", "")).strip()
    if not key or not segment:
        return Held("no_transport")
    draft_path = root / "admin" / "newsletter" / f"{slug}-draft.html"
    if not draft_path.is_file():
        return Refused("missing_issue")
    draft = draft_path.read_text(encoding="utf-8")
    try:
        html = email_html(draft)
        subject = subject_line(root, slug, draft)
    except ValueError as exc:
        reason = str(exc)
        if reason == "personal_name":
            return Refused("personal_name")
        if reason == "missing_issue":
            return Refused("missing_issue")
        if reason == "missing_footer":
            return Refused("missing_footer")
        raise
    payload = {
        "name": f"Keep, Test, Cut {slug}",
        "segment_id": segment,
        "from": FROM_ADDRESS,
        "subject": subject,
        "html": html,
        "send": True,
    }
    sender = post_broadcast if post is None else post
    return sender(payload, key)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: send_keep_cut.py <slug>", file=sys.stderr)
        return 2
    result = send_issue(Path(__file__).resolve().parent.parent, sys.argv[1])
    if isinstance(result, Held):
        print(result.reason)
        return 2
    if isinstance(result, Refused):
        print(result.reason)
        return 2
    print(result.get("id", "sent"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
