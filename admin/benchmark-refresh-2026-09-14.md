# Benchmark evidence refresh — 2026-09-14

Internal operator record for the weekly benchmark refresh of `data/benchmarks.json`.
Every figure below was read off the source registry on 2026-09-14 and is quoted verbatim in
the evidence block at the end of this file. No number was inferred or carried over.

## What changed in the snapshot

The Arena Text leaderboard served a new snapshot dated 13 Sep 2026, carrying 8,146,274 votes
across 402 models.[1] All six tracked rows keep the same exact model version as the previous
snapshot; three ratings moved by a single point and three were unchanged. Ranks are down 2–3
places across the board and every vote count was revised downward, which is what Arena
re-filtering battles looks like rather than a product regression.[1]

| Tool | Exact model | Rank | Rating ± CI | Votes | Rating moved |
|---|---|---|---|---|---|
| Grok | grok-4.1 | #53 → #54 | 1459±3 (unchanged) | 66,382 → 66,340 | no |
| DeepSeek | deepseek-v4-pro | #55 → #57 | 1458±4 → 1457±4 | 54,225 → 54,130 | yes, 1 point |
| Claude | claude-sonnet-4-5-20250929 | #62 → #65 | 1455±3 (unchanged) | 79,668 → 79,628 | no |
| Gemini | gemini-2.5-pro | #75 → #77 | 1446±2 → 1445±2 | 122,612 → 122,554 | yes, 1 point |
| ChatGPT | chatgpt-4o-latest-20250326 | #78 → #80 | 1443±3 (unchanged) | 80,696 → 80,677 | no |
| Mistral Le Chat | mistral-medium-3.5 | #103 → #106 | 1427±7 → 1426±7 | 11,017 → 10,996 | yes, 1 point |

Each moved rating shifted by one point against a published confidence interval of ±2 to ±7, so
no row supports a buying conclusion in either direction.[1] Arena-Rank computes these ratings with
Bradley-Terry reweighting for models that have fewer battles and a closed-form confidence interval
calculation,[2] which is why a one-point move inside a ±2 interval is not a finding. The leaderboard also lists newer
versions of several of these model families at higher ranks (grok-4.20-beta at #39,
claude-fable-5 at #1, gemini-3.1-pro-preview at #15, gpt-5.6-sol-xhigh at #18,
deepseek-v4-pro-high at #50), which is exactly why a product name must never be substituted for
a model version.[1]

`snapshot_date` moved 2026-09-02 → 2026-09-13 and `reviewed_date` 2026-09-07 → 2026-09-14.
`previous_snapshot_date` is now 2026-09-02.

## Rows deliberately left unchanged

**Coding-agent row (Cursor).** The maintainer submission record still reports exactly the stored
values: Cursor CLI 2026.07.08-0c04a8a with cursor/grok-4.5 at high effort, 79.33% accuracy,
445 trials, 8.99% reward-hack disqualifications, dated 2026-07-09.[10] The score is accurate but
older than it looks, so the row's note now states why: the Terminal-Bench 2.1 board is closed to
new submissions,[6] and the live Terminal-Bench 4.0 board carries no Cursor configuration at all,
so no current Cursor reading exists to move the row to.

**No SWE-bench row.** The Verified page confirms the 500-instance human-validated subset and warns
that mini-SWE-agent 1.x and 2.x results are not comparable to each other,[3] but that URL served no
dated public score table on this check, so nothing was added.

**No Artificial Analysis rows.** The intelligence, image, video and TTS methodology pages are all
live, and each documents the separation rule that governs its own pool: intelligence, quality,
performance and price are benchmarked on models and inference endpoints rather than products,[5]
image generation keeps a separate image-editing methodology,[7] video splits text-to-video from
image-to-video,[8] and text-to-speech splits controlled voices from provider voices.[9] None of
them served a dated per-model score table on this check, so no Artificial Analysis row was changed
and none was invented to fill the gap.

**LiveBench.** The repository is live, but its public changelog stops at 2026-01-08 and its README
still displays top models as of 30 September 2024.[4] livebench.ai renders client-side only, so no
dated ranking could be read without a browser. No LiveBench row was added or changed.

## Stale, blocked and ambiguous sources

- **Source 6 is now blocked by supersession.** The registered URL 308-redirects to
  `https://www.tbench.ai/?version=2.1`, and every route on that host — including the explicit
  `?version=2.1` and `?version=2-1-0` variants — served the Terminal-Bench 4.0 board, titled
  "TERMINAL-BENCH 4.0" with leaderboard slug `4-0-0`.[6] No 2.1 rows were readable from it, and no
  archived 2.1 board was found on the site. The registry entry now says "frozen" in its name and
  carries that finding in its caveat.
- **A new registry entry was added to cover the gap.** Harbor Hub's Terminal-Bench 2.1 dataset page
  is live and reports "Displaying 89 of 89 tasks" at "Version 2.1 of Terminal-Bench",[11] which
  pins the task set behind the Cursor score. It publishes tasks, not scores.
- **Terminal-Bench 2.1 and 4.0 must never be compared.** They are different harness versions with
  different task sets and different published leaders; the 4.0 board's top row is Codex with GPT-6
  Astra at 58.18% over 330 trials,[6] which has nothing to do with a 2.1 percentage. The site
  renders the 2.1 score only with its agent, model, effort, trial count and integrity metadata
  attached, as it already did.
- **No product-level transfer anywhere.** Every updated row links a model version to a product
  family only as "representative public listing" context, and each row's note says the listing is
  not necessarily that product's current default.

## Validation and deployment

- `python3 scripts/daily_content_update.py` regenerated the site: 76 tools, sitemap refreshed with
  724 URLs, benchmark hub rewritten.
- `python3 scripts/validate_site.py` → `Validation passed` / 76 tools / 736 HTML pages.
- Regeneration touched `data/benchmarks.json`, `benchmarks/index.html`,
  `downloads/arena-text-snapshot.csv`, 12 comparison pages, 9 tool reviews and 2 article/stack pages.
- Committed and pushed as `Refresh benchmark evidence: 2026-09-14`.

No credentials or secrets appear in this record or in the committed files.

## Sources

[1] https://arena.ai/leaderboard/text — Arena Text Leaderboard
    > "Sep 13, 2026"
    > "54 45 68 grok-4.1 SpaceXAI · Proprietary 1459 ±3 66,340"
    > "57 48 71 deepseek-v4-pro DeepSeek · MIT 1457 ±4 54,130"
    > "65 50 73 Anthropic claude-sonnet-4-5-20250929 Anthropic · Proprietary 1455 ±3 79,628"
    > "77 67 87 gemini-2.5-pro Google · Proprietary 1445 ±2 122,554"
    > "80 70 90 chatgpt-4o-latest-20250326 OpenAI · Proprietary 1443 ±3 80,677"
    > "106 89 129 mistral-medium-3.5 Mistral · Modified MIT 1426 ±7 10,996"
    > "Sep 13, 2026 8,146,274 votes 402 models"
[2] https://arena.ai/blog/arena-rank — Arena-Rank methodology
    > "reweighting feature to ensure fair treatment of models for which we have fewer battles"
    > "closed-form confidence interval calculation"
[3] https://www.swebench.com/verified.html — SWE-bench Verified
    > "A human-validated subset of 500 SWE-bench instances"
    > "Results of release 1.x and 2.x are not necessarily comparable to each other"
[4] https://github.com/LiveBench/LiveBench — LiveBench
    > "Top models as of 30th September 2024"
    > "Added a new math task (Integrals with Game) and a new data analysis task (consecutive events)"
[5] https://artificialanalysis.ai/methodology — Artificial Analysis methodology
[6] https://www.tbench.ai/leaderboard/terminal-bench/2.1 — Terminal-Bench 2.1 leaderboard
    > "Community submissions are currently closed for Terminal-Bench 2.1"
    > "TERMINAL-BENCH 4.0 A benchmark to measure and evolve with the frontier of agent work"
    > "Resolution rate of Terminal-Bench 4.0 tasks."
    > ""title":"Terminal-Bench 4.0","description":"The official leaderboard for Terminal-Bench 4.0.""
[7] https://artificialanalysis.ai/image/methodology — Artificial Analysis Image methodology
[8] https://artificialanalysis.ai/video/methodology — Artificial Analysis Video methodology
[9] https://artificialanalysis.ai/text-to-speech/methodology — Artificial Analysis TTS methodology
[10] https://raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/main/leaderboard/submissions/2026-07-09-cursor-grok-4-5-none-cursor-cli.json — Terminal-Bench: Cursor CLI + Grok 4.5 submission
    > ""display_accuracy": "**79.3%** \u00b1 1.5%","
    > ""accuracy": 79.33, "accuracy_stderr": 1.46,"
    > ""n_trials": 445, "pass_at_2": 0.8888,"
    > ""reward_hacks": 8.99, "display_reward_hacks": {"
    > ""agent": "cursor-cli", "agent_version": "2026.07.08-0c04a8a", "model_name": "cursor/grok-4.5","
    > ""date": "2026-07-09", "display_date": "Jul 9, 2026","
[11] https://hub.harborframework.com/datasets/terminal-bench/terminal-bench-2-1/latest — Harbor Hub - Terminal-Bench 2.1 dataset
    > "Displaying 89 of 89 tasks"
    > "Version 2.1 of Terminal-Bench"
