"""Flask app for resume upload and parsing."""
import os
import tempfile
from flask import Flask, request, render_template, jsonify

from src.api import parse_resume_file

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

ALLOWED = {".pdf", ".docx", ".txt"}


@app.errorhandler(413)
def too_large(_e):
    return jsonify({"error": "file too large (>5MB)"}), 413


def allowed(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED


@app.route("/", methods=["GET"])
def index():
    return render_template("form.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return "no file", 400
    f = request.files["resume"]
    if f.filename == "":
        return "no filename", 400
    if not allowed(f.filename):
        return "unsupported file type", 400
    suffix = os.path.splitext(f.filename)[1].lower()
    fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    try:
        f.save(tmp_path)
        result = parse_resume_file(tmp_path)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
    return render_template("result.html", result=result, filename=f.filename)


@app.route("/parse", methods=["POST"])
def parse_json():
    """JSON endpoint - same as /upload but returns JSON."""
    if "resume" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["resume"]
    if f.filename == "" or not allowed(f.filename):
        return jsonify({"error": "bad file"}), 400
    suffix = os.path.splitext(f.filename)[1].lower()
    fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    try:
        f.save(tmp_path)
        result = parse_resume_file(tmp_path)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
