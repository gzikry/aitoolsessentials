# Beehiiv setup — AIToolsEssentials Keep/Cut Digest

The site already captures emails on `/subscribe/` via FormSubmit to `aitoolsessentials@gmail.com`. Swap in Beehiiv when the embed is ready.

## Create the publication (George)

1. Sign up at https://www.beehiiv.com with `aitoolsessentials@gmail.com` (or your usual login).
2. Publication name: **AIToolsEssentials Keep/Cut Digest**
3. Promise: weekly/as-needed notes when recorded AI tool prices, plans, or models change enough to affect a keep/cut decision. No daily spam.
4. Website / About: https://aitoolsessentials.com
5. Create a subscribe form: **Settings → Subscribe Forms → New**
   - Inline / slim
   - Fields: email only
   - Thank-you: "Check your inbox to confirm."
6. Click **Get embed code**. Copy the iframe/script.

## Wire it into the site

Paste the embed HTML into `data/newsletter.json` as `embed_html` (one string). Set `"status": "beehiiv_live"`.

Then run:

```bash
python3 scripts/generate_subscribe.py
python3 scripts/daily_content_update.py
python3 scripts/validate_site.py
```

The subscribe page uses Beehiiv when `embed_html` is non-empty; otherwise it keeps FormSubmit.

Do not paste a placeholder iframe. An empty `embed_html` is correct until the real code exists.
