/* Resolution-fee versus seat calculator.
   Rates come from data/customer_support_pricing.json, inlined on the page.
   A missing list price stays null. The retry toggle's 25% is this page's
   assumption, not a vendor statistic. */
(function (root) {
  "use strict";

  function clamp(value, min, max) {
    var n = Math.round(Number(value));
    if (!isFinite(n)) return min;
    if (n < min) return min;
    if (n > max) return max;
    return n;
  }

  function money(cents) {
    if (cents == null) return "—";
    var abs = Math.abs(Math.round(cents));
    var major = Math.floor(abs / 100);
    var rem = abs % 100;
    var body = String(major).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    var text = rem === 0 ? body : body + "." + (rem < 10 ? "0" : "") + rem;
    return (cents < 0 ? "-$" : "$") + text;
  }

  function resolutionsOf(tickets, rate) {
    return Math.round(tickets * rate / 100);
  }

  function inflated(count, on) {
    if (!on) return count;
    return Math.round(count * 1.25);
  }

  function customgptCost(queries, pricing) {
    var spec = pricing.customgpt;
    function path(base, included) {
      var over = Math.max(0, queries - included);
      var packs = over === 0 ? 0 : Math.ceil(over / spec.extra_queries);
      return {
        cents: base + packs * spec.extra_cents,
        packs: packs,
        base: base,
        trap: packs * spec.extra_cents
      };
    }
    var standard = path(spec.standard_cents, spec.standard_queries);
    var premium = path(spec.premium_cents, spec.premium_queries);
    var pick = standard.cents <= premium.cents ? standard : premium;
    pick.tier = pick === standard ? "Standard" : "Premium";
    pick.included = pick === standard ? spec.standard_queries : spec.premium_queries;
    return pick;
  }

  function tidioPack(conversations, pricing) {
    var packs = pricing.tidio.packs_monthly;
    var i;
    for (i = 0; i < packs.length; i += 1) {
      if (conversations <= packs[i].conversations) return packs[i];
    }
    return null;
  }

  function priceSupport(input, pricing) {
    var tickets = clamp(input.tickets, 100, 25000);
    var rate = clamp(input.rate, 20, 80);
    var seats = clamp(input.seats, 1, 50);
    var reopen = !!input.reopen;
    var finMode = input.finMode === "standalone" ? "standalone" : "desk";
    var zdPlan = input.zdPlan === "pro" ? "pro" : "team";
    var zdAnnual = input.zdBilling !== "monthly";
    var zdCommitted = input.zdResolution === "committed";
    var copilot = !!input.copilot;
    var resolved = resolutionsOf(tickets, rate);
    var fin = pricing.intercom;
    var finOutcomes = resolved;
    var finBase = 0;
    var finTrap = 0;
    var finNote;
    if (finMode === "standalone") {
      var billed = Math.max(finOutcomes, fin.standalone_minimum_outcomes);
      finTrap = (billed - finOutcomes) * fin.outcome_cents;
      finNote = "Standalone Fin: no seat fee. Minimum " + fin.standalone_minimum_outcomes + " outcomes.";
      var finRes = billed * fin.outcome_cents;
      var finMonthly = finRes;
    } else {
      finBase = seats * fin.essential_annual_cents;
      finRes = finOutcomes * fin.outcome_cents;
      finMonthly = finBase + finRes;
      finNote = "Essential seats at the annual rate. At least one full seat. Monthly seat price was not in the FAQ extract.";
    }
    var zd = pricing.zendesk.plans[zdPlan];
    var zdSeat = zdAnnual ? zd.annual_cents : zd.monthly_cents;
    var zdBase = seats * zdSeat;
    var included = zd.included_per_agent * seats;
    var zdExtra = Math.max(0, resolved - included);
    var zdRate = zdCommitted ? pricing.zendesk.committed_cents : pricing.zendesk.payg_cents;
    var zdRes = zdExtra * zdRate;
    var zdCopilot = 0;
    var zdCopilotNote = "Copilot off.";
    if (copilot && zd.copilot) {
      zdCopilot = seats * pricing.zendesk.copilot_annual_cents;
      zdCopilotNote = "Copilot at the yearly $50 per agent rate.";
    } else if (copilot) {
      zdCopilotNote = "Copilot is listed for Professional and higher, so it is not added on Suite Team.";
    }
    var zdMonthly = zdBase + zdRes + zdCopilot;

    var lyroCount = inflated(resolved, reopen);
    var pack = tidioPack(lyroCount, pricing);
    var tidioMonthly = pack ? pack.cents : null;
    var gptQueries = inflated(resolved, reopen);
    var gpt = customgptCost(gptQueries, pricing);

    var rows = [
      {
        id: "intercom",
        name: "Intercom Fin",
        monthlyCents: finMonthly,
        baseCents: finBase,
        resolutionCents: finMode === "standalone" ? finOutcomes * fin.outcome_cents : finRes,
        trapCents: finTrap,
        detail: finNote + " Outcomes billed: " + (finMode === "standalone" ? Math.max(finOutcomes, fin.standalone_minimum_outcomes) : finOutcomes) + ". A reply in the same conversation is not a second outcome.",
        href: "https://www.intercom.com/pricing",
        rel: "external noopener",
        linkLabel: "Official pricing"
      },
      {
        id: "zendesk",
        name: "Zendesk AI agents",
        monthlyCents: zdMonthly,
        baseCents: zdBase,
        resolutionCents: zdRes,
        trapCents: zdCopilot,
        detail: zd.name + (zdAnnual ? " annual" : " monthly") + ". Included resolutions: " + included + ". Extra: " + zdExtra + " at " + money(zdRate) + ". " + zdCopilotNote,
        href: "https://www.zendesk.com/pricing/",
        rel: "external noopener",
        linkLabel: "Official pricing"
      },
      {
        id: "tidio",
        name: "Tidio Lyro",
        monthlyCents: tidioMonthly,
        baseCents: 0,
        resolutionCents: tidioMonthly,
        trapCents: 0,
        detail: pack
          ? "Monthly pack of " + pack.conversations + " Lyro conversations covers " + lyroCount + ". The free 50 do not renew, so they are not deducted."
          : "Above 1,000 Lyro conversations the pricing page says contact sales. This row is not given a dollar.",
        href: "https://www.tidio.com/pricing/",
        rel: "external noopener",
        linkLabel: "Official pricing"
      },
      {
        id: "customgpt",
        name: "CustomGPT.ai",
        monthlyCents: gpt.cents,
        baseCents: gpt.base,
        resolutionCents: 0,
        trapCents: gpt.trap,
        detail: gpt.tier + " subscription. Queries counted: " + gptQueries + ". Included: " + gpt.included + ". Extra query packs: " + gpt.packs + ". No per-resolution fee.",
        href: "/go/customgpt/",
        rel: "sponsored nofollow noopener",
        partner: true,
        linkLabel: "Partner link · CustomGPT.ai →",
        reviewHref: "/tools/customgpt/"
      },
      {
        id: "enterprise",
        name: "Ada / Sierra",
        monthlyCents: null,
        baseCents: null,
        resolutionCents: null,
        trapCents: null,
        detail: "No published per-resolution list price. Third-party contract write-ups are not added. Compare a quote with the ranked totals above.",
        href: "https://www.ada.cx/",
        rel: "external noopener",
        linkLabel: "Ada"
      }
    ];
    var priced = rows.filter(function (row) { return row.monthlyCents != null; });
    priced.sort(function (a, b) { return a.monthlyCents - b.monthlyCents; });
    var unpriced = rows.filter(function (row) { return row.monthlyCents == null; });
    priced.forEach(function (row, index) { row.rank = index + 1; });
    return {
      tickets: tickets,
      rate: rate,
      seats: seats,
      reopen: reopen,
      resolved: resolved,
      rows: priced.concat(unpriced)
    };
  }

  function render(result) {
    return result.rows.map(function (row) {
      var total = row.monthlyCents == null ? "Unpriced" : money(row.monthlyCents) + "/mo · " + money(row.monthlyCents * 12) + "/yr";
      var parts = row.monthlyCents == null ? "" : (
        "<p>Base seats " + money(row.baseCents) +
        " · resolution fees " + money(row.resolutionCents) +
        " · floor or add-on " + money(row.trapCents) + "</p>"
      );
      var review = row.reviewHref ? ' · <a href="' + row.reviewHref + '">Audit</a>' : "";
      var partner = row.partner ? ' data-partner-slug="customgpt"' : "";
      return '<article class="ledger-sheet" data-support-row="' + row.id + '">' +
        "<h3>" + (row.rank ? row.rank + ". " : "") + row.name + "</h3>" +
        "<p><strong>" + total + "</strong></p>" +
        parts +
        "<p>" + row.detail + "</p>" +
        '<p><a href="' + row.href + '" rel="' + row.rel + '"' + partner + ">" + row.linkLabel + "</a>" + review + "</p>" +
        "</article>";
    }).join("");
  }

  function readForm(form) {
    function val(name) {
      var el = form.querySelector("[name=\"" + name + "\"]");
      return el ? el.value : "";
    }
    function on(name) {
      var el = form.querySelector("[name=\"" + name + "\"]");
      return !!(el && el.checked);
    }
    return {
      tickets: val("tickets"),
      rate: val("rate"),
      seats: val("seats"),
      reopen: on("reopen"),
      finMode: val("fin-mode"),
      zdPlan: val("zd-plan"),
      zdBilling: val("zd-billing"),
      zdResolution: val("zd-resolution"),
      copilot: on("copilot")
    };
  }

  function applyPreset(form, name) {
    var presets = {
      solo: { tickets: 800, rate: 45, seats: 2 },
      ecom: { tickets: 3500, rate: 55, seats: 6 },
      scale: { tickets: 12000, rate: 60, seats: 18 }
    };
    var preset = presets[name];
    if (!preset) return;
    form.querySelector("[name=tickets]").value = preset.tickets;
    form.querySelector("[name=rate]").value = preset.rate;
    form.querySelector("[name=seats]").value = preset.seats;
  }

  function queryFrom(input) {
    var params = new URLSearchParams();
    params.set("tickets", input.tickets);
    params.set("rate", input.rate);
    params.set("seats", input.seats);
    params.set("reopen", input.reopen ? "1" : "0");
    params.set("fin", input.finMode || "desk");
    params.set("zd", input.zdPlan || "team");
    params.set("zdbill", input.zdBilling || "annual");
    params.set("zdres", input.zdResolution || "payg");
    params.set("copilot", input.copilot ? "1" : "0");
    return params.toString();
  }

  function fillForm(form, params) {
    function set(name, value) {
      var el = form.querySelector("[name=\"" + name + "\"]");
      if (el && value != null && value !== "") el.value = value;
    }
    set("tickets", params.get("tickets"));
    set("rate", params.get("rate"));
    set("seats", params.get("seats"));
    set("fin-mode", params.get("fin"));
    set("zd-plan", params.get("zd"));
    set("zd-billing", params.get("zdbill"));
    set("zd-resolution", params.get("zdres"));
    var reopen = form.querySelector("[name=reopen]");
    if (reopen && params.get("reopen") === "1") reopen.checked = true;
    var copilot = form.querySelector("[name=copilot]");
    if (copilot && params.get("copilot") === "1") copilot.checked = true;
  }

  var api = {
    priceSupport: priceSupport,
    render: render,
    readForm: readForm,
    applyPreset: applyPreset,
    queryFrom: queryFrom,
    fillForm: fillForm,
    money: money
  };
  root.SupportCalc = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
