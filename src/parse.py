"""spaCy-based parsing: name, organizations, dates."""
import spacy

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
