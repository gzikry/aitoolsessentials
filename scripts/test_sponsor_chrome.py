#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sponsor_chrome import stamp, stamp_site, write_page

HOUSE = (
    '<!-- AIT SPONSOR NAV START --><a href="/sponsor/" rel="nofollow">Sponsor us</a>'
    "<!-- AIT SPONSOR NAV END -->"
)
MAILTO_BUTTON = (
    '<a class="button button-blue" href="mailto:aitoolsessentials@gmail.com">Sponsor us</a>'
)
HTTPS_BUTTON = (
    '<a class="button button-blue" href="https://pay.example.com/sponsor" '
    'target="_blank" rel="external noopener nofollow">Sponsor us</a>'
)
QUESTIONS = (
    'Questions: <a href="mailto:aitoolsessentials@gmail.com">aitoolsessentials@gmail.com</a>'
)
PITCH = "Tools you can cancel"
EXTERNAL_LINE = (
    '<p class="sponsor-line" data-sponsor="page-foot">'
    '<span class="sponsor-line-label">Sponsored</span> '
    '<span class="sponsor-line-pitch">' + PITCH + "</span> "
    '<a href="https://example.com/north" target="_blank" rel="external noopener nofollow">Northwind</a>'
    "</p>"
)
ISSUE_LINE = (
    '<p class="sponsor-issue" data-sponsor="issue-colophon">'
    '<span class="sponsor-line-label">Sponsored</span> by '
    '<a href="https://example.com/north" target="_blank" rel="external noopener nofollow">Northwind</a>'
    "</p>"
)
OFFER = (
    "People come here to decide which AI tools to keep and which to cancel. If your product holds up, this is a good place to be seen.",
    'What you get: a line at the bottom of every page, and/or a "Sponsored by" line in Keep/Cut Weekly.',
    "What you don't get: a better review. Sponsors are labeled, kept away from scores, and never change a verdict.",
    "One sponsor at a time. We say no to tools we wouldn't use ourselves.",
)
PAGE = (
    "<!doctype html><html><body>"
    '<header class="global-nav"><nav class="nav-links home-appear">'
    '<a href="/tools/index.html">Tools</a></nav></header>'
    '<main><div class="review-layout"><aside class="review-aside">'
    '<article class="score-card">4/5</article></aside></div></main>'
    '<footer class="footer"><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>'
    "</body></html>"
)
CHARGE = (
    "<!doctype html><html><body>"
    '<header class="global-nav"><nav class="nav-links"><a href="/tools/index.html">Tools</a></nav></header>'
    "<main><h1>This page cannot verify a charge.</h1></main>"
    '<footer class="footer"><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>'
    "</body></html>"
)
NEWSLETTER = (
    "<!doctype html><html><body>"
    '<header class="global-nav"><nav class="nav-links"><a href="/tools/index.html">Tools</a></nav></header>'
    "<main><div class=\"newsletter-body\">"
    '<section class="newsletter-segment newsletter-segment--keep"><p>Keep this tool</p></section>'
    '<section class="newsletter-segment newsletter-segment--cut"><p>Cut this tool</p></section>'
    "</div>"
    '<div class="newsletter-colophon"><p>Prices verified from official pages.</p></div>'
    "</main>"
    '<footer class="footer"><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>'
    "</body></html>"
)
ENROLLED = {
    "name": "Northwind",
    "pitch": PITCH,
    "href": "https://example.com/north",
    "logo": None,
}


def _write(root: Path, payload: dict) -> None:
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "sponsor_enrollment.json").write_text(json.dumps(payload), encoding="utf-8")


def _has(html: str, needle: str) -> None:
    if needle not in html:
        raise AssertionError("missing " + needle)


def _lacks(html: str, needle: str) -> None:
    if needle in html:
        raise AssertionError("unexpected " + needle)


def _raises(fn) -> None:
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_null_enrollment_offer_and_page() -> None:
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": None})
        write_page(root)
        offer = (root / "sponsor" / "index.html").read_text()
        for paragraph in OFFER:
            _has(offer, paragraph)
        _has(offer, MAILTO_BUTTON)
        _has(offer, QUESTIONS)
        _has(offer, "<title>Sponsor AIToolsEssentials</title>")
        _has(offer, '<header class="global-nav">')
        _has(offer, '<nav class="nav-links">')
        _has(offer, "</header>")
        _has(offer, '<footer class="footer">')
        _has(offer, 'href="mailto:contact@aitoolsessentials.com"')
        _has(offer, 'href="/css/styles.css"')
        _lacks(offer, "George")
        _lacks(offer, "$")
        _lacks(offer, "data-sponsor")
        _lacks(offer, "sponsor-line")
        _lacks(offer, 'href="/sponsor/"')
        _lacks(offer, 'data-footer="slim"')
        stamped = stamp(offer, "sponsor/index.html", root=root, env={})
        _lacks(stamped, "data-sponsor")
        _lacks(stamped, "sponsor-line")
        _lacks(stamped, "George")
        _lacks(stamped, "$")
        if stamped.count(HOUSE) != 1:
            raise AssertionError("offer page house link count " + str(stamped.count(HOUSE)))
        once = stamp(PAGE, "tools/acme/index.html", root=root, env={})
        twice = stamp(once, "tools/acme/index.html", root=root, env={})
        if twice != once:
            raise AssertionError("second stamp changed the page")
        _lacks(once, "data-sponsor")
        _lacks(once, "sponsor-line")
        if once.count(HOUSE) != 1 or once.count('href="/sponsor/"') != 1:
            raise AssertionError("expected one house link")
        if once.find(HOUSE) > once.find("</nav>"):
            raise AssertionError("house link is outside nav-links")
        _has(once, 'class="score-card"')
        first = (root / "sponsor" / "index.html").read_bytes()
        write_page(root)
        second = (root / "sponsor" / "index.html").read_bytes()
        if first != second:
            raise AssertionError("second write_page changed bytes")
        if b"What you get" not in first or MAILTO_BUTTON.encode() not in first:
            raise AssertionError("offer page lost its copy")


def test_checkout_is_unchanged() -> None:
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": ENROLLED})
        page = stamp(CHARGE, "checkout/complete/index.html", root=root, env={})
        if page != CHARGE:
            raise AssertionError("checkout page changed")
        _has(page, "cannot verify a charge")
    with TemporaryDirectory() as raw:
        root = Path(raw)
        page = stamp(CHARGE, "checkout/complete/index.html", root=root, env={})
        if page != CHARGE:
            raise AssertionError("checkout page changed without an enrollment file")
        _raises(lambda: stamp(PAGE, "index.html", root=root, env={}))


def test_house_link_cleanup_and_footer_fallback() -> None:
    dirty = (
        "<!doctype html><html><body>"
        '<header class="global-nav"><nav class="nav-links home-appear">'
        '<a href="/sponsor/">Old sponsor</a>'
        '<a href="/tools/index.html">Tools</a></nav></header>'
        "<main><p>Body copy</p></main>"
        '<footer class="footer"><a href="/sponsor/">Footer sponsor</a></footer>'
        "</body></html>"
    )
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": None})
        stamped = stamp(dirty, "tools/acme/index.html", root=root, env={})
        _lacks(stamped, "Old sponsor")
        _lacks(stamped, "Footer sponsor")
        _has(stamped, "Tools")
        _has(stamped, "Body copy")
        if stamped.count('href="/sponsor/"') != 1 or stamped.count(HOUSE) != 1:
            raise AssertionError("dirty page did not collapse to one house link")
    no_nav = (
        "<!doctype html><html><body><main><p>Body</p></main>"
        '<footer class="footer"><a href="/legal/about.html">About</a></footer>'
        "</body></html>"
    )
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": None})
        stamped = stamp(no_nav, "about/index.html", root=root, env={})
        if stamped.count(HOUSE) != 1:
            raise AssertionError("footer fallback missed the house link")
        if stamped.find(HOUSE) > stamped.find("</footer>"):
            raise AssertionError("house link is not inside the footer")
        _lacks(stamped, "</nav>")


def test_enrolled_line_after_footer() -> None:
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": ENROLLED})
        stamped = stamp(PAGE, "tools/acme/index.html", root=root, env={})
        twice = stamp(stamped, "tools/acme/index.html", root=root, env={})
        if twice != stamped:
            raise AssertionError("enrolled stamp was not idempotent")
        _has(stamped, EXTERNAL_LINE)
        _has(stamped, 'rel="external noopener nofollow"')
        _lacks(stamped, 'rel="sponsored"')
        _lacks(stamped, " sponsored=")
        footer_at = stamped.rfind("</footer>")
        main_at = stamped.rfind("</main>")
        line_at = stamped.find('data-sponsor="page-foot"')
        if line_at < 0 or footer_at < 0 or main_at < 0:
            raise AssertionError("missing footer, main, or sponsor line")
        if not (line_at > footer_at + len("</footer>") and footer_at > main_at):
            raise AssertionError("sponsor line is not after footer and main")
        paragraph = stamped[stamped.find('<p class="sponsor-line"'):line_at + 400]
        _lacks(paragraph, "score-card")
        _lacks(paragraph, "position:")
        _lacks(stamped, "George")
        if stamped.count(HOUSE) != 1:
            raise AssertionError("enrolled page house link count drifted")
        _lacks(stamped, 'data-sponsor="issue-colophon"')


def test_logo_house_href_and_full_pitch() -> None:
    pitch = "T" * 40
    payload = {
        "enrollment": {
            "name": "Northwind",
            "pitch": pitch,
            "href": "/partners/north",
            "logo": {"src": "/assets/north.png", "alt": "Northwind"},
        }
    }
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, payload)
        stamped = stamp(PAGE, "tools/acme/index.html", root=root, env={})
        _has(
            stamped,
            '<span class="sponsor-line-label">Sponsored</span> '
            '<img src="/assets/north.png" alt="Northwind"> '
            '<span class="sponsor-line-pitch">' + pitch + "</span> "
            '<a href="/partners/north" rel="nofollow">Northwind</a>',
        )
        line_at = stamped.find('<p class="sponsor-line"')
        paragraph = stamped[line_at:stamped.find("</p>", line_at)]
        _lacks(paragraph, 'target="_blank"')
        _lacks(paragraph, "external")


def test_refused_slots_and_no_body_fallback() -> None:
    beside = (
        "<!doctype html><html><body>"
        '<header class="global-nav"><nav class="nav-links"><a href="/tools/index.html">Tools</a></nav></header>'
        "<main><p>Body</p></main>"
        '<footer class="footer">Contact</footer><article class="score-card sa-rec">Score</article>'
        "</body></html>"
    )
    kept = (
        "<!doctype html><html><body>"
        '<header class="global-nav"><nav class="nav-links"><a href="/tools/index.html">Tools</a></nav></header>'
        '<main><section class="newsletter-segment newsletter-segment--keep">'
        '<div class="newsletter-colophon"><p>Inside keep</p></div></section></main>'
        '<footer class="footer">Contact</footer>'
        "</body></html>"
    )
    no_footer = (
        "<!doctype html><html><body>"
        '<header class="global-nav"><nav class="nav-links"><a href="/tools/index.html">Tools</a></nav></header>'
        "<main><p>Body</p></main></body></html>"
    )
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": ENROLLED})
        beside_out = stamp(beside, "tools/acme/index.html", root=root, env={})
        _has(beside_out, HOUSE)
        _lacks(beside_out, "data-sponsor")
        _lacks(beside_out, "sponsor-line")
        kept_out = stamp(kept, "newsletter/issue.html", root=root, env={})
        _lacks(kept_out, 'data-sponsor="issue-colophon"')
        _has(kept_out, EXTERNAL_LINE)
        if kept_out.find('data-sponsor="page-foot"') < kept_out.find("</footer>"):
            raise AssertionError("kept-colophon page put the line in the wrong place")
        bare = stamp(no_footer, "tools/acme/index.html", root=root, env={})
        _has(bare, HOUSE)
        _lacks(bare, "data-sponsor")
        if bare.find(HOUSE) > bare.find("</nav>"):
            raise AssertionError("house link fell through to the body")


def test_newsletter_colophon() -> None:
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": ENROLLED})
        stamped = stamp(NEWSLETTER, "newsletter/issue.html", root=root, env={})
        _has(stamped, ISSUE_LINE)
        _has(stamped, EXTERNAL_LINE)
        issue_at = stamped.find('data-sponsor="issue-colophon"')
        prices_at = stamped.find("Prices verified from official pages.")
        colophon_at = stamped.find('class="newsletter-colophon"')
        if not (colophon_at < issue_at < prices_at):
            raise AssertionError("issue line is not the first colophon child")
        keep_at = stamped.find("newsletter-segment--keep")
        cut_at = stamped.find("newsletter-segment--cut")
        if "data-sponsor" in stamped[keep_at:cut_at]:
            raise AssertionError("sponsor line landed in the keep segment")
        if stamped.find('data-sponsor="page-foot"') < stamped.rfind("</footer>"):
            raise AssertionError("page line is not after the footer")


def test_rejected_enrollment_values() -> None:
    base = {
        "name": "Northwind",
        "pitch": PITCH,
        "href": "https://example.com/north",
    }
    cases = []
    for key in ("pricing", "placement_id", "payment_url", "note"):
        cases.append({"enrollment": {**base, key: "nope"}})
    cases.append({"enrollment": None, "pricing": "9"})
    cases.append({"enrollment": {**base, "logo": {"src": "/a.png", "title": "x"}}})
    cases.append({"enrollment": {**base, "pitch": "T" * 41}})
    cases.append({"enrollment": {**base, "name": "George"}})
    cases.append({"enrollment": {**base, "name": "george"}})
    cases.append({"enrollment": {**base, "name": "GEORGE"}})
    cases.append({"enrollment": {**base, "pitch": "Meet George today"}})
    cases.append({"enrollment": {**base, "pitch": "Save $ now please"}})
    cases.append({"enrollment": {**base, "name": "A<b>B"}})
    cases.append({"enrollment": {**base, "href": "https://try.elevenlabs.io/join"}})
    cases.append({"enrollment": {**base, "href": "https://example.com/George"}})
    for payload in cases:
        with TemporaryDirectory() as raw:
            root = Path(raw)
            _write(root, payload)
            _raises(lambda: stamp(PAGE, "tools/acme/index.html", root=root, env={}))


def test_payment_url() -> None:
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": None})
        write_page(root, {"SPONSOR_PAYMENT_URL": ""})
        html = (root / "sponsor" / "index.html").read_text()
        _has(html, MAILTO_BUTTON)
        _has(html, QUESTIONS)
        _lacks(html, "${")
        _lacks(html, "SPONSOR_PAYMENT_URL")
        write_page(root, {"SPONSOR_PAYMENT_URL": " \n "})
        blank = (root / "sponsor" / "index.html").read_text()
        _has(blank, MAILTO_BUTTON)
        _lacks(blank, "${")
        write_page(root, {"SPONSOR_PAYMENT_URL": "https://pay.example.com/sponsor"})
        paid = (root / "sponsor" / "index.html").read_text()
        _has(paid, HTTPS_BUTTON)
        _has(paid, QUESTIONS)
        _has(paid, "aitoolsessentials@gmail.com")
        _lacks(paid, MAILTO_BUTTON)
        _lacks(paid, "${")
        _lacks(paid, "George")
    for bad in (
        "https://pay.example.com/SPONSOR_PAYMENT_URL",
        "SPONSOR_PAYMENT_URL",
        "https://pay.example.com/${user}",
        "https://try.elevenlabs.io/pay",
    ):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            _write(root, {"enrollment": None})
            _raises(lambda: write_page(root, {"SPONSOR_PAYMENT_URL": bad}))
            if (root / "sponsor" / "index.html").exists():
                raise AssertionError("bad payment URL was written")


def test_stamp_site_walk() -> None:
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": None})
        tools = root / "tools" / "acme" / "index.html"
        tools.parent.mkdir(parents=True)
        tools.write_text(PAGE)
        checkout = root / "checkout" / "complete" / "index.html"
        checkout.parent.mkdir(parents=True)
        checkout.write_text(CHARGE)
        admin = root / "admin" / "secret.html"
        admin.parent.mkdir(parents=True)
        admin.write_text(PAGE)
        changed = stamp_site(root)
        if changed != 1:
            raise AssertionError("stamp_site changed " + str(changed) + " files")
        stamped = tools.read_text()
        _has(stamped, HOUSE)
        _lacks(stamped, "data-sponsor")
        _lacks(stamped, "sponsor-line")
        if checkout.read_text() != CHARGE:
            raise AssertionError("stamp_site rewrote checkout")
        if admin.read_text() != PAGE:
            raise AssertionError("stamp_site rewrote admin")
        if stamp_site(root) != 0:
            raise AssertionError("second stamp_site rewrote a page")
    with TemporaryDirectory() as raw:
        root = Path(raw)
        _write(root, {"enrollment": ENROLLED})
        issue = root / "newsletter" / "issue.html"
        issue.parent.mkdir(parents=True)
        issue.write_text(NEWSLETTER)
        admin = root / "admin" / "newsletter" / "issue.html"
        admin.parent.mkdir(parents=True)
        admin.write_text(NEWSLETTER)
        changed = stamp_site(root)
        if changed != 1:
            raise AssertionError("enrolled walk changed " + str(changed) + " files")
        text = issue.read_text()
        _has(text, EXTERNAL_LINE)
        _has(text, ISSUE_LINE)
        if text.find('data-sponsor="page-foot"') < text.rfind("</footer>"):
            raise AssertionError("walk put the line before the footer")
        if admin.read_text() != NEWSLETTER:
            raise AssertionError("walk stamped an admin newsletter")
        if stamp_site(root) != 0:
            raise AssertionError("second enrolled walk rewrote a page")


def main() -> None:
    tests = (
        test_null_enrollment_offer_and_page,
        test_checkout_is_unchanged,
        test_house_link_cleanup_and_footer_fallback,
        test_enrolled_line_after_footer,
        test_logo_house_href_and_full_pitch,
        test_refused_slots_and_no_body_fallback,
        test_newsletter_colophon,
        test_rejected_enrollment_values,
        test_payment_url,
        test_stamp_site_walk,
    )
    errors: list[str] = []
    for test in tests:
        try:
            test()
        except Exception as exc:
            errors.append(test.__name__ + ": " + str(exc))
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
