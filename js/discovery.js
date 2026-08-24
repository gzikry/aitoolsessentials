
(function(){
function initCopy(){document.querySelectorAll('[data-copy-current-url]').forEach(btn=>btn.addEventListener('click',()=>navigator.clipboard?.writeText(location.href).then(()=>{const old=btn.textContent;btn.textContent='Copied ✓';setTimeout(()=>btn.textContent=old,1400)})))}
document.addEventListener('DOMContentLoaded',initCopy);
})();
