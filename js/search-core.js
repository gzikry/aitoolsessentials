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
    loadIndex: loadIndex
  };
})(window);
