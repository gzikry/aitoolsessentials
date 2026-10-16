from __future__ import annotations

import json
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

from affiliate_util import sponsored_href_needles
from site_scope import is_public_rel

__all__ = ["production_stripe_test_errors", "stamp", "stamp_site", "write_page"]

_ENROLLMENT_FILE = Path("data") / "sponsor_enrollment.json"
_PREVIEW_FILE = Path("data") / "sponsor_payment_preview.json"
_SPONSOR_MAIL = "aitoolsessentials@gmail.com"
_PAYMENT_FALLBACK = "SPONSOR_PAYMENT_URL"
_PREVIEW_FLAG = "SPONSOR_PAYMENT_PREVIEW"
_PRODUCTION_FLAG = "PRODUCTION_BUILD"
_ALLOW_TEST_FLAG = "ALLOW_STRIPE_TEST_LINKS"
_ON = frozenset({"1", "true", "yes", "on"})
_STRIPE_TEST_HOST = "buy.stripe.com"


@dataclass(frozen=True, slots=True)
class _Tier:
    key: str
    label: str
    price: str
    env_name: str


_TIERS = (
    _Tier("issue", "Newsletter line, 1 issue", "$50", "SPONSOR_PAYMENT_URL_ISSUE"),
    _Tier("bar", "Site bar, 1 month", "$150", "SPONSOR_PAYMENT_URL_BAR"),
    _Tier("bundle", "Bundle, 1 month", "$200", "SPONSOR_PAYMENT_URL_BUNDLE"),
)
_PREVIEW_KEYS = frozenset(tier.key for tier in _TIERS)
_LABEL = "Sponsored"
_HOUSE_HREF = "/sponsor/"
_HOUSE_REL = "nofollow"
_EXTERNAL_REL = "external noopener nofollow"
_CHARGE_RETURN = "checkout/complete/index.html"
_PLAIN_LIMIT = 40

_NAV_START = "<!-- AIT SPONSOR NAV START -->"
_NAV_END = "<!-- AIT SPONSOR NAV END -->"
_LINE_START = "<!-- AIT SPONSOR LINE START -->"
_LINE_END = "<!-- AIT SPONSOR LINE END -->"
_ISSUE_START = "<!-- AIT SPONSOR ISSUE START -->"
_ISSUE_END = "<!-- AIT SPONSOR ISSUE END -->"

_HOUSE = (
    _NAV_START
    + '<a href="'
    + _HOUSE_HREF
    + '" rel="'
    + _HOUSE_REL
    + '">Sponsor us</a>'
    + _NAV_END
)

_TOP_KEYS = frozenset({"enrollment"})
_ENROLLMENT_KEYS = frozenset({"name", "pitch", "href", "logo"})
_LOGO_KEYS = frozenset({"src", "alt"})

_OFFER_TITLE = "Sponsor AIToolsEssentials"
_OFFER_PARAS = (
    "People come here to decide which AI tools to keep and which to cancel. If your product holds up, this is a good place to be seen.",
    'What you get: a line at the bottom of every page, and/or a "Sponsored by" line in Keep/Cut Weekly.',
    "What you don't get: a better review. Sponsors are labeled, kept away from scores, and never change a verdict.",
    "One sponsor at a time. We say no to tools we wouldn't use ourselves.",
)
_SIGN_OFF = "\u2014 AIToolsEssentials"

_HEADER = (
    '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">\u2726</span>'
    "<span>AIToolsEssentials</span></a><nav class=\"nav-links\">"
    '<a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a>'
    '<a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a>'
    '<a href="/alternatives/">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a>'
    '<a href="/articles/index.html">Guides</a><a href="/deals/">Deals</a></nav>'
    '<a class="nav-cta" href="/pricing/">Paid Premium</a></header>'
)
_FOOTER = (
    '<footer class="footer"><span>\u00a9 2026 AIToolsEssentials</span>'
    '<a href="/advertise/" rel="nofollow">Advertise</a>'
    '<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>'
    '<a href="mailto:contact@aitoolsessentials.com">Contact</a>'
    '<a href="/legal/about.html">About</a>'
    '<a href="/legal/privacy.html">Privacy</a>'
    '<a href="/legal/terms.html">Terms</a></footer>'
)

_FORBIDDEN_CLASSES = frozenset({
    "review-layout",
    "review-aside",
    "conversion-verdict-bar",
    "directory-card",
    "newsletter-segment--keep",
    "newsletter-segment--cut",
    "score-card",
    "sa-rec",
})
_FORBIDDEN_ID = "quiz-verdict"
_VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
})
_HOUSE_ANCHOR = re.compile(
    r'<a\b[^>]*\bhref=(["\'])/sponsor/\1[^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL,
)


class _ConfigError(ValueError):
    pass


class _Slot(Enum):
    PAGE_FOOT = "page-foot"
    ISSUE_COLOPHON = "issue-colophon"


class _PageRole(Enum):
    CHARGE_RETURN = "charge_return"
    PUBLIC = "public"


@dataclass(frozen=True, slots=True)
class _Pitch:
    text: str


@dataclass(frozen=True, slots=True)
class _Logo:
    src: str
    alt: str


@dataclass(frozen=True, slots=True)
class _Href:
    value: str
    kind: Literal["house", "external"]


@dataclass(frozen=True, slots=True)
class _Enrollment:
    name: str
    pitch: _Pitch
    href: _Href
    logo: _Logo | None


@dataclass(frozen=True, slots=True)
class _Mailto:
    address: str


@dataclass(frozen=True, slots=True)
class _ExternalPay:
    url: str


_Payment = _Mailto | _ExternalPay


@dataclass(frozen=True, slots=True)
class _Runtime:
    enrollment: _Enrollment | None
    tiers: tuple[tuple[_Tier, _Payment], ...]


@dataclass(frozen=True, slots=True)
class _Tag:
    name: str
    start: int
    end: int
    closing: bool
    self_closing: bool
    classes: frozenset[str]
    elem_id: str


@dataclass
class _Node:
    name: str
    start: int
    open_end: int
    close_start: int | None
    close_end: int | None
    classes: frozenset[str]
    elem_id: str
    parent: int | None
    children: list[int]


def write_page(root: Path, env: Mapping[str, str] | None = None) -> None:
    runtime = _runtime(root, _chosen_env(env))
    dest = root / "sponsor" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(_page_html(runtime.tiers))


def stamp(
    html: str,
    rel: str,
    *,
    root: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> str:
    if _page_role(rel) is _PageRole.CHARGE_RETURN:
        return html
    if root is None:
        root = _repo_root()
    return _apply(html, rel, _runtime(root, _chosen_env(env)))


def stamp_site(root: Path, env: Mapping[str, str] | None = None) -> int:
    chosen = _chosen_env(env)
    _runtime(root, chosen)
    changed = 0
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not is_public_rel(rel):
            continue
        html = path.read_text()
        stamped = stamp(html, rel.as_posix(), root=root, env=chosen)
        if stamped != html:
            path.write_text(stamped)
            changed += 1
    return changed


def _chosen_env(env: Mapping[str, str] | None) -> Mapping[str, str]:
    if env is None:
        return os.environ
    return env


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _page_role(rel: str) -> _PageRole:
    if rel == _CHARGE_RETURN:
        return _PageRole.CHARGE_RETURN
    return _PageRole.PUBLIC


def _runtime(root: Path, env: Mapping[str, str]) -> _Runtime:
    path = root / _ENROLLMENT_FILE
    if not path.is_file():
        raise _ConfigError("sponsor enrollment file is missing")
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise _ConfigError("sponsor enrollment file is not JSON") from exc
    if not isinstance(data, dict):
        raise _ConfigError("sponsor enrollment file must be an object")
    _reject_unknown(data, _TOP_KEYS)
    if "enrollment" not in data:
        raise _ConfigError("enrollment is required")
    needles = sponsored_href_needles(root)
    enrollment = _enrollment(data["enrollment"], needles)
    payments = _with_preview(root, env)
    return _Runtime(
        enrollment=enrollment,
        tiers=_tier_payments(payments, needles, _build(payments)),
    )


def _reject_unknown(data: dict, allowed: frozenset[str]) -> None:
    extra = set(data) - allowed
    if extra:
        raise _ConfigError("unknown key: " + ", ".join(sorted(extra)))


def _enrollment(raw: object, needles: tuple[str, ...]) -> _Enrollment | None:
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise _ConfigError("enrollment must be an object or null")
    _reject_unknown(raw, _ENROLLMENT_KEYS)
    for key in ("name", "pitch", "href"):
        if key not in raw:
            raise _ConfigError("enrollment " + key + " is required")
    name = _plain("name", raw["name"], limit=_PLAIN_LIMIT)
    pitch = _Pitch(_plain("pitch", raw["pitch"], limit=_PLAIN_LIMIT))
    href = _href(raw["href"], needles)
    logo = _logo(raw["logo"], name) if "logo" in raw else None
    return _Enrollment(name=name, pitch=pitch, href=href, logo=logo)


def _flag(env: Mapping[str, str], name: str) -> bool:
    raw = env.get(name, "")
    if not isinstance(raw, str):
        return False
    return raw.strip().casefold() in _ON


def _is_production(env: Mapping[str, str]) -> bool:
    # GitHub Pages serves committed HTML. A push to main is the live build.
    if _flag(env, _PRODUCTION_FLAG):
        return True
    ref = env.get("GITHUB_REF", "")
    return isinstance(ref, str) and ref.strip() == "refs/heads/main"


@dataclass(frozen=True, slots=True)
class _Build:
    production: bool
    allow_stripe_test: bool


def _build(env: Mapping[str, str]) -> _Build:
    return _Build(
        production=_is_production(env),
        allow_stripe_test=_flag(env, _ALLOW_TEST_FLAG),
    )


def _stripe_test_url(text: str) -> bool:
    parsed = urlsplit(text)
    return (
        parsed.scheme == "https"
        and parsed.netloc == _STRIPE_TEST_HOST
        and parsed.path.startswith("/test_")
    )


def _with_preview(root: Path, env: Mapping[str, str]) -> dict[str, str]:
    merged = {key: value for key, value in env.items() if isinstance(value, str)}
    if not _flag(env, _PREVIEW_FLAG):
        return merged
    path = root / _PREVIEW_FILE
    if not path.is_file():
        raise _ConfigError("sponsor payment preview file is missing")
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise _ConfigError("sponsor payment preview file is not JSON") from exc
    if not isinstance(data, dict):
        raise _ConfigError("sponsor payment preview file must be an object")
    _reject_unknown(data, _PREVIEW_KEYS)
    for tier in _TIERS:
        current = merged.get(tier.env_name, "")
        if isinstance(current, str) and current.strip():
            continue
        raw = data.get(tier.key, "")
        if not isinstance(raw, str) or not raw.strip():
            raise _ConfigError("preview " + tier.key + " must be an https URL")
        merged[tier.env_name] = raw.strip()
    return merged


def _https_payment(text: str, name: str, needles: tuple[str, ...], build: _Build) -> _ExternalPay:
    # A visible "${...}" fails site validation, and the variable name is not a URL.
    if name in text or "${" in text:
        raise _ConfigError(name + " is not a finished https URL")
    _reject_personal_name(text)
    if not text.startswith("https://") or len(text) <= len("https://"):
        raise _ConfigError(name + " must be https")
    if any(ch.isspace() or ord(ch) < 32 or ch in '<>"\'' for ch in text):
        raise _ConfigError(name + " must be https")
    if _needle_hit(text, needles):
        raise _ConfigError(name + " hits an affiliate needle")
    if _stripe_test_url(text) and build.production and not build.allow_stripe_test:
        raise _ConfigError(name + " is a Stripe test link")
    return _ExternalPay(text)


def _optional_https(
    env: Mapping[str, str], name: str, needles: tuple[str, ...], build: _Build
) -> _ExternalPay | None:
    if name not in env:
        return None
    raw = env.get(name, "")
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise _ConfigError(name + " must be a string")
    text = raw.strip()
    if text == "":
        return None
    return _https_payment(text, name, needles, build)


def _tier_payments(
    env: Mapping[str, str], needles: tuple[str, ...], build: _Build
) -> tuple[tuple[_Tier, _Payment], ...]:
    fallback = _optional_https(env, _PAYMENT_FALLBACK, needles, build)
    rows: list[tuple[_Tier, _Payment]] = []
    for tier in _TIERS:
        specific = _optional_https(env, tier.env_name, needles, build)
        if specific is not None:
            payment: _Payment = specific
        elif fallback is not None:
            payment = fallback
        else:
            payment = _Mailto(_SPONSOR_MAIL)
        rows.append((tier, payment))
    return tuple(rows)


def production_stripe_test_errors(
    root: Path, env: Mapping[str, str] | None = None
) -> list[str]:
    source = os.environ if env is None else env
    if not _is_production(source) or _flag(source, _ALLOW_TEST_FLAG):
        return []
    found: list[str] = []
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not is_public_rel(rel):
            continue
        if "https://buy.stripe.com/test_" in path.read_text(errors="replace"):
            found.append(rel.as_posix() + " has a Stripe test payment link")
    return found


def _plain(label: str, value: object, *, limit: int) -> str:
    if not isinstance(value, str):
        raise _ConfigError(label + " must be plain text")
    text = value.strip()
    if not text or len(text) > limit:
        raise _ConfigError(label + " must be 1 to " + str(limit) + " characters")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise _ConfigError(label + " must be plain text")
    if "<" in text or ">" in text or "$" in text:
        raise _ConfigError(label + " must be plain text")
    _reject_personal_name(text)
    return text


def _reject_personal_name(value: str) -> None:
    # Checked on every interpolated field. A name stuffed into an href still renders.
    if "george" in value.casefold():
        raise _ConfigError("personal name is not allowed")


def _href(value: object, needles: tuple[str, ...]) -> _Href:
    if not isinstance(value, str):
        raise _ConfigError("href must be a string")
    text = value.strip()
    _reject_personal_name(text)
    if "${" in text or "<" in text or ">" in text:
        raise _ConfigError("href must be root-absolute or https")
    if text.startswith("/") and not text.startswith("//") and ".." not in text and "://" not in text:
        return _Href(text, "house")
    if text.startswith("https://"):
        if _needle_hit(text, needles):
            raise _ConfigError("href hits an affiliate needle")
        return _Href(text, "external")
    raise _ConfigError("href must be root-absolute or https")


def _needle_hit(value: str, needles: tuple[str, ...]) -> bool:
    return any(needle and needle in value for needle in needles)


def _logo(raw: object, name: str) -> _Logo | None:
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise _ConfigError("logo must be an object or null")
    _reject_unknown(raw, _LOGO_KEYS)
    if "src" not in raw or not isinstance(raw["src"], str):
        raise _ConfigError("logo src is required")
    src = raw["src"].strip()
    _reject_personal_name(src)
    if "${" in src or "<" in src or ">" in src or ".." in src:
        raise _ConfigError("logo src must be https or root-absolute")
    root_absolute = src.startswith("/") and not src.startswith("//") and "://" not in src
    if not root_absolute and not src.startswith("https://"):
        raise _ConfigError("logo src must be https or root-absolute")
    alt_value = raw["alt"] if "alt" in raw else name
    alt = _plain("alt", alt_value, limit=_PLAIN_LIMIT)
    return _Logo(src=src, alt=alt)


def _page_html(rows: tuple[tuple[_Tier, _Payment], ...]) -> str:
    blocks = ["<h1>" + _OFFER_TITLE + "</h1>"]
    for paragraph in _OFFER_PARAS:
        blocks.append("<p>" + paragraph + "</p>")
    for tier, payment in rows:
        blocks.append("<h2>" + tier.label + "</h2>")
        blocks.append("<p>" + tier.price + "</p>")
        blocks.append("<p>" + _payment_anchor(payment) + "</p>")
    blocks.append(
        '<p>Questions: <a href="mailto:'
        + _SPONSOR_MAIL
        + '">'
        + _SPONSOR_MAIL
        + "</a></p>"
    )
    blocks.append("<p>" + _SIGN_OFF + "</p>")
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + _OFFER_TITLE + "</title>\n"
        '<link rel="stylesheet" href="/css/styles.css">\n'
        "</head>\n"
        "<body>\n"
        + _HEADER
        + "\n<main>\n"
        + "\n".join(blocks)
        + "\n</main>\n"
        + _FOOTER
        + "\n</body>\n</html>\n"
    )


def _payment_anchor(payment: _Payment) -> str:
    if isinstance(payment, _Mailto):
        return (
            '<a class="button button-blue" href="mailto:'
            + payment.address
            + '">Sponsor us</a>'
        )
    if isinstance(payment, _ExternalPay):
        return (
            '<a class="button button-blue" href="'
            + _esc(payment.url)
            + '" target="_blank" rel="'
            + _EXTERNAL_REL
            + '">Sponsor us</a>'
        )
    raise _ConfigError("unknown payment")


def _apply(html: str, rel: str, runtime: _Runtime) -> str:
    if _page_role(rel) is _PageRole.CHARGE_RETURN:
        return html
    html = _strip_markers(html)
    html = _strip_house_anchors(html)
    html = _insert_house(html)
    if runtime.enrollment is None:
        return html
    html = _insert_block(html, _page_foot_offset(html), _line_html(runtime.enrollment))
    html = _insert_block(html, _issue_offset(html, rel), _issue_html(runtime.enrollment))
    return html


def _strip_markers(html: str) -> str:
    for start, end in (
        (_NAV_START, _NAV_END),
        (_LINE_START, _LINE_END),
        (_ISSUE_START, _ISSUE_END),
    ):
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
        html = pattern.sub("", html)
    return html


def _strip_house_anchors(html: str) -> str:
    ranges: list[tuple[int, int]] = []
    for node in _parse(html):
        if node.name not in {"header", "footer"} or node.close_start is None:
            continue
        ranges.append((node.open_end, node.close_start))
    for start, end in reversed(ranges):
        cleaned = _HOUSE_ANCHOR.sub("", html[start:end])
        if cleaned != html[start:end]:
            html = html[:start] + cleaned + html[end:]
    return html


def _insert_house(html: str) -> str:
    nodes = _parse(html)
    nav_at = _nav_close(nodes)
    if nav_at is not None:
        return html[:nav_at] + _HOUSE + html[nav_at:]
    foot_at = _footer_close_start(nodes)
    if foot_at is None:
        return html
    return html[:foot_at] + _HOUSE + html[foot_at:]


def _insert_block(html: str, offset: int | None, block: str) -> str:
    if offset is None or not _clear(html, offset):
        return html
    return html[:offset] + block + html[offset:]


def _nav_close(nodes: list[_Node]) -> int | None:
    fallback = None
    for index, node in enumerate(nodes):
        if node.name != "nav" or "nav-links" not in node.classes or node.close_start is None:
            continue
        if _inside(nodes, index, "header"):
            return node.close_start
        if fallback is None:
            fallback = node.close_start
    return fallback


def _footer_close_start(nodes: list[_Node]) -> int | None:
    fallback = None
    for node in nodes:
        if node.name != "footer" or node.close_start is None:
            continue
        if "footer" in node.classes:
            return node.close_start
        if fallback is None:
            fallback = node.close_start
    return fallback


def _page_foot_offset(html: str) -> int | None:
    nodes = _parse(html)
    main_end = _first_main_end(nodes)
    if main_end is None:
        return None
    ends = [
        node.close_end
        for node in nodes
        if node.name == "footer" and node.close_end is not None and node.start >= main_end
    ]
    if not ends:
        return None
    return max(ends)


def _issue_offset(html: str, rel: str) -> int | None:
    if not rel.startswith("newsletter/"):
        return None
    for node in _parse(html):
        if "newsletter-colophon" in node.classes and node.close_start is not None:
            return node.open_end
    return None


def _line_html(enrollment: _Enrollment) -> str:
    parts = ['<span class="sponsor-line-label">' + _LABEL + "</span>"]
    if enrollment.logo is not None:
        parts.append(
            '<img src="'
            + _esc(enrollment.logo.src)
            + '" alt="'
            + _esc(enrollment.logo.alt)
            + '">'
        )
    parts.append('<span class="sponsor-line-pitch">' + _esc(enrollment.pitch.text) + "</span>")
    parts.append(_anchor(enrollment.href, enrollment.name))
    paragraph = (
        '<p class="sponsor-line" data-sponsor="'
        + _Slot.PAGE_FOOT.value
        + '">'
        + " ".join(parts)
        + "</p>"
    )
    return _LINE_START + "\n" + paragraph + "\n" + _LINE_END


def _issue_html(enrollment: _Enrollment) -> str:
    paragraph = (
        '<p class="sponsor-issue" data-sponsor="'
        + _Slot.ISSUE_COLOPHON.value
        + '"><span class="sponsor-line-label">'
        + _LABEL
        + "</span> by "
        + _anchor(enrollment.href, enrollment.name)
        + "</p>"
    )
    return _ISSUE_START + "\n" + paragraph + "\n" + _ISSUE_END


def _anchor(href: _Href, text: str) -> str:
    safe_href = _esc(href.value)
    safe_text = _esc(text)
    if href.kind == "house":
        return '<a href="' + safe_href + '" rel="' + _HOUSE_REL + '">' + safe_text + "</a>"
    if href.kind == "external":
        return (
            '<a href="'
            + safe_href
            + '" target="_blank" rel="'
            + _EXTERNAL_REL
            + '">'
            + safe_text
            + "</a>"
        )
    raise _ConfigError("unknown href")


def _clear(html: str, offset: int) -> bool:
    nodes = _parse(html)
    if any(_contains(node, offset) and _forbidden(node) for node in nodes):
        return False
    prev_el, next_el = _siblings(nodes, offset)
    if (prev_el is not None and _forbidden(prev_el)) or (next_el is not None and _forbidden(next_el)):
        return False
    for node in nodes:
        if node.name == "footer" and node.close_end == offset:
            main_end = _first_main_end(nodes)
            if main_end is not None and offset < main_end:
                return False
            break
    return True


def _forbidden(node: _Node) -> bool:
    if node.elem_id == _FORBIDDEN_ID:
        return True
    return bool(node.classes & _FORBIDDEN_CLASSES)


def _first_main_end(nodes: list[_Node]) -> int | None:
    ends = [node.close_end for node in nodes if node.name == "main" and node.close_end is not None]
    if not ends:
        return None
    return min(ends)


def _contains(node: _Node, offset: int) -> bool:
    if offset < node.open_end:
        return False
    if node.close_start is None:
        return True
    return offset < node.close_start


def _innermost(nodes: list[_Node], offset: int) -> _Node | None:
    best = None
    for node in nodes:
        if not _contains(node, offset):
            continue
        if best is None or node.start >= best.start:
            best = node
    return best


def _siblings(nodes: list[_Node], offset: int) -> tuple[_Node | None, _Node | None]:
    parent = _innermost(nodes, offset)
    if parent is None:
        kids = [node for node in nodes if node.parent is None]
    else:
        kids = [nodes[index] for index in parent.children]
    prev_el = None
    next_el = None
    for kid in kids:
        if kid.close_end is not None and kid.close_end <= offset:
            if prev_el is None or (prev_el.close_end is not None and kid.close_end > prev_el.close_end):
                prev_el = kid
        elif kid.start >= offset and (next_el is None or kid.start < next_el.start):
            next_el = kid
    return prev_el, next_el


def _inside(nodes: list[_Node], index: int, name: str) -> bool:
    parent = nodes[index].parent
    while parent is not None:
        if nodes[parent].name == name:
            return True
        parent = nodes[parent].parent
    return False


def _parse(html: str) -> list[_Node]:
    nodes: list[_Node] = []
    stack: list[int] = []
    for tag in _iter_tags(html):
        if tag.closing:
            while stack:
                index = stack.pop()
                node = nodes[index]
                if node.close_start is None:
                    node.close_start = tag.start
                    node.close_end = tag.end
                if node.name == tag.name:
                    break
            continue
        parent = stack[-1] if stack else None
        node = _Node(
            name=tag.name,
            start=tag.start,
            open_end=tag.end,
            close_start=tag.end if tag.self_closing else None,
            close_end=tag.end if tag.self_closing else None,
            classes=tag.classes,
            elem_id=tag.elem_id,
            parent=parent,
            children=[],
        )
        nodes.append(node)
        index = len(nodes) - 1
        if parent is not None:
            nodes[parent].children.append(index)
        if not tag.self_closing:
            stack.append(index)
    return nodes


def _iter_tags(html: str):
    i = 0
    n = len(html)
    lowered = html.lower()
    while i < n:
        start = html.find("<", i)
        if start == -1:
            return
        if html.startswith("<!--", start):
            end = html.find("-->", start + 4)
            if end == -1:
                return
            i = end + 3
            continue
        if html.startswith("<!", start) or html.startswith("<?", start):
            end = html.find(">", start + 2)
            if end == -1:
                return
            i = end + 1
            continue
        end = html.find(">", start + 1)
        if end == -1:
            return
        inner = html[start + 1:end]
        name, closing = _tag_name(inner)
        if not name:
            i = end + 1
            continue
        attrs = {} if closing else _attributes(inner)
        self_closing = (not closing) and _is_self_closing(inner, name)
        yield _Tag(
            name=name,
            start=start,
            end=end + 1,
            closing=closing,
            self_closing=self_closing,
            classes=_class_tokens(attrs),
            elem_id=attrs.get("id", ""),
        )
        i = end + 1
        if name in {"script", "style"} and not closing and not self_closing:
            close_at = lowered.find("</" + name, i)
            if close_at == -1:
                return
            i = close_at


def _tag_name(inner: str) -> tuple[str, bool]:
    raw = inner.strip()
    closing = raw.startswith("/")
    if closing:
        raw = raw[1:].lstrip()
    name: list[str] = []
    for ch in raw:
        if ch.isspace() or ch in "/>":
            break
        name.append(ch.lower())
    return "".join(name), closing


def _attributes(inner: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    i = 0
    n = len(inner)
    while i < n and not inner[i].isspace() and inner[i] not in "/>":
        i += 1
    while i < n:
        while i < n and (inner[i].isspace() or inner[i] == "/"):
            i += 1
        if i >= n:
            break
        start = i
        while i < n and not inner[i].isspace() and inner[i] not in "=/>":
            i += 1
        name = inner[start:i].lower()
        if not name:
            i += 1
            continue
        while i < n and inner[i].isspace():
            i += 1
        if i >= n or inner[i] != "=":
            attrs[name] = ""
            continue
        i += 1
        while i < n and inner[i].isspace():
            i += 1
        if i >= n:
            attrs[name] = ""
            break
        if inner[i] in "\"'":
            quote = inner[i]
            i += 1
            value_start = i
            while i < n and inner[i] != quote:
                i += 1
            attrs[name] = inner[value_start:i]
            if i < n:
                i += 1
        else:
            value_start = i
            while i < n and not inner[i].isspace() and inner[i] not in "/>":
                i += 1
            attrs[name] = inner[value_start:i]
    return attrs


def _class_tokens(attrs: dict[str, str]) -> frozenset[str]:
    return frozenset(attrs.get("class", "").split())


def _is_self_closing(inner: str, name: str) -> bool:
    if name in _VOID_TAGS:
        return True
    in_quote = ""
    last = ""
    for ch in inner:
        if in_quote:
            if ch == in_quote:
                in_quote = ""
            continue
        if ch in "\"'":
            in_quote = ch
            continue
        if not ch.isspace():
            last = ch
    return last == "/"


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
