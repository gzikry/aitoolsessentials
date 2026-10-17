#!/usr/bin/env python3
"""Restore public URLs that were removed without a redirect between Aug 21 and Sep 15, 2026.

Each row is the old path, the current path, and the visible title. The writer
leaves the same noindex refresh stub the duplicate-page consolidations use.
"""
from __future__ import annotations

from pathlib import Path

# Old path, current path, title. Current paths match the URL GitHub Pages serves.
LEGACY = (
    ("tools/adobe-firefly.html", "tools/adobe-firefly/", "Adobe Firefly review"),
    ("tools/airtable-ai.html", "tools/airtable-ai/", "Airtable AI review"),
    ("tools/bolt-new.html", "tools/bolt-new/", "Bolt.new review"),
    ("tools/canva-ai.html", "tools/canva-ai/", "Canva AI review"),
    ("tools/chatgpt.html", "tools/chatgpt/", "ChatGPT review"),
    ("tools/claude.html", "tools/claude/", "Claude review"),
    ("tools/copy-ai.html", "tools/copy-ai/", "Copy.ai review"),
    ("tools/cursor.html", "tools/cursor/", "Cursor review"),
    ("tools/deepseek.html", "tools/deepseek/", "DeepSeek review"),
    ("tools/descript.html", "tools/descript/", "Descript review"),
    ("tools/elevenlabs.html", "tools/elevenlabs/", "ElevenLabs review"),
    ("tools/fathom.html", "tools/fathom/", "Fathom review"),
    ("tools/fireflies.html", "tools/fireflies/", "Fireflies.ai review"),
    ("tools/gamma.html", "tools/gamma/", "Gamma review"),
    ("tools/gemini.html", "tools/gemini/", "Gemini review"),
    ("tools/github-copilot.html", "tools/github-copilot/", "GitHub Copilot review"),
    ("tools/grammarly.html", "tools/grammarly/", "Grammarly review"),
    ("tools/grok.html", "tools/grok/", "Grok review"),
    ("tools/heygen.html", "tools/heygen/", "HeyGen review"),
    ("tools/jasper.html", "tools/jasper/", "Jasper review"),
    ("tools/leonardo-ai.html", "tools/leonardo-ai/", "Leonardo AI review"),
    ("tools/lovable.html", "tools/lovable/", "Lovable review"),
    ("tools/make.html", "tools/make/", "Make review"),
    ("tools/meta-ai.html", "tools/meta-ai/", "Meta AI review"),
    ("tools/microsoft-copilot.html", "tools/microsoft-copilot/", "Microsoft Copilot review"),
    ("tools/midjourney.html", "tools/midjourney/", "Midjourney review"),
    ("tools/mistral-le-chat.html", "tools/mistral-le-chat/", "Mistral Le Chat review"),
    ("tools/n8n.html", "tools/n8n/", "n8n review"),
    ("tools/notion-ai.html", "tools/notion-ai/", "Notion AI review"),
    ("tools/otter-ai.html", "tools/otter-ai/", "Otter.ai review"),
    ("tools/perplexity.html", "tools/perplexity/", "Perplexity review"),
    ("tools/poe.html", "tools/poe/", "Poe review"),
    ("tools/replit-ai.html", "tools/replit-ai/", "Replit AI review"),
    ("tools/runway.html", "tools/runway/", "Runway review"),
    ("tools/slack-ai.html", "tools/slack-ai/", "Slack AI review"),
    ("tools/synthesia.html", "tools/synthesia/", "Synthesia review"),
    ("tools/v0.html", "tools/v0/", "v0 review"),
    ("tools/you-com.html", "tools/you-com/", "You.com review"),
    ("tools/zapier-ai.html", "tools/zapier-ai/", "Zapier AI review"),
    ("tools/adobe-podcast/index.html", "tools/adobe-enhance-speech/", "Adobe Podcast review"),
    ("tools/riverside/index.html", "tools/riverside-fm/", "Riverside review"),
    ("tools/hootsuite/index.html", "articles/hootsuite-vs-buffer-ai.html", "Hootsuite vs Buffer"),
    ("tools/hubspot/index.html", "articles/hubspot-vs-zoho-crm-ai.html", "HubSpot vs Zoho CRM"),
    ("tools/mem/index.html", "articles/notion-ai-vs-mem.html", "Notion AI vs Mem"),
    ("categories/Audio Production/index.html", "categories/Audio & Video/", "Audio production AI tools"),
    ("categories/Audio/index.html", "categories/Audio & Video/", "Audio AI tools"),
    ("categories/Music & Audio/index.html", "categories/Audio & Video/", "Music and audio AI tools"),
    ("categories/Podcast/index.html", "categories/Audio & Video/", "Podcast AI tools"),
    ("categories/Browser Automation/index.html", "categories/Automation/", "Browser automation AI tools"),
    ("categories/Creative & Marketing/index.html", "categories/Creative/", "Creative and marketing AI tools"),
    ("categories/Marketing/index.html", "categories/Creative/", "Marketing AI tools"),
    ("categories/Image Generation/index.html", "categories/Creative/", "Image generation AI tools"),
    ("categories/Presentations/index.html", "categories/Creative/", "Presentation AI tools"),
    ("categories/Email AI/index.html", "categories/Productivity/", "Email AI tools"),
    ("categories/Writing & Productivity/index.html", "categories/Productivity/", "Writing and productivity AI tools"),
    ("categories/Model Hub/index.html", "categories/General AI Assistant/", "Model hub AI tools"),
    ("categories/Video & 3D/index.html", "categories/Video/", "Video and 3D AI tools"),
    ("categories/Video Generation/index.html", "categories/Video/", "Video generation AI tools"),
    ("articles/best-ai-tools-for-podcasters.html", "articles/best-ai-tools-for-podcast-shows.html", "Best AI tools for podcasters"),
    ("use-cases/best-ai-tools-for-podcasters.html", "articles/best-ai-tools-for-podcast-shows.html", "Best AI tools for podcasters"),
    ("articles/why-we-moved-the-497-audit-into-premium.html", "premium/", "Why the audit moved into Premium"),
    ("vendors/submit-tool.html", "submit-tool.html", "Submit a tool"),
    ("marketing/linkable-assets/coding-assistant-quiz.html", "quiz/coding-assistant-keep-cut.html", "Coding assistant quiz"),
)


def write_legacy_redirects(root: Path) -> int:
    """Write a noindex refresh stub for every legacy path. Returns how many changed."""
    from consolidate_duplicates import redirect_stub

    written = 0
    root = Path(root)
    for loser, winner, title in LEGACY:
        path = root / loser
        path.parent.mkdir(parents=True, exist_ok=True)
        html = redirect_stub(title, winner)
        if not path.is_file() or path.read_text(encoding="utf-8") != html:
            path.write_text(html, encoding="utf-8")
            written += 1
    return written
