"""Heuristic section splitter for resumes."""
import re

SECTION_HEADERS = {
    "education": ["education", "academic", "qualifications"],
    "experience": ["experience", "employment", "work history", "professional experience"],
    "skills": ["skills", "technical skills", "core competencies"],
    "projects": ["projects", "personal projects"],
    "certifications": ["certifications", "certificates"],
    "summary": ["summary", "objective", "profile"],
}


def _looks_like_header(line):
    line_l = line.strip().lower()
    if len(line_l) > 60:
        return None
    for key, terms in SECTION_HEADERS.items():
        for t in terms:
            if line_l == t or line_l.startswith(t + ":") or line_l.startswith(t + " "):
                return key
    return None


def split_sections(text):
    sections = {}
    cur = "header"
    sections[cur] = []
    for line in text.splitlines():
        h = _looks_like_header(line)
        if h is not None:
            cur = h
            sections.setdefault(cur, [])
            continue
        sections[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items() if v}
