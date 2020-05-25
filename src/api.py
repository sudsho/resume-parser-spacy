"""End-to-end parse: text -> structured fields."""
from . import extract
from . import parse
from . import skills as skills_mod
from . import email_phone
from . import sections as sec_mod


def parse_resume_text(text, use_spacy=True):
    """Parse pre-extracted text. Set use_spacy=False to skip NER (faster, lighter)."""
    secs = sec_mod.split_sections(text)
    skills_text = secs.get("skills", text)

    out = {
        "name": None,
        "emails": email_phone.find_emails(text),
        "phones": email_phone.find_phones(text),
        "urls": email_phone.find_urls(text),
        "education": parse.find_education(secs.get("education", text)),
        "skills": skills_mod.find_skills(skills_text),
        "organizations": [],
        "dates": [],
        "sections": list(secs.keys()),
    }

    if use_spacy:
        ents = parse.parse_entities(text)
        out["name"] = parse.guess_name(text, ents=ents)
        out["organizations"] = ents.get("ORG", [])
        out["dates"] = ents.get("DATE", [])

    return out


def parse_resume_file(path, use_spacy=True):
    text = extract.extract_text(path)
    out = parse_resume_text(text, use_spacy=use_spacy)
    out["_text_length"] = len(text)
    return out
