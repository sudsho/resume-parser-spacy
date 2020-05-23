"""Tests for parse.py.

These do NOT load spaCy because en_core_web_sm may not be installed in CI;
we only test pure-python helpers like find_education and DEGREE_RE.
"""
from src.parse import find_education, DEGREE_RE


def test_degree_regex_btech():
    assert DEGREE_RE.search("B.Tech in Computer Science")


def test_degree_regex_phd():
    assert DEGREE_RE.search("PhD Machine Learning")


def test_degree_regex_negative():
    assert not DEGREE_RE.search("software engineer at Acme")


def test_find_education_picks_lines():
    text = "EDUCATION\nB.Tech, IIT Bombay\n\nEXPERIENCE\nSDE at Acme"
    edu = find_education(text)
    assert len(edu) == 1
    assert "B.Tech" in edu[0]
