/* Tool-directory filter for /tools/.
 *
 * Was: a substring test on `card.innerText`, which matched whatever prose happened to be inside
 * the card ("ai" matched nearly everything) and ignored the query string entirely - so the
 * schema.org SearchAction and the OpenSearch provider both pointed here with ?q= and the page
 * arrived unfiltered. It now reads the card's own data-name / data-category / data-use, ranks
 * by where the match landed, honours ?q= on arrival, and writes the query back to the URL.
 *
 * The cards are already in the DOM, so this filters in place instead of fetching an index.
 */
(function () {
  'use strict';

  var input = document.querySelector('#toolSearch');
  if (!input) return;

  var cards = Array.prototype.slice.call(document.querySelectorAll('.directory-card'));
  var count = document.querySelector('#toolCount');
  var grid = cards.length ? cards[0].parentNode : null;
  var originalOrder = cards.slice();
  var debounce = null;

  function norm(s) {
    return String(s == null ? '' : s)
      .toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[_.\/]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function toks(q) { return norm(q).split(' ').filter(function (t) { return t.length; }); }

  function wordHit(hay, needle) {
    var at = hay.indexOf(needle);
    while (at !== -1) {
      var before = at === 0 ? '' : hay.charAt(at - 1);
      if (before === '' || before === ' ') return true;
      at = hay.indexOf(needle, at + 1);
    }
    return false;
  }

  function score(card, tokens, phrase) {
    var name = norm(card.dataset.name || card.getAttribute('data-name') || '');
    var cat = norm(card.dataset.category || card.getAttribute('data-category') || '');
    var use = norm(card.dataset.use || card.getAttribute('data-use') || '');
    var all = name + ' ' + cat + ' ' + use;
    for (var i = 0; i < tokens.length; i++) if (all.indexOf(tokens[i]) === -1) return -1;

    var s = 0;
    if (name === phrase) s += 1000;
    else if (name.indexOf(phrase) === 0) s += 420;
    else if (name.indexOf(phrase) !== -1) s += 240;
    tokens.forEach(function (t) {
      if (name === t) s += 200;
      else if (name.indexOf(t) === 0) s += 100;
      else if (wordHit(name, t)) s += 60;
      else if (name.indexOf(t) !== -1) s += 40;
      if (wordHit(cat, t)) s += 30;
      if (wordHit(use, t)) s += 15;
    });
    return s;
  }

  function syncURL(q) {
    var url = window.location.pathname + (q ? '?q=' + encodeURIComponent(q) : '');
    try { window.history.replaceState(null, '', url); } catch (err) { /* sandboxed */ }
  }

  function apply() {
    var q = input.value.trim();
    var tokens = toks(q);

    if (!tokens.length) {
      originalOrder.forEach(function (c) { if (grid) grid.appendChild(c); c.hidden = false; });
      if (count) count.textContent = cards.length + ' tools';
      return;
    }

    var phrase = norm(q);
    var scored = [];
    cards.forEach(function (c) {
      var s = score(c, tokens, phrase);
      c.hidden = s < 0;
      if (s >= 0) scored.push({ card: c, s: s });
    });
    scored.sort(function (a, b) {
      if (b.s !== a.s) return b.s - a.s;
      return (a.card.dataset.name || '').localeCompare(b.card.dataset.name || '');
    });
    if (grid) scored.forEach(function (x) { grid.appendChild(x.card); });

    if (count) {
      count.textContent = scored.length
        ? scored.length + ' of ' + cards.length + ' tools match'
        : 'No tools match';
    }
  }

  function schedule() {
    if (debounce) clearTimeout(debounce);
    debounce = setTimeout(function () { syncURL(input.value.trim()); apply(); }, 110);
  }

  input.addEventListener('input', schedule);
  input.addEventListener('search', schedule);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && input.value) {
      e.preventDefault(); input.value = ''; syncURL(''); apply();
    }
  });

  /* Deep-link support: /tools/?q=cursor arrives filtered rather than ignored. */
  var initial = new URLSearchParams(window.location.search).get('q');
  if (initial) { input.value = initial; apply(); }
  else apply();
})();
