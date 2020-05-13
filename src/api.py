"""End-to-end parse: text -> structured fields."""
from . import extract
from . import parse
from . import skills
from . import email_phone
from . import sections


def parse_resume_text(text):
    ents = parse.parse_entities(text)
    name = parse.guess_name(text, ents=ents)
    emails = email_phone.find_emails(text)
    phones = email_phone.find_phones(text)
    urls = email_phone.find_urls(text)
    secs = sections.split_sections(text)
    skills_text = secs.get("skills", text)
    sk = skills.find_skills(skills_text)
    edu = parse.find_education(secs.get("education", text))
    return {
        "name": name,
        "emails": emails,
        "phones": phones,
        "urls": urls,
        "education": edu,
        "skills": sk,
        "organizations": ents.get("ORG", []),
        "dates": ents.get("DATE", []),
        "sections": list(secs.keys()),
    }


def parse_resume_file(path):
    text = extract.extract_text(path)
    out = parse_resume_text(text)
    out["_text_length"] = len(text)
    return out
