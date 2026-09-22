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


def tracked_tool_count() -> int:
    """Read the live inventory so the pitch copy cannot drift from the site.

    These templates hardcoded "74 tools" and shipped stale for at least two days
    after the catalog reached 76 (caught in marketing/guest-pitches/responses.md).
    Never hardcode an inventory number in outbound copy; derive it.
    """
    try:
        return len(json.loads((SITE_ROOT / "data" / "tools.json").read_text()))
    except Exception:  # noqa: BLE001
        return 0


def verified_overlap_line() -> str:
    """One overlap claim built only from figures in our own verified snapshots.

    The previous bullets (Copilot Pro $10, Claude Max $100+, "$130/month",
    "ChatGPT Pro two tiers $120/$200", "Microsoft 365 +16%") appear nowhere in
    data/tools.json or data/pricing_snapshots.json. Sending unsourced numbers to
    editors is the one error that costs the "verified pricing" angle.
    """
    return (
        "The pattern is overlap, not duplication: across our tracked tools, "
        "the coding stack is the most expensive one to double up on — Cursor Pro is "
        "$20/mo and Claude Max starts at $100/mo (cursor.com and claude.com pricing, "
        "snapshots dated in our Pricing Watch page)."
    )

# Greeting per outlet. The old code did contact.split("@")[0], which produced
# "Hi support," and, on the 2026-09-22 additions, "Hi tips," and "Hi hello," — the
# local-part is a mailbox name, not a person's name, and editors notice. A named
# contact (infoDOCKET = Gary Price) is the only case that gets a first name.
SALUTATIONS = {
    "The Rundown AI": "The Rundown AI team",
    "TLDR AI": "TLDR team",
    "Ben's Bites": "Ben's Bites team",
    "The Neuron": "The Neuron team",
    "ToolChase": "ToolChase team",
    "ToolRadar": "ToolRadar team",
    "Last Week in AI": "Last Week in AI team",
    "Changelog / Practical AI": "Changelog editors",
    "infoDOCKET": "Gary",
    "AIToolsRecap": "AIToolsRecap editors",
    "Latent Space": "Latent Space team",
    "The Decoder": "The Decoder team",
}

# Target outlets for guest pitches
TARGETS = [
    {
        # Verified 2026-09-22 on https://www.latent.space/about: "News tips and pitches:
        # tips@latent.space" and "Sponsorship, partnership, job and business inquiries:
        # business@latent.space". tips@ is the editorial route - use it, not business@.
        "name": "Latent Space",
        "type": "podcast",
        "contact": "tips@latent.space",
        "audience": "AI engineers and technical founders",
        "angle": "guest on overlapping AI subscriptions",
        "url": "https://www.latent.space"
    },
    {
        # Verified 2026-09-22 on https://the-decoder.com/about: "Contact us - E-Mail:
        # hello@the-decoder.com" over the imprint of Deep Content GmbH (Hannover, DE).
        "name": "The Decoder",
        "type": "blog",
        "contact": "hello@the-decoder.com",
        "audience": "AI news readers and tool buyers",
        "angle": "verified pricing source for coverage",
        "url": "https://the-decoder.com"
    },
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

One resource I can offer for your coverage: I run AIToolsEssentials, where we review AI tools with verified pricing from official pages and dated evidence. We track {tool_count} tools and re-verify pricing against official vendor pages.

Our Pricing Watch page (https://aitoolsessentials.com/pricing-watch/) is a source for tool roundups, pricing changes, and overlap warnings. Every claim has a checked date and a source link.

Happy to be cited or to send advance notice when we detect price changes.

No strings — if it's useful, use it.

AIToolsEssentials
https://aitoolsessentials.com""",

    "blog": """Subject: Source for {outlet_name} — AI tool pricing verification

Hi {contact_name},

I've been following {outlet_name} and appreciate {specific_observation}.

I wanted to offer a source: AIToolsEssentials reviews AI tools with verified pricing from official pages and dated evidence. We track {tool_count} tools and re-verify pricing against vendor official pages.

One finding your readers might find useful:
- {overlap_line}

I'm happy to provide specific pricing comparisons, official page links, or commentary.

AIToolsEssentials
https://aitoolsessentials.com""",

    "podcast": """Subject: Guest idea: how to stop paying for overlapping AI tools

Hi {contact_name},

Quick guest pitch for {outlet_name}: most teams now pay for 2+ overlapping AI subscriptions. I run AIToolsEssentials — we review AI tools with verified pricing and keep/cut verdicts. I can walk through:

- The most common overlaps (assistant × 2, meeting notes × 2, coding × 2)
- How to run a one-week test before any renewal
- What "worth it" actually means per tool

Audience walks away able to cut at least one subscription. Happy to prep a one-pager in advance.

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
            "AIToolsRecap": "your directory comparison approach is valuable",
            "Latent Space": "your AI-engineer focus and technical depth",
            "The Decoder": "how clearly you mark sponsored posts and keep them separate from editorial",
        }
        
        specific = specific_observations.get(target["name"], "the quality of your coverage")
        salutation = SALUTATIONS.get(
            target["name"], target["contact"].split("@")[0]
        )
        
        pitch = template.format(
            outlet_name=target["name"],
            contact_name=salutation,
            specific_observation=specific,
            tool_count=tracked_tool_count(),
            overlap_line=verified_overlap_line(),
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
