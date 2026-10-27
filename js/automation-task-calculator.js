/* Zapier, Make, and n8n burn calculator.
   Task, credit, and execution math uses the published meters.
   An empty poll has no published price. The hourly-poll figure is labeled
   as a planning assumption and drops out when the mix is all webhooks.
   Euros are not converted to dollars. */
(function (root) {
  "use strict";

  var DAYS = 30;
  var POLL_PER_DAY = 24;

  function clamp(value, min, max) {
    var n = Math.round(Number(value));
    if (!isFinite(n)) return min;
    if (n < min) return min;
    if (n > max) return max;
    return n;
  }

  function money(cents, currency) {
    if (cents == null) return "—";
    var abs = Math.abs(Math.round(cents));
    var major = Math.floor(abs / 100);
    var rem = abs % 100;
    var body = String(major).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    var text = rem === 0 ? body : body + "." + (rem < 10 ? "0" : "") + rem;
    var sign = cents < 0 ? "-" : "";
    if (currency === "EUR") return sign + "€" + text;
    return sign + "$" + text;
  }

  function makePlan(credits) {
    if (credits <= 1000) {
      return { tier: "Free", cents: 0, covers: true, note: "Free is $0 with up to 1,000 credits/month." };
    }
    if (credits <= 10000) {
      return {
        tier: "Core",
        cents: 1200,
        covers: true,
        note: "At the displayed 10,000-credit tier, Core is $12/month. Pro is $21 and Teams is $38 at that same displayed tier, so they are not a larger allowance."
      };
    }
    return {
      tier: "Above the 10,000-credit tier",
      cents: null,
      covers: false,
      note: "The checked page prices the 10,000-credit tier and does not publish the next tier. Extra-credit bundles exist on eligible paid plans, without a rate on this page."
    };
  }

  function zapierPlan(tasks) {
    if (tasks <= 100) {
      return { tier: "Free", cents: 0, covers: true, note: "Free is $0 with 100 tasks/month." };
    }
    return {
      tier: "Professional floor",
      cents: null,
      covers: false,
      note: "Professional starts at $19.99/month billed annually, and Team is $69/month billed annually. Neither published line includes the task pack that covers this volume, so this is not a quote."
    };
  }

  function n8nPlan(executions) {
    if (executions <= 2500) {
      return { tier: "Starter", cents: 2000, covers: true, note: "Starter is €20/month billed annually for 2,500 workflow executions. Steps inside a run are unlimited." };
    }
    if (executions <= 10000) {
      return { tier: "Pro", cents: 5000, covers: true, note: "Pro is €50/month billed annually for 10,000 executions." };
    }
    if (executions <= 40000) {
      return { tier: "Business", cents: 66700, covers: true, note: "Business is €667/month billed annually for 40,000 executions, self-hosted." };
    }
    return { tier: "Enterprise", cents: null, covers: false, note: "Enterprise is custom. The published Business cap is 40,000 executions." };
  }

  function priceAutomation(input) {
    var workflows = clamp(input && input.workflows, 1, 500);
    var steps = clamp(input && input.steps, 1, 100);
    var runsPerDay = clamp(input && input.runsPerDay, 0, 10000);
    var webhookPercent = clamp(input && input.webhookPercent, 0, 100);
    var webhookWorkflows = Math.round(workflows * webhookPercent / 100);
    var pollWorkflows = workflows - webhookWorkflows;
    var webhookRuns = webhookWorkflows * runsPerDay * DAYS;
    var pollRuns = pollWorkflows * POLL_PER_DAY * DAYS;
    var runs = webhookRuns + pollRuns;
    var tasks = runs * steps;
    var credits = runs * steps;
    var executions = runs;
    var make = makePlan(credits);
    var zapier = zapierPlan(tasks);
    var n8n = n8nPlan(executions);
    var rows = [
      {
        slug: "zapier",
        name: "Zapier",
        tier: zapier.tier,
        currency: "USD",
        monthlyCents: zapier.covers ? zapier.cents : null,
        annualCents: zapier.covers ? zapier.cents * 12 : null,
        covers: zapier.covers,
        units: tasks,
        unitLabel: "tasks",
        meter: "One task per action step. Filters that stop a Zap are not given a price.",
        expiry: "The checked pricing summary does not state that unused tasks roll over.",
        note: zapier.note,
        href: "/go/zapier/",
        rel: "external noopener"
      },
      {
        slug: "make",
        name: "Make",
        tier: make.tier,
        currency: "USD",
        monthlyCents: make.covers ? make.cents : null,
        annualCents: make.covers ? make.cents * 12 : null,
        covers: make.covers,
        units: credits,
        unitLabel: "credits",
        meter: "One credit per module action. AI modules can cost more; that extra is not estimated.",
        expiry: "Credits normally expire at the end of the subscription term.",
        note: make.note,
        href: "/go/make/",
        rel: "sponsored nofollow noopener"
      },
      {
        slug: "n8n",
        name: "n8n",
        tier: n8n.tier,
        currency: "EUR",
        monthlyCents: n8n.covers ? n8n.cents : null,
        annualCents: n8n.covers ? n8n.cents * 12 : null,
        covers: n8n.covers,
        units: executions,
        unitLabel: "executions",
        meter: "One cloud execution per full workflow run. Steps are unlimited and are not multiplied.",
        expiry: "Assistant credits refresh monthly and do not roll over. Workflow-execution rollover is not stated.",
        note: n8n.note + " Euros are not converted to dollars. Self-host is a separate license path and is not priced as $0 here.",
        href: "/go/n8n/",
        rel: "external noopener"
      }
    ];
    var usd = rows.filter(function (row) { return row.currency === "USD" && row.covers && row.monthlyCents != null; });
    usd.sort(function (a, b) { return a.monthlyCents - b.monthlyCents; });
    rows.forEach(function (row) { row.verdict = row.covers ? "Test" : "Test"; });
    usd.forEach(function (row) { row.verdict = "Switch"; });
    if (usd.length) usd[0].verdict = "Keep";
    var savings = 0;
    if (usd.length > 1) savings = (usd[usd.length - 1].monthlyCents - usd[0].monthlyCents) * 12;
    return {
      workflows: workflows,
      steps: steps,
      runsPerDay: runsPerDay,
      webhookPercent: webhookPercent,
      pollRuns: pollRuns,
      webhookRuns: webhookRuns,
      runs: runs,
      assumption: pollWorkflows > 0
        ? "Polling workflows are planned at 24 checks a day. The vendor pages do not publish an empty-poll price; set webhooks to 100% to drop that assumption."
        : "All workflows are webhooks, so the hourly-poll assumption is not applied.",
      rows: rows,
      savingsAnnualCents: savings,
      savingsNote: usd.length > 1
        ? "Exact annual gap between the highest and lowest published USD plan that covers this volume. Zapier is included only when the 100-task Free plan covers it. n8n stays in euros."
        : "Not enough published USD prices cover this volume for an exact switch saving. A Professional or Team floor is not treated as the bill."
    };
  }

  var api = { priceAutomation: priceAutomation, money: money };
  root.AutomationTaskCalc = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
