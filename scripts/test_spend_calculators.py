#!/usr/bin/env python3
"""Voice, automation, preset, and price-alert checks. No invented rates."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NODE = r"""
const assert = require("assert");
const voice = require("./js/voice-video-calculator.js");
const auto = require("./js/automation-task-calculator.js");
const audit = require("./js/stack-audit.js");

function row(result, slug) {
  return result.rows.filter((item) => item.slug === slug)[0];
}

const free = voice.priceVoice({ minutes: 60, retake: 1, clone: false });
assert.strictEqual(row(free, "descript").tier, "Free");
assert.strictEqual(row(free, "descript").monthlyCents, 0);
assert.strictEqual(row(free, "descript").verdict, "Keep");
assert.strictEqual(row(free, "elevenlabs").monthlyCents, null);
assert.strictEqual(row(free, "heygen").rel, "external noopener");
assert.strictEqual(row(free, "synthesia").rel, "external noopener");
assert.strictEqual(free.rows.map((item) => item.name).join(","), "Descript,ElevenLabs,HeyGen,Synthesia,Runway,Midjourney");
assert.strictEqual(row(free, "runway").covers, false);
assert.strictEqual(row(free, "runway").monthlyCents, null);
assert.strictEqual(row(free, "midjourney").tier, "Basic");
assert.strictEqual(row(free, "midjourney").monthlyCents, 1000);
assert.strictEqual(free.savingsAnnualCents, 12000);

const clip = voice.priceVoice({ minutes: 60, seconds: 10, retake: 1, clone: false });
assert.strictEqual(row(clip, "runway").tier, "Standard");
assert.strictEqual(row(clip, "runway").monthlyCents, 1500);
assert.strictEqual(row(clip, "runway").credits, 120);
assert.strictEqual(row(clip, "runway").rel, "external noopener");

const standardEdge = voice.priceVoice({ minutes: 60, seconds: 52, retake: 1, clone: false });
assert.strictEqual(row(standardEdge, "runway").credits, 624);
assert.strictEqual(row(standardEdge, "runway").tier, "Standard");
assert.strictEqual(row(standardEdge, "runway").monthlyCents, 1500);

const proClip = voice.priceVoice({ minutes: 60, seconds: 53, retake: 1, clone: false });
assert.strictEqual(row(proClip, "runway").tier, "Pro");
assert.strictEqual(row(proClip, "runway").monthlyCents, 3500);

const broll = voice.priceVoice({ minutes: 100, seconds: 40, retake: 5, clone: false });
assert.strictEqual(broll.generatedSeconds, 200);
assert.strictEqual(broll.demandedMinutes, 500);
assert.strictEqual(row(broll, "runway").credits, 2400);
assert.strictEqual(row(broll, "runway").tier, "Max");
assert.strictEqual(row(broll, "runway").monthlyCents, 9500);
assert.strictEqual(row(broll, "midjourney").tier, "Standard");
assert.strictEqual(row(broll, "midjourney").monthlyCents, 3000);

const stealth = voice.priceVoice({ minutes: 60, seconds: 10, retake: 1, clone: true });
assert.strictEqual(row(stealth, "midjourney").tier, "Pro");
assert.strictEqual(row(stealth, "midjourney").monthlyCents, 6000);
assert.strictEqual(row(stealth, "midjourney").rel, "external noopener");
assert.ok(row(stealth, "runway").note.indexOf("Turbo") !== -1);
assert.ok(row(stealth, "runway").note.indexOf("does not price Turbo") !== -1);

const hobby = voice.priceVoice({ minutes: 60, retake: 2, clone: false });
assert.strictEqual(hobby.demandedMinutes, 120);
assert.strictEqual(row(hobby, "descript").tier, "Hobbyist");
assert.strictEqual(row(hobby, "descript").monthlyCents, 2400);

const business = voice.priceVoice({ minutes: 2000, retake: 1, clone: false });
assert.strictEqual(row(business, "descript").tier, "Business");
assert.strictEqual(row(business, "descript").monthlyCents, 6500);

const over = voice.priceVoice({ minutes: 3000, retake: 1, clone: false });
assert.strictEqual(row(over, "descript").covers, false);
assert.strictEqual(row(over, "descript").monthlyCents, null);

const clone = voice.priceVoice({ minutes: 30, retake: 1, clone: true });
assert.strictEqual(row(clone, "synthesia").tier, "Enterprise");
assert.strictEqual(row(clone, "elevenlabs").monthlyCents, null);

const light = auto.priceAutomation({ workflows: 1, steps: 1, runsPerDay: 1, webhookPercent: 100 });
assert.strictEqual(light.runs, 30);
assert.strictEqual(row(light, "zapier").monthlyCents, 0);
assert.strictEqual(row(light, "make").monthlyCents, 0);
assert.strictEqual(row(light, "n8n").currency, "EUR");
assert.strictEqual(row(light, "n8n").monthlyCents, 2000);
assert.strictEqual(light.savingsAnnualCents, 0);

const core = auto.priceAutomation({ workflows: 3, steps: 5, runsPerDay: 4, webhookPercent: 100 });
assert.strictEqual(core.runs, 360);
assert.strictEqual(row(core, "zapier").units, 1800);
assert.strictEqual(row(core, "zapier").covers, false);
assert.strictEqual(row(core, "make").tier, "Core");
assert.strictEqual(row(core, "make").monthlyCents, 1200);
assert.strictEqual(row(core, "n8n").units, 360);
assert.strictEqual(core.savingsAnnualCents, 0);
assert.ok(row(core, "n8n").note.indexOf("Euros") !== -1);

const polled = auto.priceAutomation({ workflows: 1, steps: 1, runsPerDay: 0, webhookPercent: 0 });
assert.strictEqual(polled.pollRuns, 720);
assert.ok(polled.assumption.indexOf("24") !== -1);

const hooks = auto.priceAutomation({ workflows: 2, steps: 1, runsPerDay: 0, webhookPercent: 100 });
assert.strictEqual(hooks.pollRuns, 0);
assert.strictEqual(hooks.runs, 0);

assert.strictEqual(audit.presetMonthly("vibe"), 110);
assert.strictEqual(audit.presetMonthly("creator"), 95);
assert.strictEqual(audit.presetMonthly("agency"), 149);
assert.strictEqual(audit.presetMonthly("chat"), 59.99);
const vibe = audit.toolsFromPreset("vibe");
assert.strictEqual(audit.evaluate(vibe).cost.monthly, 110);
const line = audit.receiptLine(110, vibe.length, 0);
assert.strictEqual(
  line,
  "Audited my AI stack on AIToolsEssentials: $110.00/mo across 6 tools -> $0.00/yr duplicate overlap. https://aitoolsessentials.com/stack-audit.html"
);

const pasted = audit.matchReceipt([
  "OPENAI *CHATGPT",
  "ANTHROPIC",
  "CURSOR",
  "VERCEL",
  "DESCRIPT",
  "ELEVENLABS",
  "ZAPIER",
  "MAKE.COM",
  "HEYGEN",
  "SYNTHESIA",
  "LOVABLE",
  "REPLIT",
  "GAMMA",
  "MIDJOURNEY",
  "NOTION",
  "PERPLEXITY",
  "WINDSURF",
  "GITHUB COPILOT",
  "MICROSOFT COPILOT"
].join("\n"));
const by = {};
pasted.forEach((tool) => { by[tool.slug] = tool; });
assert.strictEqual(by.chatgpt.amount, 20);
assert.strictEqual(by.claude.amount, 20);
assert.strictEqual(by.cursor.amount, 30);
assert.strictEqual(by.v0.amount, 30);
assert.strictEqual(by.descript.amount, 24);
assert.strictEqual(by.elevenlabs.amount, 22);
assert.strictEqual(by["zapier-ai"].amount, null);
assert.strictEqual(by["zapier-ai"].spend_kind, "unknown");
assert.strictEqual(by.make.amount, 12);
assert.strictEqual(by.heygen.amount, 29);
assert.strictEqual(by.synthesia.amount, 29);
assert.strictEqual(by.lovable.amount, 25);
assert.strictEqual(by["replit-ai"].amount, 20);
assert.strictEqual(by.gamma.amount, 9);
assert.strictEqual(by.midjourney.amount, 10);
assert.strictEqual(by["notion-ai"].amount, 20);
assert.strictEqual(by.perplexity.amount, null);
assert.strictEqual(by["c:windsurf"].amount, 20);
assert.strictEqual(by["github-copilot"].amount, 10);
assert.strictEqual(by["microsoft-copilot"].amount, null);
assert.ok(!pasted.some((tool) => tool.slug === "zapier"));
"""


def main() -> None:
    newsletter = json.loads((ROOT / "data" / "newsletter.json").read_text(encoding="utf-8"))
    if newsletter.get("send_enabled") is not False:
        raise SystemExit("newsletter send_enabled must stay false")
    proc = subprocess.run(["node", "-e", NODE], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        raise SystemExit(proc.stderr or proc.stdout or "calculator checks failed")
    voice = (ROOT / "compare" / "ai-video-avatar-cost" / "index.html").read_text(encoding="utf-8")
    auto = (ROOT / "compare" / "automation-task-calculator" / "index.html").read_text(encoding="utf-8")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    best = (ROOT / "comparisons" / "best-ai-tools.html").read_text(encoding="utf-8")
    prices = (ROOT / "price-changes" / "index.html").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    audit = (ROOT / "stack-audit.html").read_text(encoding="utf-8")
    tool = (ROOT / "tools" / "chatgpt" / "index.html").read_text(encoding="utf-8")
    comparison = (ROOT / "comparisons" / "chatgpt-vs-claude.html").read_text(encoding="utf-8")
    for needle in (
        'id="voice-minutes"',
        'id="voice-retake"',
        'id="voice-seconds"',
        'id="voice-clone"',
        "Runway",
        "Midjourney",
        'href="/go/runway/" rel="external noopener"',
        'href="/go/midjourney/" rel="external noopener"',
        'href="/go/elevenlabs/" rel="sponsored nofollow noopener"',
        'href="/go/descript/" rel="sponsored nofollow noopener"',
        'href="/go/heygen/" rel="external noopener"',
        'href="/go/synthesia/" rel="external noopener"',
    ):
        if needle not in voice:
            raise SystemExit(f"voice hub missing {needle}")
    for needle in (
        'id="auto-workflows"',
        'id="auto-steps"',
        'id="auto-runs"',
        'id="auto-webhook"',
        'href="/go/make/" rel="sponsored nofollow noopener"',
        'href="/go/n8n/" rel="external noopener"',
        'href="/go/zapier/" rel="external noopener"',
    ):
        if needle not in auto:
            raise SystemExit(f"automation hub missing {needle}")
    for page, label in ((home, "home"), (best, "best"), (prices, "prices"), (sitemap, "sitemap")):
        for href in ("/compare/ai-video-avatar-cost/", "/compare/automation-task-calculator/"):
            if href not in page:
                raise SystemExit(f"{label} missing {href}")
    if 'class="scene scene-dark ledger-mast"' not in audit:
        raise SystemExit("stack audit mast is not the newsprint ledger")
    if "button-ghost-dark" in audit:
        raise SystemExit("stack audit still uses button-ghost-dark")
    for needle in ("data-preset=\"vibe\"", "Indie Vibe-Coder ($110/mo)", "id=\"sa-paste\"", "id=\"sa-copy-receipt\""):
        if needle not in audit:
            raise SystemExit(f"stack audit missing {needle}")
    endpoint = newsletter["subscribe_endpoint"]
    for page, tool_id in ((tool, "chatgpt"), (comparison, "chatgpt-vs-claude")):
        if "AIT PRICE ALERT START" not in page or "price-alert-form" not in page:
            raise SystemExit("price alert missing")
        if tool_id == "chatgpt" and "Track ChatGPT price &amp; credit-rule changes" not in page:
            raise SystemExit("price alert used the review headline instead of the tool name")
        if f'name="tool" value="{tool_id}"' not in page:
            raise SystemExit(f"price alert tool context missing for {tool_id}")
        if f'action="{endpoint}"' not in page or 'name="company_website"' not in page:
            raise SystemExit("price alert is not wired to the subscribe worker")
        if 'id="keep-cut-subscribe"' in page:
            raise SystemExit("price alert reused the homepage subscribe id")
    print("spend calculator checks passed")


if __name__ == "__main__":
    main()
