# Pitch drafts — 2026-10-29

**Nothing here has been sent. This run sent nothing — every route is an email, a DM or a platform
reply, all George's lane.** 210 tracked requests, **60 live unpitched, 4 sendable**
(`pitch-queue.md`, built 2026-10-29). Yesterday's three drafts are still unsent; today refreshes the
two that got stronger and swaps the third for a fresher row.

**What today actually changed.** Two of yesterday's three rows are still the best two in the queue
and both got *more* sendable, not less:

1. **Alison Coleman's two Forbes requests** are now **2 days old** (yesterday: 1) and still HTTP 200.
   Her address re-probed live today: `alisoncoleman.co.uk/contact-me/` **HTTP 200, 28,116 bytes**
   (`route-checks-2026-10-29.json`). One email closes both rows.
2. **Thibault Spirlet's Mistral row** is now **6 days old** and out of the AI-topic feed — but he
   posted a **new Business Insider call at 2026-10-28T16:43Z** (AI researchers and founders who fear
   an AI apocalypse, and what that does to their retirement saving), his **second inside 72 hours**
   after the 2026-10-26T11:46Z traders call. The reporter is demonstrably working this week. That is
   the strongest argument this monitor has ever had for his row, and section 2 now opens on it.

**The swap.** Fast Company / Tobi Amure is now **19 days** old and cold. It is still live and still
has a verified email (`hello@tobiamure.com`), and its paste-ready draft is unchanged in
`pitch-drafts-2026-10-28.md` §3 — but rewriting it a sixth time is not progress. In its place,
section 3 drafts the window's only fresh on-beat row: **Vidhya Das / Business Today**, 1 day old, in
the AI feed, on workplace AI adoption and the skills needed to use the tools.

**Today's window: 86 slugs, 7 AI-token, 0 AI+spend, 8 body-level AI hits, 0 of those carrying a real
spend token.** All 86 bodies were fetched and read; 9 rows added, 8 of them relevance low (three want
first-person testimony, three publish no route on beats where we have no standing, one is a founder
feature promo rather than a request, one has no AI in its body at all — an `ai` substring inside
`DIY`). The body scan earned its keep again: `rig-hse-staff-aienabled-cameras-trial-outcomes` carries
its AI token only as the squashed slug `aienabled` and is invisible to the slug matcher.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **99 tools**;
`data/pricing_snapshots.json` (`updated: 2026-10-29`) yields **44 with a published monthly per-seat
price, 35 of those at or under $25/month, median $17.50**. Monthly vs annual: **1.11x to 2.53x,
median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16).
**Superseded — do not reuse:** the 97-tool set in the 2026-10-27 drafts, the 95-tool set in the
2026-10-26 draft, the 94-tool set in the 2026-10-25 draft, the 40/31/$16.50 sets before 2026-10-22,
and the `1.21x–2.53x, median 1.33x` pair claim sent to Jan Suski on 2026-09-18 and corrected
2026-10-10.

**Platforms, unchanged:** HARO and Connectively HTTP 429 behind a Vercel checkpoint (expected — not
retried), Qwoted 404 at the app, Medialyst MCP 401, Source of Sources 404 at /requests, MentionMatch
200 but account-gated, ResponseSource 200 public pages with a paywalled request database. Sourcee is
the only usable source. **Mailbox: zero replies** — measured today with `jansuski.com` as a positive
control that returned its two known messages (msgs 234, 305), so the zero is a fact and not a broken
query.

**Feed membership no longer means what earlier runs treated it as.** 86 slugs entered the sitemap
window in ~24h against a 50-slot AI-topic feed, so the feed turns over in well under a day and only
**1 of the 54** tracked live rows appears in it. "Dropped off the feed" is now ordinary, not a
cooling signal; ages below come from each page's own `datePublished`.

---

## 1. Forbes — US solopreneurs: AI and the first hire, and bootstrapped founders ◀ 2d, EMAIL, SEND THIS ONE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted 2026-10-27 12:50Z, seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **2 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge "Posted in last 7 days", no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor; her Forbes bio (read via search, since
forbes.com 403s to us) describes her as a freelance journalist and founder of Coleman Media Ltd.
covering entrepreneurs and their startups.
**Ask, her words:** *"US #solopreneurs, genuinely one-person business that have used AI to eliminate
the need to hire, or simply change when and why the first hire happens."* The sibling request asks
founders who can *"quantify how AI has reduced the capital/headcount needed to build their company."*

**What we can and cannot answer.** Not the testimony — we are a publisher with a price dataset, and
the draft's second line says so rather than implying standing. The *quantified* half is exactly what
we hold: what the substitute costs, per seat, per month, with check dates.

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A plain published email, not a
DM and not a form, but every send in this queue is George's.
- Resolved off her own site, not guessed: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200,
  28,116 bytes today**, title *"Contact me : Alison Coleman"*, prints in visible body text
  `Email: alison@alisoncoleman.co.uk`, `Twitter: @alisonbcoleman`, `Skype: alisonbcoleman`, beside a
  Contact Form 7 form (`/contact-me/#wpcf7-f52-p21-o1`) as the fallback. Recorded in
  `route-checks-2026-10-29.json`. Homepage https://www.alisoncoleman.co.uk/ **HTTP 200, 21,396
  bytes**, title *"Alison Coleman"*.
- `alisoncoleman.co.uk` MX = Google Workspace (`aspmx.l.google.com` first). Deliverability is not
  SMTP-verified — a Google MX accepts at RCPT whatever the mailbox, so only a bounce proves anything.
- Dead end recorded so it is not retried: `forbes.com/sites/alisoncoleman/` answers **HTTP 403**
  (770 bytes) to us; her own site is the readable route.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> You asked US one-person businesses how AI changed when the first hire happens. I can't give you that from inside one, so I won't pretend to. I run a price dataset: what AI tools list at, read off each vendor's own pricing page, with the date of every check.
>
> The cost half of the substitution, as of 2026-10-29: of the 99 AI tools we track, 44 publish a monthly per-seat price; 35 of those sit at or under $25, and the median cheapest paid tier is $17.50. Billing is where the arithmetic moves — across 19 same-tier monthly/annual pairs, paying monthly costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). Browse AI Personal: $48/month, or $19/month billed annually (browse.ai/pricing, checked 2026-09-18).
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic from the capital side. One dataset answers both, and every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 165 including the signature — measured on this file, subject line excluded.*

---

## 2. Business Insider — European orgs moving from a US AI provider to Mistral ◀ 6d, EMAIL

**Source:** https://www.sourcee.app/journo-request/employees-at-european-orgs-switch-from-us-ai-provider-to-mistral
**Posted:** 2026-10-23 08:46 UTC — **6 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-23T08:46:17Z`, badge "Posted in last 7 days", no expiry notice. Not in
today's AI-topic feed (fourth consecutive day out — see the header note on why that now means little).
**Who:** **Thibault Spirlet**, tech reporter, Business Insider London. The body signs *"Thibault
Spirlet, Business Insider"*; page domain `businessinsider.com`.
**Ask, his words:** employees at European organisations that *"have moved from, or are considering
moving from, a US AI provider like OpenAI or Anthropic, to Mistral"*, especially where data
sovereignty, procurement rules or customer contracts drove it. Fourth question: *"what trade-offs did
the switch create in model quality, cost, or developer experience?"* Off the record is offered.

**Why now, not tomorrow:** he posted a fresh Business Insider call at **2026-10-28T16:43Z** (AI
researchers and founders who believe AI poses an existential risk, on retirement saving), his second
inside three days after the 2026-10-26T11:46Z traders call. He is actively commissioning and reading
his inbox this week; next week is a guess.

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No.**
- Resolved off his own byline page: https://www.businessinsider.com/author/thibault-spirlet **HTTP
  200, 328,800 bytes today**, title *"Thibault Spirlet - Business Insider"*, `mailto:` link present,
  address published 5 times in the markup (`route-checks-2026-10-29.json`). Fallbacks on the same
  page: `linkedin.com/in/thibault-spirlet/` and `x.com/ThibaultSpirlet`.

**Subject:** `Mistral vs US providers: the per-seat numbers, dated`

> Hi Thibault —
>
> I saw you're sourcing again this week, so: on the Mistral switch I can't give you the employee side. I run a price dataset, not an organisation that switched. I can give you the cost trade-off on your list, measured rather than estimated.
>
> As of today, 2026-10-29: Mistral's Pro tier lists at $14.99/month excluding taxes (mistral.ai/pricing, checked 2026-09-18). The comparable US individual tiers both list at $20 — ChatGPT Plus (openai.com/chatgpt/pricing, checked 2026-10-01) and Claude Pro month-to-month (anthropic.com/pricing, checked 2026-09-18). So the list-price saving is $5.01 per seat per month, $60.12 a year; against Claude Pro prepaid annually at $17 it is $2.01 a month, $24.12 a year.
>
> That is all of it — small enough that the sovereignty case has to carry the rest, which is worth saying plainly. Mistral's enterprise tier is a custom quote, so what your sources feel is a negotiation, not a list price.
>
> Same method, wider: of the 99 AI tools we track, 44 publish a monthly per-seat price, 35 of those at or under $25, median $17.50.
>
> Every figure carries its check date and vendor URL. Free to use, no attribution needed.
>
> AIToolsEssentials

*Word count: 193 including the signature — measured on this file, subject line excluded.*

---

## 3. Business Today — workplace AI adoption and the skills to use the tools ◀ 1d, LINKEDIN DM, NEW

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **1 day.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge "Posted in last 7 days", **in today's AI-topic feed**.
**Who:** **Vidhya Das**, Business Today (India Today group). Her author page
`businesstoday.in/author/vidhya-das` **HTTP 200, 662,049 bytes**, title *"Trainee Sub Editor"*.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI)
in the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI
experts, enterprise AI trainers, researchers and technology professionals"* on *"workplace AI
adoption, employee training and the skills needed to use AI efficiently."*

**The honest fit.** We are not a trainer and not an enterprise researcher; the draft says so. What we
hold is the procurement half of her story: what a seat actually costs, which is why adoption happens
faster than training does. That is a real contribution to her piece, not a pitch about the site.

**Reply route:** **LinkedIn DM to `in.linkedin.com/in/vidya-das`** — **automatable? No.** Her
request body redacts the email (*"You can also email me at [email redacted]"*) and offers *"comment
below or DM me on LinkedIn"*.
- The handle was resolved **through search on 2026-10-29**, not off the request page: profile title
  *"Trainee Sub Editor | Business Today | India Today group"*. **LinkedIn answers HTTP 999 to this
  monitor's probe**, so the handle is search-resolved rather than page-verified — check the profile
  matches her face and masthead before sending. Her Business Today author page publishes no address.
- This is the weakest route of the three (a DM, not a published email) and it is the third for that
  reason, not the first.

**Subject (DM has none — first line does the work):**

> Hi Vidhya — I can't answer as a trainer, so I won't pitch myself as one. I run a dated price census of AI tools, which covers the part of your story that sits under the training question: what a seat costs, and therefore why adoption outruns it.
>
> As of 2026-10-29: of the 99 AI tools we track, 44 publish a monthly per-seat price. 35 of those start at or under $25, and the median cheapest paid tier is $17.50 — cheap enough that an employee can adopt a tool without asking anyone. Annual billing barely helps: across 19 same-tier pairs, monthly costs 1.11x to 2.53x the annual rate, median 1.25x (re-asserted 2026-10-16).
>
> If your story is about the skills gap, that is the number that explains why the gap exists: the spending decision is small enough to stay invisible to whoever owns the training budget.
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 163 including the signature — measured on this file, subject line excluded.*

---

## Not redrafted deliberately

- **Fast Company / Tobi Amure** (`tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`, **19
  days**, `hello@tobiamure.com` — route re-probed today, `tobiamure.com` HTTP 200, 63,200 bytes).
  Live, cold, and carrying a finished 184-word draft in `pitch-drafts-2026-10-28.md` §3. A sixth
  rewrite is not progress: send it late or put a `skipped` entry in `pitch-ledger.json`.
- **WSJ / Christopher Mims** (`employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **24 days**, LinkedIn DM to `linkedin.com/in/christopher-mims-club/`, HTTP 200 re-probed today).
  Paste-ready 126-word DM in `pitch-drafts-2026-10-27.md` §3. Same call: send late or record skipped.
- **The other eight new rows** are excluded on standing, not on format — three want first-person
  testimony (Character AI users; an unpaid documentary crew call; Spirlet's existential-risk
  retirement piece, which needs a belief we do not hold), three publish no route on beats where we
  have no standing (Canadian trades/manufacturing, rig HSE camera trials, dairy livestock), one is a
  founder-feature promo rather than a request (GCC / Lenks.ai), and one has no AI in its body at all
  (SBS `Insight` DIY property sales — the token matched an `ai` substring inside `DIY`).
- **Every other live row** in `pitch-queue.md` sits in "Live but not sendable": no resolved route, or
  relevance at the tangential band. Pitching one would mean claiming standing we do not have.

---

## Still true, and the reason this file exists

Eight consecutive runs have ended with drafts and zero sends; the send count has sat at six since
2026-10-10. One email today (section 1) closes two live Forbes requests; a second closes the Business
Insider row while its reporter is visibly commissioning. Re-drafting is not on that list.
