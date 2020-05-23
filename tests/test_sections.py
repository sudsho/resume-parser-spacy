from src.sections import split_sections


SAMPLE = """John Doe
john@example.com

EDUCATION
B.Tech, IIT Bombay

EXPERIENCE
SDE, Acme

SKILLS
Python, Java
"""


def test_split_basic():
    secs = split_sections(SAMPLE)
    assert "education" in secs
    assert "experience" in secs
    assert "skills" in secs


def test_skills_section_content():
    secs = split_sections(SAMPLE)
    assert "Python" in secs["skills"]


def test_no_section_returns_header_only():
    secs = split_sections("just a single line of text")
    assert "header" in secs
