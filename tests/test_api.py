"""End-to-end test on a sample resume, with use_spacy=False so the small
en_core_web_sm model is not needed in CI.
"""
from src.api import parse_resume_text


SAMPLE = """John Doe
john.doe@example.com
+1-555-123-4567

EDUCATION
B.Tech, IIT Bombay, 2015 - 2019

EXPERIENCE
SDE, Acme Corp, 2019 - Present

SKILLS
Python, Java, AWS, Docker
"""


def test_full_text_parse_no_spacy():
    out = parse_resume_text(SAMPLE, use_spacy=False)
    assert "john.doe@example.com" in out["emails"]
    assert any("555" in p for p in out["phones"])
    assert "python" in out["skills"]
    assert "aws" in out["skills"]
    # education line picked up
    assert any("B.Tech" in e for e in out["education"])
    # sections detected
    assert "education" in out["sections"]
    assert "experience" in out["sections"]
    assert "skills" in out["sections"]
