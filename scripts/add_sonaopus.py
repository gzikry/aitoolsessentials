#!/usr/bin/env python3
"""Add Sonaopus to the directory after the vendor cleared independent verification.

Submission arrived via /submit-tool.html (FormSubmit) on 2026-09-09 and was held pending
public legal pages, controller identity, and pricing/name checks. The vendor published
Privacy Policy and Terms of Service on 2026-09-12 and answered every outstanding question,
so the listing is now published with the remaining caveats recorded as cons/unresolved claims.

Vendor follow-up 2026-09-13: homepage FAQ no longer says "Nothing stored"; a standalone
legal-review FAQ is live; affiliate terms were stated in writing (40% one-time, 30-day
cookie, Gumroad). Those three items are closed in verification notes, not open questions.

Facts verified independently on 2026-09-12 (not taken from the submission):
- $99 USD one-time on all five Gumroad products; no subscription (Gumroad structured data
  reports 99, and the live product pages were renamed to /l/ai-hr-management etc.).
- Privacy Policy at /privacy and Terms of Service at /terms, both live 2026-09-12, naming
  operator Praise Boyinde, governing law Nigeria, output ownership retained by the user,
  no-refunds position, and the two subprocessors that actually touch data (Netlify, Gumroad).
- Shipped JavaScript: localStorage keys sonaopus_hr/_ea/_pm/_re/_role; zero fetch/XHR/
  sendBeacon/WebSocket calls; no third-party <script src>; handoff targets claude.ai/new,
  chatgpt.com/, gemini.google.com/ carry no query parameters.
- The $59 figure is a stale third-party mirror (devadex.com) of a retired Gumroad account
  (sonaopusaiworkflow.gumroad.com) that now returns 404.
- sonaopus.com has no MX records, so the published Gmail contact is the only working address.
"""
from pathlib import Path
import json
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()

TOOL = {
    "slug": "sonaopus",
    "name": "Sonaopus",
    "category": "Productivity",
    "best_for": "Structuring HR, EA, project, recruiting, and real-estate situations into prompts that produce usable documents",
    "price": "$99 one-time per profession (five products)",
    "rating": 4.1,
    "official": "https://sonaopus.com/",
    "summary": "A prompt-structuring layer for five professions. You describe your situation once in a profession-specific multi-stage workflow, and Sonaopus pre-loads it into Claude, ChatGPT, or Gemini so the assistant drafts the HR policy, employee-relations letter, status report, or listing copy without you re-explaining the context.",
    "use_cases": [
        "Drafting HR policies and employee-relations letters",
        "Executive briefings, meeting prep, and correspondence",
        "Project status reports and risk logs",
        "Job adverts, screening assessments, and candidate outreach",
        "Property listing copy and CMA summaries",
    ],
    "pros": [
        "The handoff works the way it is described: your input opens in Claude or ChatGPT, or is copied to the clipboard for Gemini, with no query parameters carrying data in a URL",
        "Verified local-device storage \u2014 workflow inputs live in browser storage on your machine, and the page makes no fetch or XHR calls and loads no analytics or telemetry scripts",
        "Real free tier: eight generations per profession, no signup and no card",
        "Output ownership is stated plainly \u2014 you retain all rights to what you enter and to the draft your AI assistant writes from it",
        "Terms name the operator (Praise Boyinde, sole proprietor), the governing law (Nigeria), the subprocessors that actually hold data (Netlify, Gumroad), and a no-refunds position explained by the free trial",
    ],
    "cons": [
        "Not a writing tool \u2014 it structures your situation and hands it to Claude, ChatGPT, or Gemini; the draft quality still depends on whichever assistant you already use.",
        "No export for the workflow data stored locally, so clearing site data for sonaopus.com discards in-progress work",
        "No team, self-hosted, or shared-seat option, and the $99 one-time price applies per profession",
        "sonaopus.com publishes no MX records, so the only working contact is a personal Gmail address",
        "A stale third-party mirror still advertises the retired pre-launch $59 price, so search results can show a figure the vendor no longer charges",
    ],
    "key_features": [
        "Five profession toolkits: HR Management, Executive Assistant, Project Management, Real Estate, Recruiting",
        "Multi-stage workflow that carries your context forward between stages",
        "One-click handoff into Claude or ChatGPT with the input pre-loaded",
        "Clipboard handoff for Gemini",
        "Local browser storage of workflow inputs, output history, and in-progress state",
        "Eight free generations per profession before purchase",
        "One-time purchase with lifetime access to future updates for that profession",
        "Public affiliate program listed at 40% through Gumroad",
    ],
    "faq": [
        [
            "Is Sonaopus free?",
            "There is a free tier: eight generations per profession with no signup and no card. After that, each profession-specific toolkit is a $99 one-time purchase and there is no subscription. All five products were listed at $99 when we checked on 2026-09-12.",
        ],
        [
            "Does Sonaopus store my data?",
            "Workflow inputs, output history, and in-progress state stay in your browser's local storage on your own device, and the page makes no server calls. We re-checked sonaopus.com on 2026-09-13: the old homepage FAQ line \u201cNothing stored\u201d is gone, and the on-page wording now matches the Privacy Policy \u2014 everything runs in the browser, progress saves locally, and nothing is sent until you hand it to Claude, ChatGPT, or Gemini. Clearing site data deletes the local copy; there is no server-side copy to delete or export.",
        ],
        [
            "Does Sonaopus send my input to Sonaopus's servers?",
            "No. The handoff either opens Claude or ChatGPT with your input pre-loaded or copies it to your clipboard for Gemini, and no query parameters ride in a URL. Once you send it onward, Anthropic's, OpenAI's, or Google's own privacy policy governs it, not Sonaopus's.",
        ],
        [
            "Is Sonaopus a legal or HR advisory service?",
            "No. The Terms state that using Sonaopus creates no legal, HR, or financial advisory relationship. Outputs are drafts your chosen AI assistant writes from your input. As of 2026-09-13 the homepage has a standalone FAQ that treats ER letters, HR policies, and similar outputs as drafts to verify, and flags legal or compliance risk on-screen.",
        ],
    ],
    "trial_checklist": "Run one real task in a profession you actually work in \u2014 an ER letter, a policy, or a status report \u2014 not a demo prompt. Enter your genuine jurisdiction and organisation size, because the workflow changes what gets written from them. Before sending anything onward, open your browser's site-data settings for sonaopus.com and check what was stored locally, so you know what is on the device. Then compare how much re-explaining the multi-stage flow saves against prompting your AI assistant directly, and factor the eight-generation cap into whether $99 is worth it for that one profession.",
    "hands_on_status": "not_tested",
    "hands_on_priority": "medium",
    "rating_rationale": "Job fit 4 - five profession-specific workflows cover repeated document jobs across HR, EA, project management, recruiting and real estate, with context carried between stages. It is a prompt-structuring layer used alongside Claude, ChatGPT, or Gemini, not a writing tool in its own right. Output quality 4 - the drafts come from whichever assistant you already use, and the workflows do embed jurisdiction and legal-review instructions. Adoption 4 - no account or install is required and eight generations are free per profession; you still need an AI assistant to produce the draft. Cost 4 - $99 one-time with lifetime updates for one profession is reasonable if you need that one profession, and there is no subscription to forget to cancel. Held at 4.1 because there is no export for the local workflow data, and a stale mirror still advertises a retired $59 price.",
}

SOURCE = {
    "slug": "sonaopus",
    "pricing_checked_date": TODAY,
    "pricing_summary": "$99 USD one-time per profession-specific product, no subscription and no recurring charge. Five products: HR Management, Executive Assistant, Project Management, Real Estate, Recruiting. Free tier: up to eight generations per profession before purchase, with no signup or card. Lifetime access covers future updates to that profession's tool. Terms state that except where required by law all purchases are final and no refunds are offered, with the free trial given as the reason. A stale third-party mirror (devadex.com) still lists a retired pre-launch $59 price; the mirrored store account sonaopusaiworkflow.gumroad.com now returns 404 and the price on every live vendor page is $99.",
    "verification_notes": "Submitted via /submit-tool.html by the vendor on 2026-09-09 and held pending verification. The vendor published /privacy and /terms on 2026-09-12 and answered every outstanding question, so the listing was published 2026-09-12 with remaining caveats recorded in cons and unresolved_claims. Editorial entry written independently; no submission copy was reused. Verified on 2026-09-12: both legal pages live and substantive; all five Gumroad products at $99 with no subscription; shipped JavaScript writes only sonaopus_hr/_ea/_pm/_re/_role to localStorage, makes zero fetch/XHR/sendBeacon calls, and has no third-party script tags; handoff targets claude.ai/new, chatgpt.com/ and gemini.google.com/ carry no query parameters. Operator: Praise Boyinde, sole proprietor, no registered entity, governing law Nigeria. The domain publishes no MX records, so the Gmail address printed in both legal pages is the only reachable contact. Re-checked 2026-09-13 against the live homepage and a vendor email the same day. Closed: the homepage FAQ no longer says \u201cNothing stored\u201d; on-page copy now matches the Privacy Policy (everything runs in the browser, progress saves locally, nothing is sent until you hand it to an assistant). Closed: a standalone legal-review FAQ (\u201cNothing happens without you\u201d) is live and treats ER letters, HR policies, and similar outputs as drafts to verify, with legal or compliance risk flagged on-screen. Closed: affiliate terms were stated in writing by the vendor on 2026-09-13 \u2014 40% flat one-time commission ($39.60 per $99 product), no recurring commission because there is no subscription, 30-day cookie, attribution and payout through Gumroad; signup at https://sonaopus.com/ or https://sonaopus.gumroad.com/affiliates. We have not enrolled and have not wired a tracking URL.",
    "pricing_url": "https://sonaopus.com/",
    "docs_url": "https://sonaopus.com/terms",
    "privacy_url": "https://sonaopus.com/privacy",
    "rights_url": "https://sonaopus.com/terms",
    "unresolved_claims": [
        "No service address or city/country is published for the seller or data controller; the vendor declined to publish one beyond the Nigeria governing-law clause. The operator name is disclosed.",
        "No data-export feature exists for locally stored workflow data; the Privacy Policy states this and directs users to contact support.",
        "A stale third-party mirror (devadex.com) continues to advertise a retired $59 pre-launch price for the HR product. The mirrored Gumroad account now 404s; the mirror is outside the vendor's direct control.",
    ],
}

REVENUE_TARGET = {
    "tool_slug": "sonaopus",
    "tool_name": "Sonaopus",
    "priority": "low",
    "category": "Productivity",
    "recommended_networks_to_check": ["Direct vendor program (Gumroad affiliate)"],
    "search_queries": [],
    "target_pages": ["/tools/sonaopus/"],
    "best_audiences": ["HR and people-operations buyers", "workflow-specific buyers"],
    "status": "not_started",
    "next_action": "Vendor stated affiliate terms in writing on 2026-09-13. Do not invent enrollment. Apply only when ready to accept a Gumroad tracking URL; keep the official site URL on the review until then.",
    "notes": "Vendor-stated 2026-09-13: 40% flat one-time ($39.60 per $99 product); no recurring commission; 30-day cookie; Gumroad tracks and pays. Signup: https://sonaopus.com/ or https://sonaopus.gumroad.com/affiliates. Not enrolled. Do not invent affiliate URLs.",
}

SNAPSHOT = {
    "date": TODAY,
    "digest": "$99 USD one-time per profession (five products: HR Management, Executive Assistant, Project Management, Real Estate, Recruiting); no subscription. Free tier of eight generations per profession with no signup or card. Lifetime access includes future updates for that profession. Purchases are final with no refunds except where required by law. A stale third-party mirror still lists a retired $59 pre-launch price; live vendor pages all show $99.",
    "changes": "initial_entry",
    "sources": ["https://sonaopus.com/", "https://sonaopus.com/terms", "https://sonaopus.com/privacy"],
}


def main() -> None:
    tools_path = ROOT / "data/tools.json"
    tools = json.loads(tools_path.read_text())
    if any(t["slug"] == TOOL["slug"] for t in tools):
        print("sonaopus already present in tools.json; nothing to do")
        return
    tools.append(TOOL)
    tools_path.write_text(json.dumps(tools, indent=2, ensure_ascii=False) + "\n")

    sources_path = ROOT / "data/tool_sources.json"
    sources = json.loads(sources_path.read_text())
    sources["tools"].append(SOURCE)
    sources["checked_at"] = TODAY
    sources_path.write_text(json.dumps(sources, indent=2, ensure_ascii=False) + "\n")

    targets_path = ROOT / "data/revenue_targets.json"
    targets = json.loads(targets_path.read_text())
    targets.append(REVENUE_TARGET)
    targets_path.write_text(json.dumps(targets, indent=2, ensure_ascii=False) + "\n")

    snapshots_path = ROOT / "data/pricing_snapshots.json"
    snapshots = json.loads(snapshots_path.read_text())
    snapshots["snapshots"][TOOL["slug"]] = SNAPSHOT
    snapshots["updated"] = TODAY
    snapshots_path.write_text(json.dumps(snapshots, indent=2, ensure_ascii=False) + "\n")

    print(f"Added sonaopus: tools={len(tools)} sources={len(sources['tools'])} targets={len(targets)} snapshots={len(snapshots['snapshots'])}")


if __name__ == "__main__":
    main()
