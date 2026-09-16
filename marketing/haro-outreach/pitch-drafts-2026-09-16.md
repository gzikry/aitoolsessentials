# Pitch drafts — 2026-09-16

Written for the **best live requests in the queue**, best first. Everything below is
paste-ready and signed AIToolsEssentials. No draft names George.

**None of these has been sent.** Two of the three routes are George's lane (a LinkedIn comment
and a site contact address); one is a plain email the agent could send, but the standing rule
is that outbound pitches are reviewed by George before they go, so nothing was sent.

Every figure quoted below is read off our own verified data, with its check date. Anything not
in `data/tools.json`, `data/pricing_snapshots.json` or `data/tool_sources.json` was cut rather
than estimated.

---

## 1. Amplemarket pricing opacity — marketintelligencetools.com  ◀ the one to send

**Source:** https://www.sourcee.app/journo-request/amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot
**Posted:** 2026-09-06 16:36 UTC — **9 days** (page badge: "Posted 9 days ago")
**Writer:** Jan Suski, who runs marketintelligencetools.com and r/marketinteltools. His own
about page states he tests and prices every tool himself and re-checks each number against its
source. That is the standard to pitch to.
**Ask:** He wants to hear from people who have **signed a Growth or Elite contract**, to see
whether their number landed near Vendr's $16,608/yr tracked median.

**⚠ Honesty constraint — read before sending.** We have **not** signed an Amplemarket Growth or
Elite contract. The draft below does not pretend otherwise; it opens by saying so and offers the
thing we actually have — dated, official-vendor price evidence on list-vs-real gaps. Do not let
this draft drift into a customer testimonial.

**Reply route:** `contact@marketintelligencetools.com` — published on the site's /contact page,
which the request page links to. Domain MX is `mx1/mx2.spacemail.com` (verified live).
He is also reachable via his LinkedIn (linkedin.com/in/jan-suski) and via the original Reddit
thread in r/marketinteltools.
**Automatable?** No. It is a plain email and technically sendable without a human, but pitches
go out reviewed — and this one needs the no-contract disclosure kept intact.

> Subject: On the list-vs-real gap — and no, I haven't signed a Growth contract
>
> Hi Jan,
>
> Straight answer first: I haven't signed an Amplemarket Growth or Elite contract, so I can't add
> to your $16,608 median. I run AIToolsEssentials, where we track verified pricing for 76 AI tools.
>
> - 29 of the 76 publish both a monthly and an annual rate, and monthly costs up to 2.5x annual.
>   Browse AI is widest: $48/month vs $19/month billed annually (checked 2026-09-01). Fathom:
>   $20 vs $16. Fireflies: $18 vs $10. Otter: $16.99 vs $8.33 (checked 2026-08-21).
> - 7 of the 76 publish no paid-tier price at all — no self-serve list, no public pricing page.
>   Harvey, Spellbook, Dragon Copilot and Pika send every buyer to a sales call.
>
> Amplemarket's Growth/Elite gap is a category pattern, not an outlier. The method is mundane: the
> official pricing page, dated, terms quoted verbatim. Happy to send the full dated set — and if
> you land a Growth or Elite number, I'd like to know where it came in.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and
> AI budget visibility. Reply "stop" and I won't follow up again.

**Figures used, and where they come from:** 76 tools (`data/tools.json`, 76 records); 29 of 76
quoting both a monthly and an annual rate and 7 of 76 with no published paid-tier price
(`data/pricing_snapshots.json`, `updated` 2026-09-16); the individual monthly/annual pairs with
their `date` fields (`browse-ai` 2026-09-01; `fathom`, `fireflies`, `otter-ai` 2026-08-21). The
2.5x figure is 48/19 = 2.53x, the widest of the 8 verified pairs. The four named tools' opacity
wording is quoted from `data/tool_sources.json` ("does not publish a self-serve consumer price
list", checked 2026-08-26 for Harvey, Spellbook and Dragon Copilot; 2026-08-28 for Pika).
Verified by `_verify_drafts_0916.py`, which asserts every number in this file.

---

## 2. FinOps — agentic AI cost overruns  ◀ the best-matched request, needs a LinkedIn comment

**Source:** https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
**Posted:** 2026-09-07 14:19 UTC — **9 days** (page badge: "Posted 9 days ago")
**Writer:** an ex-Apptio practitioner who spent years building the cloud-spend tooling behind
Cloudability and now writes that "that playbook doesn't survive contact with agents". The post
is his article "The True Cost of Agentic AI".
**Ask:** "Would like to hear from others how they are managing their AI costs."

**Why it is the best-matched request the monitor has found:** it asks for exactly our subject and
invites a peer answer. It is also 9 days old and has not refreshed — so it is a comment on an
existing thread, not a fresh pitch.

**Reply route:** comment on the original LinkedIn post, or DM the author. The Sourcee page
publishes no email and no link, so this is a **LinkedIn DM/comment — George's lane.**
**Automatable?** No.

**Draft (a comment, or a short DM — keep it comment-length):**

> The half of this bill that is auditable today is the subscription layer sitting next to the
> agents.
>
> We track verified pricing for 76 AI tools and audit overlapping subscriptions. 70 of the 76 sit
> in the 13 categories holding three or more tools — and the overlap is a *category* problem, not
> a function problem. Three meeting notetakers bought separately by three teams, each of whom
> thought they were the only one:
>
> - Fathom Premium: $20/user/month monthly, $16 annual (checked 2026-08-21)
> - Fireflies Pro: $18/seat/month monthly, $10 annual (checked 2026-08-21)
> - Otter Pro: $16.99/user/month monthly, $8.33 annual (checked 2026-08-21)
>
> Token spend genuinely resists forecasting. Seats do not — you can enumerate and cancel them
> this week. In most audits the two cancelled seats fund a meaningful slice of the agent budget
> that shocked everyone, and no one had to model a single token to find it.
>
> Agreed that the cost-visibility question has moved. The part I'd add: the seat layer is where
> the answer is already sitting.

**Figures used:** 76 tools and the 13 categories holding 3+ / 70 tools (`data/tools.json`, 13
categories of 16 hold ≥3); the three notetaker prices with check dates and the Meetings category
membership Fathom / Fireflies.ai / Otter.ai (`data/pricing_snapshots.json`, keys `fathom`,
`fireflies`, `otter-ai`, all `date` 2026-08-21).

---

## 3. Enterprise AI governance & agent sprawl

**Source:** https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
**Posted:** 2026-09-05 07:46 UTC — **11 days** (page badge: "Posted 11 days ago")
**Ask:** "Are you confident you know what your AI agents are doing and consuming?" — he wants
comments to shape an article on AI governance architecture, agent ecosystems and model economics.
**Assessment: cold.** 11 days with no refresh across four digest appearances, and the author is
already writing the piece. Worth a comment only, and only if you want the enterprise framing on
the record.

**Reply route:** comment on the original LinkedIn post. **George's lane.** Not automatable.

**Draft (comment):**

> The governance question has a floor that most audits never reach: before you can govern what
> agents consume, you have to know what the seats cost.
>
> We track verified pricing for 76 AI tools and audit overlapping subscriptions. 70 sit in the 13
> categories holding three or more tools, and 7 of the 76 publish no price for the paid tier at
> all — every buyer routes through a sales conversation. So "what are we consuming and what does
> it cost" is unanswerable at the tools layer long before it is unanswerable at the agents layer.
>
> The pattern that recurs: overlap is not duplicate function, it is duplicate category. Three
> meeting notetakers, bought by three teams who never compared notes. No one owns the decision,
> so no one benefits from cutting it.
>
> Worth saying plainly in the piece — governance fails on the invoice before it fails on the
> architecture.

**Figures used:** 76 tools, 13 categories holding 3+ / 70 tools (`data/tools.json`); 7 of 76 with
no published paid-tier price (`data/pricing_snapshots.json`, `updated` 2026-09-16).

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| California AI audit bills → CIOs (Industry Dive, 6d) | Its own stated deadline — "speak with a source today" — passed on 2026-09-12. |
| UK managers / Gen Z AI overuse (9d) | Internal deadline ("by the end of the week" / "by this Wednesday September 9") has passed. Contact redacted. |
| Inc. — U.S. Founders, calls to slow AI development (0d) | Freshest in-feed request of the run, but it wants US founders' firsthand safety-guardrail accounts. We are a pricing publisher. Wrong standing. |
| Cybersecurity companies & AI scams (0d) | A PR firm building a spokesperson roster. Not a journalist request; wants cybersecurity vendors. |
| Ukraine tech builders (0d) | Asks what Ukraine's commercial-tech adaptation teaches other businesses. Not our beat. |
| Scientists paying for AI subscriptions (Science Magazine, 11d) | Wants scientists. Cold. |
| CEOs — AI impact on ops (13d) | Wants ten CEOs for a book. We are not CEOs. Cold. |
| AI startups — workplace fraud detection (9d) | Its "expenses" hook is employee expense fraud, not software spend; contact redacted. |
| Amplemarket Growth/Elite — *as a customer* | We have not signed one. Covered honestly in draft 1 instead. |

---

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake (`hermes mcp add --auth oauth`)
that cannot be completed from a scheduled run. It is a free read-only feed covering Connectively,
HARO, X, LinkedIn, MentionMatch and Substack — six platforms in one step. Until that handshake
happens, this monitor's only accessible source is Sourcee, whose on-beat supply has now been
thin for four consecutive runs.
