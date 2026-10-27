#!/usr/bin/env python3
"""priceVoice() covers the six checked voice, video, and image seats."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NODE = r"""
const assert = require("assert");
const voice = require("./js/voice-video-calculator.js");

function row(result, slug) {
  return result.rows.filter((item) => item.slug === slug)[0];
}

const names = ["ElevenLabs", "Descript", "HeyGen", "Synthesia", "Runway", "Midjourney"];
const base = voice.priceVoice({ minutes: 60, seconds: 10, retake: 1, clone: false });
assert.deepStrictEqual(base.rows.map((item) => item.name).sort(), names.slice().sort());
assert.strictEqual(base.rows.length, 6);
assert.strictEqual(row(base, "descript").tier, "Free");
assert.strictEqual(row(base, "descript").monthlyCents, 0);
assert.strictEqual(row(base, "elevenlabs").monthlyCents, null);
assert.strictEqual(row(base, "heygen").monthlyCents, null);
assert.strictEqual(row(base, "synthesia").monthlyCents, null);
assert.strictEqual(row(base, "runway").tier, "Standard");
assert.strictEqual(row(base, "runway").monthlyCents, 1500);
assert.strictEqual(row(base, "runway").credits, 120);
assert.strictEqual(row(base, "runway").rel, "external noopener");
assert.strictEqual(row(base, "midjourney").tier, "Basic");
assert.strictEqual(row(base, "midjourney").monthlyCents, 1000);
assert.strictEqual(row(base, "midjourney").rel, "external noopener");
assert.strictEqual(row(base, "descript").verdict, "Keep");
assert.strictEqual(row(base, "elevenlabs").verdict, "Test");
assert.strictEqual(row(base, "heygen").verdict, "Test");
assert.strictEqual(row(base, "synthesia").verdict, "Test");
assert.strictEqual(row(base, "runway").verdict, "Keep");
assert.strictEqual(row(base, "midjourney").verdict, "Keep");
assert.strictEqual(base.keepSlug, "descript");
assert.strictEqual(base.savingsAnnualCents, 0);

const idle = voice.priceVoice({ minutes: 60, seconds: 0, retake: 1, clone: false });
assert.strictEqual(row(idle, "runway").tier, "No clip");
assert.strictEqual(row(idle, "runway").monthlyCents, 0);
assert.strictEqual(row(idle, "runway").verdict, "Cut");
assert.strictEqual(row(idle, "descript").verdict, "Keep");
assert.notStrictEqual(row(idle, "descript").verdict, "Switch");
assert.strictEqual(row(idle, "midjourney").verdict, "Keep");
assert.strictEqual(idle.savingsAnnualCents, 0);

const noFast = voice.priceVoice({ minutes: 0, seconds: 10, retake: 1, clone: false });
assert.strictEqual(row(noFast, "midjourney").tier, "No Fast time");
assert.strictEqual(row(noFast, "midjourney").verdict, "Cut");
assert.strictEqual(row(noFast, "runway").verdict, "Keep");
assert.strictEqual(row(noFast, "descript").verdict, "Keep");

const edge = voice.priceVoice({ minutes: 60, seconds: 52, retake: 1, clone: false });
assert.strictEqual(row(edge, "runway").credits, 624);
assert.strictEqual(row(edge, "runway").tier, "Standard");
assert.strictEqual(row(edge, "runway").monthlyCents, 1500);

const pro = voice.priceVoice({ minutes: 60, seconds: 53, retake: 1, clone: false });
assert.strictEqual(row(pro, "runway").tier, "Pro");
assert.strictEqual(row(pro, "runway").monthlyCents, 3500);

const retakes = voice.priceVoice({ minutes: 100, seconds: 40, retake: 5, clone: false });
assert.strictEqual(retakes.generatedSeconds, 200);
assert.strictEqual(retakes.demandedMinutes, 500);
assert.strictEqual(row(retakes, "runway").credits, 2400);
assert.strictEqual(row(retakes, "runway").tier, "Max");
assert.strictEqual(row(retakes, "runway").monthlyCents, 9500);
assert.strictEqual(row(retakes, "midjourney").tier, "Standard");
assert.strictEqual(row(retakes, "midjourney").monthlyCents, 3000);
assert.ok(row(retakes, "runway").note.indexOf("does not price Turbo") !== -1);
assert.ok(row(retakes, "runway").note.indexOf("9,500") !== -1);

const stealth = voice.priceVoice({ minutes: 60, seconds: 10, retake: 1, clone: true });
assert.strictEqual(row(stealth, "midjourney").tier, "Pro");
assert.strictEqual(row(stealth, "midjourney").monthlyCents, 6000);
assert.strictEqual(row(stealth, "synthesia").tier, "Enterprise");
assert.ok(row(stealth, "midjourney").note.indexOf("Stealth") !== -1);

const longFast = voice.priceVoice({ minutes: 2000, seconds: 10, retake: 1, clone: true });
assert.strictEqual(row(longFast, "midjourney").tier, "Mega");
assert.strictEqual(row(longFast, "midjourney").monthlyCents, 12000);

const over = voice.priceVoice({ minutes: 4000, seconds: 900, retake: 1, clone: false });
assert.strictEqual(row(over, "runway").covers, false);
assert.strictEqual(row(over, "runway").monthlyCents, null);
assert.strictEqual(row(over, "runway").verdict, "Cut");
assert.strictEqual(row(over, "midjourney").covers, false);
assert.strictEqual(row(over, "midjourney").monthlyCents, null);
assert.strictEqual(row(over, "midjourney").verdict, "Cut");
assert.strictEqual(row(retakes, "runway").verdict, "Keep");
assert.strictEqual(row(retakes, "midjourney").verdict, "Keep");

console.log("priceVoice ok");
"""


def test_price_voice_rows() -> None:
    proc = subprocess.run(["node", "-e", NODE], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        raise AssertionError(proc.stderr or proc.stdout or "priceVoice failed")


if __name__ == "__main__":
    test_price_voice_rows()
    print("priceVoice ok")
