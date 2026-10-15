# DNS for news.aitoolsessentials.com

Keep/Cut Weekly sends from `news.aitoolsessentials.com` through Resend. Sending is off. `NEWSLETTER_SEND_ENABLED` defaults to false. Turning it on still does not send: each issue needs an operator approval, and the code has no transport. Nothing leaves on its own.

The previous list had no subscribers, so there is no export.

Resend supplies the live record values. The names below are placeholders. Do not publish guessed includes, selectors, or mail hosts.

| Purpose | Type | Host | Value |
| --- | --- | --- | --- |
| SPF | TXT | `news.aitoolsessentials.com` | `v=spf1 include:RESEND_SPF_INCLUDE -all` |
| DKIM | TXT or CNAME, whichever Resend shows | `RESEND_DKIM_SELECTOR._domainkey.news.aitoolsessentials.com` | `RESEND_DKIM_VALUE` |
| DMARC | TXT | `_dmarc.news.aitoolsessentials.com` | `v=DMARC1; p=none; rua=mailto:aitoolsessentials@gmail.com` |
| Return-path MX | MX | `news.aitoolsessentials.com` | `10 RESEND_RETURN_PATH_MX` |
| Return-path check | TXT | the host Resend names | `RESEND_RETURN_PATH_TXT` |

The From address is `RESEND_FROM_LOCAL@news.aitoolsessentials.com`.

Every draft carries the postal address `1090 West Foothill, Claremont, CA 91711` and a mailto unsubscribe link. The subscribe form at `/subscribe/` stays disabled, says the list is launching soon, and describes double opt-in without sending a confirm message.
