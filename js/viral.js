
(function(){
function params(){return new URLSearchParams(location.search)}
function find(slug){return (window.TOOLS||[]).find(t=>t.slug===slug)}
function stacks(role,budget,vibe){
 const base={freelancer:['chatgpt','perplexity','make','canva-ai','otter-ai'],agency:['jasper','copy-ai','canva-ai','make','descript'],developer:['cursor','github-copilot','claude','replit-ai','v0'],teacher:['chatgpt','gamma','canva-ai','perplexity','otter-ai'],creator:['descript','elevenlabs','canva-ai','midjourney','allvideoai'],'small-business':['chatgpt','make','zapier-ai','airtable-ai','microsoft-copilot'],researcher:['perplexity','claude','you-com','gemini','notion-ai']};
 let slugs=(base[role]||base.freelancer).slice();
 if(budget==='free') slugs=slugs.filter(s=>{let t=find(s); return t && /free/i.test(t.price||'')}).concat(['chatgpt','claude','gemini','perplexity','canva-ai','n8n']);
 if(vibe==='technical') slugs=['n8n','cursor','github-copilot','claude','airtable-ai'].concat(slugs);
 if(vibe==='low-friction') slugs=['chatgpt','canva-ai','zapier-ai','perplexity','otter-ai'].concat(slugs);
 const seen=[]; return slugs.filter(s=>find(s)&&!seen.includes(s)&&seen.push(s)).slice(0,5).map(find);
}
function card(t){return `<article class="content-hub-card"><span>${t.category} · ${t.price||''}</span><h3><a href="/tools/${t.slug}/">${t.name}</a></h3><p>${t.summary||''}</p><p><strong>Best for:</strong> ${t.best_for||''}</p><a class="button button-blue small" href="/tools/${t.slug}/">Read review</a></article>`}
function renderStack(){
 if(!window.TOOLS||!document.getElementById('stackResult')) return;
 const p=params(); ['role','budget','vibe'].forEach(id=>{if(p.get(id)&&document.getElementById(id)) document.getElementById(id).value=p.get(id)});
 const role=document.getElementById('role').value,budget=document.getElementById('budget').value,vibe=document.getElementById('vibe').value;
 const result=stacks(role,budget,vibe); const url=new URL(location.href); url.search=`?role=${role}&budget=${budget}&vibe=${vibe}`; history.replaceState(null,'',url);
 document.getElementById('stackResult').innerHTML=`<span>Your shareable stack</span><h2>${role.replace('-',' ')} · ${budget} · ${vibe}</h2><div class="content-hub-grid">${result.map(card).join('')}</div><p><button class="button button-blue" id="shareNative">Share stack</button><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a></p>`;
 const share=document.getElementById('shareNative'); if(share) share.onclick=()=>{navigator.share?navigator.share({title:document.title,url:location.href}):navigator.clipboard.writeText(location.href).then(()=>share.textContent='Copied ✓')};
}
function renderCost(){
 if(!window.COST_TOOLS||!document.getElementById('costToolList')) return;
 const list=document.getElementById('costToolList'), summary=document.getElementById('costSummary'), team=document.getElementById('teamSize');
 function est(t){let p=(t.price||'').toLowerCase(); if(p.includes('free self-hosted')) return 0; if(p.includes('free')) return 20; return 35}
 function update(){let selected=[...document.querySelectorAll('[data-cost]:checked')].map(i=>COST_TOOLS.find(t=>t.slug===i.value)); let seats=Math.max(1,Number(team.value||1)); let monthly=selected.reduce((a,t)=>a+est(t)*seats,0); summary.innerHTML=`<span>Estimated monthly stack cost</span><h2>$${monthly}/mo</h2><p>${selected.length} tools · ${seats} seat${seats===1?'':'s'} · rough planning estimate. Verify current vendor pricing before paying.</p>`}
 list.innerHTML=COST_TOOLS.map(t=>`<article class="content-hub-card"><span>${t.category} · ${t.price||''}</span><h3>${t.name}</h3><p>${t.summary||''}</p><label><input type="checkbox" data-cost value="${t.slug}"> Add to estimate</label></article>`).join('');
 list.addEventListener('change',update); team.addEventListener('input',update); update();
}
document.addEventListener('DOMContentLoaded',function(){document.getElementById('generateStack')?.addEventListener('click',renderStack);document.getElementById('copyStack')?.addEventListener('click',()=>navigator.clipboard.writeText(location.href));renderStack();renderCost();});
})();
