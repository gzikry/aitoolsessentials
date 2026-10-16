# How to collect and send Keep/Cut Weekly

The site on GitHub Pages cannot hide an API key. DNS for `aitoolsessentials.com` is at Porkbun, so a Worker custom domain on `subscribe.news.aitoolsessentials.com` is not available. The form action is the single field `subscribe_endpoint` in `data/newsletter.json`. Leave it as `""` and `/subscribe/` says signups open soon and links `aitoolsessentials@gmail.com`. It does not post.

A non-empty value is used only when it is an `https` URL on `*.workers.dev`. That is the URL Wrangler assigns at deploy. Any other value, including the Porkbun hostname, is treated as closed.

## Deploy the Worker

You need a Resend segment for Keep/Cut Weekly and an API key that can write contacts and send from `news.aitoolsessentials.com`.

From `workers/newsletter-subscribe/`:

```
npx wrangler secret put RESEND_API_KEY
npx wrangler secret put RESEND_SEGMENT_ID
npx wrangler secret put CONFIRM_SECRET
npx wrangler deploy
```

`wrangler deploy` prints a URL like `https://aitools-newsletter-subscribe.<account>.workers.dev`. Copy that exact URL into `subscribe_endpoint`, then commit the JSON. The subscribe page form posts there. Confirm links use the same origin, so they keep working on workers.dev.

`RESEND_API_KEY`, `RESEND_SEGMENT_ID`, and `CONFIRM_SECRET` are Wrangler secrets. They do not go in the repo.

A signup creates the contact with `unsubscribed` set to true, adds that contact to the segment, and emails an HMAC confirm link that expires in 48 hours. The confirm request sets `unsubscribed` to false. Resend broadcasts skip contacts that are still unsubscribed.

The honeypot field is `company_website`. A value in that field gets the same check-your-email page and does not call Resend. The Worker also keeps one signup per IP per minute in the Cache API.

## Send one issue

`NEWSLETTER_SEND_ENABLED` defaults to off. An approved issue still does not send without the key and the segment id.

1. Write `admin/newsletter/<slug>.approved` so the only text is `approved`. That file is gitignored.
2. Export `RESEND_API_KEY` and `RESEND_SEGMENT_ID`.
3. Export `NEWSLETTER_SEND_ENABLED=true`.
4. Run `python3 scripts/send_keep_cut.py <slug>`.

The script posts one Resend broadcast with `send` set to true. The From address is `Keep/Cut Weekly <weekly@news.aitoolsessentials.com>`. The HTML keeps the postal address `1090 West Foothill, Claremont, CA 91711`, the brand sign-off, and `{{{RESEND_UNSUBSCRIBE_URL}}}`. It refuses a draft that contains a personal name, and it does not call Resend when the flag is off or the approval file is missing.
