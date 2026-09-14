# Ready-to-Submit Affiliate Applications

Last verified 2026-09-13 PT. Site facts below are real and checkable — do not inflate.
Site: 736 public pages, 76 reviewed tools, 16 categories, 200 comparisons, 173 guides.
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

**Approved live: Gamma (PartnerStack unique link 2026-09-13). Applied pending: Descript (2026-09-12).**

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
| 1 | Gamma | PartnerStack listing | 25% first year | **approved 2026-09-13; link live 2026-09-13** — https://try.gamma.app/ty4k3o3rpeyd (unaffected by the network limit) |
| 2 | Descript | dash.partnerstack.com/application?company=descriptinc | $25 + 15% rec. | **applied 2026-09-12** — pending review; not cancelled (existing partnerships unaffected) |
| 3 | Copy.ai | PartnerStack listing not open | 45% rec. 12mo | **closed 2026-09-14** — listing dead and the in-app Marketplace fallback is gone with the network limit |
| 4 | Browse AI | market.partnerstack.com/artificial-intelligence/browseai | 20% rec. life | listing open (verified 2026-09-14) but **join gated by the 2026-09-14 network limit** |
| 5 | ElevenLabs | direct | 22% rec. 12mo | approved 2026-08-23 |
| 6 | Make | direct | 35% rec. 12mo | approved 2026-08-23 |
| 7 | Nous / Hermes | direct | $15 off referral | approved 2026-09-02 |
| 8 | Sonaopus | Gumroad | 40% one-time | approved 2026-09-13 |

### Gamma — APPROVED 2026-09-13 / LINK LIVE 2026-09-13
Program: https://market.partnerstack.com/artificial-intelligence/gammaapp
Unique link: https://try.gamma.app/ty4k3o3rpeyd
Commission: 25% for the first year on referred customers (partners@gamma.app / PartnerStack, 2026-09-13 PT).
Wired on `/tools/gamma/` Visit CTA with `rel="sponsored noopener nofollow"` and the existing review disclosure fineprint. Official pricing/docs/privacy/terms stay on gamma.app. Editorial score and cons unchanged.
**Caution:** `gammaapp.ai` is a DIFFERENT company from Gamma — do not cite its 50% claim.

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

### Descript — APPLIED 2026-09-12 (pending review)
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
