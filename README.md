# resume-parser-spacy

Resume parser using spaCy NER, regex pattern matchers, and a small Flask UI for file upload.

Pulls these fields out of a `.pdf`, `.docx`, or `.txt` resume:

- name (first PERSON entity from spaCy near the top of the document)
- email (regex)
- phone (regex with year-range / digit-count guards)
- education (degree regex over the education section)
- skills (matched against `configs/skills.txt` plus alias table)
- organizations and date ranges (spaCy ORG / DATE)

Built as a weekend project to learn spaCy's `Matcher` and the small English model. Posting it here so the rough edges are visible -- the regex for phone numbers in particular is brittle, and the section splitter assumes the resume has the usual `EDUCATION / EXPERIENCE / SKILLS` headers.

## Architecture

```
                     +----------------+
   PDF/DOCX/TXT ---> |  src.extract   | --raw text-->
                     +----------------+
                                                  |
                                                  v
   +-------------+    +---------------+    +----------------+
   | regex pass  |<-- |  src.api      | -->| spaCy NER pass |
   | email/phone |    |  parse_resume |    | name / org     |
   | url / skill |    +---------------+    +----------------+
   +-------------+            |
                              v
                       structured JSON
                              |
                              v
                     +----------------+
                     |  Flask UI      |
                     |  /, /upload,   |
                     |  /parse, /health
                     +----------------+
```

## Setup

```
python -m venv .venv
source .venv/bin/activate           # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

The spaCy model download is required because the parser uses NER for name and organization extraction.

## Run the Flask app

```
python app.py
# open http://localhost:5000
```

Or with Docker:

```
docker-compose up --build
```

## API

`POST /upload` -- multipart form, field `resume`, returns rendered HTML with parsed fields.

`POST /parse` -- multipart form, field `resume`, returns JSON.

`GET /health` -- returns `{"status": "ok"}`.

Example curl:

```
curl -F "resume=@data/sample_resumes/sample1.txt" http://localhost:5000/parse
```

## CLI

```
python -m src.cli data/sample_resumes/sample1.txt --pretty
```

## Tests

```
pytest
```

The matcher / NER tests skip themselves if the spaCy model is not installed (so CI can be lighter).

## Evaluation

A small held-out set lives in `data/sample_resumes/sample*.json`. Run:

```
bash scripts/run_eval.sh
```

This prints per-field precision, recall, F1, and the average across the held-out resumes. On the bundled synthetic samples the scores look like this (run on May 26):

| field | P | R | F1 |
|---|---|---|---|
| emails | 1.00 | 1.00 | 1.00 |
| phones | 1.00 | 0.85 | 0.92 |
| skills | 0.93 | 0.88 | 0.90 |

Name accuracy: 4/4 on the small sample set.

These numbers are on synthetic data, so they overstate real-world quality. Real resumes have weirder layouts (two-column PDFs, headers as images, and so on).

## Folder layout

```
.
├── app.py                       # Flask app
├── src/
│   ├── extract.py               # PDF / DOCX / TXT to raw text
│   ├── parse.py                 # spaCy NER + degree regex
│   ├── matcher.py               # spaCy Matcher patterns
│   ├── sections.py              # heuristic section splitter
│   ├── skills.py                # keyword + alias matcher
│   ├── email_phone.py           # regex for email / phone / url
│   ├── api.py                   # glue layer
│   ├── evaluate.py              # P/R/F1 on held-out set
│   ├── train_ner.py             # optional NER fine-tune
│   └── cli.py                   # quick command-line wrapper
├── templates/
│   ├── form.html
│   └── result.html
├── configs/skills.txt           # skill keyword list
├── data/
│   ├── sample_resumes/          # synthetic resumes + gold labels
│   └── train.jsonl              # tiny annotated set for fine-tune
├── tests/                       # pytest
├── scripts/                     # train + eval shell wrappers
├── Dockerfile
├── docker-compose.yml
├── Procfile + runtime.txt       # Heroku
├── .github/workflows/test.yml   # CI
├── requirements.txt
├── LICENSE
└── README.md
```

## Known limitations

- The phone regex is permissive. It still occasionally grabs zip codes and long order numbers. The post-filter (length 7 to 15 digits, reject `\d{4}\s*-\s*\d{4}`) catches most cases but not all.
- spaCy's small model is OK for name extraction but stumbles on Indian and East Asian names. A larger model or fine-tuning on labeled resume data would help; `src/train_ner.py` is a starting point but I have not pushed a trained model into the repo because it is too large.
- Section splitter is line-based, so resumes with sections on the same line as content will get lumped into "header".
- PDFs that are scanned images need OCR (Tesseract) before this pipeline. Not in scope here.

## License

MIT, see `LICENSE`.
