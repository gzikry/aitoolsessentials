#!/usr/bin/env python3
"""Inject evidence-status panels into the site's major comparison pages."""
import json, re
from pathlib import Path

COMPARISONS = {
    'chatgpt-vs-claude.html': ['chatgpt', 'claude'],
    'chatgpt-vs-grok.html': ['chatgpt', 'grok'],
    'claude-vs-grok.html': ['claude', 'grok'],
    'cursor-vs-github-copilot.html': ['cursor', 'github-copilot'],
    'perplexity-vs-chatgpt.html': ['perplexity', 'chatgpt'],
    'chatgpt-vs-perplexity.html': ['chatgpt', 'perplexity'],
    'claude-vs-cursor.html': ['claude', 'cursor'],
    'midjourney-vs-canva-ai.html': ['midjourney', 'canva-ai'],
    'zapier-vs-make-vs-n8n.html': ['zapier-ai', 'make', 'n8n'],
}


def generate(root: Path) -> int:
    tools = {x['slug']: x for x in json.loads((root/'data/tools.json').read_text())}
    sources = {x['slug']: x for x in json.loads((root/'data/tool_sources.json').read_text())['tools']}
    benchmarks = json.loads((root/'data/benchmarks.json').read_text())
    arena = {x['tool_slug']: x for x in benchmarks.get('arena_text_snapshot', [])}
    coding = {x['tool_slug']: x for x in benchmarks.get('coding_agent_snapshot', [])}
    changed = 0
    for filename, slugs in COMPARISONS.items():
        path = root/'comparisons'/filename
        if not path.exists(): continue
        html = path.read_text()
        original = html
        html = re.sub(r'<!-- AIT COMPARISON EVIDENCE START -->.*?<!-- AIT COMPARISON EVIDENCE END -->', '', html, flags=re.S)
        cards = ''
        benchmark_notes = []
        for slug in slugs:
            tool = tools[slug]; src = sources[slug]
            links = ''.join(
                f'<a href="{src[k]}" target="_blank" rel="external noopener">{label} ↗</a>'
                for label,k in [('Pricing','pricing_url'),('Docs','docs_url'),('Privacy','privacy_url'),('Rights','rights_url')] if src.get(k)
            )
            cards += f'''<div><strong>{tool['name']}</strong><p>{src.get('pricing_summary') or 'No stable public pricing verified.'}</p><span>Official sources checked {src.get('pricing_checked_date')}</span><div class="official-source-links">{links}</div></div>'''
            if slug in arena:
                b=arena[slug]; benchmark_notes.append(f"{tool['name']}: Arena Text {b['model']} — Arena rank #{b['rank']}, Arena rating {b['score']} (95% confidence interval; {b['votes']:,} preference votes; snapshot {benchmarks['snapshot_date']}).")
            if slug in coding:
                b=coding[slug]; benchmark_notes.append(f"{tool['name']}: {b['benchmark']} — {b['configuration']}, {b['score']}, {b['trials']} trials; reward-hack disqualifications {b['reward_hack_disqualification']}.")
        bench_html = '<ul>'+''.join(f'<li>{x}</li>' for x in benchmark_notes)+'</ul>' if benchmark_notes else '<p>No directly comparable exact-version numeric snapshot is published for every product in this comparison.</p>'
        panel = f'''<!-- AIT COMPARISON EVIDENCE START --><section class="comparison-evidence"><h2>Evidence status</h2><div class="decision-grid">{cards}</div><h3>External benchmark context</h3>{bench_html}<p class="benchmark-caveat">Benchmark records apply only to the exact model/configuration shown—not the whole product. Independent same-task hands-on comparison: <strong>not yet published</strong>. <a href="../legal/testing-protocol.html">See the testing protocol</a>.</p></section><!-- AIT COMPARISON EVIDENCE END -->'''
        marker = '<h2>When '
        idx = html.find(marker)
        if idx >= 0:
            html = html[:idx] + panel + html[idx:]
        else:
            html = html.replace('</div></section>', panel+'</div></section>', 1)
        html = re.sub(r'<!-- AIT RELATED LINKS START -->.*?<!-- AIT RELATED LINKS END -->\s*', '', html, flags=re.S)
        html = re.sub(r'<section class="score-card related-next-steps"><span>Related</span><h3>Next reads</h3>.*?</section>\s*', '', html, flags=re.S)
        newsletter_panel = '<!-- AIT RELATED LINKS START --><section class="score-card related-next-steps"><span>Related</span><h3>Next reads</h3><p><a href="/pricing-watch/">Pricing Watch</a> · <a href="/change-radar/">Change Radar</a> · <a href="/premium/">Premium</a> · <a href="/newsletter/">Newsletter</a></p></section><!-- AIT RELATED LINKS END -->\n'
        close_main = html.find('</main>')
        if close_main >= 0:
            html = html[:close_main] + newsletter_panel + html[close_main:]
        if html != original:
            path.write_text(html); changed += 1
    print(f'Enhanced comparison evidence on {changed} pages')
    return changed


if __name__ == '__main__':
    generate(Path(__file__).resolve().parents[1])
