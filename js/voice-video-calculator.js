/* Voice, avatar, Runway, and Midjourney seat calculator.
   Prices are the official summaries already on the tool pages.
   Descript uses media minutes. Runway uses the published Gen-4.5
   rate of 12 credits per second. Midjourney uses Fast GPU hours.
   ElevenLabs, HeyGen, and Synthesia stay unconverted. */
(function (root) {
  "use strict";

  var CHECKED = {
    elevenlabs: "2026-09-18",
    descript: "2026-09-18",
    heygen: "2026-09-18",
    synthesia: "2026-09-18",
    runway: "2026-09-18",
    midjourney: "2026-10-01"
  };
  var GEN45_CREDITS_PER_SECOND = 12;
  var RUNWAY = [
    { tier: "Standard", credits: 625, cents: 1500 },
    { tier: "Pro", credits: 2250, cents: 3500 },
    { tier: "Max", credits: 9500, cents: 9500 }
  ];
  var MIDJOURNEY = [
    { tier: "Basic", minutes: 198, cents: 1000, stealth: false, hours: "3.3" },
    { tier: "Standard", minutes: 900, cents: 3000, stealth: false, hours: "15" },
    { tier: "Pro", minutes: 1800, cents: 6000, stealth: true, hours: "30" },
    { tier: "Mega", minutes: 3600, cents: 12000, stealth: true, hours: "60" }
  ];

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

  function runwayRow(videoSeconds) {
    var credits = videoSeconds * GEN45_CREDITS_PER_SECOND;
    var base = {
      slug: "runway",
      name: "Runway",
      href: "/go/runway/",
      rel: "external noopener",
      expiry: "Standard and Pro subscription credits do not roll over. Max allows up to one month of credit rollover. Purchased credits do not expire."
    };
    var rateNote = "Checked " + CHECKED.runway + ": Gen-4.5 is 12 credits per generated second, so Standard's 625 credits are about 52 seconds. The checked page does not publish a Turbo credits-per-second rate, so this row does not price Turbo. The $95 seat is Max with 9,500 credits, not a relaxed unlimited plan and not 2,250 fast credits. Month-to-month prices are used; annual is lower on the same page.";
    if (credits === 0) {
      return Object.assign(base, {
        tier: "No clip",
        monthlyCents: 0,
        annualCents: 0,
        covers: true,
        credits: 0,
        meter: "0 Gen-4.5 credits",
        note: rateNote
      });
    }
    var fit = null;
    for (var i = 0; i < RUNWAY.length; i += 1) {
      if (RUNWAY[i].credits >= credits) {
        fit = RUNWAY[i];
        break;
      }
    }
    if (!fit) {
      return Object.assign(base, {
        tier: "Above Max",
        monthlyCents: null,
        annualCents: null,
        covers: false,
        credits: credits,
        unpriced: "Above the published cap",
        meter: credits + " Gen-4.5 credits",
        note: "Max is 9,500 credits at $95/month, about " + Math.floor(9500 / GEN45_CREDITS_PER_SECOND) + " seconds of Gen-4.5. This clip is past that cap. Enterprise is custom. " + rateNote
      });
    }
    return Object.assign(base, {
      tier: fit.tier,
      monthlyCents: fit.cents,
      annualCents: fit.cents * 12,
      covers: true,
      credits: credits,
      meter: credits + " Gen-4.5 credits · " + fit.tier + " includes " + fit.credits,
      note: "Retakes multiply finished seconds before the 12-credit Gen-4.5 rate. " + rateNote
    });
  }

  function midjourneyRow(demandedMinutes, stealth) {
    var base = {
      slug: "midjourney",
      name: "Midjourney",
      href: "/go/midjourney/",
      rel: "external noopener",
      expiry: "Unused subscription Fast time does not roll over."
    };
    var hours = demandedMinutes / 60;
    var hourLabel = (Math.round(hours * 10) / 10).toString().replace(/\.0$/, "");
    var stealthNote = "Checked " + CHECKED.midjourney + ": Basic is $10 for 3.3 Fast GPU hours, Standard is $30 for 15 hours plus unlimited Relax images, Pro is $60 for 30 hours plus Stealth Mode, and Mega is $120 for 60 hours plus Stealth Mode. Stealth is the private-mode toggle. Basic and Standard leave images in the public gallery. Month-to-month prices are used; annual is 20% lower and is not the figure here.";
    if (demandedMinutes === 0) {
      return Object.assign(base, {
        tier: "No Fast time",
        monthlyCents: 0,
        annualCents: 0,
        covers: true,
        fastHours: 0,
        meter: "0 Fast GPU hours",
        note: stealthNote
      });
    }
    var fit = null;
    for (var i = 0; i < MIDJOURNEY.length; i += 1) {
      var plan = MIDJOURNEY[i];
      if (stealth && !plan.stealth) continue;
      if (demandedMinutes <= plan.minutes) {
        fit = plan;
        break;
      }
    }
    if (!fit) {
      return Object.assign(base, {
        tier: "Above Mega",
        monthlyCents: null,
        annualCents: null,
        covers: false,
        fastHours: hours,
        unpriced: "Above the published cap",
        meter: hourLabel + " Fast GPU " + (hourLabel === "1" ? "hour" : "hours"),
        note: "Mega is 60 Fast GPU hours at $120/month. This job is past that cap. " + stealthNote
      });
    }
    return Object.assign(base, {
      tier: fit.tier,
      monthlyCents: fit.cents,
      annualCents: fit.cents * 12,
      covers: true,
      fastHours: hours,
      meter: hourLabel + " Fast GPU " + (hourLabel === "1" ? "hour" : "hours") + " · " + fit.tier + " includes " + fit.hours,
      note: (stealth ? "Stealth Mode forces Pro or Mega. " : "Relax on Standard and above is unlimited and is not converted into Fast hours. ") + stealthNote
    });
  }

  function priceVoice(input) {
    var minutes = clamp(input && input.minutes, 0, 6000);
    var retake = clamp(input && input.retake, 1, 5);
    var clone = !!(input && input.clone);
    var demanded = minutes * retake;
    var clipSeconds = input && input.seconds != null && input.seconds !== ""
      ? clamp(input.seconds, 0, 3600)
      : minutes * 60;
    var generatedSeconds = clipSeconds * retake;
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
        }),
      runwayRow(generatedSeconds),
      midjourneyRow(demanded, clone)
    ];
    // Voice and avatar seats share one workload. Runway seconds and Midjourney
    // Fast hours are separate jobs, so they do not enter this cheapest pool.
    var voiceSlugs = { descript: 1, elevenlabs: 1, heygen: 1, synthesia: 1 };
    var priced = rows.filter(function (row) {
      return voiceSlugs[row.slug] && row.covers && row.monthlyCents != null;
    });
    priced.sort(function (a, b) { return a.monthlyCents - b.monthlyCents; });
    rows.forEach(function (row) { row.verdict = "Test"; });
    if (priced.length) {
      priced[0].verdict = "Keep";
      priced.slice(1).forEach(function (row) { row.verdict = "Switch"; });
    }
    rows.forEach(function (row) {
      if (row.slug === "runway") {
        row.verdict = generatedSeconds > 0 && row.covers ? "Keep" : "Cut";
      }
      if (row.slug === "midjourney") {
        row.verdict = demanded > 0 && row.covers ? "Keep" : "Cut";
      }
    });
    var keep = priced[0] || null;
    return {
      minutes: minutes,
      retake: retake,
      demandedMinutes: demanded,
      seconds: clipSeconds,
      generatedSeconds: generatedSeconds,
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
