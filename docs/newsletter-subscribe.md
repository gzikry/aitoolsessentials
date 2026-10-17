# How to collect and send Keep/Cut Weekly

The site on GitHub Pages cannot hide an API key. DNS for `aitoolsessentials.com` is at Porkbun, so a Worker custom domain on `subscribe.news.aitoolsessentials.com` is not available. The form action is the single field `subscribe_endpoint` in `data/newsletter.json`.

The committed value is `https://aitools-newsletter-subscribe.aitoolsessentials.workers.dev`. `/subscribe/` and the homepage subscribe panel post there. An empty value, or any URL that is not `https` on `*.workers.dev`, still says signups open soon and links `aitoolsessentials@gmail.com`. It does not post. The Porkbun hostname is one of those closed values.

## Deploy the Worker

You need a Resend segment for Keep/Cut Weekly and an API key that can write contacts and send from `news.aitoolsessentials.com`.

From `workers/newsletter-subscribe/`:

```
npx wrangler secret put RESEND_API_KEY
npx wrangler secret put RESEND_SEGMENT_ID
npx wrangler secret put CONFIRM_SECRET
npx wrangler deploy
```

`wrangler deploy` prints the workers.dev URL. The committed `subscribe_endpoint` is already that URL. Confirm links use the same origin, so they keep working on workers.dev. This repo does not run `wrangler deploy`. Redeploy from the operator box after you change `worker.js` or `wrangler.toml`.

`RESEND_API_KEY`, `RESEND_SEGMENT_ID`, and `CONFIRM_SECRET` are Wrangler secrets. They do not go in the repo.

A signup creates the contact with `unsubscribed` set to true, adds that contact to the segment, and emails an HMAC confirm link that expires in 48 hours. The confirm request sets `unsubscribed` to false. Resend broadcasts skip contacts that are still unsubscribed.

The honeypot field is `company_website`. A value in that field gets the same check-your-email page and does not call Resend.

## Rate limit

The Worker calls the binding `SIGNUP_LIMIT`. `wrangler.toml` sets `namespace_id` to `847210`, `limit` to 1, and `period` to 60. The key is the `cf-connecting-ip` header. `limit({ key })` returns `{ success: false }` when that key is over the budget, and the Worker answers with the slow-down page. A missing binding, or a throw from `limit`, is treated as limited. A deploy without the binding does not accept unlimited signups.

The Cache API does not persist on `workers.dev`, so the old `caches.default` counter never held. The binding is the replacement. The budget is per Cloudflare location, not one global counter. `namespace_id` must be unique in the Cloudflare account. Change `847210` before you redeploy if that account already uses it. Reusing an id shares the budget with the other Worker that owns it.

## Send one issue

`NEWSLETTER_SEND_ENABLED` defaults to off. An approved issue still does not send without the key and the segment id.

1. Write `admin/newsletter/<slug>.approved` so the only text is `approved`. That file is gitignored.
2. Export `RESEND_API_KEY` and `RESEND_SEGMENT_ID`.
3. Export `NEWSLETTER_SEND_ENABLED=true`.
4. Run `python3 scripts/send_keep_cut.py <slug>`.

The script posts one Resend broadcast with `send` set to true. The From address is `Keep/Cut Weekly <weekly@news.aitoolsessentials.com>`. The HTML keeps the postal address `1090 West Foothill, Claremont, CA 91711`, the brand sign-off, and `{{{RESEND_UNSUBSCRIBE_URL}}}`. It refuses a draft that contains a personal name, and it does not call Resend when the flag is off or the approval file is missing.
