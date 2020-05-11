"""spaCy-based parsing: name, organizations, dates."""
import re
import spacy

DEGREE_PATTERNS = [
    r"\bb\.?\s?tech\b",
    r"\bb\.?\s?sc\b",
    r"\bm\.?\s?sc\b",
    r"\bm\.?\s?tech\b",
    r"\bphd\b",
    r"\bmba\b",
    r"\bbachelors?\b",
    r"\bmasters?\b",
    r"\bdoctorate\b",
]
DEGREE_RE = re.compile("|".join(DEGREE_PATTERNS), re.IGNORECASE)

# load once
_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def parse_entities(text):
    nlp = get_nlp()
    doc = nlp(text)
    out = {"PERSON": [], "ORG": [], "DATE": [], "GPE": []}
    for ent in doc.ents:
        if ent.label_ in out:
            out[ent.label_].append(ent.text.strip())
    # dedup
    for k in out:
        out[k] = list(dict.fromkeys(out[k]))
    return out


def guess_name(text, ents=None):
    """Pick first PERSON entity that shows up in the first ~10 lines."""
    if ents is None:
        ents = parse_entities(text)
    persons = ents.get("PERSON", [])
    if not persons:
        return None
    head = "\n".join(text.splitlines()[:12]).lower()
    for p in persons:
        if p.lower() in head:
            return p
    return persons[0]


def find_education(text):
    """Return lines that look like education entries."""
    edu = []
    for line in text.splitlines():
        if DEGREE_RE.search(line):
            edu.append(line.strip())
    return edu
