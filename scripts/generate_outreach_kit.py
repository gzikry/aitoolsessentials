#!/usr/bin/env python3
"""Backlink and directory outreach packet.

Calculator wins are the Keep row at one published workload, not a claim that
the tool is cheapest for every job. Directory blocks are copy to submit, not
a record that a submission was sent.
"""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"

# Workloads already used on the public calculators. Keep slugs were read from
# those functions at these inputs (voice/automation via the exported modules;
# coding from the hub FAQ for the same 5-seat, 20-prompt, balanced, monthly case).
WINS = [
    {
        "tool_slug": "descript",
        "calculator": "/compare/ai-video-avatar-cost/",
        "workload": "60 finished minutes, 10 Gen-4.5 seconds, 1 retake, private mode off",
        "result": "Keep on the voice pool at the Free tier ($0). Runway and Midjourney are separate jobs and are not in this pool.",
    },
    {
        "tool_slug": "runway",
        "calculator": "/compare/ai-video-avatar-cost/",
        "workload": "10 generated seconds of Gen-4.5 (12 credits per second)",
        "result": "Keep on its own row at Standard ($15, 625 credits). It does not compete with the voice seats.",
    },
    {
        "tool_slug": "midjourney",
        "calculator": "/compare/ai-video-avatar-cost/",
        "workload": "60 minutes of Fast GPU time, Stealth off",
        "result": "Keep on its own row at Basic ($10, 3.3 Fast hours). It does not compete with the voice seats.",
    },
    {
        "tool_slug": "make",
        "calculator": "/compare/automation-task-calculator/",
        "workload": "3 workflows, 5 steps, 4 runs a day, 100% webhooks",
        "result": "Keep at Core. Zapier has no published dollar at this volume (Professional floor does not cover it). n8n Starter stays in euros and is not converted.",
    },
    {
        "tool_slug": "github-copilot",
        "calculator": "/compare/ai-coding-assistants/",
        "workload": "5 seats, 20 prompts a day, balanced models, monthly billing",
        "result": "The coding hub states Copilot Pro is the lowest published subscription for that profile. Overage is not added, because GitHub does not publish credits per prompt.",
    },
]


def _tools(root: Path) -> list[dict]:
    return json.loads((root / "data" / "tools.json").read_text(encoding="utf-8"))


def _top(tools: list[dict]) -> list[dict]:
    by_slug = {tool["slug"]: tool for tool in tools}
    ordered = []
    seen = set()
    for win in WINS:
        tool = by_slug.get(win["tool_slug"])
        if not tool or tool["slug"] in seen:
            continue
        seen.add(tool["slug"])
        ordered.append({"tool": tool, "win": win})
    rest = sorted(tools, key=lambda tool: float(tool.get("rating") or 0), reverse=True)
    for tool in rest:
        if tool["slug"] in seen:
            continue
        seen.add(tool["slug"])
        ordered.append({"tool": tool, "win": None})
        if len(ordered) >= 25:
            break
    return ordered[:25]


def _vendor_note(row: dict) -> str:
    tool = row["tool"]
    name = tool.get("name") or tool["slug"]
    slug = tool["slug"]
    review = f"{DOMAIN}/tools/{slug}/"
    badge = f"{DOMAIN}/badges/{slug}.svg"
    embed = f'<a href="{review}?utm_source=badge_embed"><img alt="AUDITED BY AI TOOLS ESSENTIALS — {name}" src="{badge}" width="360" height="108"></a>'
    win = row["win"]
    if win:
        where = (
            f"On {win['calculator']} at this workload ({win['workload']}): {win['result']} "
            f"Comparison: {DOMAIN}{win['calculator']}"
        )
    else:
        where = (
            "This note does not claim a calculator win. The review is the dated price record. "
            f"Review: {review}"
        )
    return (
        f"Subject: {name} pricing audit on AI Tools Essentials\n\n"
        f"Hello,\n\n"
        f"We published a dated pricing audit of {name}. The badge below links to the review. "
        f"It is not a ranking and not a paid placement.\n\n"
        f"{where}\n\n"
        f"Review: {review}\n"
        f"Badge: {badge}\n"
        f"HTML: {embed}\n\n"
        f"If a figure on the review is stale, reply with the official pricing URL and we will re-check it.\n"
    )


def build(root: Path) -> dict:
    tools = _tools(root)
    vendors = []
    for row in _top(tools):
        tool = row["tool"]
        win = row["win"]
        vendors.append({
            "tool_slug": tool["slug"],
            "tool_name": tool.get("name"),
            "category": tool.get("category"),
            "review_url": f"{DOMAIN}/tools/{tool['slug']}/",
            "badge_svg": f"{DOMAIN}/badges/{tool['slug']}.svg",
            "calculator_url": f"{DOMAIN}{win['calculator']}" if win else None,
            "calculator_workload": win["workload"] if win else None,
            "calculator_result": win["result"] if win else None,
            "email": _vendor_note(row),
        })
    directories = [
        {
            "name": "Hacker News Show HN",
            "url": "https://news.ycombinator.com/submit",
            "canonical": f"{DOMAIN}/embeds/",
            "copy": (
                "Show HN: audited price badges and four embeddable AI cost calculators\n\n"
                f"We publish dated price receipts for the tools in the catalog ({DOMAIN}/tools/) "
                f"and four browser calculators that do not invent a per-token rate. "
                f"Vendors can embed the badge; the iframe calculators are at {DOMAIN}/embeds/."
            ),
        },
        {
            "name": "Reddit r/SaaS",
            "url": "https://www.reddit.com/r/SaaS/",
            "canonical": f"{DOMAIN}/compare/ai-coding-assistants/",
            "copy": (
                "Data post: published coding-seat prices, not a token estimate.\n\n"
                "Cursor, Claude Code, GitHub Copilot, and Windsurf do not publish a dollar per prompt. "
                f"The calculator picks the published plan for the workload and leaves overage at $0. {DOMAIN}/compare/ai-coding-assistants/"
            ),
        },
        {
            "name": "Reddit r/LocalLLaMA",
            "url": "https://www.reddit.com/r/LocalLLaMA/",
            "canonical": f"{DOMAIN}/local-ai-planner/",
            "copy": (
                "Local workbench planner plus the audited price ledger for hosted seats you might drop.\n\n"
                f"{DOMAIN}/local-ai-planner/ plans memory and model size. "
                f"The hosted-seat overlap receipt is the bill slasher embed: {DOMAIN}/embed/ai-bill-slasher/"
            ),
        },
        {
            "name": "Product Hunt",
            "url": "https://www.producthunt.com/",
            "canonical": f"{DOMAIN}/embeds/",
            "copy": (
                "AI Tools Essentials — audited price badges and embeddable cost calculators.\n\n"
                "Dated official prices, a badge vendors can embed, and four calculators "
                "(coding seats, voice and video minutes, automation tasks, overlap bill). "
                f"{DOMAIN}/embeds/"
            ),
        },
        {
            "name": "AlternativeTo",
            "url": "https://alternativeto.net/",
            "canonical": f"{DOMAIN}/",
            "copy": (
                "Independent pricing ledger for AI tools. Reviews cite the official pricing page and the check date. "
                f"Not a ranked marketplace. {DOMAIN}/"
            ),
        },
        {
            "name": "G2",
            "url": "https://www.g2.com/",
            "canonical": f"{DOMAIN}/legal/editorial-methodology.html",
            "copy": (
                "Methodology: editorial scores are not hands-on lab results and are not for sale. "
                f"{DOMAIN}/legal/editorial-methodology.html"
            ),
        },
        {
            "name": "Dev.to",
            "url": "https://dev.to/",
            "canonical": f"{DOMAIN}/compare/ai-coding-assistants/",
            "copy": (
                "Canonical syndication: AI coding assistant list prices.\n\n"
                f"Original: {DOMAIN}/compare/ai-coding-assistants/\n"
                "Do not republish the calculator as a token bill. Prompts are not converted into tokens."
            ),
        },
        {
            "name": "Hashnode",
            "url": "https://hashnode.com/",
            "canonical": f"{DOMAIN}/embeds/",
            "copy": (
                "Canonical syndication: embed the audited price badge or a 480px calculator.\n\n"
                f"Hub: {DOMAIN}/embeds/\n"
                "Badge URLs look like https://aitoolsessentials.com/badges/<slug>.svg and link back with utm_source=badge_embed."
            ),
        },
    ]
    return {
        "generated_from": "data/tools.json plus the public calculator workloads recorded in scripts/generate_outreach_kit.py",
        "catalog_count": len(tools),
        "vendor_notifications": vendors,
        "directories": directories,
    }


def _markdown(packet: dict) -> str:
    lines = [
        "# Outreach kit — October 2026",
        "",
        f"Catalog size when this file was generated: {packet['catalog_count']}.",
        "Calculator lines are one workload each. They are not a claim that the tool wins every job.",
        "Directory blocks are ready-to-submit copy. They are not a record that the form was sent.",
        "",
        "## Vendor notes",
        "",
    ]
    for row in packet["vendor_notifications"]:
        lines.append(f"### {row['tool_name']}")
        lines.append("")
        lines.append("```")
        lines.append(row["email"].rstrip())
        lines.append("```")
        lines.append("")
    lines.append("## Directories, newsletters, and posts")
    lines.append("")
    for row in packet["directories"]:
        lines.append(f"### {row['name']}")
        lines.append("")
        lines.append(f"Submit at: {row['url']}")
        lines.append(f"Canonical: {row['canonical']}")
        lines.append("")
        lines.append("```")
        lines.append(row["copy"].rstrip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def generate(root: Path) -> Path:
    packet = build(root)
    data_path = root / "data" / "backlink_outreach_targets.json"
    data_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    doc = root / "docs" / "outreach-kit-2026-10.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text(_markdown(packet), encoding="utf-8")
    return data_path
