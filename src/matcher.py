"""Custom spaCy Matcher patterns for resume sections."""
from spacy.matcher import Matcher


def build_matcher(nlp):
    matcher = Matcher(nlp.vocab)

    # section headers
    matcher.add("EDU_HEADER", None, [{"LOWER": "education"}])
    matcher.add("EXP_HEADER", None, [{"LOWER": {"IN": ["experience", "employment"]}}])
    matcher.add("SKILL_HEADER", None, [{"LOWER": "skills"}])
    matcher.add("PROJ_HEADER", None, [{"LOWER": "projects"}])

    # year ranges like "2015 - 2019"
    matcher.add(
        "YEAR_RANGE",
        None,
        [
            {"SHAPE": "dddd"},
            {"ORTH": {"IN": ["-", "-", "to"]}},
            {"SHAPE": "dddd"},
        ],
    )

    return matcher


def find_section_offsets(nlp, doc, matcher=None):
    if matcher is None:
        matcher = build_matcher(nlp)
    matches = matcher(doc)
    sections = {}
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        sections.setdefault(label, []).append((start, end))
    return sections
