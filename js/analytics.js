/* Lightweight analytics loader — activates once you create a site at plausible.io
   for aitoolsessentials.com. Until then it silently does nothing. */
(function () {
  var s = document.createElement('script');
  s.defer = true;
  s.dataset.domain = 'aitoolsessentials.com';
  s.src = 'https://plausible.io/js/script.js';
  // Only actually track when the page is served from the real domain (not localhost/preview)
  if (location.hostname === 'aitoolsessentials.com' || location.hostname === 'www.aitoolsessentials.com') {
    window.plausible = window.plausible || function() {(plausible.q = plausible.q || []).push(arguments)};
    window.plausibleQueue = window.plausibleQueue || new Set();
    window._aitools_plausible_init = window._aitools_plausible_init || false;
    window._aitools_plausible_pre = window._aitools_plausible_pre || function () {
      var names = ['pricing','premium','subscribe','stack_builder','cost_calculator','compare_shortlist','newsletter'];
      names.forEach(function (n, i) {
        document.documentElement.classList.add('plausible-event-name=' + n);
        window.plausibleQueue.add(n);
      });
      if (!window._aitools_plausible_init) {
        window._aitools_plausible_init = true;
        document.head.appendChild(s);
        document.addEventListener('click', function (e) {
          var el = e.target.closest('a[href*="/pricing/"],a[href*="/premium/"],a[href*="/subscribe/"],a[href*="/stack-builder.html"],a[href*="/cost-calculator.html"],a[href*="/compare-shortlist.html"],a[href*="/newsletter/"]');
          if (!el) return;
          var name = el.getAttribute('href').replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_|_$/g, '') || 'conversion';
          if (!window.plausibleQueue.has(name)) {
            window.plausibleQueue.add(name);
            window.plausible('conversion_' + name);
          }
        }, true);
        (function sendQueue() {
          if (!document.body) { requestAnimationFrame(sendQueue); return; }
          window.plausibleQueue.forEach(function (name) { window.plausible('conversion_' + name); });
          window.plausibleQueue.clear();
        })();
      }
    };
    if (document.readyState === 'complete') {
      window._aitools_plausible_pre();
    } else {
      window.addEventListener('load', window._aitools_plausible_pre);
    }
  }
})();
