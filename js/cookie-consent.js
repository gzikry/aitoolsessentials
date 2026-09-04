/* Cookie consent banner: lightweight, no dependencies. */
(function () {
  var KEY = 'aitoolsessentials.cookie_consent.v1';
  function getConsent() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function setConsent(val) {
    try { localStorage.setItem(KEY, val); } catch (e) {}
  }
  function buildBanner() {
    var banner = document.createElement('div');
    banner.id = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.innerHTML = '<div class="cookie-box">' +
      '<span class="cookie-text">We use essential cookies for site operation and anonymous analytics (Plausible). No advertising cookies. ' +
      '<a href="/legal/privacy.html">Privacy policy</a></span>' +
      '<div class="cookie-actions">' +
      '<button class="button button-blue" id="cookie-accept">Accept</button> ' +
      '<button class="button button-ghost" id="cookie-decline">Decline</button>' +
      '</div></div>';
    return banner;
  }
  function show() {
    if (getConsent()) return;
    var banner = buildBanner();
    document.body.appendChild(banner);
    document.getElementById('cookie-accept').addEventListener('click', function () {
      setConsent('accepted');
      banner.remove();
    });
    document.getElementById('cookie-decline').addEventListener('click', function () {
      setConsent('declined');
      banner.remove();
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', show);
  } else {
    show();
  }
})();
