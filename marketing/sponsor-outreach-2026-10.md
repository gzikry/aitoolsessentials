# Sponsor / Verified-listing outreach — October 2026

Program: $79 Verified listing + site-wide sponsor bar at $150/mo (`FOUNDING100` = first month $50).
Copy and prices match the live `/sponsor/` page (200) and `data/sponsors.json` (`site_bar`, `verified_listing`,
`issue`, `bundle`) as of 2026-10-23. Sends sign as AIToolsEssentials only.

## 2026-10-23 batch — 15 sends, 12:56–12:57 PT (19:56–19:57 UTC)

All 15 went out from `aitoolsessentials@gmail.com` and are present in `[Gmail]/Sent Mail`
(Sent IDs 320–334 at time of writing — cite by date + subject, not by ID; IDs are folder-relative).

| Recipient | Product | Review live? | MX |
|---|---|---|---|
| eric@stackblitz.com | StackBlitz | no (prospect pitch) | Google |
| press@elevenlabs.io | ElevenLabs | yes `/tools/elevenlabs/` | Google |
| press@synthesia.io | Synthesia | yes `/tools/synthesia/` | Google |
| media@copy.ai | Copy.ai | yes `/tools/copy-ai/` | Google — **local part dead, see bounce** |
| partners@jasper.ai | Jasper | yes `/tools/jasper/` | Google |
| marketing@n8n.io | n8n | yes `/tools/n8n/` | Google |
| hello@lumalabs.ai | Luma AI | yes `/tools/luma-ai/` | Google |
| partners@spellbook.legal | Spellbook | yes `/tools/spellbook/` | Google |
| hello@grantable.co | Grantable | yes `/tools/grantable/` | Google |
| partners@instrumentl.com | Instrumentl | yes `/tools/instrumentl/` | Google |
| press@otter.ai | Otter.ai | yes `/tools/otter-ai/` | Google |
| press@heygen.com | HeyGen | yes `/tools/heygen/` | Google |
| marketing@tldv.io | tl;dv | no (prospect pitch) | Google |
| press@fyxer.com | Fyxer | no (prospect pitch) | Google |
| press@superhuman.com | Superhuman | no (prospect pitch) | Google |

Domain sweep: **15/15 recipient domains publish MX** (Google Workspace or Google-hosted), so none of the
remaining fourteen is a future no-MX bounce. Verify a new recipient's MX before adding it to a batch —
a live vendor site is not evidence of a working mailbox.

The four prospect pitches (StackBlitz, Fyxer, Superhuman, tl;dv) do **not** claim a live review; their bodies
say the product "belongs in that set" / "fits that category" and pitch the $79 Verified listing as the way in.
Checked, because a pitch that links a 404 to a stranger is worse than no pitch. If any of them replies,
that reply is a vendor submission and goes through `vendor-tool-submission` vetting — do not list on the
strength of a sales thread.

## Replies received

- **Synthesia press office** (`press+noreply@synthesia.io`, 19:56 UTC, `Re: Synthesia on
  AIToolsEssentials…`) — automated press-office acknowledgement: "we will get back to you as soon as
  possible", plus a pointer to their self-serve AI press officer. **Not an answer to the ask.** No reply sent:
  an autoresponder is not a correspondent, and a same-day follow-up is nagging.
- **Luma AI** (`hello@lumalabs.ai`, 19:56 UTC, `Re: Luma AI on AIToolsEssentials…`) — automated support
  acknowledgement ("This is an automated message to confirm we've received your message") with a product
  blurb for Luma Scenes. Same handling: recorded, not answered.

Both landed within a minute of the send, which is what an autoresponder looks like. A human reply to either
thread is the only thing that would justify a follow-up.

## Delivery failure — media@copy.ai (final)

DSN `[Gmail]/All Mail` 2026-10-23 12:56 PT: **`550 5.1.3` — "The email account that you tried to reach does
not exist"** (`NoSuchUser`) for `media@copy.ai`. Final, not a delay.

- `copy.ai` MX resolves (Google, plus an `mx-verification.google.com` record at priority 15). Port 25 reaches it.
- RCPT probe returned **`250` for `media@copy.ai` AND `250` for a random local part** — the domain answers at
  RCPT for anything (accept-then-filter), so the probe cannot confirm or deny a mailbox here. Gmail's own
  hard failure on the specific local part is the stronger evidence; do not read the `250` as "deliverable".
- The only address published on `www.copy.ai/contact` is **`copyaisupport@fullcast.com`** (Copy.ai is part of
  Fullcast), which accepts mail (`250`). That is a support queue for the acquiring company, not a press or
  partnerships inbox — **no re-send was made**, because the pitch would be landing in the wrong queue.
- No retry to `media@copy.ai`: it hard-fails, and a second send would only produce a second DSN.

Operator decision left open: whether to pitch `copyaisupport@fullcast.com` once, or drop Copy.ai from the
sponsor batch and route future contact through their sales form.

Incidental check while handling the bounce: the Copy.ai listing is still accurate. Live `/pricing` today shows
Chat at $29/mo (or $24/mo billed $288/yr) and Growth at $1,000/mo billed annually, matching the 2026-09-18
snapshot digest. The site has repositioned around "GTM AI Platform" but still sells the same self-serve plan.

## Earlier sends from this program

2026-10-20 14:05–14:11 (mail timestamps −04:00, so 11:05–11:11 PT): `michael@hol.org` (HOL Registry),
`listings@robylon.ai` (Robylon), `support@sembly.ai` (Sembly). No inbound reply traced to any of the three in
`[Gmail]/All Mail` (newest 60), `[Gmail]/Spam` or `[Gmail]/Trash` as of 2026-10-23. `support@sembly.ai` is a support queue rather than a marketing inbox —
expect silence from that one rather than reading it as disinterest.

## Next actions

1. Watch for human replies to the 2026-10-23 batch; any reply that names terms is a revenue lead for the
   operator, not routine mail.
2. Decide the Copy.ai route (Fullcast support inbox vs sales form); do not re-send to `media@copy.ai`.
3. Do not re-pitch any of the fifteen inside the same week — the tracker row is the record that the ask landed.
