"""Keep third parties' personal email addresses off the public site.

Why this exists
---------------
Vendor submissions routinely carry a person's mailbox (`firstname@company.com`, or a private
Gmail / Hotmail / 163 address). Our review pages render the verification notes verbatim for
evidence, and those notes name the address we probed — so the site was republishing whichever
private mailbox the submitter happened to type into the form. The raw registries are served too
(`/data/tool_sources.json`, `/data/tools.json`), and the GitHub repository is public, so masking
only the rendered HTML would not have removed anything.

The evidence value is in *what we checked*, not in printing a usable mailbox. Sentences stay
readable — "the submission address", "the address published in the Privacy Policy" — and a redacted
address still shows that a specific route was probed.

Role addresses are deliberately kept: `support@`, `contact@`, `partnerships@` and friends are the
company's published business contact, they are what a reader needs to reach the vendor, and masking
them would degrade the citations for no privacy gain.

Used at render time (so a future submission cannot leak) and applied once to the stored records.
"""
import re

MASK = '[personal address withheld]'

# Local parts that are a company function rather than a person.
ROLE_LOCALPARTS = {
    'abuse', 'accounts', 'admin', 'affiliates', 'alerts', 'api', 'billing', 'biz', 'careers', 'compliance',
    'contact', 'dev', 'developers', 'dmca', 'dpo', 'enquiries', 'feedback', 'help', 'hi',
    'info', 'inquiries', 'jobs', 'legal', 'listings', 'marketing', 'media', 'news', 'newsletter',
    'noreply', 'no-reply', 'notifications', 'office', 'partners', 'partnerships', 'postmaster',
    'press', 'privacy', 'sales', 'schedule', 'security', 'service', 'sponsors', 'support', 'team',
    'updates', 'webmaster',
}

# Never mask these: our own addresses, which are published on purpose in the legal pages and
# footers, and any domain whose owners publish the mailbox sitewide as their contact.
ALWAYS_KEEP_ADDRESSES = {
    'aitoolsessentials@gmail.com',
    'contact@aitoolsessentials.com',
}

# Domains that must never be masked:
#   - our own, including the newsletter subdomain and the +tagged test mailboxes
#   - the RFC 2606 reserved domains, which only ever appear as placeholder text ("you@example.com")
ALWAYS_KEEP_DOMAINS = (
    'aitoolsessentials.com',
    'news.aitoolsessentials.com',
    'example.com',
    'example.org',
    'example.net',
)

EMAIL_RE = re.compile(r'[\w.+-]+@[\w.-]+\.\w{2,}')


def is_role(email: str) -> bool:
    """True when the mailbox is a company function rather than a named individual."""
    if email.lower() in ALWAYS_KEEP_ADDRESSES:
        return True
    domain = email.split('@')[-1].lower()
    if any(domain == d or domain.endswith('.' + d) for d in ALWAYS_KEEP_DOMAINS):
        return True
    local = email.split('@')[0].lower()
    # `first.last` and `first_last` are people; `support.eu` style role suffixes are rare enough
    # that treating the whole local part as the token is the safe default.
    return local in ROLE_LOCALPARTS


def mask_personal(text: str) -> str:
    """Replace every personal address in `text` with MASK. Role addresses pass through."""
    if not text:
        return text
    return EMAIL_RE.sub(lambda m: m.group(0) if is_role(m.group(0)) else MASK, text)


def personal_addresses(text: str) -> list[str]:
    """Personal addresses found in `text` — for guards that assert a file is clean."""
    if not text:
        return []
    return sorted({m.group(0) for m in EMAIL_RE.finditer(text) if not is_role(m.group(0))})
