#!/usr/bin/env python3
"""Generate internal affiliate application tracker from verified official program data."""
import json
from pathlib import Path

def generate(root: Path) -> Path:
    data=json.loads((root/'data/affiliate_programs.json').read_text())
    rows=''
    for x in data['affiliate_programs']:
        rows+=f'''<tr><td><strong>{x['tool_slug']}</strong></td><td>{x['availability']}</td><td>{x['application_status']}</td><td>{x.get('network') or '—'}</td><td>{x.get('commission_note') or 'Not published / not applicable'}</td><td><a href="{x['official_program_url']}" target="_blank" rel="external noopener">Official source ↗</a></td><td>{x['notes']}</td></tr>'''
    queue=''.join(f'<li>{x}</li>' for x in data.get('priority_application_queue',[]))
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Affiliate Tracker — AIToolsEssentials Admin</title><link rel="stylesheet" href="../css/styles.css"></head><body><header class="global-nav"><a class="brand" href="../index.html">AIToolsEssentials Admin</a><nav class="nav-links"><a href="index.html">Admin home</a><a href="operations.html">Operations</a></nav></header><main><section class="review-hero scene scene-light"><p class="kicker light">Internal</p><h1>Verified affiliate opportunities</h1><p>Checked {data['checked_at']}. “Available” does not mean approved; no review CTA changes until a real tracking URL is received.</p></section><section class="benchmark-section"><h2>Priority application queue</h2><ol>{queue}</ol><div class="table-wrap"><table><thead><tr><th>Tool</th><th>Availability</th><th>Application</th><th>Network</th><th>Official commission note</th><th>Source</th><th>Notes</th></tr></thead><tbody>{rows}</tbody></table></div></section></main></body></html>'''
    out=root/'admin/affiliate-application-tracker.html';out.write_text(html);return out

if __name__=='__main__':generate(Path('/Users/georgezikry/aitoolessentials/site'))
