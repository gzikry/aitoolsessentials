#!/usr/bin/env python3
"""Generate the Decision Brief tool — pick tools you're choosing between and get a
shareable, source-dated decision brief with overlap warnings and trial tests.

This is the competitive differentiator: rival directories list tools; this helps
people DECIDE between specific candidates and share the outcome.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


TOOLS_JSON = None


def _load_tools(root: Path) -> list[dict[str, Any]]:
    return json.loads((root / "data/tools.json").read_text())


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    global TOOLS_JSON
    if tools is None:
        tools = _load_tools(root)
    today = today or datetime.today().strftime("%Y-%m-%d")
    by_slug = {t["slug"]: t for t in tools}
    payload = json.dumps(
        [
            {
                "slug": t["slug"],
                "name": t.get("name"),
                "category": t.get("category"),
                "price": t.get("price") or t.get("pricing"),
                "rating": t.get("rating") or t.get("editorial_score"),
                "bestFor": t.get("best_for"),
                "summary": t.get("summary"),
                "pros": t.get("pros") or [],
                "cons": t.get("cons") or [],
            }
            for t in tools
        ],
        separators=(",", ":"),
    )

    desc = ("Pick two or three AI tools you are deciding between and get an instant decision brief: "
            "overlap check, cost comparison, editorial scores, trial tests, and a shareable summary.")
    title = "AI Tool Decision Brief Generator"

    html = f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(desc)}">
<title>{title} — AIToolsEssentials</title>
<link rel="canonical" href="https://aitoolsessentials.com/decision-brief.html">
<meta property="og:title" content="{title}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://aitoolsessentials.com/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"{title}","applicationCategory":"UtilityApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}},"url":"https://aitoolsessentials.com/decision-brief.html","publisher":{{"@type":"Organization","name":"AIToolsEssentials"}}}}</script>
</head><body>
<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a><a href="/tool-finder.html">Tool finder</a><a href="/alternatives/">Alternatives</a><a href="/resources/">Resources</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>
<main>
<section class="scene scene-dark"><div style="max-width:940px;margin:0 auto;padding:88px 28px 64px;text-align:center">
<p class="kicker">Decision brief generator</p>
<h1>Stuck between two AI tools? Get a verdict.</h1>
<p class="subhead">Pick two or three tools you're choosing between. You'll get an instant side-by-side brief: overlap check, monthly cost math, editorial scores, what to test in each trial, and a shareable summary card.</p>
<p><a class="button button-blue" href="#brief-builder">Build my decision brief</a><a class="button button-ghost-dark" href="/premium/sample-report.html" style="margin-left:8px">See a sample deep-dive</a></p>
</div></section>

<section class="scene scene-light content-hub"><div class="article-shell wide" id="brief-builder">
<h2>Choose your contenders</h2>
<p>Pick two or three tools. Most people are choosing between a famous default and one alternative — that's exactly the comparison this solves.</p>
<div class="score-card" id="pickers">
<div class="picker-row"><label for="pick-a">Contender 1</label><select id="pick-a"></select></div>
<div class="picker-row"><label for="pick-b">Contender 2</label><select id="pick-b"></select></div>
<div class="picker-row"><label for="pick-c">Contender 3 <em style="font-style:normal;opacity:.6">(optional)</em></label><select id="pick-c"></select></div>
<p style="margin-top:14px"><button class="button button-blue" id="generate-brief">Generate decision brief</button></p>
</div>
<div id="brief-output" hidden>
<h2 style="margin-top:44px">Your decision brief</h2>
<div id="brief-verdict"></div>
<div id="brief-table"></div>
<div id="brief-trials"></div>
<div id="brief-share" style="margin-top:22px;display:flex;gap:10px;flex-wrap:wrap"></div>
<p class="affiliate-inline">Scores are editorial ratings, not benchmarks. Pricing is verified against official sources on the review page dates shown there — confirm before paying.</p>
</div>

<section class="score-card" style="margin-top:48px">
<span>Why this beats a directory list</span>
<h2>Directories help you discover. This helps you decide.</h2>
<ul>
<li><strong>Overlap check:</strong> instantly see when two candidates do the same job so you don't pay twice.</li>
<li><strong>Cost reality:</strong> free-first vs paid-only pressure, side by side.</li>
<li><strong>Trial script:</strong> the exact same task to run in each tool before spending money.</li>
<li><strong>Shareable verdict:</strong> copy a summary your team can read in 20 seconds.</li>
</ul>
<p><a href="/premium/">Want deeper workflow-level research? See Premium →</a></p>
</section>
</div></section>
</main>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a><a href="/legal/corrections.html">Corrections</a><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>
<script>const AIT_TOOLS={payload};</script>
<script src="/js/decision-brief.js" defer></script>
<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>
</body></html>'''
    (root / "decision-brief.html").write_text(html)

    js = '''/* Decision Brief generator — client-side, no login required. */
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
'''
    (root / "js/decision-brief.js").write_text(js)
    return 1


def postprocess(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    """Durable injection of decision-brief entry links into comparison pages and hubs."""
    import re as _re
    if tools is None:
        tools = _load_tools(root)
    names = {t["slug"]: t.get("name", "") for t in tools}
    changed = 0

    # Comparison pages: contextual "vs" link
    comp_dir = root / "comparisons"
    if comp_dir.exists():
        for p in sorted(comp_dir.glob("*.html")):
            s = p.read_text()
            if "decision-brief" in s:
                continue
            m = _re.match(r"^(.+?)-vs-(.+)$", p.stem)
            slugs = []
            if m:
                for cand in (m.group(1), m.group(2)):
                    for slug in names:
                        if slug == cand or slug.replace("-ai", "") == cand.replace("-ai", ""):
                            slugs.append(slug)
                            break
            vs = f"?vs={','.join(slugs)}" if len(slugs) >= 2 else ""
            link = ('<p style="text-align:center;margin-top:14px"><a class="button button-ghost-dark" '
                    f'href="/decision-brief.html{vs}">Get a shareable decision brief for this matchup →</a></p>')
            if "</main>" in s:
                s = s.replace("</main>", link + "</main>", 1)
                p.write_text(s)
                changed += 1

    # Start-here hero link
    sh = root / "start-here/index.html"
    if sh.exists():
        s = sh.read_text()
        if "decision-brief" not in s and '</p></div></section><section class="scene scene-light' in s:
            s = s.replace(
                '</p></div></section><section class="scene scene-light',
                '</p><p style="margin-top:18px"><a class="button button-blue" href="/decision-brief.html">Torn between two tools? Get a decision brief →</a></p></div></section><section class="scene scene-light',
                1,
            )
            sh.write_text(s)
            changed += 1

    # Site-map module
    sm = root / "site-map/index.html"
    if sm.exists():
        s = sm.read_text()
        if "decision-brief" not in s and "</main>" in s:
            module = ('<section class="scene scene-light" style="padding:0 24px 72px"><div class="article-shell wide">'
                      '<section class="score-card"><span>Decide faster</span><h3>Torn between two AI tools?</h3>'
                      '<p>Use the <a href="/decision-brief.html">AI Tool Decision Brief generator</a> for an instant overlap check, '
                      'cost comparison, trial script, and shareable verdict.</p></section></div></section>\n</main>')

            s = s.replace("</main>", module, 1)
            sm.write_text(s)
            changed += 1
    return changed


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    print(generate(root))
