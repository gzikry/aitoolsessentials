#!/usr/bin/env python3
"""Re-check official pricing pages and report price-figure drift.

The previous version never requested a vendor page. It stored an empty body
for the first five slugs, then treated a missing stored hash as "no change",
so a run over all 105 tools finished in under a second with
"No changes detected."

This version fetches each tool's official pricing URL and compares the dollar
figures in the recorded snapshot with figures on the live page. It uses the
same extraction as scripts/verify_pricing_freshness.py, which ignores
framework chunk ids that look like prices.

It does not rewrite a digest from scraped HTML. Those sentences are
hand-verified. A failed or unreadable fetch is reported as unverified and is
not counted as "no change".

Usage:
    python3 scripts/recheck_pricing.py
    python3 scripts/recheck_pricing.py --only claude elevenlabs
    python3 scripts/recheck_pricing.py --json /tmp/recheck.json --pages-dir /tmp/recheck-pages
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_pricing_freshness import (  # noqa: E402
    UA,
    classify,
    norm_set,
    split_content,
)

SITE_ROOT = Path(__file__).resolve().parent.parent
PRICING_DATA = SITE_ROOT / "data" / "pricing_snapshots.json"
SOURCES = SITE_ROOT / "data" / "tool_sources.json"
CATALOG = SITE_ROOT / "data" / "stack_audit_catalog.json"

def _http_url(value: object) -> str:
    text = str(value or "").strip()
    if text.startswith("http://") or text.startswith("https://"):
        return text
    return ""


def load_urls() -> dict[str, str]:
    """Official pricing URL for each tracked slug.

    tool_sources.json is what the public Pricing Watch page links. The catalog
    and a snapshot's verified_against field are fallbacks when that URL is blank.
    """
    urls: dict[str, str] = {}
    if CATALOG.is_file():
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        for tool in catalog.get("tools", []):
            slug = tool.get("slug")
            url = _http_url(tool.get("pricing_url"))
            if slug and url:
                urls[slug] = url
    if SOURCES.is_file():
        sources = json.loads(SOURCES.read_text(encoding="utf-8"))
        for tool in sources.get("tools", []):
            slug = tool.get("slug")
            url = _http_url(tool.get("pricing_url"))
            if slug and url:
                urls[slug] = url
    return urls


def _curl(url: str, timeout: int) -> str:
    return subprocess.run(
        ["curl", "-skL", "--max-time", str(timeout), "-A", UA, url],
        capture_output=True,
        text=True,
        timeout=timeout + 10,
    ).stdout or ""


def check_one(slug: str, rec: dict, url: str, timeout: int, attempts: int) -> dict:
    """Fetch one pricing page and classify it. Never raises.

    Keeps the longest useful body. verify_pricing_freshness.fetch_text drops a
    response that parses to zero prices, which made a real page look like a
    zero-byte fetch.
    """
    if not url:
        return classify(slug, rec, None, "")
    best_text = ""
    best_prices = -1
    http_bytes = 0
    error = ""
    for _ in range(max(1, attempts)):
        try:
            raw = _curl(url, timeout)
        except Exception as exc:  # noqa: BLE001 — one vendor must not abort the run
            error = str(exc)
            continue
        http_bytes = max(http_bytes, len(raw))
        text = split_content(raw) if raw else ""
        n_prices = len(norm_set(text)) if text else 0
        if n_prices > best_prices or (n_prices == best_prices and len(text) > len(best_text)):
            best_prices = n_prices
            best_text = text
    entry = classify(slug, rec, url, best_text)
    entry["fetched_chars"] = len(best_text)
    entry["http_bytes"] = http_bytes
    if error and not best_text:
        entry["error"] = error
    if best_text:
        body = best_text.split("\n<<<SCRIPTS>>>\n", 1)[0]
        entry["excerpt"] = body[:4000]
    return entry


def is_price_change(entry: dict) -> bool:
    """True only when the live page contradicts a recorded price claim."""
    if entry.get("status") == "DRIFTED":
        return True
    if entry.get("status") == "NO_CLAIM" and entry.get("opacity_review"):
        return True
    return False


def summary_line(entry: dict) -> str:
    status = entry.get("status", "?")
    note = ""
    if status == "DRIFTED":
        note = f"  missing={entry.get('missing', [])[:6]}"
    elif status == "FRESH":
        note = f"  {entry.get('present')}/{entry.get('claimed_n')} claims still present"
        if entry.get("note"):
            note += f" ({entry['note']})"
    elif status == "NO_CLAIM":
        if entry.get("opacity_review"):
            note = f"  opacity claim contradicted by {entry['opacity_review']}"
        elif entry.get("asserts_opacity"):
            note = "  no published price, consistent with the live page"
        else:
            note = "  digest asserts no figures"
    elif status == "UNREADABLE":
        note = f"  only {entry.get('text_len', entry.get('fetched_chars', 0))} chars rendered"
    elif status == "UNVERIFIED":
        note = f"  none of {entry.get('claimed_n')} claims found among {entry.get('live_figures')} live figures"
    elif status == "NO_URL":
        note = "  no official pricing URL"
    if entry.get("error"):
        note += f"  error={entry['error']}"
    return f"  {entry['slug']:<22} {status:<12}{note}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch official pricing pages and report drift.")
    parser.add_argument("--only", nargs="*", default=None, help="limit to these slugs")
    parser.add_argument("--json", type=Path, default=None, help="write the full report here")
    parser.add_argument("--pages-dir", type=Path, default=None, help="write a text excerpt per slug")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--attempts", type=int, default=2)
    args = parser.parse_args()

    data = json.loads(PRICING_DATA.read_text(encoding="utf-8")) if PRICING_DATA.is_file() else {}
    snapshots = data.get("snapshots", {})
    urls = load_urls()
    for slug, rec in snapshots.items():
        if not urls.get(slug):
            fallback = _http_url(rec.get("verified_against"))
            if fallback:
                urls[slug] = fallback

    slugs = sorted(snapshots)
    if args.only:
        wanted = set(args.only)
        missing = sorted(wanted - set(slugs))
        if missing:
            print("Unknown slugs: " + ", ".join(missing), file=sys.stderr)
            return 2
        slugs = [slug for slug in slugs if slug in wanted]

    print(f"Fetching official pricing pages for {len(slugs)} tools...")
    results: list[dict] = []
    workers = max(1, args.workers)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(
                check_one,
                slug,
                snapshots[slug],
                urls.get(slug, ""),
                args.timeout,
                args.attempts,
            ): slug
            for slug in slugs
        }
        done = 0
        for future in as_completed(futures):
            done += 1
            entry = future.result()
            results.append(entry)
            print(f"[{done:>3}/{len(slugs)}]{summary_line(entry)}", flush=True)

    results.sort(key=lambda item: item["slug"])
    changes = [entry for entry in results if is_price_change(entry)]
    unverified = [
        entry for entry in results
        if entry.get("status") in {"UNREADABLE", "UNVERIFIED", "NO_URL"}
    ]
    fresh = [entry for entry in results if entry.get("status") in {"FRESH", "NO_CLAIM"} and not is_price_change(entry)]

    print()
    print(f"Fetched {len(results)} tools.")
    print(f"  confirmed price changes: {len(changes)}")
    print(f"  still match the recorded figures: {len(fresh)}")
    print(f"  unverified (not treated as unchanged): {len(unverified)}")
    if changes:
        print("\nPrice changes:")
        for entry in changes:
            print(summary_line(entry))
            if entry.get("url"):
                print(f"    source: {entry['url']}")

    # "No changes detected." is only honest when every requested page was
    # fetched and none of them contradicted a recorded figure.
    if changes:
        verdict = "Changes detected."
        code = 1
    elif unverified or len(fresh) != len(results):
        verdict = (
            "No confirmed price changes. "
            f"{len(unverified)} tools could not be verified from the fetched page "
            "and were not treated as unchanged."
        )
        code = 2
    else:
        verdict = "No changes detected."
        code = 0
    print(f"\n{verdict}")

    if args.pages_dir:
        args.pages_dir.mkdir(parents=True, exist_ok=True)
        for entry in results:
            excerpt = entry.get("excerpt") or ""
            (args.pages_dir / f"{entry['slug']}.txt").write_text(
                f"url: {entry.get('url') or ''}\nstatus: {entry.get('status')}\n\n{excerpt}\n",
                encoding="utf-8",
            )

    if args.json:
        payload = []
        for entry in results:
            item = dict(entry)
            item.pop("excerpt", None)
            payload.append(item)
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(
                {
                    "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "verdict": verdict,
                    "results": payload,
                },
                indent=1,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.json}")

    return code


if __name__ == "__main__":
    sys.exit(main())
