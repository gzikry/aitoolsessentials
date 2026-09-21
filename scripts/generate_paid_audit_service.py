#!/usr/bin/env python3
"""Public paid AI Stack Audit service pages.

Replaces the folded-into-Premium framing with a real, purchasable high-ticket offer.

Why this exists
---------------
A $497 AI Stack Audit was built, delivered once, and then deliberately folded into the
$12/mo Premium membership (commit 5f0ca9c9: "Remove 97 audit references; move audit into
2 Premium only"). The consequence measured 2026-09-21: the offer appears on ZERO public
pages, so ~29 visits/month arriving on offer pages are offered a $12 subscription instead
of a $497 service.

Unit economics that force this: at verified affiliate rates (~$2.42 recurring per AI-tool
referral) reaching $1,000/mo needs ~246,000 visitors. The same revenue from a $497 audit
needs ~101. The high-ticket lane is the only one reachable from current traffic.

Why the first audit was not useful, and what changes here
---------------------------------------------------------
The reference delivery answered the client's four stated goals with "do not do this", and
handed back 8 open questions plus a blank inventory because the intake left the EHR/PMS,
phone/SMS vendor, budget, and spend fields empty. Composition: 13 "unknown/blank" mentions,
10 CUT/DEFER decisions, and a final recommendation of "add nothing".

The fix is procedural, not cosmetic:

1. REQUIRED discovery. The intake gates the paid tier on the fields whose absence caused
   the failure (systems in use, who owns each, what they cost, renewal dates, the one
   bottleneck ranked). A paid audit is not accepted until discovery is complete enough to
   answer with specifics.
2. ANSWER THE ASKED QUESTIONS FIRST. Every goal the client names gets a direct
   recommendation before any "do not add" guidance. Refusals are a conclusion, not the
   deliverable.
3. BOUNDED OPEN QUESTIONS. At most 3, and only ones that need the client's private data -
   never a substitute for discovery we should have done.
4. A NAMED FIRST ACTION. The client must be able to do something concrete on Monday.

Scoring is deliberately explicit so "not helpful" becomes a measurable, fixable signal.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"

# The paid tier. Priced to match the delivered reference audit.
AUDIT_PRICE_USD = 497
AUDIT_TURNAROUND = "5 business days"
AUDIT_INTAKE_SLA = "1 business day"

STACK_AUDIT_START = "<!-- AIT PAID AUDIT START -->"
STACK_AUDIT_END = "<!-- AIT PAID AUDIT END -->"


# ---------------------------------------------------------------------------
# Content model
# ---------------------------------------------------------------------------

def discovery_fields() -> list[tuple[str, str, str]]:
    """(name, label, why) — every field here is required before a paid build starts.

    These are exactly the blanks that gutted the first audit. The `why` text is shown to
    the client so the requirement reads as a quality gate, not as friction.
    """
    return [
        ("systems",
         "Every AI tool and system you pay for, one per line",
         "The first audit could not say what to cut because it never learned what you run."),
        ("owners",
         "Who owns each one (name or role)",
         "An unowned tool never gets renewed, cancelled, or fixed on purpose."),
        ("costs",
         "What each costs per month, and the renewal date",
         "Real savings need real numbers. Blanks become 'we could not quantify this'."),
        ("workflows",
         "The 1-3 workflows you most want to change",
         "Every one of your stated goals gets a direct recommendation."),
        ("bottleneck",
         "Of those, which single one costs you the most time or money",
         "One bottleneck gets the deep treatment. The rest get a ranked plan."),
        ("current_answer",
         "What you currently do about that bottleneck, and what it costs you",
         "Replacing a known cost is defensible. Adding a tool is not."),
        ("constraints",
         "Compliance, legal, or data limits we must respect",
         "Determines what is even eligible before we recommend anything."),
        ("stack_owner",
         "Who decides purchases, and who has to live with the choice",
         "Recommendations that ignore the approver do not get implemented."),
    ]


def deliverable_sections() -> list[tuple[str, str]]:
    """(title, body) — what the client actually receives."""
    return [
        ("Direct answer to every goal you named",
         "Each workflow you asked about gets its own recommendation: do it, do it differently, "
         "or do not do it — and why. Refusals appear only alongside an alternative that works."),
        ("Keep / cut / defer table with money attached",
         "Every system you listed, priced at what you told us, with the renewal date and the "
         "decision. Where you left a field blank we say so instead of inventing a figure."),
        ("The one bottleneck, worked in depth",
         "The single highest-cost problem you ranked gets the deep pass: options compared on "
         "fit, cost, effort, and risk, with the tradeoffs stated plainly."),
        ("A Monday action per finding",
         "No finding is delivered without something concrete to do about it, owned by a named role."),
        ("A 30-day sequence",
         "What to do in week 1, 2, 3, and 4, plus the cancel rule that stops drift."),
        ("Bounded open questions",
         "At most three, and only ones that need data only you hold. Not homework."),
    ]


def scope_lines() -> list[str]:
    return [
        "Strategy and written recommendation only. No implementation.",
        "No access to your accounts, systems, credentials, or API keys — ever.",
        "No legal, medical, or compliance advice; no BAA procurement.",
        "No fabricated savings. Blank inputs are reported as blank.",
        "Delivered as a PDF plus a written summary you can forward internally.",
    ]


def not_included() -> list[str]:
    return [
        "Setting anything up, configuring tools, or migrating data",
        "Logins, account access, or API keys",
        "Ongoing support, retainers, or implementation work",
        "Vendor negotiation, procurement, or contract review",
        "Legal, privacy, or compliance sign-off",
    ]


def three_lanes() -> list[tuple[str, str, str, str]]:
    """(lane, price, what you get, what it is based on) — the honest ladder.

    Premium's $12/mo written reply and this $497 audit both exist. Stating the difference
    explicitly is what keeps the ladder from reading as a dark pattern.
    """
    return [
        ("Free instant audit",
         "$0",
         "An in-browser keep/cut scorecard for one stack. Stays on your device, no login.",
         "Your own inputs, scored immediately."),
        ("Premium keep/cut pack",
         "$12/mo",
         "Monthly dated keep/cut research, a decision matrix CSV, a weekly checklist, and a "
         "strategy-only written reply to a completed inventory template.",
         "The inventory you submit, answered at template depth."),
        ("This written audit",
         f"${AUDIT_PRICE_USD} one-time",
         "Required discovery, a direct answer to every workflow you named, a keep/cut/defer table "
         "priced with your own numbers, a deep pass on the one bottleneck you ranked, a Monday "
         "action per finding, and a 30-day sequence.",
         "Completed discovery plus public vendor documentation, priced against your actual costs "
         "and renewal dates."),
    ]


def faq_items() -> list[tuple[str, str]]:
    return [
        ("How is this different from the free Stack Audit?",
         "The free instant audit at /stack-audit.html scores one stack in your browser and stays on "
         "your device. It is a scorecard. This is a written audit: we read your actual inventory, "
         "costs, renewals, and the bottleneck you ranked, and return specific keep/cut decisions "
         "with money attached."),
        ("Why is the discovery questionnaire required?",
         "Because the alternative failed. A previous audit was built on an intake that left the "
         "systems, vendors, costs, and budget blank, so it could not say what to cut or what "
         "anything cost, and the client found it unhelpful. We now require the fields that make "
         "the answer specific. If discovery is incomplete we say so before you pay."),
        ("What if I do not know my renewal dates or exact costs?",
         "Say so. We will show the field as unknown rather than estimate it, and the decision "
         "becomes 'find this out first' with a specific way to find it. We do not invent savings."),
        ("Do you need access to my tools?",
         "No, and we will never ask. We work from what you tell us plus public vendor "
         "documentation, pricing pages, and terms."),
        ("What if the recommendation is that I should buy nothing?",
         "Then that is the recommendation, and it will be specific: which subscription to keep, "
         "which to cancel, and what to measure before revisiting. Several of our best findings are "
         "cancellations. But you also get a direct answer to each goal you named — a refusal is a "
         "conclusion, not the whole deliverable."),
        ("How long does it take?",
         f"We confirm receipt within {AUDIT_INTAKE_SLA} and confirm the audit is buildable. "
         f"The written audit follows within {AUDIT_TURNAROUND} of that confirmation."),
    ]


# ---------------------------------------------------------------------------
# Page rendering
# ---------------------------------------------------------------------------

def _esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _head(title: str, desc: str, canonical: str) -> str:
    return (
        '<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<meta name="description" content="{_esc(desc)}">'
        f'<title>{_esc(title)}</title>'
        f'<link rel="canonical" href="{canonical}">'
        f'<meta property="og:title" content="{_esc(title)}">'
        f'<meta property="og:description" content="{_esc(desc)}">'
        f'<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<link rel="stylesheet" href="/css/styles.css">'
        '<link rel="stylesheet" href="/css/share.css"></head>'
    )


def _scripts() -> str:
    return '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def _nav() -> str:
    return ('<nav class="nav-links home-appear" data-appear="1">'
            '<a href="/tools/">Tools</a>'
            '<a href="/stack-audit.html">Free audit</a>'
            '<a href="/services/paid-audit.html">Paid audit</a>'
            '<a href="/premium/">Premium</a>'
            '<a href="/subscribe/">Subscribe</a></nav>')


def _header() -> str:
    return (f'<header class="site-header"><a class="brand" href="/">✦AIToolsEssentials</a>'
            f'{_nav()}</header>')


def _footer() -> str:
    return ('<footer class="site-footer">'
            '<p>AIToolsEssentials · AI tools research and strategy.</p>'
            '<p><a href="/services/paid-audit.html">Paid audit</a> · '
            '<a href="/services/audit-intake.html">Audit intake</a> · '
            '<a href="/stack-audit.html">Free audit</a> · '
            '<a href="/legal/terms.html">Terms</a> · '
            '<a href="/legal/privacy.html">Privacy</a></p></footer>')


def generate_service_page(root: Path, today: str) -> int:
    out = root / "services"
    out.mkdir(exist_ok=True)

    desc = (f"A written AI Stack Audit for ${AUDIT_PRICE_USD}: keep/cut/defer decisions with money "
            "attached, a direct answer to every workflow you named, and a 30-day plan. Strategy "
            "only — no implementation, no logins, no fabricated savings.")

    deliverables = "".join(
        f'<article class="content-hub-card"><span>Deliverable</span><h3>{_esc(t)}</h3>'
        f'<p>{_esc(b)}</p></article>'
        for t, b in deliverable_sections())

    scope = "".join(f"<li>{_esc(x)}</li>" for x in scope_lines())
    exclusions = "".join(f"<li>{_esc(x)}</li>" for x in not_included())

    discovery = "".join(
        f'<tr><td><strong>{_esc(label)}</strong></td><td>{_esc(why)}</td></tr>'
        for _n, label, why in discovery_fields())

    faq_html = "".join(
        f'<details><summary>{_esc(q)}</summary><p>{_esc(a)}</p></details>' for q, a in faq_items())

    # Three lanes, stated explicitly. Premium's $12/mo written reply and this $497 audit both
    # exist, so the difference must be legible on the page that sells the audit — otherwise the
    # ladder reads as a dark pattern. Depth and discovery are the honest axes of difference.
    lanes_html = "".join(
        f'<tr><td><strong>{_esc(n)}</strong></td><td>{_esc(price)}</td><td>{_esc(what)}</td>'
        f'<td>{_esc(basis)}</td></tr>' for n, price, what, basis in three_lanes())

    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items()],
    }
    service_schema = {
        "@context": "https://schema.org", "@type": "Service",
        "name": "AI Stack Audit",
        "serviceType": "AI tooling strategy audit",
        "provider": {"@type": "Organization", "name": "AIToolsEssentials", "url": DOMAIN},
        "areaServed": "Worldwide",
        "description": desc,
        "offers": {"@type": "Offer", "price": AUDIT_PRICE_USD, "priceCurrency": "USD",
                   "availability": "https://schema.org/InStock",
                   "url": f"{DOMAIN}/services/paid-audit.html"},
    }

    page = f'''<!doctype html><html lang="en">{_head(f"AI Stack Audit — a written keep/cut audit for ${AUDIT_PRICE_USD}", desc, DOMAIN + "/services/paid-audit.html")}<body>
{_header()}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center">
<p class="kicker light">Strategy audit · no implementation</p>
<h1>Know which AI subscriptions to keep, which to cut, and what the bottleneck actually costs you.</h1>
<p class="subhead">A written audit of the stack you already pay for. Keep/cut/defer decisions with money attached, a direct answer to every workflow you named, and a 30-day plan. ${AUDIT_PRICE_USD} one-time.</p>
<p><a class="button button-blue" href="/services/audit-intake.html">Start the audit intake</a>
<a class="button button-ghost-dark" href="/stack-audit.html" style="margin-left:8px">Try the free instant audit first</a></p>
<p class="muted-small">Strategy and written recommendations only. We never ask for account access, credentials, or API keys. No fabricated savings — if you leave a cost blank we report it as blank.</p>
</div></section>

<section class="scene scene-light content-hub"><div class="article-shell wide">
<h2>What you get</h2>
<div class="content-hub-grid">{deliverables}</div>

<div class="score-card"><span>Three lanes, stated plainly</span>
<h2>This is not the $12 membership, and the free audit is not this.</h2>
<div class="table-wrap"><table><thead><tr><th>Lane</th><th>Price</th><th>What you get</th><th>What it is based on</th></tr></thead><tbody>{lanes_html}</tbody></table></div>
<p class="muted-small">The $12/mo Premium pack includes a written reply against its inventory template. This audit costs more because it requires completed discovery first, answers every workflow you named directly, prices decisions against your own costs and renewal dates, and works the single bottleneck you ranked in depth. If Premium is enough for you, use it — the free audit and the $12 pack are both honest stopping points.</p></div>

<div class="score-card"><span>The rule this audit is built on</span>
<h2>Discovery is required, because skipping it is what makes an audit useless.</h2>
<p>A previous version of this audit was built from an intake that left the systems, vendors, costs, budget, and renewal dates blank. It could not tell the client what to cut or what anything cost, and the client found it unhelpful. So the questions below are required before a paid build starts, not optional.</p>
<div class="table-wrap"><table><thead><tr><th>Required before we build</th><th>Why it matters</th></tr></thead><tbody>{discovery}</tbody></table></div>
<p class="muted-small">If discovery is incomplete, we tell you before you pay rather than shipping a document full of gaps.</p></div>

<h2>Scope, stated plainly</h2>
<div class="content-hub-grid">
<article class="content-hub-card"><span>Included</span><h3>What you are buying</h3><ul>{scope}</ul></article>
<article class="content-hub-card"><span>Not included</span><h3>What this is not</h3><ul>{exclusions}</ul></article>
</div>

<div class="score-card"><span>Who this fits</span>
<h2>Good fit, and honest no-fit.</h2>
<p><strong>Good fit:</strong> you already pay for 3+ AI or software subscriptions, you can list them, and you suspect overlap, underuse, or a workflow that is still manual. Solo operators, consultants, agencies, clinics, and small teams.</p>
<p><strong>Not a fit:</strong> you want someone to set tools up for you, or you need legal, privacy, or compliance sign-off. That is implementation and advisory work outside this scope, and we will say so rather than take the fee.</p></div>

<h2>Questions</h2>
<div class="faq-list">{faq_html}</div>

<div class="score-card"><span>Next step</span>
<h2>Start with the intake.</h2>
<p>It takes about 15 minutes and needs the systems you pay for, their owners, their costs, and the one bottleneck you want solved first. That is what lets the audit answer with specifics instead of generalities.</p>
<p><a class="button button-blue" href="/services/audit-intake.html">Start the audit intake</a></p></div>
</div></section>
</main>{_footer()}{_scripts()}
<script type="application/ld+json">{json.dumps(service_schema, separators=(",", ":"))}</script>
<script type="application/ld+json">{json.dumps(faq_schema, separators=(",", ":"))}</script>
</body></html>'''

    (out / "paid-audit.html").write_text(page)
    return 1


def generate_intake_page(root: Path, today: str) -> int:
    """The paid intake. Fields map 1:1 onto discovery_fields(); all are required.

    Posts to the same ACTIVATED formsubmit endpoint the existing intake uses. The plain
    contact@ address returns 200 but is not necessarily activated for this form, and an
    unactivated endpoint silently drops submissions - which would lose paid leads.
    """
    out = root / "services"
    out.mkdir(exist_ok=True)

    fields = discovery_fields()
    inputs = []
    for name, label, why in fields:
        if name in ("workflows", "systems"):
            inputs.append(
                f'<label>{_esc(label)}<textarea name="{name}" rows="5" required></textarea></label>'
                f'<p class="muted-small">{_esc(why)}</p>')
        elif name == "bottleneck":
            opts = "".join(f"<option>{_esc(x)}</option>" for x in
                           ["(list your workflows first — then pick one)",
                            "The one I named above costs me the most time",
                            "The one I named above costs me the most money",
                            "Not sure yet — help me rank them"])
            inputs.append(f'<label>{_esc(label)}<select name="{name}" required>{opts}</select></label>'
                          f'<p class="muted-small">{_esc(why)}</p>')
        else:
            inputs.append(f'<label>{_esc(label)}<input type="text" name="{name}" required></label>'
                          f'<p class="muted-small">{_esc(why)}</p>')

    contact = [
        ("name", "Your name"),
        ("email", "Email"),
        ("business", "Business or practice name"),
        ("role", "Your role"),
    ]
    contact_html = "".join(
        f'<label>{_esc(l)}<input type="{"email" if n == "email" else "text"}" name="{n}" required></label>'
        for n, l in contact)

    desc = (f"Intake for the ${AUDIT_PRICE_USD} written AI Stack Audit. Required discovery: the "
            "systems you pay for, their owners, costs, renewal dates, the workflow goals you want "
            "addressed, and the single bottleneck to work in depth.")

    page = f'''<!doctype html><html lang="en">{_head(f"AI Stack Audit intake — ${AUDIT_PRICE_USD} written audit", desc, DOMAIN + "/services/audit-intake.html")}<body>
{_header()}<main>
<section class="scene scene-light"><div class="article-shell">
<p class="kicker">Step 1 of 2</p>
<h1>AI Stack Audit intake</h1>
<p class="subhead">This is what lets the audit answer with specifics. Every field below is required — the previous version of this audit skipped them and the client found the result unhelpful. If you do not know a number, write "unknown" rather than guessing; we will report it as unknown instead of inventing a figure.</p>

<form class="stack-form" action="https://formsubmit.co/eb3d1bf5a35125c06383cafa247af931" method="POST">
<input type="hidden" name="_subject" value="PAID AI Stack Audit intake (${AUDIT_PRICE_USD})">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="{DOMAIN}/services/intake-received.html"><input type="hidden" name="_captcha" value="false"><input type="text" name="_honey" style="display:none">

<h2>Who you are</h2>
{contact_html}

<h2>The systems you pay for</h2>
{"".join(inputs)}

<h2>Scope acknowledgement</h2>
<label class="form-check"><input type="checkbox" name="scope_ack" required> I understand this is a written strategy and recommendation service. It does not include implementation, setup, account access, credentials, API keys, vendor negotiation, or ongoing support.</label>
<label class="form-check"><input type="checkbox" name="discovery_ack" required> I understand the audit is built from the information above, and that blank fields are reported as unknown rather than estimated.</label>

<p><button class="button button-blue" type="submit">Submit intake</button></p>
<p class="muted-small">We reply within {AUDIT_INTAKE_SLA} to confirm the audit is buildable and to arrange payment. Nothing is charged from this form.</p>
</form>

<div class="score-card"><span>What happens next</span><h2>Two steps, no surprises.</h2>
<p><strong>1. Review.</strong> We read the intake and confirm the audit is buildable within {AUDIT_INTAKE_SLA}. If it is not — if discovery is too incomplete, or the request is implementation work — we say so and do not take payment.</p>
<p><strong>2. Delivery.</strong> Once payment is arranged, the written audit follows within {AUDIT_TURNAROUND}. It includes a direct answer to every goal you named, a keep/cut/defer table with your own numbers, a deep pass on the bottleneck you ranked, a Monday action per finding, and a 30-day sequence.</p>
</div>
</div></section>
</main>{_footer()}{_scripts()}</body></html>'''

    (out / "audit-intake.html").write_text(page)
    return 1


def generate_received_page(root: Path, today: str) -> int:
    out = root / "services"
    out.mkdir(exist_ok=True)
    desc = f"Intake received for the ${AUDIT_PRICE_USD} AI Stack Audit. Next steps and turnaround."
    page = f'''<!doctype html><html lang="en">{_head("Intake received — AI Stack Audit", desc, DOMAIN + "/services/intake-received.html")}<body>
{_header()}<main>
<section class="scene scene-light"><div class="article-shell">
<p class="kicker">Step 2 of 2</p>
<h1>Intake received.</h1>
<p class="subhead">We have your inventory. Here is exactly what happens next.</p>
<div class="score-card"><span>Within {AUDIT_INTAKE_SLA}</span><h2>We confirm the audit is buildable.</h2>
<p>We read what you sent and reply to confirm either that we can build a specific audit from it, or that discovery needs one more thing first. <strong>No payment is taken until that confirmation.</strong> If your request is implementation work or needs legal or compliance sign-off, we will tell you it is out of scope rather than take the fee.</p></div>
<div class="score-card"><span>Within {AUDIT_TURNAROUND} of confirmation</span><h2>You receive the written audit.</h2>
<p>Every workflow you named gets a direct recommendation. Every system you listed gets a keep/cut/defer decision with the cost you gave us. The bottleneck you ranked gets the deep pass. Blank inputs stay blank — we do not estimate your spend.</p></div>
<p><a class="button button-ghost-dark" href="/services/paid-audit.html">Back to the audit overview</a></p>
<p class="muted-small">Nothing in this service includes account access, credentials, API keys, implementation, or ongoing support. Research and strategy only.</p>
</div></section>
</main>{_footer()}{_scripts()}</body></html>'''
    (out / "intake-received.html").write_text(page)
    return 1


def generate_sample_page(root: Path, today: str) -> int:
    """Public redacted sample. Never includes the real client's private data."""
    out = root / "services"
    out.mkdir(exist_ok=True)
    desc = (f"A redacted sample of the ${AUDIT_PRICE_USD} AI Stack Audit: the structure, the "
            "keep/cut table with money attached, and the level of specificity to expect.")
    page = f'''<!doctype html><html lang="en">{_head("AI Stack Audit — redacted sample", desc, DOMAIN + "/services/sample-audit.html")}<body>
{_header()}<main>
<section class="scene scene-light"><div class="article-shell">
<p class="kicker">Sample</p>
<h1>What a finished audit looks like.</h1>
<p class="subhead">Redacted structure from a real delivery. Client identity, systems, and figures are replaced with placeholders — we do not publish a client's stack or their costs.</p>

<div class="score-card"><span>Section 1</span><h2>Direct answers to the goals you named</h2>
<p>Each workflow you asked about gets its own recommendation. Example shape:</p>
<div class="table-wrap"><table><thead><tr><th>Your stated goal</th><th>Recommendation</th><th>Why</th></tr></thead><tbody>
<tr><td>Handle more inbound calls</td><td><strong>Do it differently, not with an AI receptionist</strong></td><td>Your booking system already collects requests and requires human confirmation. Adding a second booking path creates conflicts. Automate the follow-up message instead.</td></tr>
<tr><td>Reduce time on patient replies</td><td><strong>Do it — narrow and fenced</strong></td><td>Template drafting for non-sensitive messages is worth it. Anything identifying a customer stays out of a general AI workspace.</td></tr>
<tr><td>Get better at scheduling</td><td><strong>Do not do it yet</strong></td><td>Scheduling is owned by an existing system with a live calendar. Until we know which one and who confirms, a new tool adds a second source of truth.</td></tr>
</tbody></table></div>
<p class="muted-small">Note the shape: two of three are "yes, like this" rather than refusals. That was the main failure of an earlier version of this audit.</p></div>

<div class="score-card"><span>Section 2</span><h2>Keep / cut / defer, with your numbers</h2>
<div class="table-wrap"><table><thead><tr><th>System</th><th>Monthly</th><th>Owner</th><th>Renewal</th><th>Decision</th></tr></thead><tbody>
<tr><td>General assistant (seat 1)</td><td>$20</td><td>Owner</td><td>Monthly</td><td><strong>KEEP</strong> — narrow non-sensitive drafting lane</td></tr>
<tr><td>General assistant (seat 2, unowned)</td><td>$20</td><td>unknown</td><td>unknown</td><td><strong>CUT</strong> — no owner, no defined weekly job</td></tr>
<tr><td>Meeting recorder</td><td>$18</td><td>unknown</td><td>unknown</td><td><strong>CUT</strong> — not used on sensitive calls, unused for the stated workflow</td></tr>
<tr><td>Specialist documentation tool</td><td>unknown</td><td>—</td><td>—</td><td><strong>DEFER</strong> — only if the ranked bottleneck is documentation</td></tr>
</tbody></table></div>
<p class="muted-small">Where a field was left blank it stays "unknown". We do not fill in a plausible figure to make the table look complete.</p></div>

<div class="score-card"><span>Section 3</span><h2>The ranked bottleneck, worked in depth</h2>
<p>Options compared on fit, cost, effort, and risk, ending in a single recommendation and the tradeoff you are accepting. Not a list of possibilities.</p></div>

<div class="score-card"><span>Sections 4-5</span><h2>Monday actions and a 30-day sequence</h2>
<p>Every finding carries a specific next action with a named owner. The sequence covers weeks 1-4 and ends with a cancel rule so the stack does not drift back.</p></div>

<p><a class="button button-blue" href="/services/audit-intake.html">Start the audit intake</a>
<a class="button button-ghost-dark" href="/services/paid-audit.html" style="margin-left:8px">Back to overview</a></p>
</div></section>
</main>{_footer()}{_scripts()}</body></html>'''
    (out / "sample-audit.html").write_text(page)
    return 1


def generate_structure_page(root: Path, today: str) -> int:
    """The delivery standard, published. Makes "not helpful" a measurable miss."""
    out = root / "services"
    out.mkdir(exist_ok=True)
    desc = ("The delivery standard for the AI Stack Audit: what every section must contain, and the "
            "checklist that must pass before an audit is sent.")
    checks = [
        "Every workflow the client named has a direct recommendation — do it, do it differently, or do not do it.",
        "No finding is delivered without a concrete action and an accountable owner.",
        "Every system in the inventory has a keep/cut/defer decision.",
        "Every cost figure comes from the client's own intake; blanks are reported as blank.",
        "No savings, ROI, hours-saved, or payback figure is stated unless the client supplied the input.",
        "Open questions are capped at three and require data only the client holds.",
        "The ranked bottleneck is answered with one recommendation, not a menu of options.",
        "Scope, exclusions, and the no-access boundary are restated.",
        "Every factual vendor claim carries a dated public source.",
        "The document is re-read against this list before it is sent.",
    ]
    items = "".join(f"<li>{_esc(c)}</li>" for c in checks)
    page = f'''<!doctype html><html lang="en">{_head("AI Stack Audit delivery standard", desc, DOMAIN + "/services/audit-standard.html")}<body>
{_header()}<main>
<section class="scene scene-light"><div class="article-shell">
<p class="kicker">Standard</p>
<h1>The audit delivery standard.</h1>
<p class="subhead">Published so it can be checked against the real thing. An earlier audit failed three of these — it answered the client's goals mostly with refusals, handed back eight open questions, and could not attach money to anything because discovery was skipped.</p>
<div class="score-card"><span>Before any audit is sent</span><h2>Ten checks, all required.</h2><ul>{items}</ul></div>
<p class="muted-small">If you have received an audit that misses any of these, say so and we will redo it.</p>
<p><a class="button button-blue" href="/services/paid-audit.html">See the audit</a></p>
</div></section>
</main>{_footer()}{_scripts()}</body></html>'''
    (out / "audit-standard.html").write_text(page)
    return 1


def generate_all(root: Path, today: str) -> dict[str, int]:
    stats = {
        "paid_audit": generate_service_page(root, today),
        "intake": generate_intake_page(root, today),
        "received": generate_received_page(root, today),
        "sample": generate_sample_page(root, today),
        "standard": generate_structure_page(root, today),
    }
    return stats


if __name__ == "__main__":
    import sys
    root_path = Path(__file__).resolve().parents[1]
    from datetime import date
    stats = generate_all(root_path, date.today().isoformat())
    print("generated:", json.dumps(stats))
