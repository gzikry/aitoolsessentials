/* AIT site JS: share row + small niceties */
(function () {
  var mount = document.getElementById('share-row');
  if (mount && mount.hidden) {
    mount.hidden = false;
    mount.className = 'share-row';
    var url = encodeURIComponent(location.href.split('?')[0]);
    var title = encodeURIComponent(document.title);
    mount.innerHTML = '<span>Share</span>' +
      '<a href="https://twitter.com/intent/tweet?url=' + url + '&text=' + title + '" target="_blank" rel="nofollow noopener" aria-label="Share on X">' +
      '<svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>' +
      '<a href="https://www.linkedin.com/sharing/share-offsite/?url=' + url + '" target="_blank" rel="nofollow noopener" aria-label="Share on LinkedIn">' +
      '<svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0z"/></svg></a>';
    var links = mount.querySelectorAll('a');
    for (var i = 0; i < links.length; i++) links[i].addEventListener('click', function (e) {
      e.preventDefault();
      window.open(this.href, 'share', 'width=600,height=480');
    });
  }
})();

/* No-login shortlist: visitors can save tools while browsing. */
(function () {
  var KEY = 'aitoolsessentials.shortlist.v1';
  function getList() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
  }
  function setList(list) { localStorage.setItem(KEY, JSON.stringify(list.slice(0, 24))); }
  function slugFromHref(href) {
    var m = href && href.match(/\/tools\/([^\/]+)\/?(?:[#?].*)?$/);
    if (!m) m = href && href.match(/(?:^|\/)tools\/([^\/]+)\/?(?:[#?].*)?$/);
    return m ? m[1] : null;
  }
  function nameFromAnchor(a) {
    var card = a.closest('article, .review-hero, .score-card');
    var h = card && card.querySelector('h1,h2,h3');
    return (h ? h.textContent : a.textContent).replace(/\s*review\s*$/i, '').trim();
  }
  function isSaved(slug) { return getList().some(function (x) { return x.slug === slug; }); }
  function save(slug, name, url) {
    var list = getList().filter(function (x) { return x.slug !== slug; });
    list.unshift({ slug: slug, name: name, url: url, savedAt: Date.now() });
    setList(list);
  }
  function remove(slug) { setList(getList().filter(function (x) { return x.slug !== slug; })); }
  function updateButton(btn, slug) {
    var saved = isSaved(slug);
    btn.textContent = saved ? 'Saved ✓' : 'Add to shortlist';
    btn.setAttribute('aria-pressed', saved ? 'true' : 'false');
  }
  function addButtons() {
    var anchors = document.querySelectorAll('a[href*="/tools/"], a[href^="tools/"]');
    var seenCards = new WeakSet();
    anchors.forEach(function (a) {
      var slug = slugFromHref(a.getAttribute('href') || a.href);
      if (!slug || slug === 'index.html') return;
      var card = a.closest('article');
      if (!card || seenCards.has(card) || card.querySelector('.shortlist-btn')) return;
      seenCards.add(card);
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'shortlist-btn';
      btn.dataset.slug = slug;
      btn.dataset.url = a.href;
      btn.dataset.name = nameFromAnchor(a);
      updateButton(btn, slug);
      btn.addEventListener('click', function () {
        if (isSaved(slug)) remove(slug); else save(slug, btn.dataset.name, btn.dataset.url);
        updateButton(btn, slug);
        renderWidget();
      });
      var actions = card.querySelector('.card-actions') || card;
      actions.appendChild(btn);
    });
  }
  function renderWidget() {
    var list = getList();
    var w = document.getElementById('shortlist-widget');
    if (!w) {
      w = document.createElement('a');
      w.id = 'shortlist-widget';
      w.href = '/shortlist.html';
      document.body.appendChild(w);
    }
    w.hidden = !list.length;
    w.textContent = list.length + ' saved tool' + (list.length === 1 ? '' : 's') + ' →';
  }
  document.addEventListener('DOMContentLoaded', function () { addButtons(); renderWidget(); });
})();


/* Auto table-of-contents for long guides/comparisons. */
(function () {
  function slugify(text) {
    return text.toLowerCase().replace(/<[^>]+>/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 80) || 'section';
  }
  document.addEventListener('DOMContentLoaded', function () {
    var path = location.pathname;
    var eligible = /\/(articles|comparisons|research|alternatives)\//.test(path) || /free-ai-tools\.html$/.test(path);
    if (!eligible || document.querySelector('.auto-toc')) return;
    var headings = Array.prototype.slice.call(document.querySelectorAll('main h2')).filter(function (h) {
      return h.textContent.trim().length > 3 && !h.closest('.content-hub-card,.directory-card,.footer');
    }).slice(0, 12);
    if (headings.length < 4) return;
    var seen = {};
    headings.forEach(function (h) {
      var id = h.id || slugify(h.textContent);
      if (seen[id]) id += '-' + (++seen[id]); else seen[id] = 1;
      h.id = id;
    });
    var toc = document.createElement('nav');
    toc.className = 'auto-toc';
    toc.setAttribute('aria-label', 'Page sections');
    toc.innerHTML = '<span>On this page</span>' + headings.map(function (h) {
      return '<a href="#' + h.id + '">' + h.textContent.trim() + '</a>';
    }).join('');
    var firstSection = document.querySelector('main > section:nth-of-type(2)') || document.querySelector('main > section');
    if (firstSection) firstSection.insertBefore(toc, firstSection.firstChild);
  });
})();
