#!/usr/bin/env bash
# Nightly AIToolsEssentials mail digest → this Telegram DM. Add as a cronjob.
set -euo pipefail
cd /Users/georgezikry/aitoolessentials/site
OUT=$(python3 scripts/mail_triage.py inbox)
[ -z "$OUT" ] && exit 0
# Send via hermes messaging hook — replace 'telegram:DM' with the actual target.
# Prefer leaving a file the user can read; or use `hermes message send`.
echo "$OUT" > /tmp/ait-mail-digest.txt
echo "Mail digest written to /tmp/ait-mail-digest.txt"
