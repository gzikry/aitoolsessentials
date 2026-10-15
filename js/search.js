/* Live site search for AIToolsEssentials.
 *
 * Replaces an inline script that filtered the index with a substring test and dumped every
 * match in file order. Three things were wrong with that and all three are fixed here:
 *
 *  1. NOT LIVE. It re-rendered the whole list on every keystroke and, with an empty query,
 *     printed all 438 entries — so the first thing a reader saw was the entire site listing
 *     rather than a prompt. Here the fetch is warmed in the background, typing is debounced,
 *     and an empty query shows a small set of useful starting points instead of everything.
 *
 *  2. NO RANKING. `indexOf` across a concatenated blob meant "ai" matched everything and the
 *     result order was whatever the file happened to hold. Now every entry is scored: an exact
 *     name beats a name prefix beats a word inside the name beats a category, keyword, slug or
 *     description hit — so typing a tool's name puts that tool first.
 *
 *  3. NO KEYBOARD OR URL SUPPORT. Results are a real listbox: arrows move, Enter opens, Escape
 *     clears, and the query is written to ?q= so a search is shareable, survives reload, and
 *     works as the target of the browser search provider and the schema.org SearchAction.
 *
 * Dependency-free and framework-free, matching the rest of /js.
 */
(function () {
  'use strict';

  var INDEX_URL = '/data/search_index.json';
  var MAX_RESULTS = 60;
  var DEBOUNCE_MS = 110;

  var TYPE_LABELS = {
    tool: 'Tool', comparison: 'Comparison', guide: 'Guide', utility: 'Tool',
    reference: 'Reference', category: 'Category', service: 'Service', premium: 'Premium',
    page: 'Page'
  };
  /* Filters are offered in this order; any type not listed is folded into "Other". */
  var FILTER_ORDER = ['tool', 'guide', 'comparison', 'reference', 'utility', 'category'];

  var input = document.getElementById('sr-input');
  var list = document.getElementById('sr-results');
  var countEl = document.getElementById('sr-count');
  var filtersEl = document.getElementById('sr-filters');
  var clearBtn = document.getElementById('sr-clear');
  if (!input || !list) return;

  var index = [];
  var ready = false;
  var activeFilter = 'all';
  var active = -1;          /* index into the rendered slice */
  var shown = [];
  var debounceTimer = null;

  /* ---------------------------------------------------------------- helpers */

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  /* Lowercase, strip accents, collapse punctuation to spaces. Keeps "bolt.new" findable as
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
    if (!toks.length) return escaped;
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

  /* ---------------------------------------------------------------- scoring */

  function scoreEntry(e, toks, phrase) {
    var name = norm(e.name);
    var cat = norm(e.category || '');
    var kws = norm((e.keywords || []).join(' '));
    var slug = norm(e.slug || '');
    var desc = norm(e.desc || '');
    var all = name + ' ' + cat + ' ' + kws + ' ' + slug + ' ' + desc;

    /* AND semantics: every token must appear somewhere, so extra words narrow the result
       instead of widening it. */
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

    /* A tool is the most common thing a reader is hunting for; nudge it above a guide at equal
       relevance, never above it regardless of relevance. */
    if (e.type === 'tool') s += 6;
    return s;
  }

  /* ---------------------------------------------------------------- rendering */

  function passesFilter(e) {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'other') return FILTER_ORDER.indexOf(e.type) === -1;
    return e.type === activeFilter;
  }

  function compute() {
    var q = input.value.trim();
    var toks = tokens(q);
    var phrase = norm(q);
    var pool = index.filter(passesFilter);

    if (!toks.length) return { hits: pool.slice(0, 8), total: pool.length, q: q, toks: toks, empty: true };

    var scored = [];
    for (var i = 0; i < pool.length; i++) {
      var sc = scoreEntry(pool[i], toks, phrase);
      if (sc >= 0) scored.push({ e: pool[i], s: sc });
    }
    scored.sort(function (a, b) {
      if (b.s !== a.s) return b.s - a.s;
      return a.e.name.localeCompare(b.e.name);
    });
    return {
      hits: scored.slice(0, MAX_RESULTS).map(function (x) { return x.e; }),
      total: scored.length, q: q, toks: toks, empty: false
    };
  }

  function entryHTML(e, toks) {
    var type = TYPE_LABELS[e.type] || 'Page';
    var meta = type + (e.category ? ' · ' + esc(e.category) : '');
    var bits = [];
    if (e.rating) bits.push(esc(String(e.rating)) + '/5 editorial');
    if (e.price) bits.push(esc(String(e.price)).slice(0, 40));
    return '<a class="sr-result" role="option" href="' + esc(e.url) + '">' +
             '<span class="sr-type">' + meta + '</span>' +
             '<span class="sr-name">' + highlight(esc(e.name), toks) + '</span>' +
             (e.desc ? '<span class="sr-desc">' + highlight(esc(e.desc), toks) + '</span>' : '') +
             (bits.length ? '<span class="sr-meta">' + bits.join(' · ') + '</span>' : '') +
           '</a>';
  }

  function startingPoints() {
    /* Shown before anything is typed. Deliberately short: a list of everything is not a result
       set, and printing one is what made the old page feel broken. */
    var picks = [
      { href: '/tools/', label: 'Browse all tools', note: 'Every reviewed tool, by category' },
      { href: '/pricing-watch/', label: 'Pricing Watch', note: 'Dated prices and what changed' },
      { href: '/categories/', label: 'Categories', note: 'Find a tool by job' },
      { href: '/stack-audit.html', label: 'Free Stack Audit', note: 'Score the stack you already pay for' },
      { href: '/articles/', label: 'Guides', note: 'Buying and comparison guides' }
    ];
    return picks.map(function (p) {
      return '<a class="sr-result sr-start" role="option" href="' + p.href + '">' +
               '<span class="sr-type">Start here</span>' +
               '<span class="sr-name">' + esc(p.label) + '</span>' +
               '<span class="sr-desc">' + esc(p.note) + '</span>' +
             '</a>';
    }).join('');
  }

  function emptyHTML(q) {
    return '<div class="sr-empty"><h3>No matches for “' + esc(q) + '”</h3>' +
      '<p>Try a shorter term, or browse <a href="/tools/">all tools</a> and ' +
      '<a href="/categories/">categories</a>.</p></div>';
  }

  function render() {
    var r = compute();
    shown = r.hits;
    active = -1;
    input.removeAttribute('aria-activedescendant');
    input.setAttribute('aria-expanded', 'true');

    if (r.empty) {
      countEl.innerHTML = index.length
        ? esc(index.length + ' pages indexed — start typing, or jump straight in:')
        : 'Loading the index…';
      list.innerHTML = index.length ? startingPoints() : '';
      return;
    }

    if (!r.total) {
      countEl.textContent = 'No results';
      list.innerHTML = emptyHTML(r.q);
      return;
    }

    var label = r.total + ' result' + (r.total === 1 ? '' : 's');
    if (r.total > shown.length) label += ' — showing the top ' + shown.length;
    countEl.textContent = label;

    list.innerHTML = shown.map(function (e, i) {
      return entryHTML(e, r.toks).replace('class="sr-result"', 'class="sr-result" id="sr-opt-' + i + '"');
    }).join('') || emptyHTML(r.q);
  }

  function scheduleRender() {
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(render, DEBOUNCE_MS);
  }

  /* Keep the query in the URL so a search is linkable and survives a reload. replaceState, not
     pushState: typing should not fill the back button with every keystroke. */
  function syncURL() {
    var q = input.value.trim();
    var url = window.location.pathname + (q ? '?q=' + encodeURIComponent(q) : '');
    try { window.history.replaceState(null, '', url); } catch (err) { /* file:// or sandboxed */ }
  }

  /* ---------------------------------------------------------------- keyboard */

  function move(delta) {
    var opts = list.querySelectorAll('.sr-result');
    if (!opts.length) return;
    active = (active + delta + opts.length) % opts.length;
    for (var i = 0; i < opts.length; i++) {
      opts[i].classList.toggle('sr-active', i === active);
      opts[i].setAttribute('aria-selected', i === active ? 'true' : 'false');
    }
    var el = opts[active];
    el.id = 'sr-opt-' + active;
    input.setAttribute('aria-activedescendant', el.id);
    if (el.scrollIntoView) el.scrollIntoView({ block: 'nearest' });
  }

  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); if (!ready) return; move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); if (!ready) return; move(-1); }
    else if (e.key === 'Enter') {
      var opts = list.querySelectorAll('.sr-result');
      if (active >= 0 && opts[active]) { e.preventDefault(); opts[active].click(); }
    } else if (e.key === 'Escape') {
      if (input.value) { input.value = ''; syncURL(); render(); }
      else { input.blur(); }
    } else if (e.key === 'Home' && active >= 0) { e.preventDefault(); active = -1; move(1); }
  });

  input.addEventListener('input', function () { syncURL(); scheduleRender(); });

  if (clearBtn) clearBtn.addEventListener('click', function () {
    input.value = ''; syncURL(); render(); input.focus();
  });

  input.addEventListener('search', function () { scheduleRender(); });

  if (filtersEl) {
    filtersEl.addEventListener('click', function (e) {
      var btn = e.target.closest('.sr-filter');
      if (!btn) return;
      activeFilter = btn.getAttribute('data-filter');
      filtersEl.querySelectorAll('.sr-filter').forEach(function (el) {
        var on = el === btn;
        el.classList.toggle('active', on);
        el.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      render();
    });
  }

  /* ---------------------------------------------------------------- load */

  function load() {
    return fetch(INDEX_URL, { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (data) {
        index = Array.isArray(data) ? data : (data.entries || []);
        ready = true;
        buildFilters(data && data.count ? data.count : index.length);
        render();
      })
      .catch(function () {
        countEl.innerHTML = 'Search is unavailable right now. ' +
          '<a href="/tools/">Browse the tool directory</a> instead.';
      });
  }

  function buildFilters(total) {
    if (!filtersEl) return;
    var counts = {};
    index.forEach(function (e) { counts[e.type] = (counts[e.type] || 0) + 1; });
    var html = '<button class="sr-filter active" type="button" data-filter="all" aria-pressed="true">' +
               'All <span class="sr-n">' + total + '</span></button>';
    FILTER_ORDER.forEach(function (t) {
      if (!counts[t]) return;
      html += '<button class="sr-filter" type="button" data-filter="' + t + '" aria-pressed="false">' +
              (TYPE_LABELS[t] || t) + 's <span class="sr-n">' + counts[t] + '</span></button>';
    });
    var other = Object.keys(counts).reduce(function (n, t) {
      return n + (FILTER_ORDER.indexOf(t) === -1 ? counts[t] : 0);
    }, 0);
    if (other) {
      html += '<button class="sr-filter" type="button" data-filter="other" aria-pressed="false">' +
              'Other <span class="sr-n">' + other + '</span></button>';
    }
    filtersEl.innerHTML = html;
    filtersEl.hidden = false;
  }

  /* Honour ?q= on arrival so the browser search provider, the schema.org SearchAction and any
     shared link all land on an applied query rather than an empty box. */
  var initial = new URLSearchParams(window.location.search).get('q');
  if (initial) input.value = initial;

  /* Start the fetch on load but off the critical path, so the box is typeable either way. */
  if ('requestIdleCallback' in window) window.requestIdleCallback(load, { timeout: 1200 });
  else setTimeout(load, 0);
})();
