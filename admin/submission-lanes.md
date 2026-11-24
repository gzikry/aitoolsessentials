# Submission lanes (draft policy, needs George's go)

Drafted 2026-11-24. Nothing here is in force until George approves it. Until then the intake run keeps its current behavior.

## Why

The public submit page promises a "3–4 week review backlog" for the free form. In practice the intake run publishes accepted free submissions as it reviews them, with no queue: ten free submissions went live between 2026-11-19 and 2026-11-23 (for example Markin on 2026-11-19, TINY DESK AI on 2026-11-19, Ozil Goal AI and AI Genjutsu on 2026-11-20, Unblurfy and Image Text Editor on 2026-11-20, TinyCommand and GTA6 AI Video on 2026-11-21, Sarah AI on 2026-11-22, MiniMax H3 Image on 2026-11-23; see `git log`). The $79 Verified fast lane can't sell while the free lane is just as fast. Stripe showed no charges on the live account on 2026-11-24.

## The two lanes

| Lane | Price | Promise | What the intake run does |
| --- | --- | --- | --- |
| Free queue | $0 | Reviewed in arrival order. The queue currently runs 3 to 4 weeks. No written feedback if declined. | Acknowledge, add to `admin/held-submissions.md` queue with the received date, review oldest first. Publish no earlier than 14 days after receipt. |
| Verified fast lane | $79 (live link `https://buy.stripe.com/7sY6oG3Ed2SF7JZ3eD0x205`) | Written decision within one working day. Full refund if declined. Same score as the free queue. | Match the Stripe payment email to the form, review the same working day, send the written decision, publish if accepted. Refund in Stripe if declined (George's click). |

Founder products on `/founders/` (Launch-day feature $49, roundup line $29, Launch pack $99) render as email requests until George approves the Stripe products and the payment links are added to `data/founder_products.json`.

## Free-queue acknowledgement (draft — sending it needs George's go)

Subject: We got {Tool name} — here's where it is in the queue

Hi {first name or "there"},

Thanks for sending {Tool name}. It's in the free review queue, which runs in arrival order and currently takes 3 to 4 weeks. We check every tool the same way: a named operator, working legal pages, official pricing, and whether it does what its page says.

If you need a decision sooner, the Verified fast lane gets you a written decision within one working day for $79, refunded in full if we decline. It does not change the score. Details: https://aitoolsessentials.com/founders/

Either way, you don't need to resend anything.

— AIToolsEssentials

## Score independence

Neither lane can buy a score, rank, verdict, or badge. The badge is only for accepted tools, paid or free.
