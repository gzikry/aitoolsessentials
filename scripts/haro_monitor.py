#!/usr/bin/env python3
"""Daily HARO/Connectively journalist request monitor.

Checks for journalist queries about AI tools, pricing, and subscriptions.
Saves matching opportunities to a daily digest file.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = SITE_ROOT / "marketing" / "haro-outreach"
OUTPUT_DIR.mkdir(exist_ok=True)

# Keywords to match in journalist queries
KEYWORDS = [
    "ai tool", "ai pricing", "ai subscription", "chatgpt", "claude",
    "cursor", "copilot", "saas cost", "software spending", "overlapping",
    "tool consolidation", "ai for business", "ai productivity", "tech spending",
    "software budget", "ai agent", "subscription audit", "ai comparison"
]

# Query URLs to check (public pages)
URLS = {
    "help_reporter": "https://www.helpareporter.com/",
    "connectively": "https://www.connectively.us/",
}

def fetch_page(url: str, timeout: int = 15) -> str:
    """Fetch a page using curl."""
    try:
        result = run(
            ['curl', '-s', '--max-time', str(timeout), '-A',
             'Mozilla/5.0 (compatible; AIToolsEssentials/1.0; +https://aitoolsessentials.com)',
             url],
            capture_output=True, text=True, timeout=timeout + 5
        )
        return result.stdout
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return ""

def extract_queries(html: str) -> list[dict]:
    """Extract journalist queries from HTML."""
    queries = []
    # Look for common patterns in HARO/Connectively pages
    # This is a simplified extractor - in practice, you'd use more sophisticated parsing
    
    # Look for query titles/subjects
    patterns = [
        r'<h[23][^>]*>(.*?)</h[23]>',  # Headings
        r'<a[^>]*href="[^"]*query[^"]*"[^>]*>(.*?)</a>',  # Query links
        r'class="[^"]*query[^"]*"[^>]*>(.*?)</div>',  # Query containers
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        for match in matches:
            clean = re.sub(r'<[^>]+>', '', match).strip()
            if len(clean) > 20 and len(clean) < 500:
                queries.append({"text": clean, "source": "page"})
    
    return queries

def filter_relevant(queries: list[dict]) -> list[dict]:
    """Filter queries that match our keywords."""
    relevant = []
    for query in queries:
        text = query.get("text", "").lower()
        for keyword in KEYWORDS:
            if keyword in text:
                query["matched_keyword"] = keyword
                relevant.append(query)
                break
    return relevant

def save_digest(queries: list[dict]) -> Path:
    """Save today's matching queries to a digest file."""
    today = datetime.utcnow().strftime('%Y-%m-%d')
    output_file = OUTPUT_DIR / f"digest-{today}.json"
    
    digest = {
        "date": today,
        "total_queries": len(queries),
        "queries": queries,
        "generated_at": datetime.utcnow().isoformat()
    }
    
    output_file.write_text(json.dumps(digest, indent=2), encoding='utf-8')
    print(f"  Saved digest to {output_file}")
    return output_file

def main():
    print("HARO/Connectively Monitor")
    print("=" * 40)
    
    all_queries = []
    
    for source, url in URLS.items():
        print(f"\nChecking {source}...")
        html = fetch_page(url)
        if not html:
            continue
        
        queries = extract_queries(html)
        print(f"  Found {len(queries)} queries")
        
        relevant = filter_relevant(queries)
        print(f"  {len(relevant)} relevant queries")
        
        for q in relevant:
            q["source"] = source
            all_queries.append(q)
    
    print(f"\nTotal relevant queries: {len(all_queries)}")
    
    if all_queries:
        save_digest(all_queries)
        print("\nTop queries:")
        for q in all_queries[:5]:
            print(f"  - [{q.get('matched_keyword')}] {q['text'][:80]}...")
    else:
        print("\nNo relevant queries found today.")

if __name__ == "__main__":
    main()
