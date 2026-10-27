/* Presentation seat calculator.
   Prices are the checked official summaries. A deck count is not a credit.
   Month-to-month stickers that the page does not print stay unpriced. */
(function (root) {
  "use strict";

  var CHECKED = {
    gamma: "2026-10-01",
    "canva-ai": "2026-10-01",
    htmlslides: "2026-09-18",
    "microsoft-copilot": "2026-10-01"
  };

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
    var dollars = Math.floor(abs / 100);
    var rem = abs % 100;
    var body = String(dollars).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    var text = rem === 0 ? "$" + body : "$" + body + "." + (rem < 10 ? "0" : "") + rem;
    return cents < 0 ? "-" + text : text;
  }

  function row(spec) {
    return {
      slug: spec.slug,
      name: spec.name,
      tier: spec.tier,
      monthlyCents: spec.monthlyCents,
      annualCents: spec.annualCents,
      covers: spec.covers,
      meter: spec.meter,
      note: spec.note,
      href: spec.href,
      rel: spec.rel,
      verdict: "Test"
    };
  }

  function gammaRow(seats, brand, watermark, annual) {
    var checked = "Checked " + CHECKED.gamma + ". ";
    var team = " Team and Business prices did not render on that fetch, so this row does not use them.";
    var free = seats === 1 && !brand && !watermark;
    if (free) {
      return row({
        slug: "gamma",
        name: "Gamma",
        tier: "Free",
        monthlyCents: 0,
        annualCents: 0,
        covers: true,
        meter: "400 one-time signup credits that do not refill. Decks are not a credit unit.",
        note: checked + "Free is $0 for one seat. Branding removal is Plus. Custom branding is Pro." + team,
        href: "/go/gamma/",
        rel: "sponsored nofollow noopener"
      });
    }
    var pro = brand;
    var monthlyEach = pro ? 1800 : 900;
    var annualEach = pro ? 21600 : 10800;
    var tier = pro ? "Pro" : "Plus";
    var feature = pro
      ? "Custom branding is the Pro line ($18/seat/month equivalent, $216/seat billed annually)."
      : "Branding removal, or more than one seat, is the Plus line ($9/seat/month equivalent, $108/seat billed annually).";
    if (!annual) {
      return row({
        slug: "gamma",
        name: "Gamma",
        tier: tier,
        monthlyCents: null,
        annualCents: null,
        covers: false,
        meter: "The month-to-month sticker is not the figure on the checked page.",
        note: checked + feature + " Saving up to 28% is advertised and is not reversed into a monthly price." + team,
        href: "/go/gamma/",
        rel: "sponsored nofollow noopener"
      });
    }
    return row({
      slug: "gamma",
      name: "Gamma",
      tier: tier,
      monthlyCents: monthlyEach * seats,
      annualCents: annualEach * seats,
      covers: true,
      meter: (pro ? "4,000" : "1,000") + " monthly credits per seat. Decks are not a credit unit.",
      note: checked + feature + " The monthly figure is the published annual equivalent, multiplied by seats." + team,
      href: "/go/gamma/",
      rel: "sponsored nofollow noopener"
    });
  }

  function canvaRow(seats, feature, annual) {
    var checked = "Checked " + CHECKED["canva-ai"] + ". ";
    var allowance = " Allowances reset monthly. Saving from 16% on yearly billing is not reversed into a monthly price.";
    if (!feature && seats === 1) {
      return row({
        slug: "canva-ai",
        name: "Canva AI",
        tier: "Free",
        monthlyCents: 0,
        annualCents: 0,
        covers: true,
        meter: "Up to 20 Standard or Premium AI uses. No Ultra. One person.",
        note: checked + "Canva Free is US$0/year for one person." + allowance,
        href: "/go/canva-ai/",
        rel: "external noopener"
      });
    }
    if (feature && seats === 1) {
      return row({
        slug: "canva-ai",
        name: "Canva AI",
        tier: "Not confirmed",
        monthlyCents: null,
        annualCents: null,
        covers: false,
        meter: "Brand kit and watermark removal are not stated on the checked page.",
        note: checked + "Free is one person at US$0/year and does not document a brand kit. Pro is US$144/year for one person. This row does not pretend Free covers the toggle." + allowance,
        href: "/go/canva-ai/",
        rel: "external noopener"
      });
    }
    if (!annual) {
      return row({
        slug: "canva-ai",
        name: "Canva AI",
        tier: "Business",
        monthlyCents: null,
        annualCents: null,
        covers: false,
        meter: "A month-to-month Business sticker is not the figure.",
        note: checked + "More than one person uses Business at US$250/year per person on the annual view. The checked page does not print a month-to-month price." + allowance,
        href: "/go/canva-ai/",
        rel: "external noopener"
      });
    }
    var annualCents = 25000 * seats;
    return row({
      slug: "canva-ai",
      name: "Canva AI",
      tier: "Business",
      monthlyCents: Math.round(annualCents / 12),
      annualCents: annualCents,
      covers: !feature,
      meter: "US$250/year per person. Pro is one person, so extra seats are not priced as Pro.",
      note: checked + (feature
        ? "Business is the published per-person seat. A brand kit or watermark removal is not stated, so this row is not a cover."
        : "Business is US$250/year per person. The monthly cell is that annual price divided by 12.") + allowance,
      href: "/go/canva-ai/",
      rel: "external noopener"
    });
  }

  function slidesRow(seats, feature) {
    var checked = "Checked " + CHECKED.htmlslides + ". ";
    if (seats > 1) {
      return row({
        slug: "htmlslides",
        name: "HTMLSlides",
        tier: "Not a seat price",
        monthlyCents: null,
        annualCents: null,
        covers: false,
        meter: "No per-seat price is published.",
        note: checked + "Free is $0. Pro is $9.90/month, labeled a launch offer. Credits may expire, with no day window. This page does not multiply a missing seat price.",
        href: "/go/htmlslides/",
        rel: "external noopener"
      });
    }
    if (!feature) {
      return row({
        slug: "htmlslides",
        name: "HTMLSlides",
        tier: "Free",
        monthlyCents: 0,
        annualCents: 0,
        covers: true,
        meter: "10 templates, 50MB. Credits are not a deck unit.",
        note: checked + "Free is $0 for one seat. Pro at $9.90/month is a launch offer, not an annual discount.",
        href: "/go/htmlslides/",
        rel: "external noopener"
      });
    }
    return row({
      slug: "htmlslides",
      name: "HTMLSlides",
      tier: "Pro",
      monthlyCents: 990,
      annualCents: 990 * 12,
      covers: false,
      meter: "Launch offer. No published brand-kit or watermark line.",
      note: checked + "Pro is $9.90/month. The checked page does not say that price removes a watermark or adds a brand kit, so the toggle does not count as covered. There is no annual discount. The annual cell is 12 times the launch price.",
      href: "/go/htmlslides/",
      rel: "external noopener"
    });
  }

  function microsoftRow(seats, feature, annual) {
    var checked = "Checked " + CHECKED["microsoft-copilot"] + ". ";
    var list = "Copilot Business is a promotional $18/user/month paid yearly versus a $21 list price. This row uses the $21 list. ";
    var chat = "Copilot Chat without an extra license can use metered pay-as-you-go agents, and that page does not publish the meter rate, so it is not priced as $0. ";
    if (!annual) {
      return row({
        slug: "microsoft-copilot",
        name: "Microsoft 365 Copilot",
        tier: "No month-to-month sticker",
        monthlyCents: null,
        annualCents: null,
        covers: false,
        meter: "Paid yearly. Subscriptions auto-renew.",
        note: checked + list + chat + "Business Standard with Copilot is $23.50 and Business Premium with Copilot is $32, both paid yearly. No month-to-month sticker is published.",
        href: "/go/microsoft-copilot/",
        rel: "external noopener"
      });
    }
    return row({
      slug: "microsoft-copilot",
      name: "Microsoft 365 Copilot",
      tier: "Copilot Business",
      monthlyCents: 2100 * seats,
      annualCents: 2100 * seats * 12,
      covers: !feature,
      meter: "Decks do not meter. $21 list per user, paid yearly.",
      note: checked + list + chat + (feature
        ? "A brand kit or watermark removal is not a published Copilot fee, so the toggle is not covered."
        : "The figure is the $21 list multiplied by seats. The $18 promotion is a note, not the price."),
      href: "/go/microsoft-copilot/",
      rel: "external noopener"
    });
  }

  function assignVerdicts(rows) {
    var priced = rows.filter(function (item) {
      return item.covers && item.monthlyCents != null;
    });
    if (!priced.length) return 0;
    var min = priced[0].monthlyCents;
    var max = priced[0].monthlyCents;
    priced.forEach(function (item) {
      if (item.monthlyCents < min) min = item.monthlyCents;
      if (item.monthlyCents > max) max = item.monthlyCents;
    });
    var limit = min * 2.5;
    priced.forEach(function (item) {
      if (item.monthlyCents === min) item.verdict = "Keep";
      else if (item.monthlyCents <= limit) item.verdict = "Test";
      else item.verdict = "Cut";
    });
    return priced.length > 1 ? (max - min) * 12 : 0;
  }

  function priceDeck(input) {
    var seats = clamp(input && input.seats, 1, 25);
    var decks = clamp(input && input.decks, 0, 400);
    var brand = !!(input && input.brand);
    var watermark = !!(input && input.watermark);
    var annual = !(input && input.annual === false);
    var feature = brand || watermark;
    var rows = [
      gammaRow(seats, brand, watermark, annual),
      canvaRow(seats, feature, annual),
      slidesRow(seats, feature),
      microsoftRow(seats, feature, annual)
    ];
    var savings = assignVerdicts(rows);
    return {
      seats: seats,
      decks: decks,
      brand: brand,
      watermark: watermark,
      annual: annual,
      rows: rows,
      savingsAnnualCents: savings,
      checked: CHECKED
    };
  }

  var api = { priceDeck: priceDeck, money: money, CHECKED: CHECKED };
  root.PresentationCalc = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
