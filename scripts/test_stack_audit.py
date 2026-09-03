#!/usr/bin/env python3
"""Deterministic tests for the Stack Audit MVP engine."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stack_audit_lib import (  # noqa: E402
    build_catalog,
    conservative_savings,
    current_monthly_cost,
    decode_fragment,
    encode_fragment,
    evaluate,
    load_rules,
    monthly_spend,
    overlap_clusters,
    overlap_pairs,
    personal_badges,
    recommend_tool,
    sanitize_custom_name,
    sanitize_tool_input,
    stack_efficiency_score,
)


def tool(**kwargs):
    base = {
        "slug": "chatgpt",
        "name": "ChatGPT",
        "spend_kind": "unknown",
        "amount": None,
        "seats": 1,
        "weekly": False,
        "unique": False,
        "use_cases": ["writing"],
        "capabilities_known": True,
        "price_confidence": "official_summary",
        "affiliate": False,
        "sponsored": False,
    }
    base.update(kwargs)
    return base


class SpendMathTests(unittest.TestCase):
    def test_monthly_uses_entered_amount(self):
        self.assertEqual(monthly_spend(tool(spend_kind="monthly", amount=20)), 20.0)

    def test_annual_divides_by_twelve(self):
        self.assertEqual(monthly_spend(tool(spend_kind="annual", amount=240)), 20.0)

    def test_seats_multiplies(self):
        self.assertEqual(monthly_spend(tool(spend_kind="seats", amount=12, seats=3)), 36.0)

    def test_unknown_stays_unknown(self):
        self.assertIsNone(monthly_spend(tool(spend_kind="unknown", amount=99)))

    def test_free_is_zero_only_when_user_declares_free(self):
        self.assertEqual(monthly_spend(tool(spend_kind="free", amount=20)), 0.0)

    def test_free_plus_paid_label_is_not_inferred(self):
        labeled = tool(spend_kind="unknown", amount=None, price_label="Free + paid")
        self.assertIsNone(monthly_spend(labeled))
        cost = current_monthly_cost([labeled])
        self.assertEqual(cost["monthly"], 0)
        self.assertEqual(cost["unknown_count"], 1)

    def test_custom_amount_is_monthly(self):
        self.assertEqual(monthly_spend(tool(spend_kind="custom", amount=7.5)), 7.5)

    def test_promo_uses_entered_price_not_list_guess(self):
        self.assertEqual(monthly_spend(tool(spend_kind="promo", amount=11)), 11.0)

    def test_usage_without_amount_is_unknown(self):
        self.assertIsNone(monthly_spend(tool(spend_kind="usage", amount=None)))

    def test_usage_with_amount_is_known(self):
        self.assertEqual(monthly_spend(tool(spend_kind="usage", amount=18)), 18.0)

    def test_negative_and_huge_amounts_rejected(self):
        self.assertIsNone(monthly_spend(tool(spend_kind="monthly", amount=-5)))
        self.assertIsNone(monthly_spend(tool(spend_kind="monthly", amount=1_000_001)))

    def test_current_cost_sums_known_only(self):
        tools = [
            tool(slug="a", spend_kind="monthly", amount=20),
            tool(slug="b", spend_kind="unknown"),
            tool(slug="c", spend_kind="free"),
        ]
        cost = current_monthly_cost(tools)
        self.assertEqual(cost["monthly"], 20.0)
        self.assertEqual(cost["unknown_count"], 1)


class OverlapTests(unittest.TestCase):
    def test_overlap_uses_shared_use_cases_not_category(self):
        a = tool(slug="chatgpt", category="General AI Assistant", use_cases=["writing"])
        b = tool(slug="claude", category="General AI Assistant", use_cases=["coding"])
        self.assertEqual(overlap_pairs([a, b]), [])
        b["use_cases"] = ["writing"]
        pairs = overlap_pairs([a, b])
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["shared"], ["writing"])

    def test_cluster_connects_shared_use_cases(self):
        tools = [
            tool(slug="chatgpt", use_cases=["writing", "research"]),
            tool(slug="claude", use_cases=["writing"]),
            tool(slug="perplexity", use_cases=["research"]),
            tool(slug="cursor", use_cases=["coding"]),
        ]
        clusters = overlap_clusters(tools)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(sorted(clusters[0]["slugs"]), ["chatgpt", "claude", "perplexity"])

    def test_missing_capability_marks_uncertainty(self):
        a = tool(slug="chatgpt", use_cases=["writing"], capabilities_known=False)
        b = tool(slug="claude", use_cases=["writing"])
        self.assertTrue(overlap_pairs([a, b])[0]["uncertain"])


class RecommendationTests(unittest.TestCase):
    def test_unique_workflow_keeps(self):
        rec = recommend_tool(tool(unique=True, weekly=False, spend_kind="monthly", amount=20), [tool(unique=True)])
        self.assertEqual(rec["action"], "Keep")

    def test_unused_paid_is_cut(self):
        rec = recommend_tool(tool(weekly=False, unique=False, spend_kind="monthly", amount=20), [tool()])
        self.assertEqual(rec["action"], "Cut")
        self.assertNotIn("rating", rec["why"].lower())
        self.assertNotIn("category", rec["why"].lower())

    def test_never_cut_from_rating_or_category_alone(self):
        rated = tool(weekly=True, unique=False, spend_kind="monthly", amount=20, rating=2.0, category="Writing")
        rec = recommend_tool(rated, [rated])
        self.assertEqual(rec["action"], "Keep")

    def test_unknown_unused_is_review(self):
        rec = recommend_tool(tool(weekly=False, spend_kind="unknown"), [tool()])
        self.assertEqual(rec["action"], "Review")

    def test_strong_weekly_overlap_is_replace(self):
        a = tool(slug="chatgpt", weekly=True, use_cases=["writing", "research"])
        b = tool(slug="claude", name="Claude", weekly=True, use_cases=["writing", "research"])
        self.assertEqual(recommend_tool(a, [a, b])["action"], "Replace")

    def test_weak_overlap_is_trial_first(self):
        a = tool(slug="chatgpt", weekly=True, use_cases=["writing"])
        b = tool(slug="claude", name="Claude", weekly=True, use_cases=["writing"])
        self.assertEqual(recommend_tool(a, [a, b])["action"], "Trial first")

    def test_missing_catalog_data_is_review_when_weekly_and_no_overlap(self):
        custom = tool(slug="c:acme", weekly=True, use_cases=["coding"], capabilities_known=False, price_confidence="missing")
        self.assertEqual(recommend_tool(custom, [custom])["action"], "Review")

    def test_affiliate_does_not_change_recommendation(self):
        plain = tool(slug="chatgpt", weekly=True, use_cases=["coding"], affiliate=False)
        flagged = tool(slug="chatgpt", weekly=True, use_cases=["coding"], affiliate=True, sponsored=True)
        self.assertEqual(recommend_tool(plain, [plain]), recommend_tool(flagged, [flagged]))


class ScoreBoundaryTests(unittest.TestCase):
    def test_perfect_small_free_stack_high_score(self):
        tools = [
            tool(slug="chatgpt", spend_kind="free", weekly=True, unique=True, use_cases=["writing"]),
            tool(slug="perplexity", spend_kind="free", weekly=True, unique=True, use_cases=["research"]),
        ]
        score = stack_efficiency_score(tools)
        self.assertGreaterEqual(score["score"], 90)
        self.assertLessEqual(score["score"], 100)
        ids = {item["id"] for item in score["factors"]}
        self.assertIn("free_first", ids)
        self.assertIn("spend_complete", ids)

    def test_score_clamps_at_zero(self):
        tools = []
        for i in range(16):
            tools.append(tool(
                slug=f"tool-{i}",
                spend_kind="unknown",
                weekly=False,
                unique=False,
                use_cases=["writing", "research"],
            ))
        score = stack_efficiency_score(tools)
        self.assertEqual(score["score"], 0)
        self.assertTrue(any(item["id"] == "clamp" for item in score["factors"]))

    def test_score_clamps_at_hundred(self):
        tools = [tool(slug="chatgpt", spend_kind="free", weekly=True, unique=True, use_cases=["writing"])]
        score = stack_efficiency_score(tools)
        self.assertLessEqual(score["score"], 100)

    def test_affiliate_and_rating_do_not_change_score(self):
        a = [tool(slug="chatgpt", spend_kind="monthly", amount=20, weekly=True, use_cases=["writing"], affiliate=False, rating=5)]
        b = [tool(slug="chatgpt", spend_kind="monthly", amount=20, weekly=True, use_cases=["writing"], affiliate=True, sponsored=True, rating=1)]
        self.assertEqual(stack_efficiency_score(a)["score"], stack_efficiency_score(b)["score"])

    def test_viral_heuristic_not_used(self):
        unknown = tool(spend_kind="unknown", price_label="Free + paid")
        score = stack_efficiency_score([unknown])
        self.assertNotIn(20, [item["points"] for item in score["factors"]])
        self.assertNotIn(35, [item["points"] for item in score["factors"]])
        self.assertIsNone(monthly_spend(unknown))


class SavingsTests(unittest.TestCase):
    def test_savings_only_from_cut_with_known_spend(self):
        tools = [
            tool(slug="a", name="A", spend_kind="monthly", amount=20, weekly=False),
            tool(slug="b", name="B", spend_kind="unknown", weekly=False),
            tool(slug="c", name="C", spend_kind="monthly", amount=15, weekly=True, use_cases=["coding"]),
        ]
        result = evaluate(tools)
        self.assertEqual(result["savings"]["monthly"], 20.0)
        self.assertEqual(result["savings"]["annual"], 240.0)
        self.assertEqual(result["savings"]["from_tools"], ["A"])

    def test_replace_does_not_invent_savings(self):
        a = tool(slug="chatgpt", weekly=True, spend_kind="monthly", amount=20, use_cases=["writing", "research"])
        b = tool(slug="claude", weekly=True, spend_kind="monthly", amount=20, use_cases=["writing", "research"])
        result = evaluate([a, b])
        self.assertEqual(result["savings"]["monthly"], 0)
        self.assertTrue(all(rec["action"] != "Cut" for rec in result["recommendations"]))


class BadgeTests(unittest.TestCase):
    def test_personal_badges_from_current_inputs(self):
        tools = [
            tool(slug="chatgpt", spend_kind="free", weekly=True, unique=True, use_cases=["writing"]),
            tool(slug="perplexity", spend_kind="free", weekly=True, unique=True, use_cases=["research"]),
        ]
        score = stack_efficiency_score(tools)
        badges = {item["id"] for item in personal_badges(tools, score)}
        self.assertIn("lean", badges)
        self.assertIn("overlap", badges)
        self.assertIn("free", badges)
        self.assertIn("renewal", badges)

    def test_no_badges_without_inputs(self):
        score = stack_efficiency_score([])
        self.assertEqual(personal_badges([], score), [])


class ShareAndSanitizeTests(unittest.TestCase):
    def test_private_share_strips_exact_spend(self):
        tools = [tool(slug="chatgpt", spend_kind="monthly", amount=20, weekly=True, use_cases=["writing"])]
        fragment = encode_fragment(tools, include_spend=False)
        decoded = decode_fragment(fragment)
        self.assertTrue(decoded["ok"])
        self.assertFalse(decoded["include_spend"])
        self.assertIsNone(decoded["tools"][0]["amount"])
        self.assertEqual(decoded["tools"][0]["spend_kind"], "unknown")

    def test_opt_in_share_keeps_spend(self):
        tools = [tool(slug="chatgpt", spend_kind="seats", amount=12, seats=2, weekly=True, use_cases=["writing"])]
        fragment = encode_fragment(tools, include_spend=True)
        decoded = decode_fragment(fragment)
        self.assertTrue(decoded["include_spend"])
        self.assertEqual(decoded["tools"][0]["amount"], 12)
        self.assertEqual(decoded["tools"][0]["seats"], 2)
        self.assertEqual(monthly_spend(decoded["tools"][0]), 24.0)

    def test_free_survives_private_share(self):
        tools = [tool(slug="chatgpt", spend_kind="free", weekly=True, use_cases=["writing"])]
        decoded = decode_fragment(encode_fragment(tools, include_spend=False))
        self.assertEqual(decoded["tools"][0]["spend_kind"], "free")
        self.assertEqual(monthly_spend(decoded["tools"][0]), 0.0)

    def test_malformed_fragments(self):
        for fragment in ["", "#nope", "sa1.%%%", "sa1.e30", "#" + ("sa1." + "A" * 2000)]:
            decoded = decode_fragment(fragment)
            self.assertFalse(decoded["ok"], fragment)
            self.assertEqual(decoded["tools"], [])

    def test_custom_name_sanitized(self):
        self.assertEqual(sanitize_custom_name("  My <script> Tool!!  "), "My Tool")
        cleaned = sanitize_tool_input({"slug": "c:my-tool", "name": "Drop; table--", "use_cases": ["writing", "hacking"]})
        self.assertIsNotNone(cleaned)
        self.assertNotIn("<", cleaned["name"])
        self.assertEqual(cleaned["use_cases"], ["writing"])

    def test_invalid_slug_rejected(self):
        self.assertIsNone(sanitize_tool_input({"slug": "../etc/passwd"}))
        self.assertIsNone(sanitize_tool_input({"slug": "c:"}))


class CatalogContractTests(unittest.TestCase):
    def test_catalog_covers_every_directory_tool_without_invented_prices(self):
        catalog = build_catalog(ROOT)
        tools = __import__("json").loads((ROOT / "data" / "tools.json").read_text())
        slugs = {item["slug"] for item in tools}
        catalog_slugs = {item["slug"] for item in catalog["tools"]}
        self.assertEqual(slugs, catalog_slugs)
        for item in catalog["tools"]:
            self.assertIsNone(item["numeric_list_price_usd"])
            self.assertIn(item["price_confidence"], ("official_summary", "missing"))
            self.assertIn(item["capability_confidence"], ("curated", "keyword", "category_hint", "missing"))
            if not item["pricing_summary"]:
                self.assertEqual(item["price_confidence"], "missing")

    def test_rules_file_loaded(self):
        rules = load_rules()
        self.assertEqual(len(rules["use_cases"]), 13)
        self.assertEqual(rules["max_use_cases"], 5)


if __name__ == "__main__":
    unittest.main()
