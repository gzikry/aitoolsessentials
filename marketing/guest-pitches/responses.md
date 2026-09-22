# Guest pitch responses — 2026-09-03 batch (+ 2026-09-22 additions)

Tracking file for the pitches in `pitches-2026-09-22.json` (12 drafts, supersedes the
10 in `pitches-2026-09-03.json`).
**Created:** 2026-09-15 · **Re-verified:** 2026-09-22 (cron reminder run). No sends logged yet.

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
| 10 | ToolChase | blog | hello@toolchase.com ⚠️ site sells ads — monetized desk | 10 | — | — | — | NOT SENT |
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
5. **Pricing Watch freshness — still open, now measurable.**
   `python3 scripts/verify_pricing_freshness.py` (2026-09-22): **42 FRESH · 23 UNREADABLE ·
   10 NO_CLAIM · 1 UNVERIFIED** across 76 snapshots. The two figures the pitch copy actually
   cites are both FRESH — `cursor` 4/4 claims and `claude` 4/4 claims still present on the
   vendors' live pages. But the **public page still shows stale August dates** (39 entries
   dated 2026-09-18, 21 dated 2026-08-25, 16 dated 2026-09-01), while promising weekly
   re-verification. Re-run the refresh before pitching the page as current, or lead the pitch
   with the September-18 batch.

## Log

| Date | Action | Notes |
|---|---|---|
| 2026-09-15 | Tracking file created | 0 sends from this batch; contacts and draft claims verified |
| 2026-09-18 | Corrections 1–3 fixed in source | `guest_pitch_builder.py` + `haro-outreach/pitch-templates.md` (commit `3bec7a04`). No send. |
| 2026-09-22 | Re-verified + 2 fresh targets added | `theneurondaily.com` resolves again (prior NXDOMAIN note stale); `tips@latent.space` and `hello@the-decoder.com` verified from the outlets' own pages and added to `TARGETS`; greeting bug fixed; freshness re-run. 12 drafts in `pitches-2026-09-22.json`. No send. |
