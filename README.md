# resume-parser-spacy

Resume parser using spaCy NER, regex pattern matchers, and a small Flask UI for file upload.

Pulls these fields out of a resume PDF or DOCX:

- name
- email
- phone
- education (degree + institution)
- skills (matched against a curated keyword list)
- experience (companies + dates)

Built as a weekend project to learn spaCy's `Matcher` and `EntityRuler` on top of the small English model. The UI lets you drop a `.pdf` or `.docx` and it returns parsed JSON.

## Status

WIP. Currently extracting raw text. Parsing logic next.
