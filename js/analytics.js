/* Lightweight analytics loader — activates once you create a site at plausible.io
   for aitoolsessentials.com. Until then it silently does nothing. */
(function () {
  var s = document.createElement('script');
  s.defer = true;
  s.dataset.domain = 'aitoolsessentials.com';
  s.src = 'https://plausible.io/js/script.js';
  // Only actually track when the page is served from the real domain (not localhost/preview)
  if (location.hostname === 'aitoolsessentials.com' || location.hostname === 'www.aitoolsessentials.com') {
    document.head.appendChild(s);
  }
})();
