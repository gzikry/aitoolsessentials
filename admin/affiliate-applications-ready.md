# Ready-to-Submit Affiliate Applications

Last verified 2026-09-12 16:05 PT. Site facts below are real and checkable — do not inflate.
Site: 721 public pages, 75 reviewed tools, 16 categories, 192 comparisons, 175 guides.
Traffic, stated honestly: ~66 visitors / 217 pageviews per 30 days (early stage, growing).

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
- **Copy.ai, Browse AI, Descript** → *Request program*, `{{name}}` unfilled → **NOT OPEN**

`copyai.partnerstack.com` and `browseai.partnerstack.com` render the same unpopulated
template, so the vendor-hosted subdomains are not a working fallback either.

---

## STATUS 2026-09-12

**Applied: PartnerStack network account, Gamma (2026-09-12), and Descript (2026-09-12).**

| # | Program | Route | Rate | Status |
|---|---------|-------|------|--------|
| 0 | PartnerStack network | app.partnerstack.com | — | applied 2026-09-12; **email unverified** |
| 1 | Gamma | PartnerStack listing | ~30% rec. | **applied 2026-09-12** |
| 2 | Descript | dash.partnerstack.com/application?company=descriptinc | $25 + 15% rec. | **applied 2026-09-12** — pending review |
| 3 | Copy.ai | PartnerStack listing not open | 45% rec. 12mo | no working route; try in-app Marketplace |
| 4 | Browse AI | own portal 525-broken | 20% rec. life | no working route; report broken portal |
| 5 | ElevenLabs | direct | 22% rec. 12mo | approved 2026-08-23 |
| 6 | Make | direct | 35% rec. 12mo | approved 2026-08-23 |
| 7 | Nous / Hermes | direct | $15 off referral | approved 2026-09-02 |

### Gamma — APPLIED 2026-09-12
Program: https://market.partnerstack.com/artificial-intelligence/gammaapp
Official help: help.gamma.app/en/articles/11048092 · ~30% recurring (confirm in portal).
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

### Browse AI — own portal is broken
`affiliates.browse.ai/signup` returns **HTTP 525 (Cloudflare SSL handshake failed)** on
repeated attempts with two user agents, while `browse.ai/affiliate-program` renders fine.
The affiliate subdomain is misconfigured. Its PartnerStack listing is also not open.
**Next step:** email Browse AI support reporting the portal error, or apply only once the
signup returns 200.

---

## BLOCKED — do not spend time on these

- **Jasper** — hosts through **Impact**, and our Impact publisher account was rejected on
  traffic grounds. `partners.jasper.ai` returns an unavailable campaign.
- **Grammarly** — same Impact dependency; denied 2026-08-25.
- **Canva, Notion** — applications closed.
- **ChatGPT, Claude, GitHub Copilot** — no publisher commission program exists.
- **Midjourney, Zapier** — no open public affiliate application.

**The Impact reapplication is the highest-leverage single action** once traffic grows: it
unlocks Jasper, Grammarly, and every other Impact-hosted program at once.

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
