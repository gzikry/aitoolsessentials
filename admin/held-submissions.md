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
| Image Describer | imagedescriber.dev | 2026-09-08 | support@imagedescriber.dev | Awaiting reply |
| Sharpniq / Unblur Image | unblurimage.me | 2026-09-08 | support@unblurimage.me | Awaiting reply |
| Vedic Astrology Chart | vedicastrologychart.net | 2026-09-08 | support@vedicastrologychart.net | Awaiting reply |
| Video Upscaler | videoupscaler.video | 2026-09-08 | support@videoupscaler.video | **Vendor contact broken** — hard bounce `550 5.1.1 address does not exist` on 2026-09-11; the address is still printed in their own privacy/terms pages. Domain has MX. Unpublishable and unreachable until they fix it. |
| Visemix | lipsync.vip | 2026-09-09 | support@lipsync.vip | Awaiting reply |
| Blur Background / Vignra | blurbackground.vip | 2026-09-09 | support@blurbackground.vip | Awaiting reply |
| Sonaopus | sonaopus.com | 2026-09-09 | praise.ayo.boyinde@gmail.com | Awaiting reply — no privacy/terms pages, entity/jurisdiction, local-processing claims, $99 vs third-party $59, legal-review disclosure, business address |
| GetMotionTransfer / MotionTransfer | getmotiontransfer.com | 2026-09-11 | channelerH@gmail.com | Awaiting reply — entity/jurisdiction unnamed in ToS, no domain MX (Gmail-only contact), pricing contradictions (subscription tiers vs "packs", footer still says "no subscription"), credit expiry, refund terms conflict, third-party model resale rights, media retention for training |

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
