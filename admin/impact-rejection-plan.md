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
   acceptance: ShareASale/Awin, PartnerStack (SaaS-heavy, friendlier to small
   sites), CJ Affiliate.
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

These four have official direct/partner programs we haven't applied to yet.
George applies manually; answers are in `admin/affiliate-applications-ready.md`
patterns. Priority order:

1. **Grammarly** — grammarly.com/affiliates (big consumer reach, content-friendly)
2. **Jasper** — Jasper affiliate via FirstPromoter (writing audience match)
3. **Descript** — descript.com/affiliate via PartnerStack (creator/podcast audience)
4. **Gemini/Google Cloud** — CJ Affiliate via cloud.google.com/affiliate-program
   (lower priority: indirect program, B2B-ish)

For each application, reuse our Impact answer copy but swap in:
- Real traffic numbers from Plausible once available.
- The specific page where their tool is reviewed/comparisons where they appear.
- Existing approved programs (ElevenLabs, Make) as social proof.
