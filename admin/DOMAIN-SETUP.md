# Domain & HTTPS Setup (verified working 2026-08-21)

**Live URL:** https://aitoolsessentials.com

## Current architecture
- Code lives on GitHub: gzikry/aitoolsessentials (deploys to GitHub Pages on push)
- DNS at Porkbun points aitoolsessentials.com at Porkbun's proxy (207.207.210.215)
- The Porkbun proxy forwards requests to GitHub Pages and serves a Let's Encrypt cert
  (valid through Nov 19, 2026, auto-renews)

## Why "Enforce HTTPS" shows off in repo settings
GitHub cannot provision its own cert while the Porkbun proxy terminates TLS first
("The certificate does not exist yet"). This is cosmetic — real visitors get valid
HTTPS end-to-end via the proxy cert.

## If some new URLs 403 on the live domain
Porkbun/pixie-sh (openresty) sits in front of GitHub Pages. It has returned
403 for `/tools/riverside/` and `/categories/Podcast/` even when the files
exist in git. Serve those reviews under unblocked slugs
(`/tools/riverside-fm/`, `/tools/adobe-enhance-speech/`,
`/articles/best-ai-tools-for-podcast-shows.html`, category `Audio Production`)
instead of inventing a proxy bypass.

## If you ever switch DNS directly to GitHub Pages
Point A records to 185.199.108-111.153 and www CNAME to gzikry.github.io,
then wait for cert provisioning and flip Enforce HTTPS.

## Deploy flow
1. python3 scripts/daily_content_update.py   (regenerates + self-cleans)
2. python3 scripts/validate_site.py          (quality gates)
3. git add -A && git commit -m "..." && git push   (auto-deploys)

## Forms
Both /submit-tool.html and /services/intake-questionnaire.html post to FormSubmit,
which emails contact@aitoolsessentials.com. First-ever submission triggers a one-time
activation email — click it once.
