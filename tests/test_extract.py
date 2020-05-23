import os
import tempfile

import pytest

from src.extract import extract_text


def test_txt_extraction():
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("hello world\nfoo bar")
        path = f.name
    try:
        out = extract_text(path)
        assert "hello world" in out
        assert "foo bar" in out
    finally:
        os.remove(path)


def test_unknown_extension_raises():
    with pytest.raises(ValueError):
        extract_text("foo.xyz")
