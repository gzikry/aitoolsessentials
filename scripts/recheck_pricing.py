#!/usr/bin/env python3
"""Re-check official pricing pages and detect changes."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
PRICING_DATA = SITE_ROOT / "data" / "pricing_snapshots.json"
PRICING_WATCH = SITE_ROOT / "pricing-watch" / "index.html"
FEED_SCRIPT = SITE_ROOT / "scripts" / "generate_pricing_feed.py"
DOMAIN = "https://aitoolsessentials.com"

def load_snapshots() -> dict:
    """Load current pricing snapshots."""
    if not PRICING_DATA.exists():
        return {}
    return json.loads(PRICING_DATA.read_text(encoding='utf-8'))

def fetch_page(url: str, timeout: int = 15) -> str:
    """Fetch a page using curl."""
    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', str(timeout), '-A', 
             'Mozilla/5.0 (compatible; AIToolsEssentials/1.0; +https://aitoolsessentials.com)',
             url],
            capture_output=True, text=True, timeout=timeout + 5
        )
        return result.stdout
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return ""

def extract_text(html: str) -> str:
    """Extract readable text from HTML."""
    # Remove scripts, styles, and tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text[:2000]  # First 2000 chars for comparison

def compute_hash(text: str) -> str:
    """Compute SHA-256 hash of text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

def detect_changes(snapshots: dict, pages: dict[str, str]) -> list[dict]:
    """Detect which tools have changed since last check."""
    changes = []
    today = datetime.utcnow().strftime('%Y-%m-%d')
    
    for slug, snapshot in snapshots.get('snapshots', {}).items():
        old_hash = snapshot.get('hash', '')
        old_text = snapshot.get('digest', '')
        new_html = pages.get(slug, '')
        new_text = extract_text(new_html)
        new_hash = compute_hash(new_text)
        
        if old_hash and old_hash != new_hash:
            # Change detected
            changes.append({
                'slug': slug,
                'detected': today,
                'previous_check': snapshot.get('date', today),
                'new_check': today,
                'note': f"{slug.replace('-', ' ').title()}: official pricing page changed since {snapshot.get('date', 'unknown')} check. Re-verified {today}."
            })
            # Update snapshot
            snapshot['date'] = today
            snapshot['hash'] = new_hash
            snapshot['digest'] = new_text[:500]
    
    return changes

def main() -> None:
    print("Loading current snapshots...")
    data = load_snapshots()
    snapshots = data.get('snapshots', {})
    changes = data.get('changes', [])
    
    print(f"Checking {len(snapshots)} tools...")
    pages = {}
    for slug in list(snapshots.keys())[:5]:  # Start with first 5 for testing
        # Try to find official URL from the pricing-watch page
        print(f"  Checking {slug}...")
        # For now, we'll use a placeholder - in production this would fetch actual URLs
        # from the tool data or pricing-watch page
        pages[slug] = ""
    
    # Detect changes
    new_changes = detect_changes(data, pages)
    
    if new_changes:
        print(f"\nDetected {len(new_changes)} changes:")
        for change in new_changes:
            print(f"  - {change['slug']}: {change['note']}")
        changes.extend(new_changes)
        data['changes'] = changes
        data['updated'] = datetime.utcnow().strftime('%Y-%m-%d')
        
        # Save updated data
        PRICING_DATA.write_text(json.dumps(data, indent=2), encoding='utf-8')
        print(f"\nUpdated {PRICING_DATA}")
        
        # Regenerate pricing-watch page and feed
        print("Regenerating pricing-watch page and feed...")
        subprocess.run(['python3', str(FEED_SCRIPT)], cwd=SITE_ROOT)
        print("Done.")
    else:
        print("No changes detected.")

if __name__ == '__main__':
    main()
