"""Evaluate the parser on a held-out folder of labeled resumes.

Each labeled file is `<name>.txt` with a sibling `<name>.json` carrying
gold fields like:

    {"name": "...", "emails": [...], "phones": [...], "skills": [...]}

The script reports per-field precision/recall/F1 over all examples.
"""
import argparse
import glob
import json
import os

from .api import parse_resume_text


def _set_match(pred, gold):
    pred_s = set([str(x).strip().lower() for x in pred or []])
    gold_s = set([str(x).strip().lower() for x in gold or []])
    if not pred_s and not gold_s:
        return 1.0, 1.0, 1.0
    tp = len(pred_s & gold_s)
    p = tp / len(pred_s) if pred_s else 0.0
    r = tp / len(gold_s) if gold_s else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f1


def evaluate(folder):
    txts = sorted(glob.glob(os.path.join(folder, "*.txt")))
    rows = []
    for t in txts:
        gold_path = t[:-4] + ".json"
        if not os.path.exists(gold_path):
            continue
        with open(t, "r", encoding="utf-8") as f:
            text = f.read()
        with open(gold_path, "r", encoding="utf-8") as f:
            gold = json.load(f)
        pred = parse_resume_text(text)
        row = {"file": os.path.basename(t)}
        for field in ("emails", "phones", "skills"):
            p, r, f1 = _set_match(pred.get(field), gold.get(field))
            row[field] = {"P": round(p, 3), "R": round(r, 3), "F1": round(f1, 3)}
        # name is single-valued
        gold_name = (gold.get("name") or "").lower().strip()
        pred_name = (pred.get("name") or "").lower().strip()
        row["name_match"] = bool(gold_name and gold_name in pred_name)
        rows.append(row)
    return rows


def summarize(rows):
    if not rows:
        return {}
    out = {}
    for field in ("emails", "phones", "skills"):
        for k in ("P", "R", "F1"):
            vals = [r[field][k] for r in rows]
            out["%s_%s" % (field, k)] = round(sum(vals) / len(vals), 3)
    out["name_acc"] = round(sum(r["name_match"] for r in rows) / len(rows), 3)
    out["n"] = len(rows)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="data/sample_resumes")
    args = p.parse_args()
    rows = evaluate(args.data)
    summary = summarize(rows)
    print(json.dumps({"rows": rows, "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
