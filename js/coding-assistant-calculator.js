/* AI coding assistant subscription calculator.
   Prices are list prices checked 2026-10-26. Prompt counts choose a published
   plan band. They are not converted into tokens or credits, because none of
   these vendors publish that rate. */
(function (root) {
  "use strict";

  var CHECKED = "2026-10-26";

  function clamp(value, min, max) {
    var n = Math.round(Number(value));
    if (!isFinite(n)) return min;
    if (n < min) return min;
    if (n > max) return max;
    return n;
  }

  function bandOf(prompts) {
    if (prompts <= 25) return "light";
    if (prompts <= 60) return "steady";
    return "heavy";
  }

  function money(cents) {
    var sign = cents < 0 ? "-" : "";
    var abs = Math.abs(Math.round(cents));
    var dollars = Math.floor(abs / 100);
    var rem = abs % 100;
    var body = String(dollars).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    if (rem === 0) return sign + "$" + body;
    return sign + "$" + body + "." + (rem < 10 ? "0" : "") + rem;
  }

  function annualize(monthlyCents, seats, annualPerSeat, annual) {
    if (annual && annualPerSeat != null) {
      var year = annualPerSeat * seats;
      return { monthlyCents: Math.round(year / 12), annualCents: year, annualDiscount: true };
    }
    var month = monthlyCents * seats;
    return { monthlyCents: month, annualCents: month * 12, annualDiscount: false };
  }

  function cursorPlan(band, frontier) {
    if (frontier) {
      if (band === "light") return { tier: "Super", perSeat: 10000, pool: "15× Plus" };
      return { tier: "Ultra", perSeat: 20000, pool: "50× Plus" };
    }
    if (band === "light") return { tier: "Premium", perSeat: 3000, pool: "4× Plus" };
    if (band === "steady") return { tier: "Super", perSeat: 10000, pool: "15× Plus" };
    return { tier: "Ultra", perSeat: 20000, pool: "50× Plus" };
  }

  function claudePlan(band, frontier) {
    if (!frontier && band === "light") {
      return { tier: "Pro", perSeat: 2000, annualPerSeat: 20000, usage: "everyday Claude Code pool" };
    }
    if ((!frontier && band === "steady") || (frontier && band === "light")) {
      return { tier: "Max 5x", perSeat: 10000, annualPerSeat: null, usage: "5× Pro per 5-hour session" };
    }
    return { tier: "Max 20x", perSeat: 20000, annualPerSeat: null, usage: "20× Pro per 5-hour session" };
  }

  function copilotIndividual(band, frontier) {
    if (frontier) {
      if (band === "light") return { tier: "Pro+", perSeat: 3900, credits: 7000 };
      return { tier: "Max", perSeat: 10000, credits: 20000 };
    }
    if (band === "light") return { tier: "Pro", perSeat: 1000, credits: 1500 };
    if (band === "steady") return { tier: "Pro+", perSeat: 3900, credits: 7000 };
    return { tier: "Max", perSeat: 10000, credits: 20000 };
  }

  function copilotPlan(seats, band, frontier) {
    var individual = copilotIndividual(band, frontier);
    var chosen = individual;
    var orgNote = "";
    if (seats >= 2) {
      var org = (frontier || band === "heavy")
        ? { tier: "Enterprise", perSeat: 3900, credits: 3900 }
        : { tier: "Business", perSeat: 1900, credits: 1900 };
      if (org.credits >= individual.credits && org.perSeat < individual.perSeat) {
        chosen = org;
        orgNote = org.tier + " is the lower subscription whose published credit pool is at least " +
          individual.credits.toLocaleString("en-US") + ".";
      } else if (org.credits < individual.credits) {
        orgNote = org.tier + " is $" + (org.perSeat / 100) + "/user with " +
          org.credits.toLocaleString("en-US") + " AI credits. That pool is smaller than " +
          individual.tier + " (" + individual.credits.toLocaleString("en-US") +
          "), so the recommendation stays on " + individual.tier + ".";
      } else {
        orgNote = org.tier + " at $" + (org.perSeat / 100) + "/user includes " +
          org.credits.toLocaleString("en-US") + " credits. " + individual.tier +
          " at $" + (individual.perSeat / 100) + "/user is the lower subscription.";
      }
    }
    return { chosen: chosen, orgNote: orgNote };
  }

  function windsurfPlan(seats, band) {
    if (seats === 1) {
      if (band === "heavy") {
        return {
          tier: "Max",
          perSeat: 20000,
          monthlyCents: 20000,
          note: "Max is individual-only. Extra usage is API list price and is not estimated."
        };
      }
      return {
        tier: "Pro",
        perSeat: 2000,
        monthlyCents: 2000,
        note: "Pro includes frontier models inside a daily and weekly quota. Extra usage is API list price and is not estimated."
      };
    }
    var monthly = Math.max(8000, seats * 4000);
    return {
      tier: "Teams",
      perSeat: 4000,
      monthlyCents: monthly,
      note: band === "heavy"
        ? "Max is individual-only at $200 and cannot be shared. Teams full seats are $40 each, with an $80 minimum and a Pro-equivalent quota. On-demand credits are API-priced and are not estimated."
        : "Each full seat is $40/month with a Pro-equivalent quota. Teams is at least $80/month. On-demand credits are API-priced and are not estimated."
    };
  }

  function withinTestBand(cost, keepCost) {
    return cost * 2 <= keepCost * 5;
  }

  function quote(input) {
    var seats = clamp(input && input.seats, 1, 50);
    var prompts = clamp(input && input.prompts, 5, 100);
    var frontier = !!(input && input.frontier);
    var annual = !!(input && input.annual);
    var band = bandOf(prompts);

    var cursor = cursorPlan(band, frontier);
    var cursorTotals = annualize(cursor.perSeat, seats, null, annual);
    var claude = claudePlan(band, frontier);
    var claudeTotals = annualize(claude.perSeat, seats, claude.annualPerSeat, annual);
    var copilotPick = copilotPlan(seats, band, frontier);
    var copilot = copilotPick.chosen;
    var copilotTotals = annualize(copilot.perSeat, seats, null, annual);
    var windsurf = windsurfPlan(seats, band);
    var windsurfTotals = annualize(windsurf.monthlyCents / seats, seats, null, false);
    if (seats > 1) {
      windsurfTotals = {
        monthlyCents: windsurf.monthlyCents,
        annualCents: windsurf.monthlyCents * 12,
        annualDiscount: false
      };
    }

    var tools = [
      {
        id: "cursor",
        name: "Cursor",
        tier: cursor.tier,
        perSeatCents: cursor.perSeat,
        monthlyCents: cursorTotals.monthlyCents,
        annualCents: cursorTotals.annualCents,
        overageCents: 0,
        includesFrontier: false,
        allowance: cursor.pool,
        annualDiscount: false,
        note: "Overage is not added. Cursor does not publish a dollar price per prompt. Third-party models bill at API list price outside the " + cursor.pool + " pool."
      },
      {
        id: "claude",
        name: "Claude Code",
        tier: claude.tier,
        perSeatCents: annual && claude.annualPerSeat ? claude.annualPerSeat : claude.perSeat,
        monthlyCents: claudeTotals.monthlyCents,
        annualCents: claudeTotals.annualCents,
        overageCents: 0,
        includesFrontier: true,
        allowance: claude.usage,
        annualDiscount: claudeTotals.annualDiscount,
        perSeatIsAnnual: !!(annual && claude.annualPerSeat),
        note: "Overage is not added. Claude Code shares the plan pool, and Anthropic does not publish a prompt-to-token rate. Pay-as-you-go stays at API rates."
      },
      {
        id: "copilot",
        name: "GitHub Copilot",
        tier: copilot.tier,
        perSeatCents: copilot.perSeat,
        monthlyCents: copilotTotals.monthlyCents,
        annualCents: copilotTotals.annualCents,
        overageCents: 0,
        includesFrontier: copilot.tier !== "Pro",
        allowance: copilot.credits.toLocaleString("en-US") + " AI credits / user",
        annualDiscount: false,
        note: "Overage is not added. Extra usage is $0.01 per AI credit, and GitHub does not publish credits per prompt." +
          (copilotPick.orgNote ? " " + copilotPick.orgNote : "")
      },
      {
        id: "windsurf",
        name: "Windsurf",
        tier: windsurf.tier,
        perSeatCents: windsurf.perSeat,
        monthlyCents: windsurfTotals.monthlyCents,
        annualCents: windsurfTotals.annualCents,
        overageCents: 0,
        includesFrontier: true,
        allowance: seats === 1 ? "daily and weekly quota" : "Pro-equivalent quota per full seat",
        annualDiscount: false,
        note: windsurf.note
      }
    ];

    var eligible = tools.filter(function (tool) {
      return !frontier || tool.includesFrontier;
    });
    var pool = eligible.length ? eligible : tools.slice();
    var keep = pool.slice().sort(function (a, b) {
      if (a.monthlyCents !== b.monthlyCents) return a.monthlyCents - b.monthlyCents;
      var order = ["copilot", "windsurf", "claude", "cursor"];
      return order.indexOf(a.id) - order.indexOf(b.id);
    })[0];

    tools.forEach(function (tool) {
      if (tool.id === keep.id) tool.verdict = "Keep";
      else if (withinTestBand(tool.monthlyCents, keep.monthlyCents)) tool.verdict = "Test";
      else tool.verdict = "Cut";
      tool.totalMonthlyCents = tool.monthlyCents + tool.overageCents;
      tool.totalAnnualCents = tool.annualCents;
    });

    return {
      checked: CHECKED,
      seats: seats,
      prompts: prompts,
      band: band,
      frontier: frontier,
      annual: annual,
      tools: tools
    };
  }

  function baseLine(tool, seats, annual) {
    if (tool.id === "claude" && tool.perSeatIsAnnual) {
      return "Base " + money(tool.annualCents) + "/year (" + money(tool.monthlyCents) + "/mo equivalent)";
    }
    if (tool.id === "windsurf" && tool.tier === "Teams") {
      return "Base " + money(tool.perSeatCents) + "/full seat · " + money(tool.monthlyCents) + "/mo, $80 minimum";
    }
    var cadence = annual && tool.annualDiscount ? "/mo equivalent" : "/mo";
    return "Base " + money(tool.perSeatCents) + "/user × " + seats + " = " + money(tool.monthlyCents) + cadence;
  }

  function render(result) {
    var cards = result.tools.map(function (tool) {
      return '<article class="content-hub-card coding-card" data-tool="' + tool.id + '" data-verdict="' + tool.verdict + '" data-monthly="' + tool.totalMonthlyCents + '" data-annual="' + tool.totalAnnualCents + '">' +
        '<p class="coding-card-top"><span class="coding-verdict coding-verdict-' + tool.verdict.toLowerCase() + '">' + tool.verdict + '</span></p>' +
        "<h3>" + tool.name + "</h3>" +
        "<p><strong>Recommended tier:</strong> " + tool.tier + "</p>" +
        "<p>" + baseLine(tool, result.seats, result.annual) + "</p>" +
        "<p><strong>Overage added:</strong> " + money(tool.overageCents) + "</p>" +
        '<p class="coding-monthly"><strong>Monthly total:</strong> ' + money(tool.totalMonthlyCents) + "</p>" +
        "<p><strong>Annual total:</strong> " + money(tool.totalAnnualCents) + "</p>" +
        "<p>Published allowance: " + tool.allowance + ".</p>" +
        "<p>" + tool.note + "</p>" +
        '<p><a href="/go/' + ({ cursor: "cursor", claude: "claude", copilot: "github-copilot", windsurf: "windsurf" })[tool.id] + '/">Switch to ' + tool.name + "</a></p>" +
        "</article>";
    }).join("");
    var kept = result.tools.filter(function (tool) { return tool.verdict === "Keep"; })[0];
    return '<p class="coding-summary">Lowest published subscription for this profile: <strong>' + kept.name + " " + kept.tier + "</strong> at " + money(kept.totalMonthlyCents) + "/mo (" + money(kept.totalAnnualCents) + "/year). Band: " + result.band + (result.frontier ? ", frontier" : ", balanced") + ".</p>" +
      '<div class="content-hub-grid">' + cards + "</div>";
  }

  function readForm(form) {
    var tier = form.querySelector('input[name="coding-tier"]:checked');
    var cadence = form.querySelector('input[name="coding-cadence"]:checked');
    return {
      seats: form.querySelector("#coding-seats").value,
      prompts: form.querySelector("#coding-prompts").value,
      frontier: tier && tier.value === "frontier",
      annual: cadence && cadence.value === "annual"
    };
  }

  function paint(form) {
    var result = quote(readForm(form));
    var mount = document.getElementById("coding-result");
    if (mount) mount.innerHTML = render(result);
  }

  function bindPair(range, number, form) {
    function fromRange() {
      number.value = range.value;
      paint(form);
    }
    function fromNumber() {
      var min = Number(number.min);
      var max = Number(number.max);
      number.value = String(clamp(number.value, min, max));
      range.value = number.value;
      paint(form);
    }
    range.addEventListener("input", fromRange);
    number.addEventListener("input", fromNumber);
  }

  function init() {
    var form = document.getElementById("coding-calc");
    if (!form) return;
    bindPair(form.querySelector("#coding-seats-range"), form.querySelector("#coding-seats"), form);
    bindPair(form.querySelector("#coding-prompts-range"), form.querySelector("#coding-prompts"), form);
    form.addEventListener("change", function () { paint(form); });
    paint(form);
  }

  root.CodingAssistantCalc = {
    CHECKED: CHECKED,
    quote: quote,
    money: money,
    render: render,
    init: init
  };

  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", init);
    } else {
      init();
    }
  }
})(typeof window !== "undefined" ? window : globalThis);
