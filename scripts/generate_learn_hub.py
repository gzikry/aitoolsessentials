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
    ('chatgpt-free-vs-plus.html', 'ChatGPT free vs Plus: what the limits actually are', 'What OpenAI officially publishes about plan structure — without unofficial dollar figures.'),
    ('perplexity-vs-google.html', 'Is Perplexity better than Google?', 'When a cited research assistant is the better first stop than a general search page.'),
    ('can-i-cancel-ai-subscriptions.html', 'Can I cancel AI subscriptions anytime?', 'How to read cancel, downgrade, and annual-prepay terms before you lock a stack.'),
    ('do-ai-tools-work-offline.html', 'Do AI tools work offline?', 'Which AI tools run locally, which need the cloud, and how to choose offline-first AI.'),
    ('what-happens-to-my-data-when-i-delete-ai-account.html', 'What happens to my data when I delete an AI account?', 'Deletion, retention, training, and export questions to ask before canceling.'),
    ('which-ai-tool-writes-best-in-another-language.html', 'Which AI tool writes best in another language?', 'How to compare multilingual writing tools without trusting a mismatched benchmark.'),
    ('is-claude-worth-it.html', 'Is Claude worth it?', 'Who benefits from a paid Claude plan — based on verified plan structure, not hype.'),
    ('is-perplexity-worth-it.html', 'Is Perplexity worth it?', 'When the free tier is enough for cited research and when paid is rational.'),
    ('is-cursor-worth-it.html', 'Is Cursor worth it?', 'Who benefits from a paid Cursor plan for AI-assisted coding.'),
    ('is-grok-worth-it.html', 'Is Grok worth it?', 'When paid Grok through X earns its keep for real-time AI and agents.'),
    ('is-gemini-worth-it.html', 'Is Gemini worth it?', 'Who benefits from a paid Google Gemini plan inside Workspace.'),
    ('is-notion-ai-worth-it.html', 'Is Notion AI worth it?', 'When AI inside your knowledge base earns its cost vs a separate assistant.'),
    ('best-ai-tools-for-beginners.html', 'Best AI tools for beginners', 'A free-first starter stack for practical AI results without buying five subscriptions.'),
    ('launch-ai-business-whop-blueprints.html', 'How to launch an AI business with Whop Blueprints', 'Deploy a working business with products, pricing, website, and checkout in one command.'),
    ('how-to-cut-ai-tool-subscriptions.html', 'How to cut AI tool subscriptions', 'Keep/cut/trial framework for overlapping AI stacks — free first, full matrix when needed.'),
    ('ai-stack-audit-checklist.html', 'AI stack audit checklist', 'Map every paid tool, spot overlap, and decide keep/cut/trial before renewal.'),
    ('chatgpt-vs-claude-vs-grok-vs-gemini.html', 'ChatGPT vs Claude vs Grok vs Gemini', 'Choose a primary assistant with identical real tasks, not brand preference.'),
    ('is-an-ai-tool-membership-worth-it.html', 'Is an AI tool research membership worth it?', 'When $12/month research beats another SaaS seat — and when free is enough.'),
    ('ai-invoicing-admin-stack-consultants.html', 'AI invoicing stack for consultants', 'Free-first invoices, reminders, and weekly admin without five overlapping tools.'),
    ('evaluating-ai-coding-tools-team-rollout.html', 'Evaluating AI coding tools for a team', 'Security-first rollout checklist so you do not buy two IDEs.'),
    ('ai-image-rights-commercial-use.html', 'AI image rights for commercial use', 'What to check before using Midjourney or Leonardo output in client work.'),
    ('how-to-cancel-ai-tools-before-renewal.html', 'How to cancel AI tools before renewal', '14-day process to cancel unused seats without losing the weekly workflow.'),
    ('cursor-vs-copilot-which-to-pay-for.html', 'Cursor vs Copilot: which to pay for', 'Pick one paid coding assistant with a real bugfix, not two overlapping seats.'),
    ('make-vs-zapier-which-to-pay-for.html', 'Make vs Zapier: which to pay for', 'Map one workflow and count tasks vs operations before annual billing.'),
    ('pick-one-ai-meeting-notes-tool.html', 'Pick one AI meeting notes tool', 'Grade Fireflies, Otter, and Fathom on a real meeting, then keep one.'),
    ('gamma-vs-canva-which-for-decks.html', 'Gamma vs Canva: which for decks', 'Pick one paid deck tool with the same real brief.'),
    ('heygen-vs-synthesia-which-to-pay-for.html', 'HeyGen vs Synthesia: which to pay for', 'Keep one avatar video tool after the same 60-second script.'),
    ('perplexity-vs-chatgpt-for-research.html', 'Perplexity vs ChatGPT for research', 'Pay for sources or for drafting, not both by default.'),
    ('elevenlabs-vs-descript-which-for-audio.html', 'ElevenLabs vs Descript: which for audio', 'Voice generation vs transcript editing. Pick the weekly job.'),
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
