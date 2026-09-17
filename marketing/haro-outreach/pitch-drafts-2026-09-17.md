# Pitch drafts — 2026-09-17

Written for the **best live requests in the queue**. Everything below is paste-ready, signed
AIToolsEssentials, and under 200 words. No draft names George.

**None of these has been sent.** Every route in this file is George's lane: a LinkedIn DM, a
published email, and a published Signal handle. Nothing was sent by the agent.

Every figure quoted is read off our own verified data with its check date. Anything not in
`data/tools.json`, `data/pricing_snapshots.json` or `data/tool_sources.json` was cut rather than
estimated. `_verify_drafts_0917.py` asserts every number in this file.

**Why these three.** The queue's top two by rank are both `high` relevance and both still live:
FinOps/agentic cost and the Amplemarket list-vs-real request. Third slot goes to the Anthropic
subscription-value request (`medium-high`, 5 days) rather than the queue's rank-3
founder-profile post, because it carries the strongest *actionable* route in the whole queue —
a Signal handle published verbatim on the request — and this monitor's entire failure mode is
finds that never become sends. Rank-3 and below remain in `pitch-queue.md`.

---

## 1. FinOps — agentic AI cost overruns ◀ the one to send first

**Source:** https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
**Posted:** 2026-09-07 14:19 UTC — **10 days** (page badge: "Posted 10 days ago")
**Who:** named in the page's own author field this run — **Niloy Ghosh**, AI & Data Science
Leader, ex-IBM/Apptio, Citi, Flipkart. His LinkedIn profile matches the request text exactly
("Ex-IBM/Apptio", "The True Cost of Agentic AI"). His post is the one that says the Cloudability
playbook "doesn't survive contact with agents".
**Ask:** "Would like to hear from others how they are managing their AI costs."

**Why it is the best live request:** it asks the question this monitor exists for, and it invites
a peer answer rather than a customer testimonial. 10 days with four digest appearances and no
refresh — the window is closing, so send or drop it.

**Reply route:** LinkedIn DM or comment to `linkedin.com/in/niloy-ghosh`. The Sourcee page
publishes no email. **George's lane. Not automatable.**

> Hi Niloy,
>
> Your line about the Apptio playbook not surviving contact with agents is the right frame. The
> half of that bill which is auditable today is the seat subscriptions renewing next to the agents.
>
> We track verified pricing for 76 AI tools. 70 of the 76 sit in the 13 categories holding three
> or more — so overlap is a category problem, not a function problem. Three meeting notetakers,
> bought separately by three teams who each thought they were the only one:
>
> - Fathom Premium: $20/user/month monthly, $16 annual (checked 2026-08-21)
> - Fireflies Pro: $18/seat/month monthly, $10 annual (checked 2026-08-21)
> - Otter Pro: $16.99/user/month monthly, $8.33 annual (checked 2026-08-21)
>
> Token spend genuinely resists forecasting. Seats don't — you can enumerate and cancel them this
> week. In most audits the two cancelled seats fund a visible slice of the agent budget that
> shocked everyone, and nobody had to model a token to find it.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures used, and where they come from:** 76 tools (`data/tools.json`, 76 records); 13
categories holding ≥3 tools = 70 tools (`data/tools.json`, computed); the three notetaker
monthly/annual pairs with their `date` fields (`data/pricing_snapshots.json` keys `fathom`,
`fireflies`, `otter-ai`, all `date` 2026-08-21); those three are the entire `Meetings` category.

---

## 2. Amplemarket list-vs-real pricing ◀ the only verified email route in the queue

**Source:** https://www.sourcee.app/journo-request/amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot
**Posted:** 2026-09-06 16:36 UTC — **10 days** (page badge: "Posted 10 days ago")
**Who:** Jan Suski, who publishes marketintelligencetools.com and runs r/marketinteltools. His own
about page states he re-checks every number against its source. Pitch to that standard.
**Ask:** he wants to hear from anyone who has **signed a Growth or Elite contract**, to compare
against Vendr's $16,608/yr tracked median.

**⚠ Honesty constraint — read before sending.** We have **not** signed an Amplemarket Growth or
Elite contract. The draft opens by saying so. Do not let it drift into a customer testimonial.

**Reply route:** `contact@marketintelligencetools.com` — published on the site's /contact page,
re-verified live this run (root HTTP 200; MX `mx1/mx2.spacemail.com`). Also reachable via his
LinkedIn (`linkedin.com/in/jan-suski`) and the original Reddit thread.
**Automatable?** No — it is a plain email, but pitches go out reviewed, and this one needs the
no-contract disclosure kept intact.

> Subject: On the list-vs-real gap — and no, I haven't signed a Growth contract
>
> Hi Jan,
>
> Straight answer first: I haven't signed an Amplemarket Growth or Elite contract, so I can't add to
> your $16,608 median. I run AIToolsEssentials, where we track verified pricing for 76 AI tools.
>
> - 29 of the 76 publish both a monthly and an annual rate, and paying monthly costs up to 2.5x
>   annual. Browse AI is widest: $48/month vs $19/month billed annually (checked 2026-09-01).
>   Fathom: $20 vs $16. Fireflies: $18 vs $10. Otter: $16.99 vs $8.33 (checked 2026-08-21).
> - 7 of the 76 publish no price for the paid tier at all — no self-serve list, no public pricing
>   page. Harvey, Spellbook, Dragon Copilot and Pika route every buyer to a sales conversation.
>
> Amplemarket's Growth/Elite gap is a category pattern, not an outlier. The method is mundane: the
> official pricing page, dated, terms quoted verbatim. Happy to send the full dated set — and if you
> land a Growth or Elite number, I'd like to know where it came in.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures used:** 76 tools (`data/tools.json`); 29 of 76 quoting both monthly and annual and 7 of
76 with an unpublished paid-tier price (`data/pricing_snapshots.json`, `updated` 2026-09-17); the
four price pairs with their `date` fields (`browse-ai` 2026-09-01; `fathom`, `fireflies`,
`otter-ai` 2026-08-21); 2.5x is 48/19 = 2.53x, the widest of the verified pairs; the opacity
wording for Harvey, Spellbook and Dragon Copilot is quoted from their snapshots (all checked
2026-08-26) and Pika's (2026-08-28).

---

## 3. Anthropic subscription value — price vs support ◀ the strongest published route

**Source:** https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
**Posted:** 2026-09-11 16:58 UTC — **5 days** (page badge: "Posted in last 7 days")
**Who:** **Helen Li** — named in the page's own author field this run (previously not captured).
**Ask:** "I am writing a story about the difficulties that people have had with Anthropic customer
service... I'd love to chat via DMs, email, or Signal hliwrites.99"

**Fit:** on-beat as a subscription-value story, not as a grievance. We hold dated official Anthropic
pricing and no complaint of our own, so the draft leads on the price side and offers the pricing
evidence only. It does not claim we had a support failure.

**Reply route:** **Signal `hliwrites.99`** — published verbatim in the request, the only concrete
handle on any page in this queue. DMs and email are also invited; the address is redacted on
Sourcee. **George's lane. Not automatable.**

> Signal/DM —
>
> Your story is a value story, not a service one, and there's a number under it. Claude's own
> published tiers run from $17/month (Pro, with the $200 annual prepayment; $20 month-to-month) to
> $100+/month for Max, and Team lists $20/seat/month Standard up to $100/seat/month Premium
> (checked 2026-08-21; team seat figures re-checked 2026-08-25). At the top of that range a buyer is
> paying five figures a year per seat and the support channel is unchanged.
>
> I don't have a support failure to give you — I'd be inventing standing I don't have. What I can
> give you is the pricing side, dated and sourced to Anthropic's own pages, plus the same map for
> the other assistants if it helps you draw the comparison.
>
> The useful question for your piece may be the one buyers ask last: what exactly does the top tier
> buy, if the support path is the same at $20 and at $100?
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures used:** Claude Pro $17/month with $200 annual prepayment or $20 month-to-month; Max from
$100/month; Team Standard $20/seat/month, Premium $100/seat/month (`data/pricing_snapshots.json`
key `claude`, `date` 2026-08-21; same figures in `data/tool_sources.json` slug `claude`,
`pricing_checked_date` 2026-08-25). The "$100+" and "five figures a year per seat" are arithmetic
on those figures at the $100/seat/month Premium tier, not a separately published number.

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| E-Discovery AI-assisted review (Mass Lawyers Weekly, 0d) | Freshest item in the feed, but wants practising e-discovery lawyers. We are a pricing publisher. Wrong standing. |
| U.S. Founders — calls to slow AI development (Inc., 1d, Aaron Mok) | Wants founders' firsthand safety-guardrail accounts. Wrong standing. |
| Cybersecurity companies & AI scams (1d, Sandra Torres) | A PR firm building a spokesperson roster, not a journalist request. Off-beat. |
| Gen Z AI data annotators (Fortune, 1d) | Wants annotators describing their own work and pay. No standing. |
| AI Automation Experts — speaking slots (1d) | A speaking-slot solicitation. Off-beat. |
| Ecommerce marketers — AI recommendation transparency (MarketingSherpa, 1d) | Wants AEO case studies we do not have. Off-beat. |
| California AI audit bills → CIOs (Industry Dive, Paige Gross, 7d) | Its own stated deadline — "speak with a source today" — passed 2026-09-12. |
| UK managers / Gen Z AI overuse (MaryLou Costa, 10d) | Internal deadline ("by this Wednesday September 9") passed eight days ago. |
| Early-stage founders — Built From Scratch (6d) | Queue rank 3, and the best of the remaining. Left in `pitch-queue.md` rather than drafted — it is a founder-profile post, so it earns standing and no citation. |
| Individual contributors managing AI agents (Rani Molla, Sherwood, 7d) | Reachable route now resolved (Rani@Sherwood.news, Signal ranimolla.01, both published by her publication), but the story is unacknowledged management load, not spend. Adjacent. |
| Amplemarket Growth/Elite — *as a customer* | We have not signed one. Covered honestly in draft 2. |

---

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake (`hermes mcp add --auth oauth`)
that cannot be completed from a scheduled run. It is a free read-only feed covering Connectively,
HARO, X, LinkedIn, MentionMatch and Substack — six platforms in one step, and the only path to
fixing a monitor whose sole accessible source has now produced no new core-beat request for five
consecutive runs. Endpoint re-confirmed live this run (HTTP 401, `invalid_token`), and
`hermes mcp list` reports no MCP servers configured.
