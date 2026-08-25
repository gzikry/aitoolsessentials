/* Decision Brief generator — client-side, no login required. */
(function () {
  var selA = document.getElementById('pick-a');
  var selB = document.getElementById('pick-b');
  var selC = document.getElementById('pick-c');
  var out = document.getElementById('brief-output');
  var btn = document.getElementById('generate-brief');
  if (!selA || !selB || !AIT_TOOLS) return;
  var sorted = AIT_TOOLS.slice().sort(function (x, y) { return x.name.localeCompare(y.name); });

  function fill(sel, allowEmpty) {
    sel.innerHTML = '';
    if (allowEmpty) {
      var none = document.createElement('option'); none.value = ''; none.textContent = '— none —'; sel.appendChild(none);
    }
    sorted.forEach(function (t) {
      var o = document.createElement('option');
      o.value = t.slug; o.textContent = t.name + ' · ' + (t.category || '');
      sel.appendChild(o);
    });
  }
  fill(selA, false); fill(selB, false); fill(selC, true);

  // Pre-select from ?vs=slug1,slug2 links (shareable entry points)
  try {
    var vs = new URLSearchParams(window.location.search).get('vs');
    if (vs) {
      var slugs = vs.split(',').slice(0, 3);
      [selA, selB, selC].forEach(function (sel, i) { if (slugs[i]) sel.value = slugs[i]; });
    }
  } catch (e) {}

  function pricePressure(p) {
    p = (p || '').toLowerCase();
    if (p.indexOf('free') > -1 && p.indexOf('paid') > -1) return 'Free + paid tiers';
    if (p.indexOf('free') === 0) return 'Free-first';
    return 'Paid';
  }

  function render() {
    var slugs = [selA.value, selB.value, selC.value].filter(Boolean).filter(function (v, i, a) { return a.indexOf(v) === i; });
    if (slugs.length < 2) return;
    var picks = slugs.map(function (s) { return AIT_TOOLS.find(function (t) { return t.slug === s; }); }).filter(Boolean);

    // Overlap warning
    var cats = {};
    picks.forEach(function (t) { (cats[t.category] = cats[t.category] || []).push(t.name); });
    var overlaps = Object.keys(cats).filter(function (c) { return cats[c].length > 1; });
    var overlapHtml = '';
    if (overlaps.length) {
      overlapHtml = '<section class="score-card" style="border-left:4px solid #d97706;margin-bottom:18px"><span>Overlap check</span><h3>' +
        esc(overlaps.join(' & ')) + ': these do the same job</h3><p>You likely only need one. Pick by editing burden in your real workflow, not feature lists. If both are paid, run the trial before keeping both.</p></section>';
    } else {
      overlapHtml = '<section class="score-card" style="border-left:4px solid #16a34a;margin-bottom:18px"><span>Overlap check</span><h3>Different jobs — they can coexist</h3><p>No direct category overlap detected. These could complement each other instead of competing.</p></section>';
    }
    document.getElementById('brief-verdict').innerHTML = overlapHtml;

    // Comparison table
    var rows = '<div class="table-wrap"><table><thead><tr><th></th>';
    picks.forEach(function (t) { rows += '<th>' + esc(t.name) + '</th>'; });
    rows += '</tr></thead><tbody>';
    rows += '<tr><td><strong>Category</strong></td>' + picks.map(function (t) { return '<td>' + esc(t.category) + '</td>'; }).join('') + '</tr>';
    rows += '<tr><td><strong>Pricing model</strong></td>' + picks.map(function (t) { return '<td>' + esc(pricePressure(t.price)) + '</td>'; }).join('') + '</tr>';
    rows += '<tr><td><strong>Editorial score</strong></td>' + picks.map(function (t) { return '<td><strong>' + esc(t.rating) + '/5</strong></td>'; }).join('') + '</tr>';
    rows += '<tr><td><strong>Best fit</strong></td>' + picks.map(function (t) { return '<td>' + esc(t.bestFor) + '</td>'; }).join('') + '</tr>';
    rows += '<tr><td><strong>Review</strong></td>' + picks.map(function (t) { return '<td><a href="/tools/' + esc(t.slug) + '/">Read full review →</a></td>'; }).join('') + '</tr>';
    rows += '</tbody></table></div>';
    document.getElementById('brief-table').innerHTML = rows;

    // Trial script
    var names = picks.map(function (t) { return t.name; });
    var trials = '<section class="score-card" style="margin-top:18px"><span>Trial script</span><h3>Run this before paying anyone</h3><ol>' +
      '<li>Pick <strong>one real task</strong> from your actual work this week.</li>' +
      '<li>Run it in each: ' + names.map(esc).join(', ') + '.</li>' +
      '<li>Time how long until a <em>usable</em> result — then count the edits you made after.</li>' +
      '<li>Check output rights/training policy on each review page if work is commercial.</li>' +
      '<li>Keep the winner. Cancel or defer anything without a weekly job.</li></ol></section>';
    document.getElementById('brief-trials').innerHTML = trials;

    // Share
    var shareText = 'AI decision brief: ' + names.join(' vs ') + '. Scores, cost pressure, and the exact trial to run — from aitoolsessentials.com';
    var url = location.origin + '/decision-brief.html?vs=' + slugs.join(',');
    var shareEl = document.getElementById('brief-share');
    shareEl.innerHTML =
      '<a class="button button-blue" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText) + '">Share on X</a>' +
      '<a class="button button-dark" target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url) + '">Share on LinkedIn</a>' +
      '<button class="button button-ghost-dark" id="copy-brief-link">Copy link</button>';
    var copyBtn = document.getElementById('copy-brief-link');
    if (copyBtn) copyBtn.addEventListener('click', function () {
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () {
        copyBtn.textContent = 'Copied!';
        setTimeout(function () { copyBtn.textContent = 'Copy link'; }, 1600);
      }, function () { window.prompt('Copy this link:', url); });
    });

    out.hidden = false;
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  if (btn) btn.addEventListener('click', render);
})();
