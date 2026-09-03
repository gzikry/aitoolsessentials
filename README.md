# AIToolsEssentials

Evidence-aware AI tool reviews, comparisons, buyer guides, benchmark context, and strategy-only AI Stack Audits.

**Live:** https://aitoolsessentials.com  
**Repository:** https://github.com/gzikry/aitoolsessentials

## Current site

- 39 generated tool reviews
- 15 generated category buyer guides
- Comparison and audience guides
- Dated benchmark evidence hub
- Free AI Tool Evaluation Scorecard
- Honest community/editorial shortlist (no simulated votes or traffic)
- Vendor submission form
- AI Stack Audit intake and report workflow
- Premium pricing page staged for Whop plan activation

## Editorial rules

- AIToolsEssentials ratings are editorial product scores—not lab benchmarks.
- External benchmark records retain exact model/version, date, harness, source, and caveat.
- A product never inherits a score from an unspecified model.
- Affiliate availability, commission rate, and sponsorship do not affect rankings.
- No hands-on claim is published without a retained test log and evidence.
- Unverified traffic, vote, submission, or performance numbers are not published.

## Source of truth

- `data/tools.json` — tool records and review content
- `data/benchmarks.json` — benchmark sources, snapshots, coverage, and unavailable disclosures
- `data/affiliate_programs.json` — verified application status only; no invented tracking links
- `scripts/generate_reviews.py` — review generator
- `scripts/generate_categories.py` — category generator
- `scripts/generate_benchmarks.py` — benchmark hub generator
- `scripts/generate_community.py` — honest community/editorial shortlist
- `scripts/daily_content_update.py` — complete regeneration pipeline
- `scripts/validate_site.py` — quality gates

## Local workflow

```bash
python3 scripts/daily_content_update.py
python3 scripts/validate_site.py
git add -A
git commit -m "Describe the verified change"
git push
```

GitHub Pages deploys from `main`. The Porkbun proxy serves the custom domain and TLS certificate.

## Review evidence

Every review separates:

1. Official product/pricing/policy sources
2. External benchmark evidence, when exact versions match
3. Editorial product assessment
4. Hands-on evidence status and repeatable trial checklist

See:

- `/legal/editorial-methodology.html`
- `/legal/testing-protocol.html`
- `/benchmarks/`
- `/legal/corrections.html`

## Revenue model

Priorities:

1. Approved affiliate links—official product links remain until approval
2. AI Stack Audit strategy reports; no implementation or account access
3. Clearly labeled sponsored placements that never alter rankings
4. Whop Premium membership after the live plan ID is supplied

Keep/Cut Weekly is the free Beehiiv newsletter (`/subscribe/`). Premium is a separate $12/month Whop membership. Do not wire FormSubmit to the newsletter.

## Security

Never commit credentials, tokens, FTP passwords, or payment secrets. Obsolete FTP deployment code was removed and purged from Git history. The formerly exposed Porkbun FTP password must be rotated in Porkbun.
