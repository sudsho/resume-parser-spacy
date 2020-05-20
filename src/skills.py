"""Skill keyword matching against configs/skills.txt."""
import os
import re

# common aliases -> canonical name
ALIASES = {
    "py": "python",
    "js": "javascript",
    "node": "nodejs",
    "node.js": "nodejs",
    "k8s": "kubernetes",
    "ml": "machine learning",
    "dl": "deep learning",
    "tf": "tensorflow",
    "scikitlearn": "scikit-learn",
    "sklearn": "scikit-learn",
}


def load_skills(path=None):
    if path is None:
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(here, "configs", "skills.txt")
    with open(path, "r", encoding="utf-8") as f:
        skills = [line.strip().lower() for line in f if line.strip()]
    return skills


def find_skills(text, skill_list=None):
    if skill_list is None:
        skill_list = load_skills()
    text_l = text.lower()
    found = []
    seen = set()

    # try aliases first
    for alias, canon in ALIASES.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", text_l) and canon not in seen:
            found.append(canon)
            seen.add(canon)

    # exact list
    for s in skill_list:
        if s in seen:
            continue
        # word boundary for short terms; substring for multi-word
        if " " in s or "/" in s:
            if s in text_l:
                found.append(s)
                seen.add(s)
        else:
            if re.search(r"\b" + re.escape(s) + r"\b", text_l):
                found.append(s)
                seen.add(s)
    return found
