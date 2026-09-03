#!/usr/bin/env python3
"""Internal linking audit — find orphan pages and optimize PageRank flow.

Scans all HTML pages, builds a link graph, and identifies:
1. Orphan pages (no internal links pointing to them)
2. Pages with low inbound links that should be promoted
3. Conversion pages (Premium, Subscribe, Stack Audit) that need more internal links
4. Pages that link OUT but don't link back to conversion pages
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin

SITE_ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = SITE_ROOT

# Conversion pages we want to promote
CONVERSION_PAGES = [
    "/premium/",
    "/subscribe/",
    "/stack-audit.html",
    "/pricing/",
]

# Pages that should link to conversion pages
HIGH_TRAFFIC_PAGES = [
    "/tools/",
    "/comparisons/",
    "/articles/",
    "/categories/",
    "/",
]

def find_html_files() -> list[Path]:
    """Find all HTML files in the site."""
    html_files = []
    for path in HTML_DIR.rglob("*.html"):
        # Skip generated tool pages (too many, not useful for this audit)
        if "/tools/" in str(path) and path.name != "index.html":
            continue
        html_files.append(path)
    return html_files

def get_page_url(path: Path) -> str:
    """Convert file path to URL."""
    rel = path.relative_to(SITE_ROOT)
    url = "/" + str(rel).replace("\\", "/")
    # Clean up
    if url.endswith("/index.html"):
        url = url[:-10]
    return url

def extract_links(html: str, base_url: str) -> list[str]:
    """Extract all internal links from HTML."""
    links = []
    # Find all href attributes
    for match in re.finditer(r'href="([^"]+)"', html):
        href = match.group(1)
        # Skip external links, anchors, javascript
        if href.startswith(("http://", "https://", "mailto:", "javascript:", "#")):
            continue
        # Skip assets
        if href.startswith(("/css/", "/js/", "/assets/", "/images/")):
            continue
        # Resolve relative URLs
        full_url = urljoin(base_url, href)
        # Remove anchors
        full_url = full_url.split("#")[0]
        # Remove trailing index.html
        if full_url.endswith("/index.html"):
            full_url = full_url[:-10]
        links.append(full_url)
    return links

def build_link_graph(pages: list[Path]) -> dict:
    """Build a graph of internal links."""
    graph = defaultdict(list)  # page -> [linked pages]
    reverse_graph = defaultdict(list)  # page -> [pages linking to it]
    
    for page in pages:
        url = get_page_url(page)
        html = page.read_text(encoding='utf-8', errors='ignore')
        links = extract_links(html, url)
        
        # Deduplicate
        links = list(set(links))
        graph[url] = links
        
        for link in links:
            reverse_graph[link].append(url)
    
    return graph, reverse_graph

def find_orphan_pages(pages: list[Path], reverse_graph: dict) -> list[str]:
    """Find pages with no internal links pointing to them."""
    orphans = []
    for page in pages:
        url = get_page_url(page)
        if url not in reverse_graph and url != "/":
            orphans.append(url)
    return orphans

def audit_conversion_pages(reverse_graph: dict) -> dict:
    """Check how many internal links point to conversion pages."""
    results = {}
    for page in CONVERSION_PAGES:
        inbound = reverse_graph.get(page, [])
        results[page] = {
            "inbound_count": len(inbound),
            "inbound_sources": inbound[:10]  # First 10
        }
    return results

def find_link_opportunities(graph: dict, reverse_graph: dict) -> list[dict]:
    """Find pages that should link to conversion pages but don't."""
    opportunities = []
    
    for page in HIGH_TRAFFIC_PAGES:
        # Find all pages under this section
        section_pages = [p for p in graph.keys() if p.startswith(page) and p != page]
        
        for section_page in section_pages[:20]:  # Sample
            links = graph.get(section_page, [])
            has_conversion_link = any(
                any(c in link for c in CONVERSION_PAGES)
                for link in links
            )
            if not has_conversion_link:
                opportunities.append({
                    "page": section_page,
                    "links_to_conversion": False,
                    "suggestion": "Add link to /stack-audit.html or /subscribe/"
                })
    
    return opportunities

def main():
    print("Internal Linking Audit")
    print("=" * 50)
    
    pages = find_html_files()
    print(f"\nFound {len(pages)} HTML pages to audit")
    
    graph, reverse_graph = build_link_graph(pages)
    
    # 1. Orphan pages
    orphans = find_orphan_pages(pages, reverse_graph)
    print(f"\n1. ORPHAN PAGES ({len(orphans)}):")
    for orphan in orphans[:10]:
        print(f"   - {orphan}")
    
    # 2. Conversion page audit
    print("\n2. CONVERSION PAGE INBOUND LINKS:")
    conversion_audit = audit_conversion_pages(reverse_graph)
    for page, data in conversion_audit.items():
        print(f"   {page}: {data['inbound_count']} inbound links")
        if data['inbound_sources'][:3]:
            for source in data['inbound_sources'][:3]:
                print(f"      ← {source}")
    
    # 3. Link opportunities
    print("\n3. LINK OPPORTUNITIES:")
    opportunities = find_link_opportunities(graph, reverse_graph)
    print(f"   Found {len(opportunities)} pages that could link to conversion pages")
    
    # 4. Top linked pages
    print("\n4. MOST LINKED-TO PAGES:")
    sorted_pages = sorted(reverse_graph.items(), key=lambda x: len(x[1]), reverse=True)
    for page, sources in sorted_pages[:10]:
        print(f"   {page}: {len(sources)} inbound links")
    
    # 5. Recommendations
    print("\n5. RECOMMENDATIONS:")
    print("   - Add 'Free Stack Audit' CTA to all comparison pages")
    print("   - Add 'Keep/Cut Weekly' signup to all article pages")
    print("   - Add internal links from tool category pages to /stack-audit.html")
    print("   - Add 'Run free audit' link to /comparisons/best-ai-tools.html")

if __name__ == "__main__":
    main()
