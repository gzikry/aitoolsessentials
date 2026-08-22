#!/usr/bin/env python3
"""Generate the public benchmark evidence hub from data/benchmarks.json."""
import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"


def generate(root: Path) -> Path:
    data = json.loads((root / "data/benchmarks.json").read_text())
    sources = {s["id"]: s for s in data["sources"]}
    tool_names = {t['slug']: t['name'] for t in json.loads((root / 'data/tools.json').read_text())}

    snapshot_rows = ""
    for row in data.get("arena_text_snapshot", []):
        source = sources[row["source_id"]]
        snapshot_rows += f'''<tr>
<td><a href="../tools/{row['tool_slug']}/">{tool_names.get(row['tool_slug'], row['tool_slug'].replace('-', ' ').title())}</a></td>
<td><code>{row['model']}</code></td><td>#{row['rank']}</td><td>{row['score']}</td>
<td>{row['votes']:,}</td><td>{row['note']} <a href="{source['url']}" rel="external noopener">[{source['id']}]</a></td>
</tr>'''

    source_cards = ""
    for source in data["sources"]:
        source_cards += f'''<article class="benchmark-source-card">
<span class="benchmark-ref">[{source['id']}]</span>
<h3>{source['name']}</h3>
<p><strong>Measures:</strong> {source['measures']}</p>
<p><strong>Use it for:</strong> {source['use_for']}</p>
<p class="benchmark-caveat"><strong>Do not miss:</strong> {source['caveat']}</p>
<a class="text-link" href="{source['url']}" target="_blank" rel="external noopener">Open source ↗</a>
</article>'''

    html = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Dated AI benchmark snapshots with model versions, methodology, sources, and caveats. Compare evidence without confusing model scores with product reviews.">
<title>AI Benchmarks — Dated, Sourced &amp; Explained | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/benchmarks/">
<link rel="stylesheet" href="../css/styles.css"><link rel="stylesheet" href="../css/share.css">
</head><body>
<header class="global-nav"><a class="brand" href="../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>
<nav class="nav-links"><a href="../tools/index.html">Tools</a><a href="../comparisons/best-ai-tools.html">Best AI tools</a><a href="../categories/index.html">Categories</a><a href="../articles/index.html">Guides</a><a href="index.html" aria-current="page">Benchmarks</a></nav>
<a class="nav-cta" href="../legal/affiliate-disclosure.html">Disclosure</a></header>

<section class="review-hero scene scene-light"><p class="kicker light">Evidence hub</p>
<h1>AI benchmarks, with the footnotes left in.</h1>
<p>Model version, date, harness, source, and limitation—all visible. We use benchmarks as supporting evidence, never as a substitute for workflow fit.</p>
<p class="last-updated">Arena snapshot: {data['snapshot_date']} · Evidence reviewed: {data['reviewed_date']}</p></section>

<section class="benchmark-policy"><div>
<h2>{data['policy']['title']}</h2><p>{data['policy']['summary']}</p>
<div class="benchmark-rules"><span>Exact model/version</span><span>Snapshot date</span><span>Harness disclosed</span><span>Source linked</span><span>Stale after {data['policy']['staleness_days']} days</span></div>
</div></section>

<section class="benchmark-section"><div class="section-title"><p class="kicker light">Current snapshot</p><h2>Arena Text: representative model listings</h2>
<p>These rows provide model-family context for selected products. They do not claim that the listed model is the product's current default.</p></div>
<div class="table-wrap"><table class="benchmark-table"><thead><tr><th>Product family</th><th>Exact model</th><th>Rank</th><th>Arena score</th><th>Votes</th><th>Interpretation</th></tr></thead><tbody>{snapshot_rows}</tbody></table></div>
<p class="benchmark-caveat"><strong>Read this correctly:</strong> Arena scores human preference in anonymous pairwise battles. A higher rank does not prove better factuality, lower cost, stronger privacy, or a better end-user product. <a href="{sources[2]['url']}" target="_blank" rel="external noopener">Methodology [2] ↗</a></p></section>

<section class="benchmark-section scene scene-light"><div class="section-title"><p class="kicker light">Source registry</p><h2>What we trust—and what each source misses.</h2></div>
<div class="benchmark-source-grid">{source_cards}</div></section>

<section class="benchmark-section"><div class="section-title"><p class="kicker light">Where benchmarks belong</p><h2>Match the evidence to the buying decision.</h2></div>
<div class="workflow-cards benchmark-use-grid">
<article><span>01</span><h3>General assistants</h3><p>Arena preference + LiveBench objective tasks + price/latency context. Never collapse them into one magic number.</p></article>
<article><span>02</span><h3>Coding assistants</h3><p>SWE-bench only when the exact model, agent harness and release are disclosed. Product UX still needs separate evaluation.</p></article>
<article><span>03</span><h3>Image, video &amp; audio</h3><p>Use modality-specific quality and latency methods. Product outputs, rights, editing control, and consistency matter more than text benchmarks.</p></article>
</div></section>

<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="../advertise/index.html" rel="nofollow">Advertise</a><a href="../submit-tool.html" rel="nofollow">Submit a tool</a><a href="../legal/editorial-methodology.html">Methodology</a><a href="mailto:{EMAIL}">Contact</a></footer>
<script src="../js/site.js" defer></script><script src="../js/analytics.js" defer></script>
</body></html>'''
    out = root / "benchmarks" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return out


if __name__ == "__main__":
    generate(Path('/Users/georgezikry/aitoolessentials/site'))
