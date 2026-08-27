#!/usr/bin/env python3
"""Subscribe page: Beehiiv embed when present, else FormSubmit capture."""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/updates/">Digests</a><a href="/articles/index.html">Guides</a><a href="/premium/">Premium</a></nav><a class="nav-cta" href="/premium/">Premium</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/privacy.html">Privacy</a></footer>'


def esc(s: object) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def capture_block(cfg: dict) -> str:
    embed = (cfg.get("embed_html") or "").strip()
    signup = (cfg.get("signup_url") or "").strip()
    if embed:
        return f'<div class="score-card"><span>Keep/Cut digest</span><h2>Get the free digest.</h2>{embed}</div>'
    if signup:
        src = esc(signup)
        return f'''<div class="score-card"><span>Keep/Cut digest</span><h2>Get the free digest.</h2>
<p>We email when recorded pricing, plans, or model lineups change enough to affect a keep/cut decision. Unsubscribe anytime.</p>
<p><a class="button button-blue" href="{src}" rel="noopener sponsored nofollow">Subscribe on Beehiiv</a></p>
<iframe src="{src}" title="Keep/Cut digest signup" loading="lazy" referrerpolicy="no-referrer-when-downgrade" style="width:100%;min-height:520px;border:0;border-radius:12px;background:#fff;margin-top:16px"></iframe>
<p class="affiliate-inline">If the form does not load, use the button above. Hosted by Beehiiv at aitoolsessentials.beehiiv.com.</p>
</div>'''
    action = esc(cfg.get("formsubmit_ajax") or "https://formsubmit.co/ajax/eb3d1bf5a35125c06383cafa247af931")
    subject = esc(cfg.get("subject") or "Keep/Cut digest signup")
    return f'''<div class="score-card"><span>Keep/Cut digest</span><h2>Get the free digest.</h2>
<p>We email when recorded pricing, plans, or model lineups change enough to affect a keep/cut decision. Unsubscribe anytime.</p>
<form id="digest-form" action="{action}" method="POST">
<input type="hidden" name="_subject" value="{subject}">
<input type="hidden" name="_template" value="table">
<label>Email <input type="email" name="email" required autocomplete="email" style="width:100%;margin:8px 0 16px;padding:12px;border-radius:10px;border:1px solid #ccc"></label>
<button class="button button-blue" type="submit">Subscribe</button>
<p class="affiliate-inline" id="digest-status"></p>
</form>
<script>
document.getElementById('digest-form').addEventListener('submit', function(e) {{
  e.preventDefault();
  var btn = this.querySelector('button');
  var st = document.getElementById('digest-status');
  btn.disabled = true;
  fetch(this.action, {{method:'POST', body: new FormData(this), headers: {{Accept:'application/json'}}}})
    .then(function(r) {{ return r.json(); }})
    .then(function(data) {{
      if (data.success === true || data.success === 'true') {{ st.textContent = 'Check your inbox to confirm.'; }}
      else {{ throw new Error(data.message || 'Could not subscribe'); }}
    }})
    .catch(function(err) {{ st.textContent = err.message; btn.disabled = false; }});
}});
</script></div>'''


def generate(root: Path) -> int:
    cfg = json.loads((root / "data/newsletter.json").read_text())
    desc = cfg.get("description") or "Free keep/cut digest for AI tool pricing and model changes."
    block = capture_block(cfg)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(desc)}"><title>Subscribe — Keep/Cut digest | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/subscribe/"><link rel="stylesheet" href="/css/styles.css"></head><body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Free email</p><h1>The keep/cut digest.</h1><p class="subhead">{esc(desc)}</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">{block}
<p>Latest public digest: <a href="/updates/2026-08.html">August 2026</a>. Paid <a href="/premium/">Premium</a> is a separate Whop membership (7-day trial, code LAUNCH50).</p>
</div></section>
</main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
    out = root / "subscribe"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page)
    return 1


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parent.parent))
