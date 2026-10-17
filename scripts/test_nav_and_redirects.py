#!/usr/bin/env python3
"""The shared nav and the duplicate-page redirects stay put."""
from __future__ import annotations

import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from consolidate_duplicates import (
    PAIRS,
    _description_stub,
    _short_stub_copy,
    _this_moved_short,
    duplicate_errors,
    redirect_stub,
    stub_link_errors,
)
from site_chrome import CANONICAL_HEADER, header_label_errors

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []
    if 'class="nav-toggle"' not in CANONICAL_HEADER or 'id="site-nav"' not in CANONICAL_HEADER:
        errors.append("shared nav has no menu button")
    if 'href="/tools/">Tools</a>' not in CANONICAL_HEADER:
        errors.append("shared nav dropped Tools")
    if 'href="/legal/affiliate-disclosure.html">Disclosure</a>' not in CANONICAL_HEADER:
        errors.append("shared nav dropped Disclosure")
    if CANONICAL_HEADER.count(">Sponsor us</a>") != 1:
        errors.append("shared nav must have one Sponsor us link")
    sample = redirect_stub("Suno vs Udio", "comparisons/suno-vs-udio.html")
    if 'url=/comparisons/suno-vs-udio.html' not in sample or "noindex" not in sample:
        errors.append("redirect stub is not a noindex refresh")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    header = home.split("</header>", 1)[0]
    if 'data-nav="slim"' not in header:
        errors.append("homepage nav is not the short nav")
    for label in ("Stack Audit", "Premium", "Subscribe"):
        if f">{label}</a>" not in header:
            errors.append(f"homepage nav lost {label}")
    if 'class="button home-cta-primary" href="/stack-audit.html"' not in home:
        errors.append("homepage hero lost Free Stack Audit")
    claude = (ROOT / "articles/claude-vs-chatgpt.html").read_text(encoding="utf-8")
    footer = claude[claude.rfind("<footer") :]
    if 'href="/sponsor/" rel="nofollow">Sponsor us</a>' not in footer:
        errors.append("claude vs chatgpt footer lost Sponsor us")
    errors.extend(stub_link_errors(ROOT)[:8])
    errors.extend(header_label_errors(ROOT)[:8])
    errors.extend(duplicate_errors(ROOT)[:8])
    for loser, winner, _title in PAIRS:
        if loser in (ROOT / "index.html").read_text(encoding="utf-8"):
            errors.append(f"homepage still links {loser}")
        winner_html = (ROOT / winner).read_text(encoding="utf-8")
        if "This page has moved." in winner_html:
            errors.append(f"{winner} absorbed the redirect stub")
        if "affiliate" in (ROOT / loser).read_text(encoding="utf-8").casefold() and "affiliate" not in winner_html.casefold():
            errors.append(f"{winner} lost the affiliate disclosure that {loser} carried")
    site_js = (ROOT / "js/site.js").read_text(encoding="utf-8")
    if "event.key !== 'Escape'" not in site_js or "button.focus()" not in site_js:
        errors.append("Escape does not close the menu and return focus to the button")
    errors.extend(_stub_phrase_and_jsonld())
    if errors:
        raise SystemExit("\n".join(errors))


def _doc(head: str, body: str) -> str:
    return f"<!doctype html><html><head>{head}</head><body>{body}</body></html>"


def _load_evidence_case_table():
    """QA's case table when evidence/ ships one. None when it does not."""
    evidence = ROOT / "evidence"
    if not evidence.is_dir():
        return None
    suffixes = {".json", ".csv", ".tsv", ".txt"}
    for path in sorted(evidence.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if "case" not in path.name.lower():
            continue
        return _parse_case_table(path)
    return None


def _parse_case_table(path: Path) -> dict:
    import csv
    import json

    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        return {
            "fail_html": dict(data.get("fail_html") or {}),
            "pass_html": dict(data.get("pass_html") or {}),
            "llms_fail": list(data.get("llms_fail") or []),
            "llms_pass": list(data.get("llms_pass") or []),
        }
    rows = list(csv.DictReader(text.splitlines(), delimiter="\t" if path.suffix.lower() == ".tsv" else ","))
    table = {"fail_html": {}, "pass_html": {}, "llms_fail": [], "llms_pass": []}
    for row in rows:
        kind = (row.get("kind") or "html").strip().lower()
        expect = (row.get("expect") or "fail").strip().lower()
        name = (row.get("name") or "").strip()
        body = row.get("text") or row.get("html") or ""
        if kind == "llms":
            table["llms_fail" if expect == "fail" else "llms_pass"].append(body)
            continue
        if not name:
            raise ValueError(f"{path} row has no name")
        table["fail_html" if expect == "fail" else "pass_html"][name] = body
    return table


def _inline_qa_case_table() -> dict:
    """Description, llms, and body cases the main substring check still catches.

    evidence/ has no case table in this repo, so the rows live here.
    """
    compare = "<title>Compare</title>"
    safe = "<p>Current page.</p>"

    def meta(attr: str, content: str) -> str:
        return _doc(f'{attr} content="{content}">{compare}', safe)

    fails = {
        # (c) Stub sentence on every block, not only p, li, and div.
        "qa-article.html": _doc(compare, "<article>This article has moved.</article>"),
        "qa-blockquote.html": _doc(compare, "<blockquote>This guide has moved.</blockquote>"),
        "qa-td.html": _doc(compare, "<table><tr><td>This page has moved.</td></tr></table>"),
        "qa-main.html": _doc(compare, "<main>This page has moved.</main>"),
        "qa-figcaption.html": _doc(compare, "<figure><figcaption>This article has moved.</figcaption></figure>"),
        "qa-aside.html": _doc(compare, "<aside>This guide has moved.</aside>"),
        "qa-bare.html": _doc(compare, "This page has moved."),
        "qa-header-span.html": _doc(compare, "<header><span>This page has moved.</span></header>"),
        # (a) The title rule on the fields that are not the <title> or a heading.
        "qa-jsonld.html": _doc(
            compare + '<script type="application/ld+json">{"headline":"X has moved"}</script>',
            safe,
        ),
        "qa-alt.html": _doc(compare, '<img alt="Runway vs Pika has moved">'),
        "qa-aria.html": _doc(compare, '<button aria-label="Pricing has moved">Open</button>'),
        "qa-alt-mark.html": _doc(compare, '<img alt="Runway vs Pika (moved)">'),
        # (b) Separator, then the brand or a see/open tail. Named V rows cover the rest.
        "qa-endash.html": meta('<meta name="description"', "Runway vs Pika has moved – AIToolsEssentials"),
        "qa-emdash.html": meta('<meta name="description"', "has moved — AIToolsEssentials"),
        "qa-pipe.html": meta('<meta name="description"', "has moved | aitoolsessentials"),
        "qa-colon.html": meta('<meta name="description"', "has moved: see the new page"),
        "qa-middot.html": meta('<meta name="description"', "has moved · AIToolsEssentials"),
        "qa-period-brand.html": meta('<meta name="description"', "X has moved. AIToolsEssentials"),
        "qa-comma-pipe.html": meta('<meta name="description"', "has moved, | AIToolsEssentials"),
        "qa-bang-brand.html": meta('<meta name="description"', "X has moved! aitoolsessentials.com"),
        "qa-see-guide.html": meta('<meta name="description"', "X has moved. See the current guide"),
        "qa-open-page.html": meta('<meta name="description"', "X has moved - open the new page"),
        "qa-open-guide.html": meta('<meta property="og:description"', "X has moved — Open the current guide"),
    }
    passes = {
        "qa-desc-comma-brand.html": meta('<meta name="description"', "has moved, AIToolsEssentials"),
        "qa-desc-generic-brand.html": meta('<meta name="description"', "has moved — Brand"),
        "qa-desc-runway.html": meta('<meta name="description"', "Runway has moved - Pika has not"),
        "qa-desc-comma.html": meta('<meta name="description"', "pricing has moved, so…"),
        "qa-desc-export.html": meta('<meta name="description"', "The export button has moved to the Pro plan."),
        "qa-desc-login.html": meta('<meta name="description"', "its pricing page has moved behind a login"),
        "qa-desc-hyphen-on.html": meta('<meta name="description"', "The team has moved-on to the new plan."),
        "qa-see-body.html": _doc(compare, "<p>X has moved. See the current page</p>"),
        "qa-desc-long.html": meta(
            '<meta name="description"',
            "This guide has moved. " + ("Keep the dated notes. " * 12),
        ),
    }
    return {
        "fail_html": fails,
        "pass_html": passes,
        "llms_fail": [
            "X has moved. See the current page",
            "has moved -- AIToolsEssentials",
            "This page has moved.",
            "Runway vs Pika has moved - aitoolsessentials.com",
            "X has moved! Open the current page",
            "has moved -AIToolsEssentials",
            "X has moved: see the new guide",
            "X (moved)",
        ],
        "llms_pass": [
            "pricing has moved, so…",
            "The export button has moved to the Pro plan.",
            "its pricing page has moved behind a login",
            "Pricing has moved. Here's what changed",
            "Runway has moved - Pika has not",
            "The team has moved-on to the new plan.",
            "has moved, AIToolsEssentials",
            "has moved — Brand",
            "has moved-on",
            "has moved-in",
        ],
    }


def _qa_case_table():
    loaded = _load_evidence_case_table()
    if loaded is not None:
        return loaded, "evidence"
    return _inline_qa_case_table(), "inline"


def _qa_fail_pages() -> dict:
    table, _source = _qa_case_table()
    return table["fail_html"]


def _qa_pass_pages() -> dict:
    table, _source = _qa_case_table()
    return table["pass_html"]


def _main_substring_hits(text: str) -> bool:
    """origin/main flags the raw phrase anywhere in the file."""
    folded = text.casefold()
    return "has moved" in folded or "(moved)" in folded


def _rerun_qa_case_table(failures: dict, passes: dict) -> list[str]:
    """Rerun the case table. evidence/ wins when it ships one; otherwise inline."""
    misses: list[str] = []
    table, source = _qa_case_table()
    if source == "evidence":
        fail_html = table["fail_html"]
        pass_html = table["pass_html"]
    else:
        fail_html = failures
        pass_html = passes
        named = (
            "g6.html", "k3.html", "k5.html", "s3.html",
            "v1.html", "v2.html", "v3.html", "v4.html",
            "v13.html", "v14.html", "v15.html", "v16.html",
        )
        missing = [name for name in named if name not in failures]
        if missing:
            misses.append(f"named must-fail pages missing: {missing}")
        if len(failures) < 28:
            misses.append(f"only {len(failures)} must-fail pages; main's set is larger")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, html in {**fail_html, **pass_html}.items():
            (root / name).write_text(html, encoding="utf-8")
        found_lines = stub_link_errors(root)
        for name, html in fail_html.items():
            if not _main_substring_hits(html):
                misses.append(f"{source} {name} is not a case main catches")
            if not any(line.startswith(f"{name} still says has moved") for line in found_lines):
                misses.append(f"{source} {name} regressed")
        for name in pass_html:
            if any(line.startswith(f"{name} ") for line in found_lines):
                misses.append(f"{source} {name} was flagged")
    for line in table["llms_fail"]:
        if not _main_substring_hits(line):
            misses.append(f"llms line is not a case main catches: {line}")
        with tempfile.TemporaryDirectory() as tmp:
            llms = Path(tmp) / "llms.txt"
            llms.write_text(line + "\n", encoding="utf-8")
            found = stub_link_errors(Path(tmp))
            if not any(item.startswith("llms.txt still says") for item in found):
                misses.append(f"llms line regressed: {line}")
        if "(moved)" not in line.casefold() and not _description_stub(line):
            misses.append(f"llms helper missed: {line}")
    with tempfile.TemporaryDirectory() as tmp:
        llms = Path(tmp) / "llms.txt"
        llms.write_text("\n".join(table["llms_pass"]) + "\n", encoding="utf-8")
        found = stub_link_errors(Path(tmp))
        if found:
            misses.append(f"llms prose was flagged: {found}")
    for line in table["llms_pass"]:
        if _description_stub(line):
            misses.append(f"llms helper flagged prose: {line}")
    return misses


def _stub_phrase_and_jsonld() -> list[str]:
    """Titles and headings fail on the phrase. Short stub lines fail. Prose passes.

    'Pricing has moved. Here's what changed' and 'Runway has moved - Pika has not'
    fail when they are the title. The same sentences pass in body prose. That split
    is intentional: a real title never needs the phrase.
    """
    misses: list[str] = []
    failures = {
        # Z1–Z4. Hyphen tails used to slip through the separator regex.
        "z1.html": _doc("<title>Runway vs Pika has moved -</title>", "<p>Current page.</p>"),
        "z2.html": _doc("<title>has moved -- AIToolsEssentials</title>", "<p>Current page.</p>"),
        "z3.html": _doc("<title>has moved - aitoolsessentials.com</title>", "<p>Current page.</p>"),
        "z4.html": _doc("<title>has moved -AIToolsEssentials</title>", "<p>Current page.</p>"),
        # T6. A title that continues after the phrase still fails.
        "t6.html": _doc("<title>X has moved. See the current page</title>", "<p>Current page.</p>"),
        "title-bang.html": _doc("<title>X has moved! See the new guide.</title>", "<p>Current page.</p>"),
        "title-pipe.html": _doc("<title>Runway vs Pika has moved | AIToolsEssentials</title>", "<p>Current page.</p>"),
        "title-bare.html": _doc("<title>Runway vs Pika has moved</title>", "<p>Current page.</p>"),
        "h1.html": _doc("<title>Compare</title>", "<h1>Runway vs Pika has moved</h1>"),
        "h1-span.html": _doc("<title>Compare</title>", "<h1><span>Runway vs Pika has moved</span></h1>"),
        "h1-paren.html": _doc("<title>Compare</title>", "<h1>X (has moved)</h1>"),
        "title-moved-mark.html": _doc("<title>Runway vs Pika (moved)</title>", "<p>Current page.</p>"),
        # Comma cases. A comma does not save a title or heading.
        "title-comma-ellipsis.html": _doc("<title>Runway vs Pika has moved, …</title>", "<p>Current page.</p>"),
        "h1-comma.html": _doc("<title>Compare</title>", "<h1>Runway vs Pika has moved,</h1>"),
        "title-comma-pipe.html": _doc("<title>Runway vs Pika has moved, | AIToolsEssentials</title>", "<p>Current page.</p>"),
        # These two are the body sentences below. As titles they fail on purpose.
        "title-pricing-changed.html": _doc(
            "<title>Pricing has moved. Here's what changed</title>",
            "<p>Current page.</p>",
        ),
        "title-runway-pika.html": _doc(
            "<title>Runway has moved - Pika has not</title>",
            "<p>Current page.</p>",
        ),
        # G1–G7. Stub sentence, or the whole short block is '<X> has moved' plus punctuation.
        "g1.html": _doc("<title>Compare</title>", "<p>This page has moved.</p>"),
        "g2.html": _doc("<title>Compare</title>", "<div>This guide has moved.</div>"),
        "g3.html": _doc("<title>Compare</title>", "<li>This article has moved</li>"),
        "g4.html": _doc("<title>Compare</title>", "<p>Runway vs Pika has moved.</p>"),
        "g5.html": _doc("<title>Compare</title>", "<li>Runway vs Pika has moved,</li>"),
        "g6.html": _doc("<title>Compare</title>", "<section>This guide has moved.</section>"),
        "g6-ellipsis.html": _doc("<title>Compare</title>", "<div>Runway vs Pika has moved…</div>"),
        "g7.html": _doc("<title>Compare</title>", "<h2>X has moved.</h2>"),
        # K3, K5, S3. Title-like fields and a span that is not a p, li, or div.
        "k3.html": _doc(
            '<meta property="og:title" content="Runway vs Pika has moved"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "k5.html": _doc(
            '<meta name="twitter:title" content="X (moved)"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "s3.html": _doc("<title>Compare</title>", "<span>This page has moved.</span>"),
        # V1–V4. Description hyphen tails that a title already fails.
        "v1.html": _doc(
            '<meta name="description" content="Runway vs Pika has moved - AIToolsEssentials"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "v2.html": _doc(
            '<meta name="description" content="has moved -- AIToolsEssentials"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "v3.html": _doc(
            '<meta name="description" content="has moved - aitoolsessentials.com"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "v4.html": _doc(
            '<meta name="description" content="has moved -AIToolsEssentials"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        # V13–V16. A separator, then a see/open tail. V13 is the flipped description.
        "v13.html": _doc(
            '<meta name="description" content="X has moved. See the current page"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "v14.html": _doc(
            '<meta name="description" content="X has moved. See the new guide"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "v15.html": _doc(
            '<meta property="og:description" content="X has moved! Open the current page"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "v16.html": _doc(
            '<meta name="twitter:description" content="X has moved? Open the new guide"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
    }
    failures.update(_qa_fail_pages())
    passes = {
        "comma.html": _doc("<title>Pricing notes</title>", "<p>pricing has moved, so…</p>"),
        "export.html": _doc("<title>Export</title>", "<p>The export button has moved to the Pro plan.</p>"),
        "login.html": _doc("<title>Pricing</title>", "<li>its pricing page has moved behind a login</li>"),
        "pricing-prose.html": _doc("<title>Pricing</title>", "<p>Pricing has moved. Here's what changed</p>"),
        "runway-prose.html": _doc("<title>Compare</title>", "<div>Runway has moved - Pika has not</div>"),
        "hyphen-on.html": _doc("<title>Plans</title>", "<p>The team has moved-on to the new plan.</p>"),
        "hyphen-in.html": _doc("<title>Layout</title>", "<p>The control has moved-in from the sidebar.</p>"),
        "meta-heres.html": _doc(
            '<meta name="description" content="Pricing has moved. Here\'s what changed"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "og-export.html": _doc(
            '<meta property="og:description" content="The export button has moved to the Pro plan."><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "tw-login.html": _doc(
            '<meta name="twitter:description" content="its pricing page has moved behind a login"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "z2-body.html": _doc("<title>Compare</title>", "<p>has moved -- AIToolsEssentials</p>"),
        "z3-body.html": _doc("<title>Compare</title>", "<p>has moved - aitoolsessentials.com</p>"),
        "z4-body.html": _doc("<title>Compare</title>", "<div>has moved -AIToolsEssentials</div>"),
        "long-section.html": _doc(
            "<title>Compare</title>",
            "<section>This guide has moved. " + ("Keep the dated notes. " * 12) + "</section>",
        ),
    }
    passes.update(_qa_pass_pages())
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "articles").mkdir()
        (root / "articles" / "suno-vs-udio.html").write_text(
            redirect_stub("Suno vs Udio", "comparisons/suno-vs-udio.html"),
            encoding="utf-8",
        )
        (root / "index.html").write_text(
            "<!doctype html><html><head>"
            '<script type="application/ld+json">'
            '{"url":"https://aitoolsessentials.com/articles/suno-vs-udio.html"}'
            "</script></head><body><p>Still here.</p></body></html>",
            encoding="utf-8",
        )
        for name, html in {**failures, **passes}.items():
            (root / name).write_text(html, encoding="utf-8")
        found_lines = stub_link_errors(root)
        found = "\n".join(found_lines)
        for name in failures:
            if not any(line.startswith(f"{name} still says has moved") for line in found_lines):
                misses.append(f"validator missed {name}: {found}")
        for name in passes:
            if any(line.startswith(f"{name} ") for line in found_lines):
                misses.append(f"validator flagged {name}: {found}")
        if "index.html JSON-LD url points at stub articles/suno-vs-udio.html" not in found:
            misses.append(f"validator missed JSON-LD stub url: {found}")
        if "articles/suno-vs-udio.html still says" in found:
            misses.append("validator flagged the redirect stub itself")
    stub = "This page has moved. "
    exact = stub + ("x" * (180 - len(stub)))
    over = stub + ("x" * (181 - len(stub)))
    if len(exact) != 180 or not _short_stub_copy(exact):
        misses.append("a 180-character stub sentence was not flagged")
    if len(over) != 181 or _short_stub_copy(over):
        misses.append("a stub sentence longer than 180 characters was flagged")
    long_copy = "Pricing notes has moved" + (", " * 20000) + "so the plan changed"
    for label, check in (("short copy", _short_stub_copy), ("description", _description_stub)):
        started = time.perf_counter()
        flagged = check(long_copy)
        elapsed = time.perf_counter() - started
        if flagged:
            misses.append(f"a long punctuation run was treated as a stub by {label}")
        if elapsed > 0.2:
            misses.append(f"a long punctuation run took {elapsed:.3f}s in {label}")
    if not _this_moved_short(exact) or _this_moved_short(over):
        misses.append("the block stub sentence ignored the 180-character limit")
    misses.extend(_rerun_qa_case_table(failures, passes))
    return misses


if __name__ == "__main__":
    main()
