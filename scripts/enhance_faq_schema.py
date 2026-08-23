#!/usr/bin/env python3
"""Add FAQPage structured data to comparison and audience-guide pages (SEO depth)."""
import json, re
from pathlib import Path

FAQS = {
    'cursor-vs-github-copilot.html': [
        ('Which is cheaper: Cursor or GitHub Copilot?',
         'GitHub Copilot Pro is $10/month; Cursor Pro is $20/month. Copilot also has a free tier with 2,000 completions per month. Verify current prices on official pricing pages — both vendors change plans regularly.'),
        ('Do Cursor or GitHub Copilot train on my code?',
         'Cursor states it will not use content to train models unless you explicitly agree, and offers Privacy Mode on free and paid plans. GitHub Copilot has a public statement that it does not use your code for training. Check each vendor\'s current privacy documentation before committing.'),
        ('Which is better for beginners?',
         'GitHub Copilot works inside editors many developers already use (VS Code, JetBrains), so adoption is lower friction. Cursor requires switching to its editor but gives deeper AI integration. Trial both on one real task before paying for either.'),
    ],
    'zapier-vs-make-vs-n8n.html': [
        ('Which automation tool is cheapest?',
         'It depends on your workflow shape. Zapier bills per task ($19.99+/mo annual for Professional), Make bills credits (~$12/mo at the 10k tier), n8n bills executions (€20/mo for 2,500 runs). Complex multi-step workflows are usually cheapest on n8n because steps inside a run are unlimited.'),
        ('Can I self-host any of these?',
         'Only n8n. It offers a free self-hosted community edition. Zapier and Make are cloud-only.'),
        ('Which is best for AI-powered automations?',
         'Check credit/task costs of AI steps specifically: Make charges more credits for AI modules, and Zapier counts AI steps as tasks. Model your actual scenario volume in each platform\'s calculator before choosing.'),
    ],
    'chatgpt-vs-gemini.html': [
        ('Is Gemini included with Google Workspace?',
         'Gemini capabilities are bundled into Workspace plans at different tiers, and Google sells Gemini as a standalone subscription too. Check Google\'s current Workspace pricing page for what your plan includes.'),
        ('Which has better benchmark scores?',
         'Both models appear high on public leaderboards like Arena Text, but ranks shift weekly and apply only to exact model versions tested. See our benchmarks hub for dated snapshots rather than treating either as "the winner."'),
    ],
    'claude-vs-perplexity.html': [
        ('Should I use Claude or Perplexity for research?',
         'They solve different halves: Perplexity finds and cites web sources; Claude analyzes long documents you supply and produces structured writing. Many researchers run both — search in Perplexity, deep analysis in Claude.'),
    ],
    'claude-vs-gemini.html': [
        ('Claude vs Gemini: which is better for long documents?',
         'Claude handles very long single documents with strong instruction adherence, making it a common choice for contract or report analysis. Gemini integrates with Google Drive and handles multimodal inputs. The right pick depends on where your material lives.'),
        ('Do Claude and Gemini cost the same?',
         'Both offer free tiers and paid plans around $20/month, but plan features and limits change often. Check the official pricing pages before deciding — our comparison page links both directly.'),
    ],
    'heygen-vs-synthesia.html': [
        ('Do HeyGen and Synthesia allow commercial use of videos?',
         'Rights differ by plan: HeyGen\'s terms give Free-plan output only a personal, non-commercial license, while paid Creator/Pro/Business users own their outputs. Synthesia\'s terms vary by plan tier too. Read the vendor\'s current terms for your specific plan before client delivery.'),
        ('Do these tools require consent for avatars?',
         'Yes — both platforms require consent for custom avatar creation and prohibit impersonating real people without permission. AI-origin disclosure is required where applicable under their terms.'),
    ],
}

def generate(root: Path) -> int:
    made = 0
    for fname, faqs in FAQS.items():
        for base in [root/'comparisons', root/'articles']:
            p = base/fname
            if not p.exists():
                continue
            s = p.read_text()
            if 'FAQPage' in s:
                continue
            entities = []
            visible = ''
            for q, a in faqs:
                entities.append(json.dumps({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}}))
                visible += f'<details><summary>{q}</summary><p>{a}</p></details>'
            schema = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
                      + ','.join(entities) + ']}</script>')
            block = f'<section class="scene scene-light"><article class="article-shell"><h2>Frequently asked questions</h2><div class="faq-list">{visible}</div></article></section>'
            # insert schema before </head> and FAQ section before </main>
            s = s.replace('</head>', schema + '</head>', 1)
            k = s.rfind('</main>')
            s = s[:k] + block + s[k:]
            p.write_text(s)
            made += 1
    return made

if __name__ == '__main__':
    print(generate(Path(__file__).resolve().parent.parent))
