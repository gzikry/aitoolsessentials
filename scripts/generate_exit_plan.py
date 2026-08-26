#!/usr/bin/env python3
"""Inject an honest portability/exit-plan module into every tool review."""
from pathlib import Path
import re

START='<!-- AIT EXIT PLAN START -->'
END='<!-- AIT EXIT PLAN END -->'

def postprocess(root: Path, tools: list[dict]) -> int:
    changed=0
    for page in sorted((root/'tools').glob('*/index.html')):
        slug=page.parent.name
        tool=next((t for t in tools if t.get('slug')==slug),{})
        name=tool.get('name',slug)
        category=tool.get('category','')
        block=f'''\n{START}<section class="exit-plan-module"><div class="exit-plan-copy"><span class="evidence-label">Portability · before you subscribe</span><h2>Make sure you can leave.</h2><p>Good fit today does not mean low lock-in tomorrow. Before paying for {name}, test the exit path against your real workflow. We do not infer portability from marketing copy; verify the vendor's current export, retention, and cancellation rules.</p></div><div class="exit-plan-grid"><article><strong>Export one real result</strong><p>Can you download the files, text, assets, transcripts, automations, or settings your workflow creates?</p></article><article><strong>Separate reusable work</strong><p>Which prompts, templates, source files, contacts, or data remain usable outside the product?</p></article><article><strong>Find the trapped layer</strong><p>What history, credits, integrations, team knowledge, or proprietary format might not transfer?</p></article><article><strong>Test cancellation</strong><p>Confirm the retention period, downgrade behavior, renewal date, and whether cancellation deletes anything.</p></article></div><p class="exit-plan-links"><a href="/evidence/#evidence-{slug}">Check {name}'s evidence row →</a><a href="/guides/switch-guides/">Read switching guides →</a></p></section>{END}\n'''
        text=page.read_text()
        text=re.sub(re.escape(START)+r'.*?'+re.escape(END)+'\n?', '', text, flags=re.S)
        if '</main>' not in text: continue
        page.write_text(text.replace('</main>',block+'</main>',1)); changed+=1
    return changed
