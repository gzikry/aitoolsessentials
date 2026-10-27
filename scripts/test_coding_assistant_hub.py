#!/usr/bin/env python3
"""The coding-assistant calculator prices published subscriptions, not invented token burn."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

BILL = r"""
const fs = require("fs");
const vm = require("vm");
const context = { console, globalThis: {} };
context.globalThis = context;
vm.createContext(context);
vm.runInContext(fs.readFileSync("js/homepage-bill-slasher.js", "utf8"), context);
const quote = context.BillSlasher.quote;
const errors = [];
const chat = quote(["chatgpt", "claude"]);
if (chat.monthly !== 40 || chat.waste !== 240 || chat.keep.length !== 1) errors.push("chat " + JSON.stringify(chat));
const code = quote(["cursor", "copilot", "windsurf"]);
if (code.keep[0].id !== "copilot" || code.waste !== 420) errors.push("code " + JSON.stringify(code));
const stacked = quote(["claude", "claude-max"]);
if (stacked.monthly !== 100 || stacked.waste !== 240) errors.push("max " + JSON.stringify(stacked));
const v0 = quote(["v0"]);
if (!v0.traps.some((line) => line.indexOf("65 days") !== -1)) errors.push("v0 trap");
const empty = quote([]);
if (empty.monthly !== 0 || empty.waste !== 0) errors.push("empty");
if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}
"""

NODE = r"""
const fs = require("fs");
const vm = require("vm");
const context = { console, globalThis: {} };
context.globalThis = context;
vm.createContext(context);
vm.runInContext(fs.readFileSync("js/coding-assistant-calculator.js", "utf8"), context);
const quote = context.CodingAssistantCalc.quote;
const money = context.CodingAssistantCalc.money;
const errors = [];
function tool(result, id) {
  return result.tools.find((row) => row.id === id);
}
function expect(result, id, fields) {
  const row = tool(result, id);
  Object.keys(fields).forEach((key) => {
    if (row[key] !== fields[key]) {
      errors.push(id + " " + key + " " + row[key] + " !== " + fields[key]);
    }
  });
}
const team = quote({ seats: 5, prompts: 20, frontier: false, annual: false });
if (team.band !== "light") errors.push("team band " + team.band);
expect(team, "copilot", { tier: "Pro", verdict: "Keep", monthlyCents: 5000, annualCents: 60000, overageCents: 0 });
expect(team, "claude", { tier: "Pro", verdict: "Test", monthlyCents: 10000, annualCents: 120000, overageCents: 0 });
expect(team, "cursor", { tier: "Premium", verdict: "Cut", monthlyCents: 15000, annualCents: 180000, overageCents: 0 });
expect(team, "windsurf", { tier: "Teams", verdict: "Cut", monthlyCents: 20000, annualCents: 240000, overageCents: 0 });

const heavy = quote({ seats: 1, prompts: 80, frontier: true, annual: false });
if (heavy.band !== "heavy") errors.push("heavy band");
expect(heavy, "copilot", { tier: "Max", verdict: "Keep", monthlyCents: 10000, includesFrontier: true });
expect(heavy, "claude", { tier: "Max 20x", verdict: "Test", monthlyCents: 20000 });
expect(heavy, "windsurf", { tier: "Max", verdict: "Test", monthlyCents: 20000 });
expect(heavy, "cursor", { tier: "Ultra", verdict: "Test", monthlyCents: 20000, includesFrontier: false });

const annual = quote({ seats: 1, prompts: 10, frontier: false, annual: true });
expect(annual, "copilot", { tier: "Pro", verdict: "Keep", monthlyCents: 1000, annualCents: 12000 });
expect(annual, "claude", { tier: "Pro", verdict: "Test", monthlyCents: 1667, annualCents: 20000, annualDiscount: true });
expect(annual, "windsurf", { tier: "Pro", verdict: "Test", monthlyCents: 2000, annualCents: 24000 });
expect(annual, "cursor", { tier: "Premium", verdict: "Cut", monthlyCents: 3000, annualCents: 36000 });
if (money(1667) !== "$16.67") errors.push("money " + money(1667));

const steady = quote({ seats: 8, prompts: 40, frontier: false, annual: false });
expect(steady, "copilot", { tier: "Pro+", verdict: "Keep", monthlyCents: 31200 });
expect(steady, "windsurf", { tier: "Teams", verdict: "Test", monthlyCents: 32000 });
expect(steady, "cursor", { tier: "Super", verdict: "Cut", monthlyCents: 80000 });
expect(steady, "claude", { tier: "Max 5x", verdict: "Cut", monthlyCents: 80000 });
if (tool(steady, "copilot").note.indexOf("1,900") === -1) errors.push("missing Business credit note");

const frontierLight = quote({ seats: 1, prompts: 10, frontier: true, annual: false });
expect(frontierLight, "windsurf", { tier: "Pro", verdict: "Keep", monthlyCents: 2000 });
expect(frontierLight, "copilot", { tier: "Pro+", verdict: "Test", monthlyCents: 3900 });
expect(frontierLight, "claude", { tier: "Max 5x", verdict: "Cut", monthlyCents: 10000 });
expect(frontierLight, "cursor", { tier: "Super", verdict: "Cut", includesFrontier: false });

const pair = quote({ seats: 2, prompts: 5, frontier: false, annual: false });
expect(pair, "windsurf", { tier: "Teams", monthlyCents: 8000 });

const clamped = quote({ seats: 0, prompts: 500, frontier: false, annual: false });
if (clamped.seats !== 1 || clamped.prompts !== 100) errors.push("clamp " + clamped.seats + " " + clamped.prompts);

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}
"""


def _chrome_bin() -> str | None:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    return None


def _browser_errors() -> list[str]:
    chrome = _chrome_bin()
    if not chrome:
        return ["Chrome is not installed; calculator interactivity was not exercised in a browser"]
    from test_home_header_fit import _Ws, _page_socket, _serve, _start_chrome, _stop_chrome

    errors: list[str] = []
    httpd, port = _serve()
    profile = tempfile.mkdtemp(prefix="coding-calc-")
    proc = None
    ws = None
    try:
        proc, debug_port = _start_chrome(profile)
        ws = _Ws(_page_socket(debug_port))
        ws.call("Page.enable")
        ws.call("Page.navigate", {"url": f"http://127.0.0.1:{port}/compare/ai-coding-assistants/"})
        expression = r"""
        new Promise((resolve) => {
          const ready = () => {
            const keep = document.querySelector('[data-verdict="Keep"]');
            resolve({
              keep: keep ? keep.getAttribute("data-tool") : "",
              monthly: keep ? keep.getAttribute("data-monthly") : "",
              seats: document.getElementById("coding-seats").value
            });
          };
          if (document.querySelector('[data-verdict="Keep"]')) ready();
          else document.addEventListener("DOMContentLoaded", () => setTimeout(ready, 50));
        })
        """
        first = ws.call(
            "Runtime.evaluate",
            {"expression": expression, "awaitPromise": True, "returnByValue": True},
            timeout=20,
        )
        value = (first.get("result") or {}).get("value") or {}
        if value.get("keep") != "copilot" or value.get("monthly") != "5000" or value.get("seats") != "5":
            errors.append(f"default browser result {value}")
        changed = ws.call(
            "Runtime.evaluate",
            {
                "expression": """
                (() => {
                  document.getElementById("coding-seats").value = "1";
                  document.getElementById("coding-seats").dispatchEvent(new Event("input", { bubbles: true }));
                  document.getElementById("coding-prompts").value = "80";
                  document.getElementById("coding-prompts").dispatchEvent(new Event("input", { bubbles: true }));
                  document.querySelector('input[name="coding-tier"][value="frontier"]').checked = true;
                  document.getElementById("coding-calc").dispatchEvent(new Event("change", { bubbles: true }));
                  const keep = document.querySelector('[data-verdict="Keep"]');
                  const copilot = document.querySelector('[data-tool="copilot"]');
                  return {
                    keep: keep ? keep.getAttribute("data-tool") : "",
                    tier: copilot ? copilot.innerText : ""
                  };
                })()
                """,
                "returnByValue": True,
            },
            timeout=15,
        )
        after = (changed.get("result") or {}).get("value") or {}
        if after.get("keep") != "copilot" or "Max" not in str(after.get("tier")):
            errors.append(f"frontier browser result {after}")
    finally:
        if ws is not None:
            ws.close()
        if proc is not None:
            _stop_chrome(proc)
        httpd.shutdown()
        shutil.rmtree(profile, ignore_errors=True)
    return errors


def main() -> None:
    errors: list[str] = []
    proc = subprocess.run(["node", "-e", NODE], cwd=REPO, capture_output=True, text=True)
    if proc.returncode:
        errors.append(proc.stderr.strip() or proc.stdout.strip() or "calculator cases failed")
    page_path = REPO / "compare" / "ai-coding-assistants" / "index.html"
    if not page_path.is_file():
        errors.append("missing compare/ai-coding-assistants/index.html")
    else:
        page = page_path.read_text(encoding="utf-8")
        for needle in (
            "FAQPage",
            "SoftwareApplication",
            "Dataset",
            "Premium $30",
            "Max 5x",
            "Max 20x",
            "1,500",
            "$0.01",
            "Teams $40",
            "2,000 completions",
            'href="/tools/cursor/"',
            'href="/tools/claude/"',
            'href="/tools/github-copilot/"',
            'href="/articles/claude-code-vs-cursor-vs-copilot.html"',
            "https://aitoolsessentials.com/compare/ai-coding-assistants/",
            'id="coding-seats"',
            'id="coding-prompts"',
            'name="coding-tier"',
            'name="coding-cadence"',
            "Is Cursor Pro $20 enough or do I need Ultra $200?",
            "How much does Claude Code cost per month on Max vs API?",
            "What counts as a Premium Request in GitHub Copilot Pro vs Pro+?",
            "Windsurf Pro $15 vs Cursor Pro $20: how do prompt credits compare?",
            "Which AI coding stack is cheapest for a 5-person engineering team?",
        ):
            if needle not in page:
                errors.append(f"hub missing {needle}")
        for block in page.split('<script type="application/ld+json">')[1:]:
            raw = block.split("</script>", 1)[0]
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"hub JSON-LD {exc}")
    sitemap = (REPO / "sitemap.xml").read_text(encoding="utf-8")
    if "https://aitoolsessentials.com/compare/ai-coding-assistants/" not in sitemap:
        errors.append("sitemap missing the coding-assistant hub")
    home = (REPO / "index.html").read_text(encoding="utf-8")
    if 'href="/compare/ai-coding-assistants/"' not in home:
        errors.append("homepage missing the calculator card")
    comparisons = (REPO / "comparisons" / "index.html").read_text(encoding="utf-8")
    if 'href="/compare/ai-coding-assistants/"' not in comparisons:
        errors.append("comparison hub missing the calculator")
    for slug in ("cursor", "github-copilot", "claude"):
        review = (REPO / "tools" / slug / "index.html").read_text(encoding="utf-8")
        if 'href="/compare/ai-coding-assistants/"' not in review:
            errors.append(f"tools/{slug} does not link the calculator")
    article = (REPO / "articles" / "claude-code-vs-cursor-vs-copilot.html").read_text(encoding="utf-8")
    if 'href="/compare/ai-coding-assistants/"' not in article:
        errors.append("claude-code comparison does not link the calculator")
    if "Independent math" not in page or "buy.stripe.com/cNi00ideNbpb8O32az0x204" not in page:
        errors.append("coding hub missing the audit receipt footer")
    if 'href="/sponsor/"' not in page or 'href="/go/cursor/"' not in page:
        errors.append("coding hub missing sponsor or switch hop")
    home_bill = (REPO / "index.html").read_text(encoding="utf-8")
    if 'id="bill-slasher"' not in home_bill or "Email me the cut sheet" not in home_bill:
        errors.append("homepage missing the bill slasher")
    if not (REPO / "price-changes" / "index.html").is_file():
        errors.append("missing price-changes page")
    elif "65 days" not in (REPO / "price-changes" / "index.html").read_text(encoding="utf-8"):
        errors.append("price-changes missing the v0 credit clock")
    if "https://aitoolsessentials.com/price-changes/" not in sitemap:
        errors.append("sitemap missing price changes")
    go_cursor = REPO / "go" / "cursor" / "index.html"
    go_eleven = REPO / "go" / "elevenlabs" / "index.html"
    if not go_cursor.is_file() or "utm_source=aitoolsessentials" not in go_cursor.read_text(encoding="utf-8"):
        errors.append("cursor hop missing the campaign tag")
    if not go_eleven.is_file() or "try.elevenlabs.io" not in go_eleven.read_text(encoding="utf-8"):
        errors.append("elevenlabs hop missing the partner URL")
    presentation = (REPO / "articles" / "best-ai-presentation-tools.html").read_text(encoding="utf-8")
    if 'href="/go/gamma/"' not in presentation or "sponsored nofollow" not in presentation:
        errors.append("Gamma presentation CTAs were not hopped")
    switch = (REPO / "guides" / "switch-guides" / "switch-from-elevenlabs-to-descript.html").read_text(encoding="utf-8")
    if 'href="/go/elevenlabs/"' not in switch or 'href="/go/descript/"' not in switch:
        errors.append("switch guide missing partner hops")
    submit = (REPO / "submit-tool.html").read_text(encoding="utf-8")
    if "Free community queue" not in submit or "8-page comparison suite" not in submit:
        errors.append("submit page missing the two lanes")
    if not (REPO / "badges" / "audited.svg").is_file():
        errors.append("missing audited badge")
    cfg = json.loads((REPO / "data" / "newsletter.json").read_text(encoding="utf-8"))
    if cfg.get("send_enabled") is not False:
        errors.append("newsletter send_enabled must stay false")
    bill = subprocess.run(["node", "-e", BILL], cwd=REPO, capture_output=True, text=True)
    if bill.returncode:
        errors.append(bill.stderr.strip() or bill.stdout.strip() or "bill slasher cases failed")
    errors.extend(_browser_errors())
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    os.chdir(REPO)
    main()
