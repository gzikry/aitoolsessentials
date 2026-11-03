#!/usr/bin/env python3
"""Partner CTAs must land on rel="sponsored nofollow noopener".

A link that starts as rel="external nofollow" is still a partner CTA. So is
the Hermes homepage, whose official URL lives under /docs, and a hop that
already says sponsored nofollow but is missing noopener. Citation labels stay
on the official URL.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import wire_affiliate_links as wire

PARTNER_REL = 'rel="sponsored nofollow noopener"'
ELEVEN = {
    "slug": "elevenlabs",
    "name": "ElevenLabs",
    "official": "https://elevenlabs.io/",
    "affiliate": "https://try.elevenlabs.io/xs6witq7izqe",
    "public": "/go/elevenlabs/",
}
HERMES = {
    "slug": "hermes-agent",
    "name": "Hermes Agent",
    "official": "https://hermes-agent.nousresearch.com/docs/",
    "affiliate": "https://portal.nousresearch.com/r/george-zikry",
    "public": "/go/nous/",
}
PARTNERS = [ELEVEN, HERMES]


def _expect(html: str, needle: str) -> None:
    if needle not in html:
        raise SystemExit(f"missing {needle!r} in {html}")


def _reject(html: str, needle: str) -> None:
    if needle in html:
        raise SystemExit(f"unexpected {needle!r} in {html}")


def test_external_nofollow_becomes_sponsored_hop() -> None:
    source = '<a href="https://elevenlabs.io/" rel="external nofollow">Try ElevenLabs</a>'
    updated = wire._rewrite_tags(source, PARTNERS)
    _expect(updated, '<a href="/go/elevenlabs/" rel="sponsored nofollow noopener">Try ElevenLabs</a>')
    _reject(updated, "external nofollow")


def test_external_nofollow_on_existing_hop_gains_sponsored() -> None:
    source = '<a href="/go/elevenlabs/" rel="external nofollow">Try ElevenLabs</a>'
    updated = wire._rewrite_tags(source, PARTNERS)
    _expect(updated, f'<a href="/go/elevenlabs/" {PARTNER_REL}>Try ElevenLabs</a>')


def test_sponsored_nofollow_without_noopener_is_completed() -> None:
    source = '<a href="/go/elevenlabs/" rel="sponsored nofollow">Try ElevenLabs</a>'
    updated = wire._rewrite_tags(source, PARTNERS)
    _expect(updated, f'<a href="/go/elevenlabs/" {PARTNER_REL}>Try ElevenLabs</a>')


def test_hermes_docs_homepage_visit_is_a_partner_cta() -> None:
    source = '<a href="https://hermes-agent.nousresearch.com/docs/" rel="external nofollow">Visit site</a>'
    updated = wire._rewrite_tags(source, PARTNERS)
    _expect(updated, f'<a href="/go/nous/" {PARTNER_REL}>Visit site</a>')
    _reject(updated, "external nofollow")


def test_hermes_docs_citation_stays_official() -> None:
    source = (
        '<a href="https://hermes-agent.nousresearch.com/docs/" rel="external nofollow" target="_blank">'
        "Official pricing ↗</a>"
    )
    updated = wire._rewrite_tags(source, PARTNERS)
    _expect(updated, 'href="https://hermes-agent.nousresearch.com/docs/"')
    _expect(updated, 'rel="external nofollow"')
    _reject(updated, "/go/nous/")


def test_pricing_citation_is_not_a_cta() -> None:
    source = '<a href="https://elevenlabs.io/pricing" rel="external nofollow">Pricing ↗</a>'
    updated = wire._rewrite_tags(source, PARTNERS)
    if updated != source:
        raise SystemExit(f"pricing citation was rewritten: {updated}")


def test_directory_visit_rel_order_is_rewritten() -> None:
    source = (
        '<a class="button button-blue small" href="https://elevenlabs.io/" '
        'rel="external noopener nofollow" target="_blank">Visit site</a>'
    )
    updated = wire._rewrite_tags(source, PARTNERS)
    _expect(updated, f'href="/go/elevenlabs/" {PARTNER_REL}')
    _reject(updated, "target=")
    _reject(updated, "external")


def test_hub_mention_without_tool_link() -> None:
    html = "<p>Deck cost prices Gamma, Canva AI, and Make.</p>"
    gamma = {"slug": "gamma", "name": "Gamma", "official": "https://gamma.app/", "affiliate": "https://try.gamma.app/x", "public": "/go/gamma/"}
    if not wire._mentioned(html, "comparisons/index.html", gamma):
        raise SystemExit("comparison hub mention was missed")
    if wire._mentioned(html, "articles/example.html", gamma):
        raise SystemExit("article mention should stay out of this pass")


def test_app_builder_hops_get_rel_and_disclosure() -> None:
    source = (
        '<p><a href="/go/v0/">Try v0</a> · <a href="/go/bolt-new/">Try Bolt.new</a> · '
        '<a href="/go/lovable/">Try Lovable</a> · <a href="/go/replit-ai/">Try Replit</a></p>'
    )
    updated = wire._wire_app_builder_links(source)
    for href in ("/go/v0/", "/go/bolt-new/", "/go/lovable/", "/go/replit-ai/"):
        _expect(updated, f'href="{href}" rel="external noopener"')
    _expect(updated, "Some outbound links may earn a partner commission")
    _expect(updated, 'href="/legal/affiliate-disclosure.html"')
    _reject(updated, "sponsored")
    again = wire._wire_app_builder_links(updated)
    if again != updated:
        raise SystemExit("app-builder wiring was not idempotent")


def main() -> None:
    test_external_nofollow_becomes_sponsored_hop()
    test_external_nofollow_on_existing_hop_gains_sponsored()
    test_sponsored_nofollow_without_noopener_is_completed()
    test_hermes_docs_homepage_visit_is_a_partner_cta()
    test_hermes_docs_citation_stays_official()
    test_pricing_citation_is_not_a_cta()
    test_directory_visit_rel_order_is_rewritten()
    test_hub_mention_without_tool_link()
    test_app_builder_hops_get_rel_and_disclosure()
    print("affiliate wiring checks passed")


if __name__ == "__main__":
    main()
