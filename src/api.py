"""End-to-end parse: text -> structured fields."""
from . import extract
from . import parse
from . import skills
from . import email_phone


def parse_resume_text(text):
    ents = parse.parse_entities(text)
    name = parse.guess_name(text, ents=ents)
    emails = email_phone.find_emails(text)
    phones = email_phone.find_phones(text)
    urls = email_phone.find_urls(text)
    sk = skills.find_skills(text)
    edu = parse.find_education(text)
    return {
        "name": name,
        "emails": emails,
        "phones": phones,
        "urls": urls,
        "education": edu,
        "skills": sk,
        "organizations": ents.get("ORG", []),
        "dates": ents.get("DATE", []),
    }


def parse_resume_file(path):
    text = extract.extract_text(path)
    out = parse_resume_text(text)
    out["_text_length"] = len(text)
    return out
