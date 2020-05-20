#!/usr/bin/env bash
# Run the evaluator over the held-out sample set.
set -e
python -m src.evaluate --data data/sample_resumes
