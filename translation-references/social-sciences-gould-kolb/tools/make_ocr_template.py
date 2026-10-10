#!/usr/bin/env python3
"""Generate EMPTY OCR-output slots; do not copy the provisional benchmark text.

This is a model-output schema template, not an OCR inference or review approval.
The evaluator rejects submission_status=unfilled_template. A completed
model result must populate source-text fields, engine_id, engine_version
and submission_status=actual_model_output after genuinely running the engine.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from review_gate import ROOT, prepare


def template(root=ROOT):
    queue, _ = prepare(root)
    return [
        {
            "schema": "gould-kolb.ocr-structured-prediction.v1",
            "submission_status": "unfilled_template",
            "record_id": q["record_id"],
            "source_pdf_sha256": q["source_pdf_sha256"],
            "source_pdf_page": q["source_pdf_page"],
            "source_column": q["source_column"],
            "engine_id": None,
            "engine_version": None,
            "fields": {
                key: [] if key == "sections" else None
                for key in q["required_field_names"]
            },
        }
        for q in queue
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = template(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in data),
        encoding="utf-8")
    print(f"Prepared {len(data)} empty model-input slots. No OCR was performed.")


if __name__ == "__main__":
    main()
