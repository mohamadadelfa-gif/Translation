#!/usr/bin/env python3
"""Run real Tesseract on 7 SHA-256-checked scanned PDF regions.

Outputs RAW, UNSEGMENTED text only. Does not create approved dictionary
entries, mark reviewed text as gold, or calculate CER/WER. Regions can include
adjacent articles or headings. Do not interpret Tesseract confidence as accuracy.
Requires: PyMuPDF, tesseract executable with fas+eng language data.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import statistics
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for piece in iter(lambda: f.read(1024 * 1024), b""):
            h.update(piece)
    return h.hexdigest()


def load_regions(root=ROOT):
    m = json.loads((root / "ocr_pilot/REGIONS.json").read_text(encoding="utf-8"))
    if m["schema"] != "gould-kolb.ocr-crop-regions.v1":
        raise ValueError("Unsupported OCR crop schema")
    if m["source_pdf_physical_pages"] != 980:
        raise ValueError("Invalid source page count")
    assert m["psm_modes"] == [4, 6] and m["ocr_language_config"] == "fas+eng"
    ids = set()
    for r in m["regions"]:
        ident, page, rect = r["region_id"], r["source_pdf_page"], r["crop_pdf_rect_points"]
        if (ident in ids or not isinstance(ident, str) or
                not isinstance(page, int) or not 1 <= page <= 980 or
                len(rect) != 4 or
                not all(isinstance(x, (int, float)) for x in rect) or
                not rect[0] < rect[2] or not rect[1] < rect[3]):
            raise ValueError("Invalid or repeated crop locator")
        ids.add(ident)
    if len(ids) != 7:
        raise ValueError("Expected 7 source crop regions")
    return m


def scan(pdf, output, root=ROOT):
    meta = load_regions(root)
    if (pdf.stat().st_size != meta["source_pdf_bytes"] or
            sha256(pdf) != meta["source_pdf_sha256"]):
        raise ValueError("Input does not match the user-supplied original PDF")
    if not shutil.which("tesseract"):
        raise RuntimeError("Tesseract executable not found")
    lang_check = subprocess.run(["tesseract", "--list-langs"],
                                capture_output=True, text=True, check=True)
    available = lang_check.stdout + lang_check.stderr
    if not all(("\n" + lang + "\n") in ("\n" + available + "\n") for lang in ("fas", "eng")):
        raise RuntimeError("Both fas and eng Tesseract models are required")
    version = subprocess.run(["tesseract", "--version"], capture_output=True,
                             text=True, check=True).stdout.splitlines()[0]
    import fitz
    document = fitz.open(pdf)
    if len(document) != meta["source_pdf_physical_pages"]:
        raise ValueError("Unexpected number of physical PDF pages")
    output.mkdir(parents=True, exist_ok=True)
    image_dir = output / "source_crops"
    image_dir.mkdir(exist_ok=True)
    rows, run_counts = [], []
    for r in meta["regions"]:
        page = document[r["source_pdf_page"] - 1]
        rect = fitz.Rect(*r["crop_pdf_rect_points"])
        if not page.rect.contains(rect):
            raise ValueError(f"Out-of-bounds crop {r['region_id']}")
        filename = r["region_id"] + ".png"
        cropped_image = image_dir / filename
        page.get_pixmap(
            matrix=fitz.Matrix(meta["pixel_render_scale"],
                               meta["pixel_render_scale"]),
            clip=rect, alpha=False).save(cropped_image)
        for mode in meta["psm_modes"]:
            args = ["tesseract", str(cropped_image), "stdout", "-l",
                    "fas+eng", "--psm", str(mode)]
            rendered = subprocess.run(args, capture_output=True, text=True,
                                      timeout=60, check=True).stdout
            tsv = subprocess.run(args + ["tsv"], capture_output=True, text=True,
                                 timeout=60, check=True).stdout.splitlines()
            head = tsv[0].split("\t") if tsv else []
            confidences = []
            if "conf" in head and "text" in head:
                for line in tsv[1:]:
                    cols = line.split("\t")
                    if len(cols) < len(head) or not cols[head.index("text")].strip():
                        continue
                    try:
                        value = float(cols[head.index("conf")])
                        if value >= 0:
                            confidences.append(value)
                    except ValueError:
                        continue
            item = {
                "schema": "gould-kolb.ocr-raw-crop.v1",
                "submission_status": "actual_model_output",
                "engine_id": "tesseract", "engine_version": version,
                "language_config": "fas+eng", "page_segmentation_mode": mode,
                "source_pdf_sha256": meta["source_pdf_sha256"],
                "source_pdf_page": r["source_pdf_page"],
                "region_id": r["region_id"],
                "crop_pdf_rect_points": r["crop_pdf_rect_points"],
                "crop_png": "source_crops/" + filename,
                "crop_png_sha256": sha256(cropped_image),
                "reading_scope": "unsegmented_source_region_including_adjacent_headings_possible",
                "raw_text": rendered,
                "tsv_mean_word_confidence_diagnostic":
                    round(statistics.mean(confidences), 2) if confidences else None,
                "tsv_word_count": len(confidences),
                "semantic_approval": False,
                "independent_source_review_completed": False,
                "cer": None, "wer": None, "gold_reference": None,
            }
            rows.append(item)
            run_counts.append({
                "region_id": r["region_id"], "pdf_page": r["source_pdf_page"],
                "psm": mode, "raw_characters": len(rendered),
                "word_boxes": len(confidences),
                "tesseract_confidence_not_accuracy":
                    item["tsv_mean_word_confidence_diagnostic"],
            })
    document.close()
    (output / "raw_ocr_candidates.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows),
        encoding="utf-8")
    report = {
        "schema": "gould-kolb.raw-ocr-pilot-report.v1",
        "verified_original_pdf_sha256": meta["source_pdf_sha256"],
        "source_pdf_identity_verified": True, "engine_version": version,
        "language_config": "fas+eng",
        "source_regions": len(meta["regions"]), "ocr_runs": len(rows),
        "metrics": run_counts,
        "independently_approved_gold_records": 0,
        "cer": None, "wer": None,
        "quality_limitations": [
            "Tesseract word confidence is not accuracy",
            "Crops include adjacent article text",
            "Mixed-language reading order may be incorrect",
            "Human review required before dictionary ingestion",
        ],
    }
    (output / "pilot_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    parts = []
    for r in meta["regions"]:
        candidates = [x for x in rows if x["region_id"] == r["region_id"]]
        cells = "".join("<div><h3>PSM " + str(x["page_segmentation_mode"]) +
                        "</h3><pre dir='auto'>" + html.escape(x["raw_text"]) +
                        "</pre></div>" for x in candidates)
        parts.append("<section><h2>" + html.escape(r["region_id"]) + "</h2><img src='source_crops/" +
                     r["region_id"] + ".png'><div class='columns'>" + cells + "</div></section>")
    page = """<!doctype html><html><meta charset='UTF-8'><meta name='viewport'
 content='width=device-width,initial-scale=1'><title>Unverified Gould-Kolb OCR</title>
 <style>body{font:16px system-ui;max-width:1100px;margin:auto;padding:22px;background:#eee}
 section{background:white;padding:16px;margin:18px 0;border-radius:12px}
 img{width:100%;max-width:700px}.columns{display:grid;grid-template-columns:1fr 1fr;gap:12px}
 pre{white-space:pre-wrap;direction:rtl;text-align:right;font:18px/2 Tahoma,Arial}
 @media(max-width:650px){.columns{grid-template-columns:1fr}}</style>
 <h1>Unverified OCR candidates</h1><p>NOT a dictionary or an accuracy benchmark.
 Scanned excerpts and two actual Tesseract outputs. No gold standard approved.</p>""" + "".join(parts) + "</html>"
    (output / "review_side_by_side.html").write_text(page, encoding="utf-8")
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--pdf", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(scan(args.pdf, args.output, args.root),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
