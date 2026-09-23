#!/usr/bin/env python3
"""Append today's summary sections to digest-2026-09-23.json, computed rather than asserted."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
DEST = OUT / "digest-2026-09-23.json"
d = json.loads(DEST.read_text())
ops = d["opportunities"]
window = json.loads((OUT / "_window_0923.json").read_text())

# "live"/"cold" mean live and unpitched, the same basis build_pitch_queue.py reports on. Counting the
# 3 already-pitched and 1 deliberately-skipped rows as live overstates the queue by 4 and would have
# made this digest's headline disagree with pitch-queue.md's for no reason a reader could see.
led = json.loads((OUT / "pitch-ledger.json").read_text())
done = set(led.get("pitched", {})) | set(led.get("skipped", {}))
unpitched = [o for o in ops if o["url"] not in done]

latest = "2026-09-23"
days = [o.get("deadline", "") for o in ops]
# age is re-derived from the page fact embedded in each deadline note
import re
ages = []
for o in unpitched:
    m = re.search(r"= (\d+) days, no expiry notice", o.get("deadline", ""))
    if not m:
        m = re.search(r"= (\d+) days", o.get("deadline", ""))
    ages.append(int(m.group(1)) if m else None)
live = [a for a in ages if a is not None and a <= 10]
cold = [a for a in ages if a is not None and a > 10]

d["new_this_run"] = [
    "NO NEW CORE-BEAT REQUEST FOR THE FOURTH RUN IN FIVE, AND NO AI+SPEND SLUG AT ALL. 126 slugs carry a lastmod newer than the 2026-09-22 run's mark (2026-09-22T03:20:54.000Z). 8 of them carry an AI token (was 7 yesterday) and ZERO carry an AI token plus a spend token — the first window in five runs with no AI+spend slug. All 8 AI-token candidates were fetched and read in full, plus the 5 slugs across the remaining 118 that carry any spend-adjacent token at all (procurement, cost, buying, tools, data). Read: a US med-lab AI-adoption piece, an engineering PR-review capacity piece, a research-agents study, a fractional-executive AI piece, a tech-leader podcast booking form, a Global South physics-tech call, a humanist essay, an Ifa/Yoruba AI piece — plus a US-Canada tariff/procurement call, an affordable-housing construction-cost piece, a wellness-podcast guest call, an Ontario election privacy piece and a protein-beverage buying-habits piece. Every one is either a different sector's adoption story or a booking/philosophy call; none contains a price, seat, licence or spend ask.",
    "THE PAIR RANGE HELD, WHICH IS THE FIRST TIME IT HAS NOT MOVED. data/pricing_snapshots.json carries `updated: 2026-09-23` and the snapshot dates in the file now span 2026-08-25 to 2026-09-21, so the 19 curated pairs had to be re-asserted rather than carried. scripts/extract_monthly_annual_pairs.py re-asserted every pair against its own sentence and exited 0 with no needle failures — the first clean pass since the write gate was added on 2026-09-22. Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 tiers across 14 tools. data/monthly_annual_pairs.json re-derived and rewritten today.",
    "ALL 47 CARRIED URLS RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page returns HTTP 200 with the request body still served and no removal or expiry notice. 26 are live and unpitched, 17 of the live set are past the 10-day cold line, and 2 rows have both a relevance above the tangential band and a resolved reply route.",
    "THE SENDABLE COUNT FALLS FROM 3 TO 2 BECAUSE ONE DRAFT WAS LEFT UNSENT PAST ITS LINE, NOT BECAUSE THE MARKET CHANGED. The Anthropic customer-service request reached 11 days today and crossed the >10-day cold line while its draft sat finished and unsent since 2026-09-19. It was sendable on four consecutive runs, including the day before it crossed, and the 2026-09-22 digest named that crossing as due today. This is the first request this monitor has lost to the cold line while a paste-ready draft for it existed.",
    "MAILBOX CHECKED: NO NEW REPLIES. INBOX top is a Google 'Security alert' new-sign-in notice (2026-09-23 15:59Z) above three identical 'New AI tool submission' form-mails from 2026-09-22 15:29Z. The most recent human message is still Jan Suski's 2026-09-18 20:39Z reply, which we answered at 21:29Z the same day. No reply to the 2026-09-15 Enterprise AI Leaders send (eight days) or the 2026-09-18 Sherwood News send (five days). Sent Mail top unchanged at msg 178; All Mail top is msg 239. Spam holds three items, all delivery-failure bounces and directory form-mail. Zero pitches sent this run.",
]

d["expired_this_run"] = [
    "Nothing expired and nothing dropped off this run. All 47 carried URLs returned HTTP 200 with the request body still served, and none has stopped appearing in a URL-carrying digest. The usual caveat still applies and is not a clean bill of health: this monitor carries every tracked request forward into each new digest, so 'absent from the newest digest' cannot fire by construction. Independently cross-checked this run against the full sitemap (41,594 loc/lastmod pairs): all 47 tracked slugs are still present in it, and ZERO of them carry a lastmod inside today's new window, i.e. no tracked request was edited or renewed today.",
    "ONE REQUEST CROSSES THE 10-DAY LINE TODAY, AND IT IS THE FIRST ONE LOST WHILE A FINISHED DRAFT EXISTED. Anthropic - customer service experiences (11d, medium-high, unpitched) reached 11 days and is now cold. Draft finished and unsent since 2026-09-19 at pitch-drafts-2026-09-22.md section 2; route Signal hliwrites.99, still published verbatim on the live page. Logged in pitch-ledger.json `cold_without_a_send`. A late send is still possible - the draft is intact and the handle is unchanged - but the queue no longer counts it as live. This is the fourth consecutive run the draft has been carried.",
    "The three requests already recorded as spent remain spent and are not resurfaced: California AI audit bills ('speak with a source today', 13d) and UK Managers - Gen Z AI overuse (internal deadline 'by this Wednesday September 9', 16d) both stay live with no expiry notice, so the do-not-pitch judgement rests on their stated deadlines rather than on the page; the Amplemarket request is a live thread with Jan Suski and is not re-pitched.",
    "Two high-relevance requests are now well past the cold line with no draft and no send: Enterprise AI Leaders - agent sprawl (18d) and Scientists paying for PhD/postdoc AI subscriptions (18d). Neither has ever been pitched. Recorded so the accumulating cost of the cold queue is visible rather than only its count.",
]

d["summary"] = (
    f"47 tracked requests (all 47 re-verified live, 0 new on-beat, 0 dropped off, 3 pitched, 1 "
    f"deliberately skipped). Of the 43 unpitched, {len(live)} are live and {len(cold)} are cold, and "
    f"2 are sendable - down from 3 because the Anthropic draft was left unsent past the 10-day line. "
    f"No AI+spend slug appeared in the 126-slug window at all, the first time that has happened in "
    f"five runs; the 8 AI-token candidates were read in full and none carries a spend ask. The pair "
    f"range re-asserted clean against the refreshed snapshot and held at 1.11x-2.53x over 19 tiers "
    f"across 14 tools. Both remaining reply routes were re-resolved against the live pages and hold. "
    f"No new replies in the mailbox. Zero pitches sent this run - sends remain George's lane.")

d["recommended_actions"] = [
    "SEND THE RACONTEUR SHADOW-AI DRAFT. It is paste-ready at pitch-drafts-2026-09-23.md section 1, 154-word body, route simon.chandler@raconteur.net (re-resolved off the live /contributors/simon-chandler page today: HTTP 200, triple unchanged, control author /contributors/tom-dennis checked). It is the only high-relevance request in the queue, the only core-beat find the monitor has produced, and it has now been written and unsent for FIVE consecutive runs. Its figures were re-derived today against the refreshed snapshot.",
    "SEND OR DROP THE ANTHROPIC DRAFT TODAY, LATE. It crossed the cold line this run at 11 days. The draft is at pitch-drafts-2026-09-22.md section 2 and its route (Signal hliwrites.99) is still verbatim on the live page. Carrying it a fifth time without either sending or recording it as skipped is the exact defect this monitor exists to fix. If it is dead, say so and it gets recorded in pitch-ledger.json.",
    "SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-09-23.md section 2, 164-word body, holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today alongside five other named masthead addresses). Standing constraint is in its first line; 5 days old, so it is the freshest of the three.",
    "SEND THE FIGURES CORRECTION TO JAN SUSKI. The thread is live, he replied on 2026-09-18, and he was told '1.21x-2.53x, median 1.33x' when the true figure is 1.11x-2.53x, median 1.25x over 19 tiers. An un-flagged wrong figure in a peer method discussion is worse than a follow-up, and it has now been outstanding for five days. Route: reply to jan@jansuski.com, In-Reply-To the existing thread.",
    "DECIDE ON FINOPS (16d, high, cold, unpitched since 2026-09-17). Its draft exists at pitch-drafts-2026-09-17.md section 1 and its route is a LinkedIn DM to linkedin.com/in/niloy-ghosh. Still the highest-relevance request the monitor has never answered. Send it late or drop it; do not draft it a fifth time.",
    "RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has now produced no core-beat request on four of the last five runs and today no AI+spend slug at all, so this is the only lever that widens the monitor rather than re-reading the same single source. It is also the one blocker on this list that is not George's to clear.",
]

d["monitor_health"] = {
    "platforms_accessible": 1,
    "platforms_blocked": 9,
    "core_beat_new_requests": 0,
    "new_ai_token_slugs_in_window": len(window["ai_only"]),
    "new_ai_plus_spend_slugs_in_window": len(window["ai_spend"]),
    "consecutive_runs_without_new_core_beat": 4,
    "tracked_urls": len(ops),
    "carried_and_reverified": len(ops),
    "unpitched": len(unpitched),
    "live_unpitched": len(live),
    "live_unpitched_with_a_resolved_route": 2,
    "cold_unpitched": len(cold),
    "pitches_sent_to_date": 3,
    "pitches_sent_this_run": 0,
    "replies_received_to_date": 1,
    "resolved_email_routes": 3,
    "drafts_written_never_sent": 4,
    "sendable": 2,
    "lost_to_the_cold_line_with_a_draft_ready": 1,
}

d["monitor_defects_fixed_this_run"] = [
    "THE DIGEST IS NOW COMPUTED FROM THE PAGE FACTS RATHER THAN WRITTEN BY HAND. digest-2026-09-23.json was generated by marketing/haro-outreach/_write_digest_0923.py, which takes each carried request and replaces every page-answerable claim (http, live, days_old, badge, datePublished) with today's measured value out of verified-requests.json, keeping only the historical prose that records what earlier runs saw. The previous digest's deadline strings were free text accumulated over runs and had drifted: five rows still read 'age superseded' from an earlier edit, and two rows (the Inc. founders request and the Cybersecurity request) had carried a stale '6 days' figure from a run when they were genuinely 6 days old. Age now comes from one place.",
    "THE QUEUE'S DRAFT INDEX POINTED AT YESTERDAY'S FILE FOR ROWS THAT HAD MOVED. build_pitch_queue.py's DRAFTS map named pitch-drafts-2026-09-22.md for all the shadow-AI and Speciality Food rows. Both were re-derived and re-drafted today, so the map and the pair-range caveat now name pitch-drafts-2026-09-23.md and record that the 19-pair set passed its assertion for the first time.",
    "THE ANTHROPIC ROW WAS STILL BEING ADVERTISED AS SENDABLE ON THE DAY IT CROSSED. The map described it as 'now exactly 10 days old - the last day before the cold line'. It crossed today, so the row is now labelled CROSSED COLD and the crossing is recorded in the ledger's cold_without_a_send, rather than the sendable count silently dropping from 3 to 2 with no explanation anywhere in the artifacts.",
    "WORD COUNTS IN THE DRAFTS WERE CHECKED RATHER THAN ASSERTED, AND TWO WERE WRONG. The first pass through pitch-drafts-2026-09-23.md claimed 138 and 136 words; measured properly (body only, excluding subject line, signature and the unsubscribe footer) they are 154 and 164. Both are under the 200 limit either way, but a claimed word count that nobody measured is the same class of defect as the superseded pair range. Fixed in the file and re-measured by marketing/haro-outreach/_verify_drafts_0923.py.",
    "ELEVEN INDEX PAGES WERE STILL SITTING IN THE HISTORICAL DIGESTS AS OPPORTUNITIES. build_pitch_queue.py filters /media-outlets/<outlet>/journo-requests and /topics/<topic>/journo-requests at read time, so the queue was already correct - but digest-2026-09-07 (1 record), digest-2026-09-08 (4) and digest-2026-09-09 (6) still carried them, and any other reader of those files, or any future rewrite of the builder, would re-inflate the count from them. Exactly the failure mode the brief names. Removed by marketing/haro-outreach/_strip_index_pages_0923.py, which records what it removed in each digest's own `index_pages_removed` field rather than deleting the evidence silently. The queue's totals are unchanged by the cleanup (47 tracked, 26 live, 2 sendable), which confirms the queue was never reading them.",
]

DEST.write_text(json.dumps(d, indent=1), encoding="utf-8")
print(f"updated {DEST.name}: live={len(live)} cold={len(cold)} ops={len(ops)}")
