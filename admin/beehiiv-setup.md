# Beehiiv — AIToolsEssentials Keep/Cut Digest

Live publication (verified 2026-08-27):

- Publication ID: `pub_6019c431-f531-4041-b2b8-674214bc2a90`
- Site: https://aitoolsessentials.beehiiv.com/
- Signup: https://aitoolsessentials.beehiiv.com/subscribe
- MCP: https://mcp.beehiiv.com/mcp

`/subscribe/` on aitoolsessentials.com points at that official Beehiiv signup (button + iframe). Optional slim embed: paste `embed_html` into `data/newsletter.json` and regenerate.

## MCP (Hermes)

OAuth cannot finish in this non-interactive session. In a local Terminal:

```bash
hermes mcp add beehiiv --url https://mcp.beehiiv.com/mcp --auth oauth
```

Complete the browser login, then we can list forms, draft posts, and pull the native embed code.

Do not invent `embeds.beehiiv.com` form UUIDs. The publication signup URL is the verified capture path until a real embed script exists.
