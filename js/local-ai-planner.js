(() => {
  const form = document.querySelector('#local-ai-planner');
  const result = document.querySelector('#planner-result');
  if (!form || !result) return;
  const esc = (value) => String(value).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const recommendations = {
    apple: {name:'Apple Silicon desktop', link:'../hardware/mac-mini-m5-pro.html', text:'A unified-memory Mac mini M5 Pro is the compact Apple path. Prefer 48GB or 64GB when local models are central; 32GB is more comfortable for smaller models and agent/UI work.'},
    cuda: {name:'NVIDIA discrete-GPU workstation', link:'../hardware/nvidia-rtx-5090-workstation.html', text:'A CUDA workstation is the clearest fit when dedicated VRAM, NVIDIA tooling, and local generation performance matter. Budget for PSU, case clearance, cooling, and system RAM.'},
    gateway: {name:'Low-power gateway host', link:'../hardware/raspberry-pi-5-gateway.html', text:'A Raspberry Pi 5 or small Linux host can run the gateway/control plane while models run in the cloud or on a separate inference machine.'},
    studio: {name:'High-memory Apple workstation', link:'../hardware/mac-studio-m5-ultra.html', text:'A high-memory Mac Studio is the Apple option when very large models or several concurrent local workloads justify the cost. Validate the exact runtime and model before purchase.'}
  };
  function submit(event) {
    event.preventDefault();
    const model = Number(document.querySelector('#planner-model').value);
    const bits = Number(document.querySelector('#planner-quant').value);
    const concurrency = Number(document.querySelector('#planner-concurrency').value);
    const workload = document.querySelector('#planner-workload').value;
    const priority = document.querySelector('#planner-priority').value;
    const gatewayOnly = workload === 'gateway' || model === 0;
    const weightGb = model ? model * (bits / 8) * 1.08 : 0;
    const headroom = gatewayOnly ? 3 : (workload === 'both' ? 8 : 5);
    const estimated = Math.ceil((weightGb + headroom) * concurrency);
    let tier, rec;
    if (gatewayOnly && priority === 'budget') { tier = 'Gateway tier'; rec = recommendations.gateway; }
    else if (estimated >= 70 || (model >= 70 && concurrency > 1)) { tier = 'High-memory tier'; rec = recommendations.studio; }
    else if (priority === 'cuda' || priority === 'privacy' && model >= 32) { tier = 'Discrete-GPU tier'; rec = recommendations.cuda; }
    else { tier = 'Compact local tier'; rec = recommendations.apple; }
    const modelLine = gatewayOnly ? 'Cloud-model or gateway-first plan' : `${model}B-class model at ${bits}-bit precision`;
    const services = gatewayOnly ? 'OpenClaw or Hermes Agent as the control plane; use a cloud provider or remote inference backend.' : 'Ollama or LM Studio for the model runtime; Open WebUI for a browser workspace; Hermes Agent or OpenClaw only after permissions and network boundaries are reviewed.';
    result.hidden = false;
    result.innerHTML = `<div class="planner-result-head"><span class="kicker">Your explainable brief</span><h2>${esc(tier)}</h2><p>Planning estimate: <strong>${esc(gatewayOnly ? 'No local model memory required' : `about ${estimated}GB of system/unified memory or usable VRAM headroom`)}</strong> for ${esc(modelLine)}${concurrency > 1 ? ' with concurrent workloads' : ''}.</p></div><div class="planner-result-grid"><div><h3>Recommended direction</h3><p>${esc(rec.text)}</p><a class="button button-blue" href="${esc(rec.link)}">Review hardware evidence →</a></div><div><h3>Suggested service stack</h3><p>${esc(services)}</p><p class="planner-caveat">The estimate excludes exact KV-cache behavior, runtime overhead, model-specific kernels, OS memory, and thermal throttling. Test the exact model before committing.</p></div></div><div class="planner-result-foot"><strong>Next test:</strong> use the same prompt, context size, and output target in the chosen runtime; record cold start, tokens/sec, memory use, quality, and machine responsiveness.</div>`;
    result.scrollIntoView({behavior:'smooth', block:'start'});
  }
  form.addEventListener('submit', submit);
})();
