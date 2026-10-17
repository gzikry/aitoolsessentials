"""Public Keep/Cut archive pages from admin/newsletter drafts."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_hold import public_colophon_html

DOMAIN = "https://aitoolsessentials.com"
_SIGN = "\u2014 AIToolsEssentials"


@dataclass(frozen=True)
class Letter:
    slug: str
    issue: int
    when: str
    title: str
    dek: str
    body: str


def esc(value: object) -> str:
    return (
        str(value or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _plain(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html)
    return (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .strip()
    )


def _clean_fragment(fragment: str) -> str:
    def repl(match: re.Match[str]) -> str:
        attrs = match.group(1)
        inner = re.sub(r'\sstyle="[^"]*"', "", match.group(2))
        inner = inner.replace(DOMAIN, "")
        inner = inner.strip()
        border = re.search(r"border-top:[^;\"]*", attrs)
        if border is None:
            return "<p>" + inner + "</p>"
        rule = border.group(0)
        tone = "gold"
        if "#2f6b4f" in rule:
            tone = "green"
        elif "#3b5c8a" in rule:
            tone = "blue"
        elif "#1a1714" in rule:
            tone = "ink"
        return f'<h2 class="letter-rule letter-rule--{tone}">' + inner + "</h2>"

    return re.sub(r"<p([^>]*)>(.*?)</p>", repl, fragment, flags=re.S)


def parse_draft(html: str, slug: str) -> Letter:
    issue_match = re.search(r"Issue\s+(\d+)\s+·\s+([^·<]+)", html)
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S)
    if issue_match is None or title_match is None:
        raise ValueError(f"{slug} draft is missing an issue line or title")
    after = html.split("</h1>", 1)[1]
    before, found, _rest = after.partition(_SIGN)
    if not found:
        raise ValueError(f"{slug} draft is missing the brand signature")
    before = re.sub(r"<p[^>]*>\s*$", "", before.strip())
    cleaned = _clean_fragment(before).strip()
    first, sep, rest = cleaned.partition("</p>")
    if not sep:
        raise ValueError(f"{slug} draft is missing a lead paragraph")
    dek = _plain(first + sep)
    body = rest.strip() + f'<p class="newsletter-signoff">{_SIGN}</p>'
    return Letter(
        slug=slug,
        issue=int(issue_match.group(1)),
        when=issue_match.group(2).strip(),
        title=_plain(title_match.group(1)),
        dek=dek,
        body=body,
    )


def _overlay_public(letter: Letter, html: str) -> Letter:
    issue_match = re.search(
        r'<p class="newsletter-issue-line">Issue\s+(\d+)\s+·\s+([^·<]+)',
        html,
    )
    title_match = re.search(r'<h1 class="newsletter-subject">(.*?)</h1>', html, flags=re.S)
    dek_match = re.search(r'<p class="newsletter-dek">(.*?)</p>', html, flags=re.S)
    if issue_match is None or title_match is None or dek_match is None:
        return letter
    return Letter(
        slug=letter.slug,
        issue=int(issue_match.group(1)),
        when=issue_match.group(2).strip(),
        title=_plain(title_match.group(1)),
        dek=_plain(dek_match.group(1)),
        body=letter.body,
    )


def load_letters(root: Path) -> list[Letter]:
    pack = root / "admin" / "newsletter"
    letters: list[Letter] = []
    if not pack.is_dir():
        return letters
    for path in sorted(pack.glob("*-draft.html")):
        slug = path.name[: -len("-draft.html")]
        letter = parse_draft(path.read_text(encoding="utf-8"), slug)
        public = root / "newsletter" / f"{slug}.html"
        if public.is_file() and "Morning." in public.read_text(encoding="utf-8"):
            letter = _overlay_public(letter, public.read_text(encoding="utf-8"))
        letters.append(letter)
    letters.sort(key=lambda item: item.issue, reverse=True)
    return letters


def blurb(dek: str) -> str:
    stop = dek.find(". ")
    if stop == -1:
        return dek
    return dek[: stop + 1]


def card(letter: Letter) -> str:
    return (
        '<article class="newsletter-issue-card">'
        f'<p class="newsletter-issue-card-meta">Issue {letter.issue} · {esc(letter.when)}</p>'
        f'<h3><a href="/newsletter/{esc(letter.slug)}.html">{esc(letter.title)}</a></h3>'
        f"<p>{esc(blurb(letter.dek))}</p></article>"
    )


def cards_html(letters: list[Letter]) -> str:
    return "".join(card(letter) for letter in letters)


_CHROME = re.compile(
    r"<!-- newsletter-issue-chrome -->.*?<!-- /newsletter-issue-chrome -->",
    flags=re.S,
)
_DONOR_VERIFICATION = re.compile(
    r"<p>Prices verified from official pages, rechecked 2026-08-25\..*?</p>\s*",
    flags=re.S,
)


def strip_donor_verification(html: str, letter: Letter) -> str:
    """Issue 1's price note is copied onto later letters by the page shell. Drop it."""
    if letter.issue == 1:
        return html
    return _DONOR_VERIFICATION.sub("", html, count=1)


def _pager_link(kind: str, letter: Letter) -> str:
    label = "Previous" if kind == "prev" else "Next"
    return (
        f'<a class="newsletter-pager-{kind}" href="/newsletter/{esc(letter.slug)}.html">'
        f"{label} · Issue {letter.issue} · {esc(letter.title)}</a>"
    )


def chrome_html(older: Letter | None, newer: Letter | None) -> str:
    links = []
    if older is not None:
        links.append(_pager_link("prev", older))
    if newer is not None:
        links.append(_pager_link("next", newer))
    nav = '<nav class="newsletter-pager" aria-label="Other issues">' + "".join(links) + "</nav>"
    cta = '<p class="newsletter-subscribe-cta"><a class="button button-blue" href="/subscribe/">Get the free email</a></p>'
    return "<!-- newsletter-issue-chrome -->" + nav + cta + "<!-- /newsletter-issue-chrome -->"


def apply_chrome(html: str, chrome: str) -> str:
    html = _CHROME.sub("", html)
    if "</article>" not in html:
        raise ValueError("issue page is missing </article>")
    return html.replace("</article>", chrome + "</article>", 1)


def apply_cards(index_html: str, cards: str) -> str:
    updated, count = re.subn(
        r'(<div class="newsletter-issue-list">).*?(</div>)',
        lambda match: match.group(1) + cards + match.group(2),
        index_html,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise ValueError("newsletter index is missing newsletter-issue-list")
    return updated


def splice_letter(donor: str, letter: Letter) -> str:
    head, rest = donor.split('<div class="newsletter-body">', 1)
    _old, tail = rest.split('<div class="newsletter-colophon">', 1)
    html = (
        head
        + '<div class="newsletter-body">'
        + letter.body
        + '</div><div class="newsletter-colophon">'
        + tail
    )
    html = html.replace(
        '<main class="newsletter-issue">',
        '<main class="newsletter-issue newsletter-letter">',
        1,
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="' + esc(letter.dek) + '"',
        html,
        count=1,
    )
    html = html.replace(
        f"{DOMAIN}/newsletter/2026-w35.html",
        f"{DOMAIN}/newsletter/{letter.slug}.html",
    )
    html = html.replace("The AI bill you forgot to cancel", letter.title)
    html = re.sub(
        r'(<p class="newsletter-issue-line">).*?(</p>)',
        lambda match: match.group(1) + f"Issue {letter.issue} · {esc(letter.when)}" + match.group(2),
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="newsletter-dek">).*?(</p>)',
        lambda match: match.group(1) + esc(letter.dek) + match.group(2),
        html,
        count=1,
    )
    return html


def _keep_existing(existing: str, letter: Letter) -> bool:
    if "Morning." in existing and "newsletter-sheet" in existing:
        return True
    return (
        letter.title in existing
        and "newsletter-sheet" in existing
        and "newsletter-letter" in existing
    )


def sync_archive(root: Path) -> int:
    letters = load_letters(root)
    out = root / "newsletter"
    out.mkdir(exist_ok=True)
    donor_path = out / "2026-w35.html"
    donor = donor_path.read_text(encoding="utf-8") if donor_path.is_file() else ""
    written = 0
    order = {letter.slug: index for index, letter in enumerate(letters)}
    for letter in letters:
        dest = out / f"{letter.slug}.html"
        existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
        if not _keep_existing(existing, letter):
            if "newsletter-sheet" not in donor or "Morning." not in donor:
                raise ValueError("newsletter/2026-w35.html must stay the page shell")
            existing = splice_letter(donor, letter)
            written += 1
        index = order[letter.slug]
        older = letters[index + 1] if index + 1 < len(letters) else None
        newer = letters[index - 1] if index > 0 else None
        updated = apply_chrome(strip_donor_verification(existing, letter), chrome_html(older, newer))
        if updated != (dest.read_text(encoding="utf-8") if dest.is_file() else ""):
            dest.write_text(updated, encoding="utf-8")
    cards = cards_html(letters)
    index = out / "index.html"
    if index.is_file() and 'class="newsletter-issue-list"' in index.read_text(encoding="utf-8"):
        index.write_text(apply_cards(index.read_text(encoding="utf-8"), cards), encoding="utf-8")
    else:
        index.write_text(_minimal_index(cards), encoding="utf-8")
    return written


def _minimal_index(cards: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keep, Test, Cut | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/newsletter/"><link rel="stylesheet" href="/css/styles.css"></head><body><main class="newsletter-archive"><div class="newsletter-archive-intro"><p class="newsletter-name">Keep, Test, Cut</p><h1>Past issues.</h1></div><div class="newsletter-issue-list">{cards}</div></main><footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/newsletter/">Keep, Test, Cut</a>{public_colophon_html()}</footer><script src="/js/analytics.js" defer></script></body></html>'''
