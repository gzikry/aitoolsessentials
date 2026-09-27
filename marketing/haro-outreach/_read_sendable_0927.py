#!/usr/bin/env python3
"""Read the two sendable request pages verbatim, to copy their live cutoff wording."""
import re
import subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
SLUGS = [
    "fulltime-employees-shadow-ai-use-and-paying-outofpocket",
    "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech",
]
for s in SLUGS:
    url = f"https://www.sourcee.app/journo-request/{s}"
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    hm = re.search(r"__HTTP__(\d+)__", raw)
    print(f"===== {s}")
    print(f"  HTTP {hm.group(1) if hm else '000'}  badge={badge.group(1) if badge else None}")
    print(f"  {core[:1400]}")
    print("  CUTOFF WORDS:", re.findall(r"[^.]*(?:deadline|by \w+day|before \w+day|expires|closing|urgent)[^.]*\.",
                                      core, re.I)[:4])
    print()
