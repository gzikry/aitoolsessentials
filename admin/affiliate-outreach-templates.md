# Affiliate Application Outreach — AIToolsEssentials

Priority queue (still open): Browse AI, Grammarly, Jasper, Gemini (Google).
Already approved and wired: ElevenLabs, Make, Nous / Hermes, Sonaopus, Gamma (PartnerStack).
Networks to join first: Impact.com, CJ Affiliate, PartnerStack (covers most SaaS programs).
**Network status 2026-09-14: Impact rejected (2026-08-25); PartnerStack DECLINED (2026-09-14)** —
our Network Profile was not accepted and access to *new* Marketplace programs is limited. Existing
partnerships are unaffected (Gamma's link stays live, Descript's application is not cancelled).
Every remaining marketplace-hosted target — Browse AI, Grammarly Business, Copy.ai — is now gated
on the network profile, not on the vendor. Reapply is dashboard-only and George-only. Direct
programs are the path that still works; do not open new network applications until traffic grows.

## Standard application blurb

> AIToolsEssentials (aitoolsessentials.com) is an evidence-first AI tools directory:
> 76 independently reviewed tools with verified official pricing, dated benchmark
> evidence, and buyer guides for specific audiences (agencies, freelancers,
> developers). We publish honest cons alongside pros — our reviews carry trust
> because we show tradeoffs.
>
> Traffic is in early growth; we apply now for consideration as coverage expands.
> Placement: contextual links inside relevant reviews and comparisons only —
> never display ads or popups. All placements follow FTC-compliant disclosure.

## Per-program notes
- **Impact (network)**: apply once, then add individual programs (Make, Jasper...). Site profile: content site, IAB category Software/SaaS.
- **Grammarly**: uses Impact. Emphasize writing-tools guide coverage.
- **ElevenLabs**: direct program on their site (/affiliates). Strong fit — voice tools review is a top page.
- **Gemini**: via Google's affiliate program (rare approvals early); deprioritize until traffic proves out.
- **Make**: direct application at make.com partner page. Automation comparison pages are natural placement.

## Rules
- Record every status change in data/affiliate_programs.json.
- Only swap CTA links after an approved tracking URL exists in that file.
- rel="sponsored nofollow" on all affiliate links, per disclosure policy.

## AdSense track (secondary revenue)
1. Apply at adsense.google.com with aitoolsessentials.com once ≥20-30 organic visits/day.
2. On approval: ads.txt line (google.com, pub-XXXX..., DIRECT, f08c47fec0942fa0) + script snippet in cleanup_html.py.
3. Keep ad density minimal — sponsor-direct revenue beats AdSense RPM for this niche; use AdSense only as backfill.
