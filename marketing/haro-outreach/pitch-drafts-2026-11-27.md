# Pitch queue — 2026-11-27

Two live, routable requests. **Neither pitch has been sent.** Sourcee request pages were fetched today (HTTP 200, “Posted in last 7 days”); addresses were re-probed on the publications' or reporters' own pages in `route-checks-2026-11-27.json`. Send is George's lane. The Sourcee AI topic browse feed omits both; its rolling membership does not prove either request expired.

## 1. Personnel Today — Jo Faragher (send first)

**Source:** https://www.sourcee.app/journo-request/hr-professionals-ai-hiring-economics-and-workforce-planning
**Page age:** 4 days (datePublished 2026-11-23; badge “Posted in last 7 days”).
**Exact reply route:** `jo.faragher@personneltoday.com` — the Personnel Today editorial contact page `https://www.personneltoday.com/contact-us/` names Jo Faragher and publishes this address; route HTTP 200 re-probed 2026-11-27. **Automatable: no; George sends.**

**Subject:** The seat-price numbers behind your AI-versus-hiring question

> Hi Jo —
>
> GitHub Copilot Pro lists $10/month with 1,500 monthly AI credits (vendor pricing captured 2026-11-14). That is one concrete seat-and-usage example for your question about AI cost versus employing people and token caps.
>
> In our vendor-page price snapshots, 54 of 139 tracked AI tools publish a monthly price; 44 of those have a price at or below $25/month. The median cheapest paid monthly price in that subset is $15 (snapshot updated 2026-11-27). Those are listed prices, not measured enterprise spend, employment substitution or ROI. Token caps and seat costs should be budgeted separately: Bolt's free plan lists a 300,000-token daily limit (checked 2026-10-25).
>
> I can share the vendor URLs and check dates behind each figure if useful for your workforce-planning piece. We are not an HR employer case study, but can supply the price evidence.
>
> AIToolsEssentials

## 2. Telegraph Money — Katie Strick

**Source:** https://www.sourcee.app/journo-request/brits-using-ai-subscription-spend-vs-annual-savings-and-earnings
**Page age:** 3 days (datePublished 2026-11-24; badge “Posted in last 7 days”).
**Exact reply route:** `katiestrickwrites@gmail.com` — published on the reporter's own `https://katiestrick.co.uk/contact/` (HTTP 200, re-probed 2026-11-27); Sourcee redacts the request's email. **Automatable: no; George sends.**

**Subject:** Listed AI subscription costs for your Telegraph Money case studies

> Hi Katie —
>
> ChatGPT Plus and Claude Pro each list $20/month on month-to-month billing (vendor pages checked 2026-11-14). A reader paying for both therefore has two separate subscriptions to account for before calculating whether either saves or earns them money.
>
> Our vendor-page snapshots cover 1140 AI tools; 54 publish a monthly price, and the median cheapest paid monthly price among those 54 is $15 (snapshot updated 2026-11-27). These are US-dollar listed prices, not UK bank-statement spending, exchange-rate-adjusted costs or evidence of personal returns. We can share the underlying vendor URLs and check dates for your pricing context.
>
> Your request calls for British subscribers with first-hand savings or earnings stories. We cannot supply one and would not represent ourselves as one; this is background price evidence only, if useful alongside your interviews.
>
> AIToolsEssentials

**Data provenance:** `data/pricing_snapshots.json` (`updated: 2026-11-27`; individual vendor check dates above) and `data/tools.json`. The subset counts and median are recomputed from the snapshot digests by `scripts/build_digest.py` and `scripts/build_pitch_queue.py`; no invented participant outcomes. Each draft is below 200 words.
