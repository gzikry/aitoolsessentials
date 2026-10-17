# DNS for news.aitoolsessentials.com

Keep/Cut Weekly sends from `news.aitoolsessentials.com` through Resend. The sending domain is verified. Sending stays off until `NEWSLETTER_SEND_ENABLED` is true, the issue has an approval file, and `scripts/send_keep_cut.py` has `RESEND_API_KEY` plus `RESEND_SEGMENT_ID`. Signup hosting is separate and is described in `docs/newsletter-subscribe.md`.

The previous list had no subscribers, so there is no export.

Resend supplies the live record values. The names below are placeholders. Do not publish guessed includes, selectors, or mail hosts.

| Purpose | Type | Host | Value |
| --- | --- | --- | --- |
| SPF | TXT | `news.aitoolsessentials.com` | `v=spf1 include:RESEND_SPF_INCLUDE -all` |
| DKIM | TXT or CNAME, whichever Resend shows | `RESEND_DKIM_SELECTOR._domainkey.news.aitoolsessentials.com` | `RESEND_DKIM_VALUE` |
| DMARC | TXT | `_dmarc.news.aitoolsessentials.com` | `v=DMARC1; p=none; rua=mailto:aitoolsessentials@gmail.com` |
| Return-path MX | MX | `news.aitoolsessentials.com` | `10 RESEND_RETURN_PATH_MX` |
| Return-path check | TXT | the host Resend names | `RESEND_RETURN_PATH_TXT` |

The From address is `weekly@news.aitoolsessentials.com`.

Every draft carries the postal address `1090 West Foothill, Claremont, CA 91711` and an unsubscribe link. `/subscribe/` posts to the workers.dev URL in `subscribe_endpoint`. See `docs/newsletter-subscribe.md`. A broadcast replaces the mailto unsubscribe with `{{{RESEND_UNSUBSCRIBE_URL}}}`.
