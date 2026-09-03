/* Stack Audit — client-side only. No accounts, no submissions, no inferred spend. */
(function (root) {
  var catalogEl = typeof document !== "undefined" ? document.getElementById("sa-catalog") : null;
  var CATALOG = catalogEl ? JSON.parse(catalogEl.textContent) : { tools: [], rules: {} };
  var RULES = CATALOG.rules || {};
  var TOOLS = CATALOG.tools || [];
  var BY_SLUG = {};
  TOOLS.forEach(function (t) { BY_SLUG[t.slug] = t; });
  var USE_IDS = (RULES.use_cases || []).map(function (u) { return u.id; });
  var USE_LABEL = {};
  (RULES.use_cases || []).forEach(function (u) { USE_LABEL[u.id] = u.label; });
  var SESSION_KEY = RULES.session_key || "ait.stackAudit.v1";
  var LOCAL_KEY = RULES.local_key || "ait.stackAudit.saved.v1";
  var PREFIX = RULES.fragment_prefix || "sa1.";
  var MAX_TOOLS = RULES.max_tools || 16;
  var MAX_USE = RULES.max_use_cases || 5;
  var MAX_NAME = RULES.max_custom_name || 40;
  var MAX_FRAG = RULES.max_fragment_chars || 1800;
  var MAX_AMT = RULES.max_amount || 100000;
  var MAX_SEATS = RULES.max_seats || 1000;
  var SCORE = RULES.score || {};

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function sanitizeName(name) {
    var cleaned = String(name || "").replace(/<[^>]*>/g, "");
    cleaned = cleaned.replace(/[^a-zA-Z0-9 .'+&/-]+/g, "").trim().replace(/\s+/g, " ");
    return cleaned.slice(0, MAX_NAME);
  }
  function customSlug(name) {
    var stem = sanitizeName(name).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    return ("c:" + (stem || "custom")).slice(0, 50);
  }
  function validSlug(slug) {
    return /^[a-z0-9][a-z0-9-]{0,62}$/.test(slug) || /^c:[a-z0-9][a-z0-9-]{0,47}$/.test(slug);
  }
  function finiteAmount(value) {
    if (value === null || value === undefined || value === "") return null;
    var n = Number(value);
    if (!isFinite(n) || n < 0 || n > MAX_AMT) return null;
    return Math.round(n * 100) / 100;
  }
  function normalizeUse(values) {
    var out = [];
    (values || []).forEach(function (id) {
      if (USE_IDS.indexOf(id) !== -1 && out.indexOf(id) === -1 && out.length < MAX_USE) out.push(id);
    });
    return out;
  }
  function monthlySpend(tool) {
    var kind = tool.spend_kind || "unknown";
    var amount = finiteAmount(tool.amount);
    var seats = Math.max(1, Math.min(MAX_SEATS, parseInt(tool.seats, 10) || 1));
    if (kind === "free") return 0;
    if (kind === "unknown") return null;
    if (kind === "annual") return amount == null ? null : Math.round((amount / 12) * 100) / 100;
    if (kind === "seats") return amount == null ? null : Math.round((amount * seats) * 100) / 100;
    if (kind === "monthly" || kind === "custom" || kind === "promo" || kind === "usage") return amount;
    return null;
  }
  function sharedUse(a, b) {
    var right = normalizeUse(b.use_cases);
    return normalizeUse(a.use_cases).filter(function (id) { return right.indexOf(id) !== -1; }).sort();
  }
  function overlapPairs(tools) {
    var pairs = [];
    for (var i = 0; i < tools.length; i++) {
      for (var j = i + 1; j < tools.length; j++) {
        var shared = sharedUse(tools[i], tools[j]);
        if (shared.length) {
          pairs.push({
            a: tools[i].slug, b: tools[j].slug,
            a_name: tools[i].name, b_name: tools[j].name,
            shared: shared,
            uncertain: !tools[i].capabilities_known || !tools[j].capabilities_known
          });
        }
      }
    }
    return pairs;
  }
  function overlapClusters(tools) {
    var parent = {};
    tools.forEach(function (t) { parent[t.slug] = t.slug; });
    function find(s) { while (parent[s] !== s) { parent[s] = parent[parent[s]]; s = parent[s]; } return s; }
    overlapPairs(tools).forEach(function (p) {
      var ra = find(p.a), rb = find(p.b);
      if (ra !== rb) parent[rb] = ra;
    });
    var groups = {};
    tools.forEach(function (t) {
      var rootSlug = find(t.slug);
      (groups[rootSlug] = groups[rootSlug] || []).push(t);
    });
    return Object.keys(groups).map(function (k) { return groups[k]; }).filter(function (m) { return m.length > 1; }).map(function (members) {
      var shared = {};
      var uncertain = members.some(function (m) { return !m.capabilities_known; });
      for (var i = 0; i < members.length; i++) {
        for (var j = i + 1; j < members.length; j++) {
          sharedUse(members[i], members[j]).forEach(function (id) { shared[id] = true; });
        }
      }
      return {
        slugs: members.map(function (m) { return m.slug; }),
        names: members.map(function (m) { return m.name; }),
        shared: Object.keys(shared).sort(),
        uncertain: uncertain
      };
    });
  }
  function catalogGap(tool) {
    if (String(tool.slug || "").indexOf("c:") === 0) return true;
    if (tool.capabilities_known === false) return true;
    if (!tool.price_confidence || tool.price_confidence === "missing") return true;
    return false;
  }
  function recommendTool(tool, tools) {
    var unique = !!tool.unique;
    var weekly = !!tool.weekly;
    var spend = monthlySpend(tool);
    var partners = [];
    tools.forEach(function (other) {
      if (other.slug === tool.slug) return;
      var shared = sharedUse(tool, other);
      if (shared.length) partners.push({ other: other, shared: shared });
    });
    partners.sort(function (x, y) {
      return y.shared.length - x.shared.length || (x.other.weekly ? 0 : 1) - (y.other.weekly ? 0 : 1);
    });
    var top = partners[0];
    if (unique) return { action: "Keep", why: "You marked a unique must-keep workflow that the rest of this stack does not replace." };
    if (!weekly) {
      if (spend != null && spend > 0) {
        if (top) return { action: "Cut", why: "Not used weekly, overlaps with " + top.other.name + " on " + top.shared.map(labelOf).join(", ") + ", and has entered paid spend with no unique workflow." };
        return { action: "Cut", why: "Not used weekly and has entered paid spend with no unique must-keep workflow." };
      }
      if (spend === 0) return { action: "Cut", why: "Not used weekly, marked free by you, and has no unique must-keep workflow." };
      return { action: "Review", why: "Not used weekly, but spend is unknown — confirm the bill before canceling." };
    }
    if (top) {
      var labels = top.shared.map(labelOf).join(", ");
      var weeklyPartner = partners.some(function (p) { return p.other.weekly; });
      if (top.shared.length >= 2 && weeklyPartner) {
        return { action: "Replace", why: "Shares " + top.shared.length + " use cases (" + labels + ") with " + top.other.name + ", which is also used weekly. Decide which tool should own that job." };
      }
      return { action: "Trial first", why: "Possible overlap with " + top.other.name + " on " + labels + ". Run the same weekly task in both before paying for both." };
    }
    if (catalogGap(tool)) return { action: "Review", why: "Official price or capability data is missing, so this stays a review — nothing is invented." };
    return { action: "Keep", why: "Used weekly and does not share a normalized use case with another selected tool." };
  }
  function labelOf(id) { return USE_LABEL[id] || id; }
  function currentCost(tools) {
    var monthly = 0, known = 0, unknownNames = [];
    tools.forEach(function (t) {
      var value = monthlySpend(t);
      if (value == null) unknownNames.push(t.name);
      else { monthly += value; known += 1; }
    });
    return { monthly: Math.round(monthly * 100) / 100, known_count: known, unknown_count: unknownNames.length, unknown_names: unknownNames };
  }
  function savings(tools, recs) {
    var by = {};
    tools.forEach(function (t) { by[t.slug] = t; });
    var monthly = 0, from = [];
    recs.forEach(function (rec) {
      if (rec.action !== "Cut") return;
      var t = by[rec.slug];
      var value = t ? monthlySpend(t) : null;
      if (value && value > 0) { monthly += value; from.push(t.name); }
    });
    monthly = Math.round(monthly * 100) / 100;
    return { monthly: monthly, annual: Math.round(monthly * 12 * 100) / 100, from_tools: from };
  }
  function scoreStack(tools) {
    var factors = [{ id: "base", label: "Starting score", points: SCORE.start || 100 }];
    var total = SCORE.start || 100;
    var unusedPaid = 0, unknown = 0, freeCount = 0, known = 0;
    tools.forEach(function (t) {
      var value = monthlySpend(t);
      if (value == null) unknown += 1;
      else {
        known += 1;
        if (value > 0 && !t.weekly && !t.unique) unusedPaid += 1;
      }
      if (t.spend_kind === "free") freeCount += 1;
    });
    if (unusedPaid) {
      var p = (SCORE.unused_paid || -12) * unusedPaid;
      total += p;
      factors.push({ id: "unused_paid", label: unusedPaid + " unused paid tool" + (unusedPaid === 1 ? "" : "s") + " (not weekly, no unique workflow, known spend > $0)", points: p });
    }
    var pairs = overlapPairs(tools);
    if (pairs.length) {
      var raw = (SCORE.overlap_pair || -8) * pairs.length;
      var pts = Math.max(raw, SCORE.overlap_pair_cap || -40);
      total += pts;
      factors.push({ id: "overlap_pair", label: pairs.length + " overlapping pair" + (pairs.length === 1 ? "" : "s") + " by shared use case", points: pts });
    }
    if (unknown) {
      var up = (SCORE.unknown_spend || -5) * unknown;
      total += up;
      factors.push({ id: "unknown_spend", label: unknown + " tool" + (unknown === 1 ? "" : "s") + " with unknown spend", points: up });
    }
    var extra = Math.max(0, tools.length - (SCORE.stack_size_over || 5));
    if (extra) {
      var sp = Math.max((SCORE.stack_size_each || -3) * extra, SCORE.stack_size_cap || -15);
      total += sp;
      factors.push({ id: "stack_size", label: tools.length + " tools (penalty starts after " + (SCORE.stack_size_over || 5) + ")", points: sp });
    }
    var coverage = {};
    tools.forEach(function (t) {
      normalizeUse(t.use_cases).forEach(function (id) { (coverage[id] = coverage[id] || []).push(t); });
    });
    var unowned = Object.keys(coverage).some(function (id) {
      return coverage[id].length >= 2 && !coverage[id].some(function (t) { return t.unique; });
    });
    if (unowned) {
      total += SCORE.unowned_overlap || -6;
      factors.push({ id: "unowned_overlap", label: "A shared use case has no unique-owner flag", points: SCORE.unowned_overlap || -6 });
    }
    var weeklyUnique = 0;
    Object.keys(coverage).forEach(function (id) {
      if (coverage[id].filter(function (t) { return t.weekly; }).length === 1) weeklyUnique += 1;
    });
    if (weeklyUnique) {
      var wp = Math.min((SCORE.weekly_unique_each || 4) * weeklyUnique, SCORE.weekly_unique_cap || 16);
      total += wp;
      factors.push({ id: "weekly_unique", label: weeklyUnique + " use case" + (weeklyUnique === 1 ? "" : "s") + " covered by exactly one weekly tool", points: wp });
    }
    if (tools.length && freeCount * 2 >= tools.length) {
      total += SCORE.free_first || 6;
      factors.push({ id: "free_first", label: "At least half of the stack is user-declared free", points: SCORE.free_first || 6 });
    }
    if (tools.length && known === tools.length) {
      total += SCORE.spend_complete || 4;
      factors.push({ id: "spend_complete", label: "Every tool has known spend (including free = $0)", points: SCORE.spend_complete || 4 });
    }
    var clamped = Math.max(0, Math.min(100, total));
    if (clamped !== total) factors.push({ id: "clamp", label: "Clamped to 0–100", points: clamped - total });
    return {
      score: Math.round(clamped),
      raw: total,
      factors: factors,
      disclaimer: "This is a personal Stack Efficiency Score from your current inputs. It is not a financial-performance rating, ROI claim, or peer ranking."
    };
  }
  function badges(tools, score) {
    var unusedPaid = tools.some(function (t) {
      var value = monthlySpend(t) || 0;
      return value > 0 && !t.weekly && !t.unique;
    });
    var pairs = overlapPairs(tools);
    var coverage = {};
    tools.forEach(function (t) {
      normalizeUse(t.use_cases).forEach(function (id) { (coverage[id] = coverage[id] || []).push(t); });
    });
    var uniqueOwned = Object.keys(coverage).every(function (id) {
      return coverage[id].length < 2 || coverage[id].some(function (t) { return t.unique; });
    });
    var freeCount = tools.filter(function (t) { return t.spend_kind === "free"; }).length;
    var known = tools.filter(function (t) { return monthlySpend(t) != null; }).length;
    var out = [];
    if (tools.length && tools.length <= 4 && !unusedPaid && score.score >= 70) out.push({ id: "lean", label: "Lean Stack", why: "Four or fewer tools, no unused paid seats, score 70+." });
    if (tools.length && (!pairs.length || uniqueOwned)) out.push({ id: "overlap", label: "Overlap Resolver", why: "No unresolved overlapping use cases." });
    if (tools.length && (freeCount === tools.length || (freeCount >= 1 && known === tools.length && tools.every(function (t) { return (monthlySpend(t) || 0) === 0; })))) {
      out.push({ id: "free", label: "Free-First", why: "Every selected tool is user-declared free or $0 entered spend." });
    }
    var ready = tools.length && known === tools.length && tools.every(function (t) { return t.weekly || t.unique; });
    if (ready) out.push({ id: "renewal", label: "Renewal Ready", why: "Spend is known and every tool is weekly or uniquely required." });
    return out;
  }
  function evaluate(tools) {
    var recs = tools.map(function (t) {
      var rec = recommendTool(t, tools);
      return { slug: t.slug, name: t.name, action: rec.action, why: rec.why };
    });
    var scored = scoreStack(tools);
    return { cost: currentCost(tools), savings: savings(tools, recs), score: scored, badges: badges(tools, scored), clusters: overlapClusters(tools), recommendations: recs };
  }
  function b64urlEncode(str) {
    var b64 = btoa(unescape(encodeURIComponent(str)));
    return b64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
  }
  function b64urlDecode(str) {
    var pad = str + "===".slice((str.length + 3) % 4);
    return decodeURIComponent(escape(atob(pad.replace(/-/g, "+").replace(/_/g, "/"))));
  }
  function encodeFragment(tools, includeSpend) {
    var payload = { v: 1, p: includeSpend ? 1 : 0, t: tools.slice(0, MAX_TOOLS).map(function (t) {
      var row = { s: t.slug, k: t.spend_kind || "unknown", w: t.weekly ? 1 : 0, u: t.unique ? 1 : 0, c: normalizeUse(t.use_cases) };
      if (String(t.slug).indexOf("c:") === 0) row.n = sanitizeName(t.name);
      if (includeSpend) {
        if (t.amount != null) row.a = t.amount;
        if (t.spend_kind === "seats") row.q = t.seats || 1;
      }
      return row;
    }) };
    var fragment = PREFIX + b64urlEncode(JSON.stringify(payload));
    if (fragment.length > MAX_FRAG) throw new Error("share fragment exceeds length limit");
    return fragment;
  }
  function decodeFragment(fragment) {
    var text = String(fragment || "").replace(/^#/, "");
    if (text.indexOf(PREFIX) !== 0) return { ok: false, error: "unsupported or missing fragment", tools: [], include_spend: false };
    if (text.length > MAX_FRAG) return { ok: false, error: "fragment too long", tools: [], include_spend: false };
    try {
      var payload = JSON.parse(b64urlDecode(text.slice(PREFIX.length)));
      if (!payload || payload.v !== 1 || !Array.isArray(payload.t)) throw new Error("bad");
      var includeSpend = !!payload.p;
      var tools = [];
      payload.t.slice(0, MAX_TOOLS).forEach(function (row) {
        if (!row || !validSlug(row.s)) return;
        var rec = BY_SLUG[row.s] || {};
        var kind = row.k;
        if ((RULES.spend_kinds || []).indexOf(kind) === -1) kind = "unknown";
        if (!includeSpend) kind = kind === "free" ? "free" : "unknown";
        tools.push({
          slug: row.s,
          name: sanitizeName(row.n || rec.name || row.s),
          spend_kind: kind,
          amount: includeSpend ? finiteAmount(row.a) : null,
          seats: includeSpend ? Math.max(1, Math.min(MAX_SEATS, parseInt(row.q, 10) || 1)) : 1,
          weekly: !!row.w,
          unique: !!row.u,
          use_cases: normalizeUse(row.c),
          capabilities_known: !!rec.capabilities_known,
          price_confidence: rec.price_confidence || (String(row.s).indexOf("c:") === 0 ? "missing" : "official_summary")
        });
      });
      return { ok: true, error: null, tools: tools, include_spend: includeSpend };
    } catch (err) {
      return { ok: false, error: "malformed fragment", tools: [], include_spend: false };
    }
  }

  var Engine = {
    monthlySpend: monthlySpend,
    evaluate: evaluate,
    encodeFragment: encodeFragment,
    decodeFragment: decodeFragment,
    sanitizeName: sanitizeName,
    overlapPairs: overlapPairs
  };
  root.StackAuditEngine = Engine;
  if (typeof module !== "undefined" && module.exports) module.exports = Engine;
  if (typeof document === "undefined") return;

  var state = { step: 1, selected: [], includeSpend: false, started: false };
  var els = {
    step1: document.getElementById("sa-step-1"),
    step2: document.getElementById("sa-step-2"),
    results: document.getElementById("sa-results"),
    search: document.getElementById("sa-search"),
    grid: document.getElementById("sa-tool-grid"),
    chips: document.getElementById("sa-chips"),
    customName: document.getElementById("sa-custom-name"),
    addCustom: document.getElementById("sa-add-custom"),
    cards: document.getElementById("sa-config-cards"),
    error: document.getElementById("sa-error"),
    live: document.getElementById("sa-live")
  };

  function track(name) {
    try {
      if (typeof plausible === "function") plausible("stack_audit_" + name);
    } catch (err) {}
  }
  function markStarted() {
    if (state.started) return;
    state.started = true;
    track("started");
  }
  function persistSession() {
    try { sessionStorage.setItem(SESSION_KEY, JSON.stringify({ selected: state.selected, includeSpend: state.includeSpend })); } catch (err) {}
  }
  function loadSession() {
    try {
      var raw = sessionStorage.getItem(SESSION_KEY);
      if (!raw) return;
      var parsed = JSON.parse(raw);
      if (parsed && Array.isArray(parsed.selected)) state.selected = parsed.selected.filter(function (t) { return t && validSlug(t.slug); }).slice(0, MAX_TOOLS);
      if (parsed && parsed.includeSpend) state.includeSpend = true;
    } catch (err) {}
  }
  function selectedSlugs() { return state.selected.map(function (t) { return t.slug; }); }
  function upsertSelected(tool) {
    var idx = state.selected.findIndex(function (t) { return t.slug === tool.slug; });
    if (idx === -1) {
      if (state.selected.length >= MAX_TOOLS) return showError("You can audit up to " + MAX_TOOLS + " tools.");
      var rec = BY_SLUG[tool.slug] || {};
      state.selected.push({
        slug: tool.slug,
        name: tool.name || rec.name || tool.slug,
        spend_kind: "unknown",
        amount: null,
        seats: 1,
        weekly: false,
        unique: false,
        use_cases: normalizeUse(rec.suggested_use_cases || []),
        capabilities_known: !!rec.capabilities_known,
        price_confidence: rec.price_confidence || "missing"
      });
    }
    persistSession();
  }
  function removeSelected(slug) {
    state.selected = state.selected.filter(function (t) { return t.slug !== slug; });
    persistSession();
  }
  function showError(msg) {
    if (els.error) els.error.textContent = msg || "";
  }
  function announce(msg) {
    if (els.live) els.live.textContent = msg;
  }
  function setStep(n) {
    state.step = n;
    if (els.step1) els.step1.hidden = n !== 1;
    if (els.step2) els.step2.hidden = n !== 2;
    if (els.results) els.results.hidden = n !== 3;
    document.querySelectorAll(".sa-progress-step").forEach(function (el) {
      var step = Number(el.getAttribute("data-step"));
      if (step === n) el.setAttribute("aria-current", "step");
      else el.removeAttribute("aria-current");
    });
    var focusTarget = n === 1 ? els.search : n === 2 ? document.getElementById("sa-config-heading") : document.getElementById("sa-results-heading");
    if (focusTarget) focusTarget.focus();
  }
  function renderGrid() {
    if (!els.grid) return;
    var q = (els.search && els.search.value || "").toLowerCase().trim();
    var picks = TOOLS.filter(function (t) {
      if (!q) return true;
      return (t.name + " " + t.category + " " + t.slug).toLowerCase().indexOf(q) !== -1;
    });
    els.grid.innerHTML = picks.map(function (t) {
      var checked = selectedSlugs().indexOf(t.slug) !== -1 ? " checked" : "";
      return '<label class="sa-pick"><input type="checkbox" value="' + esc(t.slug) + '"' + checked + '><span><strong>' + esc(t.name) + '</strong><small>' + esc(t.category) + (t.price_label ? " · " + esc(t.price_label) : "") + '</small></span></label>';
    }).join("") || '<p class="sa-note">No directory tools match that search. Add a custom tool below.</p>';
  }
  function renderChips() {
    if (!els.chips) return;
    els.chips.innerHTML = state.selected.map(function (t) {
      return '<span class="sa-chip">' + esc(t.name) + ' <button type="button" data-remove="' + esc(t.slug) + '" aria-label="Remove ' + esc(t.name) + '">×</button></span>';
    }).join("");
  }
  function spendFields(t) {
    var kind = t.spend_kind || "unknown";
    var needsAmount = ["monthly", "annual", "seats", "usage", "custom", "promo"].indexOf(kind) !== -1;
    var html = '<div class="sa-field"><span>Spend</span><div class="sa-inline">';
    [["monthly", "Monthly $"], ["annual", "Annual $"], ["seats", "Per-seat $ × seats"], ["usage", "Usage / metered"], ["custom", "Custom amount"], ["promo", "Promotional price"], ["free", "Free (I pay $0)"], ["unknown", "Unknown"]].forEach(function (opt) {
      html += '<label><input type="radio" name="spend-' + esc(t.slug) + '" value="' + opt[0] + '"' + (kind === opt[0] ? " checked" : "") + '> ' + opt[1] + '</label>';
    });
    html += "</div></div>";
    if (needsAmount) {
      html += '<label class="sa-field">Amount (USD)<input data-amount="' + esc(t.slug) + '" type="number" min="0" max="' + MAX_AMT + '" step="0.01" value="' + (t.amount == null ? "" : esc(t.amount)) + '"></label>';
    }
    if (kind === "seats") {
      html += '<label class="sa-field">Seats<input data-seats="' + esc(t.slug) + '" type="number" min="1" max="' + MAX_SEATS + '" value="' + esc(t.seats || 1) + '"></label>';
    }
    if (kind === "unknown" || (kind === "usage" && t.amount == null)) {
      html += '<p class="sa-note">Unknown spend stays unknown. This page will not guess a dollar amount from “Free + paid” labels.</p>';
    }
    if (kind === "promo") html += '<p class="sa-note">Enter what you actually pay on the promo — not a guessed list price. Promo rates can rise later.</p>';
    return html;
  }
  function renderConfig() {
    if (!els.cards) return;
    els.cards.innerHTML = state.selected.map(function (t) {
      var rec = BY_SLUG[t.slug] || {};
      var uses = RULES.use_cases.map(function (u) {
        var checked = (t.use_cases || []).indexOf(u.id) !== -1 ? " checked" : "";
        return '<label><input type="checkbox" data-use="' + esc(t.slug) + '" value="' + esc(u.id) + '"' + checked + '> ' + esc(u.label) + "</label>";
      }).join("");
      var official = rec.pricing_summary ? '<p class="sa-note"><strong>Official pricing note</strong> (' + esc(rec.pricing_checked_date || "undated") + '): ' + esc(rec.pricing_summary.slice(0, 280)) + (rec.pricing_url ? ' <a href="' + esc(rec.pricing_url) + '" target="_blank" rel="noopener">Source</a>' : "") + "</p>" : '<p class="sa-note">No official pricing summary is on file. Recommendation defaults toward Review.</p>';
      return '<article class="score-card sa-tool-card"><h3>' + esc(t.name) + "</h3>" + spendFields(t) +
        '<fieldset class="sa-field"><legend>Primary use cases (up to 5)</legend><div class="sa-use-cases">' + uses + "</div></fieldset>" +
        '<div class="sa-inline"><label><input type="checkbox" data-weekly="' + esc(t.slug) + '"' + (t.weekly ? " checked" : "") + "> Used weekly</label>" +
        '<label><input type="checkbox" data-unique="' + esc(t.slug) + '"' + (t.unique ? " checked" : "") + "> Unique must-keep workflow</label></div>" + official + "</article>";
    }).join("");
  }
  function money(n) { return "$" + (Math.round(n * 100) / 100).toFixed(2); }
  function actionClass(action) {
    return { Keep: "sa-keep", Cut: "sa-cut", Replace: "sa-replace", Review: "sa-review", "Trial first": "sa-trial" }[action] || "sa-review";
  }
  function renderResults() {
    var result = evaluate(state.selected);
    var costNote = result.cost.unknown_count ? result.cost.unknown_count + " tool" + (result.cost.unknown_count === 1 ? "" : "s") + " have unknown spend and are excluded from the dollar total." : "Every selected tool has known spend.";
    var badgeHtml = result.badges.length ? result.badges.map(function (b) { return '<span class="sa-badge" title="' + esc(b.why) + '">' + esc(b.label) + "</span>"; }).join("") : '<p class="sa-note">No personal badges from this input set.</p>';
    var clusterHtml = result.clusters.length ? result.clusters.map(function (c) {
      return '<article class="score-card"><span>Overlap cluster</span><h3>' + esc(c.names.join(" · ")) + "</h3><p>Shared use cases: " + esc(c.shared.map(labelOf).join(", ") || "none named") + ".</p>" + (c.uncertain ? "<p class=\"sa-note\">Uncertainty: at least one tool is missing catalog capability data, so this overlap is based only on the use cases you selected.</p>" : "<p class=\"sa-note\">Overlap is based on normalized shared use cases, not directory category alone.</p>") + "</article>";
    }).join("") : '<p class="sa-note">No pairwise use-case overlap detected in this selection.</p>';
    var recHtml = result.recommendations.map(function (rec) {
      return '<article class="score-card sa-rec"><span class="sa-rec-action ' + actionClass(rec.action) + '">' + esc(rec.action) + "</span><div><strong>" + esc(rec.name) + "</strong><p>" + esc(rec.why) + "</p></div></article>";
    }).join("");
    var factorHtml = result.score.factors.map(function (f) {
      var sign = f.points > 0 ? "+" : "";
      return "<li>" + esc(f.label) + ": <strong>" + sign + f.points + "</strong></li>";
    }).join("");
    document.getElementById("sa-result-body").innerHTML =
      '<div class="sa-metrics"><div class="sa-metric"><span>Current monthly cost</span><strong>' + money(result.cost.monthly) + '</strong><p class="sa-note">' + esc(costNote) + '</p></div>' +
      '<div class="sa-metric"><span>Conservative monthly savings</span><strong>' + money(result.savings.monthly) + '</strong><p class="sa-note">Annual: ' + money(result.savings.annual) + '. Only Cut tools with entered spend. Unknown spend is not guessed.</p></div>' +
      '<div class="sa-metric"><span>Stack Efficiency Score</span><strong>' + result.score.score + '</strong><p class="sa-note">' + esc(result.score.disclaimer) + "</p></div></div>" +
      '<section class="score-card"><span>Score factors</span><h3>Exactly what changed the score</h3><ol class="sa-factors">' + factorHtml + "</ol></section>" +
      '<section class="score-card"><span>Personal badges</span><h3>From this audit only</h3><div class="sa-badges">' + badgeHtml + '</div><p class="sa-note">No community totals or rankings.</p></section>' +
      "<h3>Overlap</h3>" + clusterHtml + "<h3>Keep / Cut / Replace / Review</h3>" + recHtml;
    announce("Audit complete. Score " + result.score.score + ".");
  }
  function shareUrl(includeSpend) {
    var url = new URL(location.href);
    url.hash = encodeFragment(state.selected, includeSpend);
    return url.toString();
  }
  function exportText() {
    var result = evaluate(state.selected);
    var lines = ["AIToolsEssentials Stack Audit", result.score.disclaimer, "", "Monthly cost (known only): " + result.cost.monthly, "Conservative monthly savings: " + result.savings.monthly, "Score: " + result.score.score, ""];
    result.score.factors.forEach(function (f) { lines.push(f.label + ": " + f.points); });
    lines.push("", "Recommendations:");
    result.recommendations.forEach(function (r) { lines.push("- " + r.name + " · " + r.action + " — " + r.why); });
    return lines.join("\n");
  }
  function exportJSON() {
    return JSON.stringify({ generated_by: "aitoolsessentials-stack-audit", result: evaluate(state.selected), tools: state.selected.map(function (t) {
      return { slug: t.slug, name: t.name, spend_kind: t.spend_kind, amount: t.amount, seats: t.seats, weekly: t.weekly, unique: t.unique, use_cases: t.use_cases };
    }) }, null, 2);
  }
  function exportCSV() {
    var result = evaluate(state.selected);
    var rows = [["name", "slug", "action", "why", "spend_kind", "monthly_spend", "weekly", "unique", "use_cases"]];
    result.recommendations.forEach(function (rec) {
      var t = state.selected.filter(function (x) { return x.slug === rec.slug; })[0] || {};
      var spend = monthlySpend(t);
      rows.push([rec.name, rec.slug, rec.action, rec.why, t.spend_kind || "", spend == null ? "" : spend, t.weekly ? "yes" : "no", t.unique ? "yes" : "no", (t.use_cases || []).join("|")]);
    });
    return rows.map(function (r) { return r.map(function (c) { return '"' + String(c).replace(/"/g, '""') + '"'; }).join(","); }).join("\n");
  }
  function download(filename, text, type) {
    var blob = new Blob([text], { type: type || "text/plain;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 800);
    track("export");
  }
  function bind() {
    if (els.search) els.search.addEventListener("input", renderGrid);
    if (els.grid) els.grid.addEventListener("change", function (e) {
      var input = e.target.closest("input[type=checkbox]");
      if (!input) return;
      markStarted();
      if (input.checked) upsertSelected({ slug: input.value });
      else removeSelected(input.value);
      renderGrid();
      renderChips();
    });
    if (els.chips) els.chips.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-remove]");
      if (!btn) return;
      removeSelected(btn.getAttribute("data-remove"));
      renderGrid();
      renderChips();
    });
    if (els.addCustom) els.addCustom.addEventListener("click", function () {
      var name = sanitizeName(els.customName && els.customName.value);
      if (!name) return showError("Enter a custom tool name.");
      markStarted();
      upsertSelected({ slug: customSlug(name), name: name });
      if (els.customName) els.customName.value = "";
      showError("");
      renderGrid();
      renderChips();
    });
    document.getElementById("sa-to-step-2").addEventListener("click", function () {
      if (!state.selected.length) return showError("Select at least one tool.");
      showError("");
      renderConfig();
      setStep(2);
    });
    document.getElementById("sa-back-1").addEventListener("click", function () { setStep(1); });
    if (els.cards) {
      els.cards.addEventListener("change", function (e) {
        var t = e.target;
        var slug = (t.name || t.getAttribute("data-use") || t.getAttribute("data-weekly") || t.getAttribute("data-unique") || t.getAttribute("data-amount") || t.getAttribute("data-seats") || "").replace(/^spend-/, "");
        var item = state.selected.filter(function (x) { return x.slug === slug; })[0];
        if (!item) return;
        if (t.name && t.name.indexOf("spend-") === 0) item.spend_kind = t.value;
        if (t.hasAttribute("data-amount")) item.amount = finiteAmount(t.value);
        if (t.hasAttribute("data-seats")) item.seats = Math.max(1, Math.min(MAX_SEATS, parseInt(t.value, 10) || 1));
        if (t.hasAttribute("data-weekly")) item.weekly = t.checked;
        if (t.hasAttribute("data-unique")) item.unique = t.checked;
        if (t.hasAttribute("data-use")) {
          var uses = item.use_cases.slice();
          if (t.checked) {
            if (uses.indexOf(t.value) === -1) uses.push(t.value);
            if (uses.length > MAX_USE) {
              t.checked = false;
              uses = uses.slice(0, MAX_USE);
              showError("Up to " + MAX_USE + " use cases per tool.");
            }
          } else uses = uses.filter(function (id) { return id !== t.value; });
          item.use_cases = uses;
        }
        persistSession();
        if (t.name && t.name.indexOf("spend-") === 0) renderConfig();
      });
    }
    document.getElementById("sa-run").addEventListener("click", function () {
      renderResults();
      setStep(3);
      persistSession();
      history.replaceState(null, "", "#" + encodeFragment(state.selected, false));
      track("completed");
    });
    document.getElementById("sa-back-2").addEventListener("click", function () { setStep(2); renderConfig(); });
    document.getElementById("sa-restart").addEventListener("click", function () {
      state.selected = [];
      persistSession();
      renderGrid();
      renderChips();
      setStep(1);
    });
    document.getElementById("sa-copy-link").addEventListener("click", function () {
      var url = shareUrl(document.getElementById("sa-share-spend").checked);
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () {
        announce("Private-by-default share link copied.");
      }, function () { window.prompt("Copy this link:", url); });
    });
    document.getElementById("sa-share-spend").addEventListener("change", function (e) {
      state.includeSpend = e.target.checked;
      persistSession();
    });
    document.getElementById("sa-print").addEventListener("click", function () { track("export"); window.print(); });
    document.getElementById("sa-json").addEventListener("click", function () { download("stack-audit.json", exportJSON(), "application/json"); });
    document.getElementById("sa-csv").addEventListener("click", function () { download("stack-audit.csv", exportCSV(), "text/csv"); });
    document.getElementById("sa-text").addEventListener("click", function () { download("stack-audit.txt", exportText(), "text/plain"); });
    document.getElementById("sa-save-local").addEventListener("click", function () {
      try {
        localStorage.setItem(LOCAL_KEY, JSON.stringify({ selected: state.selected, savedAt: new Date().toISOString() }));
        announce("Saved on this device. Nothing was sent to a server.");
      } catch (err) { showError("Could not save on this device."); }
    });
    document.getElementById("sa-load-local").addEventListener("click", function () {
      try {
        var raw = localStorage.getItem(LOCAL_KEY);
        if (!raw) return showError("No local save found.");
        var parsed = JSON.parse(raw);
        state.selected = (parsed.selected || []).slice(0, MAX_TOOLS);
        persistSession();
        renderGrid();
        renderChips();
        renderConfig();
        announce("Loaded the local save.");
      } catch (err) { showError("Local save could not be read."); }
    });
    document.querySelectorAll("[data-sa-cta]").forEach(function (el) {
      el.addEventListener("click", function () { track("cta"); });
    });
  }

  loadSession();
  if (location.hash) {
    var decoded = decodeFragment(location.hash);
    if (decoded.ok && decoded.tools.length) {
      state.selected = decoded.tools;
      state.includeSpend = decoded.include_spend;
      persistSession();
    } else if (location.hash.length > 1) {
      showError("That share link could not be read. Start a new audit — nothing was stored on a server.");
    }
  }
  var shareBox = document.getElementById("sa-share-spend");
  if (shareBox) shareBox.checked = !!state.includeSpend;
  bind();
  renderGrid();
  renderChips();
  if (state.selected.length && location.hash) {
    renderConfig();
    renderResults();
    setStep(3);
  } else {
    setStep(1);
  }
})(typeof window !== "undefined" ? window : globalThis);
