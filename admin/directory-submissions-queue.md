# Directory submission queue — free + do-follow targets

Source: **SaaSHub Submit**, the free distribution tool unlocked when SaaSHub approved the
AIToolsEssentials listing (2026-09-28). Reachable only from the token-login links in
SaaSHub's mail — `https://www.saashub.com/manage/aitoolsessentials/submit`.

Columns are SaaSHub's own: **Pop** (popularity score), **Traffic** (monthly), **DS**
(average of Moz DA and Ahrefs DR), **Follow** (do-follow), **Free**.

## Rules carried from site policy

- **Free and do-follow only.** Paid queue jumps and "fast track" tiers are declined —
  same answer already given to MemeBurn, ToolScout, techsy.io, zplatform.ai and SaaSHub
  Priority+ ($75).
- **No account creation by the agent.** Any target whose `Registration` is Yes is
  George-only (third-party signups are his lane). Do not accept credential-bearing work.
- **Record a listing only after a fetched 200 with the link visible.** A directory's own
  "approved" email is not a backlink — one prior cycle counted a listing that had never
  been live.

## Tier 1 — free, do-follow, no registration (agent-executable)

| Target | Traffic | DS | Submit URL | Status |
|---|---|---|---|---|
| AI to Grow | 200 | 14 | https://aitogrow.com/#send-your-tool | **SUBMITTED 2026-09-28** |

**AI to Grow — submitted 2026-09-28.** The form is a plain WordPress Contact Form 7
(`form.wpcf7-form`, fields `your-name` / `email` / `url` / `textarea`, native AJAX to
`/wp-json/contact-form-7/v1/contact-forms/274/feedback`). No login gate, confirmed
empirically before sending. Submitted as AIToolsEssentials with the site's published
contact address and a factual description; the form returned "Thank you for your
message. It has been sent." **The listing is not confirmed until a fetched public page
shows the site link** — re-check the directory's listing pages, not the form's notice.

> Caution: the same page also carries a SendFox newsletter form that requires a password
> (`sendfox.com/form/...`). That is not a submission form — do not fill or submit it.

## Tier 2 — free + do-follow, registration required (George-gated)

Highest-reach first. These are worth George's time; the agent should not sign up.

| Target | Traffic | DS | Submit URL |
|---|---|---|---|
| FutureTools.io | 602 K | 49 | https://futuretools.io/submit-a-tool |
| TOOOLS.design | 185 K | 32 | https://www.toools.design |
| StartupInspire | 11.7 K | 30 | https://www.startupinspire.com/ |
| AppRater | 11.3 K | 15 | https://apprater.net/ |
| AI Agents Directory | 6.5 K | 26 | https://aiagentsdirectory.com/ |
| Startup Fame | 5.2 K | 49 | https://startupfa.me/ |
| Hrefgo | 5 K | 23 | https://hrefgo.com/submit |
| Awesome Indie | 4.1 K | 15 | https://awesomeindie.com |
| Nick Launches | 3 K | 48 | https://nicklaunches.com/ |
| Theres An AI | 1.5 K | 9 | https://theresanai.com |
| Tool Summary | 100 | 3 | https://toolsummary.com/submit-ai-tool |
| LunarList | 50 | 37 | https://www.lunarlist.ai/list-your-tool |
| PeerPush | — | 47 | https://peerpush.net/ |
| LaunchBoard.dev | — | 8 | https://launchboard.dev/ |
| e-SideHustles | 0 | 12 | https://esidehustles.com/submit-a-resource/ |
| CyberSecTools | 0 | 11 | https://cybersectools.com |
| GrowthBoosters.com | 0 | 10 | https://growthboosters.com/product/add |

**Note on FutureTools.io:** a 2026-08 outreach pass logged its submit page as a 404
("blocked"). SaaSHub now lists `/submit-a-tool` as the live submit path. Re-check before
declaring it dead again — the earlier verdict may have been a stale path.

## Already handled

- **SaaSHub** — approved 2026-09-28. Listing completed and verified 2026-09-27 (features,
  platforms, screenshots, description count, Verify click). Do not re-submit or email.

## Copy assets

SaaSHub holds the submission kit (logo URL, name, tagline, description, image URLs) on any
`/manage/aitoolsessentials/submit/<target>` detail page under "YOUR PRODUCT". Pull from
there rather than rewriting positioning per directory.

Tagline in use:
> Independently verified AI tool reviews, comparisons and weekly pricing snapshots. No pay-to-rank listings.

## Verification recipe

After a submission, fetch the public listing and assert the site link is present. Do not
count the submission until it returns a 200 with the link visible in the rendered page.
