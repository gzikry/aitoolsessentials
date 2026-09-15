# Guest pitch responses — 2026-09-03 batch

Tracking file for the 10 pitches in `pitches-2026-09-03.json`.
**Created:** 2026-09-15 (cron reminder run). No sends logged yet for this batch.

Status legend: `NOT SENT` · `SENT` · `AWAITING` · `REPLIED` · `NO RESPONSE` · `CLOSED`

| # | Outlet | Type | Contact | Priority | Sent | Follow-up | Response | Outcome |
|---|---|---|---|---|---|---|---|---|
| 1 | TLDR AI | newsletter | dan@tldr.tech ⚠️ no contact route published | 1 | — | — | — | NOT SENT |
| 2 | The Rundown AI | newsletter | support@therundown.ai | 2 | — | — | — | NOT SENT |
| 3 | Ben's Bites | newsletter | team@bensbites.com | 4 | — | — | — | NOT SENT |
| 4 | The Neuron | newsletter | team@theneurondaily.com ❌ domain NXDOMAIN | 3 | — | — | — | NOT SENT — bounce confirmed |
| 5 | Last Week in AI | podcast | contact@lastweekinai.com ⚠️ site unreachable | 5 | — | — | — | NOT SENT |
| 6 | Changelog / Practical AI | podcast | editors@changelog.com ✅ verified contact page | 6 | — | — | — | NOT SENT |
| 7 | ToolChase | blog | hello@toolchase.com ⚠️ site sells ads — likely monetized desk | 7 | — | — | — | NOT SENT |
| 8 | AIToolsRecap | blog | editor@aitoolsrecap.com ⚠️ "paid review" / sponsored on site | 8 | — | — | — | NOT SENT |
| 9 | ToolRadar | blog | contact@aitoolradar.io ⚠️ "Submit Tool" / sponsored on site | 9 | — | — | — | NOT SENT |
| 10 | infoDOCKET | blog | gprice@gmail.com ✅ verified — Gary Price, Library Journal | 10 | — | — | — | NOT SENT |

## Contact verification (checked 2026-09-15)

- **`theneurondaily.com` no longer resolves — NXDOMAIN at both 1.1.1.1 and 8.8.8.8.** No MX, no A record. The live newsletter is on **theneuron.ai**. Sending to `team@theneurondaily.com` will hard-bounce. Source the contact from theneuron.ai before any send, or drop it from the batch.
- **TLDR AI publishes no editorial/feedback address.** `tldr.tech` links only to `https://advertise.tldr.tech/`. `dan@tldr.tech` is a guess.
- **Last Week in AI:** `lastweekinai.com` did not respond to an HTTPS request (curl timeout / no response). Mailbox exists (PrivateEmail MX) but the site's reachability needs re-checking.
- Confirmed deliverable: tldr.tech, therundown.ai, bensbites.com, changelog.com, infodocket.com, toolchase.com, aitoolradar.io, aitoolsrecap.com all have live MX.

## Do not re-send blindly

An earlier resource pitch to `dan@tldr.tech`, `support@therundown.ai`, `team@bensbites.com`, and `team@theneurondaily.com` went out around **Sep 3** and drew **0/10 responses** (see `traffic/weekly-report-2026-09-07.md`). The Sep-14 report's finding applies to this list too: addresses that reply are monetized placement desks, not editors — ToolChase, ToolRadar, and AIToolsRecap all advertise sponsored/paid-review placements on their homepages. A second identical resource pitch to the same newsletter addresses six weeks later is a follow-up, not a new pitch — either change the angle or skip them.

## Content corrections before sending

1. **"We track 74 tools" is stale in all 10 drafts.** The site publishes **76** (verified on `/tools/`, 2026-09-15). `scripts/guest_pitch_builder.py` hardcodes 74 — fix the template.
2. **The blog-template bullets are unverified claims.** The drafts assert "Copilot Pro ($10) + Cursor Pro ($20) + Claude Max ($100+) = $130/month" and "ChatGPT Pro split into two tiers ($120/$200)." Neither figure appears in `data/tools.json` or `data/pricing_snapshots.json` — our own verified data has ChatGPT priced as "Free + paid plans" and no "Copilot Pro" tier at all. For a site whose pitch is *verified pricing with dated evidence*, shipping unsourced numbers to editors is the one error that costs the angle. Either source and snapshot them first, or cut the bullets.
3. **Signature.** Drafts are signed "— George Zikry". Standing convention is outbound mail signed **AIToolsEssentials**, never George's name.
4. **Pricing Watch freshness.** Snapshots run 2026-08-21 → 2026-09-13; 37 of 76 are from 2026-08-21 (25 days old) while the page promises weekly re-verification. An editor who clicks today sees August dates. Re-verify before pitching it as current.

## Log

| Date | Action | Notes |
|---|---|---|
| 2026-09-15 | Tracking file created | 0 sends from this batch; contacts and draft claims verified |
