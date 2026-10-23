# Pitch drafts — 2026-10-23

**Nothing here has been sent. This run sent nothing.** 179 tracked requests, **58 live unpitched, 0 sendable**
(`pitch-queue.md`, built 2026-10-23). The ledger still records six `pitched` entries: five delivered, one bounced.

**Two drafts. Both are for live pages with live routes. Both are past this monitor's own 10-day line,
which is a heuristic, not the platform's — neither page carries an expiry and both routes answered
HTTP 200 today.** A late send or a ledger entry closes each one. Two identical files have now been
written on consecutive days with no send in between; if neither goes out, record them as `skipped` and
stop redrafting them.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **91 tools**;
`data/pricing_snapshots.json` (`updated: 2026-10-23`) yields **44 with a published monthly price, 35 of
those at or under $25/month, median $17.50**. Monthly vs annual: **1.11x to 2.53x, median 1.25x over 19
tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16). Per-tool pairs carry their own snapshot
dates (all 2026-09-18 except Replit 2026-09-21).
**Superseded — do not reuse:** the 2026-10-22 file's "Gamma Pro is $18/seat/month-equivalent on either
term". Gamma's own snapshot (2026-10-01) now reads plus $9/seat/month-equivalent vs $108/seat billed
annually, i.e. no monthly penalty on that tier, so the claim has been cut from both drafts rather than
restated.

---

## 1. Fast Company Work Life — AI at work, jobs and hiring ◀ 13d, LATE SEND — EMAIL, paste-ready

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **13 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-10T13:51:49Z`, badge "Posted 13 days ago", no expiry notice. Not in the newest
AI-topic feed (a 50-slot recency window), which is why it reads colder than its age.
**Who:** **Tobi Amure** — the page's own author field; sourcing for **Fast Company's Work Life** section.
**Ask, his words:** *"For experts: the credential and the research behind it. Original data, or a survey
with its sample size and method. Workplace expert is not a credential."* He is *"not placing bylined
guest posts"* — so this offers a dataset, never a post.
**The door:** *"No DM pitches here on LinkedIn. Email me."*

**Reply route:** **hello@tobiamure.com** — self-published on his own site. Re-probed today:
https://tobiamure.com/ **HTTP 200, 62,685 bytes**, address present; fallback https://tobiamure.com/contact/
**HTTP 200, 17,777 bytes** with a form.
**Deliverability is not SMTP-verified.** `tobiamure.com` MX is Namecheap forwarding and answers
554 5.7.1 Relay access denied for `hello@`, a fake control and `postmaster@` alike, so the probe
discriminates nothing. Self-publication on his live site is the evidence; a bounce is itself the answer.
**Automatable? No** — sends are George's lane. One draft is now staged in Gmail Drafts (see "Staged" below).

**Subject:** `The $17.50 median: method and denominator first`

> Hi Tobi —
>
> Method first, since that is the bar you set. This is not a survey: it is a census of published list prices. We hand-check the pricing page of 91 AI tools and store the date of every check.
>
> As of today, 2026-10-23, 44 of those 91 publish a monthly per-seat price. 35 of the 44 start at or under $25/month, and the median cheapest paid tier is $17.50.
>
> The same set answers the annual-discount question. Paying monthly instead of yearly costs between 1.11x and 2.53x, median 1.25x across 19 tiers, pair set re-asserted 2026-10-16. Two rows with their check dates: Browse AI Personal is $48/month or $19/month billed annually, 2.53x (browse.ai/pricing, checked 2026-09-18); Otter.ai Pro is $16.99/month or $8.33/month billed annually, 2.04x (otter.ai/pricing, checked 2026-09-18).
>
> For your AI-at-work lane that is the personal-economics half: what a seat costs the individual, and how often it comes out of their own pocket.
>
> You asked for the credential too. I do not have one to offer; I have a dated dataset, its method, and the source URL behind every number, free to use.
>
> AIToolsEssentials

*Word count: 184 including the signature — measured on this file with a script, not asserted.*

---

## 2. WSJ blocked work accounts — what the workaround buyer pays ◀ 18d, LATE SEND — LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **18 days.** Page re-read today: HTTP 200, body served, no expiry.
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist.
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.

**Honesty constraint — do not edit out.** The request wants the respondent's own annoyance. We are a
publisher, not a blocked employee. The draft says so in its first sentence.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-probed today:
**HTTP 200, 624,065 bytes**, title "Christopher Mims - The Wall Street Journal | LinkedIn". The request's
own body says "(DMs open)".
**Automatable? No.** No address, no form, no booking link; the text below is the whole message and must go
from George's own LinkedIn.
Dead ends recorded so they are not retried: `muckrack.com/christopher-mims` HTTP 403,
`wsj.com/news/author/christopher-mims` HTTP 401.

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 91 AI tools. 44 publish a monthly price and 35 of those start at or under $25/month — median $17.50, checked today (2026-10-23).
>
> That is what the people who route around a blocked work account pay. Browse AI is $48/month against $19/month billed annually (2.53x, checked 2026-09-18); Otter.ai Pro is $16.99 against $8.33 (2.04x, same date). Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Word count: 125 including the signature — measured on this file with a script, not asserted.*

---

## Staged for send

**One email draft is sitting in Gmail Drafts** (`[Gmail]/Drafts`, account `aitools`) addressed to
hello@tobiamure.com, subject as above, body as above, signed AIToolsEssentials. It was placed there with
`himalaya message save`, which writes a draft — it does **not** send, and the monitor cannot send. Open
Drafts, read it once, press send. If you would rather not send, delete it and record
`tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring` as `skipped` in `pitch-ledger.json`.

The WSJ row cannot be staged anywhere: it is a LinkedIn DM, so the text above is the entire artifact.

## Why there is no third draft

Today's window was 93 slugs; 6 carried an AI token, **0 carried an AI token plus a real spend token**,
and all 93 bodies were read (8 body-level AI hits, 0 with spend). The 8 rows added this run are all
off-beat, and each is recorded with its reasoning in `digest-2026-10-23.json`:

- `claude-users-anthropic-public-benefit-fund-trust-and-job-impact` (Ryan Moeller, 0d, low-medium) — the
  only adjacent one. Anthropic's Public Benefit Fund is a value-distribution story and our dated Claude
  prices would be a real data point, but the ask is for Claude users' personal takes ("the best stories
  and hottest takes get featured next week"), and it publishes no route. Not ours to answer.
- `fanvue-chatters-nsfw-ai-model-experiences` (Dazed), `couples-letting-ai-dictate-relationship-emotions-and-intimacy`
  (The Sun), `students-and-professionals-balancing-ai-use-and-human-focus`, `parish-event-organizers-...`,
  `rig-hse-officers-...`, `founders-and-ctos-production-ai-tradeoffs-...` (bry.net podcast) — all want
  first-hand testimony from a role we do not hold, all with no published route.
- `people-recreating-iconic-runway-looks-halloween-costume-story` — **a fashion runway, not the AI tool.**
  Recorded as a false positive so the count stays honest; `scripts/sourcee_terms.py` now requires a model
  suffix (Gen-N / ML / AI) before "runway" scores as an AI hit in prose.

The 58 live rows in `pitch-queue.md` are the same shape: every one is relevance `low` (one is
`low-medium`) and none has a resolved route. Nothing there can be drafted without claiming standing we
do not have.
