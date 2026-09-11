# Backlink outreach — September 2026

## Response log

| Date (UTC) | Target | Result | Status |
|---|---|---|---|
| 2026-09-11 | memeburn.com — carl.davis@memeburn.com | Offered paid press releases, partnered articles, and banner placements ($600–$1,200 on MemeBurn; $400–$900 on NFT Plazas/NFT Evening). Replied that AIToolsEssentials is not buying sponsored coverage and was seeking an editorial resource mention only. | Closed — paid only |
| 2026-09-11 | toolscout.ai — contact@toolscout.ai | Asked what AIToolsEssentials would pay for a sponsored feature/resource placement. Replied that no budget is allocated to paid placement and the request was for an editorial mention only. | Closed — paid only |
| 2026-09-11 | stackaible.com — info@stackaible.com | **Hard bounce (550 no such user)** for the Sept 9 keep/cut resource note. The site publishes no email address on `/`, `/about`, `/privacy`, `/terms`, `/system`, or `/newsletter` — operator David Bowers is reachable only via X/YouTube (`@aiorchestration`). No retry: no valid published address. | Closed — unreachable |
| 2026-09-11 | videoupscaler.video — support@videoupscaler.video | **Hard bounce (550 5.1.1 address does not exist)** for the Sept 7 verification request. The address is still printed in the site's own privacy and terms pages, so the vendor's published contact is broken. Domain has MX (Cloudflare Email Routing), so a different address may work. | Blocked — vendor must publish a working address |
| 2026-09-11 | aitoolswise.com — contact@aitoolswise.com | **Delayed bounce, then confirmed dead end.** Domain has no MX records at all; apex sends a 308 to `https://aitoolswise.com/`, and HTTPS then fails with a TLS `tlsv1 alert internal error` behind Caddy at 65.108.89.221. The site is only reachable via Google's cache/index. Domain registered 2026-02-08 (Cloudflare NS). Do not retry. | Closed — unreachable |

## Delivery-failure handling notes

- An hourly sweep of every September outreach and verification recipient (58 sends, 51 domains) found exactly one domain with no MX at all (`aitoolswise.com`); the other 50 resolve.
- Two hard bounces on Sept 11 were for addresses the vendors themselves publish (`support@videoupscaler.video`) or that the outreach list assumed (`info@stackaible.com`). Neither is worth a retry without a working address from the vendor.
- Bounce subjects arrive as `Delivery Status Notification (Delay)` first and `(Failure)` later; a Delay is not actionable on its own — check the referenced `To:` header inside the attached `message/rfc822` block, not the `mailer-daemon` envelope.
