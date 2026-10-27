# Ready-to-Submit Affiliate Applications

Last verified 2026-09-13 PT; inventory counts refreshed 2026-10-14 against the site's own
`/site-status.json`. Site facts below are real and checkable — do not inflate.
Site: 741 public pages, 77 reviewed tools, 16 categories, 211 comparisons, 181 guides.
Traffic, stated honestly: ~69 visitors / 223 pageviews per 30 days (early stage, growing).

**Shared answers** (use in every form):

- Business name: AIToolsEssentials
- Website: https://aitoolsessentials.com
- Platform type: Website — independent AI tool review directory
- Country: United States
- Contact: contact@aitoolsessentials.com

---

## PartnerStack network account — ALREADY CREATED, email verification outstanding

Signup was completed with **Sign in with Google** as `aitoolsessentials@gmail.com`
(profile `AiToolsEssentials`) on 2026-09-12 15:32 PT. PartnerStack sent
"Verify your email address" at 15:34 PT (SendGrid DKIM/SPF pass, from
`hello@partnerstackmail.com`).

**The verification link has not been opened.** It is a single-use token — do **not**
pre-fetch, automate, or share it; open it from the mailbox and stay signed in.

**Corrected 2026-09-12 (evidence): the unverified email did *not* block applications.**
The earlier claim that "until the email is verified, individual program applications may
not go through" is false. Both Descript and Gamma accepted submissions through the
PartnerStack application flow while the network email was still unverified, and
PartnerStack sent a separate "Your Application to join <program>" acknowledgement for
each — Descript at 16:36 PT, Gamma at 15:51 PT. Verification is still required to unlock
the dashboard, track status and collect payouts, but an application itself is not gated
on it. Do not treat the outstanding verification as a reason to delay applying.

**Also verified 2026-09-12:** the Descript acknowledgement landed in `[Gmail]/Trash`, not
Sent or All Mail, while the Gamma one stayed in INBOX. Scan `[Gmail]/Trash` when checking
whether an application registered — the same folder trap that hides outbound sends.

---

## How to tell whether a PartnerStack listing is actually open

Do not trust HTTP 200. A worked listing renders **"Apply to program"** with real details
(attribution type, SubIDs). A dead one renders **"Request program"** plus unfilled
placeholders — `{{name}}`, `{{company.description}}`, literal `undefined`.

Verified 2026-09-12:
- **Gamma** → *Apply to program*, populated → **OPEN**
- **ClickUp** (control) → *Apply to program*, populated → worked listing
- **Copy.ai** → marketplace listing returns a null company block (no offers, no program
  state) → **NOT OPEN**. Note: the *"Request program" + unfilled `{{name}}`* signature
  previously cited here proves nothing — the identical 15,260-byte template is served by
  `browseai/copyai/descript/gamma.partnerstack.com`, including programs we successfully
  applied to. Do not cite that signature again.

`copyai.partnerstack.com` and `browseai.partnerstack.com` render the same unpopulated
template, so the vendor-hosted subdomains are not a working fallback either.

---

## STATUS 2026-09-14

**Approved live: Gamma (PartnerStack unique link 2026-09-13) and Descript (PartnerStack unique link 2026-10-16). No program application is outstanding.**

**CHANGED 2026-09-14 — PartnerStack network application was DECLINED, not still pending.**
`networkquality@partnerstack.com` ("The status of your PartnerStack Network Application",
2026-09-14 09:17 PT) says PartnerStack has **limited our access to new programs via the
Marketplace**: "We are working on expanding our Network. Your profile is not a great fit, but
may be in the future."

What it does and does not do:
- **Does not affect existing partnerships** (their words): Gamma's approved tracking link stays
  live, and the pending Descript application is not cancelled. ElevenLabs, Make, Nous and
  Sonaopus are direct programs and were never PartnerStack-dependent.
- **Does block every NEW marketplace join**, including **Browse AI** — its listing is genuinely
  open (`application=true, approved=true`, 20% recurring lifetime), but the *join* is gated by
  the network limit. The vendor-side fact and the network-side gate are different things: the
  listing is open, the join is not available.
- **Closes the last fallback for Copy.ai and the Grammarly lead.** Copy.ai's earlier next step
  ("search the in-app Marketplace inside the dashboard") is gone; treat Copy.ai as closed. The
  private Grammarly Business group (`co_s4UUPYp9Nuvh1L`, `approved=false`) is likewise
  unreachable until the profile is re-approved.
- **Reapplying is dashboard-only and George-only** at `app.partnerstack.com`. PartnerStack says
  re-evaluation is possible "based on new or corrected information."

This is the same class of outcome as the Impact rejection: a network-level gate on traffic and
profile fit, not a vendor-level refusal. The site's answer is unchanged — keep building direct
programs (ElevenLabs, Make, Nous, Sonaopus already live) and revisit networks once traffic
supports acceptance.

**George-only, outstanding:** Gumroad sent "Confirmation instructions" for the account
carrying the Sonaopus affiliate program on 2026-09-13 16:50 UTC, about an hour before the
program was approved (17:58 UTC). Whether that confirmation was completed is not
verifiable from the website side, so treat the account's verification state as George's
to check. The affiliate link itself already works — the ref and per-product checkout URLs
return 200 with tracking — so this blocks only dashboard access, affiliate stats, and
payouts, not the live links. Same class as the PartnerStack network verification: it
gates visibility and payment, not placement. Do not rebuild the links.

| # | Program | Route | Rate | Status |
|---|---------|-------|------|--------|
| 0 | PartnerStack network | app.partnerstack.com | — | **DECLINED 2026-09-14** — marketplace access limited ("profile is not a great fit"); existing partnerships unaffected; reapply is dashboard-only, George-only |
| 1 | Gamma | PartnerStack listing | 25% first year — **rate queried 2026-10-14, vendor email claims 30%** | **approved 2026-09-13; link live 2026-09-13, re-verified live 2026-10-14** — https://try.gamma.app/ty4k3o3rpeyd (unaffected by the network limit) |
| 2 | Descript | dash.partnerstack.com/application?company=descriptinc | $25 + 15% rec. — program-page terms; the approval email supplied the link only, no rate | **APPROVED 2026-10-16; link live 2026-10-16** — https://get.descript.com/wvafmtthtkp5, wired on /tools/descript/ and named on /legal/affiliate-disclosure.html. The pre-limit application was honoured; the network limit still bars NEW marketplace joins |
| 3 | Copy.ai | PartnerStack listing not open | 45% rec. 12mo | **closed 2026-09-14** — listing dead and the in-app Marketplace fallback is gone with the network limit |
| 4 | Browse AI | market.partnerstack.com/artificial-intelligence/browseai | 20% rec. life | listing open (verified 2026-09-14) but **join gated by the 2026-09-14 network limit** |
| 5 | ElevenLabs | direct | 22% rec. 12mo | approved 2026-08-23 |
| 6 | Make | direct | 35% rec. 12mo | approved 2026-08-23 |
| 7 | Nous / Hermes | direct | $15 off referral | approved 2026-09-02 |
| 8 | Sonaopus | Gumroad | 40% one-time | approved 2026-09-13 |
| 9 | AIDetector.cx | direct (partnerships@aidetector.cx) | 30% recurring | **VERIFICATION SENT 2026-10-06 — await reply before publishing.** Terms confirmed by the vendor in writing on 2026-10-06 (mail `partnerships@`, 13:46 −05:00): 30% recurring on eligible subscription payments, **30-day attribution window**, **30-day commission holding period**, **$50 minimum payout in USD**, own tracked link + affiliate dashboard, complimentary testing credits. Account registered and verified under aitoolsessentials@gmail.com 2026-10-03 (Sent msgs 190, 191). **Reply sent 2026-10-06 (Sent msg 211)** — it states the 30% recurring / 30-day cookie / 30-day hold / $50 USD payout back to them for confirmation, declines paid placement per `/legal/trust.html`, and raises nine items from our own read of the live site. Open blockers, highest first: (1) **training-use contradiction** — `/detector` says "We do not use submitted content to train or fine-tune our models" while `/privacy` §2 says "Analysis text may be used in anonymized, aggregated form to train detection models unless you opt out in your account settings", with the §5 opt-out scoped to "Enterprise and Professional plan users" only; (2) **unverified named testimonials** on `/detector` attributed to named staff at Forbes, Stripe, HubSpot and Nature Portfolio with no illustrative/early-access label; (3) **"SOC-2 Type II Certified" in the footer vs "SOC 2-aligned controls" in the body**; (4) **98.7% / 1.2s / 12.4M+ / 142+ country marketing figures**, absent from their own benchmark page, which reports precision 0.97 / recall 0.94 / F1 0.955 / FPR 1.2% on a 400-doc internal corpus; (5) **Paystack in Privacy §1 vs Stripe in the Cookie Policy** for self-serve checkout; (6) retention — analysis results 12 months default, no stated path for the submitted text itself; (7) confirm AI Checker for Bloggers at 30 credits/report means 10 reports/month on Pro's 300; (8) whether the 30% covers annual plans and recurs on renewals "for the lifetime of the customer" as `/affiliate-hub` states; (9) **name in active commercial use on other domains** — aidetector.com (registered **2017-09-21**), aidetector.net, aidetector.ai (2016) — not squatting (aidetector.cx registered 2026-06-03), but any listing must carry the exact domain. **TRACKED LINK RECEIVED 2026-10-08 (mail `partnerships@aidetector.cx` 11:09 −05:00 / 16:09 UTC); access confirmed in writing; still NOT publishable — the two blocker questions were explicitly deferred by the vendor.** The mail activates the account, adds **300 complimentary credits**, and supplies the tracked link **`https://aidetector.cx/ai-checker-for-bloggers?aff=e3b5c457-7d5e-41a5-ab62-8977dfaf7f84`** (general signup `https://aidetector.cx/signup?aff=e3b5c457-…`); resolves item (8) affirmatively — **"annual subscriptions remain part of the affiliate commission program"** — and restates the plan matrix (Pro $12/mo 300 cr or $120/yr; Pro Plus $29/mo 1,000 cr or $290/yr; Business $79/mo 3,000 cr or $790/yr), matching the prices I read from the SPA bundle on 2026-10-06. **Verified live today (2026-10-08): the link follows the `aidetector.cx` → `www.aidetector.cx` 308 and returns 200 on `/ai-checker-for-bloggers`, title "AI Checker for Bloggers | AIDetector.cx".** On the blockers the vendor wrote that the product-policy and claim-verification points "should be treated separately from the affiliate setup" and that we should publish only what we can independently support — i.e. **the two publication blockers are deferred, not answered.** Re-checked the live site today and **both are unchanged:** (1) `/detector` still reads "We do not use submitted content to train or fine-tune our models" while `/privacy` §2 still reads "Analysis text may be used in anonymized, aggregated form to train detection models unless you opt out in your account settings" with §5 still scoping the opt-out to "Enterprise and Professional plan users"; (2) the `/detector` testimonials still name Forbes / Stripe / HubSpot / Nature Portfolio staff with no illustrative or early-access label. **Reply sent 2026-10-08 (Sent msg 219)** — thanks, logs the now-confirmed terms and link, declines to publish while those two are open, offers to publish crediting the genuine positives (their own conservative benchmark figures, stated output ownership, named legal set and California governing law), and re-states the remaining six non-blocking items. *2026-10-08 RESOLVED — TOOL PUBLISHED.* The vendor's second reply (10:55 −07:00) shipped the fixes: `/privacy` §3 now states *submitted analysis text is not used to train or fine-tune detection models **on any plan*** (old anonymized-training sentence and the Enterprise/Professional-scoped §5 opt-out both gone), and the four named Forbes/Stripe/HubSpot/Nature Portfolio testimonials were **removed** from `/detector`; the SOC-2 footer claim and the 98.7/12.4M/142+ figures were also removed. Re-checked live the same day before publishing. **Listing live: https://aitoolsessentials.com/tools/aidetector-cx/ (rating 4.0, category Productivity).** The 30% recurring tracked link `…/ai-checker-for-bloggers?aff=e3b5c457-…` is wired to the review CTA (`rel="sponsored noopener nofollow"`, disclosure fineprint) and AIDetector.cx is named on `/legal/affiliate-disclosure.html`. Open (non-blocking): Paystack named for billing on `/privacy` vs Stripe named on `/cookies`. **Registry surfaces confirmed complete 2026-10-10 — the earlier note that the link had nowhere to be wired was stale: `affiliate_programs.json` carries `aidetector-cx` (status `approved`, network Direct, tracked URL `…?aff=e3b5c457-…`), and the review CTA and `/legal/affiliate-disclosure.html` both carry the program, so no wiring work remains.** Mail auth note: the 2026-10-06 mail is Gmail-hosted (`mail.gmail.com`, DKIM pass `gappssmtp.com`, header `Date: 13:46:34 -0500`) with `spf=none` and `dmarc=fail` — treat the address as the mailbox but do not treat sender identity as cryptographically proven for any future payment instruction. |

### Gamma — APPROVED 2026-09-13 / LINK LIVE 2026-09-13
Program: https://market.partnerstack.com/artificial-intelligence/gammaapp
Unique link: https://try.gamma.app/ty4k3o3rpeyd
Commission: 25% for the first year on referred customers (partners@gamma.app / PartnerStack, 2026-09-13 PT).
Wired on `/tools/gamma/` Visit CTA with `rel="sponsored noopener nofollow"` and the existing review disclosure fineprint. Official pricing/docs/privacy/terms stay on gamma.app. Editorial score and cons unchanged.
**Caution:** `gammaapp.ai` is a DIFFERENT company from Gamma — do not cite its 50% claim.

**Partner engagement + rate discrepancy 2026-10-14.** `partners@gamma.app` ("How top Gamma partners get clicks",
2026-10-14 11:10 UTC / 04:10 PT — a PartnerStack campaign sent via SendGrid, signed Justine, Affiliate Consultant)
reports a month of partner inactivity, restates the same tracking link, and claims **"30% recurring commission for
1 year"**. That contradicts the same sender's own approval email of 2026-09-13 PT ("You'll earn 25% commission for the
first year") and the live listing, which carries exactly **one** offer — `percent` value **2500** = 25%, named
"25% for each signup". The listing JSON was re-read on 2026-10-14 to confirm no 30% offer exists anywhere in it.
**25%/first-year stays the recorded governing term** (it is the term the tracking link was granted under) and the
30% figure is carried as unresolved until Gamma confirms in writing. This is a term question, not a placement
question — no paid placement was sought or offered.

**Reply sent 2026-10-14** — the first outbound message to this partner; Sent Mail carried no prior reply of any
kind. It gives the site link, honest audience info (last verified Search Console reading, dated, rather than a
guess at today's), and asks Gamma to confirm which rate is authoritative for the tracked link. No CTA, score,
public page or admin pack changed for it: the tracking URL on `/tools/gamma/` was re-verified live the same day
and is unchanged (HTTP 200, `rel="sponsored noopener nofollow"`).

**MX caveat for this domain.** `gamma.app` is Google Workspace and accepts mail for *any* local part — a random
control address also returned `250` — so the pre-send `RCPT TO` probe proves only that the message will not bounce.
Do not cite it as evidence that `partners@` is read by a human.

**Second campaign, 2026-10-15 16:51 UTC — no answer, no action, record corrected.** A second PartnerStack
campaign from the same `partners@gamma.app` ("Your Gamma links are getting attention!", signed Justine)
restates the same tracking link, repeats the **30% for the first year** claim, and does not address the
2026-10-14 rate question. It also claims the link "has started receiving clicks" while the 2026-10-14 campaign
said the partner had been inactive for a month — both are campaign copy, and click volume is **not verifiable
from our side**: the Plausible API is locked (no active subscription; reported in `marketing/traffic/`) and the
PartnerStack dashboard is George-only. **No reply sent** — the question was asked 28 minutes after the previous
campaign and this one adds nothing; 25%/first-year stays the governing term.
**Record correction (same pass):** the 2026-10-14 reply is a genuine send but Gmail filed it in
`[Gmail]/Trash` (msg 71, subject `Re: How top Gamma partners get clicks`, 2026-10-14 11:38 UTC), **not** in
`[Gmail]/Sent Mail` — verified by exporting both folders. A Sent-Mail-only sweep therefore shows no prior reply
to this partner; cite the send by date + subject and check Trash before ever re-sending. Live re-check the same
day: `/tools/gamma/` carries `https://try.gamma.app/ty4k3o3rpeyd` with `rel="sponsored noopener nofollow"` on
both the public URL and the origin.

Answers used (reusable for the reference/audience fields if the portal asks again):

> Our Gamma review (aitoolsessentials.com/tools/gamma/) documents dated pricing, an
> editorial score with published reasoning, and explicit trade-offs — including that
> important decks still need design review. Gamma also appears in our
> best-AI-presentation-tools and best-AI-productivity-tools guides.
>
> The strongest converting content is comparative: readers searching for a faster deck
> workflow land on our presentation guides already comparing paid options. Links are
> contextual, FTC-disclosed, and never influence ranking.

**Audience:** Consultants, marketers, founders, and educators who build decks regularly
and are choosing between paid presentation tools.

### Descript — APPROVED 2026-10-16 (link live)
**Apply:** https://dash.partnerstack.com/application?company=descriptinc&group=affiliates
(linked from descript.com/affiliate as "Apply Now")
**Commission:** $25 one-time per new subscriber + 15% recurring for 12 months; 30-day
cookie. Approval typically ~1 week, up to 30 days. PartnerStack company slug `descriptinc`.

> Our Descript review (aitoolsessentials.com/tools/descript/) has dated pricing, an
> editorial score with published reasoning, and the workflow limitation stated plainly —
> advanced video work may still need a dedicated editor. Descript appears in our
> best-AI-video-tools and best-AI-voice-tools guides, and in a published switch guide
> from ElevenLabs to Descript for readers changing their audio/video stack.
>
> The switch-guide format is our best converter for this category: it targets people
> already paying for a tool and actively moving.

**Audience:** Podcasters, creators, video editors, and small content teams choosing
transcript-based editing tools.

**What was stated on the application (traffic):** ~4,600 impressions and 66 visitors in the
trailing 30 days, average position improving from 62 to 44 across three weeks. The case made
was **intent, not volume**: a published Descript-vs-Riverside comparison and an
ElevenLabs-to-Descript switch guide both reach readers who already pay for an audio tool and
are actively moving. Descript-relevant pages currently sit at positions 41-83, so near-term
signup volume is expected to be under 1/month — deliberately not overstated, because
PartnerStack verifies the live site and a misrepresentation rejection is not appealable.

**APPROVED 2026-10-16.** `affiliates@descript.com` ("Welcome to the Descript partner program",
2026-10-16 13:18 UTC, sent on behalf of Descript via PartnerStack/SendGrid) supplied the unique
referral link `https://get.descript.com/wvafmtthtkp5` — and nothing else. No rate was restated, so
the recorded $25 + 15%/12-month figures remain program-page terms unconfirmed by the approval
itself; ask for written confirmation of the current rate when the PartnerStack dashboard is
reachable. Link verified the same day: a GET follows one redirect to
`https://www.descript.com/?utm_medium=influencer&utm_source=affiliate&pscd=get.descript.com` with
`ps_partner_key=MGVjZWY0Nzk5NDI1` present and HTTP 200, so it is live and attributable.
Wired the same day: the /tools/descript/ Visit CTA carries the tracking URL with
`rel="sponsored noopener nofollow"` plus the disclosure fineprint, Descript is named in the
current-programs list on `/legal/affiliate-disclosure.html`, and the revenue target is set to
approved. The 2026-09-14 network limit did not cancel this application — it was submitted before
the limit and approved 34 days later — but it still bars NEW marketplace joins, so Browse AI
stays gated. Editorial score, pros and cons unchanged.

**Confirmation reply sent 2026-10-16 13:33 UTC** (`himalaya`, account `aitools`, one record in
`[Gmail]/Sent Mail`, none in Trash — no duplicate): thanks, links to the live review CTA and the
disclosure page, asks for the commission rate in writing since the approval restated none, states
the audience honestly (the same "early growth / applied on intent" case as the application), and
asks whether dashboard access is issued separately. Signed AIToolsEssentials.

**2026-10-18: PartnerStack portal orientation received, not answered.** `affiliates@descript.com`,
"Descript | Using our partner portal, PartnerStack", 2026-10-18 14:30 UTC — an automated
SendGrid campaign explaining the PartnerStack dashboard (Links / Referrals / Resources / Payouts),
not a vendor reply and not a question. It restates no commission rate, so the written-rate ask in
the 2026-10-16 confirmation is **still open**; it also does not answer whether dashboard access is
issued separately, because the campaign assumes it already is. Recorded only, no reply: replying to
campaign copy adds nothing to an outbound question already sitting in the thread.

Two chores it names that are **dashboard-only and therefore George's lane** (never attempted here —
login-gated, no credentials handled):

1. Sign in at `dash.partnerstack.com` and **accept the Descript program's Terms of Service**; the
   campaign states full dashboard access is gated on that acceptance (it must be accepted per
   program, and separately for any other program joined).
2. In **Payouts**, choose and set up a payment provider so accrued rewards can be cashed out
   monthly. Until that exists, approved referrals accrue but cannot be paid.

Dashboard faults go to `support@partnerstack.com`; program-specific questions go through the
portal's program-management contact, which the campaign does not publish as an email address.
Affiliate surfaces re-verified live 2026-10-18 while recording this: `/tools/descript/` returns 200
with `get.descript.com/wvafmtthtkp5` on the CTA under `rel="sponsored noopener nofollow"`, and
`/legal/affiliate-disclosure.html` returns 200 naming Descript.

> **Correction, 2026-10-27: the review page does not carry the tracking URL any more, and that is not
> a regression.** Approved programs are now wired through the `/go/<slug>/` noindex hop
> (`scripts/wire_affiliate_links.py` — "Point approved-partner CTAs at `/go/<slug>/`"), which holds the
> partner URL. `/tools/descript/` carries exactly one `href="/go/descript/"` and `/go/descript/`
> carries the tracking URL twice (meta refresh plus a fallback anchor under
> `rel="sponsored nofollow noopener"`). An audit that greps the review page for `get.descript.com`
> will report it unwired and be wrong — follow the hop. The 2026-10-18 sentence above describes the
> pre-hop wiring and should not be read as the current mechanism.

**2026-10-27: "Your Descript link is getting some activity!" — automated campaign, recorded, not answered.**
`affiliates@descript.com`, 2026-10-27 22:03 UTC (PartnerStack via SendGrid), claims clicks have already
been earned on the referral link, restates `https://get.descript.com/wvafmtthtkp5` unchanged, and invites
a short program-feedback survey. It is campaign copy, not a vendor reply and not a question, and it
restates **no commission rate** — so the written-rate ask from the 2026-10-16 confirmation is **still
open**. No reply sent: answering campaign copy adds nothing to a question already sitting in the thread.

**The click claim is not verifiable from our side, and is recorded that way.** The Plausible API is
locked (`402 — site is locked due to missing active subscription`) and the PartnerStack dashboard is
operator-only, so the only corroborating sources are unavailable; our own previews and bots also hit a
hop page. Do not carry "clicks are coming in" into any report as measured traffic.

**What the mail does establish is that the hop works.** Re-verified live 2026-10-27 (cache-busted):
`/tools/descript/` **200** with exactly one `href="/go/descript/"`; `/go/descript/` **200** carrying
`get.descript.com/wvafmtthtkp5` twice; `/legal/affiliate-disclosure.html` **200** naming Descript.

**The two dashboard chores below are now the binding constraint on ever being paid** — clicks without
accepted program terms and a payout provider accrue nothing payable. Both are George-only; nothing was
attempted here.

### Copy.ai — no working public route as of 2026-09-12
Its PartnerStack listing shows *Request program* with unfilled placeholders, and
`copyai.partnerstack.com` renders the same dead template. Copy.ai was acquired by Fullcast
in October 2025 and repositioned toward enterprise GTM, which may explain an unmaintained
affiliate listing.
**Next step:** inside the verified PartnerStack dashboard, search the in-app Marketplace for
Copy.ai. If it is not joinable there, treat the program as closed. Do not submit to
`copyai.partnerstack.com/signup` — it is not a live application form.

**Two dead routes previously conflated here, now recorded precisely** (so neither is cited
as evidence again):
- `copyai.partnerstack.com/signup` serves a 15,260-byte generic template with unfilled
  `{{name}}`/`{{company.description}}`. **That signature proves nothing** — the byte-identical
  template is served by `browseai`/`copyai`/`descript`/`gamma.partnerstack.com`, including
  programs we successfully applied to. It is not evidence of availability in either direction.
- `affiliates.copy.ai/apply` is a Notion-hosted SPA (1.3 MB) whose Notion API endpoints 301
  away, so it could not be read from the command line. **Unverified either way** — it may
  still be a working form that only renders in a browser.

The real evidence that Copy.ai is closed: its marketplace listing's embedded state returns
`company: null` — no `base_offers`, no `default_group_application`, no program state at all.
That is the signature of a removed or unlisted program (contrast the six validated open
controls).

### Browse AI — listing OPEN, join BLOCKED by the network limit
**Corrected 2026-09-14: the previous "portal broken, wait for a 200" advice was wrong.**
`affiliates.browse.ai/signup` does return **HTTP 525**, but that subdomain is *not* the
application route — so a 525 there never meant the program was closed. The live route is the
PartnerStack marketplace listing, and it is **open**.

Evidence (marketplace listing's embedded `window.__INITIAL_STATE__.company.company`):
`application=true`, `approved=true`, `archived=false`, `base_offers[0]` = 20% / value 2000 /
*"Earn 20% commission as long as the user is subscribed"*,
`default_group_application=marketplace`.

That discriminator was validated against six programs PartnerStack markets as joinable
(`adcreative`, `activecampaign`, `beautifulai`, `clickup`, `getresponse`, `runpod` — all
`application=true, approved=true`) and three known-closed listings (`canva`, `airtable`,
`logomeai` — `application=false`).

**Next step:** apply from
`market.partnerstack.com/artificial-intelligence/browseai` using its **Apply to program**
button. Do **not** hand-build a `dash.partnerstack.com/application` URL: every such URL
returns an identical 1,428-byte SPA shell regardless of program, so it cannot be verified from
the command line and is not evidence either way.

**BLOCKER ADDED 2026-09-14 (same day) — do not attempt the join.** PartnerStack limited our
marketplace access the same afternoon (see STATUS above). Their words are explicit: *"You will
not be able to join any new programs through our marketplace until your Network Profile has
been approved into our network."* That is a guarantee of failure, not a maybe, so the join is
**not worth an attempt** — and a declined join may itself count against the profile.

The listing being open is a fact about Browse AI; the join is what the network limit gates.
Blocked on the network, not on the vendor. Revisit only after the Network Profile is
re-approved. Do not substitute the dead `affiliates.browse.ai/signup` route.

Terms: 20% recurring for the life of the referral, 30-day cookie, monthly via Wise (PayPal on
request, $200 minimum). Browse AI is already a reviewed tool on the site, so the pitch is
straightforward. The offer's per-click stats show 8.4% signup rate and ~$13.91 revenue per
click, which is strong for this category.

---

## Arvow — public program, held submission (2026-10-15)

`arvow.com` submitted through `/submit-tool.html` on 2026-10-15 and is **held pending
verification** (`admin/held-submissions.md`). Do **not** apply from this note and do **not** wire
anything: there is no review page for a tracking link to live on, and an approval would not change
the hold.

The program is public, so these are readable terms rather than an inbound offer — read from
`arvow.com/affiliates` on **2026-10-15** (not from an email):

- **30% commission, for the life of the referral**, described as uncapped
- Headline figure on the page is "up to $128.70 on each sale every month, for life" — that is 30%
  of $429, which is **not a price published on `/pricing`**, so the headline may be stale
- **90-day cookie, first-touch**
- Payouts **30 days after the referral, at month end**; **$100 minimum**; paid by **PayPal**
- Terms §15 rules: no paid ads on brand keywords or the domain name, no self-referrals and no
  "coworkers", no coupon sites / doorway pages / thin sites, no deceptive promotion
- The same page advertises a **"Creators Program"** where the vendor pays for content — that is a
  paid-placement offer and is **declined** under `/legal/trust.html`

If Arvow clears verification and is listed, re-read the terms at application time rather than
copying these figures forward.

---

## BLOCKED — do not spend time on these

- **Jasper** — hosts through **Impact**, and our Impact publisher account was rejected on
  traffic grounds. `partners.jasper.ai` returns an unavailable campaign.
- **Grammarly** — same Impact dependency; denied 2026-08-25.
  **One unverified lead (2026-09-14):** a Grammarly listing *does* exist on PartnerStack
  (`company key co_s4UUPYp9Nuvh1L`, group `grammarlybusinessaffiliateprogram`) with
  `application=true` — but `approved=false`, i.e. it is not publicly discoverable. Not an open
  route: `application=true` is unreliable for private listings (Notion shows the same while
  its program is officially closed). **Worth one look from inside George's dashboard** — if
  that private Grammarly Business group is visible to him, applying there bypasses Impact
  entirely. Do not attempt it blind from a URL.
- **Canva, Notion** — applications closed.
- **ChatGPT, Claude, GitHub Copilot** — no publisher commission program exists.
- **Midjourney, Zapier** — no open public affiliate application.

**The Impact reapplication is the highest-leverage single action** once traffic grows: it
unlocks Jasper, Grammarly, and every other Impact-hosted program at once.

**Assessed 2026-09-14 — do NOT reapply yet.** Published guidance on Impact approval puts
successful applicants at roughly **5,000+ monthly unique visitors** with engagement proof;
the site currently has **77 visitors / 247 pageviews per 30 days** (Plausible, verified
2026-09-14) against a 58% bounce and 133s average visit. That is ~1.5% of the low bound.
Impact also declined on **MSA standards**, which assess content quality and brand alignment
rather than raw pageviews alone — so the fix is more than traffic, and a second rejection
would burn the retry. Revisit around **20–30 visits/day** as previously recorded.

---

## After approval (per program)

1. Add the tracking URL and `application_status: approved` to `data/affiliate_programs.json`.
   The validator requires the key `affiliate_url` (not `approved_tracking_url`).
2. Run `python3 scripts/wire_affiliate_links.py` — swaps the official-URL CTA for the
   tracking URL across `tools/<slug>/`, `articles/`, `comparisons/`.
3. Pipeline: `daily_content_update.py` → `validate_site.py` → `git push`.
4. Log the approval date in the table above.

## Rejection playbook

If declined for low traffic: reply asking for early-partner consideration, cite the concrete
page count and dated-evidence approach, and reapply in 30 days. Never misstate traffic —
several networks check the live site, and a misrepresentation rejection is not appealable.
