"""Custom spaCy Matcher patterns for resume sections."""
from spacy.matcher import Matcher


def _add(matcher, key, pattern):
    """Add a pattern across spaCy versions.

    spaCy 3.x signature is matcher.add(key, patterns); spaCy 2.x was
    matcher.add(key, on_match, *patterns). Try the modern call first and fall
    back to the old positional-None form.
    """
    try:
        matcher.add(key, [pattern])
    except TypeError:
        matcher.add(key, None, [pattern])


def build_matcher(nlp):
    matcher = Matcher(nlp.vocab)

    # section headers
    _add(matcher, "EDU_HEADER", [{"LOWER": "education"}])
    _add(matcher, "EXP_HEADER", [{"LOWER": {"IN": ["experience", "employment"]}}])
    _add(matcher, "SKILL_HEADER", [{"LOWER": "skills"}])
    _add(matcher, "PROJ_HEADER", [{"LOWER": "projects"}])

    # year ranges like "2015 - 2019" or "2015 to 2019"
    _add(
        matcher,
        "YEAR_RANGE",
        [
            {"SHAPE": "dddd"},
            {"ORTH": {"IN": ["-", "to"]}},
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
