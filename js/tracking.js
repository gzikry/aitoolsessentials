// Lightweight local click instrumentation for future analytics migration.
(function () {
  document.addEventListener('click', function (event) {
    const link = event.target.closest && event.target.closest('a[data-outbound="true"]');
    if (!link) return;
    try {
      const key = 'aitoolsessentials_outbound_clicks';
      const data = JSON.parse(localStorage.getItem(key) || '{}');
      const href = link.getAttribute('href') || 'unknown';
      data[href] = (data[href] || 0) + 1;
      localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      // Keep navigation unaffected if storage is unavailable.
    }
  });
})();
