"""Deterministic Stack Audit engine and catalog contract.

Spend is never inferred from directory price labels such as "Free + paid".
Affiliate/sponsor flags are stored for disclosure only and never affect
score, recommendations, inclusion, or ranking.
The $20 / $35 viral.js planning heuristic is not used.
"""
from __future__ import annotations

import base64
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "data" / "stack_audit_rules.json"

CUSTOM_SLUG_RE = re.compile(r"^c:[a-z0-9][a-z0-9-]{0,47}$")
DIR_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
NAME_SANITIZE_RE = re.compile(r"[^a-zA-Z0-9 .'+&/-]+")
PROMO_RE = re.compile(r"promo|promotional|first month|first-year|discount|% off", re.I)

CATEGORY_HINTS = {
    "Audio & Video": ["audio", "video"],
    "Automation": ["automation"],
    "Creative": ["design"],
    "Development": ["coding"],
    "General AI Assistant": ["writing", "research"],
    "Meetings": ["meetings"],
    "Productivity": ["email"],
    "Research": ["research"],
    "Video": ["video"],
    "AI Agents": ["automation"],
    "Local AI": ["local"],
    "Healthcare": ["writing"],
    "Legal": ["writing", "research"],
    "Education": ["writing", "presentations"],
    "Nonprofit": ["writing", "marketing"],
    "Property Management": ["writing", "email"],
}

KEYWORD_RULES = [
    (re.compile(r"writ|draft|copy|blog|essay|grant|grammar|edit", re.I), "writing"),
    (re.compile(r"research|citation|search|perplex|source-backed|literature", re.I), "research"),
    (re.compile(r"cod|develop|ide\b|github|replit|cursor|programming|frontend", re.I), "coding"),
    (re.compile(r"design|image|midjourney|firefly|leonardo|canva|graphic|visual", re.I), "design"),
    (re.compile(r"video|runway|heygen|synthesia|avatar|clip", re.I), "video"),
    (re.compile(r"audio|voice|speech|eleven|tts|podcast|dubb", re.I), "audio"),
    (re.compile(r"meeting|transcri|otter|fathom|fireflies", re.I), "meetings"),
    (re.compile(r"market|campaign|social|gtm|brand voice", re.I), "marketing"),
    (re.compile(r"automat|zapier|make\b|n8n|agent|workflow|scrap", re.I), "automation"),
    (re.compile(r"email|inbox|slack|notion|productiv|gmail", re.I), "email"),
    (re.compile(r"present|slide|gamma|deck", re.I), "presentations"),
    (re.compile(r"spread|sheet|data|rows|airtable|excel", re.I), "data"),
    (re.compile(r"local|self-host|ollama|openclaw|hermes|lm studio|open webui", re.I), "local"),
]

CURATED_USE_CASES = {
    "chatgpt": ["writing", "research", "coding"],
    "claude": ["writing", "research", "coding"],
    "gemini": ["writing", "research", "email"],
    "grok": ["writing", "coding", "research"],
    "perplexity": ["research"],
    "you-com": ["research"],
    "notebooklm": ["research"],
    "grammarly": ["writing"],
    "jasper": ["marketing", "writing"],
    "copy-ai": ["marketing", "writing"],
    "cursor": ["coding"],
    "github-copilot": ["coding"],
    "replit-ai": ["coding"],
    "v0": ["coding"],
    "bolt-new": ["coding"],
    "lovable": ["coding"],
    "canva-ai": ["design", "marketing", "presentations"],
    "midjourney": ["design"],
    "adobe-firefly": ["design"],
    "leonardo-ai": ["design"],
    "ideogram": ["design", "marketing"],
    "gamma": ["presentations"],
    "htmlslides": ["presentations"],
    "descript": ["audio", "video"],
    "elevenlabs": ["audio"],
    "speechify": ["audio"],
    "suno": ["audio"],
    "udio": ["audio"],
    "runway": ["video"],
    "heygen": ["video"],
    "synthesia": ["video"],
    "allvideoai": ["video"],
    "luma-ai": ["video"],
    "pika": ["video"],
    "fathom": ["meetings"],
    "fireflies": ["meetings"],
    "otter-ai": ["meetings"],
    "make": ["automation"],
    "zapier-ai": ["automation"],
    "n8n": ["automation"],
    "browse-ai": ["automation"],
    "airtable-ai": ["data", "automation"],
    "rows": ["data"],
    "shortwave": ["email"],
    "notion-ai": ["email", "writing"],
    "slack-ai": ["email"],
    "microsoft-copilot": ["email", "writing", "meetings"],
    "ollama": ["local"],
    "lm-studio": ["local"],
    "open-webui": ["local"],
    "openclaw": ["local", "automation"],
    "hermes-agent": ["local", "automation"],
    "typingmind": ["local", "writing"],
    "catch-ai": ["email", "meetings", "automation"],
}


def load_rules(path: Path | None = None) -> dict[str, Any]:
    return json.loads((path or RULES_PATH).read_text())


def use_case_ids(rules: dict[str, Any] | None = None) -> list[str]:
    rules = rules or load_rules()
    return [item["id"] for item in rules["use_cases"]]


def use_case_label(use_case_id: str, rules: dict[str, Any] | None = None) -> str:
    rules = rules or load_rules()
    for item in rules["use_cases"]:
        if item["id"] == use_case_id:
            return item["label"]
    return use_case_id


def sanitize_custom_name(name: str, rules: dict[str, Any] | None = None) -> str:
    rules = rules or load_rules()
    cleaned = re.sub(r"<[^>]*>", "", str(name or ""))
    cleaned = NAME_SANITIZE_RE.sub("", cleaned).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[: rules["max_custom_name"]]


def custom_slug(name: str) -> str:
    stem = re.sub(r"[^a-z0-9]+", "-", sanitize_custom_name(name).lower()).strip("-")
    return f"c:{stem or 'custom'}"[:50]


def is_valid_slug(slug: str) -> bool:
    text = str(slug or "")
    return bool(DIR_SLUG_RE.fullmatch(text) or CUSTOM_SLUG_RE.fullmatch(text))


def _finite_amount(value: Any, maximum: float) -> float | None:
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number != number or number < 0 or number > maximum:
        return None
    return round(number, 2)


def monthly_spend(tool: dict[str, Any], rules: dict[str, Any] | None = None) -> float | None:
    """Return known monthly USD or None when spend is unknown.

    Free is $0 only when the user selected the free kind. Directory
    labels such as "Free + paid" never become inferred spend.
    """
    rules = rules or load_rules()
    kind = str(tool.get("spend_kind") or "unknown")
    amount = _finite_amount(tool.get("amount"), rules["max_amount"])
    seats = tool.get("seats")
    try:
        seat_count = int(seats)
    except (TypeError, ValueError):
        seat_count = 1
    seat_count = max(1, min(seat_count, rules["max_seats"]))

    if kind == "free":
        return 0.0
    if kind == "unknown":
        return None
    if kind == "annual":
        return None if amount is None else round(amount / 12.0, 2)
    if kind == "seats":
        return None if amount is None else round(amount * seat_count, 2)
    if kind in ("monthly", "custom", "promo", "usage"):
        return amount
    return None


def known_spend_tools(tools: list[dict[str, Any]], rules: dict[str, Any] | None = None) -> list[tuple[dict[str, Any], float]]:
    known = []
    for tool in tools:
        value = monthly_spend(tool, rules)
        if value is not None:
            known.append((tool, value))
    return known


def current_monthly_cost(tools: list[dict[str, Any]], rules: dict[str, Any] | None = None) -> dict[str, Any]:
    known = known_spend_tools(tools, rules)
    unknown = [tool for tool in tools if monthly_spend(tool, rules) is None]
    return {
        "monthly": round(sum(value for _, value in known), 2),
        "known_count": len(known),
        "unknown_count": len(unknown),
        "unknown_names": [tool.get("name") or tool.get("slug") for tool in unknown],
    }


def normalize_use_cases(values: Any, rules: dict[str, Any] | None = None) -> list[str]:
    rules = rules or load_rules()
    allowed = set(use_case_ids(rules))
    out: list[str] = []
    for item in values or []:
        key = str(item).strip()
        if key in allowed and key not in out:
            out.append(key)
        if len(out) >= rules["max_use_cases"]:
            break
    return out


def shared_use_cases(a: dict[str, Any], b: dict[str, Any], rules: dict[str, Any] | None = None) -> list[str]:
    left = set(normalize_use_cases(a.get("use_cases"), rules))
    right = set(normalize_use_cases(b.get("use_cases"), rules))
    return sorted(left & right)


def overlap_pairs(tools: list[dict[str, Any]], rules: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    pairs = []
    for i, left in enumerate(tools):
        for right in tools[i + 1 :]:
            shared = shared_use_cases(left, right, rules)
            if shared:
                uncertain = (not left.get("capabilities_known", True)) or (not right.get("capabilities_known", True))
                pairs.append({
                    "a": left.get("slug"),
                    "b": right.get("slug"),
                    "a_name": left.get("name") or left.get("slug"),
                    "b_name": right.get("name") or right.get("slug"),
                    "shared": shared,
                    "uncertain": uncertain,
                })
    return pairs


def overlap_clusters(tools: list[dict[str, Any]], rules: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    pairs = overlap_pairs(tools, rules)
    parent = {tool.get("slug"): tool.get("slug") for tool in tools}

    def find(slug: str) -> str:
        while parent[slug] != slug:
            parent[slug] = parent[parent[slug]]
            slug = parent[slug]
        return slug

    for pair in pairs:
        ra, rb = find(pair["a"]), find(pair["b"])
        if ra != rb:
            parent[rb] = ra

    grouped: dict[str, list[dict[str, Any]]] = {}
    for tool in tools:
        grouped.setdefault(find(tool["slug"]), []).append(tool)

    clusters = []
    for members in grouped.values():
        if len(members) < 2:
            continue
        shared: set[str] = set()
        uncertain = any(not member.get("capabilities_known", True) for member in members)
        for i, left in enumerate(members):
            for right in members[i + 1 :]:
                shared.update(shared_use_cases(left, right, rules))
        clusters.append({
            "slugs": [member["slug"] for member in members],
            "names": [member.get("name") or member["slug"] for member in members],
            "shared": sorted(shared),
            "uncertain": uncertain,
        })
    clusters.sort(key=lambda item: (-len(item["slugs"]), item["slugs"]))
    return clusters


def _catalog_gap(tool: dict[str, Any]) -> bool:
    if str(tool.get("slug", "")).startswith("c:"):
        return True
    if tool.get("capabilities_known") is False:
        return True
    if tool.get("price_confidence") in (None, "missing"):
        return True
    return False


def recommend_tool(tool: dict[str, Any], tools: list[dict[str, Any]], rules: dict[str, Any] | None = None) -> dict[str, Any]:
    """Keep / Cut / Replace / Review / Trial first. Never uses rating or category alone."""
    rules = rules or load_rules()
    unique = bool(tool.get("unique"))
    weekly = bool(tool.get("weekly"))
    spend = monthly_spend(tool, rules)
    partners = []
    for other in tools:
        if other.get("slug") == tool.get("slug"):
            continue
        shared = shared_use_cases(tool, other, rules)
        if shared:
            partners.append((other, shared))
    partners.sort(key=lambda item: (-len(item[1]), not item[0].get("weekly"), item[0].get("slug") or ""))
    top = partners[0] if partners else None
    gap = _catalog_gap(tool)

    if unique:
        return {
            "action": "Keep",
            "why": "You marked a unique must-keep workflow that the rest of this stack does not replace.",
        }
    if not weekly:
        if spend is not None and spend > 0:
            if top:
                names = top[0].get("name") or top[0].get("slug")
                return {
                    "action": "Cut",
                    "why": f"Not used weekly, overlaps with {names} on {', '.join(use_case_label(x, rules) for x in top[1])}, and has entered paid spend with no unique workflow.",
                }
            return {
                "action": "Cut",
                "why": "Not used weekly and has entered paid spend with no unique must-keep workflow.",
            }
        if spend == 0:
            return {
                "action": "Cut",
                "why": "Not used weekly, marked free by you, and has no unique must-keep workflow.",
            }
        return {
            "action": "Review",
            "why": "Not used weekly, but spend is unknown — confirm the bill before canceling.",
        }

    if top:
        other, shared = top
        other_name = other.get("name") or other.get("slug")
        labels = ", ".join(use_case_label(item, rules) for item in shared)
        weekly_partner = any(item[0].get("weekly") for item in partners)
        if len(shared) >= 2 and weekly_partner:
            return {
                "action": "Replace",
                "why": f"Shares {len(shared)} use cases ({labels}) with {other_name}, which is also used weekly. Decide which tool should own that job.",
            }
        return {
            "action": "Trial first",
            "why": f"Possible overlap with {other_name} on {labels}. Run the same weekly task in both before paying for both.",
        }

    if gap:
        return {
            "action": "Review",
            "why": "Official price or capability data is missing, so this stays a review — nothing is invented.",
        }
    return {
        "action": "Keep",
        "why": "Used weekly and does not share a normalized use case with another selected tool.",
    }


def conservative_savings(tools: list[dict[str, Any]], recs: list[dict[str, Any]], rules: dict[str, Any] | None = None) -> dict[str, Any]:
    """Dollar savings only from Cut tools with user-entered known spend."""
    by_slug = {tool.get("slug"): tool for tool in tools}
    monthly = 0.0
    counted = []
    for rec in recs:
        if rec.get("action") != "Cut":
            continue
        tool = by_slug.get(rec.get("slug"))
        if not tool:
            continue
        spend = monthly_spend(tool, rules)
        if spend and spend > 0:
            monthly += spend
            counted.append(tool.get("name") or tool.get("slug"))
    monthly = round(monthly, 2)
    return {
        "monthly": monthly,
        "annual": round(monthly * 12, 2),
        "from_tools": counted,
        "note": "Savings only count Cut tools with user-entered known spend. Unknown, usage-without-amount, and Replace tools are not guessed.",
    }


def stack_efficiency_score(tools: list[dict[str, Any]], rules: dict[str, Any] | None = None) -> dict[str, Any]:
    """Personal diagnostic score. Not financial performance and not a peer ranking."""
    rules = rules or load_rules()
    cfg = rules["score"]
    factors: list[dict[str, Any]] = []
    total = cfg["start"]
    factors.append({"id": "base", "label": "Starting score", "points": cfg["start"]})

    unused_paid = 0
    unknown = 0
    free_count = 0
    known_count = 0
    for tool in tools:
        spend = monthly_spend(tool, rules)
        if spend is None:
            unknown += 1
        else:
            known_count += 1
            if spend > 0 and not tool.get("weekly") and not tool.get("unique"):
                unused_paid += 1
        if tool.get("spend_kind") == "free":
            free_count += 1

    if unused_paid:
        points = cfg["unused_paid"] * unused_paid
        total += points
        factors.append({
            "id": "unused_paid",
            "label": f"{unused_paid} unused paid tool{'s' if unused_paid != 1 else ''} (not weekly, no unique workflow, known spend > $0)",
            "points": points,
        })

    pairs = overlap_pairs(tools, rules)
    if pairs:
        raw = cfg["overlap_pair"] * len(pairs)
        points = max(raw, cfg["overlap_pair_cap"])
        total += points
        factors.append({
            "id": "overlap_pair",
            "label": f"{len(pairs)} overlapping pair{'s' if len(pairs) != 1 else ''} by shared use case",
            "points": points,
        })

    if unknown:
        points = cfg["unknown_spend"] * unknown
        total += points
        factors.append({
            "id": "unknown_spend",
            "label": f"{unknown} tool{'s' if unknown != 1 else ''} with unknown spend",
            "points": points,
        })

    extra = max(0, len(tools) - cfg["stack_size_over"])
    if extra:
        points = max(cfg["stack_size_each"] * extra, cfg["stack_size_cap"])
        total += points
        factors.append({
            "id": "stack_size",
            "label": f"{len(tools)} tools (penalty starts after {cfg['stack_size_over']})",
            "points": points,
        })

    unowned = False
    coverage: dict[str, list[dict[str, Any]]] = {}
    for tool in tools:
        for use_case in normalize_use_cases(tool.get("use_cases"), rules):
            coverage.setdefault(use_case, []).append(tool)
    for holders in coverage.values():
        if len(holders) >= 2 and not any(item.get("unique") for item in holders):
            unowned = True
            break
    if unowned:
        total += cfg["unowned_overlap"]
        factors.append({
            "id": "unowned_overlap",
            "label": "A shared use case has no unique-owner flag",
            "points": cfg["unowned_overlap"],
        })

    weekly_unique = 0
    for use_case, holders in coverage.items():
        weekly_holders = [item for item in holders if item.get("weekly")]
        if len(weekly_holders) == 1:
            weekly_unique += 1
    if weekly_unique:
        points = min(cfg["weekly_unique_each"] * weekly_unique, cfg["weekly_unique_cap"])
        total += points
        factors.append({
            "id": "weekly_unique",
            "label": f"{weekly_unique} use case{'s' if weekly_unique != 1 else ''} covered by exactly one weekly tool",
            "points": points,
        })

    if tools and free_count * 2 >= len(tools):
        total += cfg["free_first"]
        factors.append({
            "id": "free_first",
            "label": "At least half of the stack is user-declared free",
            "points": cfg["free_first"],
        })

    if tools and known_count == len(tools):
        total += cfg["spend_complete"]
        factors.append({
            "id": "spend_complete",
            "label": "Every tool has known spend (including free = $0)",
            "points": cfg["spend_complete"],
        })

    clamped = max(0, min(100, total))
    if clamped != total:
        factors.append({"id": "clamp", "label": "Clamped to 0–100", "points": clamped - total})
    return {
        "score": int(round(clamped)),
        "raw": total,
        "factors": factors,
        "disclaimer": "This is a personal Stack Efficiency Score from your current inputs. It is not a financial-performance rating, ROI claim, or peer ranking.",
    }


def personal_badges(tools: list[dict[str, Any]], score: dict[str, Any], rules: dict[str, Any] | None = None) -> list[dict[str, str]]:
    """Personal badges only. No community totals or rankings."""
    rules = rules or load_rules()
    unused_paid = any(
        (monthly_spend(tool, rules) or 0) > 0 and not tool.get("weekly") and not tool.get("unique")
        for tool in tools
    )
    pairs = overlap_pairs(tools, rules)
    unique_owned = True
    coverage: dict[str, list[dict[str, Any]]] = {}
    for tool in tools:
        for use_case in normalize_use_cases(tool.get("use_cases"), rules):
            coverage.setdefault(use_case, []).append(tool)
    for holders in coverage.values():
        if len(holders) >= 2 and not any(item.get("unique") for item in holders):
            unique_owned = False
            break
    free_count = sum(1 for tool in tools if tool.get("spend_kind") == "free")
    known_count = sum(1 for tool in tools if monthly_spend(tool, rules) is not None)
    badges = []
    if tools and len(tools) <= 4 and not unused_paid and score["score"] >= 70:
        badges.append({"id": "lean", "label": "Lean Stack", "why": "Four or fewer tools, no unused paid seats, score 70+."})
    if tools and (not pairs or unique_owned):
        badges.append({"id": "overlap", "label": "Overlap Resolver", "why": "No unresolved overlapping use cases."})
    if tools and (free_count == len(tools) or (free_count >= 1 and known_count == len(tools) and all((monthly_spend(t, rules) or 0) == 0 for t in tools))):
        badges.append({"id": "free", "label": "Free-First", "why": "Every selected tool is user-declared free or $0 entered spend."})
    ready = True
    if not tools or known_count != len(tools):
        ready = False
    for tool in tools:
        if not (tool.get("weekly") or tool.get("unique")):
            ready = False
            break
    if ready:
        badges.append({"id": "renewal", "label": "Renewal Ready", "why": "Spend is known and every tool is weekly or uniquely required."})
    return badges


def sanitize_tool_input(raw: dict[str, Any], catalog: dict[str, Any] | None = None, rules: dict[str, Any] | None = None) -> dict[str, Any] | None:
    rules = rules or load_rules()
    slug = str(raw.get("slug") or "")
    if not is_valid_slug(slug):
        return None
    record = (catalog or {}).get(slug, {})
    name = sanitize_custom_name(raw.get("name") or record.get("name") or slug, rules)
    if not name:
        return None
    kind = str(raw.get("spend_kind") or "unknown")
    if kind not in rules["spend_kinds"]:
        kind = "unknown"
    amount = _finite_amount(raw.get("amount"), rules["max_amount"])
    try:
        seats = int(raw.get("seats") or 1)
    except (TypeError, ValueError):
        seats = 1
    seats = max(1, min(seats, rules["max_seats"]))
    return {
        "slug": slug,
        "name": name,
        "spend_kind": kind,
        "amount": amount,
        "seats": seats,
        "weekly": bool(raw.get("weekly")),
        "unique": bool(raw.get("unique")),
        "use_cases": normalize_use_cases(raw.get("use_cases"), rules),
        "capabilities_known": bool(record.get("capabilities_known", slug.startswith("c:") is False and record.get("suggested_use_cases"))),
        "price_confidence": record.get("price_confidence") or ("missing" if slug.startswith("c:") or not record else record.get("price_confidence", "official_summary")),
        "affiliate": bool(record.get("affiliate")),
        "sponsored": bool(record.get("sponsored")),
        "rating": record.get("rating"),
        "category": record.get("category"),
    }


def evaluate(tools: list[dict[str, Any]], rules: dict[str, Any] | None = None) -> dict[str, Any]:
    rules = rules or load_rules()
    cleaned = [tool for tool in tools if tool]
    recs = []
    for tool in cleaned:
        rec = recommend_tool(tool, cleaned, rules)
        recs.append({"slug": tool.get("slug"), "name": tool.get("name") or tool.get("slug"), **rec})
    cost = current_monthly_cost(cleaned, rules)
    score = stack_efficiency_score(cleaned, rules)
    return {
        "cost": cost,
        "savings": conservative_savings(cleaned, recs, rules),
        "score": score,
        "badges": personal_badges(cleaned, score, rules),
        "clusters": overlap_clusters(cleaned, rules),
        "recommendations": recs,
    }


def encode_fragment(tools: list[dict[str, Any]], include_spend: bool = False, rules: dict[str, Any] | None = None) -> str:
    rules = rules or load_rules()
    payload = {
        "v": 1,
        "p": 1 if include_spend else 0,
        "t": [],
    }
    for tool in tools[: rules["max_tools"]]:
        row: dict[str, Any] = {
            "s": tool.get("slug"),
            "k": tool.get("spend_kind") or "unknown",
            "w": 1 if tool.get("weekly") else 0,
            "u": 1 if tool.get("unique") else 0,
            "c": normalize_use_cases(tool.get("use_cases"), rules),
        }
        if str(tool.get("slug", "")).startswith("c:"):
            row["n"] = sanitize_custom_name(tool.get("name") or "", rules)
        if include_spend:
            if tool.get("amount") is not None:
                row["a"] = tool.get("amount")
            if tool.get("spend_kind") == "seats":
                row["q"] = tool.get("seats") or 1
        payload["t"].append(row)
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    token = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    fragment = rules["fragment_prefix"] + token
    if len(fragment) > rules["max_fragment_chars"]:
        raise ValueError("share fragment exceeds length limit")
    return fragment


def decode_fragment(fragment: str, catalog: dict[str, Any] | None = None, rules: dict[str, Any] | None = None) -> dict[str, Any]:
    rules = rules or load_rules()
    text = str(fragment or "").strip()
    if text.startswith("#"):
        text = text[1:]
    if not text.startswith(rules["fragment_prefix"]):
        return {"ok": False, "error": "unsupported or missing fragment", "tools": [], "include_spend": False}
    if len(text) > rules["max_fragment_chars"]:
        return {"ok": False, "error": "fragment too long", "tools": [], "include_spend": False}
    token = text[len(rules["fragment_prefix"]) :]
    pad = "=" * (-len(token) % 4)
    try:
        raw = base64.urlsafe_b64decode(token + pad)
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        return {"ok": False, "error": "malformed fragment", "tools": [], "include_spend": False}
    if not isinstance(payload, dict) or payload.get("v") != 1 or not isinstance(payload.get("t"), list):
        return {"ok": False, "error": "malformed fragment", "tools": [], "include_spend": False}
    include_spend = bool(payload.get("p"))
    tools = []
    for row in payload["t"][: rules["max_tools"]]:
        if not isinstance(row, dict):
            continue
        slug = str(row.get("s") or "")
        raw_tool = {
            "slug": slug,
            "name": row.get("n") or slug,
            "spend_kind": row.get("k") or "unknown",
            "amount": row.get("a") if include_spend else None,
            "seats": row.get("q") if include_spend else 1,
            "weekly": bool(row.get("w")),
            "unique": bool(row.get("u")),
            "use_cases": row.get("c") or [],
        }
        if not include_spend:
            raw_tool["spend_kind"] = "unknown" if raw_tool["spend_kind"] != "free" else "free"
            raw_tool["amount"] = None
        cleaned = sanitize_tool_input(raw_tool, catalog, rules)
        if cleaned:
            tools.append(cleaned)
    return {"ok": True, "error": None, "tools": tools, "include_spend": include_spend}


def map_use_cases(tool: dict[str, Any], rules: dict[str, Any] | None = None) -> tuple[list[str], str]:
    rules = rules or load_rules()
    slug = tool.get("slug")
    if slug in CURATED_USE_CASES:
        return CURATED_USE_CASES[slug][: rules["max_use_cases"]], "curated"
    text = " ".join([
        str(tool.get("name") or ""),
        str(tool.get("category") or ""),
        str(tool.get("best_for") or ""),
        str(tool.get("summary") or ""),
        " ".join(tool.get("use_cases") or []),
        " ".join(tool.get("key_features") or []),
    ])
    found: list[str] = []
    for pattern, use_case in KEYWORD_RULES:
        if pattern.search(text) and use_case not in found:
            found.append(use_case)
        if len(found) >= rules["max_use_cases"]:
            break
    if found:
        return found, "keyword"
    hints = [item for item in CATEGORY_HINTS.get(str(tool.get("category") or ""), []) if item in use_case_ids(rules)]
    if hints:
        return hints[: rules["max_use_cases"]], "category_hint"
    return [], "missing"


def build_catalog(root: Path | None = None, today: str | None = None) -> dict[str, Any]:
    root = root or ROOT
    rules = load_rules(root / "data" / "stack_audit_rules.json")
    tools = json.loads((root / "data" / "tools.json").read_text())
    sources = json.loads((root / "data" / "tool_sources.json").read_text())
    source_by_slug = {item.get("slug"): item for item in sources.get("tools", [])}
    affiliates = json.loads((root / "data" / "affiliate_programs.json").read_text())
    affiliate_by_slug = {item.get("tool_slug"): item for item in affiliates.get("affiliate_programs", [])}
    sponsors = json.loads((root / "data" / "sponsors.json").read_text())
    sponsored_slugs = {
        item.get("tool_slug")
        for item in sponsors.get("sponsors", [])
        if item.get("active") and item.get("tool_slug")
    }

    records = []
    for tool in tools:
        slug = tool["slug"]
        source = source_by_slug.get(slug, {})
        suggested, confidence = map_use_cases(tool, rules)
        summary = source.get("pricing_summary") or ""
        records.append({
            "slug": slug,
            "name": tool.get("name") or slug,
            "category": tool.get("category") or "",
            "official_url": tool.get("official") or source.get("pricing_url") or "",
            "review_url": f"/tools/{slug}/",
            "price_label": tool.get("price") or "",
            "pricing_summary": summary,
            "pricing_url": source.get("pricing_url") or "",
            "pricing_checked_date": source.get("pricing_checked_date") or "",
            "price_confidence": "official_summary" if summary else "missing",
            "numeric_list_price_usd": None,
            "promotion_mentioned": bool(summary and PROMO_RE.search(summary)),
            "suggested_use_cases": suggested,
            "capability_confidence": confidence,
            "capabilities_known": confidence in ("curated", "keyword"),
            "affiliate_status": (affiliate_by_slug.get(slug) or {}).get("application_status"),
            "affiliate": (affiliate_by_slug.get(slug) or {}).get("application_status") == "approved",
            "sponsored": slug in sponsored_slugs,
        })

    return {
        "generated_at": today or date.today().isoformat(),
        "policy": (
            "Normalized Stack Audit contract generated from data/tools.json and "
            "data/tool_sources.json. Numeric spend is never invented. Missing "
            "price or capability yields Review. Affiliate and sponsor flags are "
            "disclosure-only and never change score, inclusion, or recommendations. "
            "The viral.js $20/$35 heuristic is not used."
        ),
        "rules": rules,
        "tools": records,
    }


def catalog_index(catalog: dict[str, Any]) -> dict[str, Any]:
    return {item["slug"]: item for item in catalog.get("tools", [])}
