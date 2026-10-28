#!/usr/bin/env python3
"""Wave 9: credit-trap utilization ledger, sixth embed, preset stacks, billing paste."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NODE = r"""
const assert = require("assert");
const audit = require("./js/stack-audit.js");
assert.strictEqual(audit.presetMonthly("vibe"), 110);
assert.strictEqual(audit.presetMonthly("creator"), 95);
assert.strictEqual(audit.presetMonthly("vibe-coder"), 135);
assert.strictEqual(audit.presetMonthly("creator-voice"), 120);
assert.strictEqual(audit.presetMonthly("founder"), 151);
const pasted = audit.matchReceipt([
  "OPENAI *CHATGPT",
  "GITHUB",
  "RUNWAY",
  "CUSTOMGPT",
  "CANVA",
  "GRAMMARLY",
  "OTTER.AI",
  "MAKE.COM"
].join("\n"));
const by = {};
pasted.forEach((tool) => { by[tool.slug] = tool; });
assert.strictEqual(by.chatgpt.amount, 20);
assert.strictEqual(by["github-copilot"].amount, 10);
assert.strictEqual(by.runway.amount, 15);
assert.strictEqual(by.customgpt.amount, 99);
assert.strictEqual(by["canva-ai"].amount, null);
assert.strictEqual(by.grammarly.amount, null);
assert.strictEqual(by["otter-ai"].amount, null);
assert.strictEqual(by.make.amount, 12);
"""


def need(text: str, needle: str, errors: list[str], label: str) -> None:
    if needle not in text:
        errors.append(f"{label} missing {needle}")


def main() -> None:
    errors: list[str] = []
    proc = subprocess.run(["node", "-e", NODE], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode:
        errors.append(proc.stdout + proc.stderr)

    traps = (ROOT / "pricing-watch" / "credit-traps" / "index.html").read_text(encoding="utf-8")
    embed = (ROOT / "embed" / "credit-traps.html").read_text(encoding="utf-8")
    embeds = (ROOT / "embeds" / "index.html").read_text(encoding="utf-8")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    watch = (ROOT / "pricing-watch" / "index.html").read_text(encoding="utf-8")
    prices = (ROOT / "price-changes" / "index.html").read_text(encoding="utf-8")
    audit = (ROOT / "stack-audit.html").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for needle in (
        'id="trap-util"',
        'min="25"',
        'max="100"',
        'data-pill="all"',
        'data-pill="reset"',
        'data-pill="expiry90"',
        'data-pill="lock"',
        'data-pill="meter"',
        'data-pill="longroll"',
        'data-pill="annual"',
        "Monthly Reset / No Rollover",
        "60–65 Day Expiry",
        "Downgrade / Cancel Credit Wipe",
        "Attempted vs. Resolved Meter",
        "2-Year / Long Rollover",
        "Check if my tools have credit traps",
        "Monthly credits expire after 65 days.",
        "Standard is $99 per month with 1,000 queries.",
        "Fin outcomes are $0.99.",
        "Extra resolutions are $1.50 committed or $2.00 pay-as-you-go.",
        "do not state a 2-year pack validity window",
        'href="/go/customgpt/" rel="sponsored nofollow noopener"',
        'href="/go/elevenlabs/" rel="sponsored nofollow noopener"',
        'href="/tools/suno/"',
        'href="/tools/umevo/"',
    ):
        need(traps, needle, errors, "traps")
    if "HeyGen credits do not roll" in traps or "Zapier tasks reset" in traps:
        errors.append("traps page invented a rollover rule")
    for needle in (
        'src="/embed/credit-traps.html"',
        "6 calculators",
        'height="480"',
    ):
        need(embeds, needle, errors, "embeds")
    need(embed, 'id="trap-util"', errors, "embed")
    need(embed, "#FAF8F5", errors, "embed")
    need(embed, 'href="/pricing-watch/credit-traps/"', errors, "embed")
    need(home, 'href="/pricing-watch/credit-traps/"', errors, "home")
    need(home, "home-learn-card-wide", errors, "home")
    need(watch, 'id="credit-trap-card"', errors, "watch")
    need(prices, 'id="credit-trap-card"', errors, "prices")
    for needle in (
        'data-testid="preset-stacks"',
        'data-testid="billing-paste-box"',
        'data-preset="vibe-coder"',
        'data-preset="creator-voice"',
        'data-preset="founder"',
        'data-preset="vibe"',
        "Indie Vibe-Coder ($110/mo)",
        'id="sa-paste"',
        "Vibe-Coder Stack",
        "Creator Video &amp; Voice Stack",
        "Founder &amp; Support Stack",
    ):
        need(audit, needle, errors, "audit")
    js = (ROOT / "js" / "stack-audit.js").read_text(encoding="utf-8")
    need(js, "sa-rec-links", errors, "audit-js")
    need(js, "scrollIntoView", errors, "audit-js")
    need(sitemap, "https://aitoolsessentials.com/pricing-watch/credit-traps/", errors, "sitemap")
    need(sitemap, "https://aitoolsessentials.com/embed/credit-traps.html", errors, "sitemap")
    if errors:
        raise SystemExit("\n".join(errors))
    print("wave 9 ok")


if __name__ == "__main__":
    main()
