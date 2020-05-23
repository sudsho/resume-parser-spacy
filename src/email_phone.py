"""Regex-based extractors for emails, phone numbers, urls."""
import re

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

# match international and indian formats; tightened to avoid grabbing random year ranges
_PHONE = (
    r"(?:\+?\d{1,3}[-.\s]?)?"
    r"(?:\(?\d{2,4}\)?[-.\s]?)?"
    r"\d{3,4}[-.\s]?\d{4}"
)
PHONE_RE = re.compile(_PHONE)

URL_RE = re.compile(r"https?://[^\s)]+")


def find_emails(text):
    return list(set(EMAIL_RE.findall(text)))


def find_phones(text):
    out = []
    for m in re.finditer(PHONE_RE, text):
        candidate = m.group(0).strip()
        digits = re.sub(r"\D", "", candidate)
        # need at least 7 digits to be a phone number, not a year/zip
        if len(digits) < 7:
            continue
        # too many digits = probably an account number
        if len(digits) > 15:
            continue
        # likely a 4-digit year range like "2015 - 2019"
        if re.match(r"^\d{4}\s*-\s*\d{4}$", candidate):
            continue
        out.append(candidate)
    # preserve order, dedup
    seen = set()
    uniq = []
    for p in out:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def find_urls(text):
    return list(set(URL_RE.findall(text)))
