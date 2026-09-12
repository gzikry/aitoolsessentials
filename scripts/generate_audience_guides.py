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



ASSISTANTS_DEPTH = """<h2>What each assistant actually costs</h2>
<p>Prices below are official published amounts with check dates. Note where the official page does <em>not</em> publish a figure — that is recorded as such rather than estimated.</p>
<table>
<thead><tr><th>Assistant</th><th>Free tier</th><th>Paid step</th><th>Checked</th></tr></thead>
<tbody>
<tr><td><strong>ChatGPT</strong></td><td>$0</td><td>Paid self-service plans are billed per user per month; exact localized prices were not exposed by the official pricing page during verification, so no figure is stated here</td><td>2026-08-25</td></tr>
<tr><td><strong>Claude</strong></td><td>$0</td><td>Pro $17/mo with $200 annual prepayment, or $20 month-to-month. Max from $100/mo</td><td>2026-08-25</td></tr>
<tr><td><strong>Gemini</strong></td><td>$0</td><td>Google AI Pro $19.99/mo; Ultra from $99.99/mo</td><td>2026-08-25</td></tr>
<tr><td><strong>Grok</strong></td><td>$0</td><td>SuperGrok $30/mo; SuperGrok Plus $100/mo</td><td>2026-08-25</td></tr>
<tr><td><strong>Mistral Le Chat</strong></td><td>$0</td><td>Pro $14.99/mo; Team $24.99/user/mo (excl. tax)</td><td>2026-08-25</td></tr>
<tr><td><strong>DeepSeek</strong></td><td>Free web chat</td><td>No official paid consumer or team plan located</td><td>2026-08-25</td></tr>
<tr><td><strong>Meta AI</strong></td><td>Free</td><td>Meta states higher usage is available via subscription plans but publishes no plan names, prices, or limits</td><td>2026-08-25</td></tr>
<tr><td><strong>Poe</strong></td><td>Free daily points</td><td>From $49.99/yr (~$4.17/mo) up to $2,499.99/yr (~$208.33/mo) in five tiers</td><td>2026-08-25</td></tr>
</tbody>
</table>
<p class="monetization-note">Two entries deliberately show no dollar amount. ChatGPT's and Meta AI's official pages did not publish verifiable consumer figures at check time, and this site does not print an amount it cannot source.</p>

<h2>How to choose in ten minutes</h2>
<p>Most people over-research this decision and then buy on a feature they never use. The three questions that actually separate these products:</p>
<ol>
<li><strong>Where does your work already live?</strong> If it is Google Docs, Gmail, and Android, Gemini's inclusion in Workspace editions removes a decision entirely. If it is a corporate Microsoft tenant, Copilot is already partly provisioned — Microsoft 365 Copilot Chat works for work or education without an additional Copilot licence. Buying against your existing stack is usually cheaper than buying the best standalone model.</li>
<li><strong>Do you need your assistant to read long documents?</strong> This is where Claude is distinctive — sustained long-context work where the whole document stays coherent. If your job is long contracts, policy documents, or research synthesis, that capability is worth a premium. If your job is short drafting and questions, it is not.</li>
<li><strong>Do you need current information with visible sources?</strong> That is a search problem, not an assistant problem, and it points at Perplexity or Gemini rather than a chat model.</li>
</ol>

<h2>The free tiers are more capable than most people assume</h2>
<p>Every assistant in the table above has a usable free tier, and several are genuinely good rather than crippled trials. The honest test: run your single most repeated weekly task on the free tier for two weeks. If it completes without hitting a limit that interrupts real work, you do not have a reason to pay — and "I might need more" is not a reason.</p>
<p>Upgrade when a <em>published, specific limit</em> interrupts you more than once a week. That is a measurable trigger. Anything vaguer means you are buying reassurance, not capability.</p>

<h2>What matters beyond the model</h2>
<ul>
<li><strong>Data handling on the tier you are buying.</strong> Consumer tiers and business tiers carry different terms at every vendor here. Anthropic publishes its training policy explicitly; Google and OpenAI publish theirs; Mistral documents admin-level data controls. Check the policy for your plan, not the vendor's reputation.</li>
<li><strong>Team administration.</strong> Claude Team supports 2-150 users with Standard seats at $20/seat/mo and Premium at $100/seat/mo. Microsoft Copilot Business lists at a promotional $18/user/mo paid yearly against a $21 list. If you need to onboard and offboard people, an individual plan is the wrong shape regardless of model quality.</li>
<li><strong>What you can take with you.</strong> Export, API access, and whether your conversation history is portable differ widely. Poe is the outlier here — it is a multi-model front end rather than a single vendor, priced from $49.99/year.</li>
</ul>

<h2>Assistant questions we get asked</h2>
<details><summary>Which AI assistant is actually the best?</summary><p>There is no single answer, which is why this page scores eight of them rather than crowning one. Claude leads on long-document editing, Gemini on ecosystem integration if you use Google products, ChatGPT on breadth and ecosystem, Grok on newest-model velocity and real-time information. The right question is which one fits the work you actually repeat.</p></details>
<details><summary>Should I pay for two assistants?</summary><p>Usually not. Two paid assistants is the most common form of AI subscription overlap: capability that duplicates rather than adds. The exception is a genuine split of jobs — a long-context editor plus a search-and-citations tool are doing different work. Two general chat assistants are not.</p></details>
<details><summary>Is the free tier enough for professional work?</summary><p>Often yes, and you should prove it before upgrading. Run your most repeated task for two weeks on free. If a specific published limit interrupts you more than once a week, upgrade that tool. If not, you have your answer for $0.</p></details>
<details><summary>Does my employer's licence cover personal use?</summary><p>No. A work Copilot or Workspace licence is administered by your employer, and using it for personal work typically breaches the acceptable-use terms. Personal use needs a personal plan. If you need both, that is a legitimate reason to hold two — and it is a different situation from paying twice for the same capability.</p></details>
"""

SEARCH_DEPTH = """<h2>AI search is a different purchase from an AI assistant</h2>
<p>An assistant generates a plausible answer. An AI search tool finds something and shows you where it came from. If your task requires a source you can open and check, you are buying search — and the deciding question is not model quality but <strong>citation behaviour</strong>: does the tool keep sources visible, and can you verify each one.</p>

<h2>What each search tool costs</h2>
<table>
<thead><tr><th>Tool</th><th>Free tier</th><th>Paid step</th><th>Checked</th></tr></thead>
<tbody>
<tr><td><strong>Perplexity</strong></td><td>Standard/Free plan</td><td>Consumer Pro and Max dollar prices were not exposed on the reviewed public pages. Enterprise Pro is $40/seat monthly or $400/seat annually</td><td>2026-08-25</td></tr>
<tr><td><strong>You.com</strong></td><td>Free chat plan with unlimited Smart Agent access</td><td>Public pricing page primarily lists APIs: Web Search $5/1,000 calls, Contents $1/1,000 pages, Answer $5/1,000 calls, Research from $12/1,000 calls</td><td>2026-08-25</td></tr>
<tr><td><strong>Gemini</strong></td><td>$0</td><td>Google AI Pro $19.99/mo; Ultra from $99.99/mo</td><td>2026-08-25</td></tr>
<tr><td><strong>NotebookLM</strong></td><td>Free (now Gemini Notebook)</td><td>No paid consumer subscription published</td><td>2026-09-01</td></tr>
<tr><td><strong>Grok</strong></td><td>$0</td><td>SuperGrok $30/mo; real-time access is the differentiator</td><td>2026-08-25</td></tr>
</tbody>
</table>
<p class="monetization-note">Where an official page did not publish a figure, none is stated. That is a deliberate policy, not an oversight.</p>

<h2>The distinction that decides it: web search vs your own documents</h2>
<p>These tools answer two different questions and are often conflated.</p>
<ul>
<li><strong>Searching the open web.</strong> Perplexity is built around keeping sources visible while answering. You.com is search-first with multiple agent modes. Both are for questions where the answer exists somewhere public.</li>
<li><strong>Searching documents you already have.</strong> NotebookLM (now Gemini Notebook) is the clearest case in the whole catalogue: it grounds answers in files <em>you uploaded</em> — PDFs, websites, YouTube videos, audio, Google Docs and Slides — with citations and an Audio Overview feature, and it is free for individuals. If your problem is "I have 40 documents and cannot find the sentence I need", this is a different and often better fit than a web search tool.</li>
</ul>
<p>Choosing the wrong one is the common mistake: people buy web-search tools to interrogate their own files, or expect a document tool to know about this week.</p>

<h2>How to test citation reliability before paying</h2>
<ol>
<li><strong>Ask something you already know the answer to</strong>, where the answer is in a specific document you can open. Check whether the tool cites that document and whether the cited passage actually supports the claim.</li>
<li><strong>Ask something with a false premise.</strong> A tool that invents a confident, well-formatted answer to a question with no true answer is telling you how it will behave on the questions you cannot check. This is the single most informative test, and it takes two minutes.</li>
<li><strong>Ask a question whose answer changed recently.</strong> This separates tools with live retrieval from ones leaning on training data.</li>
<li><strong>Count how many citations you had to open.</strong> If you verify every source, the tool is a research accelerator. If you verify none and trust the summary, you have a liability.</li>
</ol>

<h2>Search-engine-optimisation traffic is not your audience</h2>
<p>Worth noting if you publish: AI search tools are heavily used by people auditing sites, which produces search-console impressions from operator queries rather than readers. Judge this category by citations you can verify, not by traffic patterns.</p>

<h2>AI search questions we get asked</h2>
<details><summary>Is Perplexity better than Google for research?</summary><p>For questions where you need to see and open sources, yes — that is the design. For navigational queries, shopping, and local results, a conventional search engine remains better. Most researchers end up using both, and that is not a failure of either.</p></details>
<details><summary>Can I use an AI search tool to interrogate my own documents?</summary><p>Use a document-grounded tool instead. NotebookLM ingests your PDFs, Docs, Slides, audio, and video and answers from them with citations, free for individuals. A web-search tool will answer from the public web and may not know your file exists.</p></details>
<details><summary>How do I know the citations are real?</summary><p>Open them. Every time, at least while you are deciding whether to trust the tool. A citation that does not support the claim is worse than no citation, because it looks like verification.</p></details>
<details><summary>Should I pay for an AI search subscription?</summary><p>Only if a published limit interrupts real work. Free tiers in this category are capable, and the paid steps mostly buy query volume and access to stronger models. Test on free first, then upgrade the tool that demonstrably slows you down.</p></details>
"""

REALESTATE_DEPTH = """<h2>The real constraint for agents is not the model</h2>
<p>Real-estate work has three properties that shape every tooling decision: you handle <strong>regulated advertising</strong>, you handle <strong>personally identifying client information</strong>, and you compete on <strong>responsiveness</strong>. A tool that is excellent for general marketing can be actively dangerous here, because listing copy and client communication sit under fair-housing and disclosure rules that no AI tool enforces for you.</p>
<p>This page is not fair-housing advice and nothing here is a compliance certification. It is a map of which task each tool fits, and where a human review step is non-negotiable.</p>

<h2>What a working agent stack costs</h2>
<table>
<thead><tr><th>Tool</th><th>Free tier</th><th>Paid step</th><th>Checked</th></tr></thead>
<tbody>
<tr><td><strong>ChatGPT</strong></td><td>$0</td><td>Paid plans billed per user per month; official page did not expose exact localized prices at check time</td><td>2026-08-25</td></tr>
<tr><td><strong>Perplexity</strong></td><td>Standard/Free plan</td><td>Consumer Pro/Max prices not published; Enterprise Pro $40/seat monthly</td><td>2026-08-25</td></tr>
<tr><td><strong>Canva AI</strong></td><td>$0 (up to 200 Standard or 20 Premium AI uses/month)</td><td>Pro $180/year for one person; Business $250/year per person</td><td>2026-08-25</td></tr>
<tr><td><strong>Gamma</strong></td><td>$0 with 400 one-time signup credits that do not refill</td><td>Plus $9/seat/mo equivalent ($108/seat annually); Pro $18/seat/mo equivalent</td><td>2026-08-25</td></tr>
<tr><td><strong>Grammarly</strong></td><td>$0 with 100 generative-AI prompts/month</td><td>Pro displayed at $12 with 2,000 AI prompts/month</td><td>2026-08-25</td></tr>
<tr><td><strong>Zapier AI</strong></td><td>$0 with 100 tasks/month</td><td>Professional from $19.99/mo billed annually; Team $69/mo billed annually</td><td>2026-08-25</td></tr>
</tbody>
</table>
<p class="monetization-note">Published amounts with check dates, not quotes. Verify current pricing before subscribing — several of these vendors changed plan structure during 2026.</p>

<h2>Which tool for which task</h2>
<ul>
<li><strong>Listing descriptions and marketing copy.</strong> A general assistant (ChatGPT) drafts; you review for fair-housing language and factual accuracy. Never publish unreviewed output. Property descriptions are advertising, and advertising is regulated.</li>
<li><strong>Market and neighbourhood research.</strong> Perplexity, because citations stay visible and you can open the source. Never cite a metric in a client-facing document that you have not opened yourself.</li>
<li><strong>Listing visuals, social tiles, open-house flyers.</strong> Canva AI. The Free tier cap is specific — up to 200 Standard or 20 Premium AI uses per month — so a busy listing season can exhaust it, which makes Pro at $180/year a real consideration rather than an upsell.</li>
<li><strong>Client presentations and market updates.</strong> Gamma. Note the free tier's 400 credits are one-time and do not refill, so it is an evaluation tier rather than a working one; Plus at $108/seat annually is the first genuinely usable step.</li>
<li><strong>Email and client correspondence.</strong> Grammarly. Free includes 100 AI prompts/month; Pro's 2,000 prompts/month is the step that makes it a working tool rather than a sample.</li>
<li><strong>Follow-up and pipeline admin.</strong> Zapier AI, but budget carefully: AI steps draw from a shared task pool, with Standard model steps consuming 1 task per run, Advanced 3, and Premium 5. A workflow that looks cheap per run can consume a plan quickly at volume.</li>
</ul>

<h2>Client data: the line that matters</h2>
<p>Client names, addresses, phone numbers, offer terms, and anything in a transaction file are personally identifying information. General consumer AI tools are not the right place for it, regardless of how convenient the assistant is.</p>
<p>Practical rules that hold up: keep identifiable client data in your CRM or transaction system, not in a chat window. When you need an assistant to help with a client situation, describe the situation without identifiers. Check whether your brokerage has an approved AI policy before using any tool on client material — most now do, and following it is also your protection if something goes wrong.</p>

<h2>Fair housing and disclosure: what AI cannot do for you</h2>
<p>No tool on this page will tell you that a listing description violates fair-housing rules. Language that signals preference or exclusion — about families, religion, national origin, disability, or anything else protected — is a legal exposure that a language model will happily generate if prompted loosely, and will not reliably flag even when asked.</p>
<p>Treat AI output as a first draft that a human with training reviews. If you would not publish a sentence a junior colleague wrote without reading it, do not publish an AI draft unread either. The disclosure question is separate and increasingly contractual: check your listing agreements and state AI disclosure rules in your market rather than assuming silence is fine.</p>

<h2>Real-estate AI questions we get asked</h2>
<details><summary>Can I use AI to write listing descriptions?</summary><p>To draft, yes. To publish unchecked, no. Listing copy is regulated advertising, and a model will generate language with fair-housing exposure if your prompt is loose — and will not reliably catch it if you ask. Draft with AI, review with a trained human.</p></details>
<details><summary>Is it a problem to put client details into ChatGPT?</summary><p>Yes, for identifiable client information on a consumer plan. Describe the situation without names, addresses, or offer terms, or keep the work inside systems your brokerage has approved for client data.</p></details>
<details><summary>What is the cheapest stack that actually works?</summary><p>ChatGPT free for drafting, Grammarly Pro at $12 for correspondence volume, and Canva AI free while your AI-use count stays under the monthly cap. That covers most solo agents for very little. Add Gamma Plus or Zapier only when a specific task is demonstrably slowed by the free tier.</p></details>
<details><summary>Do my clients need to know I use AI?</summary><p>Increasingly yes, and it is usually governed by your listing agreements and market rules rather than left to judgment. Check your contract language and your brokerage's policy before assuming disclosure is optional.</p></details>
"""


DEPTH_BLOCKS = {
    'agencies': AGENCY_DEPTH,
    'teachers': TEACHERS_DEPTH,
    'assistants': ASSISTANTS_DEPTH,
    'search': SEARCH_DEPTH,
    'realestate': REALESTATE_DEPTH,
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
