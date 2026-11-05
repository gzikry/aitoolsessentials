# Pitch drafts — 2026-11-05

**Nothing here has been sent. This run sent nothing — every route is an email or a DM, all George's
lane.** 248 tracked requests, **48 live unpitched, 3 sendable** (`pitch-queue.md`, built 2026-11-05),
43 of them expired on the platform.
Sends still stand at six ledger entries (five delivered, one bounced).

**Today's news is an expiry, and it changes the rules.** Sourcee removed **44 requests** that our
2026-11-03 digest re-verified live: each now answers **HTTP 404** and each has been **deleted from the
sitemap** (0 of 44 still listed). Two more died *between* today's sitemap pull and the verification
pass. This is the **first expiry this monitor has ever observed** on this source — every prior digest
recorded that no page carried an expiry, and treated a past-the-line row as "late, not dead." That is
now falsified. The queue's cold-line wording has been retired with the digest, and the practical
effect is simple: **a live row is worth sending today, and a "send it late" row is worth assuming it
may already be gone.** Among our own drafts, the Business Insider Mistral row (Thibault Spirlet) is
one of the 44 and is now dead — the decision that sat on it for eight days has been made by the
platform.

**What is actually sendable today (3 rows, 2 drafts):**

1. **Forbes / Alison Coleman — 9 days, EMAIL, ONE DAY LEFT inside the 10-day line.** One email closes
   **both** of her open calls. This is the only row in the queue with a published address that has
   been re-verified on the writer's own live page every run since 2026-10-28. Drafted as §1.
2. **Business Today / Vidhya Das — 8 days, LINKEDIN DM.** The best on-beat row for our core subject
   (workplace AI adoption) and the weakest route: the handle is search-resolved, because the body
   redacts the address. Drafted as §2.

Both rows cross the 10-day line **tomorrow**. Nothing in the 16 new rows is draftable: **0 ask about
AI tool costs** (the second consecutive run at zero AI+spend), **6 of the 16 publish no reply route at
all**, and the 10 that publish something — three Signal handles, two lnkd.in links, a bit.ly
evidence-submission page, a Tally survey, one "DM me" and one obfuscated magazine address — all want
testimony, regulatory evidence or an audience we are not in, not a price census.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **105 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-05`) yields **44 with a published monthly per-seat
price, 35 of those at or under $25/month, median $16.50**. Monthly vs annual: **1.11x to 2.53x,
median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted 2026-10-16). Superseded,
do not reuse: every 99-tool / $17.50 draft before 2026-11-03, and the `1.21x–2.53x` pair claim sent to
Jan Suski on 2026-09-18.

**Mailbox: zero replies**, measured today with `jansuski.com` as a positive control that returned its
two known messages (234, 305) before the sweep — so the zero is a fact, not a broken query. No reply
to any pitch since 2026-10-11. The one DSN in the inbox (msg 241, 2026-11-03) is a vendor-outreach
bounce to `info@krisp.ai`, not a pitch.

---

## 1. Forbes — US solopreneurs and bootstrapped founders ◀ 9d, EMAIL, CROSSES THE LINE TOMORROW

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted 2026-10-27 12:50Z, seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **9 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, no expiry notice — but see the expiry note above: this page has
survived two purge waves, which is luck, not a guarantee.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups;
page domain `forbes.com`.
**Ask, her words:** *"US #solopreneurs, genuinely one-person business that have used AI to eliminate
the need to hire, or simply change when and why the first hire happens."* The sibling call asks
founders who can *"quantify how AI has reduced the capital/headcount needed to build their company."*
**The honest fit:** not the testimony — we are a publisher with a price dataset, and the draft's
second line says so rather than implying standing. The quantified half is ours.

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email, but every
send in this queue is George's.
- Re-probed live today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,112 bytes**, address
  present once in visible body text beside a Contact Form 7 form (`route-checks-2026-11-05.json`);
  homepage `alisoncoleman.co.uk/` **HTTP 200, 21,396 bytes**.
- Dead end, do not retry: `forbes.com/sites/alisoncoleman/` answers **HTTP 403**; her own site is the
  only readable route.
- `alisoncoleman.co.uk` MX = Google Workspace. Deliverability is **not** SMTP-verified — a Google MX
  accepts at RCPT whatever the mailbox, so only a bounce proves anything.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> You asked US one-person businesses how AI changed when the first hire happens, and founders who
> can quantify what AI took out of the build. I can't answer from inside one, so I won't pretend to.
> I run a price census: what AI tools list at, read off each vendor's own pricing page, with the date
> of every check.
>
> As of 2026-11-05: of the 105 AI tools we track, 44 publish a monthly per-seat price; 35 of those
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

## 2. Business Today — workplace AI adoption and the skills to use the tools ◀ 8d, LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **8 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, not in today's AI-topic feed.
**Who:** **Vidhya Das**, Business Today (India Today group); her author page
`businesstoday.in/author/vidhya-das` **HTTP 200**, title *"Trainee Sub Editor"*.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI) in
the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI experts,
enterprise AI trainers, researchers and technology professionals"*.
**The honest fit:** we are not a trainer or an enterprise researcher; the draft says so in its first
line. What we hold is the procurement half of her story — what a seat costs, which is why adoption
outruns training.

**Reply route:** **LinkedIn DM to `linkedin.com/in/vidya-das`** — **automatable? No.**
- The body redacts the email (*"You can also email me at [email redacted]"*) and offers *"comment below
  or DM me on LinkedIn"*. The handle was resolved through search on 2026-10-29, not off the request
  page; **LinkedIn answers HTTP 999 to this monitor's probe**, so confirm the profile matches her face
  and masthead before sending. This is the weakest route in the queue and the reason §2 is second.

**Subject (a DM has none — the first line does the work):**

> Hi Vidhya — I can't answer as a trainer, so I won't pitch myself as one. I run a dated price census
> of AI tools, which covers the part of your story that sits under the training question: what a seat
> costs, and therefore why adoption outruns it.
>
> As of 2026-11-05: of the 105 AI tools we track, 44 publish a monthly per-seat price. 35 of those
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

## Closed by the platform, not by a decision

- **Business Insider / Thibault Spirlet** (`employees-at-european-orgs-switch-from-us-ai-provider-to-mistral`)
  — **HTTP 404 today, slug removed from the sitemap.** Drafted four times across seven runs, never
  sent. The row is dead; no ledger entry is needed to close it, but its staged draft was already
  deleted on 2026-11-03 for the stale-figure reason.
- **InformationWeek / Kelsey Ziser** (`cios-and-cisos-steps-to-address-ai-orphans`) — page still
  **HTTP 200** at 2 days, but its own deadline (*"Wednesday EOD"* = 2026-11-04) passed unsent. Moved to
  `skipped` in `pitch-ledger.json` today and Gmail draft uid 52 deleted rather than left clickable.

## Still open past the line — send late or record skipped

- **Fast Company / Tobi Amure** — `tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`, **26
  days**, page still HTTP 200 today. Route `hello@tobiamure.com` re-verified (tobiamure.com **HTTP
  200, 63,370 bytes**, address 6 times; /contact/ 18,505 bytes, 5 times). Draft in
  `pitch-drafts-2026-10-28.md` §3.
- **WSJ / Christopher Mims** — `employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **31 days**, page still HTTP 200. LinkedIn DM to `linkedin.com/in/christopher-mims-club/`
  (**HTTP 200**, 629,178 bytes). Draft in `pitch-drafts-2026-10-27.md` §3.
- **Raconteur / Simon Chandler** — **49 days**, page still HTTP 200. The address we hold
  (`simon.chandler@raconteur.net`) **bounced 550 on 2026-10-10**; `sb@raconteur.net` and
  `id@raconteur.net` answer 250 at RCPT. A send needs a route decision, not a redraft.

---

## The 16 new rows that are not drafted, and why

None asks what an AI tool costs — the second consecutive window at **0 AI+spend**. Recorded in full
in `digest-2026-11-05.json` (`relevance_notes` per row). The shape of them:

- **Testimony-only calls (the bulk of the 16), 6 of them with no route at all:** Anthropic employees
  (NYT, Signal only), UK job hunters, Ireland job-seekers using AI, retail workers (Bloomberg asks for
  *"personal stories, not product pitches"*, Signal only), designers on a podcast, AI data-centre
  operators (deadline story, already past, "DM me"), falsely-accused-of-AI-use freelancers (DMs open),
  biometrics experts (E&T), document-fraud experts (lnkd.in only), Dallas insurance executives (FT;
  "pricing" = insurance premiums), nurse-adoption founders (HLTH show floor).
- **Routed but unusable:** a beehiiv *State of Newsletters* respondent survey (Tally form — answering
  it would also mean answering for a platform we no longer use), a Real Estate Magazine call that
  prints `courtney(at)realestatemagazine(dot)ca` and wants Canadian agents, and a mental-wellbeing
  commission's evidence call (bit.ly submission, regulator-only).
- **Not source requests:** an NRF conference-preview post and a podcast episode invitation.
