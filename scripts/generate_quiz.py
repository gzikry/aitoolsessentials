#!/usr/bin/env python3
"""Generate the public coding-assistant keep/cut quiz.

This was authored as a linkable marketing asset but lived under /marketing/,
which is a working directory and should never be in the sitemap. The quiz is
published at a real public URL so it can be linked and promoted.
"""
from __future__ import annotations

from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
SLUG = "coding-assistant-keep-cut"

HEADER = (
    '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span>'
    '<span>AIToolsEssentials</span></a><nav class="nav-links">'
    '<a href="/tools/index.html">Tools</a>'
    '<a href="/comparisons/best-ai-tools.html">Best AI tools</a>'
    '<a href="/categories/index.html">Categories</a>'
    '<a href="/articles/index.html">Guides</a>'
    '<a href="/benchmarks/">Benchmarks</a>'
    '</nav><a class="nav-cta" href="/premium/">Paid Premium</a></header>'
)

FOOTER = (
    '<div id="share-row" hidden></div>\n'
    '<footer class="footer"><span>© 2026 AIToolsEssentials</span>'
    '<a href="/advertise/index.html" rel="nofollow">Advertise</a>'
    '<a href="/submit-tool.html" rel="nofollow">Submit a tool</a>'
    '<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>'
    '<a href="/legal/about.html">About</a>'
    '<a href="/legal/privacy.html">Privacy</a>'
    '<a href="/legal/terms.html">Terms</a>'
    f'<a href="mailto:{EMAIL}">Contact</a></footer>'
)

QUIZ_STYLE = """
.quiz-shell { max-width: 760px; margin: 0 auto; padding: 40px 22px 60px; }
.quiz-card { background: #fff; border-radius: 16px; padding: 30px; box-shadow: rgba(0,0,0,.05) 0 8px 24px; }
.quiz-badge { display: inline-block; padding: 4px 12px; background: #eef0ff; color: #3d46a8; border-radius: 999px; font-size: 12px; font-weight: 700; margin-bottom: 14px; }
.quiz-question { font-size: 18px; font-weight: 700; margin: 22px 0 14px; }
.quiz-options { display: grid; gap: 12px; }
.quiz-option { padding: 14px 18px; border: 2px solid #e4e5ee; border-radius: 12px; cursor: pointer; transition: border-color .2s ease, background .2s ease, color .2s ease; font-weight: 600; color: #1d1d1f; background: #fff; text-align: left; font: inherit; font-weight: 600; }
.quiz-option:hover, .quiz-option:focus-visible { border-color: #5e6ad2; background: #f4f5ff; }
.quiz-option.selected { border-color: #3d46a8; background: #3d46a8; color: #fff; }
.quiz-result { display: none; padding: 24px; background: #f4f5ff; border-radius: 12px; margin-top: 26px; }
.quiz-result.show { display: block; }
.quiz-result h3 { font-size: 21px; margin-bottom: 10px; color: #1d1d1f; }
.quiz-result p { margin-bottom: 12px; color: #1d1d1f; }
.quiz-savings { font-weight: 700; color: #3d46a8; }
.quiz-source { font-size: 13px; color: #6e6e73; margin-top: 16px; }
"""

QUIZ_SCRIPT = """
(function () {
  var answers = {};
  var verdict = document.getElementById('quiz-verdict');
  var explanation = document.getElementById('quiz-explanation');
  var savings = document.getElementById('quiz-savings');
  var result = document.getElementById('quiz-result');
  var quiz = document.getElementById('quiz');
  if (!quiz || !result) return;
  function show(step) {
    var q = document.getElementById('quiz-q' + step);
    var o = document.getElementById('quiz-opts' + step);
    if (q) q.style.display = 'block';
    if (o) o.style.display = 'grid';
  }
  function handleSelect(step, value, el) {
    answers[step] = value;
    el.parentElement.querySelectorAll('.quiz-option').forEach(function (b) { b.classList.remove('selected'); });
    el.classList.add('selected');
    if (step === 3) { showResult(); } else { show(step + 1); }
  }
  function showResult() {
    var workflow = answers[1];
    var budget = answers[3];
    var v = '';
    var e = '';
    var s = '';
    if (workflow === 'vscode') {
      v = 'Keep Copilot Pro ($10/month)';
      e = "If you are primarily in VS Code or JetBrains and want better completions without switching editors, Copilot Pro does the job. You likely do not need Cursor on top of it.";
      s = '$20 to $120/month (drop Cursor Pro, drop Claude Max)';
    } else if (workflow === 'agent') {
      v = 'Keep Claude Pro ($20/month) or Max ($100/month)';
      e = 'For terminal agent work (Claude Code, Codex), the Claude API or Max tier is purpose-built. Copilot and Cursor overlap here: they are completion tools, not agent tools.';
      s = '$10 to $30/month (drop Copilot Pro, review whether you still need Cursor)';
    } else if (workflow === 'native') {
      v = 'Keep Cursor Pro ($20/month)';
      e = 'If you want an AI-native editor with multi-file context and agent modes, Cursor is the clear choice. Copilot becomes redundant because Cursor completions cover the same ground.';
      s = '$10 to $100/month (drop Copilot Pro, drop Claude Max if you are not doing terminal agent work)';
    }
    if (budget === 'tight') {
      e += ' Given your budget, pick one tool per job and cancel the rest.';
    } else if (budget === 'flexible') {
      e += ' With your budget you could keep two tools if they serve meaningfully different jobs, but only if you use both weekly.';
    }
    verdict.textContent = v;
    explanation.textContent = e;
    savings.textContent = s;
    quiz.style.display = 'none';
    result.classList.add('show');
  }
  quiz.querySelectorAll('.quiz-option').forEach(function (el) {
    el.addEventListener('click', function () { handleSelect(Number(el.dataset.step), el.dataset.val, el); });
  });
})();
"""


def build_question(step: int, text: str, options: list[tuple[str, str]], hidden: bool) -> str:
    style = ' style="display:none"' if hidden else ''
    buttons = "".join(
        f'<button class="quiz-option" type="button" data-step="{step}" data-val="{value}">{label}</button>'
        for value, label in options
    )
    return (
        f'<div class="quiz-question" id="quiz-q{step}"{style}>{step}. {text}</div>'
        f'<div class="quiz-options" id="quiz-opts{step}"{style}>{buttons}</div>'
    )


QUIZ_LINK_MARK_START = "<!-- AIT QUIZ LINK START -->"
QUIZ_LINK_MARK_END = "<!-- AIT QUIZ LINK END -->"

# Public pages where a keep/cut quiz is the natural next step.
QUIZ_LINK_TARGETS = (
    "tools/index.html",
    "articles/cursor-vs-copilot-which-to-pay-for.html",
    "articles/claude-code-vs-cursor-vs-copilot.html",
    "articles/best-ai-coding-tools.html",
    "articles/is-cursor-worth-it.html",
    "articles/is-github-copilot-worth-it.html",
    "categories/Development/index.html",
)


def link_quiz(root: Path) -> int:
    """Link the quiz from related public pages so it is not an orphan."""
    block = (
        f'\n{QUIZ_LINK_MARK_START}\n'
        '<section class="score-card related-next-steps"><span>Free quiz</span>'
        '<h2>Paying for two coding assistants?</h2>'
        '<p>Answer three questions and get a keep/cut verdict for Copilot Pro, Cursor Pro, and Claude Max.</p>'
        f'<p><a class="button button-blue" href="/quiz/{SLUG}.html">Take the keep/cut quiz</a>'
        '<a class="button button-blue" href="/stack-audit.html" style="margin-left:8px">Run the free Stack Audit</a></p>'
        f'</section>\n{QUIZ_LINK_MARK_END}\n'
    )
    linked = 0
    for rel in QUIZ_LINK_TARGETS:
        path = root / rel
        if not path.exists():
            continue
        html = path.read_text()
        if QUIZ_LINK_MARK_START in html:
            continue
        if "</main>" not in html:
            continue
        path.write_text(html.replace("</main>", block + "</main>", 1))
        linked += 1
    return linked


def generate(root: Path) -> Path:
    out_dir = root / "quiz"
    out_dir.mkdir(exist_ok=True)
    questions = (
        build_question(1, "What is your primary coding workflow?", [
            ("vscode", "VS Code or JetBrains, and I want better completions"),
            ("agent", "Terminal agent, for Claude Code or Codex"),
            ("native", "AI-native editor, for Cursor or Windsurf"),
        ], hidden=False)
        + build_question(2, "How many hours a week do you code?", [
            ("light", "Under 10 hours, occasional coding"),
            ("medium", "10 to 30 hours, regular development"),
            ("heavy", "30+ hours, full-time coding"),
        ], hidden=True)
        + build_question(3, "What is your monthly AI tool budget?", [
            ("tight", "Tight, I want to cut spend"),
            ("moderate", "Moderate, under $40"),
            ("flexible", "Flexible, if the fit is real"),
        ], hidden=True)
    )

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Answer three questions and get a keep/cut verdict for overlapping coding AI subscriptions: Copilot Pro, Cursor Pro, and Claude Max.">
<title>Which coding assistant should you keep? — Free quiz | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/quiz/{SLUG}.html">
<link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css">
<meta property="og:title" content="Which coding assistant should you keep?">
<meta property="og:description" content="Three questions, one keep/cut verdict for overlapping coding AI subscriptions.">
<meta property="og:url" content="{DOMAIN}/quiz/{SLUG}.html">
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image">
<style>{QUIZ_STYLE}</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"Coding assistant keep/cut quiz","applicationCategory":"UtilityApplication","operatingSystem":"Web","url":"{DOMAIN}/quiz/{SLUG}.html","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}},"publisher":{{"@type":"Organization","name":"AIToolsEssentials","url":"{DOMAIN}/"}}}}</script>
</head>
<body>
{HEADER}
<main>
<section class="scene scene-dark"><div style="max-width:820px;margin:0 auto;padding:80px 24px 56px;text-align:center">
<p class="kicker">Free quiz · no login</p>
<h1>Which coding assistant should you keep?</h1>
<p class="subhead">Copilot Pro is $10. Cursor Pro is $20. Claude Max starts at $100. Stacked, that is $130 a month for overlapping coding work. Answer three questions for a keep/cut verdict.</p>
</div></section>
<section class="scene scene-light"><div class="quiz-shell">
<div class="quiz-card">
<span class="quiz-badge">Interactive quiz</span>
<div id="quiz">
{questions}
</div>
<div class="quiz-result" id="quiz-result">
<h3 id="quiz-verdict"></h3>
<p id="quiz-explanation"></p>
<p>Potential monthly savings: <span class="quiz-savings" id="quiz-savings"></span></p>
<p><a class="button button-blue" href="/stack-audit.html">Run the free Stack Audit on your whole stack</a></p>
<p><a class="button button-dark" href="/articles/cursor-vs-copilot-which-to-pay-for.html">Read the Cursor vs Copilot guide</a></p>
</div>
<p class="quiz-source">Verdicts use officially published plan prices checked against vendor pages. Verify current pricing before you cancel anything. Nothing you answer is submitted to a server.</p>
</div>
</div></section>
</main>
{FOOTER}
<script>{QUIZ_SCRIPT}</script>
<script src="../js/site.js" defer></script>
<script src="../js/cookie-consent.js" defer></script>
<script src="../js/analytics.js" defer></script>
</body>
</html>
'''
    out = out_dir / f"{SLUG}.html"
    out.write_text(html)
    return out


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    print(f"Generated quiz: {generate(root)}")
    print(f"Linked quiz from {link_quiz(root)} pages")
