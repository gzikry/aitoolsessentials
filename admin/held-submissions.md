# Held vendor submissions

Submissions that arrived through `/submit-tool.html` (FormSubmit → `aitoolsessentials@gmail.com`)
and are **not published**. Each was reviewed independently and placed on hold pending
verification. A verification request was sent in every case; hold means "not rejected".

Rule: do not re-send a verification request for an entry that is already listed here with a
sent date, and do not publish a held tool until the vendor answers the outstanding questions.

| Submission | Domain | Held since | Request sent to | Status |
|---|---|---|---|---|
| RoomMaker AI | roommakerai.org | 2026-08-29 | s07811005141@gmail.com | Awaiting reply — ownership, retention, testimonial evidence, working domain address, shared-operator question (RoomMaker AI / ImgToLayers) |
| ImgToLayers | img2layers.org | 2026-08-29 | s07811005141@gmail.com | Awaiting reply — same operator question, retention/deletion not built yet, Fal.ai subprocessor terms |
| BrickGPT | brickgpt.online | 2026-08-31 | charliiai2024@gmail.com | Awaiting reply — name-squat risk (CMU ICCV 2025 BrickGPT), no legal pages |
| Zirvox | zirvoxinc@gmail.com | 2026-09-01 | zirvoxinc@gmail.com | Awaiting reply |
| FreeGen | freegen.ai | 2026-09-07 | justacatbot@proton.me | Awaiting reply — operator identity, HF account `cgb` link, controller/jurisdiction, name collision |
| Image Describer | imagedescriber.dev | 2026-09-08 | support@imagedescriber.dev | Awaiting reply. **Re-submitted 2026-09-22 15:29 UTC** (identical payload — same name/url/category/summary/contact; `pricing_url` and `docs_url` still blank), first submission 2026-09-08 05:04 UTC. Our 2026-09-07 request was accepted, not bounced (no DSN for this recipient in any folder). Re-checked live 2026-09-22: privacy/ToS now carry retention (temporary server uploads removed after processing, one-day cleanup fallback; local history 20 records/7 days; payment-recovery images 30 minutes), an explicit "we do not train public models on user-uploaded images", and output ownership. **Still open: no legal entity, controller, or jurisdiction named anywhere** (ToS §11 reads "governed by applicable laws" with no chosen law), **no subprocessor named at all** (the AWS/Redis/Crisp hits were substring false positives on "laws"/"credits"), and the four paid tiers the site actually sells were never disclosed. |
| Sharpniq / Unblur Image | unblurimage.me | 2026-09-08 | support@unblurimage.me | Awaiting reply — submission said $19.90/month, site sells one-time packs. **Re-submitted 2026-09-22 15:29 UTC** (identical payload), first submission 2026-09-08 05:05 UTC. Prior request accepted, not bounced. Re-checked live 2026-09-22: the credit-model contradiction is now resolved and consistent across pricing, ToS and FAQ — Starter $4.99/100 credits (10 images), Plus $9.99/220 credits (22 images), 10 credits per Cloud Unblur result, **no subscription anywhere**, 10 free new-account credits. Retention stated (originals and outputs scheduled for deletion after 24 hours), processors named (Fal.ai, Stripe; Creem only if shown at checkout), and a brand `/about` page explains Sharpniq = Unblur Image + Image Clarity Checker. **Still open: no legal entity, controller, or jurisdiction named**, and training use is unstated. |
| Vedic Astrology Chart | vedicastrologychart.net | 2026-09-08 | support@vedicastrologychart.net | Awaiting reply |
| Video Upscaler | videoupscaler.video | 2026-09-08 | support@videoupscaler.video | **Vendor contact broken** — hard bounce `550 5.1.1 address does not exist` on 2026-09-11; the address is still printed in their own privacy/terms pages. Domain has MX. Unpublishable and unreachable until they fix it. |
| Visemix | lipsync.vip | 2026-09-09 | support@lipsync.vip | Awaiting reply |
| Blur Background / Vignra | blurbackground.vip | 2026-09-09 | support@blurbackground.vip | Awaiting reply. **Re-submitted 2026-09-22 15:29 UTC** (identical payload), first submission **2026-09-08 05:07 UTC** (mail `id=35`; the 2026-09-09 in the held-since column is the local working date), prior request accepted (no DSN). Re-checked live 2026-09-22: the 365-day expiry contradiction is **still live and unchanged** — `/pricing` says "Purchased Credits never expire" three times while `/terms-of-service` says "Purchased Credit Packs are one-time purchases, do not renew automatically, and currently expire 365 days after grant." Packs confirmed: Starter $2.99/10 images, Plus $6.99/30, Creator $12.99/60. Retention now specified (source photo available ≤24h; delivered result up to 30 days; Fal mask deleted when rendering completes), Fal named as the only AI processor. **Still open: no legal entity, controller, or jurisdiction named**, and auth/storage/payment/analytics are still described only as "third parties". |
| Sonaopus | sonaopus.com | 2026-09-09 | praise.ayo.boyinde@gmail.com | **PUBLISHED 2026-09-12** (commit `328c5223`) after the vendor cleared verification. Vendor published `/privacy` + `/terms` on 2026-09-12, naming operator Praise Boyinde (sole proprietor), governing law Nigeria, user-retained output ownership, no-refunds position, and the subprocessors that actually touch data (Netlify, Gumroad). Local-storage claim re-verified from shipped JS: keys `sonaopus_hr`/`_ea`/`_pm`/`_re`/`_role`, zero `fetch`/XHR/sendBeacon, no third-party scripts, no URL-passing (`claude.ai/new`, `chatgpt.com/`, `gemini.google.com/` carry no query params). $99 confirmed on all five Gumroad products. $59 traced to a **stale third-party mirror** — `devadex.com` mirrors retired account `sonaopusaiworkflow.gumroad.com` (now 404, still indexed). Publication reply sent 2026-09-12. **2026-09-13 vendor follow-up (live re-check):** homepage FAQ no longer says "Nothing stored" — wording now matches the Privacy Policy (browser-local storage / everything runs in the browser). Standalone legal-review FAQ (“Nothing happens without you”) is live. Affiliate terms stated in writing: 40% flat one-time ($39.60 per $99), no recurring, 30-day cookie, Gumroad payout; signup at sonaopus.com or sonaopus.gumroad.com/affiliates. Those three items are closed in verification notes. Remaining open: no service address, no local-data export, stale $59 mirror, no MX (Gmail-only contact). Affiliate program approved 2026-09-13; disclosed tracking URLs wired on the review (site ref + five per-product Gumroad links), and Sonaopus was added to the public affiliate-disclosure program list 2026-09-13. Correction email sent 2026-09-13 (Sent msg 166) because our previous note said we had not enrolled yet, which the approval superseded an hour later. |
| GetMotionTransfer / MotionTransfer | getmotiontransfer.com | 2026-09-11 | channelerH@gmail.com | Awaiting reply — entity/jurisdiction unnamed in ToS, no domain MX (Gmail-only contact), pricing contradictions (subscription tiers vs "packs", footer still says "no subscription"), credit expiry, refund terms conflict, third-party model resale rights, media retention for training |
| Short.now | short.now | 2026-09-14 | gem88612@gmail.com (cc mail@short.now) | **Request sent 2026-09-14** (Sent msg 168). **Vendor replied 2026-09-14 18:00 +01:00** (Alex, halyapin@gmail.com) confirming only that `mail@short.now` is the correct contact and that he is authorised to speak for the product — **item 6 closed**. **Follow-up sent 2026-09-14** (Sent msg 170, cc mail@short.now) after re-fetching every page: items 1–5 are all **still live on their site, nothing fixed**. Awaiting substantive reply — (1) no legal entity, registered address, or jurisdiction named (ToS §13 still says "the jurisdiction in which Short.now is incorporated"; `/impressum/` and `/de/impressum/` still 404); (2) no subprocessors named, training use unstated, and the retention conflict is unchanged and specific — Privacy says "deleted from our servers within 30 days of processing unless you explicitly save them," ToS §10 says free-plan "uploaded videos and generated media are stored for 30 days, after which they are permanently deleted"; (3) free-plan allowance still contradicts itself — homepage card + FAQ "3 videos to start, then 1 every week" vs `/tools/`, `/tools/free-clipping/`, `/compare/best-ai-video-clipping-tools/`, `/for/youtubers/`, `/compare/short-now-vs-opus-clip/` all "3 free videos every month"/"3 videos/month free", llms.txt "3 long videos to start, then 1 more every week"; (4) plan-name contradiction still live — homepage Starter card $7/mo ($5.50/mo annual, $67/yr, 5 videos) and Creator $12/mo ($144/yr, 10 videos, auto-posting) per llms.txt, but `/compare/short-now-vs-opus-clip/` says "Starter paid plan $12/month (8 videos)" and `/compare/best-ai-video-clipping-tools/` says "Starting price $12/month" — Creator's price under the Starter label, and 8 vs 10 videos; `/pricing/` returns 404 so the homepage card + llms.txt are the only citable sources; (5) competitor free-tier rows still inaccurate — Opus Clip publishes $0 with 60 credits/month, Starter $15/mo, Pro $29/mo. Affiliate terms still unstated. |
| SaaSHub listing re-review | saashub.com/aitoolsessentials | 2026-09-13 | (none — SaaSHub mail says do not send details by email) | **No action required.** Stan@saashub.com asked 2026-09-13 for competitors, ≥3 categories, logo and pricing. All four were already completed from published site facts via the one-time token-login management pages on 2026-09-13 and verified on the live listing. The remaining "Pending approval" banner clears only on SaaSHub's own re-review (up to ~32 days). Do not email them; do not re-submit. |
| Img2STL | img2stl.org | 2026-09-12 | s07811005141@gmail.com | **Request sent 2026-09-12** (Sent msg 161). Awaiting reply — **name collision + third domain from the same operator as RoomMaker AI + ImgToLayers** (identical Gmail, identical Cloudflare NS pair `damon`/`violet`). **Domain registered 2026-09-08 (Spaceship), four days before the submission**; a live commercial photo-to-3D product already runs at `img2stl.art` (registered 2026-06-06) and public `img2stl` GitHub lithophane projects predate both. No MX on the domain; Gmail is the only contact (mailto in their own footer). No named entity/controller/jurisdiction, no governing-law section. Privacy/ToS are Cloudflare boilerplate shared with the sister sites (ToS byte-identical to both; privacy 0.961 similar to RoomMaker). ToS references "our refund policy" but `/refund`, `/refund-policy`, `/contact-us` all 404. No output-rights page (`/rights` 404) — commercial use appears only as a plan bullet. Privacy describes accounts + payment data while advertised free modes need no account. AI Full 3D upload destination, retention, and training use undisclosed; Plausible (self-hosted at `plausible.danhsu.space`), AdSense, GA, tawk.to and Crisp are bundled but none are named as subprocessors. Submission omitted every paid tier (Maker $19/mo, Studio $49/mo, Business $129/mo, Scale $299/mo) and sent `pricing_url` = homepage |

## Operator template cluster: 5 sites, no entity named (verified 2026-09-22)

A second cluster — separate from the `s07811005141@gmail.com` one — is proven by the sites' **own public
cross-links**, not by inference. Every member footer links to the other three, so the relationship is
published by the operator rather than deduced:

| Domain | MX | NS pair | Footer cross-links to |
|---|---|---|---|
| blurbackground.vip | Cloudflare | `alan`/`beth` | imagedescriber.dev, vedicastrologychart.net, videoupscaler.video |
| imagedescriber.dev | Cloudflare | `pedro`/`sunny` | blurbackground.vip, vedicastrologychart.net, videoupscaler.video |
| vedicastrologychart.net | AWS inbound-smtp | `pedro`/`sunny` | blurbackground.vip, imagedescriber.dev, videoupscaler.video |
| videoupscaler.video | Cloudflare | `pedro`/`sunny` | blurbackground.vip, imagedescriber.dev, vedicastrologychart.net |
| unblurimage.me | Cloudflare | `alan`/`beth` | no footer links — but shares the `alan`/`beth` NS pair with blurbackground.vip, uses the same template (identical `/privacy-policy`, `/terms-of-service`, `/pricing`, `/contact`, `/data-deletion`, `/refund-policy` route set, same `support@` handle, same one-time-credit-pack model, same "Browser Free / Cloud" split) |

Shared across all five: **not one names a legal entity, data controller, or jurisdiction**; all sell
one-time credit packs (no subscriptions); none has a governing-law clause naming a country.
unblurimage.me names Fal.ai + Stripe; blurbackground.vip names only Fal; imagedescriber.dev names
none. All four submissions from this cluster arrived in one burst
(2026-09-08 05:04–05:07 UTC; FormSubmit timestamps carry minute resolution, so the ordering
is exact but sub-minute spacing cannot be asserted), which is batch submission from one
operator.

**Not yet sent:** one combined request covering all five domains. Three of the five already have
individual requests on file (blurbackground.vip 2026-09-09, unblurimage.me and imagedescriber.dev
2026-09-07); the combined request would supersede those and add vedicastrologychart.net and
videoupscaler.video, which have holds but no outgoing request on record. Held back because this
cron run's instruction to reply automatically covers *new* submissions, and resending to senders
that already have requests on file is exactly the double-send the ledger rule forbids.

## Operator cluster: `s07811005141@gmail.com` (three domains)

The same operator has now submitted three domains through `/submit-tool.html`, all still unpublished:

| Domain | Submitted | Held since | Product |
|---|---|---|---|
| roommakerai.org | 2026-08 | 2026-08-29 | RoomMaker AI |
| img2layers.org | 2026-09-02 | 2026-08-29 | ImgToLayers |
| img2stl.org | 2026-09-12 | 2026-09-12 | Img2STL |

Name-collision evidence for Img2STL (verified 2026-09-12): `img2stl.org` registered 2026-09-08;
`img2stl.art` registered 2026-06-06 and already sells a photo-to-3D converter with Studio, credits and
tiered pricing under the same name; public `img2stl` GitHub lithophane projects (e.g. `smrini/img2stl`,
`rmrao/img2stl`) predate both. Ask for rights to the name before any listing.

Verified shared signals (2026-09-12): identical contact `s07811005141@gmail.com`; none of the three
domains has MX records; all three serve Cloudflare-hosted legal boilerplate — the ToS text is
byte-identical across all three and RoomMaker's privacy policy is 0.961-similar to Img2STL's, while
their own product privacy pages differ (ImgToLayers 0.553-similar, documenting the real upload
pathway). None names a legal entity, controller, or jurisdiction; none publishes a refund policy URL
despite the ToS referring to one. All three are template-built product microsites.

Two verifications are already outstanding against this operator (sent 2026-08-29, no reply). Each new
domain gets its own targeted request, but the shared items (ownership, entity, working contact,
template legal pages, refund policy) are stated once and apply to all three. Do not publish any of the
three until the operator answers.

## Notes for future runs

- The GetMotionTransfer submission (Sep 3, 2026 UTC) had been filtered to `[Gmail]/Spam` and was
  not covered by the hourly monitor, which only scanned `[Gmail]/All Mail`. The monitor now scans
  both folders and treats `submissions@formsubmit.co` mail in Spam as actionable.
- Verified pricing and plan structure for GetMotionTransfer were captured from
  `getmotiontransfer.com/pricing` on 2026-09-11: Starter $19/mo ($180/yr, 1,000 credits),
  Pro $49/mo ($540/yr, 3,500 credits), Studio $109/mo ($1,188/yr, 8,000 credits);
  a conflicting spec table lists 500 / 2,500 / 7,000 credit "packs"; Kling V3 motion control is
  15 credits/s Standard, 20 credits/s Professional.
- If a vendor replies and clears the questions, add the tool to all four data registries
  (`data/tools.json`, `data/tool_sources.json`, `data/revenue_targets.json`,
  `data/pricing_snapshots.json`), regenerate, validate, deploy, then send the publication reply.
