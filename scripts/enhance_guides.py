#!/usr/bin/env python3
"""Add transparent evidence/test-status panels to primary buyer guides."""
import json, re
from pathlib import Path

GUIDES = {
 'best-ai-assistants.html':'General AI Assistant',
 'best-ai-coding-tools.html':'Development',
 'best-ai-automation-tools.html':'Automation',
 'best-ai-image-tools.html':'Creative',
 'best-ai-video-tools.html':'Video',
 'best-ai-voice-tools.html':'Audio',
 'best-ai-research-tools.html':'Research',
 'best-ai-productivity-tools.html':'Productivity',
 'best-ai-meeting-tools.html':'Meetings',
 'best-ai-presentation-tools.html':'Presentations',
 'best-ai-app-builders.html':'Development',
}

def generate(root: Path) -> int:
    source_data=json.loads((root/'data/tool_sources.json').read_text())
    benchmark_data=json.loads((root/'data/benchmarks.json').read_text())
    benchmark_sources={x['id']:x for x in benchmark_data['sources']}
    changed=0
    for filename,category in GUIDES.items():
        p=root/'articles'/filename
        if not p.exists():continue
        h=p.read_text();original=h
        h=re.sub(r'<!-- AIT GUIDE EVIDENCE START -->.*?<!-- AIT GUIDE EVIDENCE END -->','',h,flags=re.S)
        ids=benchmark_data.get('coverage',{}).get(category,[])
        links=' · '.join(f'<a href="{benchmark_sources[i]["url"]}" target="_blank" rel="external noopener">{benchmark_sources[i]["name"]} [{i}] ↗</a>' for i in ids if i in benchmark_sources)
        if not links:links='<a href="../benchmarks/">No directly comparable category benchmark—see evidence policy</a>'
        panel=f'''<!-- AIT GUIDE EVIDENCE START --><div class="review-benchmark"><span class="evidence-label">Guide evidence status</span><h3>Official product sources checked {source_data['checked_at']}</h3><p>Prices and vendor-policy links are maintained in the individual reviews. External benchmarks apply only to exact model/configuration records: {links}</p><p>Independent same-task hands-on ranking: <strong>not yet published</strong>. Until retained test logs exist, ordering remains an editorial product assessment. <a href="../legal/testing-protocol.html">Testing protocol →</a></p></div><!-- AIT GUIDE EVIDENCE END -->'''
        idx=h.find('<h2>')
        if idx>=0:h=h[:idx]+panel+h[idx:]
        if h!=original:p.write_text(h);changed+=1
    print(f'Enhanced buyer-guide evidence on {changed} pages')
    return changed

if __name__=='__main__':generate(Path('/Users/georgezikry/aitoolessentials/site'))
