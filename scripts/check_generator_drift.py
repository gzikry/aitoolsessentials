#!/usr/bin/env python3
"""Fail when a generator pass leaves customer pages different from HEAD.

Calendar dates and asset query hashes are normalized so a later day does not
look like a content drift. Admin packs are not customer pages.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_MONTH = re.compile(
    r"(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+\d{1,2},\s+\d{4}"
)
_HASH = re.compile(r"\?v=[0-9a-fA-F]+")
_SKIP = ("admin/", "content_briefs/")


def normalize(text: str) -> str:
    text = _HASH.sub("?v=HASH", text)
    text = _DATE.sub("DATE", text)
    return _MONTH.sub("MONTH DATE", text)


def changed_names() -> list[str]:
    out = subprocess.check_output(
        ["git", "diff", "--name-only", "-z", "HEAD"],
        cwd=ROOT,
    )
    return [name for name in out.decode().split("\0") if name]


def main() -> int:
    errors: list[str] = []
    for name in changed_names():
        if name.startswith(_SKIP):
            continue
        path = ROOT / name
        old = subprocess.run(
            ["git", "show", f"HEAD:{name}"],
            cwd=ROOT,
            capture_output=True,
        )
        if old.returncode != 0:
            errors.append(name + " is new generator output")
            continue
        if not path.is_file():
            errors.append(name + " was removed by the generator")
            continue
        new_b = path.read_bytes()
        old_b = old.stdout
        if b"\0" in old_b[:8000] or b"\0" in new_b[:8000]:
            if old_b != new_b:
                errors.append(name + " binary output drifted")
            continue
        old_t = normalize(old_b.decode("utf-8", "replace"))
        new_t = normalize(new_b.decode("utf-8", "replace"))
        if old_t != new_t:
            errors.append(name + " drifted from the generator")
    if errors:
        print("generator drift:")
        for err in errors:
            print("-", err)
        return 1
    print("generator drift ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
