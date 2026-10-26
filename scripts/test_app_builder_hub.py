#!/usr/bin/env python3
"""The app-builder calculator prices duplicate seats from the 25 Oct 2026 check."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NODE = r"""
const fs = require("fs");
const vm = require("vm");
const context = { console };
vm.createContext(context);
vm.runInContext(fs.readFileSync("js/app-builder-calculator.js", "utf8"), context);
const rec = context.AppBuilderCalc.recommend;
const cases = [
  [["legacy-v0", "bolt-pro", "lovable-pro"], "shipping", null, 600, ["Legacy v0 Premium ($20/mo)"], ["Bolt.new Pro ($25/mo)", "Lovable Pro ($25/mo)"]],
  [["bolt-pro"], "shipping", null, 0, ["Bolt.new Pro ($25/mo)"], []],
  [["bolt-pro", "lovable-pro"], "quarterly", null, 600, [], ["Bolt.new Pro ($25/mo)", "Lovable Pro ($25/mo)"]],
  [[], "shipping", null, 0, [], []],
  [["replit-core", "v0-plus"], "shipping", "replit-core", 360, ["Replit Core ($20/mo)"], ["v0 Plus ($30/mo)"]],
  [["legacy-v0", "v0-plus"], "idle", null, 360, ["Legacy v0 Premium ($20/mo)"], ["v0 Plus ($30/mo)"]],
  [["lovable-pro"], "idle", null, 300, [], ["Lovable Pro ($25/mo)"]],
  [["v0-plus"], "shipping", null, 0, ["v0 Plus ($30/mo)"], []]
];
const errors = [];
for (const [seats, cadence, active, waste, keep, cut] of cases) {
  const result = rec(seats, cadence, active);
  if (result.wasteAnnual !== waste) errors.push(seats.join("+") + " " + cadence + " waste " + result.wasteAnnual);
  if (JSON.stringify(result.keep) !== JSON.stringify(keep)) errors.push(seats.join("+") + " keep " + JSON.stringify(result.keep));
  if (JSON.stringify(result.cut) !== JSON.stringify(cut)) errors.push(seats.join("+") + " cut " + JSON.stringify(result.cut));
  if (!result.test.some((line) => line.indexOf("Bolt.new Free") !== -1)) errors.push("missing Bolt.new Free");
  if (!result.test.some((line) => line.indexOf("Lovable Free") !== -1)) errors.push("missing Lovable Free");
}
const v0 = rec(["v0-plus"], "shipping", null);
if (!v0.expiry.some((line) => line.indexOf("65 days") !== -1)) errors.push("v0 expiry");
const lovable = rec(["lovable-pro"], "quarterly", null);
if (!lovable.expiry.some((line) => line.indexOf("2 months") !== -1)) errors.push("lovable expiry");
if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}
"""


def main() -> None:
    errors: list[str] = []
    proc = subprocess.run(
        ["node", "-e", NODE],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    if proc.returncode:
        errors.append(proc.stderr.strip() or proc.stdout.strip() or "calculator cases failed")
    page_path = REPO / "compare" / "ai-app-builders" / "index.html"
    if not page_path.is_file():
        errors.append("missing compare/ai-app-builders/index.html")
    else:
        page = page_path.read_text(encoding="utf-8")
        for needle in (
            "Legacy v0 $20",
            "v0 Plus $30",
            "Replit Core $20",
            "Bolt.new Pro $25",
            "Lovable Pro $25",
            "65 days",
            "2 months",
            "FAQPage",
            "SoftwareApplication",
            "Article",
            'href="/tools/v0/"',
            'href="/tools/replit-ai/"',
            'href="/tools/bolt-new/"',
            'href="/tools/lovable/"',
            'href="/newsletter/2026-w44.html"',
            "https://aitoolsessentials.com/compare/ai-app-builders/",
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
    if "https://aitoolsessentials.com/compare/ai-app-builders/" not in sitemap:
        errors.append("sitemap missing the app-builder hub")
    for slug in ("v0", "replit-ai", "bolt-new", "lovable"):
        review = (REPO / "tools" / slug / "index.html").read_text(encoding="utf-8")
        if 'href="/compare/ai-app-builders/"' not in review:
            errors.append(f"tools/{slug} does not link the calculator")
    letter = (REPO / "newsletter" / "2026-w44.html").read_text(encoding="utf-8")
    if 'href="/compare/ai-app-builders/"' not in letter:
        errors.append("issue 7 does not link the calculator")
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
