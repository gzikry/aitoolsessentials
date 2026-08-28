#!/usr/bin/env python3
"""Sync pricing changes into the current newsletter issue."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
PRICING_DATA = SITE_ROOT / "data" / "pricing_snapshots.json"
ISSUES_DATA = SITE_ROOT / "data" / "weekly_issues.json"
NEWSLETTER_SCRIPT = SITE_ROOT / "scripts" / "generate_weekly_newsletter.py"
TOOLS_DATA = SITE_ROOT / "data" / "tools.json"

def load_tools() -> dict[str, str]:
    """Load tool slug -> name mapping."""
    if not TOOLS_DATA.exists():
        return {}
    tools = json.loads(TOOLS_DATA.read_text(encoding='utf-8'))
    if isinstance(tools, list):
        return {t.get("slug", ""): t.get("name", t.get("slug", "")) for t in tools if t.get("slug")}
    if isinstance(tools, dict):
        return {k: v.get("name", k) for k, v in tools.items() if isinstance(v, dict)}
    return {}

def load_pricing_changes() -> list[dict]:
    """Load pricing changes from canonical source."""
    if not PRICING_DATA.exists():
        return []
    data = json.loads(PRICING_DATA.read_text(encoding='utf-8'))
    return data.get("changes", [])

def get_latest_issue(issues: list[dict]) -> dict | None:
    """Get the latest issue by send_date."""
    if not issues:
        return None
    return max(issues, key=lambda x: x.get("send_date", ""))

def sync_pricing_changes() -> None:
    """Sync pricing changes into the latest newsletter issue."""
    print("Loading data...")
    tools = load_tools()
    pricing_changes = load_pricing_changes()
    
    if not pricing_changes:
        print("No pricing changes to sync.")
        return
    
    issues = json.loads(ISSUES_DATA.read_text(encoding='utf-8'))
    latest = get_latest_issue(issues)
    
    if not latest:
        print("No issues found to update.")
        return
    
    # Check if already synced
    existing = latest.get("pricing_changes", [])
    existing_slugs = {p.get("slug") for p in existing}
    
    # Add any new changes not already in the issue
    new_changes = []
    for change in pricing_changes:
        slug = change.get("slug", "")
        if slug and slug not in existing_slugs:
            name = tools.get(slug, slug.replace("-", " ").title())
            new_changes.append({
                "name": name,
                "slug": slug,
                "change": change.get("note", f"Pricing change detected {change.get('detected', '')}")
            })
    
    if not new_changes:
        print("Latest issue already has all current pricing changes.")
        return
    
    # Update the issue
    updated_changes = existing + new_changes
    latest["pricing_changes"] = updated_changes
    
    # Save
    ISSUES_DATA.write_text(json.dumps(issues, indent=2), encoding='utf-8')
    print(f"Added {len(new_changes)} new pricing changes to issue {latest.get('slug')}:")
    for p in new_changes:
        print(f"  - {p['name']}: {p['change']}")
    
    # Regenerate newsletter
    print("Regenerating newsletter...")
    import subprocess
    result = subprocess.run(
        ['python3', str(NEWSLETTER_SCRIPT)],
        cwd=SITE_ROOT,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"Newsletter regenerated: {result.stdout.strip()}")
    else:
        print(f"Error regenerating newsletter: {result.stderr}")
        return 1
    
    print("Done.")
    return 0

if __name__ == "__main__":
    exit(sync_pricing_changes() or 0)
