/* Predictive search box for the site header.
 *
 * George's ask: "when someone types the search is working already, it'll be nice to have it be
 * predictive." The page at /search/ ranks well but you have to navigate to it first. This puts a
 * box in the header of every page that starts suggesting on the first keystroke, ranked by the
 * same engine the full page uses (js/search-core.js) so the two never disagree.
 *
 * Degrades without JavaScript: the markup is a real <form action="/search/" method="get"> with a
 * named input, so submitting lands on /search/?q=… and the full page renders it. JS only adds the
 * dropdown.
 *
 * The index (~245 KB) is fetched lazily on first focus or first keystroke, never on page load,
 * and is cached across both search surfaces by search-core.
 */
(function () {
  'use strict';

  var form = document.getElementById('ait-hs');
  var input = document.getElementById('ait-hs-input');
  var list = document.getElementById('ait-hs-list');
  if (!form || !input || !list) return;

  var MAX = 7;
  var DEBOUNCE_MS = 70;
  var S = window.AITSearch;
  if (!S) return;

  var index = null;
  var loading = false;
  var failed = false;
  var timer = null;
  var active = -1;
  var items = [];

  function ensureIndex() {
    if (index || loading || failed) return;
    loading = true;
    S.loadIndex().then(function (entries) {
      index = entries;
      loading = false;
      /* A keystroke may have arrived while the index was in flight. */
      if (input.value.trim()) render();
    }).catch(function () {
      loading = false;
      failed = true;
      close();
    });
  }

  function resultRow(e, toks) {
    var type = S.TYPE_LABELS[e.type] || 'Page';
    var meta = type + (e.category ? ' · ' + e.category : '');
    return '<a class="ait-hs-item" role="option" href="' + S.esc(e.url) + '">' +
             '<span class="ait-hs-type">' + S.esc(meta) + '</span>' +
             '<span class="ait-hs-name">' + S.highlight(S.esc(e.name), toks) + '</span>' +
           '</a>';
  }

  function render() {
    var q = input.value.trim();
    items = [];
    active = -1;

    if (!q) {
      /* Predictions are for typing. On an empty box, show nothing rather than a menu. */
      close();
      return;
    }
    if (failed) { close(); return; }
    if (!index) {
      ensureIndex();
      list.innerHTML = '<li class="ait-hs-note">Loading search…</li>';
      open();
      return;
    }

    var r = S.rank(index, q, MAX);
    if (!r.total) {
      /* A dead end is the worst outcome: the reader assumes the site lacks the thing. Offer the
         closest entries by name/slug/keyword so a typo ("halo" for "HOL Registry") still lands. */
      var near = S.suggest(index, q, 4);
      var inner = '<li class="ait-hs-note">No matches for “' + S.esc(q) + '”' +
                  (near.length ? ' — did you mean:' : '.') + '</li>';
      inner += near.map(function (e, i) {
        return resultRow(e, []).replace('class="ait-hs-item"',
          'class="ait-hs-item" id="ait-hs-opt-' + i + '"');
      }).join('');
      inner += '<li class="ait-hs-all" role="option" id="ait-hs-opt-all" data-all="1">' +
               'Search everything for “' + S.esc(q) + '”</li>';
      items = near.slice();
      list.innerHTML = inner;
      open();
      return;
    }

    items = r.hits;
    var html = r.hits.map(function (e, i) {
      return resultRow(e, r.toks).replace('class="ait-hs-item"',
        'class="ait-hs-item" id="ait-hs-opt-' + i + '"');
    }).join('');

    html += '<li class="ait-hs-all" role="option" id="ait-hs-opt-all" data-all="1">' +
              'See all ' + r.total + ' result' + (r.total === 1 ? '' : 's') + ' for “' + S.esc(q) + '”' +
            '</li>';

    list.innerHTML = html;
    open();
  }

  function open() {
    list.hidden = false;
    input.setAttribute('aria-expanded', 'true');
    form.classList.add('ait-hs-open');
  }

  function close() {
    list.hidden = true;
    list.innerHTML = '';
    input.setAttribute('aria-expanded', 'false');
    input.removeAttribute('aria-activedescendant');
    form.classList.remove('ait-hs-open');
    active = -1;
  }

  function options() {
    return list.querySelectorAll('.ait-hs-item, .ait-hs-all');
  }

  function move(delta) {
    var opts = options();
    if (!opts.length) return;
    active = (active + delta + opts.length) % opts.length;
    for (var i = 0; i < opts.length; i++) {
      opts[i].classList.toggle('ait-hs-active', i === active);
      opts[i].setAttribute('aria-selected', i === active ? 'true' : 'false');
    }
    var el = opts[active];
    input.setAttribute('aria-activedescendant', el.id);
  }

  function goFullResults() {
    var q = input.value.trim();
    window.location.href = '/search/' + (q ? '?q=' + encodeURIComponent(q) : '');
  }

  input.addEventListener('focus', ensureIndex);

  input.addEventListener('input', function () {
    ensureIndex();
    if (timer) clearTimeout(timer);
    timer = setTimeout(render, DEBOUNCE_MS);
  });

  input.addEventListener('keydown', function (ev) {
    if (ev.key === 'ArrowDown') { ev.preventDefault(); if (!list.hidden) move(1); }
    else if (ev.key === 'ArrowUp') { ev.preventDefault(); if (!list.hidden) move(-1); }
    else if (ev.key === 'Escape') {
      if (!list.hidden) { ev.preventDefault(); close(); }
      else { input.blur(); }
    } else if (ev.key === 'Enter') {
      var opts = options();
      if (!list.hidden && active >= 0 && opts[active]) {
        ev.preventDefault();
        if (opts[active].getAttribute('data-all')) goFullResults();
        else opts[active].click();
      }
      /* With no highlighted row, let the form submit to /search/?q= as it would without JS. */
    }
  });

  /* Close when focus or the pointer leaves the widget. */
  document.addEventListener('click', function (ev) {
    if (!form.contains(ev.target)) close();
  });
  form.addEventListener('focusout', function () {
    setTimeout(function () {
      if (!form.contains(document.activeElement)) close();
    }, 120);
  });

  /* Keyboard users land here with "/" the way most search-first sites behave, but only when
     they are not already typing into a field. */
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== '/' || ev.metaKey || ev.ctrlKey || ev.altKey) return;
    var el = document.activeElement;
    var tag = el ? el.tagName : '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (el && el.isContentEditable)) return;
    ev.preventDefault();
    input.focus();
    input.select();
  });
})();
