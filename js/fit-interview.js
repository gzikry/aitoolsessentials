(()=>{
const dataEl=document.getElementById('fit-data');
if(!dataEl)return;
const TOOLS=JSON.parse(dataEl.textContent),form=document.getElementById('fit-form'),results=document.getElementById('fit-results'),cards=document.getElementById('fit-cards'),reset=document.getElementById('fit-reset');
const val=n=>form.querySelector(`input[name="${n}"]:checked`).value;
function score(t,a){let s=0,why=[];const text=t.summary+' '+t.best_for+' '+t.pros.join(' ')+' '+t.cons.join(' ');
 if(a.category==='all'||t.category===a.category){s+=42;why.push('matches your selected workflow')}else if(t.best_for.toLowerCase().includes(a.category.toLowerCase())){s+=18;why.push('overlaps your workflow')}
 if(a.priority==='quality'&&t.rating>=4.5){s+=18;why.push('has a strong editorial quality signal')}
 if(a.priority==='simplicity'&&/simple|easy|fast|friendly|straightforward/i.test(text)){s+=14;why.push('sounds aligned with a low-friction start')}
 if(a.priority==='control'&&/developer|api|integration|custom|agent|workflow|automation/i.test(text)){s+=14;why.push('supports a more controllable workflow')}
 if(a.priority==='portability'&&/export|open|api|integration|workflow/i.test(text)){s+=14;why.push('shows signals of a portable workflow')}
 if(a.budget==='free'&&/free/i.test(t.price)){s+=14;why.push('offers a free entry point')}
 if(a.budget==='low'&&/free|\$0|low|affordable/i.test(t.price+' '+t.summary)){s+=10;why.push('looks compatible with a cost-conscious trial')}
 if(a.budget==='flexible')s+=5;
 if(a.complexity==='low'&&!/developer|api|self-host|advanced|agent/i.test(text)){s+=10;why.push('does not lead with heavy technical setup')}
 if(a.complexity==='high'&&/developer|api|self-host|advanced|agent|integration/i.test(text)){s+=10;why.push('offers signals of deeper control')}
 if(a.risk==='evidence'){s+=6;why.push('can be checked through its dated review and evidence row')}
 if(a.risk==='value'&&/free|credit|usage|plan/i.test(t.price+' '+t.cons.join(' '))){s+=7;why.push('deserves a pricing-first comparison')}
 return {score:s,why:why.slice(0,3)};
}
function render(){const a={category:val('category'),priority:val('priority'),budget:val('budget'),complexity:val('complexity'),risk:val('risk')};const ranked=TOOLS.map(t=>({t,...score(t,a)})).sort((x,y)=>y.score-x.score).slice(0,3);cards.innerHTML=ranked.map((x,i)=>`<article class="fit-card"><div class="fit-rank">0${i+1}</div><div><span class="evidence-label">${x.t.category} · fit signal ${x.score}</span><h3><a href="/tools/${x.t.slug}/">${x.t.name}</a></h3><p>${x.t.best_for}.</p><ul>${x.why.map(w=>`<li>${w}</li>`).join('')}</ul><p class="fit-links"><a href="/tools/${x.t.slug}/">Read review →</a><a href="/evidence/#evidence-${x.t.slug}">Check evidence →</a></p></div></article>`).join('');form.hidden=true;results.hidden=false;window.scrollTo({top:results.offsetTop-30,behavior:'smooth'});}
form.addEventListener('submit',e=>{e.preventDefault();render()});reset.addEventListener('click',()=>{results.hidden=true;form.hidden=false;window.scrollTo({top:0,behavior:'smooth'})});
})();
