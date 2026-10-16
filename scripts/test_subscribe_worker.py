#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def main() -> None:
    errors: list[str] = []
    worker = (REPO / "workers" / "newsletter-subscribe" / "worker.js").read_text(encoding="utf-8")
    toml = (REPO / "workers" / "newsletter-subscribe" / "wrangler.toml").read_text(encoding="utf-8")
    if "re_" in worker or "re_" in toml or "RESEND_API_KEY =" in toml:
        errors.append("worker files contain a secret")
    if "unsubscribed: true" not in worker or "company_website" not in worker:
        errors.append("worker is missing double opt-in or the honeypot")
    code = """
import { classify, sign, sameHex } from "./workers/newsletter-subscribe/worker.js";
if (classify({ email: "reader@example.com", company_website: "" }) !== "accept") process.exit(2);
if (classify({ email: "reader@example.com", company_website: "http://spam.example" }) !== "honeypot") process.exit(3);
if (classify({ email: "nope", company_website: "" }) !== "bad_email") process.exit(4);
const token = await sign("test-secret", "reader@example.com", "100");
const other = await sign("test-secret", "reader@example.com", "101");
if (token.length !== 64) process.exit(5);
if (!sameHex(token, token)) process.exit(6);
if (sameHex(token, other)) process.exit(7);
process.stdout.write("ok");
"""
    run = subprocess.run(
        ["node", "--input-type=module", "-e", code],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if run.returncode != 0 or run.stdout != "ok":
        errors.append(f"worker token check failed {run.returncode} {run.stdout} {run.stderr}")
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
