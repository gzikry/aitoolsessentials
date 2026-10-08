# Guest pitch responses — 2026-09-03 batch (+ 2026-09-22 additions)

Tracking file for the pitches in `pitches-2026-09-22.json` (12 drafts, supersedes the
10 in `pitches-2026-09-03.json`).
**Created:** 2026-09-15 · **Re-verified:** 2026-09-29 (cron reminder run). Still no sends logged.

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

## Send plan for the week of 2026-09-22 (3 sends)

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
