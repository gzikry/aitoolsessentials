#!/usr/bin/env python3
"""Generate audience-based buyer guides (freelancers, students, agencies, developers, small business)."""
import html as H
import json
from datetime import datetime
from pathlib import Path

GUIDES = {
    'best-ai-tools-for-freelancers.html': {
        'kicker': 'Audience guide', 'audience': 'freelancers',
        'title': 'Best AI tools for freelancers',
        'subhead': 'A lean AI stack for solo operators: one assistant, one writing tool, one automation platform — chosen by cost per delivered project.',
        'slugs': ['chatgpt','claude','canva-ai','zapier-ai','notion-ai','grammarly'],
        'angle': ('Freelancers feel every subscription personally, so the stack has to earn its keep '
                  'monthly. The pattern that works: one general assistant for drafting and analysis, '
                  'one client-facing production tool, and one automation to kill repetitive admin. '
                  'Start free-tier everywhere; only upgrade the single tool that saves you hours weekly.'),
    },
    'best-ai-tools-for-students.html': {
        'kicker': 'Audience guide', 'audience': 'students',
        'title': 'Best AI tools for students',
        'subhead': 'Free-first AI tools for research, writing, notes, and presentations — with academic-integrity guardrails.',
        'slugs': ['perplexity','chatgpt','gamma','otter-ai','notion-ai'],
        'angle': ('Students rarely need paid plans. The free tiers of Perplexity, ChatGPT, Gamma, and '
                  'Otter cover research, drafting, slides, and lecture capture. Two rules: verify every '
                  'citation against the actual source before it goes in your work, and check your '
                  'institution\'s AI policy per course — disclosure rules differ widely.'),
    },
    'best-ai-tools-for-agencies.html': {
        'kicker': 'Audience guide', 'audience': 'agencies',
        'title': 'Best AI tools for agencies',
        'subhead': 'Team-plan decisions for content production, design, meetings, and client reporting — evaluated on seats, permissions, and margin.',
        'slugs':['claude','jasper','copy-ai','adobe-firefly','heygen','fireflies'],
        'depth': 'agencies',
        'angle': ('Agencies buy seats, not subscriptions. The evaluation axis is different from solo use: '
                  'team workspaces, permission controls, brand-voice consistency, output rights you can '
                  'transfer to clients, and per-seat cost against billable value. Consumer plans usually '
                  'break here — check commercial-use terms before client delivery.'),
    },
    'best-ai-tools-for-developers.html': {
        'kicker': 'Audience guide', 'audience': 'developers',
        'title': 'Best AI tools for developers',
        'subhead': 'Coding assistants, app builders, and automation for engineering teams — with training-policy and code-ownership notes.',
        'slugs':['cursor','github-copilot','v0','bolt-new','replit-ai','n8n'],
        'angle': ('Developer tooling decisions hinge on two things beyond raw quality: whether your code '
                  'trains vendor models (Cursor: no unless opted in; check each vendor\'s current policy) '
                  'and where suggestions run (local context vs cloud). Prototype builders like v0 and '
                  'Bolt are for scaffolding, not production paths.'),
    },
    'best-ai-tools-for-consultants.html': {
        'kicker': 'Audience guide', 'audience': 'consultants',
        'title': 'Best AI tools for consultants',
        'subhead': 'Research, deck production, meeting capture, and analysis for client work — with confidentiality as a first-class constraint.',
        'slugs':['claude','perplexity','gamma','fireflies','microsoft-copilot'],
        'angle': ('Consultants trade on trust, so data-handling terms matter as much as capability. Before '
                  'putting client material into any tool, read its training policy: Claude consumer chats '
                  'may be used for training unless opted out; business tiers differ. Prefer tools with '
                  'explicit no-training commitments on your plan tier.'),
    },
    'best-ai-tools-for-healthcare-admin.html': {
        'kicker': 'Audience guide', 'audience': 'healthcare administrators and medical professionals',
        'title': 'Best AI tools for healthcare admin',
        'subhead': 'Documentation drafts, literature lookup, and practice-admin workflows for medical teams — with no implied HIPAA, FDA, or clinical-decision certification.',
        'slugs':['heidi-health','openevidence','dragon-copilot','microsoft-copilot','perplexity','otter-ai'],
        'angle': ('Healthcare buyers need a different filter than consumer AI shoppers. Separate '
                  'administrative drafting from anything that touches identifiable patient data, billing, '
                  'or the signed medical record. Heidi Health is the public self-serve documentation '
                  'starting point; OpenEvidence is official-homepage-free literature lookup for healthcare '
                  'professionals; Dragon Copilot is Microsoft quote-based enterprise documentation. '
                  'Vendor HIPAA marks are claims to verify in contract review, not certifications by this site. '
                  'Do not paste PHI into a general tool during a trial.'),
    },
    'best-ai-tools-for-lawyers.html': {
        'kicker': 'Audience guide', 'audience': 'lawyers and in-house counsel',
        'title': 'Best AI tools for lawyers',
        'subhead': 'Confidentiality-first tools for legal research, contract review, and drafting — with no implied privilege, bar, or legal-advice certification.',
        'slugs':['harvey','spellbook','cocounsel','claude','perplexity','microsoft-copilot'],
        'angle': ('Legal buyers start with privilege, not features. Harvey is the quote-based enterprise '
                  'platform for firms and in-house teams. Spellbook is Word-native contract review and drafting. '
                  'CoCounsel Legal is Thomson Reuters’ Westlaw- and Practical Law-grounded assistant; the only '
                  'official dollar figure recorded here is Westlaw Advantage with CoCounsel Essentials starting '
                  'at $415.35/month. Consumer chat tiers are the wrong place for client-identifiable files. '
                  'Verify every citation in a primary research product before advice or filing.'),
    },
    'best-ai-tools-for-teachers.html': {
        'kicker': 'Audience guide', 'audience': 'teachers and instructional coaches',
        'title': 'Best AI tools for teachers',
        'subhead': 'Free-first tools for lesson plans, rubrics, slides, and family emails — with no implied FERPA, grading, or student-data certification.',
        'slugs':['magicschool','khanmigo','canva-ai','gamma','chatgpt','perplexity'],
        'depth': 'teachers',
        'angle': ('Teachers should start on official free education tiers, not a $20 chatbot, unless a general '
                  'assistant already owns a weekly task. MagicSchool publishes a $0 individual teacher plan and '
                  'Plus at $12.99/month or $8.33/month billed annually. Khanmigo’s official teacher page states '
                  'teacher tools are free; learner and family plans are $4/month or $44/year, and classroom student '
                  'access is a district implementation, not a teacher-account toggle. Vendor FERPA/COPPA marks are '
                  'claims to verify with your school. Do not paste identifiable student records into a personal chat.'),
    },
    'best-ai-tools-for-nonprofits.html': {
        'kicker': 'Audience guide', 'audience': 'nonprofit staff and grant writers',
        'title': 'Best AI tools for nonprofits',
        'subhead': 'Grant-writing and development tools with published free or trial paths — and no implied fundraising, tax, or award certification.',
        'slugs':['grantable','instrumentl','chatgpt','claude','notion-ai','canva-ai'],
        'angle': ('Small nonprofits should not start on a $299/month grant database. Grantable publishes a real '
                  'free plan (5 messages/day) plus Starter at $50/month and Pro at $150/month, with a one-year 50% '
                  'discount to $25/$75 for qualifying 501(c)(3)s under about $500K. Instrumentl is the paid discovery '
                  'and lifecycle platform: official Discover is $299/month billed annually or $349 monthly, with a '
                  '14-day free trial. Vendor win-rate and revenue-uplift claims are marketing. Keep eligibility, '
                  'budgets, and authorized submissions with a human grant lead.'),
    },
    'best-ai-tools-for-podcast-shows.html': {
        'kicker': 'Audience guide', 'audience': 'podcasters and show producers',
        'title': 'Best AI tools for podcasters',
        'subhead': 'Record, enhance, edit, clip, and voice a weekly show — with published free or trial paths and no implied music-rights or likeness certification.',
        'slugs':['riverside-fm','adobe-enhance-speech','descript','elevenlabs','canva-ai','chatgpt'],
        'angle': ('Start on official free recording and cleanup tiers before stacking Descript plus a voice lab. '
                  'Riverside publishes Free at $0 with a 2-hour one-off multi-track allowance, then Pro at $24/month '
                  'billed annually or $29 monthly. Adobe Podcast publishes Free Enhance Speech and Studio limits and '
                  'a 30-day Premium trial, but no official USD Premium price on the plans page. Descript and ElevenLabs '
                  'stay in the stack for transcript editing and voiceover. Check guest consent, voice-clone rights, '
                  'and watermarks before you publish.'),
    },
    'best-ai-tools-for-property-managers.html': {
        'kicker': 'Audience guide', 'audience': 'property managers and independent landlords',
        'title': 'Best AI tools for property managers',
        'subhead': 'Listings, rent follow-up, and maintenance notes with published free or trial paths — and no implied fair-housing or tenant-screening certification.',
        'slugs':['landlord-studio','tenantcloud','chatgpt','canva-ai','notion-ai','otter-ai'],
        'angle': ('Small portfolios should not start on a quote-only enterprise PMS. Landlord Studio publishes a '
                  'Go plan at $0 for up to 3 units, then Pro at $12/month or $144/year. TenantCloud publishes Starter '
                  'at $25/month or $180/year, with Growth and Pro self-serve tiers and Business from $100/month. '
                  'Use ChatGPT or Canva only on de-identified amenity lists. Keep applicant Social Security numbers, '
                  'screening reports, and bank details out of consumer chat. A human still owns fair-housing review.'),
    },
}

# Verified seat pricing and rights notes for the depth sections. Amounts and check dates
# come from data/tool_sources.json; do not add a figure that is not sourced there.
AGENCY_SEAT_DATA = {
    'claude': {
        'price': '$20/seat/mo (Standard teams, 2-150 users); Premium seats $100/seat/mo',
        'checked': '2026-08-25',
        'rights': 'Consumer Terms govern Free/Pro; Team and Enterprise add commercial terms. '
                  'Check the training policy for the tier you buy.',
        'rights_url': 'https://www.anthropic.com/legal/consumer-terms',
    },
    'jasper': {
        'price': 'Pro $69/seat/mo monthly or $59/seat/mo yearly (1 seat included); Business custom',
        'checked': '2026-08-25',
        'rights': 'Pro includes 2 Brand Voices, 5 Knowledge assets, 3 Audiences. Client-delivery '
                  'rights sit in the main Terms — review before reselling output.',
        'rights_url': 'https://www.jasper.ai/legal/terms',
    },
    'copy-ai': {
        'price': 'Chat $29/mo (5 seats) or $24/mo billed annually; Growth from $1,000/mo (75 seats)',
        'checked': '2026-08-25',
        'rights': 'Seat counts rise steeply between tiers — price the tier that matches your '
                  'actual headcount, not the entry plan.',
        'rights_url': 'https://www.copy.ai/terms-of-service',
    },
    'adobe-firefly': {
        'price': 'Standard $9.99/mo (2,000 credits); Pro $19.99/mo (4,000); Pro Plus $49.99/mo',
        'checked': '2026-08-25',
        'rights': 'Adobe generative-AI user guidelines govern commercial use; Firefly is positioned '
                  'as commercially safe, which matters when output goes to a client.',
        'rights_url': 'https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html',
    },
    'heygen': {
        'price': 'Creator $29/mo (600 credits); Business $149/mo + $20 per extra seat',
        'checked': '2026-08-25',
        'rights': 'Avatar consent and likeness rights are the risk here; confirm the terms for '
                  'each presenter you create.',
        'rights_url': 'https://www.heygen.com/terms',
    },
    'fireflies': {
        'price': 'Pro $18/seat/mo monthly or $10/seat/mo billed annually; Business $29/seat/mo',
        'checked': '2026-08-25',
        'rights': 'Recording consent is the compliance issue: you are capturing client calls. '
                  'A written recording policy is a prerequisite, not an afterthought.',
        'rights_url': 'https://fireflies.ai/terms-of-service',
    },
}

AGENCY_DEPTH = """<h2>What agencies actually get wrong about AI seats</h2>
<p>Solo buyers optimise for capability. Agencies have to optimise for four things the consumer plans do not address: <strong>seat economics</strong>, <strong>permission boundaries</strong>, <strong>brand consistency across writers</strong>, and <strong>the right to hand output to a client</strong>. A tool that is excellent for one person often becomes a liability at eight, because the per-seat price is only the visible cost.</p>
<p>The hidden costs are the ones that show up in month two: seats you bought for contractors who finished their engagement, a plan tier that silently excludes the feature your senior writer needs, and output you cannot legally deliver because the plan you are on reserves commercial rights for a higher tier.</p>

<h2>Per-seat cost, priced for a real team</h2>
<p>Prices below are per official vendor pages as checked. Where a plan includes an unusual seat count, that matters more than the headline number.</p>
<table>
<thead><tr><th>Tool</th><th>Verified seat pricing</th><th>Checked</th></tr></thead>
<tbody>
<tr><td><strong>Claude</strong></td><td>{claude}</td><td>{claude_d}</td></tr>
<tr><td><strong>Jasper</strong></td><td>{jasper}</td><td>{jasper_d}</td></tr>
<tr><td><strong>Copy.ai</strong></td><td>{copy_ai}</td><td>{copy_ai_d}</td></tr>
<tr><td><strong>Adobe Firefly</strong></td><td>{firefly}</td><td>{firefly_d}</td></tr>
<tr><td><strong>HeyGen</strong></td><td>{heygen}</td><td>{heygen_d}</td></tr>
<tr><td><strong>Fireflies.ai</strong></td><td>{fireflies}</td><td>{fireflies_d}</td></tr>
</tbody>
</table>
<p class="monetization-note">These are official published amounts with check dates, not quotes. Teams plans, volume discounts, and annual prepayment change the real number — confirm at signup.</p>

<h2>Do the seat math before you buy</h2>
<p>A worked example using the verified numbers, for a seven-person agency with three writers, two designers, one producer, and one account lead:</p>
<ul>
<li><strong>Writing layer (3 seats).</strong> Jasper Pro at $59/seat/mo billed annually is <strong>$177/month</strong>. Claude Team at $20/seat/mo is <strong>$60/month</strong> for the same three people. The difference is roughly $117/month — about $1,400/year — and it buys brand-voice controls rather than raw writing quality.</li>
<li><strong>Creative layer (2 seats).</strong> Firefly Pro at $19.99/seat/mo is <strong>$39.98/month</strong> for 4,000 credits per seat. Credits, not seats, are the real constraint for image-heavy work.</li>
<li><strong>Meetings layer (7 seats).</strong> Fireflies Pro at $10/seat/mo billed annually is <strong>$70/month</strong> across the whole team. This is the cheapest per-seat layer and usually the easiest to justify.</li>
<li><strong>Producer and account lead.</strong> Do not buy them a writing seat. Give them the shared assistant and the meeting tool; a seat they open twice a month is the most common wasted line on an agency's AI invoice.</li>
</ul>
<p>Total for that shape lands near <strong>$290-350/month</strong> depending on which writing path you take. The single biggest lever is the writing layer, and the decision there is brand consistency versus cost.</p>

<h2>Permissions, client data, and what you are allowed to deliver</h2>
<p>Two questions decide most agency rollouts, and neither is answered by a feature comparison.</p>
<p><strong>Who can see what?</strong> Shared workspaces are the reason agencies move off individual plans, but a shared workspace also means a junior can read a senior's client drafts. Check whether the plan separates projects or workspaces per client before you consolidate everyone onto one account.</p>
<p><strong>Can you deliver the output?</strong> Commercial-use rights are plan-specific. On Claude, the Consumer Terms govern Free and Pro while Team and Enterprise add commercial terms. On Jasper, delivery rights sit in the main Terms. On Adobe Firefly, the generative-AI user guidelines are what make it the safer default for client-facing visuals. The practical rule: <em>read the rights page for the exact tier you are buying, and do it before the first client deliverable, not after.</em></p>
<p><strong>Meeting recording is a consent problem, not a tooling problem.</strong> Any tool that joins a client call — Fireflies included — captures client conversation. A written recording policy that you state in the call is a prerequisite. This is the one area where a cheap seat can create an expensive conversation.</p>

<h2>Rollout order that survives month two</h2>
<ol>
<li><strong>Start with the meeting layer.</strong> It is the cheapest per seat, the benefit is obvious to everyone in the room, and it produces a searchable record that improves every other workflow.</li>
<li><strong>Add one assistant for the whole team</strong> before adding specialists. A shared assistant replaces scattered personal subscriptions and gives you one place to answer the data-handling question.</li>
<li><strong>Add the writing layer only when brand consistency is a real problem.</strong> If two writers produce inconsistent client copy, brand-voice tooling earns its premium. If they do not, you are paying $1,400/year for a feature you will not use.</li>
<li><strong>Add creative generation last.</strong> Image and video credits are the hardest to forecast, and the rights question is the most consequential because the output is most visible to clients.</li>
</ol>

<h2>Agency AI questions we get asked</h2>
<details><summary>Should an agency buy team plans or individual subscriptions?</summary><p>Team plans, once you pass roughly three people. Individual subscriptions cannot be administered — you cannot offboard a departing employee, you cannot enforce a permission boundary per client, and the data-handling terms are written for a consumer. The visible per-seat premium is usually smaller than the administrative cost of not having it.</p></details>
<details><summary>How do we stop paying for seats nobody uses?</summary><p>Audit seats monthly against actual logins, not against who asked for one. Contractors and part-time contributors are the usual source of waste — buy them seats for the engagement and remove them when it ends. Most vendors bill per active seat, so an unused seat is a pure loss.</p></details>
<details><summary>Which tools can we safely use on client work?</summary><p>Start with the rights page for the tier you are on, not the marketing page. Firefly is the safest default for client-facing visuals because Adobe publishes explicit generative-AI guidelines. For writing, Team and Enterprise tiers generally carry commercial terms that consumer plans do not. Never assume a consumer plan you tested personally grants delivery rights at work.</p></details>
<details><summary>Do we need to tell clients we use AI?</summary><p>Increasingly yes, and it is usually contractual rather than optional. Check your master service agreements for AI disclosure clauses, and state your recording policy in the call before any meeting tool joins. Being able to describe your process plainly is a sales advantage with sophisticated clients, not a risk.</p></details>
"""


# Placeholder key -> slug, because the template uses short names ({firefly}) while the
# data uses slugs (adobe-firefly).
DEPTH_KEY_MAP = {
    'claude': 'claude', 'jasper': 'jasper', 'copy_ai': 'copy-ai',
    'firefly': 'adobe-firefly', 'heygen': 'heygen', 'fireflies': 'fireflies',
}


def _fill(values):
    """Flatten seat data into .format() keys: {claude} for price, {claude_d} for the date."""
    out = {}
    for key, slug in DEPTH_KEY_MAP.items():
        d = values.get(slug)
        if not d:
            continue
        out[key] = d['price']
        out[key + '_d'] = d['checked']
    return out


DEPTH_FILL = _fill(AGENCY_SEAT_DATA)

TEACHERS_DEPTH = """<h2>The teacher-buying situation is unusual: the best options are free</h2>
<p>Teachers are the one audience where the correct answer is usually <strong>not to pay at all</strong>. Two education-specific platforms publish real free teacher tiers, and the general assistants your school may already license cover the rest. The decision is therefore not "which tool is best" but "which of the free tiers actually fits the task, and where does a paid plan start to earn its place".</p>

<h2>What the free tiers actually include</h2>
<table>
<thead><tr><th>Tool</th><th>Free tier</th><th>Paid step</th></tr></thead>
<tbody>
<tr><td><strong>MagicSchool</strong></td><td>$0 forever-free individual teacher plan</td><td>Plus $12.99/month, or $8.33/month billed annually ($99.96/year). District Enterprise is quote-only.</td></tr>
<tr><td><strong>Khanmigo</strong></td><td>Teacher tools free in supported locales</td><td>Learners and families $4/month or $44/year. District classroom rollout is quote-only.</td></tr>
<tr><td><strong>Canva AI</strong></td><td>Free plan with limited AI credits</td><td>Paid plans unlock more generation and brand controls</td></tr>
<tr><td><strong>Gamma</strong></td><td>Free plan with credit limits</td><td>Paid plans for more decks and faster generation</td></tr>
<tr><td><strong>ChatGPT / Perplexity</strong></td><td>Capable free tiers</td><td>Paid plans add higher limits and stronger models</td></tr>
</tbody>
</table>
<p class="monetization-note">Amounts are official published prices with check dates, not quotes. District and school-wide pricing is quote-only for both MagicSchool and Khanmigo.</p>

<h2>Which free tier fits which task</h2>
<ul>
<li><strong>Lesson plans, rubrics, quiz drafts, family emails.</strong> MagicSchool is purpose-built for these and its free plan is a real plan, not a trial. Its generation limits are published, so you can see the ceiling before you hit it.</li>
<li><strong>Tutoring and learner-facing practice.</strong> Khanmigo. Note the access rule that catches schools out: the teacher tools being free does not automatically give students Khanmigo access. Learner and parent subscriptions are governed by official age and geographic rules, so a teacher cannot simply issue student accounts.</li>
<li><strong>Slides and visuals.</strong> Gamma for deck structure, Canva AI for templated classroom materials. Both have workable free tiers; expect credit limits on generation.</li>
<li><strong>Research and drafting outside a purpose-built tool.</strong> Perplexity for anything needing citations, ChatGPT for general drafting. Check your school's AI policy per course before using either for student-facing material.</li>
</ul>

<h2>Why teachers should stop before paying for a general assistant</h2>
<p>A $20/month general chatbot is the wrong purchase for most teachers, for three reasons. It duplicates capabilities the school may already license. It has no classroom-specific scaffolding — you supply the pedagogy in the prompt every time. And the plan you tested personally is a consumer plan, which typically does not carry the data-handling terms an institution needs.</p>
<p>The exception is real but narrow: if one general assistant already owns a recurring weekly task for you — drafting parent communication, adapting a text to three reading levels — then a paid plan is defensible. That is a task-specific justification, not a capability one.</p>

<h2>Safety, student data, and what these tools are not</h2>
<p>This is the section that matters most, and it is where most "best AI tools for teachers" pages are dangerously quiet.</p>
<ul>
<li><strong>These are not student-data systems.</strong> Do not paste identifiable student information — names, IEPs, behavioural records, grades — into a general AI tool. Purpose-built education tools make claims about FERPA, COPPA, and SOC 2; those are <em>vendor claims to verify through your district</em>, not certifications made by this site or any reviewer.</li>
<li><strong>These are not grading systems.</strong> Use them to draft practice questions and feedback scaffolds. A grade that decides a student's path should not be the output of an unreviewed model.</li>
<li><strong>No implied institutional approval.</strong> Nothing here substitutes for your school's or district's AI policy. Disclosure rules differ widely between institutions and even between courses within one institution.</li>
<li><strong>Verify anything cited.</strong> Research-backed answers from Perplexity or a general assistant still need opening the actual source before the material reaches students.</li>
</ul>

<h2>District and school-wide buyers</h2>
<p>If you are buying for a school or district rather than yourself, the calculus changes entirely. Both MagicSchool and Khanmigo route district pricing through a quote, which means contract review, data-processing terms, and a roll-out plan rather than a credit-card signup. Ask three questions in that process: <strong>what is the data-retention and deletion policy</strong>, <strong>which staff roles get access to student-linked features</strong>, and <strong>what is the offboarding path when a teacher leaves or a contract ends</strong>. The last one is the question most districts forget and the one that causes the most trouble.</p>

<h2>Teacher AI questions we get asked</h2>
<details><summary>Is there really a free AI tool for teachers, or is it a trial?</summary><p>MagicSchool publishes a forever-free individual teacher plan at $0 with published generation limits. Khanmigo's official teacher page states teacher tools are free in supported locales. Both are genuinely free tiers rather than trials, but both limit generation and both route district features through a quote.</p></details>
<details><summary>Do I need to worry about student privacy if I only use it myself?</summary><p>Yes, the moment student information enters the tool. Drafting a generic lesson plan carries no student data. Summarising a specific student's progress or writing an IEP narrative does — and general consumer tools are not the right place for that. Keep identifiable student information inside systems your district has approved.</p></details>
<details><summary>Can my students use Khanmigo because my teacher account is free?</summary><p>No. Teacher-free access does not extend to students. Learner and family subscriptions follow official age and geographic rules, and district classroom access is a quote-based arrangement. Confirm eligibility rather than assuming student access follows from your teacher account.</p></details>
<details><summary>What is worth paying for as a teacher?</summary><p>Usually one thing, chosen by the task it replaces. If generation limits interrupt real work more than once a week, MagicSchool Plus at $8.33/month billed annually is the cheapest purpose-built upgrade. If you need student-facing practice with guardrails, a family or learner Khanmigo subscription at $44/year is cheaper than most general assistants. Upgrade only after a free tier has demonstrably slowed you down.</p></details>
"""


DEPTH_BLOCKS = {
    'agencies': AGENCY_DEPTH,
    'teachers': TEACHERS_DEPTH,
}

HEADER = '<header class="global-nav"><a class="brand" href="../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="../tools/index.html">Tools</a><a href="../comparisons/best-ai-tools.html">Best AI tools</a><a href="../categories/index.html">Categories</a><a href="../articles/index.html">Guides</a><a href="../benchmarks/">Benchmarks</a>\n</nav><a class="nav-cta" href="../legal/affiliate-disclosure.html">Disclosure</a></header>'

FOOTER = '''<footer class="footer">
    <span>© 2026 AIToolsEssentials</span>
    <a href="../advertise/index.html" rel="nofollow">Advertise</a>
    <a href="../submit-tool.html" rel="nofollow">Submit a tool</a>
    <a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
    <a href="mailto:contact@aitoolsessentials.com">Contact</a>
  <a href="../legal/about.html">About</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a><a href="../legal/corrections.html">Corrections</a></footer><script src="../js/site.js" defer></script>
<script src="../js/analytics.js" defer></script>'''


def _e(x): return H.escape(str(x))


def generate(root: Path) -> int:
    tools = {t['slug']: t for t in json.loads((root/'data/tools.json').read_text())}
    srcs = {x['slug']: x for x in json.loads((root/'data/tool_sources.json').read_text())['tools']}
    today = datetime.today().strftime('%B %d, %Y')
    made = 0
    articles_dir = root/'articles'
    for fname, spec in GUIDES.items():
        cards = ''
        picks = []
        for s in spec['slugs']:
            t = tools[s]
            checked = srcs[s].get('pricing_checked_date', '')
            cards += (f'<article class="tool-pick"><div class="pick-head"><h3>{_e(t["name"])}</h3>'
                      f'<span class="pick-score">{t.get("rating","—")}/5 editorial</span></div>'
                      f'<p>{_e(t.get("summary",""))}</p>'
                      f'<p class="pick-meta">Category: {_e(t["category"])} · Pricing verified {_e(checked)}</p>'
                      f'<div class="pick-actions"><a class="button button-blue" href="../tools/{s}/">Read review</a>'
                      f'<a class="text-link" href="../legal/editorial-methodology.html">How we score</a></div></article>')
            picks.append(t['name'])
        depth_html = ''
        if spec.get('depth') and spec['depth'] in DEPTH_BLOCKS:
            depth_html = DEPTH_BLOCKS[spec['depth']].format(**DEPTH_FILL)
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{_e(spec['title'])}: {_e(spec['subhead'])}"><title>{_e(spec['title'])} — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css"><!-- AIT SEO START -->
  <link rel="canonical" href="https://aitoolsessentials.com/articles/{fname}">
  <meta property="og:site_name" content="AIToolsEssentials"><meta property="og:type" content="article">
  <meta property="og:title" content="{_e(spec['title'])} — AIToolsEssentials">
  <meta property="og:description" content="{_e(spec['subhead'])}">
  <meta property="og:url" content="https://aitoolsessentials.com/articles/{fname}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "Article", "name": "{_e(spec['title'])}", "headline": "{_e(spec['title'])}", "description": "{_e(spec['subhead'])}", "url": "https://aitoolsessentials.com/articles/{fname}", "author": {{"@type": "Organization", "name": "AIToolsEssentials"}}, "publisher": {{"@type": "Organization", "name": "AIToolsEssentials"}}}}</script>
  <!-- AIT SEO END -->

  <!-- AIT FAVICON START -->
  <link rel="icon" href="../assets/aitools-bot-mark.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../assets/aitools-bot-logo-256.png">
  <!-- AIT FAVICON END -->
</head><body>{HEADER}<main><section class="scene scene-light article-hero"><p class="kicker light">{_e(spec['kicker'])}</p><h1>{_e(spec['title'])}</h1><p>{_e(spec['subhead'])}</p><p class="last-updated">Official sources checked {today} · Editorial scores are AIToolsEssentials ratings, not benchmarks · Independent hands-on results not yet published</p><div class="actions"><a class="button button-blue" href="../tools/index.html">Browse all tools</a><a class="button button-dark" href="../downloads/premium/aitools-premium-comparison-archive-2026-09.csv">Download comparison archive</a></div></section>
<section class="scene scene-light"><article class="article-shell">
<h2>How this stack is chosen</h2><p>{_e(spec['angle'])}</p>
<h2>The shortlist</h2>
{cards}
{depth_html}<h2>Before you pay for anything</h2>
<p>Run each finalist's trial checklist on one real task. Record time-to-result, corrections needed, and what the plan actually costs at your volume — then decide. Our <a href="../downloads/ai-tool-evaluation-scorecard.html">free scorecard</a> gives you the template.</p>
<p class="monetization-note">Official product links remain in place until affiliate programs are approved and verified.</p>
</article></section>
<section class="newsletter-panel"><div><span>AI Tool Evaluation Scorecard</span><h2>Decide with evidence, not demos</h2><p>Compare candidates on workflow fit, quality, review time, privacy, collaboration, cost, and ROI.</p><p class="affiliate-inline">No email required. No newsletter signup.</p></div><div class="newsletter-actions"><a class="button button-blue" href="../downloads/ai-tool-evaluation-scorecard.html">Open scorecard</a><a class="button button-dark" href="../benchmarks/">See benchmark evidence</a></div></section>

</main><div id="share-row" hidden></div>
  {FOOTER}</body></html>'''
        (articles_dir/fname).write_text(page)
        made += 1
    return made


if __name__ == '__main__':
    print(generate(Path(__file__).resolve().parent.parent))
