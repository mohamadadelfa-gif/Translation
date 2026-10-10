#!/usr/bin/env python3
"""CER / WER for manually verified *full page* ground truths only.

Never interpret OCR model confidence or PDF-to-OCR similarity as accuracy.
Gold JSONL: {"page": 1, "verified_text": "...", "verification": "visual_full_page"}
Predicted JSONL: pages.jsonl from persian_pdf_ocr.py
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import unicodedata


def distance(a, b):
    # Two-row Levenshtein distance; memory bounded.
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        curr = [i]
        for j, y in enumerate(b, 1):
            curr.append(min(curr[-1] + 1, prev[j] + 1, prev[j-1] + (x != y)))
        prev = curr
    return prev[-1]


def normalize_for_scoring(s: str) -> str:
    # Evaluation-only, does not change original/OCR output; preserves ZWNJ.
    return " ".join(unicodedata.normalize("NFC", s).split())


def compare(gold: str, prediction: str) -> dict:
    a, b = normalize_for_scoring(gold), normalize_for_scoring(prediction)
    wa, wb = a.split(), b.split()
    char_edits = distance(a, b)
    word_edits = distance(wa, wb)
    return {"gold_chars": len(a), "gold_words": len(wa),
            "char_edits": char_edits, "word_edits": word_edits,
            "cer": round(char_edits / max(1, len(a)), 4),
            "wer": round(word_edits / max(1, len(wa)), 4)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gold", required=True, type=Path)
    p.add_argument("--predicted", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    gold_records = [json.loads(x) for x in args.gold.read_text(encoding="utf-8").splitlines() if x.strip()]
    predicted = {int(j["page"]): j for line in args.predicted.read_text(encoding="utf-8").splitlines() if (j := json.loads(line))}
    rows = []
    for item in gold_records:
        if item.get("verification") != "visual_full_page" or not isinstance(item.get("verified_text"), str) or not item["verified_text"].strip():
            p.error("Gold input requires nonempty verified_text and verification=visual_full_page")
        page = int(item["page"])
        if page not in predicted:
            p.error(f"Prediction missing page {page}")
        row = {"page": page}
        for label, prediction in [("selected", predicted[page]["selected_text"]),
                                  ("embedded", predicted[page]["embedded_text"]),
                                  ("ocr", predicted[page]["ocr_text"])]:
            if prediction is not None:
                row[label] = compare(item["verified_text"], prediction)
        rows.append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"pages": rows, "note": "Only manually verified full-page references; no scores without gold"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Scored {len(rows)} fully verified pages: {args.output}")


if __name__ == "__main__":
    main()
