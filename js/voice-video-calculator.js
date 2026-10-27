/* Voice and avatar seat calculator.
   Prices are the official summaries already on the tool pages.
   Finished minutes select a plan only when that page meters media hours.
   Credit tools do not get an invented credit-per-minute rate. */
(function (root) {
  "use strict";

  var CHECKED = {
    elevenlabs: "2026-09-18",
    descript: "2026-09-18",
    heygen: "2026-09-18",
    synthesia: "2026-09-18"
  };

  var DESCRIPT = [
    { tier: "Free", minutes: 60, cents: 0 },
    { tier: "Hobbyist", minutes: 600, cents: 2400 },
    { tier: "Creator", minutes: 1800, cents: 3500 },
    { tier: "Business", minutes: 2400, cents: 6500 }
  ];

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

  function descriptRow(minutes) {
    var fit = null;
    for (var i = 0; i < DESCRIPT.length; i += 1) {
      if (DESCRIPT[i].minutes >= minutes) {
        fit = DESCRIPT[i];
        break;
      }
    }
    if (!fit) {
      return {
        slug: "descript",
        name: "Descript",
        tier: "Above Business",
        monthlyCents: null,
        annualCents: null,
        covers: false,
        meter: "Media hours",
        expiry: "The checked page gives a monthly media-hour cap and does not say unused hours roll over.",
        note: "Business is 40 media hours (2,400 minutes) at $65/month. This job is past that published cap. Enterprise is custom.",
        href: "/go/descript/",
        rel: "sponsored nofollow noopener"
      };
    }
    return {
      slug: "descript",
      name: "Descript",
      tier: fit.tier,
      monthlyCents: fit.cents,
      annualCents: fit.cents * 12,
      covers: true,
      meter: fit.minutes + " published media minutes",
      expiry: "The checked page gives a monthly media-hour cap and does not say unused hours roll over.",
      note: "Month-to-month list price. Annual billing is cheaper on the same page and is not the figure used here. Retakes count as another full media minute. No separate Overdub fee is published.",
      href: "/go/descript/",
      rel: "sponsored nofollow noopener"
    };
  }

  function creditRow(spec) {
    return {
      slug: spec.slug,
      name: spec.name,
      tier: spec.tier,
      monthlyCents: null,
      annualCents: null,
      covers: false,
      meter: spec.meter,
      expiry: spec.expiry,
      note: spec.note,
      href: spec.href,
      rel: spec.rel
    };
  }

  function priceVoice(input) {
    var minutes = clamp(input && input.minutes, 0, 6000);
    var retake = clamp(input && input.retake, 1, 3);
    var clone = !!(input && input.clone);
    var demanded = minutes * retake;
    var rows = [
      descriptRow(demanded),
      creditRow({
        slug: "elevenlabs",
        name: "ElevenLabs",
        tier: "Credit seat",
        meter: "Credits, not minutes",
        expiry: "Paid-plan credits can roll over up to two months' worth while the subscription stays active.",
        note: "Checked " + CHECKED.elevenlabs + ": Free $0 / 10,000 credits, Starter $6 / 30,000, Creator $22 / 121,000 (first month advertised at $11; the list price is $22), Pro $99 / 600,000. No credit-per-finished-minute is in that summary, so minutes do not pick a tier and overage stays $0.",
        href: "/go/elevenlabs/",
        rel: "sponsored nofollow noopener"
      }),
      creditRow({
        slug: "heygen",
        name: "HeyGen",
        tier: "Credit seat",
        meter: "Credits, not minutes",
        expiry: "The checked pricing summary does not state a credit rollover rule.",
        note: "Checked " + CHECKED.heygen + ": Free $0 up to 3 videos/month, Creator $29/month with 600 credits, Pro starts at $49 with 1,000 credits, Business $149 with 1,500 credits. No credit-per-minute rate is published there. The clone toggle does not add a fee.",
        href: "/go/heygen/",
        rel: "external noopener"
      }),
      clone
        ? creditRow({
          slug: "synthesia",
          name: "Synthesia",
          tier: "Enterprise",
          meter: "Personal Avatars on Enterprise",
          expiry: "The checked pricing summary does not state a credit rollover rule.",
          note: "Checked " + CHECKED.synthesia + ": the pricing text puts unlimited Personal Avatars on Enterprise, which is custom. Starter is $29/month with 1,200 credits when you are not pricing a personal avatar. This page does not invent a clone add-on.",
          href: "/go/synthesia/",
          rel: "external noopener"
        })
        : creditRow({
          slug: "synthesia",
          name: "Synthesia",
          tier: "Credit seat",
          meter: "Credits, not minutes",
          expiry: "The checked pricing summary does not state a credit rollover rule.",
          note: "Checked " + CHECKED.synthesia + ": Basic $0 / 1,200 credits a month, Starter $29 / 1,200 credits, Creator $89 / 3,600 credits. No credit-per-minute rate is in that summary.",
          href: "/go/synthesia/",
          rel: "external noopener"
        })
    ];
    var priced = rows.filter(function (row) { return row.covers && row.monthlyCents != null; });
    priced.sort(function (a, b) { return a.monthlyCents - b.monthlyCents; });
    rows.forEach(function (row) { row.verdict = "Test"; });
    if (priced.length) {
      priced[0].verdict = "Keep";
      priced.slice(1).forEach(function (row) { row.verdict = "Switch"; });
    }
    var keep = priced[0] || null;
    return {
      minutes: minutes,
      retake: retake,
      demandedMinutes: demanded,
      clone: clone,
      rows: rows,
      keepSlug: keep ? keep.slug : "",
      savingsAnnualCents: priced.length > 1 ? (priced[priced.length - 1].monthlyCents - priced[0].monthlyCents) * 12 : 0
    };
  }

  var api = { priceVoice: priceVoice, money: money, CHECKED: CHECKED };
  root.VoiceVideoCalc = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
