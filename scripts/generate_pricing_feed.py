#!/usr/bin/env python3
"""Generate RSS feed for AI Pricing Watch changes."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
PRICING_DATA = SITE_ROOT / "data" / "pricing_snapshots.json"
FEED_PATH = SITE_ROOT / "feed-pricing.xml"
DOMAIN = "https://aitoolsessentials.com"

def load_changes() -> list[dict]:
    """Load pricing changes from the canonical JSON source."""
    if not PRICING_DATA.exists():
        return []
    data = json.loads(PRICING_DATA.read_text(encoding='utf-8'))
    return data.get('changes', [])

def build_feed(changes: list[dict]) -> str:
    """Build RSS 2.0 feed from pricing changes."""
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = 'AIToolsEssentials — AI Pricing Watch Changes'
    ET.SubElement(channel, 'link').text = f'{DOMAIN}/pricing-watch/'
    ET.SubElement(channel, 'description').text = 'Confirmed price changes and re-verifications across tracked AI tools.'
    ET.SubElement(channel, 'language').text = 'en'
    ET.SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    for change in changes[:20]:
        entry = ET.SubElement(channel, 'item')
        tool = change.get('slug', 'unknown').replace('-', ' ').title()
        ET.SubElement(entry, 'title').text = f"Price change detected: {tool}"
        ET.SubElement(entry, 'link').text = f"{DOMAIN}/pricing-watch/"
        ET.SubElement(entry, 'guid').text = f"{DOMAIN}/pricing-watch/#change-{change.get('slug', 'unknown')}"
        pub_date = change.get('detected', datetime.utcnow().strftime('%Y-%m-%d'))
        ET.SubElement(entry, 'pubDate').text = datetime.strptime(pub_date, '%Y-%m-%d').strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(entry, 'description').text = change.get('note', 'Pricing change detected.')
    
    return ET.tostring(rss, encoding='unicode')

def main() -> None:
    changes = load_changes()
    
    if not changes:
        # Empty feed placeholder
        changes = [{'slug': 'no-changes-yet', 'note': 'No pricing changes detected in the latest verification run.', 'detected': datetime.utcnow().strftime('%Y-%m-%d')}]
    
    feed = build_feed(changes)
    FEED_PATH.write_text(feed, encoding='utf-8')
    print(f"Generated {FEED_PATH} ({len(changes)} items)")

if __name__ == '__main__':
    main()
