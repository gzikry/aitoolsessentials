#!/usr/bin/env python3
"""Generate SEO growth hubs: free AI tools and alternatives."""
from pathlib import Path
import json

HEADER = '''<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a><a href="/alternatives/index.html">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/categories/index.html">Categories</a><a href="/articles/index.html">Guides</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>'''
FOOTER = '''<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:contact@aitoolsessentials.com">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'''

def card(t):
    return f'''<article class="content-hub-card"><span>{t['category']} · {t['price']}</span><h3><a href="/tools/{t['slug']}/">{t['name']}</a></h3><p>{t['summary']}</p><p><strong>Best for:</strong> {t.get('best_for','')}</p><a class="button button-blue small" href="/tools/{t['slug']}/">Read review</a></article>'''

def generate_free(root: Path, tools):
    free = [t for t in tools if 'free' in t.get('price','').lower()]
    by_cat = {}
    for t in free:
        by_cat.setdefault(t['category'], []).append(t)
    featured = sorted(free, key=lambda t: float(t.get('rating',0) or 0), reverse=True)[:12]
    sections = ''
    for cat, items in sorted(by_cat.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        sections += f'<h2>{cat}</h2><div class="content-hub-grid">' + ''.join(card(t) for t in sorted(items, key=lambda x: float(x.get('rating',0) or 0), reverse=True)[:6]) + '</div>'
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="The best free AI tools by category: writing, research, meetings, automation, creative media, coding, and productivity. Verified pricing from official sources."><title>Best Free AI Tools — 33 Free-Tier Picks | AIToolsEssentials</title><link rel="canonical" href="https://aitoolsessentials.com/free-ai-tools.html"><link rel="stylesheet" href="css/styles.css"></head><body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:820px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Free AI tools</p><h1>Start free. Upgrade only when limits hurt.</h1><p class="subhead">We found {len(free)} tools in the directory with a free tier or free self-hosted option. This hub groups them by job so you can test before paying.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card" style="margin-bottom:34px"><span>Quick answer</span><h2 style="font-size:30px">The best free AI tool depends on the constraint.</h2><p>For general work, start with ChatGPT, Claude, Gemini, or Perplexity. For visuals, compare Canva AI, Adobe Firefly, Leonardo AI, and Midjourney's trial availability. For automation, Make and Zapier are easiest; n8n is the free self-hosted option if you can run it yourself.</p><p>Free tiers change quickly. Every linked review includes an official-pricing block and verification date.</p></div><h2>Top free-tier picks</h2><div class="content-hub-grid">{''.join(card(t) for t in featured)}</div>{sections}<h2>How to use free tiers well</h2><ul><li>Test your real workflow — not a demo prompt.</li><li>Track the limit that stops you: messages, minutes, credits, exports, or team seats.</li><li>Upgrade only where the free limit breaks paid work.</li><li>For client or student data, check privacy terms before uploading anything sensitive.</li></ul><p><a class="button button-blue" href="/tool-finder.html">Use the tool finder</a> <a class="button button-dark" href="/research/ai-tool-pricing-2026.html" style="margin-left:8px">See pricing research</a></p></div></section></main><section class="newsletter-panel premium-conversion-panel"><div><span>Premium research layer</span><h2>Want the member-only decision archive?</h2><p>Premium adds monthly research briefs, stack-audit templates, weekly checklists, tool-change alerts, hands-on protocols, ROI calculators, and member-requested deep dives through Whop.</p><p class="affiliate-inline">7-day free trial · then $12/month · code LAUNCH50 for 50% off first paid month · Whop handles billing and access · research and strategy only.</p></div><div class="newsletter-actions"><a class="button button-blue" href="https://whop.com/checkout/ch_DKm5yxA1OBXoDru/" rel="external noopener">Subscribe on Whop</a><a class="button button-dark" href="/premium/">See Premium library</a><a class="button button-dark" href="/newsletter/">Read Keep/Cut Weekly</a><a class="button button-dark" href="/premium/faq.html">FAQ</a></div></section>{FOOTER}<script src="js/site.js" defer></script><script src="js/analytics.js" defer></script></body></html>'''
    (root/'free-ai-tools.html').write_text(page)
    return 1

def generate_alternatives(root: Path, tools):
    slug_to_tool = {t['slug']: t for t in tools}
    groups = [
        ('ChatGPT alternatives', 'General assistants for writing, research, coding help, and everyday work.', ['claude','gemini','perplexity','grok','deepseek','meta-ai']),
        ('Jasper alternatives', 'Marketing and copy tools when you need campaign copy, brand voice, or lower-cost drafting.', ['copy-ai','chatgpt','claude','grammarly','canva-ai']),
        ('Zapier alternatives', 'Automation platforms for connecting apps, routing approvals, and orchestrating workflows.', ['make','n8n','airtable-ai']),
        ('Midjourney alternatives', 'Image and creative generation tools for social, ads, product concepts, and design exploration.', ['leonardo-ai','adobe-firefly','canva-ai']),
        ('Perplexity alternatives', 'Research tools and assistants for source-backed answers and knowledge work.', ['chatgpt','claude','you-com','gemini']),
        ('Notion AI alternatives', 'Knowledge work and workspace AI when you need docs, notes, and team workflows.', ['microsoft-copilot','chatgpt','claude','airtable-ai']),
        ('ElevenLabs alternatives', 'Voice and media workflow tools for creators, podcasts, and repurposing.', ['descript','allvideoai','heygen','synthesia']),
    ]
    blocks=''
    for title, desc, slugs in groups:
        items=[slug_to_tool[s] for s in slugs if s in slug_to_tool]
        blocks += f'<section style="margin:54px 0"><h2>{title}</h2><p>{desc}</p><div class="content-hub-grid">' + ''.join(card(t) for t in items) + '</div></section>'
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Find alternatives to ChatGPT, Jasper, Zapier, Midjourney, Perplexity, Notion AI, and ElevenLabs using verified AI tool reviews."><title>AI Tool Alternatives — Better Fits by Workflow | AIToolsEssentials</title><link rel="canonical" href="https://aitoolsessentials.com/alternatives/index.html"><link rel="stylesheet" href="../css/styles.css"></head><body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:820px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Alternatives hub</p><h1>Don't just pick the famous tool. Pick the fit.</h1><p class="subhead">Use these alternatives lists when the default tool is too expensive, too broad, too limited, or simply wrong for the workflow.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>How to use this page</span><p>Start with the tool you already know, then compare alternatives by workflow and pricing model. Each card links to a full review with official-source pricing verification.</p></div>{blocks}<p><a class="button button-blue" href="/tool-finder.html">Use the tool finder</a> <a class="button button-dark" href="/comparisons/best-ai-tools.html" style="margin-left:8px">See best AI tools</a></p></div></section></main>{FOOTER}<script src="../js/site.js" defer></script><script src="../js/analytics.js" defer></script></body></html>'''
    out=root/'alternatives'/'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    return 1

def generate(root: Path) -> int:
    tools=json.loads((root/'data/tools.json').read_text())
    return generate_free(root, tools)+generate_alternatives(root, tools)

if __name__ == '__main__':
    print(generate(Path(__file__).resolve().parent.parent))
