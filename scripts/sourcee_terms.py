#!/usr/bin/env python3
"""Shared token sets for the Sourcee journo-request monitor.

Why this module exists: the per-run window scripts (`marketing/haro-outreach/_window_*.py`)
each rolled their own AI regex, and that regex listed product classes (`ai`, `llm`, `gpt`,
`agents`, `automation`, `ml`) but no vendor names. On 2026-10-11 that cost the monitor a real
find: `anthropic-gtm-leaders-scaling-300k-b2b-clients` sat in the 2026-10-10 sitemap window,
its body was fetched, and it was then dropped, because the slug says "anthropic" and not one
of the AI tokens. A journalist request about the company serving 300k B2B clients is core beat
for a site that tracks Anthropic's seat and token prices; the filter, not the supply, lost it.

The AI token list therefore carries vendor and product names as well as product classes. Keep
this list here rather than in each `_window_*.py` so the next run inherits the fix.
"""
from __future__ import annotations

import re

# Product classes AND vendor/product names. A slug can name a vendor without naming an AI class.
AI_TOKENS = (
    # product classes
    "ai", "a-i", "llm", "gpt", "chatgpt", "claude", "gemini", "copilot", "agents?",
    "machine-learning", "automation", "ml", "genai", "gen-ai", "chatbot", "rag",
    "inference", "prompt", "token-burn", "tokenmaxxing", "agentic", "foundation-model",
    # vendors and products (added 2026-10-11 after the Anthropic miss)
    "anthropic", "openai", "open-ai", "chat-gpt", "deepseek", "mistral", "llama", "grok",
    "perplexity", "midjourney", "elevenlabs", "eleven-labs", "nvidia", "microsoft-365",
    "m365", "salesforce", "hubspot", "zapier", "n8n", "databricks", "snowflake",
    "scale-ai", "hugging-face", "huggingface", "cohere", "stability-ai", "runway",
    "grammarly", "jasper", "synthesia", "descript", "notion-ai", "canva-ai", "cursor",
    "windsurf", "replit", "v0", "lovable", "browse-ai", "gamma", "otter", "fireflies",
    # added 2026-10-18: xAI names itself in slugs and bodies without any other AI token. A Memphis
    # data-centre request carried 'xai' in its slug and scored as a non-AI request for a whole run;
    # it was found only because every window body is also read.
    "xai", "x-ai",
)

AI = re.compile(r"(^|[-/])(" + "|".join(AI_TOKENS) + r")([-/]|$)", re.I)

SPEND = re.compile(
    r"(pricing|prices?|price|cost|costs|spend|spending|budget|budgets|subscription|subscriptions|"
    r"saas|licen[cs]e|seat|seats|billing|invoice|credits|procurement|roi|pay|paid|afford)", re.I)

# A spend token that survives word-boundary checks — "paid" inside "portadown" is not spend.
REAL_SPEND = re.compile(
    r"(?<![a-z])(pricing|prices?|costs?|spend(?:ing)?|budgets?|subscriptions?|saas|"
    r"licen[cs]es?|seats?|billing|invoices?|credits|procurement|roi|afford)(?![a-z])", re.I)

# Prose-mode AI matcher. AI above is written for SLUGS, where a token must be delimited by
# hyphens, so it never matches the word "AI" inside a request body and the body-level scan
# reported a false zero on every run up to and including 2026-10-13. This one is written for
# prose: word boundaries, no hyphen requirement, plus the two-word forms that only appear in
# sentences ("generative ai", "machine learning", "large language model").
AI_PROSE = re.compile(
    r"\b(ai|a\.i\.|llms?|large language models?|machine learning|generative ai|genai|gen-ai|"
    r"chatgpts?|chat gpt|claude|gemini|copilot|agentic|chatbots?|anthropic|openai|open-ai|"
    r"deepseek|mistral|llama|grok|perplexity|midjourney|elevenlabs|nvidia|m365|"
    r"microsoft 365|salesforce|hubspot|zapier|n8n|databricks|snowflake|hugging face|cohere|"
    r"runway|grammarly|jasper|synthesia|descript|cursor|windsurf|replit|browse ai|gamma|otter|"
    r"fireflies)\b", re.I)


def ai_hit(slug: str) -> list[str]:
    """Every AI token in a slug — vendor names included."""
    return sorted({m.group(2).lower() for m in AI.finditer(slug)})


def prose_ai(text: str) -> list[str]:
    """Every AI token in a request BODY. Use this, not `AI`, on prose — see AI_PROSE above."""
    return sorted({m.group(1).lower() for m in AI_PROSE.finditer(text or "")})


if __name__ == "__main__":
    for s in ("anthropic-gtm-leaders-scaling-300k-b2b-clients",
              "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring",
              "employees-pay-transparency-good-or-bad",
              "portadown-residents-and-community-organisers-last-two-weeks",
              "google-and-claude-enterprise-users-seats-and-token-costs"):
        print(f"{str(ai_hit(s)):<34} spend={bool(SPEND.search(s))} real_spend={bool(REAL_SPEND.search(s))}  {s}")
