# Pitch drafts — 2026-11-06

**Nothing here has been sent. This run sent nothing — every route is an email or a DM, all George's
lane.** 258 tracked requests, **54 live unpitched, 3 sendable** (`pitch-queue.md`, built 2026-11-06),
43 of them expired on the platform. Sends still stand at six ledger entries (five delivered, one
bounced).

**Today's headline is a deadline, not a find.** Both live sendable requests are at the end of the
10-day line: the two Forbes calls are **10 days old today and cross it tonight**, and Business Today
is **9 days old and crosses tomorrow**. One email to Alison Coleman closes two rows at once.

**The supply was the weakest of the week and it changes nothing.** The 53-slug window produced 6
AI-token slugs and **0 AI+spend** for the third consecutive run. All 10 new rows were read in full;
**not one asks what an AI tool, seat or subscription costs**, none publishes an email address (four
redact it, four publish only a `lnkd.in` shortlink, two publish nothing), and the two closest to our
beat fail on standing rather than route: The Stack wants security leaders on how they protect
developers from supply-chain compromise, and the Daily Mail wants an AI policy expert on a possible
US pause. We are a price census, not a CISO or a policy voice.

**No new expiry today — and that is a measurement, not an assumption.** The 44 requests that the
2026-11-05 digest recorded as 404 answered 404 again and remain absent from the sitemap. This run's
digest initially counted them a second time as a fresh wave of 44; the overlap is 44 of 44, so
`scripts/build_digest.py` now baselines "expired this run" against the previous digest's own page
verdict, and the queue's expiry note reads the inheritance rather than claiming a purge.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **105 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-06`) yields **44 with a published monthly per-seat
price, 35 of those at or under $25/month, median $16.50**. Monthly vs annual: **1.11x to 2.53x,
median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted 2026-10-16). Superseded,
do not reuse: every 99-tool / $17.50 draft written before 2026-11-03, and the `1.21x–2.53x` pair
claim sent to Jan Suski on 2026-09-18.

**Mailbox: zero replies**, measured today with `jansuski.com` as a positive control that returned
its two known messages (234, 305) before the sweep — so the zero is a fact, not a broken query. No
reply to any pitch since 2026-10-11.

---

## 1. Forbes — US solopreneurs and bootstrapped founders ◀ 10d, EMAIL, LAST DAY INSIDE THE LINE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted 2026-10-27 12:50Z, seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **10 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge *"Posted 10 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups;
page domain `forbes.com`.
**Ask, her words:** *"US #solopreneurs, genuinely one-person business that have used AI to eliminate
the need to hire, or simply change when and why the first hire happens."* The sibling call asks
founders who can *"quantify how AI has reduced the capital/headcount needed to build their company."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email, but every
send in this queue is George's.
- Re-probed live today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,113 bytes**,
  address present in visible body text beside a Contact Form 7 form (`route-checks-2026-11-06.json`);
  homepage `alisoncoleman.co.uk/` **HTTP 200, 21,366 bytes**.
- Dead end, do not retry: `forbes.com/sites/alisoncoleman/` answers **HTTP 403**; her own site is the
  only readable route.
- `alisoncoleman.co.uk` MX = Google Workspace. Deliverability is **not** SMTP-verified — a Google MX
  accepts at RCPT whatever the mailbox, so only a bounce proves anything.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> You asked US one-person businesses how AI changed when the first hire happens, and founders who
> can quantify what AI took out of the build. I can't answer from inside either, so I won't pretend
> to.
>
> I run a price census: what AI tools list at, read off each vendor's own pricing page, with the date
> of every check.
>
> As of 2026-11-06: of the 105 AI tools we track, 44 publish a monthly per-seat price; 35 of those
> sit at or under $25, and the median cheapest paid tier is $16.50. Five seats on that median cost
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

## 2. Business Today — workplace AI adoption and the skills to use the tools ◀ 9d, LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **9 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge *"Posted 9 days ago"*, not in today's AI-topic feed.
**Who:** **Vidhya Das**, Business Today (India Today group); her author page
`businesstoday.in/author/vidhya-das` **HTTP 200**, title *"Trainee Sub Editor"*.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI) in
the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI experts,
enterprise AI trainers, researchers and technology professionals"*.

**Reply route:** **LinkedIn DM to `linkedin.com/in/vidya-das`** — **automatable? No.**
- The body redacts the email (*"You can also email me at [email redacted]"*) and offers *"comment below
  or DM me on LinkedIn"*. The handle was resolved through search on 2026-10-29, not off the request
  page; **LinkedIn answers HTTP 999 to this monitor's probe**, so confirm the profile matches her face
  and masthead before sending. Weakest route in the queue and the reason §2 is second.

**Subject (a DM has none — the first line does the work):**

> Hi Vidhya — I can't answer as a trainer, so I won't pitch myself as one. I run a dated price census
> of AI tools, which covers the part of your story that sits under the training question: what a seat
> costs, and therefore why adoption outruns it.
>
> As of 2026-11-06: of the 105 AI tools we track, 44 publish a monthly per-seat price. 35 of those
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

## Why there is no third draft today

Ten new rows, none drafted. Not one asks what an AI tool costs, and none carries an email address:

- **Closest to the beat, wrong ask:** `cisos-and-senior-cybersecurity-leaders-protecting-developers`
  (The Stack, 1d) opens on a developer compromised while installing *"a popular AI coding tool"* and
  then asks security leaders how they protect developers upstream — a dated price census does not
  answer it. `ai-policy-expert-possible-pause-on-ai-in-us` (Daily Mail, 1d) wants an AI policy expert;
  we have no policy standing.
- **Testimony only:** CNBC Make It on friends and coworkers who disagree about AI (0d); The Future
  Collective / Henley Business School on early-career work (1d); a doctoral-writing call (1d).
- **Debate slots needing a named individual with a headshot:** two Business Spotlight (ZEIT SPRACHEN)
  Head-to-Head calls — banning AI datacentre expansion until safety rules land (1d), and handwriting
  in business (1d). Both publish only a `lnkd.in` shortlink.
- **Deadline already open:** REALTOR Magazine's NAR NXT call (1d) needs people on the New Orleans
  floor between 2026-11-06 and 11-08.
- **Not a source request:** an AI/virtual-influencer index submission (1d).

## Still open past the line — send late or record skipped

- **Fast Company / Tobi Amure** — `tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`, **27
  days**, page still HTTP 200. Route `hello@tobiamure.com` re-verified today (tobiamure.com **HTTP
  200, 63,370 bytes**; /contact/ **18,505 bytes**). Draft in `pitch-drafts-2026-10-28.md` §3.
- **WSJ / Christopher Mims** — `employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **32 days**, page still HTTP 200. LinkedIn DM to `linkedin.com/in/christopher-mims-club/`
  (**HTTP 200**, 621,250 bytes). Draft in `pitch-drafts-2026-10-27.md` §3.
- **Raconteur / Simon Chandler** — **50 days**, page still HTTP 200. The address we hold
  (`simon.chandler@raconteur.net`) **bounced 550 on 2026-10-10**; `sb@raconteur.net` and
  `id@raconteur.net` answer 250 at RCPT. A send needs a route decision, not a redraft.

## What is already staged in Gmail

**uid 53** — the Forbes email to `alison@alisoncoleman.co.uk`, staged 2026-11-05. Its body says *"As of
2026-11-05"*, so **it must be replaced with §1 above before it is sent**; the figures are unchanged
(105 / 44 / 35 / $16.50) but the check date in the letter would be a day wrong. Business Today is a
LinkedIn DM and cannot be staged.
