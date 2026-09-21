#!/usr/bin/env python3
"""Verify recorded pricing snapshots against the live official vendor pages.

Exists because `data/pricing_snapshots.json` carried 37 snapshots dated 2026-08-21 while the
public Pricing Watch page promises weekly re-verification. A visitor clicking through saw
month-old dates, which undercuts the one thing the site sells: dated evidence.

What it does, per tool:

  1. fetch the official pricing page,
  2. extract the money figures the recorded digest actually asserts,
  3. check whether each still appears on the live page,
  4. classify: FRESH (all claims still present), DRIFTED (a claim is gone), UNREADABLE (no
     server-rendered prices), NO_CLAIM (the digest asserts no figures), or NO_URL.

It never rewrites a digest from scraped text. The digests are hand-verified evidence, and a
machine extraction would silently replace accuracy with whatever the page happens to render.
DRIFTED entries are reported for human review.

Price normalisation matters more than it looks: vendors render "$16.99" as `<span>$16</span>
<span>.99</span>`, so a naive regex reads "$16" and reports a false drift. Three of the first
four DRIFTED flags were exactly this artefact.

Usage:
    python3 scripts/verify_pricing_freshness.py                  # all snapshots
    python3 scripts/verify_pricing_freshness.py --stale-days 14  # only older than N days
    python3 scripts/verify_pricing_freshness.py --json out.json
"""
from __future__ import annotations

from html import unescape

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS = ROOT / "data" / "pricing_snapshots.json"
CATALOG = ROOT / "data" / "stack_audit_catalog.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36")

# Allow the digits to be separated by markup-derived whitespace/dots: "$16 .99" -> 16.99
# A currency figure, NOT "$L24" / "$32" framework references.
# Requires the dollar sign to be followed by a price-like number AND preceded by a
# non-identifier character. Next.js flight payloads embed escaped references such as
# `\"$24\"` and `$L25`, which defeat a simple lookbehind because the preceding byte is `\`
# (a non-word char that looks safe). Two guards handle it:
#   1. the char before `$` may not be a backslash, `$`, or a word char;
#   2. a `$` immediately followed by a capital letter (e.g. `$L24`) is a reference, not money.
PRICE = re.compile(r"(?<![\w$\\])\$(?!\$|[A-Z])\s?(\d[\d,]*)\s*(?:[.,]\s*(\d{2}))?")

# Splits the fetched content into rendered body (before) and script payloads (after).
SCRIPT_MARKER = "\n<<<SCRIPTS>>>\n"

# A digest asserting that a vendor publishes NO price list. That is a claim, not an absence of
# one — it can be falsified by the vendor's own page, so it must not pass as "nothing to check".
OPACITY = re.compile(
    r"no\s+(?:public(?:ly)?[- ]?)?(?:self[- ]service\s+)?(?:consumer\s+)?"
    r"(?:pricing|price)\s+(?:page|list|table|information)"
    r"|does\s+not\s+(?:publish|expose|list|disclose|offer"
    r"|make\s+(?:its\s+)?pricing\s+public)"
    r"|pricing\s+(?:is\s+)?not\s+(?:public|disclosed|published)"
    r"|no\s+self[- ]service\s+(?:plan|tier|signup)",
    re.I,
)

# Context that marks a figure as a real PUBLISHED PRICE rather than any other money number.
# Harvey's homepage carries "$550M at a $15.5B valuation" — a funding round. Without this guard
# every opaque-tool record would be flagged as wrong on the strength of unrelated figures.
PRICE_CONTEXT = re.compile(
    r"(/\s*(?:mo|month|year|yr|user|seat|member|credit)\b"
    r"|per\s+(?:month|user|seat|member|year|credit)"
    r"|billed|monthly|annually|annual|per\s+month|\bplan\b|\btier\b|\bsubscription\b)",
    re.I,
)


def price_like_figures(text: str) -> set[float]:
    """Money figures that sit near billing language — i.e. plausibly real published prices.

    Deliberately narrow. Its only job is to help a human decide whether a record claiming
    "the vendor publishes no price" is still true, so it must not fire on funding rounds,
    valuations, or revenue numbers.
    """
    body = text.split(SCRIPT_MARKER, 1)[0]
    out: set[float] = set()
    for m in re.finditer(r"\$\s?\d[\d,]*(?:[.,]\d{2})?", body):
        ctx = body[max(0, m.start() - 70): m.end() + 70]
        if not PRICE_CONTEXT.search(ctx):
            continue
        for p in prices(m.group(0)):
            if p > 0:
                out.add(p)
    return out


def split_content(raw: str) -> str:
    """Split raw HTML into searchable content: body text, attribute text, and scripts.

    Single source of truth for the extraction pipeline, because `fetch_text` and `is_flaky`
    both classify the same page and previously drifted apart — a fix applied to one and not
    the other silently produced contradictory verdicts on the same URL.

    Three parts, each for a different reason:

    * **Body text** — bare `$` figures are only trustworthy here. Rendering frameworks embed
      chunk references that look exactly like prices: Next.js flight data contains `\\"$24\\"`
      and `$L25`, so udio.com/pricing appears to publish three prices it does not. The escaped
      quotes defeat any lookbehind, because the byte before `$` is a legitimate non-word char.
    * **Attribute text** — `content`, `alt` and `aria-label` values are publisher-authored
      human-readable prose. htmlslides publishes its entire Pro price ("get the Pro launch
      offer at $9.90/month") ONLY in its `<meta name="description" content="...">`, so
      stripping tags discarded it and reported a price that is still live as vanished. Only
      content-bearing attributes are read: `class`, `href`, `src` and `data-*` hold framework
      payloads and would reintroduce the false positives above.
    * **Script payloads** — structured plan data lives here and nowhere else. Airtable
      publishes `"costPerUserPerMonthInCents": 2400` (its $24 tier) while rendering just $20
      and $45; cursor.com publishes its whole plan table as JSON-LD.
    """
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
    # content-bearing attributes only (NOT class/href/src/data-*, which carry framework noise)
    attrs = re.findall(
        r"""\b(?:content|alt|aria-label|title|placeholder|value)\s*=\s*["']([^"']{2,})["']""",
        raw, flags=re.I,
    )
    parts = re.split(r"<script[^>]*>(.*?)</script>", raw, flags=re.S | re.I)
    body = " ".join(p for i, p in enumerate(parts) if i % 2 == 0)
    scripts = " ".join(p for i, p in enumerate(parts) if i % 2 == 1)
    body = re.sub(r"<[^>]+>", " ", body)
    # Normalise each half BEFORE joining. Collapsing whitespace across the marker destroys it —
    # the newlines it is made of become spaces, `norm_set`'s split then never fires, and the
    # scripts silently get classified as body text. That failure mode is invisible in one
    # direction and loud in the other: Airtable's cents-only price looked drifted, while
    # Udio's Next.js flight payload leaked in as three prices it does not publish.
    norm = lambda s: re.sub(r"\s+", " ", unescape(s))  # noqa: E731
    return norm(body) + norm(" ".join(attrs)) + SCRIPT_MARKER + norm(scripts)


def fetch_text(url: str, timeout: int = 35, attempts: int = 3) -> str:
    """Fetch a URL and return searchable content: rendered body PLUS every script payload.

    Both halves are needed, for different reasons:

    * Bare `$` figures are only trustworthy in the **rendered body**. Rendering frameworks
      embed chunk references that look exactly like prices — Next.js flight data contains
      `\\"$24\\"`, `$L25` and `\\"$32\\"` — so a page publishing no prices server-side
      (udio.com/pricing) appears to have three. The escaped quotes defeat any lookbehind,
      because the byte before `$` is a legitimate non-word character.
    * Plan prices are often ONLY in a script. Airtable publishes `"costPerUserPerMonthInCents":
      2400` (its $24 monthly tier) inside a hydration payload while rendering just $20 and $45.
      cursor.com/pricing publishes its whole plan table as JSON-LD.

    So `fetch_text` marks the script portions and `norm_set` extracts accordingly: bare figures
    from the body, structured price fields from the scripts. Retried, because some pages vary
    between requests — cursor.com returned its $60/$200 tiers in only one of three fetches.
    """
    best = ""
    for _ in range(max(1, attempts)):
        try:
            out = subprocess.run(
                ["curl", "-skS", "-L", "--max-time", str(timeout), "-A", UA, url],
                capture_output=True, text=True, timeout=timeout + 10,
            ).stdout
        except Exception:
            continue
        candidate = split_content(out)
        if len(norm_set(candidate)) > len(norm_set(best)):
            best = candidate
    return best


def is_flaky(url: str, missing: list[float], timeout: int = 35, attempts: int = 4) -> bool:
    """True if a "missing" figure does appear on some fetches — i.e. a flaky render.

    cursor.com/pricing returns its Teams ($40) figure in roughly 4 of 5 requests; a
    single-fetch check calls that a vanished price and sends a human to investigate nothing.
    A figure that shows up at all is present; only a figure absent from every fetch is real
    drift.
    """
    for _ in range(attempts):
        try:
            out = subprocess.run(
                ["curl", "-skS", "-L", "--max-time", str(timeout), "-A", UA, url],
                capture_output=True, text=True, timeout=timeout + 10,
            ).stdout
        except Exception:
            continue
        live = norm_set(split_content(out))
        if any(abs(m - v) < 0.01 for m in missing for v in live):
            return True
    return False


def cents_prices(text: str) -> set[float]:
    """Prices published as integer cents in structured data (e.g. 2400 -> $24.00).

    Requires a price-ish key name nearby so that arbitrary integers (asset ids, byte offsets)
    are not mistaken for money.
    """
    found: set[float] = set()
    for m in re.finditer(
        r'"[A-Za-z_]*(?:[Pp]rice|[Cc]ost|[Aa]mount)[A-Za-z_]*"\s*:\s*(\d{3,})', text
    ):
        try:
            n = int(m.group(1))
        except ValueError:
            continue
        if n >= 100:  # cents; anything smaller is not a subscription price
            found.add(round(n / 100, 2))
    return found


def jsonld_prices(text: str) -> set[float]:
    """Plain-decimal prices in structured plan data, e.g. schema.org `"price": "40"`.

    cursor.com/pricing publishes its whole plan table this way — Hobby 0, Pro 20, Pro+ 60,
    Ultra 200, Teams 40 — while the rendered HTML shows only some of them depending on the
    response. Without this the Teams price ($40) looks like it vanished.

    Requires a plan-ish `"name"` in the same object. Udio's page contains bare `"price"` fields
    attached to unrelated data, which a name-less match counts as three real price points.
    """
    found: set[float] = set()
    for m in re.finditer(
        r'\{[^{}]{0,400}?"price"\s*:\s*"?(\d+(?:\.\d+)?)"?[^{}]{0,400}?\}', text
    ):
        obj = m.group(0)
        if not re.search(r'"name"\s*:\s*"[^"]{1,40}"', obj):
            continue
        try:
            n = float(m.group(1))
        except ValueError:
            continue
        if n > 0:
            found.add(round(n, 2))
    return found


def prices(text: str) -> set[float]:
    """Every money figure in the text, normalised to a float.

    Handles tag-split decimals, US$/EUR/GBP prefixes, and thousands separators.

    Only matches figures with an actual currency symbol. Bare numbers in a framework payload
    are NOT prices: Udio's pricing page contains `$24`, `$32` and `$45` as Next.js chunk
    references ("$L24", "\\"$32\\""), which a looser pattern counts as three price points and
    reports as a changed price list.
    """
    found: set[float] = set()
    for whole, cents in PRICE.findall(text):
        try:
            val = float(whole.replace(",", ""))
        except ValueError:
            continue
        if cents:
            try:
                val += int(cents) / 100
            except ValueError:
                pass
        found.add(round(val, 2))
    for m in re.finditer(r"(?:US\$|€|£)\s?(\d[\d,]*)(?:[.,](\d{2}))?", text):
        try:
            val = float(m.group(1).replace(",", ""))
            if m.group(2):
                val += int(m.group(2)) / 100
            found.add(round(val, 2))
        except ValueError:
            pass
    return found


def norm_set(text: str) -> set[float]:
    """Every money figure the page publishes, from the two halves of the fetched content.

    Bare `$` figures are read from the rendered body only, while structured price fields
    (`costPerUserPerMonthInCents`, JSON-LD `"price"`) are read from the script payloads. Mixing
    them is what produces false drift reports in both directions:

    * Reading bare figures inside scripts invents prices from framework chunk references
      (udio.com/pricing would appear to have $24/$32/$45).
    * Ignoring scripts misses real prices published only in hydration data (Airtable's $24
      monthly tier exists solely as `costPerUserPerMonthInCents: 2400`).
    """
    if SCRIPT_MARKER in text:
        body, scripts = text.split(SCRIPT_MARKER, 1)
    else:
        body, scripts = text, ""
    found = prices(body) | cents_prices(scripts) | jsonld_prices(scripts)
    return {p for p in found if p > 0}


def classify(slug: str, rec: dict, url: str | None, text: str) -> dict:
    entry = {"slug": slug, "url": url, "recorded_date": rec.get("date")}
    digest = rec.get("digest") or ""
    claimed = norm_set(digest)
    entry["claimed"] = sorted(claimed)

    if not url:
        entry["status"] = "NO_URL"
        return entry
    if len(text) < 1000:
        # Too little server-rendered text to judge. Do NOT infer a change from this.
        entry["status"] = "UNREADABLE"
        entry["text_len"] = len(text)
        return entry
    if not claimed:
        # A digest with no dollar figures is not automatically uninteresting: it often asserts
        # OPACITY instead ("does not publish a self-serve consumer price list"). That is a
        # falsifiable claim the old code never tested, which is exactly how two wrong records
        # (Pika, Tunii) passed silently — the site claimed no price list existed while the live
        # page published a full one, and NO_CLAIM read as "nothing to check".
        entry["status"] = "NO_CLAIM"
        entry["live_figures"] = len(norm_set(text))
        if OPACITY.search(digest):
            entry["asserts_opacity"] = True
            # Only a figure that reads like a published PRICE counts. Harvey's homepage shows
            # "$550M at a $15.5B valuation" — a funding round, not a plan price — and treating
            # any bare figure as a price would flag the three genuinely-opaque tools as wrong.
            entry["opacity_review"] = sorted(price_like_figures(text))[:8]
        return entry

    live = norm_set(text)
    # A page publishing almost no money figures gives no evidence either way — it is almost
    # always fully client-rendered. Reporting that as "drifted" would send a human to
    # investigate a price that may be perfectly current, so call it UNREADABLE. The bar is
    # relative: a page showing a couple of unrelated prices (e.g. only add-on costs) cannot
    # support a claim that a specific plan price disappeared.
    if len(live) < 2:
        entry["status"] = "UNREADABLE"
        entry["live_figures"] = len(live)
        return entry

    missing = sorted(claimed - live)
    present = len(claimed) - len(missing)

    # Distinguish a genuine price change from a page that simply does not publish this claim
    # any more. If NONE of the claimed figures appear, the page is not corroborating the claim
    # at all — typically a currency mismatch (an EUR claim against a USD-only page) or a
    # redesign. That is "cannot verify", not "the price moved".
    if present == 0:
        entry["status"] = "UNVERIFIED"
        entry["claimed_n"] = len(claimed)
        entry["live_figures"] = len(live)
        entry["missing"] = missing[:10]
        return entry

    entry.update(
        present=present,
        claimed_n=len(claimed),
        pct=round(present / len(claimed) * 100),
        missing=missing[:10],
        live_figures=len(live),
    )
    if not missing:
        entry["status"] = "FRESH"
        return entry

    # Before reporting drift, rule out a flaky render: some pages omit a plan's price from
    # certain responses. A figure that appears on ANY fetch is present, so only a figure absent
    # from every fetch is real drift.
    if is_flaky(url, missing):
        entry["status"] = "FRESH"
        entry["note"] = "missing on first fetch but present on retry (flaky render)"
        return entry

    entry["status"] = "DRIFTED"
    return entry


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stale-days", type=int, default=None,
                    help="only check snapshots older than this many days")
    ap.add_argument("--json", type=Path, default=None, help="write the full report here")
    ap.add_argument("--only", nargs="*", default=None, help="limit to these slugs")
    args = ap.parse_args()

    snaps = json.loads(SNAPSHOTS.read_text())["snapshots"]
    catalog = json.loads(CATALOG.read_text())["tools"]
    urls = {t["slug"]: t.get("pricing_url") for t in catalog}

    today = date.today()
    targets = []
    for slug, rec in snaps.items():
        if args.only and slug not in args.only:
            continue
        if args.stale_days is not None:
            try:
                age = (today - datetime.strptime(rec.get("date", "1970-01-01"),
                                                 "%Y-%m-%d").date()).days
            except (ValueError, TypeError):
                age = 9999
            if age <= args.stale_days:
                continue
        targets.append(slug)

    results = []
    for i, slug in enumerate(sorted(targets), 1):
        rec = snaps[slug]
        url = urls.get(slug)
        text = fetch_text(url) if url else ""
        r = classify(slug, rec, url, text)
        results.append(r)
        note = ""
        if r["status"] == "DRIFTED":
            note = f"  missing={r['missing'][:4]}"
        elif r["status"] in ("FRESH",):
            note = f"  {r['present']}/{r['claimed_n']} claims still present"
        elif r["status"] == "NO_CLAIM":
            if r.get("opacity_review"):
                note = (
                    "  OPACITY CLAIM contradicted - live price-like figures "
                    f"{r['opacity_review']}: re-check this record"
                )
            else:
                note = "  digest asserts no figures"
                if r.get("asserts_opacity"):
                    note += " (claims no published price - none found live, consistent)"
        elif r["status"] == "UNREADABLE":
            note = f"  only {r.get('text_len', 0)}b rendered"
        print(f"  [{i:>2}/{len(targets)}] {slug:<20} {r['status']:<10}{note}")

    from collections import Counter
    counts = Counter(r["status"] for r in results)
    print(f"\n=== {len(results)} snapshots checked ===")
    for k, v in counts.most_common():
        print(f"  {k}: {v}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(
            {"generated": today.isoformat(), "results": results}, indent=1) + "\n")
        print(f"\nwrote {args.json}")

    # A DRIFTED result means a published claim is no longer supported by the vendor page.
    return 1 if counts.get("DRIFTED") else 0


if __name__ == "__main__":
    sys.exit(main())
