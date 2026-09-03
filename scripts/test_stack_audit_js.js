/* Node checks for Stack Audit share/spend helpers. */
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const catalog = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", "stack_audit_catalog.json"), "utf8"));
const html = `<script type="application/json" id="sa-catalog">${JSON.stringify(catalog)}</script>`;
const { JSDOM } = (function () {
  try { return { JSDOM: require("jsdom").JSDOM }; } catch (err) { return {}; }
})();

if (!JSDOM) {
  const src = fs.readFileSync(path.join(__dirname, "..", "js", "stack-audit.js"), "utf8");
  assert.ok(src.includes("monthlySpend"));
  assert.ok(src.includes("includeSpend"));
  assert.ok(!src.includes("est(t)"));
  assert.ok(!/return 20;/.test(src));
  assert.ok(!/return 35;/.test(src));
  console.log("js source checks passed (jsdom not installed)");
  process.exit(0);
}
