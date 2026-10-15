/* Full search page for AIToolsEssentials.
 *
 * Ranking, tokenizing, matching and index loading live in js/search-core.js, shared with the
 * predictive header box. This file is only the page UI: filters, result list, keyboard navigation
 * and URL sync. Two search surfaces that ordered results differently would be a bug — a reader who
 * ran the same query in the header and on this page would get two different answers and neither
 * would look wrong — so the engine lives in exactly one place.
 *
 * It replaced a 60-line inline script that filtered with a single `indexOf` over a concatenated
 * blob, returned results in file order, and — with an empty query — printed all 438 entries, so
 * the first thing a reader saw was the entire site listing.
 *
 * Requires js/search-core.js (provides window.AITSearch).
 */
(function () {
  'use strict';

  var S = window.AITSearch;
  var input = document.getElementById('sr-input');
  var list = document.getElementById('sr-results');
  var countEl = document.getElementById('sr-count');
  var filtersEl = document.getElementById('sr-filters');
  var clearBtn = document.getElementById('sr-clear');
  if (!S || !input || !list) return;

  var MAX_RESULTS = 60;
  var DEBOUNCE_MS = 90;

  var index = [];
  var ready = false;
  var activeFilter = 'all';
  var active = -1;
  var debounceTimer = null;

  function passesFilter(e) {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'other') return S.FILTER_ORDER.indexOf(e.type) === -1;
    return e.type === activeFilter;
  }

  function compute() {
    var q = input.value.trim();
    var pool = index.filter(passesFilter);
    if (!S.tokens(q).length) {
      return { hits: [], total: pool.length, q: q, toks: [], empty: true };
    }
    var r = S.rank(pool, q, MAX_RESULTS);
    return { hits: r.hits, total: r.total, q: q, toks: r.toks, empty: false };
  }

  function entryHTML(e, toks) {
    var type = S.TYPE_LABELS[e.type] || 'Page';
    var meta = type + (e.category ? ' · ' + S.esc(e.category) : '');
    var bits = [];
    if (e.rating) bits.push(S.esc(String(e.rating)) + '/5 editorial');
    if (e.price) bits.push(S.esc(String(e.price)).slice(0, 40));
    return '<a class="sr-result" role="option" href="' + S.esc(e.url) + '">' +
             '<span class="sr-type">' + meta + '</span>' +
             '<span class="sr-name">' + S.highlight(S.esc(e.name), toks) + '</span>' +
             (e.desc ? '<span class="sr-desc">' + S.highlight(S.esc(e.desc), toks) + '</span>' : '') +
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
               '<span class="sr-name">' + S.esc(p.label) + '</span>' +
               '<span class="sr-desc">' + S.esc(p.note) + '</span>' +
             '</a>';
    }).join('');
  }

  function emptyHTML(q) {
    return '<div class="sr-empty"><h3>No matches for “' + S.esc(q) + '”</h3>' +
      '<p>Try a shorter term, or browse <a href="/tools/">all tools</a> and ' +
      '<a href="/categories/">categories</a>.</p></div>';
  }

  function render() {
    var r = compute();
    active = -1;
    input.removeAttribute('aria-activedescendant');
    input.setAttribute('aria-expanded', 'true');

    if (r.empty) {
      countEl.textContent = index.length
        ? index.length + ' pages indexed — start typing, or jump straight in:'
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
    if (r.total > r.hits.length) label += ' — showing the top ' + r.hits.length;
    countEl.textContent = label;

    list.innerHTML = r.hits.map(function (e, i) {
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
    if (e.key === 'ArrowDown') { e.preventDefault(); if (ready) move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); if (ready) move(-1); }
    else if (e.key === 'Enter') {
      var opts = list.querySelectorAll('.sr-result');
      if (active >= 0 && opts[active]) { e.preventDefault(); opts[active].click(); }
    } else if (e.key === 'Escape') {
      if (input.value) { input.value = ''; syncURL(); render(); }
      else { input.blur(); }
    }
  });

  input.addEventListener('input', function () { syncURL(); scheduleRender(); });
  input.addEventListener('search', function () { scheduleRender(); });

  if (clearBtn) clearBtn.addEventListener('click', function () {
    input.value = ''; syncURL(); render(); input.focus();
  });

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

  function buildFilters(total) {
    if (!filtersEl) return;
    var counts = {};
    index.forEach(function (e) { counts[e.type] = (counts[e.type] || 0) + 1; });
    var html = '<button class="sr-filter active" type="button" data-filter="all" aria-pressed="true">' +
               'All <span class="sr-n">' + total + '</span></button>';
    S.FILTER_ORDER.forEach(function (t) {
      if (!counts[t]) return;
      html += '<button class="sr-filter" type="button" data-filter="' + t + '" aria-pressed="false">' +
              (S.TYPE_LABELS[t] || t) + 's <span class="sr-n">' + counts[t] + '</span></button>';
    });
    var other = Object.keys(counts).reduce(function (n, t) {
      return n + (S.FILTER_ORDER.indexOf(t) === -1 ? counts[t] : 0);
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

  S.loadIndex().then(function (entries) {
    index = entries;
    ready = true;
    buildFilters(index.length);
    render();
  }).catch(function () {
    countEl.innerHTML = 'Search is unavailable right now. ' +
      '<a href="/tools/">Browse the tool directory</a> instead.';
  });
})();
