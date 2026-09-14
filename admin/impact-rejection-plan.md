# Impact.com Rejection — Response Plan (2026-08-24)

Impact.com rejected our publisher application. This is normal for early-traffic
sites and does not block monetization. Impact was always the lowest-priority
channel per our revenue strategy.

## Why this likely happened

- Site launched August 2026 — very little organic traffic history yet.
- Impact favors publishers with established monthly traffic (often 10k+ visits).
- Nothing about our content, compliance, or disclosure was deficient — the
  verification meta is deployed and all application answers were accurate.

## What NOT to do

- Do not reapply immediately — rejections followed by instant reapplication
  with no material change usually extend the cooldown.
- Do not pay for anything on Impact. Publisher signup is free; there is nothing
  to upgrade.
- Leave the impact-site-verification meta in place. It is harmless and will be
  ready if/when we reapply.

## The plan instead (direct-first strategy)

1. **Direct vendor affiliate programs first** — apply directly to vendors with
   in-house programs. These don't require a network:
   - Check `data/affiliate_programs.json` for programs marked available with
     official program URLs we haven't applied to yet.
   - Strong candidates typically: ElevenLabs (done ✅), Make.com (done ✅),
     plus any tools offering direct/partner signup.
2. **Other networks are optional backups**, applied only when traffic supports
   acceptance: ShareASale/Awin, CJ Affiliate.
   - **PartnerStack — DECLINED 2026-09-14.** The line here previously called it
     "SaaS-heavy, friendlier to small sites". That turned out to be wrong for us:
     `networkquality@partnerstack.com` limited our Marketplace access the same way,
     saying our Network Profile "is not a great fit, but may be in the future."
     Two network rejections in three weeks on the same ground — traffic and profile fit
     — so treat **networks as closed until the traffic threshold is met**, not as a
     queue to keep working. Direct programs are the only channel still accepting us.
   - Existing PartnerStack partnerships survive the limit (Gamma's link is live), so the
     rejection cost us nothing already earned; it only closes new marketplace joins
     (Browse AI, Grammarly Business, Copy.ai).
3. **Reapply to Impact at ~20–30 organic visits/day** (the same threshold as
   AdSense). At that point include:
   - Plausible screenshot or public dashboard link showing real traffic.
   - Updated page count and any conversion evidence from existing affiliate links.

## Update the application answers before reapplying

Edit `admin/impact-application-answers.md` when reapplying:
- Replace "154 pages / early-growth" with real traffic numbers from Plausible.
- Add conversion data from ElevenLabs/Make clicks if available.
- Mention Premium membership revenue as proof of monetization beyond affiliates.

## George's action items

- [ ] Note the rejection reason if Impact's email gave one (share it and we'll adjust).
- [ ] Keep clicking Verify/completing direct-program signups as they come.
- [ ] No Impact reapplication until the ~20–30 visits/day threshold.


## Direct-application queue (apply now, no Impact needed)

These have official direct/partner programs we haven't applied to yet.
George applies manually; answers are in `admin/affiliate-applications-ready.md`
patterns. Priority order:

1. **Grammarly** — grammarly.com/affiliates (big consumer reach, content-friendly)
   — still routes through Impact, so blocked on the Impact reapplication. A private
   Grammarly Business listing exists on PartnerStack but is itself gated by the
   2026-09-14 network limit.
2. **Jasper** — Jasper affiliate via FirstPromoter (writing audience match) — hosts
   through Impact; blocked on the same reapplication.
3. **Descript** — descript.com/affiliate via PartnerStack (creator/podcast audience)
   — **application submitted 2026-09-12 and still pending**; the network limit does
   not cancel existing partnerships, so leave it.
4. **Gemini/Google Cloud** — CJ Affiliate via cloud.google.com/affiliate-program
   (lower priority: indirect program, B2B-ish)

Note as of 2026-09-14: items 1-2 both depend on Impact, and every
PartnerStack-hosted route is gated by the network limit, so this queue is effectively
**paused on traffic** rather than actionable today. The work that still pays is
direct-program outreach and the site itself.

For each application, reuse our Impact answer copy but swap in:
- Real traffic numbers from Plausible once available.
- The specific page where their tool is reviewed/comparisons where they appear.
- Existing approved programs (ElevenLabs, Make) as social proof.
