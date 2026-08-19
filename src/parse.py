"""spaCy-based parsing: name, organizations, dates.

If the en_core_web_sm model is installed, spaCy NER is used for name / ORG /
DATE. If it is not installed (offline, no download), we fall back to a blank
tokenizer (spacy.blank("en")) plus a rule-based name guess so parsing still
runs end to end with no model download.
"""
import os
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
_ner_available = None

# section-header words that should never be mistaken for a person name
_HEADER_WORDS = {
    "education", "experience", "employment", "skills", "projects",
    "certifications", "summary", "objective", "profile", "academic",
    "qualifications", "work history", "professional experience",
    "technical skills", "core competencies", "contact", "resume",
    "curriculum vitae",
}


def get_nlp():
    """Return a loaded spaCy pipeline.

    Prefers the small English model (NER for name/ORG/DATE). If it is not
    installed we fall back to a blank English pipeline so nothing needs to be
    downloaded. Set RESUME_PARSER_NO_MODEL=1 to force the offline blank path.
    """
    global _nlp, _ner_available
    if _nlp is None:
        force_blank = os.environ.get("RESUME_PARSER_NO_MODEL") == "1"
        if not force_blank:
            try:
                _nlp = spacy.load("en_core_web_sm")
                _ner_available = True
            except Exception:
                _nlp = None
        if _nlp is None:
            _nlp = spacy.blank("en")
            _ner_available = False
    return _nlp


def ner_available():
    """True if the spaCy NER model is loaded (name/ORG/DATE via entities)."""
    if _ner_available is None:
        get_nlp()
    return _ner_available


def _guess_name_rulebased(text):
    """Pick a name from the top of the resume without NER.

    Heuristic: the first non-empty line in the first ~8 lines that looks like a
    person name - 1 to 4 alphabetic tokens, no digits, no '@', not a section
    header, and not an all-caps banner longer than a couple of words.
    """
    for raw in text.splitlines()[:8]:
        line = raw.strip()
        if not line:
            continue
        low = line.lower().rstrip(":")
        if low in _HEADER_WORDS:
            continue
        if "@" in line or any(c.isdigit() for c in line):
            continue
        tokens = line.split()
        if not (1 <= len(tokens) <= 4):
            continue
        if not all(re.match(r"^[A-Za-z][A-Za-z.'-]*$", t) for t in tokens):
            continue
        return line
    return None


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
    """Pick first PERSON entity in the first ~12 lines, else a rule-based guess.

    With the NER model this uses PERSON entities. On the blank/offline pipeline
    there are no entities, so it falls back to _guess_name_rulebased.
    """
    if ents is None:
        ents = parse_entities(text)
    persons = ents.get("PERSON", [])
    if persons:
        head = "\n".join(text.splitlines()[:12]).lower()
        for p in persons:
            if p.lower() in head:
                return p
        return persons[0]
    return _guess_name_rulebased(text)


def find_education(text):
    """Return lines that look like education entries."""
    edu = []
    for line in text.splitlines():
        if DEGREE_RE.search(line):
            edu.append(line.strip())
    return edu
