"""Optional: fine-tune spaCy NER on a small annotated set.

Usage:
    python -m src.train_ner --train data/train.jsonl --out models/ner
"""
import argparse
import json
import random
import os

import spacy
from spacy.util import minibatch, compounding


def load_jsonl(path):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            text = row["text"]
            ents = [(e[0], e[1], e[2]) for e in row.get("entities", [])]
            examples.append((text, {"entities": ents}))
    return examples


def train(train_path, out_dir, n_iter=20, base_model="en_core_web_sm"):
    nlp = spacy.load(base_model)
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe("ner")

    train_data = load_jsonl(train_path)

    # add labels
    for _, ann in train_data:
        for ent in ann["entities"]:
            ner.add_label(ent[2])

    other_pipes = [p for p in nlp.pipe_names if p != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.resume_training()
        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
            print("iter %d losses %s" % (itn, losses))

    os.makedirs(out_dir, exist_ok=True)
    nlp.to_disk(out_dir)
    print("saved to", out_dir)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--train", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--iters", type=int, default=20)
    args = p.parse_args()
    train(args.train, args.out, n_iter=args.iters)


if __name__ == "__main__":
    main()
