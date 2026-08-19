"""Offline smoke test for resume-parser-spacy.

Runs the full parse pipeline on a bundled sample resume and boots the Flask
serving endpoint in-process, all without any network access or model download.

Two parse passes are exercised:

1. default  - uses en_core_web_sm if it happens to be installed, otherwise the
   blank/offline fallback (spacy.blank("en") + rule-based name guess).
2. forced offline - RESUME_PARSER_NO_MODEL=1 makes it take the blank path even
   when the model is present, proving the no-download path works.

The serving check uses Flask's in-process test client (no socket, no server
process) to POST the sample resume to /parse and hit /health.

Run:  python scripts/smoke.py      (or:  make smoke)
Exit code 0 = pass, non-zero = failure.
"""
import io
import json
import os
import sys

# make "src" and the repo root importable when run as a script
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

SAMPLE_PATH = os.path.join(ROOT, "data", "sample_resumes", "sample1.txt")


def _check(cond, msg):
    status = "ok  " if cond else "FAIL"
    print("  [%s] %s" % (status, msg))
    if not cond:
        raise AssertionError(msg)


def _assert_fields(out, label):
    print("--- %s ---" % label)
    print(json.dumps(out, indent=2, default=str))
    print("checks (%s):" % label)
    _check("johndoe@example.com" in out["emails"], "email extracted")
    _check(any("555" in p for p in out["phones"]), "phone extracted")
    _check("python" in out["skills"], "skill 'python' extracted")
    _check("aws" in out["skills"], "skill 'aws' extracted")
    _check(len(out["skills"]) >= 3, "several skills extracted (>=3)")
    _check(any("B.Tech" in e for e in out["education"]), "education line extracted")
    for sec in ("education", "experience", "skills"):
        _check(sec in out["sections"], "section '%s' detected" % sec)
    _check(out["name"] == "John Doe", "name == 'John Doe' (got %r)" % out["name"])
    print()


def main():
    from src import api, parse

    with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    print("=" * 64)
    print("resume-parser-spacy offline smoke")
    print("sample:", SAMPLE_PATH)
    print("=" * 64)

    # 1. default pass (model if installed, else blank fallback)
    out1 = api.parse_resume_text(text, use_spacy=True)
    print("NER model available on default path:", parse.ner_available())
    _assert_fields(out1, "pass 1: default")

    # 2. forced offline pass (blank pipeline, no model, no download)
    os.environ["RESUME_PARSER_NO_MODEL"] = "1"
    parse._nlp = None            # reset the cached pipeline
    parse._ner_available = None
    out2 = api.parse_resume_text(text, use_spacy=True)
    _check(parse.ner_available() is False, "forced-offline path uses blank pipeline")
    _assert_fields(out2, "pass 2: forced offline (spacy.blank)")

    # 3. serving endpoint in-process (no socket, no download)
    print("--- pass 3: Flask serving endpoint (in-process test client) ---")
    import app as flask_app_module

    client = flask_app_module.app.test_client()

    health = client.get("/health")
    print("GET /health ->", health.status_code, health.get_json())
    _check(health.status_code == 200, "GET /health returns 200")
    _check(health.get_json().get("status") == "ok", "GET /health status ok")

    data = {"resume": (io.BytesIO(text.encode("utf-8")), "sample1.txt")}
    resp = client.post("/parse", data=data, content_type="multipart/form-data")
    body = resp.get_json()
    print("POST /parse ->", resp.status_code)
    print(json.dumps(body, indent=2, default=str))
    _check(resp.status_code == 200, "POST /parse returns 200")
    _check("johndoe@example.com" in body["emails"], "POST /parse email extracted")
    _check("python" in body["skills"], "POST /parse skill extracted")
    print()

    print("=" * 64)
    print("SMOKE PASSED (offline, no model download)")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
