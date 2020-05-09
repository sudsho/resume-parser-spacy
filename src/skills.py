"""Skill keyword matching against configs/skills.txt."""
import os


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
    found = []
    text_l = text.lower()
    for s in skill_list:
        if s in text_l:
            found.append(s)
    return found
