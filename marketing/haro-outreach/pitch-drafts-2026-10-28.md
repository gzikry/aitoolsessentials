# Pitch drafts — 2026-10-28

**Nothing here has been sent. This run sent nothing — sends are George's lane.** 201 tracked
requests, **51 live unpitched, 3 sendable** (`pitch-queue.md`, built 2026-10-28). That is the first
three-sendable day this monitor has recorded: two of the three are new finds from today's window,
not re-readings of a carried row.

**Today's window: 106 slugs, 5 AI-token, 0 AI+spend, 6 body-level AI hits, 0 of those carrying a
real spend token.** All 106 bodies were fetched and read. Six rows were added; five of them ask for
testimony or standing we do not have and publish no route.

**The find of the day.** Forbes / **Alison Coleman** posted two requests seven minutes apart on
2026-10-27: US solopreneurs whose AI use changed when the first hire happens (12:57Z) and
bootstrapped US founders who can *quantify* how AI cut the capital or headcount needed (12:50Z). Both
are 1 day old, both HTTP 200, both in today's AI-topic feed, and both redact the address — but she
publishes her own on her site: **alison@alisoncoleman.co.uk**, in visible text on
`alisoncoleman.co.uk/contact-me/` (HTTP 200, 28,082 bytes, `route-checks-2026-10-28.json`), with that
page's contact form as the fallback. **Section 1 covers both asks in one email**, which is why two
rows are closed by one send.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **99 tools**;
`data/pricing_snapshots.json` (`updated: 2026-10-28`) yields **44 with a published monthly per-seat
price, 35 of those at or under $25/month, median $17.50**. Monthly vs annual: **1.11x to 2.53x,
median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16).
**Superseded — do not reuse:** the 97-tool set in the 2026-10-27 drafts and the two drafts staged in
Gmail on that date (both re-staged today), the 95-tool set in the 2026-10-26 draft, the 94-tool set in
the 2026-10-25 draft, the 40/31/$16.50 sets before 2026-10-22, and the `1.21x–2.53x, median 1.33x`
pair claim sent to Jan Suski on 2026-09-18 and corrected on 2026-10-10.

**Platforms, unchanged:** HARO and Connectively HTTP 429 behind a Vercel checkpoint (expected — not
retried), Qwoted 404 at the app, Medialyst MCP 401, Source of Sources 404 at /requests, MentionMatch
200 but account-gated, ResponseSource 200 public pages with a paywalled request database. Sourcee is
the only usable source. **Mailbox: zero replies** — measured today with `jansuski.com` as a positive
control that returned its two known messages (msgs 234, 305), so the zero is a fact and not a broken
query.

---

## 1. Forbes — US solopreneurs: AI and the first hire, and bootstrapped founders ◀ 1d, EMAIL, SEND THIS ONE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted 2026-10-27 12:50Z, seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **1 day.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge "Posted in last 7 days", no expiry notice. **In today's
AI-topic feed** (one of only 5 AI-token slugs in a 106-slug window).
**Who:** **Alison Coleman**, Forbes senior contributor; her Forbes bio (read via search today, since
forbes.com 403s to us) describes her as a freelance journalist and founder of Coleman Media Ltd.
covering entrepreneurs and their startups.
**Ask, her words:** *"US #solopreneurs, genuinely one-person business that have used AI to eliminate
the need to hire, or simply change when and why the first hire happens."* The sibling request asks
founders who can *"quantify how AI has reduced the capital/headcount needed to build their company."*

**What we can and cannot answer.** Not the testimony — we are a publisher with a price dataset, and
the draft says so in its second line rather than implying standing. The *quantified* half is exactly
what we hold: what the substitute costs, per seat, per month, with check dates.

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A plain published email, not a
DM and not a form, but every send in this queue is George's.
- Resolved off her own site, not guessed: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200,
  28,082 bytes**, title *"Contact me : Alison Coleman"*, prints in visible body text
  `Email: alison@alisoncoleman.co.uk`, `Twitter: @alisonbcoleman`, `Skype: alisonbcoleman`, beside a
  Contact Form 7 form (`/contact-me/#wpcf7-f52-p21-o1`) as the fallback. Recorded in
  `route-checks-2026-10-28.json`. Homepage https://www.alisoncoleman.co.uk/ **HTTP 200, 21,396
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
> The cost half of the substitution, as of 2026-10-28: of the 99 AI tools we track, 44 publish a monthly per-seat price; 35 of those sit at or under $25, and the median cheapest paid tier is $17.50. Billing is where the arithmetic moves — across 19 same-tier monthly/annual pairs, paying monthly costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). Browse AI Personal: $48/month, or $19/month billed annually (browse.ai/pricing, checked 2026-09-18).
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic from the capital side. One dataset answers both, and every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 165 including the signature — measured on this file, subject line excluded.*

---

## 2. Business Insider — European orgs moving from a US AI provider to Mistral ◀ 5d, EMAIL

**Source:** https://www.sourcee.app/journo-request/employees-at-european-orgs-switch-from-us-ai-provider-to-mistral
**Posted:** 2026-10-23 08:46 UTC — **5 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-23T08:46:17Z`, badge "Posted in last 7 days", no expiry notice. **Not in
today's AI-topic feed** (third consecutive day out — colder than 5 days suggests, and still live).
**Who:** **Thibault Spirlet**, tech reporter, Business Insider London. The body signs *"Thibault
Spirlet, Business Insider"*; page domain `businessinsider.com`.
**Ask, his words:** employees at European organisations that *"have moved from, or are considering
moving from, a US AI provider like OpenAI or Anthropic, to Mistral"*, especially where data
sovereignty, procurement rules or customer contracts drove it. Fourth question: *"what trade-offs did
the switch create in model quality, cost, or developer experience?"* Off the record is offered.

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No.**
- Resolved off his own byline page: https://www.businessinsider.com/author/thibault-spirlet **HTTP
  200, 328,516 bytes** today, title *"Thibault Spirlet - Business Insider"*, `mailto:` link present,
  address published 5 times in the markup (`route-checks-2026-10-28.json`).
- Why this one still matters after six runs: he was commissioning on 2026-10-26 (a second request went
  up at 11:46Z), so the inbox is live even though this request has stopped being promoted.

**Subject:** `Mistral vs US providers: the per-seat numbers, dated`

> Hi Thibault —
>
> I saw you're sourcing again this week, so: on the Mistral switch I can't give you the employee side. I run a price dataset, not an organisation that switched. I can give you the cost trade-off on your list, measured rather than estimated.
>
> As of today, 2026-10-28: Mistral's Pro tier lists at $14.99/month excluding taxes (mistral.ai/pricing, checked 2026-09-18). The comparable US individual tiers both list at $20 — ChatGPT Plus (openai.com/chatgpt/pricing, checked 2026-10-01) and Claude Pro month-to-month (anthropic.com/pricing, checked 2026-09-18). So the list-price saving is $5.01 per seat per month, $60.12 a year; against Claude Pro prepaid annually at $17 it is $2.01 a month, $24.12 a year.
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

## 3. Fast Company Work Life — AI at work, jobs and hiring ◀ 18d, LATE SEND — EMAIL

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **18 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-10T13:51:49Z`, no expiry notice. **Not in today's AI-topic feed.**
**Who:** **Tobi Amure** — the page's own author field; sourcing for **Fast Company's Work Life**.
**Ask, his words:** *"For experts: the credential and the research behind it. Original data, or a
survey with its sample size and method. Workplace expert is not a credential."* He is *"not placing
bylined guest posts"* and says *"No DM pitches here on LinkedIn. Email me."*

**Reply route:** **hello@tobiamure.com** — self-published on his own site; re-probed today,
https://tobiamure.com/ **HTTP 200, 63,200 bytes**, title *"Tobi Amure, CFEI® | Finance & Technology
Journalist"*; fallback https://tobiamure.com/contact/ **HTTP 200, 18,362 bytes** with a form.
**Automatable? No** — George's lane. Deliverability is not SMTP-verified: the domain's MX answers
554 Relay access denied for `hello@`, a fake control and `postmaster@` alike, so a bounce is the only
real evidence.

**This is now a send-or-skip decision, not a draft.** It has been rewritten on four consecutive runs
and crossed the 10-day line on 2026-10-21. Send it late, or put a `skipped` entry in
`pitch-ledger.json`. A fifth rewrite is not an option this monitor should keep offering.

**Subject:** `The $17.50 median: method and denominator first`

> Hi Tobi —
>
> Method first, since that is the bar you set. This is not a survey: it is a census of published list prices. We hand-check the pricing page of 99 AI tools and store the date of every check.
>
> As of today, 2026-10-28, 44 of those 99 publish a monthly per-seat price. 35 of the 44 start at or under $25/month, and the median cheapest paid tier is $17.50.
>
> The same set answers the annual-discount question. Paying monthly instead of yearly costs between 1.11x and 2.53x, median 1.25x across 19 tiers, pair set re-asserted 2026-10-16. Two rows with their check dates: Browse AI Personal is $48/month or $19/month billed annually, 2.53x (browse.ai/pricing, checked 2026-09-18); Otter.ai Pro is $16.99/month or $8.33/month billed annually, 2.04x (otter.ai/pricing, checked 2026-09-18).
>
> For your AI-at-work lane that is the personal-economics half: what a seat costs the individual, and how often it comes out of their own pocket.
>
> You asked for the credential too. I do not have one to offer; I have a dated dataset, its method, and the source URL behind every number, free to use.
>
> AIToolsEssentials

*Word count: 184 including the signature — measured on this file, subject line excluded.*

---

## Not redrafted deliberately

- **The WSJ / Christopher Mims row** (`employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  23 days, LinkedIn DM to `linkedin.com/in/christopher-mims-club/`, HTTP 200 re-probed today) still
  has its paste-ready 126-word DM in `pitch-drafts-2026-10-27.md` §3. It is not rewritten here
  because at 23 days the useful action is a DM from George's own LinkedIn or a `skipped` entry.
- **The other four new rows** are excluded on standing, not on format:
  `users-who-linked-bank-and-brokerage-accounts-to-llms-ai-finance` (MarketWatch, consumer bank-linked
  testimony, address redacted), `musicians-artists-writers-and-creators-ai-impact-on-creativity` (no
  publication named, no route at all), `ai-startup-founders-and-marketers-b2b-marketing-as-show-business`
  (LiveMint marketing practice, no route), and `literary-writers-thoughts-on-lit-mags-funny-deep-frustrated`
  (the AI token is the columnist's joke).
- **Every other live row** in `pitch-queue.md` sits in "Live but not sendable": no resolved route, or
  relevance at the tangential band. Pitching one would mean claiming standing we do not have.

---

## Still true, and the reason this file exists

A written draft is not progress. Three sends (or three `skipped` entries in `pitch-ledger.json`)
close today; more drafting does not. All three routes above are email addresses a human sends from —
none is machine-writable, which is why 201 tracked requests have produced six sends.
