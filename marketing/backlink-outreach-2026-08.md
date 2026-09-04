# Directory submission live state (2026-08-31, updated 2026-09-03)

Do not trust "best free AI directories 2026" listicles. Verify the live form before filling anything. Do not pay and do not create third-party accounts without George.

Outreach pack + pitch templates: `site/marketing/backlink-outreach-2026-08.md`.

## Submitted

- **SaaSHub (free queue).** Real form: `https://www.saashub.com/services/submit` — `/submit` is a different product (their 107-directory list). Flow: URL → name/tagline/categories/competitors/email → Free button (not $75 Priority+) → Alpine.js competitor cards (`div.boxed`, click the card not the outbound `<a>`) → category checkboxes → confirmation `https://www.saashub.com/aitoolsessentials/added`. Categories used: AI, AI Tools, Software Directory. Competitors: FutureTools.io, OpenTools, AIToolIntel. Contact: aitoolsessentials@gmail.com. Approval up to 32 days. Claiming/verifying needs a SaaSHub account (George).
- **The Next AI** — SUBMITTED 2026-09-03, approved. Free, no account required. Form: `thenextai.com/submit-ai-tool/`. Fields: Tool Name, Website URL, Category (select), Pricing Model (select), Short Description, Full Description, Logo URL, Email, Tags, math captcha. Dofollow backlink, 120k monthly visitors, dedicated tool page at `/ai-tools/your-tool/`. Review within a few business days.
- **AIAI.Tools** — SUBMITTED 2026-09-03, confirmation shown ("Thanks for contribution"). Free, no account. Tally form embed: `tally.so/r/3NADy0`. Fields: Your Name, Contact Email, Tool Name, Tool URL, Screenshot URL, link-back YES/NO. Uses React native setter workaround (see `references/tally-form-submission-pattern-2026-09-03.md`).

## Paid on the live form (skip unless George approves spend)

- Toolify `/submit` — $99 express only; no free-queue CTA on the 2026-08-31 page
- TopAI.tools `/submit` — $47 Fast Track
- AIXploria submit page — $79 Fast Listing / $279 Verified; FAQ still mentions free, live CTAs are paid
- TAAFT `/launch` — $49+ (held)
- Futurepedia — $247+ (hold until ~5K monthly visits)
- SEOFAI — $29 one-time basic (paid only, no free tier)
- AIToolSync — $29 one-time basic (paid only, no free tier)
- Stork.ai — $49 listing (free only with badge backlink — do not add without George)

## Account-gated (resume after George signs up)

- **AlternativeTo** — "Suggest new application" is in the signed-in user menu; form route `/manage-item/`; needs verified email. `/contribute/` 404s.
- **Uneed** — `https://www.uneed.best/submit-a-tool` preview works without an account (scraped our homepage). Saving requires signup at `/signup?redirectTo=/submit-a-tool`. Resume from that preview after George creates the account.
- **ToolScout** — requires account ("Sign in to continue").

## Attempted 2026-09-03 (blocked or incomplete)

- **AIToolsDirectory.com** — submission form is embedded Paperform (`aitool.paperform.co`). Paperform renders a YES/NO question ("Are you interested in buying ad space on the homepage?") with SPAN elements styled as buttons, not real `<button>` nodes. The AX tree exposes no button roles for them; `fill_input`/`click` by selector fails. Workaround: `click_at_xy` on the SPAN coordinates works, but the page also validates "Please choose an answer" if the click doesn't register as a selection. Status: **incomplete** — needs George to either complete manually or accept the ad-space upsell.
- **PoweredByAI** — category and subcategory fields are React Select components (`react-select-*` IDs). Standard `fill_input` does not open the dropdown or select an option; the hidden `category`/`subcategory` inputs stay empty. Status: **blocked** — React selects need a different automation approach (typing into the input + selecting from the menu portal).
- **Dofollow.Tools** — multi-step form with an "AI auto-fill" button that didn't populate fields after clicking. The AI button has class `bg-indigo-600` but the fetch to extract tool data from the URL silently failed. Status: **incomplete**.
- **Futuretools.io** — submit page 404. Status: **blocked**.

## Pitfalls

- SaaSHub competitor step: `Selected: 0` means you clicked the outbound name link, not the Alpine `div.boxed` card.
- Headless Chrome hits Cloudflare on Toolify; a headed CDP session passed. That is an environment note, not a reason to skip the directory if George later pays.
- **Paperform YES/NO buttons** are SPAN elements, not `<button>` nodes — they don't appear in the AX tree as buttons. Use `click_at_xy` on the SPAN coordinates after `getBoundingClientRect`.
- **React Select components** (PoweredByAI, others) don't respond to `fill_input`. They need: type into the search input → wait for the menu portal to render → click the option by text.
- **AI auto-fill buttons** on directory forms may silently fail (network error, rate limit, JS exception) without surfacing an error. Always verify the expected fields filled after clicking.
- **Tally forms** use React's synthetic event system — `fill_input` sets the DOM value but React doesn't see it. Must use native value setter + dispatch events (see `references/tally-form-submission-pattern-2026-09-03.md`).
- **Neil Patel AI Tools** (aitools.neilpatel.com) — Submit URL redirects to Ubersuggest apps page, not a submission form.
- **Fazier.com** — Free tier requires reciprocal backlink to Fazier on your homepage/footer. Do not add without George.
