/* Shared search engine for AIToolsEssentials.
 *
 * One ranking implementation, used by both the /search/ page and the predictive header box.
 * Two search surfaces that order results differently is a bug: a reader who types the same
 * query in the header and on the page would see two different answers, and neither would look
 * wrong. So scoring, tokenizing and index loading live here exactly once.
 *
 * Exposed as window.AITSearch. No dependencies.
 */
(function (root) {
  'use strict';

  var INDEX_URL = '/data/search_index.json';

  var TYPE_LABELS = {
    tool: 'Tool', comparison: 'Comparison', guide: 'Guide', utility: 'Tool',
    reference: 'Reference', category: 'Category', service: 'Service', premium: 'Premium',
    page: 'Page'
  };

  /* Filters are offered in this order; any type not listed folds into "Other". */
  var FILTER_ORDER = ['tool', 'guide', 'comparison', 'reference', 'utility', 'category'];

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  /* Lowercase, strip accents, collapse punctuation to spaces, so "bolt.new" is findable as
     both "bolt.new" and "bolt new". */
  function norm(s) {
    return String(s == null ? '' : s)
      .toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[_./]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function tokens(q) {
    return norm(q).split(' ').filter(function (t) { return t.length > 0; });
  }

  /* True when `needle` appears in `hay` on a word boundary. Avoids building a RegExp per token
     per entry, which is the obvious way to write this and the slow way to run it. */
  function wordHit(hay, needle) {
    var at = hay.indexOf(needle);
    while (at !== -1) {
      var before = at === 0 ? '' : hay.charAt(at - 1);
      if (before === '' || before === ' ') return true;
      at = hay.indexOf(needle, at + 1);
    }
    return false;
  }

  /* Wrap every token occurrence in <mark>. Operates on the already-escaped string so a query
     containing "<" cannot inject markup. */
  function highlight(escaped, toks) {
    if (!toks || !toks.length) return escaped;
    var out = escaped;
    toks.forEach(function (t) {
      if (t.length < 2) return;
      var lower = out.toLowerCase();
      var from = 0;
      while (from < out.length) {
        var at = lower.indexOf(t, from);
        if (at === -1) break;
        /* Skip matches inside an inserted tag so we never nest <mark> or split an entity. */
        var insideTag = out.lastIndexOf('<', at) > out.lastIndexOf('>', at);
        if (insideTag) { from = at + t.length; continue; }
        out = out.slice(0, at) + '<mark>' + out.slice(at, at + t.length) + '</mark>' + out.slice(at + t.length);
        lower = out.toLowerCase();
        from = at + t.length + 13;
      }
    });
    return out;
  }

  /* Higher is better; -1 means "does not match". Every token must appear somewhere (AND
     semantics), so extra words narrow the result set instead of widening it. */
  function scoreEntry(e, toks, phrase) {
    var name = norm(e.name);
    var cat = norm(e.category || '');
    var kws = norm((e.keywords || []).join(' '));
    var slug = norm(e.slug || '');
    var desc = norm(e.desc || '');
    var all = name + ' ' + cat + ' ' + kws + ' ' + slug + ' ' + desc;

    for (var i = 0; i < toks.length; i++) {
      if (all.indexOf(toks[i]) === -1) return -1;
    }

    var s = 0;
    if (name === phrase) s += 1200;
    else if (name.indexOf(phrase) === 0) s += 480;
    else if (name.indexOf(phrase) !== -1) s += 260;
    if (slug === phrase) s += 300;

    toks.forEach(function (t) {
      if (name === t) s += 200;
      else if (name.indexOf(t) === 0) s += 110;
      else if (wordHit(name, t)) s += 70;
      else if (name.indexOf(t) !== -1) s += 45;

      if (wordHit(cat, t)) s += 34;
      if (wordHit(kws, t)) s += 24;
      if (wordHit(slug, t)) s += 18;
      if (desc.indexOf(t) !== -1) s += 8;
    });

    /* A tool is the most common thing a reader hunts for; nudge it above a guide at equal
       relevance, never above it regardless of relevance. */
    if (e.type === 'tool') s += 6;
    return s;
  }

  /* Rank a pool against a query. Returns {hits, total, toks, phrase}. */
  function rank(pool, q, limit) {
    var toks = tokens(q);
    var phrase = norm(q);
    if (!toks.length) return { hits: [], total: 0, toks: toks, phrase: phrase };
    var scored = [];
    for (var i = 0; i < pool.length; i++) {
      var sc = scoreEntry(pool[i], toks, phrase);
      if (sc >= 0) scored.push({ e: pool[i], s: sc });
    }
    scored.sort(function (a, b) {
      if (b.s !== a.s) return b.s - a.s;
      return a.e.name.localeCompare(b.e.name);
    });
    var hits = scored.map(function (x) { return x.e; });
    return { hits: limit ? hits.slice(0, limit) : hits, total: scored.length, toks: toks, phrase: phrase };
  }

  /* ---------------------------------------------------------------- near-miss suggestions */

  /* Jaro-Winkler. Chosen after bigram-Dice and edit-distance both failed on the real case: "halo"
     for "HOL" scored 0.00 on Dice (no shared bigram: ha/al/lo vs ho/ol) and only 0.50 on edit
     distance, while the unrelated word "local" scored 0.57 — so the correct answer ranked below
     noise. Jaro-Winkler scores "halo"/"hol" at 0.75 and "halo"/"local" at 0.00, because it rewards
     a shared prefix and tolerates an inserted letter, which is what typos of short names are. */
  function jaro(a, b) {
    if (a === b) return 1;
    var la = a.length, lb = b.length, i, j;
    if (!la || !lb) return 0;
    var win = Math.max(0, Math.floor(Math.max(la, lb) / 2) - 1);
    var am = [], bm = [], m = 0;
    for (i = 0; i < la; i++) am[i] = false;
    for (j = 0; j < lb; j++) bm[j] = false;
    for (i = 0; i < la; i++) {
      var lo = Math.max(0, i - win), hi = Math.min(lb - 1, i + win);
      for (j = lo; j <= hi; j++) {
        if (bm[j] || a.charAt(i) !== b.charAt(j)) continue;
        am[i] = true; bm[j] = true; m++; break;
      }
    }
    if (!m) return 0;
    var t = 0, k = 0;
    for (i = 0; i < la; i++) {
      if (!am[i]) continue;
      while (!bm[k]) k++;
      if (a.charAt(i) !== b.charAt(k)) t++;
      k++;
    }
    t = t / 2;
    return (m / la + m / lb + (m - t) / m) / 3;
  }

  /* Combined similarity on a 0..1 scale: Jaro-Winkler, which already applies the prefix bonus. */
  function similar(a, b) {
    a = norm(a).replace(/ /g, '');
    b = norm(b).replace(/ /g, '');
    if (!a || !b) return 0;
    if (a === b) return 1;
    var j = jaro(a, b);
    var p = 0, max = Math.min(4, a.length, b.length);
    for (var i = 0; i < max; i++) {
      if (a.charAt(i) === b.charAt(i)) p++; else break;
    }
    return j + p * 0.1 * (1 - j);
  }

  /* Letter-subset match: the shorter string's letters all appear in the longer one, with a length
     difference of at most 2. That is the "one letter inserted or dropped" typo — "halo" for "hol" —
     and it needs its own rule because general similarity does NOT separate it: on the real index
     "handles" scored 0.781 and "health" 0.775 against "halo", both ranking ABOVE the correct "hol"
     at 0.750.

     Returns the number of inserted letters (0 when not a subset match), so the caller can GRADE the
     result rather than flatten every hit to one score. That grading is load-bearing: with a flat
     score, "halo service" tied HOL Registry against an unrelated page matching "service" -> "serve"
     (also a two-letter insertion), and the tie broke alphabetically onto the wrong entry. */
  function subsetTypo(a, b) {
    a = norm(a).replace(/ /g, '');
    b = norm(b).replace(/ /g, '');
    if (!a || !b || a === b) return 0;
    var diff = Math.abs(a.length - b.length);
    if (diff === 0 || diff > 2) return 0;
    var short = a.length <= b.length ? a : b;
    var long = a.length <= b.length ? b : a;
    if (short.length < 3) return 0;
    if (short.charAt(0) !== long.charAt(0) &&
        short.charAt(short.length - 1) !== long.charAt(long.length - 1)) return 0;
    var pool = {}, i;
    for (i = 0; i < long.length; i++) pool[long.charAt(i)] = (pool[long.charAt(i)] || 0) + 1;
    for (i = 0; i < short.length; i++) {
      var ch = short.charAt(i);
      if (!pool[ch]) return 0;
      pool[ch]--;
    }
    return diff;
  }

  /* Score for a subset typo: one inserted letter beats two. Stays above any plausible Jaro-Winkler
     score for unrelated words (which cluster around 0.75-0.78) so a real typo always outranks a
     coincidental letter overlap. */
  function typoScore(inserted) {
    return 0.94 - 0.06 * (inserted - 1);
  }

  /* Every searchable field for an entry, joined — the same set strict scoring matches against. */
  function entryAll(e) {
    return norm([e.name, e.category, (e.keywords || []).join(' '), e.slug, e.desc].join(' '));
  }

  /* Query-side filler words. The index never stores these (the generator strips them), so a query
     made only of them matches nothing and would otherwise trigger the near-miss fallback and
     suggest arbitrary pages — "the" suggested five. Deliberately small and separate from the
     generator's list: this one filters what a READER typed, not what we store. */
  var QUERY_FILLER = {};
  ('the a an and or but if of to in on at by for with from as is are was were be been being am ' +
   'do does did has have had can could will would should may might must not no nor so than that ' +
   'this these those it its they them their there here what which who whom when where why how ' +
   'all any both each few more most other some such only own same too very just about into over ' +
   'after before between under above again further then once during out off up down my your our ' +
   'his her him she he you i we us me')
    .split(' ').forEach(function (w) { QUERY_FILLER[w] = true; });

  /* When a query matches nothing, offer the closest entries rather than a dead end. A reader who
     types "halo" for "HOL Registry" gets a suggestion instead of "no results", which is the
     difference between a search that feels broken and one that feels helpful.

     Only the tokens that match NOTHING are used to rank suggestions. That is the whole trick: for
     "halo service", "service" matches "services" perfectly (Jaro-Winkler 0.975, since one is a
     prefix of the other) and therefore drowned out the actual typo, suggesting eight AI Stack Audit
     pages instead of HOL Registry. But "service" is not why the search failed — "halo" is. Ranking
     on the failing token alone puts the answer first without special-casing anything.

     Matched word-against-word so a two-word query reaches a two-word name, and against the entry's
     name, slug and keywords only — never the description, or a typo would pull back long prose that
     merely shares letters. */
  function suggest(pool, q, limit) {
    var phrase = norm(q);
    if (!phrase) return [];
    var qToks = phrase.split(' ').filter(function (t) { return t.length > 1; });
    /* A query of nothing but filler ("the") has no answer to suggest — return before matching, or
       the fallback invents one out of coincidental letter overlap. */
    var meaningful = qToks.filter(function (t) { return !QUERY_FILLER[t]; });
    if (!meaningful.length) return [];
    var qToks2 = meaningful;

    /* Cache the joined text once: this runs over the whole index on a zero-result query. */
    var texts = pool.map(entryAll);
    var failing = qToks2.filter(function (t) {
      for (var i = 0; i < texts.length; i++) {
        if (texts[i].indexOf(t) !== -1) return false;
      }
      return true;
    });
    if (!failing.length) failing = qToks2;

    var out = [];
    for (var i = 0; i < pool.length; i++) {
      var e = pool[i];
      var cand = [norm(e.name), norm(e.slug || '')];
      (e.keywords || []).forEach(function (k) { cand.push(norm(k)); });
      var words = [];
      cand.forEach(function (c) {
        if (!c) return;
        words.push(c);
        c.split(' ').forEach(function (w) { if (w.length > 1) words.push(w); });
      });
      var best = 0;
      for (var j = 0; j < words.length; j++) {
        for (var k2 = 0; k2 < failing.length; k2++) {
          var s = similar(failing[k2], words[j]);
          var ins = subsetTypo(failing[k2], words[j]);
          if (ins) s = Math.max(s, typoScore(ins));
          if (s > best) best = s;
        }
      }
      if (best >= 0.72) out.push({ e: e, s: best });
    }
    out.sort(function (x, y) {
      if (y.s !== x.s) return y.s - x.s;
      /* On a tie the tool itself is the canonical answer; a comparison that merely mentions it in
         its title should not outrank the page the reader actually wants. */
      var xt = x.e.type === 'tool' ? 0 : 1, yt = y.e.type === 'tool' ? 0 : 1;
      if (xt !== yt) return xt - yt;
      return x.e.name.localeCompare(y.e.name);
    });
    return out.slice(0, limit || 5).map(function (x) { return x.e; });
  }

  /* One fetch per page load, shared by every search surface, and only when something actually
     asks for it. A rejected/empty result is not cached so a later call can retry. */
  var indexPromise = null;
  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(INDEX_URL, { credentials: 'same-origin' })
        .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(function (data) {
          var entries = Array.isArray(data) ? data : (data.entries || []);
          if (!entries.length) throw new Error('empty index');
          return entries;
        })
        .catch(function (err) {
          indexPromise = null;
          throw err;
        });
    }
    return indexPromise;
  }

  root.AITSearch = {
    INDEX_URL: INDEX_URL,
    TYPE_LABELS: TYPE_LABELS,
    FILTER_ORDER: FILTER_ORDER,
    esc: esc,
    norm: norm,
    tokens: tokens,
    wordHit: wordHit,
    highlight: highlight,
    scoreEntry: scoreEntry,
    rank: rank,
    similar: similar,
    suggest: suggest,
    loadIndex: loadIndex
  };
})(window);
