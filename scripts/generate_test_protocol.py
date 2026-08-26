#!/usr/bin/env python3
"""Inject a repeatable real-task test protocol into every tool review."""
from pathlib import Path
import html,re
START='<!-- AIT TEST PROTOCOL START -->'; END='<!-- AIT TEST PROTOCOL END -->'
def esc(x): return html.escape(str(x or ''))
def postprocess(root: Path, tools: list[dict]) -> int:
    changed=0
    for page in sorted((root/'tools').glob('*/index.html')):
        slug=page.parent.name; t=next((x for x in tools if x.get('slug')==slug),{})
        name=t.get('name',slug); best=t.get('best_for',''); checklist=t.get('trial_checklist','Use one real task from your workflow and compare the result with an alternative.')
        block=f'''\n{START}<section class="test-protocol-module"><span class="evidence-label">Repeatable evaluation · before you pay</span><h2>Run the same job, not a demo.</h2><p>Use one representative {esc(best.lower().rstrip('.'))} task and run it through every finalist. The point is not to produce a fake benchmark; it is to expose the time, quality, retries, review work, and cost your workflow actually creates.</p><div class="test-protocol-grid"><article><strong>01 · Same input</strong><p>Use the same source material, prompt, files, constraints, and success criteria for each tool.</p></article><article><strong>02 · Measure time</strong><p>Record setup time, time to first usable result, and time spent fixing or editing the output.</p></article><article><strong>03 · Score the result</strong><p>Rate quality, consistency, control, and reviewer effort from 1–5. Keep the notes, not just the average.</p></article><article><strong>04 · Price the run</strong><p>Record credits, seats, limits, retries, and any human review cost required to finish the task.</p></article></div><details class="test-protocol-script"><summary>Tool-specific trial checklist for {esc(name)}</summary><p>{esc(checklist)}</p></details><p class="test-protocol-links"><a href="/decision-brief.html">Generate a comparison brief →</a><a href="/resources/">Download buyer worksheets →</a></p></section>{END}\n'''
        text=page.read_text(); text=re.sub(re.escape(START)+r'.*?'+re.escape(END)+'\n?','',text,flags=re.S)
        anchor='<!-- AIT EXIT PLAN START -->'
        if anchor in text: text=text.replace(anchor,block+anchor,1)
        elif '</main>' in text: text=text.replace('</main>',block+'</main>',1)
        else: continue
        page.write_text(text); changed+=1
    return changed
