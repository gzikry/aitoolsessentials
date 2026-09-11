# Backlink outreach — September 2026

## Response log

| Date (UTC) | Target | Result | Status |
|---|---|---|---|
| 2026-09-11 | memeburn.com — carl.davis@memeburn.com | Offered paid press releases, partnered articles, and banner placements ($600–$1,200 on MemeBurn; $400–$900 on NFT Plazas/NFT Evening). Replied that AIToolsEssentials is not buying sponsored coverage and was seeking an editorial resource mention only. | Closed — paid only |
| 2026-09-11 | toolscout.ai — contact@toolscout.ai | Asked what AIToolsEssentials would pay for a sponsored feature/resource placement. Replied that no budget is allocated to paid placement and the request was for an editorial mention only. | Closed — paid only |
| 2026-09-11 | stackaible.com — info@stackaible.com | **Hard bounce (550 no such user)** for the Sept 9 keep/cut resource note. The site publishes no email address on `/`, `/about`, `/privacy`, `/terms`, `/system`, or `/newsletter` — operator David Bowers is reachable only via X/YouTube (`@aiorchestration`). No retry: no valid published address. | Closed — unreachable |
| 2026-09-11 | videoupscaler.video — support@videoupscaler.video | **Hard bounce (550 5.1.1 address does not exist)** for the Sept 7 verification request. The address is still printed in the site's own privacy and terms pages, so the vendor's published contact is broken. Domain has MX (Cloudflare Email Routing), so a different address may work. | Blocked — vendor must publish a working address |
| 2026-09-11 | aigearbase.com — contact@aigearbase.com | **Delayed bounce, then confirmed dead end.** Domain has **no MX records at all** (Cloudflare NS `todd`/`jean`; apex A records 172.67.164.102 / 104.21.50.168; port 25 times out). The address is printed on `/contact` only as a Cloudflare-obfuscated `data-cfemail` token that decodes to that same dead address, and the contact form is a JS stub (`alert()` + `reset()`, no fetch, no `/api/contact`, `/contact.php` → 404). No reachable channel exists. Do not retry. | Closed — unreachable |
| 2026-09-11 | aitoolswise.com — contact@aitoolswise.com | **Delayed bounce, then confirmed dead end.** Domain has no MX records at all; apex sends a 308 to `https://aitoolswise.com/`, and HTTPS then fails with a TLS `tlsv1 alert internal error` behind Caddy at 65.108.89.221. The site is only reachable via Google's cache/index. Domain registered 2026-02-08 (Cloudflare NS). Do not retry. | Closed — unreachable |

## Delivery-failure handling notes

- **Corrected sweep (2026-09-11).** The Sept 9 keep/cut batch was **52 sends across 52 distinct domains**. Re-resolving MX for each recipient domain taken from the actual `To:` header found **two** no-MX domains in the September set: `aitoolswise.com` (already closed) and `aigearbase.com` (row above). This supersedes the earlier claim that the September set held "exactly one domain with no MX" — that sweep missed `aigearbase.com`.
- Lesson: MX-check the **exact domain from the `To:` header of every send**, not a curated target list. A recipient added outside the source list is exactly the one an aggregate sweep silently passes while the mail dies.
- Two hard bounces on Sept 11 were for addresses the vendors themselves publish (`support@videoupscaler.video`) or that the outreach list assumed (`info@stackaible.com`). Neither is worth a retry without a working address from the vendor.
- Bounce subjects arrive as `Delivery Status Notification (Delay)` first and `(Failure)` later; a Delay is not actionable on its own — check the referenced `To:` header inside the attached `message/rfc822` block, not the `mailer-daemon` envelope.
- **A Delay is not evidence of a dead end by itself, and a live website is not evidence of a working mailbox.** `aigearbase.com` returns HTTP 200 with a full, polished directory and publishes a contact address; that address's domain has no MX at all and its web form is a non-functional JS stub. Always resolve MX before treating a published contact as reachable.
