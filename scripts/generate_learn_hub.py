#!/usr/bin/env python3
"""Generate the Learn hub: indexes all how-to and question-intent articles."""
import html as H
from pathlib import Path

LEARN = [
    ('how-to-choose-an-ai-tool.html', 'How to choose an AI tool', 'A repeatable decision framework: workflow fit, evidence, cost at volume, and policy terms.'),
    ('ai-tools-for-content-creation-workflow.html', 'The AI content creation workflow', 'From brief to publish: where AI tools fit in a blog pipeline, and where humans stay in the loop.'),
    ('ai-meeting-notes-workflow.html', 'Meeting notes to CRM, automatically', 'Capture calls, extract action items, and sync to your tools without manual admin.'),
    ('how-to-test-ai-tools-free-trials.html', 'Get real value from free trials', 'Test plans properly without surprise charges or wasted evaluation time.'),
    ('ai-prompting-basics-for-work.html', 'Prompting basics for non-engineers', 'Practical patterns that improve output quality in any chat assistant.'),
    ('when-not-to-use-ai.html', 'When not to use AI', 'Jobs where plain automation or humans beat AI tools — and how to tell before you pay.'),
    ('is-chatgpt-worth-it.html', 'Is ChatGPT worth it?', 'Who actually benefits from paid plans, based on verified plan limits — not hype.'),
    ('claude-vs-chatgpt-for-writing.html', 'Claude vs ChatGPT for writing', 'Where each assistant tends to shine in drafting and editing workflows.'),
    ('are-ai-tools-safe-for-business-data.html', 'Are AI tools safe for business data?', 'Training policies, retention, and the questions to ask before pasting client material.'),
    ('can-ai-write-my-blog-posts.html', 'Can AI write my blog posts?', 'What AI drafting does well, what it fails at, and the review work that remains yours.'),
    ('do-i-need-paid-ai-plans.html', 'Do I need paid AI plans?', 'When free tiers are enough and when limits start costing more than subscriptions.'),
    ('what-is-a-good-ai-tool-starter-stack.html', 'A good starter AI stack', 'The minimal first three tools for most knowledge workers, with upgrade triggers.'),
]

HEADER = '<header class="global-nav"><a class="brand" href="../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="../tools/index.html">Tools</a><a href="../comparisons/best-ai-tools.html">Best AI tools</a><a href="../categories/index.html">Categories</a><a href="../articles/index.html">Guides</a><a href="../benchmarks/">Benchmarks</a>\n</nav><a class="nav-cta" href="../legal/affiliate-disclosure.html">Disclosure</a></header>'
FOOTER = '''<footer class="footer">
    <span>© 2026 AIToolsEssentials</span>
    <a href="../advertise/index.html" rel="nofollow">Advertise</a>
    <a href="../submit-tool.html" rel="nofollow">Submit a tool</a>
    <a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
    <a href="mailto:contact@aitoolsessentials.com">Contact</a>
  <a href="../legal/about.html">About</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a><a href="../legal/corrections.html">Corrections</a></footer>'''


def generate(root: Path) -> int:
    cards = ''
    for f, t, d in LEARN:
        if (root/'articles'/f).exists():
            cards += (f'<article class="content-hub-card"><h3><a href="{f}">{H.escape(t)}</a></h3>'
                      f'<p>{H.escape(d)}</p><a class="text-link" href="{f}">Read guide</a></article>')
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Practical guides on choosing, testing, and working with AI tools — decision frameworks, workflows, and straight answers."><title>Learn — AI tool guides &amp; answers — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css"><link rel="stylesheet" href="../css/share.css">
<link rel="canonical" href="https://aitoolsessentials.com/articles/learn.html"></head><body>{HEADER}
<main><section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">Learn</p><h1>Decide better, then pick the tool.</h1><p class="subhead">Decision frameworks, workflows, and straight answers about AI tools — written to be checked against official sources.</p></div></section>
<section class="scene scene-light content-hub"><div class="content-hub-grid">{cards}</div></section></main><div id="share-row" hidden></div>
{FOOTER}<script src="../js/site.js" defer></script><script src="../js/analytics.js" defer></script></body></html>'''
    (root/'articles'/'learn.html').write_text(page)
    return len([1 for f,_,_ in LEARN if (root/'articles'/f).exists()])


if __name__ == '__main__':
    print(generate(Path(__file__).resolve().parent.parent))
