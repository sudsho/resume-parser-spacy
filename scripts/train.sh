#!/usr/bin/env bash
# Fine-tune NER on the small labeled set.
set -e
python -m src.train_ner --train data/train.jsonl --out models/ner --iters 30
