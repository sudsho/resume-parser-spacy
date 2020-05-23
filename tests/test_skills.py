from src.skills import find_skills, load_skills


def test_load_skills_nonempty():
    skills = load_skills()
    assert "python" in skills
    assert len(skills) > 10


def test_find_basic():
    text = "Worked with Python, Java, and AWS for 3 years"
    found = find_skills(text)
    assert "python" in found
    assert "java" in found
    assert "aws" in found


def test_find_alias():
    text = "I use TF and PyTorch every day"
    found = find_skills(text)
    assert "tensorflow" in found


def test_find_multiword():
    text = "interested in machine learning and deep learning"
    found = find_skills(text)
    assert "machine learning" in found
    assert "deep learning" in found


def test_word_boundary():
    # 'aws' should not match inside 'awsome' (typo for awesome)
    text = "javascript is awsome"
    found = find_skills(text)
    assert "aws" not in found
