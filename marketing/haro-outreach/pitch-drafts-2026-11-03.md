# Pitch drafts — 2026-11-03

**Nothing here has been sent. This run sent nothing — every route is an email or a DM, all George's
lane.** 232 tracked requests, **50 live unpitched, 4 sendable** (`pitch-queue.md`, built
2026-11-03). The queue has been empty of sends since 2026-10-10: six ledger entries, five delivered,
one bounced.

**What changed since the last run (2026-10-29 — five days, not one).** No monitor run happened
between Friday 2026-10-29 and today, so this sitemap window spans **309 slugs over five days** (18
AI-token, 1 AI+spend, 20 body-level AI hits, every one of the 309 bodies fetched and read) instead of
the ~90 a daily run sees. Out of that: **22 rows added, one of them draftable**, and **32 rows
crossed the 10-day line** in the gap — the largest single crossing this monitor has recorded,
because it is five days of ageing in one step.

**What today actually moved, in one line each:**

1. **A new row is the most urgent in the queue.** Kelsey Ziser / **InformationWeek**, posted today,
   on *AI orphans* — agents abandoned by their users or never tied to a human identity — with a
   **hard deadline of Wednesday EOD, 2026-11-04, i.e. tomorrow**. Address redacted on the request;
   resolved off her own author page today at **Kelsey.ziser@informationweek.com**. Drafted as §2.
2. **Alison Coleman's two Forbes requests are now 7 days old** and still the cleanest send in the
   queue: one email closes both calls, to a published address verified live again today
   (`alisoncoleman.co.uk/contact-me/`, HTTP 200, 28,113 bytes). Drafted as §1.
3. **Thibault Spirlet's Mistral row has crossed cold at 11 days.** Its draft stands unchanged in
   `pitch-drafts-2026-10-29.md` §2 and the route is still live, but this run stops ranking it as
   actionable. Send it late or record it skipped — re-drafting it a third time is not on this list.
4. **Vidhya Das / Business Today is 6 days old** and still the best on-beat row for our core
   subject; its only route remains a search-resolved LinkedIn handle. Drafted as §3.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **105 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-03`) yields **44 with a published monthly per-seat
price, 35 of those at or under $25/month, median $16.50**. Monthly vs annual: **1.11x to 2.53x,
median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted 2026-10-16).
**Superseded — do not reuse:** the 99-tool / median $17.50 set in every draft before today, the
97-tool set (2026-10-27), the 95-tool set (2026-10-26), the 94-tool set (2026-10-25), the
40/31/$16.50 sets before 2026-10-22, and the `1.21x–2.53x, median 1.33x` pair claim sent to Jan
Suski on 2026-09-18 and corrected 2026-10-10.

**Platforms.** HARO and Connectively both answered **HTTP 200** on their homepages today for the
first time in this monitor's history — but those are marketing shells with no public query list, and
Connectively's `/queries` still answers **HTTP 429 behind a Vercel checkpoint**. The email wall has
not moved, only the landing page's status code. Qwoted 404 at the app, Medialyst MCP 401, Source of
Sources 404 at `/requests`, MentionMatch 200 but account-gated, ResponseSource public pages only.
Sourcee remains the only usable source.

**Mailbox: zero replies** — measured today with `jansuski.com` as a positive control that returned
its two known messages (msgs 234, 305) before the sweep, so the zero is a fact and not a broken
query. No reply has arrived to any pitch since 2026-10-11.

---

## 1. Forbes — US solopreneurs: AI and the first hire, and bootstrapped founders ◀ 7d, EMAIL, SEND THIS ONE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted 2026-10-27 12:50Z, seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **7 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge "Posted in last 7 days", no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups;
page domain `forbes.com`.
**Ask, her words:** *"US #solopreneurs, genuinely one-person business that have used AI to eliminate
the need to hire, or simply change when and why the first hire happens."* The sibling asks founders
who can *"quantify how AI has reduced the capital/headcount needed to build their company."*

**What we can and cannot answer.** Not the testimony — we are a publisher with a price dataset, and
the draft's second line says so rather than implying standing. The *quantified* half is ours: what
the substitution costs, per seat, per month, with check dates.

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A plain published email, not a
DM and not a form, but every send in this queue is George's.
- Re-probed live today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,113 bytes**,
  title *"Contact me : Alison Coleman"*, address printed in visible body text beside a Contact Form 7
  form as fallback (`route-checks-2026-11-03.json`). Homepage `alisoncoleman.co.uk/` **HTTP 200,
  21,397 bytes**.
- Dead end recorded so it is not retried: `forbes.com/sites/alisoncoleman/` answers **HTTP 403** to
  us; her own site is the only readable route.
- `alisoncoleman.co.uk` MX = Google Workspace. Deliverability is not SMTP-verified — a Google MX
  accepts at RCPT whatever the mailbox, so only a bounce proves anything.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> You asked US one-person businesses how AI changed when the first hire happens, and founders who
> can quantify what AI took out of the build. I can't answer from inside one, so I won't pretend to.
> I run a price census: what AI tools list at, read off each vendor's own pricing page, with the date
> of every check.
>
> As of 2026-11-03: of the 105 AI tools we track, 44 publish a monthly per-seat price; 35 of those
> sit at or under $25, and the median cheapest paid tier is $16.50. On that median, five seats cost
> $82.50 a month, about $990 a year — the figure a solo founder weighs against a salary. Billing is
> the other half: across 19 same-tier monthly/annual pairs, paying monthly costs 1.11x to 2.53x the
> annual rate, median 1.25x (pair set re-asserted 2026-10-16).
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic from the
> capital side. One dataset answers both, and every figure carries its vendor URL and check date.
> Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 179 including the signature — measured on this file, subject line excluded.*

---

## 2. InformationWeek — CIOs and CISOs on AI orphans ◀ 0d, EMAIL, DEADLINE TOMORROW (2026-11-04 EOD)

**Source:** https://www.sourcee.app/journo-request/cios-and-cisos-steps-to-address-ai-orphans
**Posted:** 2026-11-02 18:10 UTC — **0 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-02T18:10:28Z`, badge "Posted in last 7 days", **in today's AI-topic feed**.
**Also the only time-boxed row in the whole queue:** the body's own words are *"Deadline for
interviews is Wednesday EOD"* — **2026-11-04**.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek (`informationweek.com`), author of a
recent *"FedEx CISO: Vet AI agents with guardrails first"*.
**Ask, her words:** *"Looking for CIOs and CISOs to discuss what steps they can take to address the
problem of AI orphans — AI agents that are abandoned by their human users or aren't associated with
a human's identity."* A follow-up to her earlier piece.

**The honest fit.** We are not a CIO or a CISO and the draft opens by saying so. What we hold is the
step *before* the orphan exists: per-seat pricing low enough that a single team can stand up an agent
without a procurement review — and a procurement review is usually where an owner gets assigned.

**Reply route:** **Kelsey.ziser@informationweek.com** — **automatable? No.** Email to a published
address; the send is George's.
- The request body redacts its address (*"Email: [email redacted]"*). The route was resolved **off
  her publication's own author page today**, not guessed:
  https://www.informationweek.com/author/kelsey-ziser **HTTP 200, 587,272 bytes**, title *"Kelsey
  Ziser | Senior Editor, InformationWeek"*, publishing `Kelsey.ziser@informationweek.com` twice in
  the markup (both casings). Recorded in `route-checks-2026-11-03.json`, probed with
  `probe_routes.py --add` so tomorrow's run re-checks it.
- The only other link on the request page is `lnkd.in/eECBX7_D`, her earlier article on LinkedIn —
  login-walled and not a reply route.
- Because the deadline is tomorrow, this is the one row where waiting costs the opportunity rather
  than the freshness.

**Subject:** `Where AI orphans come from: the seat price that skips procurement`

> Hi Kelsey —
>
> I'm not a CIO or a CISO, so I can't give you the governance steps. I run a price census of AI
> tools, and it measures what happens before an agent is orphaned: whether anyone has to approve
> buying one.
>
> As of 2026-11-03, of the 105 AI tools we track, 44 publish a monthly per-seat price; 35 of those
> sit at or under $25, median $16.50. Agent and automation platforms sit in the same band — Make's
> first paid tier is $12/month, n8n's is €20/month billed annually (both checked 2026-10-01) — which
> is low enough for one team to stand an agent up on a card without a procurement review, and a
> procurement review is usually where an owner gets named.
>
> If that works as your "how do they get created" paragraph, take it. If you need a practitioner
> instead, I'd rather you had one.
>
> Every figure carries its vendor URL and check date.
>
> AIToolsEssentials

*Word count: 158 including the signature — measured on this file, subject line excluded.*

---

## 3. Business Today — workplace AI adoption and the skills to use the tools ◀ 6d, LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **6 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge "Posted in last 7 days", not in today's feed (which now
turns over in under a day; see the last run's note).
**Who:** **Vidhya Das**, Business Today (India Today group); her author page
`businesstoday.in/author/vidhya-das` **HTTP 200**, title *"Trainee Sub Editor"*.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI)
in the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI
experts, enterprise AI trainers, researchers and technology professionals"*.

**The honest fit.** We are not a trainer and not an enterprise researcher; the draft says so. What we
hold is the procurement half of her story: what a seat costs, which is why adoption outruns training.

**Reply route:** **LinkedIn DM to `linkedin.com/in/vidya-das`** — **automatable? No.**
- The body redacts the email (*"You can also email me at [email redacted]"*) and offers *"comment
  below or DM me on LinkedIn"*. The handle was resolved through search on 2026-10-29, not off the
  request page; **LinkedIn answers HTTP 999 to this monitor's probe**, so check the profile matches
  her face and masthead before sending. This is the weakest route of the three, which is why it is
  third.

**Subject (a DM has none — the first line does the work):**

> Hi Vidhya — I can't answer as a trainer, so I won't pitch myself as one. I run a dated price census
> of AI tools, which covers the part of your story that sits under the training question: what a seat
> costs, and therefore why adoption outruns it.
>
> As of 2026-11-03: of the 105 AI tools we track, 44 publish a monthly per-seat price. 35 of those
> start at or under $25, and the median cheapest paid tier is $16.50 — cheap enough that an employee
> can adopt a tool without asking anyone. Annual billing barely helps: across 19 same-tier pairs,
> monthly costs 1.11x to 2.53x the annual rate, median 1.25x (re-asserted 2026-10-16).
>
> If your story is about the skills gap, that is the number that explains why the gap exists: the
> spending decision is small enough to stay invisible to whoever owns the training budget.
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 163 including the signature — measured on this file, subject line excluded.*

---

## Send late or close — do not redraft

- **Business Insider / Thibault Spirlet** (`employees-at-european-orgs-switch-from-us-ai-provider-to-mistral`,
  **11 days**, crossed cold today). Route re-probed live today (`businessinsider.com/author/thibault-spirlet`,
  HTTP 200, 328,608 bytes, `tspirlet@businessinsider.com`). Its 193-word draft stands unchanged in
  `pitch-drafts-2026-10-29.md` §2. Send it late or put a `skipped` entry in `pitch-ledger.json` —
  this run will not rewrite it again.
- **Fast Company / Tobi Amure** (**24 days**, now crossed). Draft at `pitch-drafts-2026-10-28.md` §3,
  route `hello@tobiamure.com` re-probed today (HTTP 200, 63,370 bytes).
- **WSJ / Christopher Mims** (**29 days**). Draft at `pitch-drafts-2026-10-27.md` §3, LinkedIn DM to
  `linkedin.com/in/christopher-mims-club/` (HTTP 200 today, 629,178 bytes).

## The 21 new rows that are not drafted, and why

Twenty of the 22 new rows ask for first-person testimony, institutional standing, or a campus and
industry affiliation we do not have, and 17 of those publish no usable route at all. Two publish an
address and still fail: **Suzanne Reilley / Business Insider** (`midlife-professionals-career-regret`,
4d) prints *suzanne [dot] reilley @ gmail [dot] com* in its own body but only wants personal stories
(career regret, AI burnout, an IPO aftermath) — a route without an ask we can answer; and
**CNBC / Lindsay Dodgson** (`uk-recruiters-…`, 1d) wants UK recruitment agencies and redacts its
address.

Two are not source requests at all — a Web Summit networking post and a PR contractor recruiting
vendor case studies for a hotel platform — and two are the reverse direction: **MIT Technology
Review** buying freelance features on an Automation theme, and a LinkedIn Live host booking 2027
guests. Four more are student or campus projects that exclude us by their own terms (The Charlatan,
Daily Texan, UCLA majors, a law-review note). The rest are industry-specific calls with no route:
multifamily property AI adoption, robotics world models, UK chatbot-crime law, design systems,
Canadian AI policy, and a Reddit agent-churn request that is a beat signal rather than a candidate.

---

## Still true, and the reason this file exists

Every run since 2026-10-10 has ended with drafts and zero sends; the send count has sat at six since
that date. Two emails today close three live requests: §1 closes two Forbes calls at a published
address, §2 closes a deadline that expires tomorrow. Re-drafting is not on that list.
