# Pitch drafts — 2026-10-26

**Nothing here has been sent. This run sent nothing.** 186 tracked requests, **46 live unpitched, 1
sendable** (`pitch-queue.md`, built 2026-10-26). The ledger still records six `pitched` entries: five
delivered, one bounced (`simon.chandler@raconteur.net`, 550 NoSuchUser — dead mailbox, do not retry).

**Today's window produced no new candidate at all**: 33 slugs, zero AI tokens, zero spend tokens, and
the only body-level AI request (the SHIFT podcast companion-story call) asks for first-hand testimony
we cannot supply. So this document is the same three sends as yesterday, with every figure re-derived
against today's snapshot rather than restated. That is the honest state of the queue: **the send is the
bottleneck, not the supply.**

**One change to draft 1's status, and it matters:** the Business Insider row **left the AI-topic feed
today** while its page still serves 200. It was in the feed on 2026-10-24 and 2026-10-25. Under this
monitor's own rule, a request that stops appearing in the feed is colder than its age suggests — 3 days
old by `datePublished`, but no longer being promoted by the platform. It is still the best row in the
queue and still the one to send first; it is no longer as fresh as it looked yesterday.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **95 tools**;
`data/pricing_snapshots.json` (`updated: 2026-10-26`) yields **44 with a published monthly price, 35
of those at or under $25/month, median $17.50**. Monthly vs annual: **1.11x to 2.53x, median 1.25x
over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16).
**Superseded — do not reuse:** the 94-tool set in the 2026-10-25 draft, the 40/31/$16.50 sets in drafts
before 2026-10-22, and the `1.21x–2.53x, median 1.33x` pair claim sent to Jan Suski on 2026-09-18 and
corrected on 2026-10-10.

---

## 1. Business Insider — European orgs moving from a US AI provider to Mistral ◀ 3d, EMAIL, paste-ready

**Source:** https://www.sourcee.app/journo-request/employees-at-european-orgs-switch-from-us-ai-provider-to-mistral
**Posted:** 2026-10-23 08:46 UTC — **3 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-23T08:46:17Z`, badge "Posted in last 7 days", no expiry notice. **No longer in
the AI-topic feed** (it was, on 2026-10-24 and 2026-10-25). Live, unexpired, no longer promoted.
**Who:** **Thibault Spirlet**, tech reporter, Business Insider London. The page's domain field is
`businessinsider.com`; the body signs *"Thibault Spirlet, Business Insider"*.
**Ask, his words:** employees at European organisations that *"have moved from, or are considering
moving from, a US AI provider like OpenAI or Anthropic, to Mistral"*, especially where data
sovereignty, procurement rules or customer contracts drove it. His fourth question is *"what trade-offs
did the switch create in model quality, cost, or developer experience?"* He offers to talk off the record.

**What we can and cannot answer.** We cannot answer the testimony part — we are not an employee of a
switching organisation, and the draft says so in its first line rather than implying standing. Cost is
one of his four questions, and it is the one we measure with dated source URLs.

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No** (sends are George's lane), but
it is a plain email address, not a DM or a form.
- Resolved off his own byline page, not guessed: https://www.businessinsider.com/author/thibault-spirlet
  **HTTP 200, 326,718 bytes**, title *"Thibault Spirlet - Business Insider"*, re-probed today and
  recorded in `route-checks-2026-10-26.json`; the page publishes a `mailto:` link and the address
  appears **5 times** in the page markup.
- Fallbacks published on the same page: `linkedin.com/in/thibault-spirlet/`, `x.com/ThibaultSpirlet`.
- Deliverability not SMTP-verified — no probe was run against the BI mailbox, and one would not
  discriminate anyway.
- **This is the shortest path to a sent pitch in the entire queue: one email, no form, no login.**

**Subject:** `Mistral vs US providers: the per-seat numbers, dated`

> Hi Thibault —
>
> I can't give you the employee side of this: I run a price dataset, not an organisation that switched.
> I can give you the cost trade-off on your list, measured rather than estimated.
>
> As of today, 2026-10-26: Mistral's Pro tier lists at $14.99/month excluding taxes (checked
> 2026-09-18, mistral.ai/pricing). The comparable US individual tiers both list at $20/month — Claude
> Pro at $20 month-to-month or $17 with the $200 annual prepayment (checked 2026-09-18,
> anthropic.com/pricing), ChatGPT Plus at $20/month (checked 2026-10-01). So at list price the Mistral
> seat is $5.01/month cheaper than either, $60.12 per seat per year, or $2.01/month cheaper against
> Claude Pro prepaid annually. That is the whole of the list-price saving — small enough that it is
> worth stating plainly, because the sovereignty case has to carry the rest. Mistral's enterprise tier
> is a custom quote, so the number your sources feel is a negotiation, not a list price.
>
> Same method, wider: of the 95 AI tools we track, 44 publish a monthly per-seat price; 35 of those
> start at or under $25/month, median $17.50.
>
> Every figure carries its check date and the vendor URL behind it. Free to use, no attribution needed.
>
> AIToolsEssentials

*Word count: 198 words including the signature — measured by `scripts/verify_drafts.py` on this file (subject line excluded).*

---

## 2. Fast Company Work Life — AI at work, jobs and hiring ◀ 16d, LATE SEND — EMAIL, paste-ready

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **16 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-10T13:51:49Z`, no expiry notice. **Not in the newest AI-topic feed.**
**Who:** **Tobi Amure** — the page's own author field; sourcing for **Fast Company's Work Life** section.
**Ask, his words:** *"For experts: the credential and the research behind it. Original data, or a survey
with its sample size and method. Workplace expert is not a credential."* He is *"not placing bylined
guest posts"* — so this offers a dataset, never a post. **The door:** *"No DM pitches here on LinkedIn.
Email me."*

**Reply route:** **hello@tobiamure.com** — self-published on his own site. Re-probed today:
https://tobiamure.com/ **HTTP 200, 62,818 bytes**, title *"Tobi Amure, CFEI® | Finance & Technology
Journalist"*, address present **6 times**; fallback https://tobiamure.com/contact/ **HTTP 200, 17,905
bytes**, address 5 times, beside a contact form. **Automatable? No** — George's lane.
**Deliverability is not SMTP-verified.** `tobiamure.com` MX is Namecheap forwarding and answers
554 5.7.1 Relay access denied for `hello@`, a fake control and `postmaster@` alike, so the probe
discriminates nothing. Self-publication on his live site is the evidence; a bounce is itself the answer.

**Subject:** `The $17.50 median: method and denominator first`

> Hi Tobi —
>
> Method first, since that is the bar you set. This is not a survey: it is a census of published list
> prices. We hand-check the pricing page of 95 AI tools and store the date of every check.
>
> As of today, 2026-10-26, 44 of those 95 publish a monthly per-seat price. 35 of the 44 start at or
> under $25/month, and the median cheapest paid tier is $17.50.
>
> The same set answers the annual-discount question. Paying monthly instead of yearly costs between
> 1.11x and 2.53x, median 1.25x across 19 tiers, pair set re-asserted 2026-10-16. Two rows with their
> check dates: Browse AI Personal is $48/month or $19/month billed annually, 2.53x
> (browse.ai/pricing, checked 2026-09-18); Otter.ai Pro is $16.99/month or $8.33/month billed
> annually, 2.04x (otter.ai/pricing, checked 2026-09-18).
>
> For your AI-at-work lane that is the personal-economics half: what a seat costs the individual, and
> how often it comes out of their own pocket.
>
> You asked for the credential too. I do not have one to offer; I have a dated dataset, its method, and
> the source URL behind every number, free to use.
>
> AIToolsEssentials

*Word count: 184 words including the signature — measured by `scripts/verify_drafts.py` on this file (subject line excluded).*

---

## 3. WSJ blocked work accounts — what the workaround buyer pays ◀ 21d, LATE SEND — LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **21 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-05T15:15:11Z`, no expiry notice.
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist.
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work
by hand.

**Honesty constraint — do not edit out.** The request wants the respondent's own annoyance. We are a
publisher, not a blocked employee. The draft says so in its first sentence.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-probed
today: **HTTP 200, 624,994 bytes**, title *"Christopher Mims - The Wall Street Journal | LinkedIn"*.
The request's own body says *"(DMs open)"*. **Automatable? No** — no address, no form, no booking link;
the text below is the whole message and must go from George's own LinkedIn.
Dead ends recorded so they are not retried: `muckrack.com/christopher-mims` HTTP 403,
`wsj.com/news/author/christopher-mims` HTTP 401.

**Subject:** none (DM)

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 95 AI tools. 44 publish a monthly price and 35 of those start at or under $25/month — median $17.50, checked today (2026-10-26).
>
> That is what the people who route around a blocked work account pay. Browse AI Personal is $48/month against $19/month billed annually (2.53x, checked 2026-09-18); Otter.ai Pro is $16.99 against $8.33 (2.04x, same date). Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Word count: 126 words including the signature — measured by `scripts/verify_drafts.py` on this file (subject line excluded).*

---

## Not redrafted deliberately

- **This run's two new rows are not drafts.** `people-using-llms-as-companions-emotional-support-stories`
  (Kim Shirin Cupal with Hilke Schellmann, SHIFT podcast, Pulitzer-funded): the ask is your own story of
  using an AI companion; it publishes a real route for the first time on this monitor — Reddit
  `u/KimCupal` and Discord `kimcupal`, both printed in the body — but we have no such story to tell, and
  we would have to invent one. `sound-artists-and-field-recordists-run-radio-aarhus-open-call`: its
  body-level "ai" hit is a substring artefact; it is an open call for field recordings, not an AI
  request, with a redacted address.
- **The 45 other live rows** are relevance `low` (a handful `low-medium`) with no resolved route, so
  drafting one would mean claiming standing we do not have. The exclusions are documented per row in
  `digest-2026-10-26.json`. The three `high` rows that are not BI — finops (49d, LinkedIn DM), Science
  Magazine (51d, thread reply), Forbes (97d) — are all far past the line and have been drafted or
  excluded before; re-drafting them a fifth time is the failure mode this file exists to stop.
