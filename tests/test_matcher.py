"""Tests for matcher.py.

Skipped if en_core_web_sm is not available (CI runners without the model).
"""
import pytest

spacy = pytest.importorskip("spacy")

try:
    nlp_for_test = spacy.load("en_core_web_sm")
except Exception:
    nlp_for_test = None

skip_no_model = pytest.mark.skipif(
    nlp_for_test is None, reason="en_core_web_sm not installed"
)


@skip_no_model
def test_build_matcher_returns_matcher():
    from src.matcher import build_matcher
    m = build_matcher(nlp_for_test)
    assert m is not None


@skip_no_model
def test_year_range_matched():
    from src.matcher import build_matcher
    matcher = build_matcher(nlp_for_test)
    doc = nlp_for_test("Worked at Acme 2015 - 2019.")
    matches = matcher(doc)
    labels = [nlp_for_test.vocab.strings[mid] for mid, _, _ in matches]
    assert "YEAR_RANGE" in labels
