#!/usr/bin/env python3
"""Generate the 6 question-intent FAQ articles (concise, evidence-first)."""
import html as H
from pathlib import Path

ARTICLES = {
 'is-chatgpt-worth-it.html': {
  'title':'Is ChatGPT worth it?','kicker':'Straight answer','desc':'Who actually benefits from a paid ChatGPT plan, based on verified plan structure — not hype.',
  'body':'''
<p><strong>Short answer:</strong> worth it if you use it several times a week for work output; not worth it for occasional questions. The free tier is genuinely capable.</p>
<h2>What paying actually buys</h2>
<p>OpenAI lists Free, Go, Plus, Pro, Business, and Enterprise plans. Paid tiers primarily buy higher usage limits, priority access to newer models, and advanced features (deeper research modes, higher file limits). Exact prices and limits change often — check OpenAI's official pricing page before deciding.</p>
<h2>You probably don't need paid if…</h2>
<ul><li>You ask a few questions daily and wait times don't bother you</li><li>Your tasks are short drafts, summaries, or quick explanations</li><li>You're evaluating whether AI fits your workflow at all</li></ul>
<h2>Paid starts earning its keep when…</h2>
<ul><li>A free-tier limit interrupts real work more than once a week</li><li>You need consistent access during peak hours for deadlines</li><li>Advanced data analysis or long-document work is routine</li></ul>
<h2>How to decide in one week</h2>
<p>Use the free tier on your three most common real tasks. Note every time you hit a limit. If that happens five-plus times, do the math: an hour of your time vs roughly $20/month. Our <a href="how-to-test-ai-tools-free-trials.html">free-trial testing guide</a> walks the full process.</p>
<p class="monetization-note">Pricing verified against official sources August 21, 2026. Verify current plans before purchasing.</p>'''},
 'claude-vs-chatgpt-for-writing.html': {
  'title':'Claude vs ChatGPT for writing','kicker':'Versus','desc':'Where each assistant tends to shine for drafting, editing, and long-form work.',
  'body':'''
<p>Both are excellent writers, and neither is universally "better." The honest pattern we see from their design positions:</p>
<h2>Claude's typical strengths</h2>
<ul><li>Long documents: analyzing 50+ page inputs without losing thread</li><li>Natural prose that needs less "AI de-sanding" during edits</li><li>Instruction adherence on style guides and tone constraints</li></ul>
<h2>ChatGPT's typical strengths</h2>
<ul><li>Breadth: images, files, web browsing, and voice in one place</li><li>Structured formats: tables, outlines, multi-section drafts</li><li>Ecosystem: custom GPTs let teams reuse role-specific setups</li></ul>
<h2>The practical test</h2>
<p>Take one real piece you're working on. Draft it in both with identical instructions. Edit each output to publishable quality and count the corrections needed. That number — not any benchmark — is your answer. Most professional writers we talk to run both and pick per task.</p>
<p>See our <a href="../comparisons/chatgpt-vs-claude.html">full ChatGPT vs Claude comparison</a> with verified pricing from official sources.</p>'''},
 'are-ai-tools-safe-for-business-data.html': {
  'title':'Are AI tools safe for business data?','kicker':'Data safety','desc':'Training policies, retention, and the questions to ask before pasting client material into any AI tool.',
  'body':'''
<p>"Safe" depends on the specific tool, the specific plan, and what you paste. Consumer plans and business plans of the same product often have completely different data terms.</p>
<h2>The four questions to ask per tool</h2>
<ol><li><strong>Does this plan train models on my inputs?</strong> Some consumer tiers default to yes (with opt-outs); business tiers usually default to no. Cursor, for example, states it won't train on your content unless you explicitly agree.</li><li><strong>How long are inputs retained?</strong> Retention ranges from zero-retention enterprise commitments to 30-day abuse-review windows to indefinite.</li><li><strong>Do I own the outputs?</strong> Most major vendors assign output rights to users, but ownership doesn't guarantee copyright protection for AI-generated content.</li><li><strong>What's prohibited?</strong> Client confidential material under NDA may be contractually off-limits regardless of the tool's policy.</li></ol>
<h2>The practical rule</h2>
<p>Treat every consumer-tier AI chat as a public surface until you've read that plan's training policy. For client work, prefer business/enterprise tiers with explicit no-training commitments, and never paste anything you wouldn't put in an email to a stranger.</p>
<p>Every review on this site links directly to each vendor's privacy documentation so you can verify current terms.</p>'''},
 'can-ai-write-my-blog-posts.html': {
  'title':'Can AI write my blog posts?','kicker':'Straight answer','desc':'What AI drafting does well, what it fails at, and the review work that stays yours.',
  'body':'''
<p><strong>Short answer:</strong> AI can draft your posts; it cannot write them. The draft is maybe 40% of the work, and skipping the other 60% is why AI-written blogs underperform.</p>
<h2>What AI does well</h2>
<ul><li>First drafts from a detailed outline — fast and competent</li><li>Restructuring messy notes into logical flow</li><li>Variations: titles, intros, meta descriptions at volume</li></ul>
<h2>What fails without you</h2>
<ul><li><strong>Facts:</strong> fluent but unverified claims. Every statistic needs a primary source you actually checked.</li><li><strong>Experience:</strong> readers (and search engines) reward first-hand knowledge AI doesn't have.</li><li><strong>Judgment:</strong> knowing which point matters to <em>your</em> reader is the actual skill.</li></ul>
<h2>The workflow that works</h2>
<ol><li>You outline from real knowledge of the topic</li><li>AI expands sections; you fact-check every claim against primary sources</li><li>You add experience, examples, and opinion</li><li>You edit for voice — read it aloud; if it sounds like no human you know, rewrite</li></ol>
<p>Tools like <a href="../tools/jasper/">Jasper</a>, <a href="../tools/copy-ai/">Copy.ai</a>, and <a href="../tools/chatgpt/">ChatGPT</a> all fit step two. None of them replace steps one, three, or four.</p>'''},
 'do-i-need-paid-ai-plans.html': {
  'title':'Do I need paid AI plans?','kicker':'Straight answer','desc':'When free tiers are enough and when limits start costing more than subscriptions.',
  'body':'''
<p><strong>Short answer:</strong> start free everywhere. Upgrade only the single tool where limits interrupt real work weekly.</p>
<h2>The free tier reality</h2>
<p>Most major tools — ChatGPT, Claude, Gemini, Perplexity, Canva, Otter — offer functional free tiers. For occasional use, they're genuinely enough. The catch is limits: message caps, slower models at peak, feature gates.</p>
<h2>When paid becomes rational</h2>
<ul><li>A limit costs you an hour+ of waiting or workaround time in a week</li><li>You need the paid feature (not just more volume): deeper research modes, longer context, team workspaces</li><li>Client delivery depends on consistent access</li></ul>
<h2>The upgrade math</h2>
<p>Most plans run $10–25/month. If your hourly value is $50+, breaking even requires saving about 30 minutes monthly. Track limit-hits for two weeks using our <a href="../downloads/ai-tool-evaluation-scorecard.html">free scorecard</a>; the decision makes itself.</p>
<h2>One warning</h2>
<p>Don't stack subscriptions "just in case." Five partial tools beat by two well-used ones. Annual billing locks you in — prefer monthly until you're certain.</p>'''},
 'what-is-a-good-ai-tool-starter-stack.html': {
  'title':'A good starter AI stack','kicker':'Starter guide','desc':'The minimal first three AI tools for most knowledge workers, with upgrade triggers.',
  'body':'''
<p>Three tools cover 90% of beginner needs. Total cost to start: $0.</p>
<h2>The stack</h2>
<ol><li><strong>A general assistant</strong> (ChatGPT, Claude, or Gemini — all have capable free tiers). This is your drafting, summarizing, explaining, brainstorming layer. Pick one and learn it deeply rather than switching.</li><li><strong>A research tool</strong> (Perplexity free). Cited answers for anything factual. Use it instead of asking your assistant to recall facts.</li><li><strong>One production tool matched to your work</strong>: <a href="../tools/canva-ai/">Canva</a> for visuals, <a href="../tools/gamma/">Gamma</a> for decks, <a href="../tools/otter-ai/">Otter</a> if meetings dominate your week.</li></ol>
<h2>Upgrade triggers</h2>
<p>Move to paid only when: the assistant's free limit breaks real work weekly (then ~$20/month there), or your production tool's free tier blocks client deliverables. Everything else waits.</p>
<h2>What not to add early</h2>
<p>Automation platforms, coding assistants, and specialty writers only earn their cost once the core stack is habit. Adding them first is how people end up with six subscriptions and no workflow. Revisit after 60 days of daily use.</p>
<p>Full evaluation criteria live in <a href="how-to-choose-an-ai-tool.html">our choosing framework</a>.</p>'''},
}

HEADER = '<header class="global-nav"><a class="brand" href="../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="../tools/index.html">Tools</a><a href="../comparisons/best-ai-tools.html">Best AI tools</a><a href="../categories/index.html">Categories</a><a href="../articles/index.html">Guides</a><a href="../benchmarks/">Benchmarks</a>\n</nav><a class="nav-cta" href="../legal/affiliate-disclosure.html">Disclosure</a></header>'
FOOTER = '''<footer class="footer">
    <span>© 2026 AIToolsEssentials</span>
    <a href="../advertise/index.html" rel="nofollow">Advertise</a>
    <a href="../submit-tool.html" rel="nofollow">Submit a tool</a>
    <a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
    <a href="mailto:contact@aitoolsessentials.com">Contact</a>
  <a href="../legal/about.html">About</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a><a href="../legal/corrections.html">Corrections</a></footer>'''


def generate(root: Path) -> int:
    made=0
    import json
    for fname,a in ARTICLES.items():
        p=root/'articles'/fname
        if p.exists(): continue
        faq_schema=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":a['title'],"acceptedAnswer":{"@type":"Answer","text":"See article for the complete evidence-based answer."}}]})
        page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{H.escape(a['desc'])}"><title>{H.escape(a['title'])} — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css">
<link rel="canonical" href="https://aitoolsessentials.com/articles/{fname}">
<meta property="og:title" content="{H.escape(a['title'])} — AIToolsEssentials"><meta property="og:description" content="{H.escape(a['desc'])}"><meta property="og:url" content="https://aitoolsessentials.com/articles/{fname}">
<script type="application/ld+json">{faq_schema}</script>
<link rel="icon" href="../assets/aitools-bot-mark.svg" type="image/svg+xml"></head><body>{HEADER}
<main><section class="scene scene-light article-hero"><p class="kicker light">{H.escape(a['kicker'])}</p><h1>{H.escape(a['title'])}</h1><p>{H.escape(a['desc'])}</p><div class="actions"><a class="button button-blue" href="../tools/index.html">Browse tools</a><a class="button button-dark" href="learn.html">More guides</a></div></section>
<section class="scene scene-light"><article class="article-shell">{a['body']}</article></section>
<section class="newsletter-panel"><div><span>AI Tool Evaluation Scorecard</span><h2>Decide with evidence, not demos</h2><p>Compare candidates on workflow fit, quality, review time, privacy, collaboration, cost, and ROI.</p><p class="affiliate-inline">No email required.</p></div><div class="newsletter-actions"><a class="button button-blue" href="../downloads/ai-tool-evaluation-scorecard.html">Open scorecard</a><a class="button button-dark" href="../pricing/">Premium research</a></div></section>

</main><div id="share-row" hidden></div>
{FOOTER}<script src="../js/site.js" defer></script><script src="../js/analytics.js" defer></script></body></html>'''
        p.write_text(page);made+=1
    return made

ARTICLES['does-google-index-ai-content.html'] = {
 'title':'Does Google penalize AI content?','kicker':'Straight answer','desc':'What Google actually says about AI-generated content, and what it means for publishers.',
 'body':'''
<p><strong>Short answer:</strong> Google rewards quality and originality regardless of how content is produced. Its policies target spam — mass-produced, unhelpful pages — not AI assistance itself.</p>
<h2>What Google officially says</h2>
<p>Google's guidance focuses on helpfulness and E-E-A-T signals: experience, expertise, authoritativeness, trustworthiness. Production method is not a ranking factor. The relevant policy is "scaled content abuse" — publishing volumes of pages with little value for searchers.</p>
<h2>Why some AI-heavy sites lose rankings anyway</h2>
<ul><li>Thin content: pages saying nothing beyond a search snippet</li><li>No first-hand experience or verifiable primary sources</li><li>Factual errors that erode trust signals over time</li></ul>
<h2>The practical standard</h2>
<p>Publish less, verify more: every claim sourced to a reference you actually checked, real experience included, human editing before publish. That standard protects you under any future policy change.</p>'''}

ARTICLES['ai-tools-for-real-estate-listings.html'] = {
 'title':'AI workflow: listing photos to closing docs','kicker':'Workflow guide','desc':'Where AI tools slot into a real estate transaction pipeline — and which steps should stay manual.',
 'body':'''
<h2>Listing creation</h2>
<p><a href="../tools/canva-ai/">Canva AI</a> turns listing photos and copy into marketing materials; assistants draft property descriptions from feature lists. Review fair-housing compliance on every generated description — automation errors here carry legal cost.</p>
<h2>Client communication</h2>
<p><a href="../tools/chatgpt/">ChatGPT</a> drafts follow-ups from bullet notes. Never paste client financials into consumer-tier tools — see <a href="are-ai-tools-safe-for-business-data.html">the data-safety guide</a>.</p>
<h2>Closing paperwork</h2>
<p>This stays human. Contract review carries liability no current tool absorbs. Use <a href="../tools/otter-ai/">Otter</a> for meeting notes with consent; keep document review and execution manual.</p>
<p>Full picks in the <a href="best-ai-tools-for-real-estate-agents.html">real estate agents guide</a>.</p>'''}

ARTICLES['chatgpt-free-vs-plus.html'] = {
 'title':'ChatGPT free vs Plus: what the limits actually are','kicker':'Question guide','desc':'What OpenAI officially publishes about ChatGPT plan structure — without treating unofficial dollar figures as list prices.',
 'body':'''
<p><strong>Short answer:</strong> start on Free. Upgrade only if a published limit interrupts real work more than once a week. Exact localized Plus prices were not consistently exposed on OpenAI’s official pricing page during the last check, so verify <a href="https://openai.com/chatgpt/pricing/" rel="sponsored noopener nofollow" target="_blank">openai.com/chatgpt/pricing</a> before you pay.</p>
<h2>What is official</h2>
<p>OpenAI lists ChatGPT Free, Go, Plus, Pro, Business, and Enterprise. Free is $0. Paid self-service plans are billed per user per month. Enterprise is sales-assisted. Our last official-source check (2026-08-25) did not treat unofficial third-party dollar amounts as list prices.</p>
<h2>What paying is for</h2>
<ul><li>Higher usage limits when Free interrupts a weekly workflow</li><li>Priority access to newer models and advanced features</li><li>Business or Enterprise terms when client files cannot sit on a consumer chat plan</li></ul>
<h2>A one-week test</h2>
<p>Use Free on your three real tasks. Write down every limit hit. If it happens five or more times, open the official pricing page and compare that cost to an hour of your time. See also <a href="is-chatgpt-worth-it.html">Is ChatGPT worth it?</a> and the <a href="../tools/chatgpt/">ChatGPT review</a>.</p>
<p class="monetization-note">Plan structure checked against official OpenAI sources. Confirm current prices on the vendor page before purchasing.</p>'''}

ARTICLES['perplexity-vs-google.html'] = {
 'title':'Is Perplexity better than Google?','kicker':'Question guide','desc':'When a cited research assistant is the better first stop than a general search page — without a fake winner.',
 'body':'''
<p><strong>Short answer:</strong> Perplexity is better as a first draft of sources for a research question. Google is still the better place to open the actual page, check freshness, and run navigational searches. They are not substitutes.</p>
<h2>Use Perplexity first when</h2>
<ul><li>You need a cited starting set of pages for a specific question</li><li>You want a synthesis you will then verify in the linked sources</li><li>You are comparing two documented product claims</li></ul>
<h2>Stay in Google when</h2>
<ul><li>You already know the site you want</li><li>You need local results, shopping, or a login page</li><li>The answer depends on a page that was updated today</li></ul>
<h2>Official pricing stance</h2>
<p>Perplexity publishes free access plus paid individual and organization plans. The last official consumer-plan check did not expose current Pro or Max dollar prices on the reviewed public pages. An official organization-onboarding article listed Enterprise Pro at $40/seat monthly or $400/seat annually. Verify <a href="../tools/perplexity/">the Perplexity review</a> and Perplexity’s current pricing page before buying.</p>
<p>Never treat a cited answer as the primary source. Open the link.</p>'''}

ARTICLES['can-i-cancel-ai-subscriptions.html'] = {
 'title':'Can I cancel AI subscriptions anytime?','kicker':'Question guide','desc':'How to read cancel, downgrade, and annual-prepay terms before you lock a stack.',
 'body':'''
<p><strong>Short answer:</strong> many tools let you cancel or downgrade, but annual prepay is not the same as month-to-month. Read the official billing page for the exact plan. Do not assume a forum post is current.</p>
<h2>What to verify on the official page</h2>
<ol><li>Is the advertised monthly price billed monthly, or is it an annual equivalent paid upfront?</li><li>Does canceling stop future charges or only stop auto-renew at period end?</li><li>Do unused credits expire at cancel?</li><li>Can you export your files after you leave?</li></ol>
<h2>Examples already recorded on this site</h2>
<ul><li>Landlord Studio’s official FAQ says you can cancel or downgrade anytime and keep access to your data.</li><li>Grantable’s official docs say canceling moves the account to Free and keeps workspaces.</li><li>Instrumentl’s official Discover rate is paid upfront annually, with a higher month-to-month alternative.</li><li>Riverside’s official FAQ says annual billing saves up to 20% versus monthly.</li></ul>
<h2>Practical rule</h2>
<p>Stay on monthly until the tool owns a weekly job. Annual discounts are real only if you would have paid all twelve months. Use the <a href="../pricing-watch/">pricing watch</a> and each tool’s official billing URL before you prepay.</p>'''}

ARTICLES['do-ai-tools-work-offline.html'] = {
 'title':'Do AI tools work offline?','kicker':'Question guide','desc':'Which AI tools can run locally, which need the cloud, and how to choose offline-first AI without buying the wrong hardware.',
 'body':'''
<p><strong>Short answer:</strong> most popular AI tools need the cloud. Offline AI is possible with local runtimes such as Ollama, LM Studio, and Open WebUI, but you trade convenience for hardware, model setup, and slower updates.</p>
<h2>Cloud-first tools</h2>
<p>ChatGPT, Claude, Perplexity, Canva, Riverside, and most SaaS assistants require an internet connection for the core AI features. They are easier to start, but your inputs leave the device under that plan’s terms.</p>
<h2>Local-first tools</h2>
<p><a href="../tools/ollama/">Ollama</a>, <a href="../tools/lm-studio/">LM Studio</a>, and <a href="../tools/open-webui/">Open WebUI</a> can run models on your own hardware. Use the <a href="../local-ai-planner/">Local AI Workbench Planner</a> before buying a Mac, GPU workstation, or mini PC.</p>
<h2>The practical test</h2>
<ol><li>Pick the exact workflow: private notes, coding help, summarization, or chat.</li><li>Choose one model size you can actually run.</li><li>Measure response speed on your hardware.</li><li>Only then decide if offline is worth the maintenance.</li></ol>'''}

ARTICLES['what-happens-to-my-data-when-i-delete-ai-account.html'] = {
 'title':'What happens to my data when I delete an AI account?','kicker':'Data guide','desc':'Deletion, retention, training, and export questions to ask before canceling an AI subscription.',
 'body':'''
<p><strong>Short answer:</strong> deletion is not always instant erasure. Vendors may keep backups, abuse logs, billing records, or de-identified analytics under their published policy. The exact answer depends on the tool and plan.</p>
<h2>Read these four sections first</h2>
<ol><li>Account deletion policy</li><li>Data retention and backup windows</li><li>Training or product-improvement controls</li><li>Export/download rules after cancellation</li></ol>
<h2>Why plan tier matters</h2>
<p>Consumer and business plans often have different training and retention terms. A team or enterprise plan may include no-training commitments that a free consumer account does not. Every AIToolsEssentials review links to the vendor privacy or rights page where available.</p>
<h2>Practical rule</h2>
<p>Export important files before canceling. For client, student, patient, tenant, donor, or legal matter data, do not rely on a delete button as your only control — keep sensitive material out of unapproved consumer AI tools in the first place.</p>'''}

ARTICLES['which-ai-tool-writes-best-in-another-language.html'] = {
 'title':'Which AI tool writes best in another language?','kicker':'Question guide','desc':'How to compare multilingual writing tools without trusting a benchmark that does not match your audience.',
 'body':'''
<p><strong>Short answer:</strong> test the language you actually publish in. The best tool for English sales copy may not be the best for Spanish support emails, Arabic summaries, or French legal-style prose.</p>
<h2>A repeatable language test</h2>
<ol><li>Write one source brief in your native language.</li><li>Ask ChatGPT, Claude, Gemini, and Perplexity for the same output.</li><li>Have a fluent human mark tone, accuracy, idioms, formality, and hallucinated facts.</li><li>Count edits required to publish.</li></ol>
<h2>What to watch for</h2>
<ul><li>Overly literal translations</li><li>Wrong level of formality</li><li>Invented local facts, laws, or prices</li><li>Region mismatch: Latin America vs Spain, Canadian French vs France, etc.</li></ul>
<p>Use the <a href="../compare-shortlist.html">Compare Shortlist</a> and <a href="../downloads/ai-tool-evaluation-scorecard.html">scorecard</a> to record the winner for your language and workflow.</p>'''}

ARTICLES['is-claude-worth-it.html'] = {
 'title':'Is Claude worth it?','kicker':'Straight answer','desc':'Who benefits from a paid Claude plan, based on verified plan structure and real workflow fit — not hype.',
 'body':'''
<p><strong>Short answer:</strong> worth it if your work involves long documents, careful prose, or instruction-heavy drafting. Not worth it for quick questions or image generation.</p>
<h2>What paying actually buys</h2>
<p>Anthropic offers Claude Free, Pro, Max, Team, and Enterprise. Paid tiers buy higher message limits, priority access during peak hours, and access to extended thinking and deeper research modes. Exact prices change — check Anthropic's official pricing page before deciding.</p>
<h2>You probably don't need paid if…</h2>
<ul><li>You ask short questions and free-tier limits don't interrupt you</li><li>Your tasks are quick summaries or brief explanations</li><li>You need images, voice, or file analysis more than long-form writing</li></ul>
<h2>Paid starts earning its keep when…</h2>
<ul><li>You routinely work with documents over 30 pages</li><li>A free-tier limit interrupts real work more than once a week</li><li>You need consistent access during peak hours for deadlines</li><li>Instruction adherence on style or format matters to your output</li></ul>
<h2>How to decide in one week</h2>
<p>Use the free tier on your three most common real tasks. Note every time you hit a limit. If it happens five-plus times, compare that cost to an hour of your time. See our <a href="how-to-test-ai-tools-free-trials.html">free-trial testing guide</a> and the <a href="../tools/claude/">Claude review</a>.</p>
<p class="monetization-note">Plan structure checked against official Anthropic sources. Confirm current prices on the vendor page before purchasing.</p>'''}

ARTICLES['is-perplexity-worth-it.html'] = {
 'title':'Is Perplexity worth it?','kicker':'Straight answer','desc':'Who benefits from a paid Perplexity plan, and when the free tier is genuinely enough for cited research.',
 'body':'''
<p><strong>Short answer:</strong> worth it if you do cited research daily and hit the free tier's search limit. Not worth it if you only look up a few things per week.</p>
<h2>What paying actually buys</h2>
<p>Perplexity offers Free, Pro, and Max plans. Pro buys more searches per day, file uploads, and access to more powerful models for synthesis. Max adds higher limits and priority access. Exact prices change — check Perplexity's official pricing page before deciding.</p>
<h2>You probably don't need paid if…</h2>
<ul><li>You do a handful of research lookups per day</li><li>You use it as a secondary check, not a primary research tool</li><li>You're fine opening the cited sources yourself</li></ul>
<h2>Paid starts earning its keep when…</h2>
<ul><li>The daily search limit interrupts a real research workflow</li><li>You need deeper model access for complex synthesis</li><li>You rely on cited answers for client or team deliverables</li></ul>
<h2>How to decide in one week</h2>
<p>Use the free tier for your actual research tasks. Count every time you hit the search limit. If it happens daily, the paid plan is rational. See the <a href="../tools/perplexity/">Perplexity review</a> and our <a href="perplexity-vs-google.html">Perplexity vs Google guide</a>.</p>
<p class="monetization-note">Plan structure checked against official Perplexity sources. Confirm current prices on the vendor page before purchasing.</p>'''}

ARTICLES['is-cursor-worth-it.html'] = {
 'title':'Is Cursor worth it?','kicker':'Straight answer','desc':'Who benefits from a paid Cursor plan, and when the free tier or VS Code is enough for AI-assisted coding.',
 'body':'''
<p><strong>Short answer:</strong> worth it if you code daily and the AI completions save you more than 30 minutes a week. Not worth it for occasional edits or non-developers.</p>
<h2>What paying actually buys</h2>
<p>Cursor offers a Free tier with limited completions and a Pro tier with higher limits, agent mode, and access to frontier models. Cursor also ships its own model stack including Cursor Grok 4.6 and Composer 2.5. Exact prices change — check Cursor's official pricing page before deciding.</p>
<h2>You probably don't need paid if…</h2>
<ul><li>You edit code a few times a week, not daily</li><li>GitHub Copilot or free VS Code extensions cover your needs</li><li>You're learning to code and need to build fundamentals first</li></ul>
<h2>Paid starts earning its keep when…</h2>
<ul><li>You code daily and AI completions are part of your flow</li><li>Agent mode (multi-file edits, autonomous fixes) saves real time</li><li>You want frontier model access inside the editor without switching tools</li></ul>
<h2>How to decide in one week</h2>
<p>Use the free tier for your actual coding tasks. Track every time a completion or agent run saves you meaningful time. See the <a href="../tools/cursor/">Cursor review</a> and our <a href="../comparisons/cursor-vs-github-copilot.html">Cursor vs GitHub Copilot comparison</a>.</p>
<p class="monetization-note">Plan structure checked against official Cursor sources. Confirm current prices on the vendor page before purchasing.</p>'''}

ARTICLES['is-grok-worth-it.html'] = {
 'title':'Is Grok worth it?','kicker':'Straight answer','desc':'Who benefits from a paid Grok plan through X, and when the free tier is enough for real-time AI assistance.',
 'body':'''
<p><strong>Short answer:</strong> worth it if you want real-time AI with live web and X data, or use Grok Bot always-on agents. Not worth it if you only need a general chat assistant.</p>
<h2>What paying actually buys</h2>
<p>Grok is available through X with free and paid tiers. Paid access buys higher usage limits, access to newer models like Grok 4.6, and features like Grok Build and Imagine. Grok Bot offers always-on agents for automated workflows. Exact prices change — check X's official pricing or Grok's official page before deciding.</p>
<h2>You probably don't need paid if…</h2>
<ul><li>You use a general assistant for quick questions</li><li>You don't need real-time X/web data in your AI responses</li><li>You already have ChatGPT or Claude and don't need a third assistant</li></ul>
<h2>Paid starts earning its keep when…</h2>
<ul><li>Real-time information from X and the web is part of your workflow</li><li>You use Grok Bot agents for repeatable tasks</li><li>You want image generation (Imagine) and model building (Grok Build) in one place</li></ul>
<h2>How to decide in one week</h2>
<p>Use the free tier on your real tasks. If real-time data or agent automation is part of your daily work, paid is rational. See the <a href="../tools/grok/">Grok review</a> and our <a href="../comparisons/chatgpt-vs-grok.html">ChatGPT vs Grok comparison</a>.</p>
<p class="monetization-note">Plan structure checked against official X/Grok sources. Confirm current prices on the vendor page before purchasing.</p>'''}

ARTICLES['is-gemini-worth-it.html'] = {
 'title':'Is Gemini worth it?','kicker':'Straight answer','desc':'Who benefits from a paid Google Gemini plan, and when the free tier or Google AI tools are enough.',
 'body':'''
<p><strong>Short answer:</strong> worth it if you live in Google Workspace and want AI integrated into Docs, Gmail, and Drive. Not worth it if you don't use Google's ecosystem.</p>
<h2>What paying actually buys</h2>
<p>Google offers Gemini Free and paid tiers including Google AI Pro and Ultra. Paid plans buy higher usage limits, deeper Google Workspace integration, and access to more powerful models. Exact prices change — check Google's official pricing page before deciding.</p>
<h2>You probably don't need paid if…</h2>
<ul><li>You don't use Google Workspace daily</li><li>Your tasks are quick questions a free assistant handles</li><li>You prefer ChatGPT or Claude for your primary assistant</li></ul>
<h2>Paid starts earning its keep when…</h2>
<ul><li>You live in Google Docs, Sheets, Gmail, and Drive</li><li>You want AI integrated directly into your documents and email</li><li>You need Gemini's multimodal capabilities (images, video understanding) for work</li></ul>
<h2>How to decide in one week</h2>
<p>Use the free tier inside your actual Google workflow. If the integration saves you a switch to another tool, paid is rational. See our <a href="../comparisons/chatgpt-vs-gemini.html">ChatGPT vs Gemini comparison</a> and <a href="../comparisons/claude-vs-gemini.html">Claude vs Gemini comparison</a>.</p>
<p class="monetization-note">Plan structure checked against official Google sources. Confirm current prices on the vendor page before purchasing.</p>'''}

ARTICLES['is-notion-ai-worth-it.html'] = {
 'title':'Is Notion AI worth it?','kicker':'Straight answer','desc':'Who benefits from Notion AI, and when a separate AI assistant plus your existing notes is the better choice.',
 'body':'''
<p><strong>Short answer:</strong> worth it if your team lives in Notion and wants AI inside the knowledge base. Not worth it if you only need a general chat assistant.</p>
<h2>What paying actually buys</h2>
<p>Notion AI is available as an add-on to Notion plans. It buys AI-assisted writing, summarization, database queries, and search inside your Notion workspace. Exact prices change — check Notion's official pricing page before deciding.</p>
<h2>You probably don't need paid if…</h2>
<ul><li>You don't use Notion as your primary workspace</li><li>You're fine copying text into ChatGPT or Claude when needed</li><li>Your notes are simple and don't benefit from in-context AI</li></ul>
<h2>Paid starts earning its keep when…</h2>
<ul><li>Your team's knowledge base lives in Notion and AI search saves time finding things</li><li>You want AI to summarize pages, draft from database entries, or fill templates</li><li>Switching between Notion and a separate assistant breaks your flow</li></ul>
<h2>How to decide in one week</h2>
<p>Try the free Notion AI trial on your actual workspace. Count times the in-context AI saves you a tool switch. See our <a href="personal-knowledge-base-notion-ai.html">Notion AI knowledge base guide</a> and the <a href="../comparisons/notion-ai-vs-microsoft-copilot.html">Notion AI vs Copilot comparison</a>.</p>
<p class="monetization-note">Plan structure checked against official Notion sources. Confirm current prices on the vendor page before purchasing.</p>'''}

ARTICLES['best-ai-tools-for-beginners.html'] = {
 'title':'Best AI tools for beginners','kicker':'Beginner guide','desc':'A free-first starter stack for people who want practical AI results without buying five subscriptions.',
 'body':'''
<p><strong>Short answer:</strong> beginners should start with three tools: one general assistant, one cited research tool, and one production tool that matches the work they actually do. Do not buy a large AI stack on day one.</p>
<h2>The beginner stack</h2>
<ol><li><strong>General assistant:</strong> start with <a href="../tools/chatgpt/">ChatGPT</a>, <a href="../tools/claude/">Claude</a>, or <a href="../tools/gemini/">Gemini</a>. Use one for drafting, summaries, brainstorming, and everyday questions.</li><li><strong>Cited research:</strong> use <a href="../tools/perplexity/">Perplexity</a> when the answer depends on sources you need to open and verify.</li><li><strong>One production tool:</strong> choose <a href="../tools/canva-ai/">Canva AI</a> for visuals, <a href="../tools/gamma/">Gamma</a> for decks, <a href="../tools/otter-ai/">Otter</a> for meetings, or <a href="../tools/notion-ai/">Notion AI</a> if your notes already live in Notion.</li></ol>
<h2>Best free-first picks</h2>
<ul><li><strong>ChatGPT:</strong> easiest starting point for general help and everyday prompts.</li><li><strong>Claude:</strong> strong for long documents, careful writing, and instruction-heavy drafts.</li><li><strong>Gemini:</strong> most useful if your work already lives in Google apps.</li><li><strong>Perplexity:</strong> better first stop for source-backed research than asking a chatbot to remember facts.</li><li><strong>Canva AI:</strong> practical for non-designers making social graphics, simple decks, and marketing visuals.</li><li><strong>Otter:</strong> good entry point when meetings are the recurring time sink.</li></ul>
<h2>When to upgrade</h2>
<p>Upgrade only after a free limit interrupts real work more than once a week, or when a paid-only feature is required for a deliverable. Start with <a href="is-chatgpt-worth-it.html">Is ChatGPT worth it?</a>, <a href="is-claude-worth-it.html">Is Claude worth it?</a>, and <a href="do-i-need-paid-ai-plans.html">Do I need paid AI plans?</a> before adding subscriptions.</p>
<h2>One-week beginner test</h2>
<ol><li>Pick three real tasks you already do every week.</li><li>Run each task through the same assistant for five workdays.</li><li>Record where the output saved time and where you had to correct it.</li><li>Use <a href="../downloads/ai-tool-evaluation-scorecard.html">the free scorecard</a> to decide what stays.</li></ol>
<p><strong>Rule:</strong> one useful workflow beats ten installed tools. If a tool does not save time in a real task during week one, remove it from the stack.</p>'''}

ARTICLES['launch-ai-business-whop-blueprints.html'] = {
 'title':'How to launch an AI business with Whop Blueprints','kicker':'How-to guide','desc':'Deploy a working digital product business — products, pricing, website, and checkout — in one command with the Whop CLI and Blueprints.',
 'body':'''
<p><strong>Short answer:</strong> Whop Blueprints let you deploy a complete business — products, pricing, a live website, and payment wiring — in one step, either from the gallery or the CLI. You can then manage everything from the terminal or hand it to an AI agent.</p>
<h2>What a Blueprint deploys</h2>
<ul><li><strong>Products:</strong> copied from the blueprint with pricing plans, images, and store-page styling</li><li><strong>Website:</strong> live at your own whop.site address</li><li><strong>Payment wiring:</strong> the site can take payments from the moment it is up</li></ul>
<h2>Step 1: Pick a Blueprint</h2>
<p>Browse the gallery at <a href="https://whop.com/blueprints" rel="sponsored noopener nofollow" target="_blank">whop.com/blueprints</a>. Categories include ecommerce stores, agencies, gyms, marketplaces, and more. Each blueprint is a real running business — deploying it gives you your own copy.</p>
<h2>Step 2: Deploy</h2>
<p>Click deploy on the blueprint detail page. Whop creates your business if you do not have one, copies the products and site over, and serves it at your route. Nothing builds on your machine.</p>
<p>Or from the CLI:</p>
<p><code>whop apps init --template app_xxxxxxxx --name "My Store" --route my-store</code></p>
<h2>Step 3: Manage from the terminal</h2>
<p>Install the <a href="../tools/whop-cli/">Whop CLI</a> and run <code>whop</code> to sign in. Then:</p>
<ul><li><code>whop products list</code> — see what you are selling</li><li><code>whop plans create</code> — add or change pricing</li><li><code>whop checkout-configurations create --plan_id plan_xxx</code> — get a shareable checkout link</li><li><code>whop stats time_series</code> — pull your numbers</li></ul>
<h2>Step 4: Hand it to an AI agent</h2>
<p>The CLI is self-describing and works with AI agents (Claude, Cursor, Codex):</p>
<ul><li><code>whop --llms</code> — machine-readable manifest of all commands</li><li><code>whop mcp add</code> — register with supported coding agents</li><li><code>whop skills add</code> — install the Whop agent skill</li></ul>
<p>You can ask your agent to create products, set pricing, pull stats, or run ad campaigns — all from natural language.</p>
<h2>Where this fits</h2>
<p>If you are building an AI-powered business, the Whop CLI + Blueprints combination removes the setup friction. You bring the product idea; Whop handles hosting, payments, and the infrastructure. For non-technical founders, the dashboard works. For developers and agent-driven workflows, the CLI is faster.</p>
<p>See our <a href="../tools/whop-cli/">Whop CLI review</a> and the <a href="best-ai-automation-tools.html">best AI automation tools</a> guide for more.</p>'''}

ARTICLES['how-to-cut-ai-tool-subscriptions.html'] = {
 'title':'How to cut AI tool subscriptions without losing work','kicker':'Cost-cutting guide','desc':'A practical keep/cut/trial framework for AI stacks that overlap — free scorecard first, Premium matrix when you need the full archive.',
 'body':'''
<p><strong>Short answer:</strong> most teams do not need more AI tools. They need a keep/cut/trial process that forces every subscription to own a weekly workflow. Start free, then use a full decision matrix only if the stack is still messy after one honest review.</p>
<h2>The 30-minute cut process</h2>
<ol>
<li><strong>List every AI subscription</strong> with monthly cost, owner, and last real use.</li>
<li><strong>Group by job</strong> — drafting, research, meetings, coding, visuals, automation. Overlap lives inside a job, not across the whole stack.</li>
<li><strong>Run one real task</strong> in each contender for the same job. Demos do not count.</li>
<li><strong>Tag keep / trial / replace / cancel</strong>. Keep only tools used weekly with a clear owner.</li>
<li><strong>Cancel or pause</strong> anything without a weekly workflow before the next renewal.</li>
</ol>
<h2>Free tools that help right now</h2>
<ul>
<li><a href="../downloads/ai-tool-evaluation-scorecard.html">AI Tool Evaluation Scorecard</a> — score one real task before paying.</li>
<li><a href="../cost-calculator.html">Cost calculator</a> — estimate stack spend before annual lock-in.</li>
<li><a href="../pricing-watch/">AI Pricing Watch</a> — verified pricing snapshots with checked dates.</li>
<li><a href="../decision-brief.html">Decision Brief</a> — pick 2–3 tools and generate a shareable brief with overlap warnings.</li>
</ul>
<h2>When a free review is not enough</h2>
<p>If you have five or more paid AI tools, multiple owners, or annual prepays on the calendar, a one-page scorecard is not enough. You need a full matrix, a stack-audit template, a weekly checklist, and a change-alert feed so renewals are not decided from memory.</p>
<p>That is what <a href="../premium/">AIToolsEssentials Premium</a> is for: a $12/month research membership with a 7-day free trial, stack-audit template, weekly checklist, tool-change alerts, hands-on comparison protocols, ROI calculator, and priority research slots. Research and strategy only — no implementation or account access.</p>
<p>Use code <strong>LAUNCH50</strong> for 50% off the first paid month after the trial (new users). Start from the <a href="../premium/">Premium page</a> or <a href="../pricing/">pricing</a>.</p>
<h2>Decision rule</h2>
<p>If a tool does not save measurable time on a weekly workflow, it is a cancel candidate. "Just in case" is not a workflow. Prefer free trials and monthly billing until one tool clearly owns the job.</p>
'''}

ARTICLES['ai-stack-audit-checklist.html'] = {
 'title':'AI stack audit checklist: keep, cut, or trial','kicker':'Audit checklist','desc':'A free AI stack audit checklist for mapping every paid tool, spotting overlap, and deciding keep/cut/trial before the next renewal.',
 'body':'''
<p><strong>Short answer:</strong> an AI stack audit is a structured inventory of every paid AI tool, what job it owns, how often it is used, and what it costs. The goal is not a prettier spreadsheet — it is fewer overlapping subscriptions.</p>
<h2>What to capture for every tool</h2>
<ul>
<li>Name and plan tier</li>
<li>Monthly or annual cost</li>
<li>Owner (person accountable for the spend)</li>
<li>Weekly use hours (honest estimate)</li>
<li>Primary job it owns</li>
<li>Whether another paid tool already does that job</li>
<li>Privacy or client-data constraints</li>
<li>Cancellation risk (annual prepay, seats, contracts)</li>
</ul>
<h2>Free path</h2>
<ol>
<li>Download the <a href="../downloads/ai-tool-evaluation-scorecard.html">evaluation scorecard</a> and score one real task per contender.</li>
<li>Use the <a href="../cost-calculator.html">cost calculator</a> to total monthly spend.</li>
<li>Run a <a href="../decision-brief.html">decision brief</a> for any 2–3 tool shortlist.</li>
<li>Check <a href="../pricing-watch/">Pricing Watch</a> before renewing anything annual.</li>
</ol>
<h2>When to use the Premium audit pack</h2>
<p><a href="../premium/">Premium members</a> get a fillable <strong>AI Stack Audit Template</strong>, a weekly checklist, an ROI calculator, and a full 61-tool decision matrix. Reply with a completed audit for a strategy-only keep/cut/trial recommendation within 48 hours. No account access required. 7-day free trial, then $12/month; code <strong>LAUNCH50</strong> for 50% off the first paid month (new users).</p>
<h2>Red flags</h2>
<ul>
<li>Two paid tools own the same weekly job</li>
<li>A tool has no owner</li>
<li>No real task test in the last 30 days</li>
<li>Annual prepay before a 2-week real-work trial</li>
<li>Client data pasted into a tool with unclear training defaults</li>
</ul>
'''}

ARTICLES['chatgpt-vs-claude-vs-grok-vs-gemini.html'] = {
 'title':'ChatGPT vs Claude vs Grok vs Gemini: how to choose','kicker':'Comparison guide','desc':'A practical way to choose between ChatGPT, Claude, Grok, and Gemini using identical real tasks — not brand preference or generic benchmarks.',
 'body':'''
<p><strong>Short answer:</strong> do not pick a general AI assistant by brand. Run the same drafting, research, and coding tasks in each finalist and keep the one that reduces review time without raising verification risk.</p>
<h2>What each assistant is usually best for</h2>
<ul>
<li><strong><a href="../tools/chatgpt/">ChatGPT</a>:</strong> broad everyday work — drafting, files, browsing, and multimodal tasks in one place.</li>
<li><strong><a href="../tools/claude/">Claude</a>:</strong> long documents, careful prose, instruction-heavy drafting, and document review.</li>
<li><strong><a href="../tools/grok/">Grok</a>:</strong> real-time X/web context, always-on agent features, and image generation where available.</li>
<li><strong><a href="../tools/gemini/">Gemini</a>:</strong> Google Workspace-native work across Docs, Gmail, Drive, and multimodal tasks.</li>
</ul>
<p>Confirm current model names and plan limits on each vendor page — lineups change. See also our model lineup notes and the individual <a href="is-chatgpt-worth-it.html">worth-it guides</a>.</p>
<h2>30-minute hands-on protocol</h2>
<ol>
<li>Write one brief for drafting, one for research, one for coding/debugging.</li>
<li>Run the identical brief in ChatGPT, Claude, Grok, and Gemini on the plan you actually pay for (or free).</li>
<li>Score editing burden, factual verification effort, and whether the output is usable without heavy rewrite.</li>
<li>Keep one primary assistant. Keep a second only if it owns a different weekly job.</li>
</ol>
<h2>Free vs Premium</h2>
<p>Public pages give you the comparison framework and tool reviews. <a href="../premium/">Premium</a> members get a fillable hands-on comparison CSV, the full decision matrix, tool-change alerts when model lineups shift, and priority research slots. 7-day free trial · $12/month · code <strong>LAUNCH50</strong> for 50% off the first paid month (new users).</p>
<p>Related: <a href="claude-vs-chatgpt-for-writing.html">Claude vs ChatGPT for writing</a>, <a href="../comparisons/chatgpt-vs-claude.html">ChatGPT vs Claude</a>, <a href="../comparisons/chatgpt-vs-gemini.html">ChatGPT vs Gemini</a>, <a href="../comparisons/chatgpt-vs-grok.html">ChatGPT vs Grok</a>.</p>
'''}

ARTICLES['is-an-ai-tool-membership-worth-it.html'] = {
 'title':'Is an AI tool research membership worth it?','kicker':'Straight answer','desc':'When a $12/month AI research membership beats another SaaS subscription — and when free directories and scorecards are enough.',
 'body':'''
<p><strong>Short answer:</strong> a research membership is worth it if you already pay for multiple AI tools, renewals are coming up, and you need dated decision archives more than another generative app. It is not worth it if you only need one free assistant and have no stack to manage.</p>
<h2>When free is enough</h2>
<ul>
<li>You use one general assistant a few times a week</li>
<li>You can finish a decision with a free scorecard and one trial</li>
<li>No annual prepays or multi-seat tools are on the calendar</li>
</ul>
<p>Start with the <a href="../downloads/ai-tool-evaluation-scorecard.html">scorecard</a>, <a href="best-ai-tools-for-beginners.html">beginner guide</a>, and free <a href="../tools/index.html">tool reviews</a>.</p>
<h2>When a membership earns its keep</h2>
<ul>
<li>You have 3+ paid AI tools and unclear ownership</li>
<li>Pricing, models, or plan names change faster than you track them</li>
<li>You need a reusable audit, weekly checklist, and comparison protocol</li>
<li>You want priority research on a specific workflow without hiring a consultant</li>
</ul>
<p><a href="../premium/">AIToolsEssentials Premium</a> is built for that case: monthly decision matrix, stack-audit template, weekly checklist, tool-change alert feed, hands-on protocols, ROI calculator, and priority research slots. It is research and strategy only — not implementation, setup, integrations, or account access.</p>
<p><strong>Price:</strong> 7-day free trial, then $12/month via Whop. Code <strong>LAUNCH50</strong> = 50% off the first paid month for new users. Cancel anytime from Whop. All sales final — no refunds.</p>
<h2>How to evaluate any research membership</h2>
<ol>
<li>Does it give dated sources, not undated opinions?</li>
<li>Can you download CSVs or templates you will reuse monthly?</li>
<li>Is the scope clearly research-only, so you are not buying vague "support"?</li>
<li>Is there a trial before the first charge?</li>
</ol>
<p>If those fail, stay on the free site. If they pass and your stack is already expensive, $12/month is usually cheaper than one unused AI seat.</p>
'''}

ARTICLES['ai-invoicing-admin-stack-consultants.html'] = {
 'title':'AI invoicing and admin stack for solo consultants','kicker':'How-to workflow','desc':'A free-first admin stack for invoices, follow-up, and weekly bookkeeping so consultants do not buy five overlapping AI tools.',
 'body':'''
<p><strong>Short answer:</strong> solo consultants should keep one general assistant for drafts, one notes or CRM-adjacent tool for follow-up, and a real invoicing system. Do not add an AI billing product until invoices are late every month.</p>
<h2>The job</h2>
<p>Weekly admin: write invoices, chase unpaid work, log expenses, and turn call notes into next actions. AI helps the writing. It does not replace your books.</p>
<h2>Free-first stack</h2>
<ol>
<li><strong>Drafting:</strong> <a href="../tools/chatgpt/">ChatGPT</a> or <a href="../tools/claude/">Claude</a> free tier for invoice language, reminder emails, and scope notes.</li>
<li><strong>Notes:</strong> <a href="../tools/notion-ai/">Notion AI</a> only if your notes already live in Notion. Otherwise keep a plain notes app.</li>
<li><strong>Follow-up automation:</strong> test <a href="../tools/make/">Make</a> or <a href="../tools/zapier-ai/">Zapier AI</a> on one real unpaid-invoice reminder before paying.</li>
</ol>
<p>See the workflow page: <a href="../workflows/consultant-invoicing-admin.html">consultant invoicing admin</a>.</p>
<h2>What to test in one week</h2>
<ul>
<li>Write two real invoices with the same brief in your primary assistant.</li>
<li>Send one reminder email you would actually send.</li>
<li>Count minutes saved vs minutes spent editing.</li>
<li>Do not connect bank or client financial data to a consumer AI plan.</li>
</ul>
<p>Use the <a href="../downloads/ai-tool-evaluation-scorecard.html">scorecard</a> and <a href="../cost-calculator.html">cost calculator</a>. If you already pay for overlapping admin tools, the <a href="ai-stack-audit-checklist.html">stack audit checklist</a> and <a href="../premium/">Premium</a> audit template help you cut before renewal. 7-day trial; code LAUNCH50 for 50% off the first paid month (new users).</p>
'''}

ARTICLES['evaluating-ai-coding-tools-team-rollout.html'] = {
 'title':'Evaluating AI coding tools for a team rollout','kicker':'Security checklist','desc':'A security-first checklist for rolling out Cursor, Copilot, or chat coding assistants to a team without leaking source or buying two IDEs.',
 'body':'''
<p><strong>Short answer:</strong> pick one primary coding assistant. Run the same real bugfix on each finalist. Check training defaults, repo access, and offboarding before any annual plan.</p>
<h2>Do not skip these questions</h2>
<ol>
<li>Does this plan train on your code by default?</li>
<li>Can admins disable sharing, retention, or repo plugins?</li>
<li>What happens when a seat leaves?</li>
<li>Can you export or revoke access to indexed code?</li>
</ol>
<p>Walk the same list in <a href="../workflows/coding-assistant-security-review.html">coding assistant security review</a>.</p>
<h2>Hands-on protocol</h2>
<ol>
<li>Choose one real bugfix or small feature, not a demo todo app.</li>
<li>Run it in <a href="../tools/cursor/">Cursor</a>, <a href="../tools/github-copilot/">GitHub Copilot</a>, and your current chat assistant on the plan you actually pay for.</li>
<li>Score first-output acceptance rate and edit burden.</li>
<li>Keep one primary. Keep a second only if it owns a different weekly job.</li>
</ol>
<p>Related: <a href="is-cursor-worth-it.html">Is Cursor worth it?</a> and <a href="../comparisons/cursor-vs-github-copilot.html">Cursor vs GitHub Copilot</a>.</p>
<p>If the team already pays for two coding seats, use the <a href="../premium/">Premium</a> coding shortlist and stack audit. Research only; no implementation or account access. 7-day free trial; LAUNCH50 for 50% off the first paid month (new users).</p>
'''}

ARTICLES['ai-image-rights-commercial-use.html'] = {
 'title':'AI image rights: using Midjourney or Leonardo output commercially','kicker':'Rights guide','desc':'What to check before using AI image output in client work: plan terms, likeness, trademarks, and when you still need a human designer.',
 'body':'''
<p><strong>Short answer:</strong> commercial use depends on the vendor plan and the content of the image. Output that looks like a real person, brand, or copyrighted character is still your legal problem even if the tool allowed the prompt.</p>
<h2>Check before you publish</h2>
<ul>
<li>Current commercial-use terms on the official <a href="https://www.midjourney.com/" rel="sponsored noopener nofollow" target="_blank">Midjourney</a> and <a href="https://leonardo.ai/" rel="sponsored noopener nofollow" target="_blank">Leonardo</a> plan pages.</li>
<li>Whether the paid plan you have actually includes commercial rights.</li>
<li>Likeness, celebrity, and trademark risk in the prompt and the output.</li>
<li>Client contract language: some NDAs forbid AI-generated creative without disclosure.</li>
</ul>
<p>This is not legal advice. Confirm current terms on vendor pages. See <a href="../workflows/commercial-image-rights.html">commercial image rights workflow</a>.</p>
<h2>Practical test</h2>
<p>Generate one real asset you would actually deliver. Compare acceptance rate, edit time, and whether a designer still has to rebuild it. Reviews: <a href="../tools/midjourney/">Midjourney</a>, <a href="../tools/leonardo-ai/">Leonardo AI</a>, <a href="../tools/canva-ai/">Canva AI</a>.</p>
<p>If you pay for two image tools you barely use, cut with the <a href="how-to-cut-ai-tool-subscriptions.html">cut subscriptions guide</a> or the <a href="../premium/">Premium</a> visual shortlist. 7-day trial; LAUNCH50 for 50% off first paid month (new users).</p>
'''}

ARTICLES['how-to-cancel-ai-tools-before-renewal.html'] = {
 'title':'How to cancel AI tools before renewal without losing work','kicker':'Renewal guide','desc':'A 14-day process for canceling unused AI subscriptions before the next charge while keeping the one tool that owns a weekly job.',
 'body':'''
<p><strong>Short answer:</strong> export anything you need, run one real task on the replacement, then cancel at least 48 hours before renewal. Do not cancel the only tool that owns a weekly workflow.</p>
<h2>14-day cancel process</h2>
<ol>
<li>List every AI subscription, renewal date, and annual vs monthly billing.</li>
<li>Mark keep / trial / cancel using the <a href="ai-stack-audit-checklist.html">stack audit checklist</a>.</li>
<li>Export chats, files, or project history you still need.</li>
<li>Run the weekly job once on the replacement (free tier first).</li>
<li>Cancel in the vendor billing portal. Screenshot confirmation.</li>
<li>Watch the next statement. Some tools bill through app stores.</li>
</ol>
<p>Related: <a href="can-i-cancel-ai-subscriptions.html">Can I cancel AI subscriptions anytime?</a> and <a href="how-to-cut-ai-tool-subscriptions.html">How to cut AI tool subscriptions</a>.</p>
<h2>When the free process is not enough</h2>
<p>If you have five-plus paid tools, mixed annual contracts, or no owner for the spend, use <a href="../premium/">Premium</a>: 30-day renewal calendar, cancel-savings tracker, and stack-audit template. Research and strategy only. 7-day free trial, then $12/month; code <strong>LAUNCH50</strong> for 50% off the first paid month (new users).</p>
'''}

ARTICLES['cursor-vs-copilot-which-to-pay-for.html'] = {
 'title':'Cursor vs Copilot: which one should you pay for?','kicker':'Straight answer','desc':'A practical way to pick one paid coding assistant. Run the same real bugfix in Cursor and GitHub Copilot before you keep both.',
 'body':'''
<p><strong>Short answer:</strong> pay for one primary coding assistant. Keep Cursor if the agent/editor workflow saves more than 30 minutes a week on real tasks. Keep Copilot if you already live in VS Code/GitHub and completions are enough. Paying for both is usually overlap.</p>
<h2>How to decide in 45 minutes</h2>
<ol>
<li>Pick one real bugfix or small feature from your repo, not a demo app.</li>
<li>Run it in <a href="../tools/cursor/">Cursor</a> and <a href="../tools/github-copilot/">GitHub Copilot</a> on the plan you actually have (or trial).</li>
<li>Score first-output acceptance rate, edit burden, and whether secrets or repos need extra controls.</li>
<li>Read training/retention terms on each vendor page before annual billing.</li>
</ol>
<p>See the full comparison: <a href="../comparisons/cursor-vs-github-copilot.html">Cursor vs GitHub Copilot</a>. Team rollout: <a href="evaluating-ai-coding-tools-team-rollout.html">security checklist</a>.</p>
<p>If you already pay for both, use the <a href="../premium/">Premium</a> coding shortlist and stack audit. Research only. 7-day free trial; code <strong>LAUNCH50</strong> for 50% off the first paid month (new users).</p>
'''}

ARTICLES['make-vs-zapier-which-to-pay-for.html'] = {
 'title':'Make vs Zapier: which automation plan should you pay for?','kicker':'Straight answer','desc':'Do not compare sticker prices. Map one real workflow, count tasks vs operations, then pick Make or Zapier (or n8n) before annual billing.',
 'body':'''
<p><strong>Short answer:</strong> Zapier is usually simpler for linear app-to-app jobs. Make is usually better when you need visual branching. n8n belongs in the mix if you can self-host. Sticker price is meaningless until you know the billing unit.</p>
<h2>The test</h2>
<ol>
<li>Map one real workflow you already do weekly.</li>
<li>Estimate monthly volume (emails, form submits, CRM updates).</li>
<li>Build the same workflow in <a href="../tools/zapier-ai/">Zapier AI</a> and <a href="../tools/make/">Make</a> on free or trial tiers.</li>
<li>Count tasks vs operations vs executions before you compare plan pages.</li>
</ol>
<p>Related: <a href="../comparisons/zapier-vs-make-vs-n8n.html">Zapier vs Make vs n8n</a>, <a href="zapier-alternatives.html">Zapier alternatives</a>, <a href="automating-client-onboarding-zapier-make.html">client onboarding automation</a>.</p>
<p>If you pay for Zapier and Make, that is overlap until proven otherwise. <a href="../premium/">Premium</a> includes an automation pricing decoder CSV. 7-day trial; <strong>LAUNCH50</strong> for 50% off first paid month (new users).</p>
'''}

ARTICLES['pick-one-ai-meeting-notes-tool.html'] = {
 'title':'Pick one AI meeting notes tool: Fireflies vs Otter vs Fathom','kicker':'Straight answer','desc':'Grade meeting tools on real calls only. Keep one paid notes tool unless a second owns a different weekly job such as CRM writeback.',
 'body':'''
<p><strong>Short answer:</strong> most teams should pay for one meeting notes tool. Test Fireflies, Otter, and Fathom on the same real meeting. Score action-item quality, vocabulary, and whether CRM handoff actually happens.</p>
<h2>30-minute protocol</h2>
<ol>
<li>Use one real meeting recording (with consent).</li>
<li>Run it through <a href="../tools/fireflies/">Fireflies</a>, <a href="../tools/otter-ai/">Otter</a>, and <a href="../tools/fathom/">Fathom</a> on current plans.</li>
<li>Grade action items, speaker labels, and industry vocabulary. Demos do not count.</li>
<li>Keep the winner. Keep a free tier of a second only if it is used weekly.</li>
</ol>
<p>Related: <a href="best-ai-meeting-tools.html">best AI meeting tools</a>, <a href="../comparisons/fireflies-vs-otter-ai.html">Fireflies vs Otter</a>, <a href="../workflows/sales-call-follow-up.html">sales call follow-up workflow</a>.</p>
<p>If you already pay for two meeting tools, cut with the <a href="how-to-cut-ai-tool-subscriptions.html">cut subscriptions guide</a> or <a href="../premium/">Premium</a> meeting-notes decision sheet. 7-day trial; <strong>LAUNCH50</strong> for 50% off first paid month (new users).</p>
'''}

ARTICLES['gamma-vs-canva-which-for-decks.html'] = {
 'title':'Gamma vs Canva: which should you pay for decks?','kicker':'Straight answer','desc':'Pick one paid deck tool. Test Gamma and Canva AI on the same real presentation brief before you keep both.',
 'body':'''
<p><strong>Short answer:</strong> pay for one deck tool. Use Gamma if you need a narrative deck from a brief. Use Canva if design templates and brand kits are the weekly job. Paying for both is usually overlap.</p>
<h2>The test</h2>
<ol>
<li>Write one real deck brief (client update, internal review, or workshop).</li>
<li>Build it in <a href="../tools/gamma/">Gamma</a> and <a href="../tools/canva-ai/">Canva AI</a> on the plan you actually have.</li>
<li>Score time-to-usable-slides, brand match, and how much you still rebuilt by hand.</li>
<li>Keep the winner. Keep a free tier of the other only if you use it weekly.</li>
</ol>
<p>See <a href="../comparisons/gamma-vs-canva-ai.html">Gamma vs Canva AI</a>.</p>
<p>If you already pay for two visual tools, use the <a href="../premium/">Premium</a> visual shortlist. 7-day trial; <strong>LAUNCH50</strong> for 50% off the first paid month (new users).</p>
'''}

ARTICLES['heygen-vs-synthesia-which-to-pay-for.html'] = {
 'title':'HeyGen vs Synthesia: which AI video tool should you pay for?','kicker':'Straight answer','desc':'Keep one paid avatar/video tool. Test HeyGen and Synthesia on the same real script before annual billing.',
 'body':'''
<p><strong>Short answer:</strong> most teams should pay for one avatar video tool. Run the same 60-second script in both. Score usable takes, voice/likeness controls, and whether you still need a human edit.</p>
<h2>Protocol</h2>
<ol>
<li>Use one real script you would actually publish.</li>
<li>Generate it in <a href="../tools/heygen/">HeyGen</a> and <a href="../tools/synthesia/">Synthesia</a>.</li>
<li>Compare first-take acceptance, export limits, and commercial-use terms on official plan pages.</li>
<li>Do not buy annual until one tool owns a weekly video job.</li>
</ol>
<p>See <a href="../comparisons/heygen-vs-synthesia.html">HeyGen vs Synthesia</a>.</p>
<p>Overlapping video seats: <a href="how-to-cut-ai-tool-subscriptions.html">cut subscriptions guide</a> or <a href="../premium/">Premium</a>. 7-day trial; <strong>LAUNCH50</strong> for 50% off first paid month (new users).</p>
'''}

ARTICLES['perplexity-vs-chatgpt-for-research.html'] = {
 'title':'Perplexity vs ChatGPT for research: which should you pay for?','kicker':'Straight answer','desc':'Use Perplexity when you need sources you can open. Use ChatGPT when the job is drafting after research. Paying for both is optional, not default.',
 'body':'''
<p><strong>Short answer:</strong> pay for Perplexity if cited research is a daily job and the free search limit gets in the way. Pay for ChatGPT if drafting and files are the weekly job. Keep both only if they own different weekly workflows.</p>
<h2>The split</h2>
<ul>
<li><a href="../tools/perplexity/">Perplexity</a>: first stop for source-backed questions.</li>
<li><a href="../tools/chatgpt/">ChatGPT</a>: drafting, files, and multimodal work after you have sources.</li>
</ul>
<p>Run the same research question in both. Count how many citations you actually opened and verified. That number beats a generic benchmark.</p>
<p>Related: <a href="../comparisons/chatgpt-vs-perplexity.html">ChatGPT vs Perplexity</a>, <a href="is-perplexity-worth-it.html">Is Perplexity worth it?</a>, <a href="perplexity-vs-google.html">Perplexity vs Google</a>.</p>
<p>If you pay for both plus Claude for the same research, that is overlap. <a href="../premium/">Premium</a> hands-on protocol helps you pick a primary. 7-day trial; <strong>LAUNCH50</strong> for 50% off first paid month (new users).</p>
'''}

ARTICLES['elevenlabs-vs-descript-which-for-audio.html'] = {
 'title':'ElevenLabs vs Descript: which should you pay for audio?','kicker':'Straight answer','desc':'ElevenLabs is for generating voice. Descript is for editing real recordings. Pay for the job you actually do weekly, not both by default.',
 'body':'''
<p><strong>Short answer:</strong> pay for ElevenLabs if you need generated or cloned voice as a weekly output. Pay for Descript if you edit podcasts or video by editing text. They overlap only if you force them to.</p>
<h2>Pick by job</h2>
<ul>
<li><a href="../tools/elevenlabs/">ElevenLabs</a>: narration, dubbing, voice agents.</li>
<li><a href="../tools/descript/">Descript</a>: transcript-based edit of real recordings.</li>
</ul>
<p>Test one real episode or one real narration brief. Keep the tool that owns that weekly job. Confirm commercial voice-rights on the vendor plan page before client work.</p>
<p>See <a href="../comparisons/elevenlabs-vs-descript.html">ElevenLabs vs Descript</a> and <a href="../workflows/podcast-editing.html">podcast editing workflow</a>.</p>
<p>Two audio seats you barely use: cut with <a href="how-to-cancel-ai-tools-before-renewal.html">cancel before renewal</a> or <a href="../premium/">Premium</a>. 7-day trial; <strong>LAUNCH50</strong> for 50% off first paid month (new users).</p>
'''}

ARTICLES['claude-code-vs-cursor-vs-copilot.html'] = {
 'title':'Claude Code vs Cursor vs Copilot','kicker':'Straight answer',
 'desc':'Keep one paid coding surface. Test Copilot, Cursor, and Claude Code on the same real bugfix before you stack seats.',
 'body':'''
<p><strong>Short answer:</strong> keep one paid coding surface as the default. Copilot if you want inline completions in the editor you already use. Cursor if you want an AI-native IDE. Claude Code if the job is terminal/agent work on a repo. Paying for two or three for the same weekly job is overlap.</p>
<h2>The split</h2>
<ul>
<li><a href="../tools/github-copilot/">GitHub Copilot</a>: completions and chat inside VS Code / JetBrains / GitHub.</li>
<li><a href="../tools/cursor/">Cursor</a>: AI-first editor. Test Composer on a real multi-file change.</li>
<li><a href="../tools/claude/">Claude</a> (Claude Code): terminal agent for repo-scale tasks. Confirm current bundling on Anthropic plan pages. Claude Code is a workflow, not a separate directory listing.</li>
</ul>
<h2>45-minute protocol</h2>
<ol>
<li>Pick one real bugfix or small feature from your repo.</li>
<li>Run it in Copilot, Cursor, and Claude Code on the plan you actually pay for (or trial).</li>
<li>Score first-output acceptance, edit burden, and whether you needed extra repo access.</li>
<li>Read training and retention terms before annual billing.</li>
<li>Keep one primary. Add a second only if it owns a different weekly job.</li>
</ol>
<p>Related: <a href="cursor-vs-copilot-which-to-pay-for.html">Cursor vs Copilot</a>, <a href="evaluating-ai-coding-tools-team-rollout.html">team rollout checklist</a>, <a href="../comparisons/cursor-vs-github-copilot.html">Cursor vs GitHub Copilot</a>.</p>
<p>If you already pay for two coding seats, use <a href="../premium/">Premium</a> coding shortlist and stack audit. 7-day trial; code <strong>LAUNCH50</strong> for 50% off the first paid month (new users).</p>
'''}
