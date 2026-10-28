#!/usr/bin/env python3
"""Resolution-fee calculator: published rates only, partner hop on CustomGPT.ai."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NODE = r"""
const assert = require("assert");
const fs = require("fs");
const calc = require("./js/customer-support-calculator.js");
const pricing = JSON.parse(fs.readFileSync("./data/customer_support_pricing.json", "utf8"));

const solo = calc.priceSupport({ tickets: 800, rate: 45, seats: 2, reopen: false, finMode: "desk", zdPlan: "team", zdBilling: "annual", zdResolution: "payg", copilot: false }, pricing);
assert.strictEqual(solo.resolved, 360);
const by = Object.fromEntries(solo.rows.map((row) => [row.id, row]));
assert.strictEqual(by.customgpt.monthlyCents, 9900);
assert.strictEqual(by.customgpt.resolutionCents, 0);
assert.strictEqual(by.customgpt.partner, true);
assert.strictEqual(by.customgpt.href, "/go/customgpt/");
assert.strictEqual(by.intercom.monthlyCents, 2 * 2900 + 360 * 99);
assert.strictEqual(by.zendesk.monthlyCents, 2 * 5500 + (360 - 10) * 200);
assert.strictEqual(by.tidio.monthlyCents, 70000);
assert.strictEqual(by.enterprise.monthlyCents, null);
assert.ok(by.customgpt.rank < by.intercom.rank);

const floor = calc.priceSupport({ tickets: 100, rate: 20, seats: 1, finMode: "standalone", zdPlan: "team", zdBilling: "annual", zdResolution: "payg" }, pricing);
const fin = floor.rows.filter((row) => row.id === "intercom")[0];
assert.strictEqual(fin.monthlyCents, 50 * 99);

const quiet = calc.priceSupport({ tickets: 100, rate: 50, seats: 1, reopen: false, finMode: "desk", zdPlan: "team", zdBilling: "annual", zdResolution: "payg" }, pricing);
const reopen = calc.priceSupport({ tickets: 100, rate: 50, seats: 1, reopen: true, finMode: "desk", zdPlan: "team", zdBilling: "annual", zdResolution: "payg" }, pricing);
const before = Object.fromEntries(quiet.rows.map((row) => [row.id, row]));
const again = Object.fromEntries(reopen.rows.map((row) => [row.id, row]));
assert.strictEqual(again.intercom.monthlyCents, before.intercom.monthlyCents);
assert.strictEqual(again.zendesk.monthlyCents, before.zendesk.monthlyCents);
assert.strictEqual(before.tidio.monthlyCents, 7500);
assert.strictEqual(again.tidio.monthlyCents, 14000);

const scale = calc.priceSupport({ tickets: 12000, rate: 60, seats: 18, finMode: "desk", zdPlan: "team", zdBilling: "annual", zdResolution: "payg" }, pricing);
const gpt = scale.rows.filter((row) => row.id === "customgpt")[0];
assert.strictEqual(gpt.monthlyCents, 49900 + 3 * 37500);
assert.strictEqual(scale.rows.filter((row) => row.id === "tidio")[0].monthlyCents, null);
"""


def main() -> None:
    proc = subprocess.run(["node", "-e", NODE], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode:
        raise SystemExit(proc.stderr or proc.stdout or "support calc failed")
    hub = (ROOT / "compare" / "ai-customer-support-cost" / "index.html").read_text(encoding="utf-8")
    embed = (ROOT / "embed" / "customer-support-cost.html").read_text(encoding="utf-8")
    embeds = (ROOT / "embeds" / "index.html").read_text(encoding="utf-8")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    audit = (ROOT / "stack-audit.html").read_text(encoding="utf-8")
    traps = (ROOT / "pricing-watch" / "credit-traps" / "index.html").read_text(encoding="utf-8")
    custom = (ROOT / "tools" / "customgpt" / "index.html").read_text(encoding="utf-8")
    for needle, page, label in (
        ("consume quota on attempted inbound tickets", hub, "hub"),
        ("consume quota on attempted inbound tickets", embed, "embed"),
        ('id="support-calc"', hub, "hub"),
        ("Copy shareable receipt link", hub, "hub"),
        ("Embed this calculator", hub, "hub"),
        ('data-partner-slug="customgpt"', hub, "hub"),
        ("sponsored nofollow noopener", hub, "hub"),
        ("#FAF8F5", embed, "embed"),
        ('id="support-calc"', embed, "embed"),
        ('src="/embed/customer-support-cost.html"', embeds, "showcase"),
        ('height="480"', embeds, "showcase"),
        ('href="/compare/ai-customer-support-cost/"', home, "home"),
        ('href="/compare/ai-customer-support-cost/"', audit, "audit"),
        ('href="/compare/ai-customer-support-cost/"', traps, "traps"),
        ('href="/compare/ai-customer-support-cost/"', custom, "customgpt"),
        ("ledger-page", home, "home-should-not"),
    ):
        if label == "home-should-not":
            if needle in page:
                raise SystemExit("homepage picked up ledger-page")
            continue
        if needle not in page:
            raise SystemExit(f"{label} missing {needle}")
    if "send_enabled" in (ROOT / "data" / "newsletter.json").read_text(encoding="utf-8"):
        cfg = json.loads((ROOT / "data" / "newsletter.json").read_text(encoding="utf-8"))
        if cfg.get("send_enabled") is not False:
            raise SystemExit("send_enabled flipped")
    print("support calculator ok")


if __name__ == "__main__":
    main()
