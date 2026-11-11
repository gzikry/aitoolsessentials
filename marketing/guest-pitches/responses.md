# Guest pitch responses — 2026-09-03 batch (+ 2026-09-22, 2026-10-13, 2026-10-20 and 2026-11-03 additions)

Tracking file for the pitches in `pitches-2026-11-10.json` (12 drafts, supersedes the 12 in
`pitches-2026-11-03.json`, the 12 in `pitches-2026-10-20.json`, the 12 in `pitches-2026-10-13.json`,
the 12 in `pitches-2026-09-22.json` and the 10 in `pitches-2026-09-03.json` — never send from a
superseded file).
**Created:** 2026-09-15 · **Re-verified:** 2026-11-10 (cron reminder run). Still **0 sends** from the
Sep-22, Oct-13, Oct-20, Nov-03 and Nov-10 batches; Sent folder confirms the last pitch mail of any kind
is the 2026-10-08 ToolChase reply (newest outbound IDs 396–402 are vendor submission mail, 11-08/11-10).

Status legend: `NOT SENT` · `SENT` · `AWAITING` · `REPLIED` · `NO RESPONSE` · `CLOSED`

| # | Outlet | Type | Contact | Priority | Sent | Follow-up | Response | Outcome |
|---|---|---|---|---|---|---|---|---|
| 1 | The Decoder | blog | hello@the-decoder.com ✅ published "Contact us", live MX | 1 | — | — | — | NOT SENT — fresh route |
| 2 | Latent Space | podcast | tips@latent.space ✅ published "News tips and pitches", live MX | 2 | — | — | — | NOT SENT — fresh route |
| 3 | Ben's Bites | newsletter | team@bensbites.com ✅ live MX | 3 | — | — | — | NOT SENT — needs NEW angle (pitched Sep 3) |
| 4 | infoDOCKET | blog | gprice@gmail.com ✅ named editor (Gary Price, Library Journal) | 4 | — | — | — | NOT SENT |
| 5 | The Rundown AI | newsletter | support@therundown.ai ✅ live MX | 5 | — | — | — | NOT SENT — needs NEW angle (pitched Sep 3) |
| 6 | Changelog / Practical AI | podcast | editors@changelog.com ✅ verified contact page | 6 | — | — | — | NOT SENT — pitched Sep 3 |
| 7 | TLDR AI | newsletter | dan@tldr.tech ⚠️ no contact route published — address is a guess | 7 | — | — | — | NOT SENT — do not send to a guessed address |
| 8 | The Neuron | newsletter | team@theneurondaily.com ⚠️ domain resolves again (see below) | 8 | — | — | — | NOT SENT — pitched Sep 3 |
| 9 | Last Week in AI | podcast | contact@lastweekinai.com ✅ live MX (PrivateEmail) | 9 | — | — | — | NOT SENT |
| 10 | ToolChase | blog | hello@toolchase.com ✅ live MX (smtp.google.com) | 10 | 2026-09-03 | — | 2026-10-08 | REPLIED (Emre) — polite acknowledgement, **no rate card, no placement ask**; our reply corrected the pitch's stale "74 tools" figure to 76 |
| 11 | AIToolsRecap | blog | editor@aitoolsrecap.com ⚠️ "paid review" / sponsored on site | 11 | — | — | — | NOT SENT |
| 12 | ToolRadar | blog | contact@aitoolradar.io ⚠️ "Submit Tool" / sponsored on site | 12 | — | — | — | NOT SENT |

## 2026-10-13 — the Cursor figure in every blog draft went stale, and the news hook went up

Cursor's pricing page stopped rendering the standalone ladder. On 2026-10-12 Cursor shipped inside
**The X Subscription**, a bundle of Cursor, Grok and X Premium:

| The X Subscription | Monthly | Annual |
|---|---|---|
| Free | $0 | $0 |
| Plus | $8/mo | $80/yr ($7/mo) |
| Premium | $30/mo | $300/yr ($25/mo) |
| Super | $100/mo | $1,000/yr ($84/mo) |
| Ultra | $200/mo | $2,000/yr ($167/mo) |

Team seats are Premium $30, Super $100 and Ultra $200 per seat. Verified 2026-10-13 from the
vendor's own pages: `cursor.com/pricing` (rendered ladder) and `docs.x.ai/x-subscription/pricing`
(the price list and the team-seat line). xAI's docs are explicit that **existing Cursor, SuperGrok
and X Premium plans continue and switching is optional**, so nobody is repriced — but the standalone
Pro $20 / Pro Plus $60 / Teams $40 tiers are no longer on the page.

What that broke, and what was done about it:

- `data/tool_sources.json` — cursor row re-checked 2026-10-13 with the new ladder; the retired digest
  is preserved in the row's notes rather than deleted. The grok row notes the same unification.
- `/pricing-watch/` — Cursor row and public change log updated, **live-verified at
  https://aitoolsessentials.com/pricing-watch/** (row now reads 2026-10-13; the retired
  "Pro $20/mo, Pro Plus $60/mo" string is gone). Patched in place on purpose: running
  `generate_pricing_watch.py` alone strips the site-wide structured data, discovery links and share
  row, which only `daily_content_update.py` re-injects.
- `scripts/guest_pitch_builder.py` — `verified_overlap_line()` asserted "Cursor Pro is $20/mo". That
  price no longer exists and it was the only concrete claim in the blog drafts. It now cites only
  figures stamped on our own page. Fresh batch: **`pitches-2026-10-13.json` (12 drafts, 77 tools)**.
  Superseded: `pitches-2026-09-03.json`, `pitches-2026-09-22.json` — do not send from them.
- `admin/newsletter/2026-w42-draft.html` (today's issue, not yet sent — sending is held)
  carries "Cursor (18 Sep 2026): Pro $20, Pro Plus $60, Ultra $200, Teams $40 a user". That line is
  now false. Flagged here, not edited: it is another lane's draft and the fix is a re-sync from
  sources, not a hand-edit.

Blocker status: **none.** Freshness after the fix (2026-10-13): **41 FRESH · 22 UNREADABLE ·
10 NO_CLAIM · 2 DRIFTED · 2 UNVERIFIED** — `cursor` and `claude` both **FRESH 4/4**. The two
remaining DRIFTED rows (`aidetector-cx`, `instrumentl`) appear in no draft.

## Send plan for the week of 2026-11-10 (2-3 sends)

**68 days since the last pitch mail of any kind (2026-09-03 batch), 7 days since the Nov-03 plan,
still 0 sends from every batch since Sep 22.** Sent folder re-checked today: newest outbound is vendor
submission mail (IDs 396–402, 11-08/11-10); the only pitch mail on record is still the 2026-10-08
ToolChase reply. Inbox has no outlet replies since then (only tool submissions and vendor threads).

**The Nov-03 drafts went stale on the tool count.** `data/tools.json` is now at **108 tools**, not the
105 baked into `pitches-2026-11-03.json` — the one sentence an editor can check in ten seconds.
Regenerated as **`pitches-2026-11-10.json` (12 drafts, 108 tools)**; the derived checked dates still
resolve correctly (`cursor` 2026-11-03, `claude` 2026-09-18). `pitches-2026-11-03.json` and everything
older is superseded — do not send from it.

**On the reminder's "start with newsletters" advice:** true of newsletters in general, false of this
list. The Sep-3 newsletter sends went **0/5**; of the four newsletter rows, one address is a guess
(`dan@tldr.tech`), one is a general support inbox (`support@therundown.ai`), and two were already
pitched on Sep 3. One viable newsletter send exists — Ben's Bites with a changed opening.

1. **The Decoder** — `hello@the-decoder.com`, blog, **first touch.** Best odds on the list: real
   editorial address from their own `/about`, MX live, never contacted. *Keep the drafted first line:*
   "I've been following The Decoder — how clearly you mark sponsored posts and keep them separate from
   editorial." Draft's concrete claim is the X Subscription ladder, re-derived from the 2026-11-03 check.
2. **Latent Space** — `tips@latent.space`, podcast, **first touch.** `tips@` is the address the show
   publishes for pitches (`business@` is the sponsorship inbox). The ask is an interview walkthrough.
   *Add:* "Your AI-engineer audience is the one group that actually has to choose between overlapping
   coding subscriptions, so this may land better here than with a general AI newsletter."
3. **Ben's Bites** — `team@bensbites.com`, newsletter, **second touch, new angle required.** The draft
   is still verbatim the Sep-3 resource pitch that drew no reply — do not send it as written. Replace
   the first two paragraphs with the repricing lead:
   > Hi Ben's Bites team,
   >
   > Not a re-pitch — Cursor stopped selling standalone seats on 12 Oct and now sits on an X
   > Subscription ladder that also carries Grok and X Premium (cursor.com/pricing, re-checked
   > 2026-11-03). We track 108 AI tools with dated pricing evidence, and the overlap math is what
   > changed: a coding seat plus a frontier chat seat is now the most expensive stack to double up on.
   >
   > If a short "what the repricing actually costs you" item fits a future issue, the dated table is
   > here: https://aitoolsessentials.com/pricing-watch/ — every row carries its own checked date.

**Skip this week:** TLDR AI (guessed address), The Rundown AI (support inbox), The Neuron (already
pitched; live newsletter on theneuron.ai), ToolRadar and AIToolsRecap (monetized placement desks),
Changelog and Last Week in AI (lower fit than the three above), infoDOCKET (`gprice@gmail.com` is a
personal Gmail — low-yield unless Gary is actively soliciting).

**Fallback if all three cold routes feel like too much:** send #1 and #3 only. Two sends beats a
fifth consecutive week of zero.

## Send plan for the week of 2026-11-03 (2-3 sends) — historical

**40 days since the last pitch mail of any kind (2026-09-03 batch), 14 days since the Oct-20 batch was
written, still 0 sends from the Sep-22, Oct-13 and Oct-20 batches.** Sent folder re-checked 2026-11-03:
most recent outbound is vendor/submission mail (IDs 378–392, all 2026-11-02/03), and the only pitch
mail on record is the 2026-10-08 ToolChase reply. Nothing on the site is blocking a send.

**The Oct-20 drafts went stale in the one sentence an editor can check.** `data/tools.json` is now at
**105 tools**, not the 80 baked into `pitches-2026-10-20.json`; `cursor` was also re-verified today
(2026-11-03), so "on our 2026-10-13 check" would have shipped a two-week-old date. Regenerated as
**`pitches-2026-11-03.json` (12 drafts, 105 tools, live checked dates)** — `pitches-2026-10-20.json` and
everything older is superseded, do not send from it.

**Do not default to newsletters on this list.** The reminder's standing advice ("start with
newsletters, highest response rate") is true of newsletters generally and false here: the Sep-3
newsletter sends went **0/5**, and of the four newsletter rows on the list one address is a guess
(`dan@tldr.tech`), one is a general support inbox (`support@therundown.ai`), and the remaining two were
already pitched on Sep 3. One viable newsletter send exists — with a changed opening, not the resource
re-pitch.

1. **The Decoder** — `hello@the-decoder.com`, blog, **first touch.** The best odds on the list: a real
   editorial address from their own `/about` (Deep Content GmbH imprint), MX live (checked 2026-11-03),
   never contacted. The draft's one concrete claim is the X Subscription ladder, re-verified today.
   *Keep the drafted first line:* "I've been following The Decoder — how clearly you mark sponsored
   posts and keep them separate from editorial."
2. **Latent Space** — `tips@latent.space`, podcast, **first touch.** `tips@` is the address the show
   publishes for pitches (`business@` is the sponsorship inbox); MX live. The ask is an interview
   walkthrough, not a placement.
   *Add:* "Your AI-engineer audience is the one group that actually has to choose between overlapping
   coding subscriptions, so this may land better here than with a general AI newsletter."
3. **Ben's Bites** — `team@bensbites.com`, newsletter, **second touch, new angle required.** The Oct-20
   draft is still verbatim the Sep-3 resource pitch that drew no reply — do not send it as written.
   Replace the first two paragraphs with the repricing lead:
   > Hi Ben's Bites team,
   >
   > Not a re-pitch — Cursor stopped selling standalone seats on 12 Oct and now sits on an X
   > Subscription ladder that also carries Grok and X Premium (cursor.com/pricing, re-checked today).
   > We track 105 AI tools with dated pricing evidence, and the overlap math is what changed: a coding
   > seat plus a frontier chat seat is now the most expensive stack to double up on.
   >
   > If a short "what the repricing actually costs you" item fits a future issue, the dated table is
   > here: https://aitoolsessentials.com/pricing-watch/ — every row carries its own checked date.

**Skip this week:** TLDR AI (guessed address), The Rundown AI (support inbox), The Neuron (already
pitched, live newsletter moved to theneuron.ai), ToolRadar and AIToolsRecap (monetized placement desks),
Changelog and Last Week in AI (lower fit than the three above), infoDOCKET (`gprice@gmail.com` is a
personal Gmail — low-yield unless Gary is actively soliciting).

**Fallback if all three cold routes feel like too much:** send #1 and #3 only. Two sends beats a
fourth week of zero.

## Send plan for the week of 2026-10-20 (2-3 sends) — historical

**28 days, 0 sends.** The Oct-13 plan was never executed — the Sent folder shows only vendor
submission replies from 10-13 to 10-20. Nothing is blocking the route; the drafts just didn't go out.

The reminder that generated this entry said "start with newsletters — highest response rate."
That is true of newsletters in general and false of *this* list: the Sep-3 newsletter sends went
**0/5** (the batch's only reply was a blog, ToolChase), three of the five newsletter addresses are
unsendable (`dan@tldr.tech` guessed, `support@therundown.ai` a support inbox, `editor@`/`contact@`
placement desks are separate rows), and the other two were already pitched. So the picks below are
the two **uncontacted editorial routes** plus one warm follow-up.

1. **The Decoder** — `hello@the-decoder.com`, blog, **first touch.** Best odds on the list: a real
   editorial address verified from their own `/about`, no prior send, and the draft's one concrete
   claim (the X Subscription ladder, checked 2026-10-13) is still what `cursor.com/pricing` renders.
   *Keep the drafted first line:* "I've been following The Decoder — how clearly you mark sponsored
   posts and keep them separate from editorial."
2. **Latent Space** — `tips@latent.space`, podcast, **first touch.** `tips@` is the route the show
   publishes for pitches; `business@` is the sponsorship inbox. Guest format matches their interview
   show, and the ask is a walkthrough, not a placement.
   *Add the plan's first line:* "Your AI-engineer audience is the one group that actually has to
   choose between overlapping coding subscriptions, so this may land better here than with a general
   AI newsletter."
3. **ToolChase** — `hello@toolchase.com`, **warm follow-up, not a fresh pitch.** Emre acknowledged on
   2026-10-08 and we already replied. Send three sentences offering the bundle breakdown; do not
   re-send the resource offer.
4. **Ben's Bites** (optional third send) — only with the plan's opening *replacing* the drafted one.
   The 2026-10-20 draft is still verbatim the Sep-3 resource pitch that drew no reply; paste the
   bundle line in as the first paragraph or skip the outlet this week.

**Do not send to:** `dan@tldr.tech` (guessed, no published editorial route), `support@therundown.ai`
(general support), `contact@aitoolradar.io` and `editor@aitoolsrecap.com` (monetized placement
desks), `team@theneurondaily.com` (already pitched; live newsletter is on `theneuron.ai`).

## Send plan for the week of 2026-10-13 (3 sends) — historical

Same three outlets as the Sep-22 plan, but **the first line is now the repricing, not the resource
offer**. A newsletter that ignores a Grok+Cursor+X bundle is the wrong audience for a pricing
tracker pitch.

1. **The Decoder** (`hello@the-decoder.com`) — blog, first touch. Draft in
   `pitches-2026-10-13.json`; its one concrete claim is the X Subscription ladder, checked today.
   *First line:* "I saw The Decoder is running the ChatGPT-pricing coverage under your own byline
   rather than sponsored placements — that's the reason I'm writing to you and not to a placement desk."
2. **Latent Space** (`tips@latent.space`) — podcast, first touch. Editorial route only; `business@`
   is the sponsorship inbox.
   *First line:* "Your AI-engineer audience is the one group that actually has to choose between
   overlapping coding subscriptions, so this may land better here than with a general AI newsletter."
3. **Ben's Bites** (`team@bensbites.com`) — newsletter, **changed angle required.** Lead with the
   bundle, not with "here is our resource again."
   *First line:* "Cursor stopped selling standalone seats on 12 Oct — it now sits on an X
   Subscription ladder that also carries Grok and X Premium. We re-checked every price on it today
   and the overlap math changes for anyone stacking an editor seat next to a chat seat."

Optional swap: **ToolChase** (`hello@toolchase.com`) replied 2026-10-08 and is the only warm address
on the list. A short follow-up offering the bundle breakdown is a cheaper send than a cold
newsletter re-pitch.

**Do not send to:** `dan@tldr.tech` (guessed address, no published editorial route),
`contact@aitoolradar.io` and `editor@aitoolsrecap.com` (monetized placement desks),
`support@therundown.ai` (general support inbox, not editorial).

## Send plan for the week of 2026-09-22 (3 sends) — historical

Newsletters do have the best response rate **in general**, but every newsletter address on
this list received the identical resource pitch on Sep 3 and drew 0/10 responses. A verbatim
second send is a follow-up, not a pitch — so the plan is **two fresh verified routes plus one
newsletter with a genuinely changed opening**.

1. **The Decoder** (`hello@the-decoder.com`) — blog, first touch, no prior relationship.
   *First line to use:* "I saw The Decoder is running the ChatGPT-pricing coverage under your
   own byline rather than sponsored placements — that's the reason I'm writing to you and not
   to a placement desk."
2. **Latent Space** (`tips@latent.space`) — podcast, first touch. This is the route the show
   publishes for pitches specifically; do not use `business@latent.space`, which is the
   sponsorship inbox.
   *First line to use:* "Your AI-engineer audience is the one group that actually has to
   choose between overlapping coding subscriptions, so this may land better here than with a
   general AI newsletter."
3. **Ben's Bites** (`team@bensbites.com`) — newsletter, **changed angle required.**
   *First line to use:* "Quick update rather than a re-pitch: we refreshed 39 of our 76 pricing
   snapshots on 2026-09-18, so the pricing table is materially different from the version I
   sent you in early September."

## Contact verification (re-checked 2026-09-22)

- **New, verified from the outlets' own pages:** `tips@latent.space` (Latent Space `/about`:
  "News tips and pitches") and `hello@the-decoder.com` (The Decoder `/about`: "Contact us —
  E-Mail", over the Deep Content GmbH imprint, Hannover DE). Both domains have live MX.
- **The Neuron: the 2026-09-15 "NXDOMAIN / hard bounce" finding is no longer true.**
  `theneurondaily.com` now resolves (A 104.21.7.74, MX `aspmx.l.google.com`) and answers HTTP
  403 behind Cloudflare. A mailbox exists again. It stays low priority for other reasons —
  already pitched, and the live newsletter is on `theneuron.ai`.
- **TLDR AI still publishes no editorial address.** `tldr.tech` links only to
  `https://advertise.tldr.tech/`. `dan@tldr.tech` is a guess and must not be sent to.
- **`support@therundown.ai`** appears on therundown.ai's own contact/advertise pages, but it is
  a general support inbox, not an editorial route.
- Live MX confirmed 2026-09-22 on: latent.space, the-decoder.com, therundown.ai, tldr.tech,
  bensbites.com, theneuron.ai, lastweekinai.com, changelog.com, infodocket.com, toolchase.com,
  aitoolradar.io, aitoolsrecap.com.

## Do not re-send blindly

An earlier resource pitch to `dan@tldr.tech`, `support@therundown.ai`, `team@bensbites.com`,
and `team@theneurondaily.com` went out around **Sep 3** and drew **0/10 responses** (see
`traffic/weekly-report-2026-09-07.md`). The Sep-14 report's finding applies here too: the
addresses that reply are monetized placement desks, not editors — ToolChase, ToolRadar, and
AIToolsRecap all advertise sponsored/paid-review placements on their homepages. Either change
the angle or skip those addresses.

## Content corrections

1. ~~**"We track 74 tools" is stale in all 10 drafts.**~~ **FIXED 2026-09-18** (commit
   `3bec7a04`). `scripts/guest_pitch_builder.py` derives the count from `data/tools.json`
   (`tracked_tool_count()`), so it cannot drift again. Drafts now read "We track 76 tools".
2. ~~**The blog-template bullets are unverified claims.**~~ **FIXED 2026-09-18** (same commit).
   The unsourced bullets are replaced by `verified_overlap_line()`, which cites only figures
   present in our own dated snapshots.
3. ~~**Signature.**~~ **FIXED 2026-09-18** (same commit). All templates close as
   AIToolsEssentials only; zero occurrences of a personal name.
4. **Greeting line — FIXED 2026-09-22.** The builder derived the greeting from the email
   local-part, producing "Hi support," and, on the two new targets, "Hi tips," and
   "Hi hello,". A `SALUTATIONS` map now renders "Hi Latent Space team," / "Hi The Decoder
   team," / "Hi Gary," (infoDOCKET only, where the contact is a named person).
5. ~~**Pricing Watch freshness — STALE, blocking issue for pitching the page.**~~ **CLEARED
   2026-10-06.** The public page no longer shows August as its headline: 34 rows now carry
   2026-10-01 stamps (39 carry 2026-09-18); the newest public date is 2026-10-01, versus
   2026-09-13 on 2026-09-29. Freshness re-run: **41 FRESH · 23 UNREADABLE · 9 NO_CLAIM ·
   2 UNVERIFIED · 1 DRIFTED** — the two figures the pitch copy cites (`cursor`, `claude`) are
   still **FRESH, 4/4 claims present**. Residual items, none of which block a send:
   `instrumentl` DRIFTED (a $349.0 claim left the page), `cocounsel` and `n8n` UNVERIFIED.
   Note the phrasing was already fixed in the builder on 2026-09-22 (item 1) — drafts now read
   "re-verify pricing against vendor official pages", i.e. **no "weekly" claim remains** in any
   draft, so the one-click-falsifiable sentence is gone from the copy regardless.

6. **Tool count drifted 77 → 80 in the week after the Oct-13 batch — regenerated 2026-10-20.**
   `pitches-2026-10-13.json` says "We track 77 tools"; `data/tools.json` now has 80 (BotLoadout,
   Robylon, HOL Registry and others published live in the interim). The builder already derives the
   number via `tracked_tool_count()`, so the fix is to **regenerate, not hand-edit**: 12 fresh drafts
   in `pitches-2026-10-20.json` now read 80. Treat any batch older than a few days as suspect on
   this line — it is the one sentence an editor can check in ten seconds.
7. **Blog greeting grammar — FIXED 2026-10-20.** The blog template rendered
   "I've been following {outlet} and appreciate {observation}." against observations that are
   already full clauses, producing "and appreciate your pricing verification methodology is solid"
   (ToolChase), "…your editorial independence stands out" (ToolRadar) and "…your directory
   comparison approach is valuable" (AIToolsRecap). Template now reads
   "I've been following {outlet} — {observation}." Also fixed the misspelled observation key
   (`infoDocket` → `infoDOCKET`), which had been silently falling back to a noun fragment
   ("infoDOCKET — the quality of your coverage."); the fallback is now a full clause.

8. **The overlap line's checked dates were hardcoded — FIXED 2026-11-03.** `verified_overlap_line()`
   printed "on our 2026-10-13 check" and "checked 2026-09-18" as literals. The daily run re-verified
   `cursor` on 2026-11-03, so every blog draft would have cited a 21-day-old check for a figure the site
   itself stamps as current — the same class of error as the hardcoded tool count (correction 6). The
   builder now calls `pricing_checked_date(slug, default)`, which reads `pricing_checked_date` from
   `data/tool_sources.json`. Any future re-check flows into the copy with no edit.

## Log

| Date | Action | Notes |
|---|---|---|
| 2026-09-15 | Tracking file created | 0 sends from this batch; contacts and draft claims verified |
| 2026-09-18 | Corrections 1–3 fixed in source | `guest_pitch_builder.py` + `haro-outreach/pitch-templates.md` (commit `3bec7a04`). No send. |
| 2026-09-22 | Re-verified + 2 fresh targets added | `theneurondaily.com` resolves again (prior NXDOMAIN note stale); `tips@latent.space` and `hello@the-decoder.com` verified from the outlets' own pages and added to `TARGETS`; greeting bug fixed; freshness re-run. 12 drafts in `pitches-2026-09-22.json`. No send. |
| 2026-09-29 | Cron reminder re-verification | **7 days with 0 sends from either batch.** Live MX re-confirmed on all 6 remaining candidates (latent.space, the-decoder.com, bensbites.com, lastweekinai.com, changelog.com, toolchase.com). Freshness re-run: 41/23/10/2 (see correction 5 — Pricing Watch still shows August dates). No send. |
| 2026-10-06 | Cron reminder re-verification | **14 days with 0 sends from either batch.** Live MX re-confirmed on the same 5 candidates. **Correction 5 CLEARED** — Pricing Watch now headlines 2026-10-01 (34 rows); freshness 41/23/9/2/1 with `cursor`+`claude` still FRESH. No blocker remains on the 3 sends below. No send. |
| 2026-10-08 | First reply from the Sep-3 batch logged | **ToolChase (Emre) replied 2026-10-08 13:30+03:00** to the Sep-3 resource pitch — a courteous acknowledgement ("will keep it in mind"), with **no rate card and no placement ask**, unlike Lilach Bullock's $300 offer. ToolChase row corrected from the erroneous "NOT SENT" to `SENT 2026-09-03 · REPLIED 2026-10-08`. Replied 2026-10-08 10:48 UTC correcting our own stale "74 tools" figure to the live 76 and pointing at the per-row checked dates on `/pricing-watch/`; signed AIToolsEssentials. Live MX re-confirmed (smtp.google.com); one Sent record, no duplicate. |
| 2026-10-08 | Batch status corrected | The weekly report of 2026-09-07 and this file's row 10 both carried ToolChase as "No response/NOT SENT"; the Sep-3 send to `hello@toolchase.com` (Sent 2026-09-03 22:09 UTC) is on record, so the batch's response tally is now **1 of 10**, not 0. |
| 2026-10-20 | Cron reminder run — 28 days, 0 sends; batch regenerated | Sent folder confirms no pitch mail since 2026-10-13 (only vendor submission replies), so the Oct-13 plan was never executed. Regenerated as `pitches-2026-10-20.json`: tool count re-derived 77 → 80; blog greeting grammar fixed (3 drafts) plus an `infoDOCKET` key typo that had been falling back to a fragment. MX re-confirmed live on the 6 candidate routes (the-decoder.com, latent.space, bensbites.com, toolchase.com, changelog.com, lastweekinai.com). Claims re-checked at source: `cursor` snapshot 2026-10-13 (X Subscription ladder), `claude` 2026-09-18 (Max $100). Send plan rewritten around two uncontacted editorial routes + the ToolChase warm follow-up, because the newsletter-first ordering this reminder suggested is contradicted by the batch's own 0/5 newsletter record. No send. |
| 2026-11-10 | Cron reminder run — 68 days, 0 sends; batch regenerated at 108 tools | Sent folder: newest outbound IDs 396–402 are vendor submission mail (11-08/11-10); last pitch mail remains the 2026-10-08 ToolChase reply. Inbox since 11-04 holds only tool submissions and vendor threads — no outlet replies. `data/tools.json` reached **108**, so `pitches-2026-11-03.json` (105) would have shipped a checkable-wrong count; regenerated as `pitches-2026-11-10.json` (12 drafts, 108 tools, dates cursor 2026-11-03 / claude 2026-09-18). Week plan unchanged: The Decoder + Latent Space first touch, Ben's Bites second touch with the repricing opening (not the Sep-3 resource text). No send. |
| 2026-11-03 | Cron reminder run — 40 days, 0 sends; checked dates now derived, batch regenerated | Sent folder: newest outbound is vendor/submission mail (IDs 378–392, 11-02/03); last pitch mail remains the 2026-10-08 ToolChase reply, so the Oct-20 plan also went unexecuted. `data/tools.json` reached **105**, i.e. `pitches-2026-10-20.json` was 25 tools behind, and `cursor` re-verified today made its "2026-10-13 check" string stale. `verified_overlap_line()` now calls new `pricing_checked_date()` and reads `cursor`/`claude` checked dates from `data/tool_sources.json` instead of hardcoding them — same drift class as the tool count. Regenerated `pitches-2026-11-03.json` (12 drafts, 105 tools, dates 2026-11-03 / 2026-09-18). MX live re-checked 11-03: the-decoder.com (mail.the-decoder.com), latent.space (smtp.google.com), bensbites.com (google). Week plan: The Decoder + Latent Space first touch, Ben's Bites second touch with the repricing opening. No send. |
