"""Regex-based extractors for emails, phone numbers, urls."""
import re

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}")
URL_RE = re.compile(r"https?://[^\s)]+")


def find_emails(text):
    return list(set(EMAIL_RE.findall(text)))


def find_phones(text):
    matches = PHONE_RE.findall(text)
    # findall with groups returns tuples; rebuild
    out = []
    for m in re.finditer(PHONE_RE, text):
        out.append(m.group(0).strip())
    return list(set(out))


def find_urls(text):
    return list(set(URL_RE.findall(text)))
