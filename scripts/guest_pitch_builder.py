#!/usr/bin/env python3
"""Guest post / podcast pitch finder and email builder.

Finds AI tools podcasts, newsletters, and blogs that accept guest contributions.
Generates personalized pitch emails based on their content.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = SITE_ROOT / "marketing" / "guest-pitches"
OUTPUT_DIR.mkdir(exist_ok=True)

# Target outlets for guest pitches
TARGETS = [
    {
        "name": "The Rundown AI",
        "type": "newsletter",
        "contact": "support@therundown.ai",
        "audience": "AI tool buyers and operators",
        "angle": "resource for tool roundups",
        "url": "https://therundown.ai"
    },
    {
        "name": "TLDR AI",
        "type": "newsletter", 
        "contact": "dan@tldr.tech",
        "audience": "engineering managers and developers",
        "angle": "verified pricing snapshots as source",
        "url": "https://tldr.tech/ai"
    },
    {
        "name": "Ben's Bites",
        "type": "newsletter",
        "contact": "team@bensbites.com",
        "audience": "AI enthusiasts and builders",
        "angle": "resource for launch roundups",
        "url": "https://bensbites.com"
    },
    {
        "name": "The Neuron",
        "type": "newsletter",
        "contact": "team@theneurondaily.com",
        "audience": "AI operators and founders",
        "angle": "pricing intelligence source",
        "url": "https://theneurondaily.com"
    },
    {
        "name": "ToolChase",
        "type": "blog",
        "contact": "hello@toolchase.com",
        "audience": "AI tool buyers",
        "angle": "verified pricing source for roundups",
        "url": "https://toolchase.com"
    },
    {
        "name": "ToolRadar",
        "type": "blog",
        "contact": "contact@aitoolradar.io",
        "audience": "AI tool evaluators",
        "angle": "editorial perspective on AI pricing trends",
        "url": "https://aitoolradar.io"
    },
    {
        "name": "Last Week in AI",
        "type": "podcast",
        "contact": "contact@lastweekinai.com",
        "audience": "AI researchers and practitioners",
        "angle": "guest on overlapping subscriptions",
        "url": "https://lastweekinai.com"
    },
    {
        "name": "Changelog / Practical AI",
        "type": "podcast",
        "contact": "editors@changelog.com",
        "audience": "developers and AI practitioners",
        "angle": "guest on AI tool evaluation methodology",
        "url": "https://changelog.com/practicalai"
    },
    {
        "name": "infoDOCKET",
        "type": "blog",
        "contact": "gprice@gmail.com",
        "audience": "library and information professionals",
        "angle": "AI pricing intelligence resource",
        "url": "https://infodocket.com"
    },
    {
        "name": "AIToolsRecap",
        "type": "blog",
        "contact": "editor@aitoolsrecap.com",
        "audience": "AI tool buyers",
        "angle": "cross-directory pricing verification",
        "url": "https://aitoolsrecap.com"
    }
]

PITCH_TEMPLATES = {
    "newsletter": """Subject: Resource for {outlet_name} — verified AI pricing snapshots

Hi {contact_name},

I read {outlet_name} regularly — {specific_observation}.

One resource I can offer for your coverage: I run AIToolsEssentials, where we review AI tools with verified pricing from official pages and dated evidence. We track 74 tools and re-verify pricing weekly.

Our Pricing Watch page (https://aitoolsessentials.com/pricing-watch/) is a source for tool roundups, pricing changes, and overlap warnings. Every claim has a checked date and a source link.

Happy to be cited or to send advance notice when we detect price changes.

No strings — if it's useful, use it.

— George Zikry
AIToolsEssentials
https://aitoolsessentials.com""",

    "blog": """Subject: Source for {outlet_name} — AI tool pricing verification

Hi {contact_name},

I've been following {outlet_name} and appreciate {specific_observation}.

I wanted to offer a source: AIToolsEssentials reviews AI tools with verified pricing from official pages and dated evidence. We track 74 tools and re-verify pricing weekly against vendor official pages.

A few recent findings your readers might find useful:
- The most common overlap: Copilot Pro ($10) + Cursor Pro ($20) + Claude Max ($100+) = $130/month for the same coding job
- Microsoft 365 raised commercial pricing ~16% in July 2026 while expanding AI tool catalogs
- ChatGPT Pro split into two tiers ($120/$200) in Q2 2026

I'm happy to provide specific pricing comparisons, official page screenshots, or commentary.

— George Zikry
AIToolsEssentials
https://aitoolsessentials.com""",

    "podcast": """Subject: Guest idea: how to stop paying for overlapping AI tools

Hi {contact_name},

Quick guest pitch for {outlet_name}: most teams now pay for 2+ overlapping AI subscriptions. I run AIToolsEssentials — we review AI tools with verified pricing and keep/cut verdicts. I can walk through:

- The most common overlaps (assistant × 2, meeting notes × 2, coding × 2)
- How to run a one-week test before any renewal
- What "worth it" actually means per tool

Audience walks away able to cut at least one subscription. Happy to prep a one-pager in advance.

— George Zikry
AIToolsEssentials
https://aitoolsessentials.com"""
}

def generate_pitches() -> list[dict]:
    """Generate personalized pitch emails for each target."""
    pitches = []
    today = datetime.utcnow().strftime('%Y-%m-%d')
    
    for target in TARGETS:
        template = PITCH_TEMPLATES.get(target["type"], PITCH_TEMPLATES["newsletter"])
        
        # Customize specific observation based on outlet
        specific_observations = {
            "The Rundown AI": "your daily roundups are one of the few newsletters I actually read",
            "TLDR AI": "the engineering-focused format makes complex topics scannable",
            "Ben's Bites": "your launch coverage is consistently thorough",
            "The Neuron": "your no-hype approach to AI tools is refreshing",
            "ToolChase": "your pricing verification methodology is solid",
            "ToolRadar": "your editorial independence stands out",
            "Last Week in AI": "your coverage of AI industry developments is thorough",
            "Changelog / Practical AI": "your technical depth is unmatched",
            "infoDocket": "your library perspective on information tools is unique",
            "AIToolsRecap": "your directory comparison approach is valuable"
        }
        
        specific = specific_observations.get(target["name"], "the quality of your coverage")
        
        pitch = template.format(
            outlet_name=target["name"],
            contact_name=target["contact"].split("@")[0],
            specific_observation=specific
        )
        
        pitches.append({
            "outlet": target["name"],
            "type": target["type"],
            "contact": target["contact"],
            "audience": target["audience"],
            "angle": target["angle"],
            "pitch": pitch,
            "generated": today
        })
    
    return pitches

def save_pitches(pitches: list[dict]) -> Path:
    """Save pitches to a file."""
    today = datetime.utcnow().strftime('%Y-%m-%d')
    output_file = OUTPUT_DIR / f"pitches-{today}.json"
    output_file.write_text(json.dumps(pitches, indent=2), encoding='utf-8')
    print(f"Saved {len(pitches)} pitches to {output_file}")
    return output_file

def main():
    print("Guest Post / Podcast Pitch Builder")
    print("=" * 40)
    
    pitches = generate_pitches()
    
    print(f"\nGenerated {len(pitches)} pitches:")
    for p in pitches:
        print(f"  - [{p['type']}] {p['outlet']} ({p['contact']})")
    
    save_pitches(pitches)
    
    print("\nSample pitch (newsletter):")
    print("-" * 40)
    for p in pitches:
        if p["type"] == "newsletter":
            print(p["pitch"])
            break

if __name__ == "__main__":
    main()
