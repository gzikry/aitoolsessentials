"""Audited-pricing SVG badges and the cite/embed drawer.

Prices and credit-trap lines come from the dated catalog. A tool that is
not on the credit-trap ledger is labeled that way. Nothing here invents a
dollar figure or a trap.
"""
from __future__ import annotations

import html
from typing import Any

from generate_credit_traps import TRAPS

DOMAIN = "https://aitoolsessentials.com"
MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
STAMP = "AUDITED BY AI TOOLS ESSENTIALS"


def xml(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def audit_month(source: dict[str, Any] | None) -> str:
    raw = str((source or {}).get("pricing_checked_date") or "")
    parts = raw.split("-")
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        month = int(parts[1])
        if 1 <= month <= 12:
            return f"{MONTHS[month - 1]} {parts[0]}"
    return "UNDATED"


def _clip(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:(")
    return (cut or text[: limit - 1]) + "…"


def short_price(tool: dict[str, Any], source: dict[str, Any] | None) -> str:
    """A short verified price line. Prefer the first dollar amount in the dated summary."""
    summary = " ".join(str((source or {}).get("pricing_summary") or "").split())
    price = " ".join(str(tool.get("price") or "").split())
    dollar = summary.find("$")
    if dollar >= 0:
        start = max(
            summary.rfind(":", 0, dollar),
            summary.rfind(";", 0, dollar),
            summary.rfind(". ", 0, dollar),
        )
        if start >= 0:
            start += 1
            while start < len(summary) and summary[start] in " :;.)":
                start += 1
        else:
            start = summary.rfind(" ", 0, max(0, dollar - 18))
            start = 0 if start < 0 else start + 1
        return _clip(summary[start:], 78)
    if price:
        return _clip(price, 78)
    if summary:
        return _clip(summary, 78)
    return "See the dated review"


def trap_status(slug: str) -> str:
    hits = [row for row in TRAPS if row.get("slug") == slug]
    if not hits:
        return "Not in the credit-trap ledger"
    return _clip(str(hits[0].get("rule") or ""), 46)


def badge_svg(tool: dict[str, Any], source: dict[str, Any] | None) -> str:
    name = str(tool.get("name") or tool.get("slug") or "")
    price = short_price(tool, source)
    trap = trap_status(str(tool.get("slug") or ""))
    month = audit_month(source)
    name_size = 16 if len(name) <= 28 else 13
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="108" viewBox="0 0 360 108" role="img" aria-label="{xml(STAMP)} — {xml(name)}">
  <rect width="360" height="108" fill="#FAF8F5"/>
  <rect x="0.5" y="0.5" width="359" height="107" fill="none" stroke="#111315"/>
  <rect width="8" height="108" fill="#156E3F"/>
  <text x="18" y="20" font-family="IBM Plex Mono, ui-monospace, monospace" font-size="10" letter-spacing="0.08em" fill="#156E3F">{xml(STAMP)}</text>
  <text x="18" y="44" font-family="Newsreader, Georgia, serif" font-size="{name_size}" font-weight="700" fill="#111315">{xml(name)}</text>
  <text x="18" y="66" font-family="IBM Plex Mono, ui-monospace, monospace" font-size="11" fill="#111315">{xml(price)}</text>
  <text x="18" y="86" font-family="IBM Plex Mono, ui-monospace, monospace" font-size="10" fill="#111315">{xml(trap)}</text>
  <text x="342" y="86" text-anchor="end" font-family="IBM Plex Mono, ui-monospace, monospace" font-size="11" fill="#111315">{xml(month)}</text>
  <line x1="18" y1="74" x2="342" y2="74" stroke="#D8D2C5"/>
</svg>
'''


def audited_stamp_svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="320" height="64" viewBox="0 0 320 64" role="img" aria-label="{STAMP}">
  <rect width="320" height="64" fill="#FAF8F5"/>
  <rect x="0.5" y="0.5" width="319" height="63" fill="none" stroke="#111315"/>
  <rect width="8" height="64" fill="#156E3F"/>
  <text x="18" y="28" font-family="IBM Plex Mono, ui-monospace, monospace" font-size="11" letter-spacing="0.06em" fill="#156E3F">{STAMP}</text>
  <text x="18" y="48" font-family="Newsreader, Georgia, serif" font-size="14" fill="#111315">Audited price ledger</text>
</svg>
'''


def citation_fact(tool: dict[str, Any], source: dict[str, Any] | None) -> str:
    name = str(tool.get("name") or tool.get("slug") or "")
    month = audit_month(source)
    price = short_price(tool, source)
    slug = str(tool.get("slug") or "")
    url = f"{DOMAIN}/tools/{slug}/"
    return (
        f"{name}, audited {month} by AI Tools Essentials: {price}. "
        f"{trap_status(slug)}. Source: {url}"
    )


def cite_drawer_html(tool: dict[str, Any], source: dict[str, Any] | None) -> str:
    slug = str(tool.get("slug") or "")
    name = str(tool.get("name") or slug)
    page = f"{DOMAIN}/tools/{slug}/?utm_source=badge_embed"
    badge = f"{DOMAIN}/badges/{slug}.svg"
    alt = f"{STAMP} — {name}"
    html_snippet = (
        f'<a href="{page}"><img alt="{alt}" src="{badge}" width="360" height="108"></a>'
    )
    markdown = f"[![{alt}]({badge})]({page})"
    fact = citation_fact(tool, source)
    year = audit_month(source).split(" ")[-1] if audit_month(source) != "UNDATED" else "2026"
    bibtex = (
        f"@misc{{aitoolsessentials_{slug.replace('-', '_')}_{year},\n"
        f"  title = {{{name} pricing audit}},\n"
        f"  author = {{{{AIToolsEssentials}}}},\n"
        f"  year = {{{year}}},\n"
        f"  url = {{{DOMAIN}/tools/{slug}/}},\n"
        f"  note = {{{fact}}}\n"
        f"}}"
    )
    plain = fact
    return f'''
<details class="cite-drawer" id="cite-audit">
<summary>Cite or embed this audit</summary>
<p>The badge links to this review. It is a dated price receipt, not a ranking and not a paid placement.</p>
<p><img alt="{xml(alt)}" src="/badges/{xml(slug)}.svg" width="360" height="108"></p>
<label>HTML badge snippet
<textarea readonly data-cite-box>{xml(html_snippet)}</textarea></label>
<button type="button" data-cite-copy>Copy HTML</button>
<label>Markdown badge snippet
<textarea readonly data-cite-box>{xml(markdown)}</textarea></label>
<button type="button" data-cite-copy>Copy Markdown</button>
<label>Editorial citation
<textarea readonly data-cite-box>{xml(plain)}</textarea></label>
<button type="button" data-cite-copy>Copy citation</button>
<label>BibTeX
<textarea readonly data-cite-box>{xml(bibtex)}</textarea></label>
<button type="button" data-cite-copy>Copy BibTeX</button>
</details>
<script>
document.querySelectorAll("[data-cite-copy]").forEach(function (button) {{
  button.addEventListener("click", function () {{
    var box = button.previousElementSibling && button.previousElementSibling.querySelector("textarea");
    if (!box) return;
    var done = function () {{ button.textContent = "Copied"; }};
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(box.value).then(done);
    }} else {{
      box.select();
      document.execCommand("copy");
      done();
    }}
  }});
}});
</script>
'''


CITE_STYLE = """
<style>
.cite-drawer{margin:28px auto;max-width:980px;padding:16px 18px;background:#FAF8F5;color:#111315;border:1px solid #111315}
.cite-drawer summary{cursor:pointer;font-family:"IBM Plex Mono",ui-monospace,monospace;letter-spacing:.04em;font-size:13px}
.cite-drawer textarea{width:100%;min-height:72px;margin:6px 0 8px;padding:8px;border:1px solid #D8D2C5;background:#fff;color:#111315;font:12px/1.4 "IBM Plex Mono",ui-monospace,monospace}
.cite-drawer button{margin:0 0 14px;border:1px solid #111315;background:#111315;color:#FAF8F5;padding:6px 10px;font:12px "IBM Plex Mono",ui-monospace,monospace;cursor:pointer}
.cite-drawer label{display:block;margin-top:8px;font-size:13px}
</style>
"""
