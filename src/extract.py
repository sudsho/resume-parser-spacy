"""Pull raw text out of resume files."""
import os


def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_pdf(path)
    if ext == ".docx":
        return extract_docx(path)
    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    raise ValueError("unsupported extension: %s" % ext)


def extract_pdf(path):
    # TODO: pdfminer.six
    raise NotImplementedError


def extract_docx(path):
    # TODO: docx2txt
    raise NotImplementedError
