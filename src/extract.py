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
    from pdfminer.high_level import extract_text as pdf_extract
    return pdf_extract(path)


def extract_docx(path):
    import docx2txt
    return docx2txt.process(path)
