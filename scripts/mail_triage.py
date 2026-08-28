#!/usr/bin/env python3
"""AIToolsEssentials email experience.

Commands:
  python3 scripts/mail_triage.py inbox        — classified inbox digest
  python3 scripts/mail_triage.py intake       — latest FormSubmit intake parsed
  python3 scripts/mail_triage.py reply-audit  — draft an audit intake reply (not sent)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HIM = "himalaya"
CLIENT_AUDITS = Path("/Users/georgezikry/aitoolessentials/client-audits")
MAIL_DIR = Path("/Users/georgezikry/aitoolessentials/site/admin/email")
MAIL_DIR.mkdir(parents=True, exist_ok=True)


def run(args, inp=None):
    r = subprocess.run([HIM, *args], input=inp, capture_output=True, text=True, timeout=60)
    return r.stdout, r.stderr, r.returncode


def list_folder(folder, n=30):
    out, _, rc = run(["envelope", "list", "--folder", folder, "--page-size", str(n), "--output", "json"])
    try:
        return json.loads(out)
    except Exception:
        return []


def read_msg(mid, folder="INBOX"):
    out, _, _ = run(["message", "read", str(mid), "--folder", folder])
    return out


def parse_intake(text):
    """Parse the FormSubmit intake email.

    Himilaya 'message read' plain view puts the form on ONE long line between
    a 'Value' header and a 'Submitted at' footer. Fields are joined by the
    next key name. We split on the known field names.
    """
    # Normalize to one line for regex simplicity.
    flat = " ".join(text.split())
    # Boundary between 'Value' and 'Submitted at'.
    m = re.search(r"\bValue\s+(.*?)\s+Submitted at\b", flat, re.IGNORECASE)
    section = m.group(1) if m else flat
    field_names = ["name", "email", "business_type", "website", "current_tools",
                   "workflows", "questions", "budget"]
    fields = {}
    # Build alternation of keys and capture lazily until next key.
    keys_alt = "|".join(field_names)
    pattern = rf"\b({keys_alt})\s+(.*?)(?=\s+(?:{keys_alt})\s+|$)"
    for mm in re.finditer(pattern, section):
        fields[mm.group(1)] = mm.group(2).strip()
    return fields


def classify(msg):
    subj = (msg.get("subject") or "").lower()
    frm = ((msg.get("from") or {}).get("addr") or "").lower()
    has_att = msg.get("has_attachment")
    if "formsubmit" in frm and "intake" in subj:
        return "🔥 AUDIT INTAKE — reply within 24h (paid lead)"
    if "formsubmit" in frm and "tool" in subj:
        return "📬 VENDOR SUBMISSION — review queue"
    if "formsubmit" in frm and ("test" in subj or "report" in subj):
        return "📬 TEST REPORT — community"
    if frm.startswith("noreply"):
        return "🗑  noise (system)"
    if has_att:
        return "📎 attachment — check"
    if "re:" in subj:
        return "⏳ thread — check if they answered back"
    return "📥 reply — a human wrote you"


def digest():
    inbox = list_folder("INBOX", 30)
    if not inbox:
        print("Inbox empty or unreadable.")
        return
    print(f"{'='*72}\nAITOOLSESSENTIALS MAIL — {len(inbox)} in INBOX\n{'='*72}\n")
    order = {"🔥": 0, "📎": 1, "⏳": 2, "📥": 3, "📬": 4, "🗑": 9}
    rows = sorted(inbox, key=lambda m: order.get(classify(m)[:1], 5))
    for m in rows:
        c = classify(m)
        print(f"{c}")
        print(f"  from: {(m['from'].get('name') or m['from']['addr'])}")
        print(f"  subj: {m['subject']}")
        print(f"  date: {m['date']}   id: {m['id']}")
        if m.get("has_attachment"):
            print(f"  📎 has attachment")
        print()


def intake():
    inbox = list_folder("INBOX", 30)
    intakes = [m for m in inbox if "intake" in (m.get("subject") or "").lower()]
    if not intakes:
        print("No intake mails in INBOX.")
        return
    latest = intakes[0]
    print(f"Latest intake: id={latest['id']} date={latest['date']}\n")
    body = read_msg(latest["id"])
    fields = parse_intake(body)
    for k, v in fields.items():
        print(f"  {k:15} {v}")
    print()
    print("Next: reply-audit drafts a response (not sent).")


def reply_audit():
    inbox = list_folder("INBOX", 30)
    intakes = [m for m in inbox if "intake" in (m.get("subject") or "").lower()]
    if not intakes:
        print("No intake to reply to.")
        return
    latest = intakes[0]
    body = read_msg(latest["id"])
    fields = parse_intake(body)
    name = (fields.get("name") or "there").split()[0]
    email = fields.get("email") or ""
    biz = fields.get("website") or "your business"
    draft = f"""From: aitoolsessentials@gmail.com
To: {email}
Subject: Re: AI Stack Audit — {biz}

Hi {name},

Thanks for the intake. I have what I need to start the audit.

What you'll get:
1. A page-one cover + confidentiality marker.
2. Findings: what's actually true about your stack (with confidence, not vibes).
3. Keep / cut / trial for every tool you named — no padding.
4. A PHI fence page that shows exactly where ChatGPT stops.
5. Phones, scheduling, replies: how to use what you already pay for.
6. A print-ready front-desk page: 8 templates + the fence + the emergency rule.
7. 30-day roadmap + a blank worksheet you keep.
8. BAA questions if you ever trial a documentation tool.

Turnaround is 3 business days from this message.

**Scope** — This is strategy only. I will not set up software, access your EHR, take logins, sign BAAs, or offer ongoing support. Nothing in the deliverable is medical advice, diagnosis, triage, or treatment.

One question that will sharpen everything: what EHR/PMS, and what vendor handles your phones + SMS right now?

Best,
AIToolsEssentials
https://aitoolsessentials.com
Research and strategy only
"""
    out = MAIL_DIR / f"draft-intake-reply-{latest['id']}.txt"
    out.write_text(draft)
    print(f"Draft saved: {out}")
    print("Review it, then send with:")
    print(f"  cat {out} | himalaya template send")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "inbox"
    if cmd == "inbox":
        digest()
    elif cmd == "intake":
        intake()
    elif cmd == "reply-audit":
        reply_audit()
    else:
        print(__doc__)
