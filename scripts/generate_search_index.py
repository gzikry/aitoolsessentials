#!/usr/bin/env python3
"""Build `data/search_index.json` from the pages that actually exist.

Why this file exists
--------------------
`data/search_index.json` had **no generator at all**. It was written once by hand (or by a script
since deleted) and last built 2026-09-03, so it had drifted to 74 tools and 438 entries against a
site of 78 tools and 748 crawlable URLs. Nothing failed when it went stale, because nothing
watched it: search quietly returns results that no longer reflect the site, and the reader
concludes the site lacks content it actually has.

So the index is now derived on every pipeline run from the page tree itself, using the project's
own public-page definition (`scripts/site_scope.py`) rather than a hand-kept list. Anything
public, crawlable and generated is in the index the same day it ships.

Entry shape (kept small — this file is fetched by the browser):
    {type, name, slug, url, category, desc, keywords, tool?}

`keywords` carries the terms a reader is likely to type that do NOT appear in the title or
description — a tool's category, its use cases, its slug. Without it, "voice" does not find
ElevenLabs and "resume" does not find a writing tool.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_scope import is_public_rel  # noqa: E402

OUT = ROOT / "data" / "search_index.json"
DOMAIN = "https://aitoolsessentials.com"
SITE_SUFFIXES = (" — AIToolsEssentials", " | AIToolsEssentials", " – AIToolsEssentials",
                 " - AIToolsEssentials", "| AIToolsEssentials", " · AIToolsEssentials")
DESC_LIMIT = 180
KEYWORD_LIMIT = 8
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "you", "are", "was", "were",
    "best", "guide", "tools", "tool", "html", "index", "www", "com", "aitoolsessentials",
    "how", "what", "why", "when", "which", "into", "over", "than", "them", "they", "their",
    # Filler that leaks out of prose fields (best_for / use_cases / key_features) and would
    # otherwise occupy keyword slots that a real search term should have.
    "one", "two", "any", "all", "but", "not", "can", "could", "will", "would", "should", "may",
    "each", "every", "some", "most", "more", "less", "very", "just", "also", "even", "only",
    "own", "same", "other", "others", "such", "via", "per", "out", "its", "it", "is", "be",
    "has", "have", "had", "get", "got", "use", "used", "using", "uses", "make", "makes",
    "making", "need", "needs", "want", "wants", "work", "works", "working", "help", "helps",
    "without", "within", "across", "before", "after", "while", "still", "then", "there", "here",
    "specific", "spanning", "finding", "comparing", "listing", "adding", "following", "checking",
    "free", "paid", "new", "about", "page", "site", "review", "pricing", "category",
}

# Path prefix -> result type, longest first so /guides/switch-guides/ beats /guides/.
TYPE_BY_PREFIX = (
    ("tools/", "tool"),
    ("comparisons/", "comparison"),
    ("alternatives/", "comparison"),
    ("compare/", "comparison"),
    ("articles/", "guide"),
    ("guides/", "guide"),
    ("how-to/", "guide"),
    ("workflows/", "guide"),
    ("use-cases/", "guide"),
    ("best-for/", "guide"),
    ("glossary/", "reference"),
    ("categories/", "category"),
    ("model-lineups/", "reference"),
    ("benchmarks/", "reference"),
    ("pricing-watch/", "reference"),
    ("change-radar/", "reference"),
    ("resources/", "utility"),
    ("downloads/", "utility"),
    ("updates/", "reference"),
    ("weekly/", "reference"),
    ("pricing-index/", "reference"),
    ("fit-interview/", "utility"),
    ("confidence-check/", "utility"),
    ("stacks/", "utility"),
    ("services/", "service"),
    ("premium/", "premium"),
    ("legal/", "reference"),
)

# Root-level pages that are utilities rather than articles.
UTILITY_FILES = {
    "stack-audit.html", "stack-builder.html", "tool-finder.html", "cost-calculator.html",
    "automation-cost-decoder.html", "decision-brief.html", "compare-shortlist.html",
    "confidence-check.html", "quiz.html", "free-ai-tools.html", "deals/index.html",
    "resources/index.html", "downloads/index.html", "start-here.html", "search/index.html",
    "newsletter/index.html", "subscribe/index.html", "contact.html", "faq.html",
}

# Pages that exist to be crawled, not to be found by a reader searching for a tool or a guide.
EXCLUDE_PREFIXES = ("legal/", "go/")
EXCLUDE_FILES = {"404.html", "checkout/complete/index.html", "premium/welcome/index.html"}


def _clean(text: str | None) -> str:
    if not text:
        return ""
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _meta(page: str, name: str) -> str:
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', page, re.I)
    return html.unescape(m.group(1)).strip() if m else ""


def _title(page: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I)
    t = _clean(m.group(1)) if m else ""
    # Two separator conventions are in use across the generators ("— " and " | "), and 216 of
    # 750 titles kept the site name because only the em-dash form was stripped. A result reading
    # "Best Adobe Firefly alternatives | AIToolsEssentials" is noise on a page whose own header
    # already says where you are.
    changed = True
    while changed:
        changed = False
        for suffix in SITE_SUFFIXES:
            if t.endswith(suffix):
                t = t[: -len(suffix)].strip()
                changed = True
    return t.strip()


def _h1(page: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S | re.I)
    return _clean(m.group(1)) if m else ""


def _result_type(rel: str) -> str:
    # /tools/ itself is the directory listing, not a tool. Counting it as one made the index
    # report 79 tools against a 78-tool catalog and would have let "tools" rank the index page
    # above every actual review.
    if rel == "tools/index.html":
        return "utility"
    if rel in UTILITY_FILES:
        return "utility"
    for prefix, kind in TYPE_BY_PREFIX:
        if rel.startswith(prefix):
            return kind
    return "page"


# Curated, VERIFIED aliases for terms a reader may reasonably type that appear nowhere in the
# tool's name, summary or features. Every entry must come from a fact we hold in our own records
# (the vendor's own About page, the submission, or tool_sources) — never a guess. Keep this small:
# it exists for operator/company names and older product names, not for keyword stuffing.
SEARCH_ALIASES = {
    # Operator is "Hashgraph Online" (a Hedera-ecosystem DAO), named on hol.org's own About and
    # corroborated by the GitHub org — recorded in admin/held-submissions.md when it was published.
    # The reader who knows the company types "hashgraph", not "HOL".
    "hol-registry": ["hashgraph", "hashgraph online", "hol plugins"],
}


def _host_words(url: str) -> list[str]:
    """Words from a vendor domain, so a reader who types the site they half-remember finds it.

    `hol.org` must be findable by typing "hol.org" or "hol org". The official URL is the single
    most reliable alias a tool has, and it is already in `tools.json` for every entry.
    """
    if not url:
        return []
    host = re.sub(r"^https?://", "", str(url)).split("/")[0].lower()
    host = re.sub(r"^www\.", "", host)
    stem = host.rsplit(".", 1)[0] if "." in host else host
    words = [w for w in re.split(r"[.\-]", stem) if len(w) > 1]
    return words + [host, stem]


def _words(text, limit: int = 10) -> list[str]:
    if not text:
        return []
    if isinstance(text, (list, tuple)):
        text = " ".join(str(x) for x in text)
    out = []
    for w in re.split(r"\W+", str(text)):
        w = w.lower()
        if len(w) > 2 and w not in STOPWORDS:
            out.append(w)
        if len(out) >= limit:
            break
    return out


def _excluded(rel: str) -> bool:
    if rel in EXCLUDE_FILES:
        return True
    return any(rel.startswith(p) for p in EXCLUDE_PREFIXES)


def build(root: Path) -> list[dict]:
    tools = json.loads((root / "data" / "tools.json").read_text())
    by_slug = {t["slug"]: t for t in tools}
    entries: list[dict] = []
    seen_urls: set[str] = set()

    for path in sorted(root.rglob("*.html")):
        rel_path = path.relative_to(root)
        if not is_public_rel(rel_path):
            continue
        rel = rel_path.as_posix()
        if _excluded(rel):
            continue

        page = path.read_text(errors="ignore")
        title = _title(page)
        if not title:
            continue
        desc = _meta(page, "description")
        h1 = _h1(page)
        kind = _result_type(rel)

        # Canonical directory form: index.html -> its directory.
        if rel.endswith("index.html"):
            url = "/" + rel[: -len("index.html")]
        else:
            url = "/" + rel
        if url != "/" and not url.endswith("/") and url.endswith(".html"):
            pass  # keep the .html form; that is how the page is served
        if url.startswith("/index.html"):
            url = "/"
        if url in seen_urls:
            continue
        seen_urls.add(url)

        entry: dict = {"type": kind, "url": url}

        if kind == "tool":
            # Prefer the curated record: its category and best_for are the site's own words.
            slug = rel.split("/")[1]
            tool = by_slug.get(slug)
            if tool:
                entry["slug"] = slug
                entry["name"] = tool.get("name") or title
                entry["category"] = tool.get("category", "")
                entry["desc"] = (tool.get("best_for") or tool.get("summary") or desc)[:DESC_LIMIT]
                # Ordered by usefulness so the cap drops the least valuable terms, not whichever
                # happened to sort last alphabetically. Dedupe preserving order, cap, then sort
                # only for a deterministic file.
                kw = []
                kw += [slug.replace("-", " ")]                 # slug form: "hol registry"
                kw += _host_words(tool.get("official"))        # the vendor's own domain
                kw += SEARCH_ALIASES.get(slug, [])             # verified operator/product aliases
                kw += [tool.get("category", ""), "ai tool", "review", "pricing"]
                kw += _words(tool.get("key_features"), 10)     # specific, low-noise feature names
                kw += _words(tool.get("use_cases"), 12)        # split into words, not whole sentences
                kw += _words(tool.get("best_for"), 8)
                seen, ordered = set(), []
                for k in kw:
                    k = str(k).lower().strip()
                    if len(k) < 2 or k in seen or k in STOPWORDS:
                        continue
                    seen.add(k)
                    ordered.append(k)
                entry["keywords"] = sorted(ordered[:26])
                if tool.get("rating"):
                    entry["rating"] = tool["rating"]
                if tool.get("price"):
                    entry["price"] = str(tool["price"])[:60]
                entries.append(entry)
                continue
            entry["slug"] = slug
            entry["name"] = title
        else:
            name = title or h1 or rel
            entry["name"] = name
            if desc:
                entry["desc"] = desc[:DESC_LIMIT]
            slug = rel.rsplit("/", 1)
            if len(slug) > 1:
                entry["slug"] = slug[0]
            # Keywords from the path segments: a reader typing "switch guides" should find
            # /guides/switch-guides/ even when the title says "Switching AI tools".
            words = [w for w in re.split(r"[/\-_.]", rel.rsplit(".", 1)[0]) if len(w) > 2]
            words += [w for w in re.split(r"\W+", h1) if len(w) > 3]
            entry["keywords"] = sorted({w.lower() for w in words if w.lower() not in STOPWORDS})[:KEYWORD_LIMIT]

        entries.append(entry)

    # Deterministic order: tools first, then by name. Keeps the file diffable.
    order = {"tool": 0, "comparison": 1, "guide": 2, "category": 3, "reference": 4,
             "utility": 5, "service": 6, "premium": 7, "page": 8}
    entries.sort(key=lambda e: (order.get(e["type"], 9), e["name"].lower()))
    return entries


def main() -> int:
    entries = build(ROOT)
    payload = {
        "built": date.today().isoformat(),
        "count": len(entries),
        "entries": entries,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")

    counts: dict[str, int] = {}
    for e in entries:
        counts[e["type"]] = counts.get(e["type"], 0) + 1
    tools_indexed = counts.get("tool", 0)
    catalog = len(json.loads((ROOT / "data" / "tools.json").read_text()))
    print(f"search index: {len(entries)} entries, {OUT.stat().st_size // 1024} KB -> {OUT.relative_to(ROOT)}")
    print("  by type: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])))
    print(f"  tools indexed: {tools_indexed} of {catalog} in the catalog")
    if tools_indexed != catalog:
        print(f"  WARNING: {catalog - tools_indexed} catalog tools have no index entry", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
