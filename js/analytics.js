/* Lightweight Plausible loader for aitoolsessentials.com.
   Conversion events fire only from actual matching link clicks on OUR pages.
   Goal names are intent-based, not href-based: deriving them from the raw href
   produced dozens of near-duplicate goals for the same destination (relative vs
   absolute spellings, per-role stack-builder variants) and labelled clicks on
   EXTERNAL vendor /pricing/ links as if they were our own conversion. */
(function () {
  var s = document.createElement('script');
  s.defer = true;
  s.dataset.domain = 'aitoolsessentials.com';
  s.src = 'https://plausible.io/js/script.js';

  var SITE_HOST = 'aitoolsessentials.com';

  // Ordered: first match wins. Each entry maps a destination to ONE stable goal name.
  var DESTINATIONS = [
    { goal: 'pricing',                test: '/pricing/' },
    { goal: 'premium',                test: '/premium' },
    { goal: 'subscribe',              test: '/subscribe/' },
    { goal: 'newsletter',             test: '/newsletter/' },
    // Distinct from stack-audit.js's own stack_audit_started/completed events:
    // this records a click that LEADS to the page (entry intent), not funnel progress.
    { goal: 'stack_audit_entry',      test: '/stack-audit.html' },
    { goal: 'stack_builder',          test: '/stack-builder.html' },
    { goal: 'cost_calculator',        test: '/cost-calculator.html' },
    { goal: 'automation_cost_decoder',test: '/automation-cost-decoder' },
    { goal: 'compare_shortlist',      test: '/compare-shortlist.html' }
  ];

  function isInternal(a) {
    if (a.hasAttribute('data-outbound')) return false;
    var href = a.getAttribute('href') || '';
    if (!href || href.charAt(0) === '#') return false;
    if (href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) return false;
    if (/^https?:\/\//i.test(href)) {
      try {
        return new URL(href, location.href).hostname.replace(/^www\./, '') === SITE_HOST;
      } catch (err) {
        return false;
      }
    }
    return true;
  }

  function goalFor(a) {
    if (!isInternal(a)) return null;
    var href = a.getAttribute('href') || '';
    for (var i = 0; i < DESTINATIONS.length; i++) {
      if (href.indexOf(DESTINATIONS[i].test) !== -1) return DESTINATIONS[i].goal;
    }
    return null;
  }

  // Only actually track when the page is served from the real domain (not localhost/preview)
  if (location.hostname === SITE_HOST || location.hostname === 'www.' + SITE_HOST) {
    window.plausible = window.plausible || function () { (plausible.q = plausible.q || []).push(arguments); };
    window.plausibleQueue = window.plausibleQueue || new Set();
    window._aitools_plausible_init = window._aitools_plausible_init || false;
    window._aitools_plausible_pre = window._aitools_plausible_pre || function () {
      if (!window._aitools_plausible_init) {
        window._aitools_plausible_init = true;
        document.head.appendChild(s);
        document.addEventListener('click', function (e) {
          var el = e.target.closest && e.target.closest('a[href]');
          if (!el) return;
          var goal = goalFor(el);
          if (!goal) return;
          if (window.plausibleQueue.has(goal)) return;
          window.plausibleQueue.add(goal);
          window.plausible('conversion_' + goal);
        }, true);
      }
    };
    if (document.readyState === 'complete') {
      window._aitools_plausible_pre();
    } else {
      window.addEventListener('load', window._aitools_plausible_pre);
    }
  }
})();
