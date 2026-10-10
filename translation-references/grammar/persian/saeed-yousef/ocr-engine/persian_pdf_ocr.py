#!/usr/bin/env python3
"""Evidence-preserving Persian PDF OCR. See README for limitations.

Requires PyMuPDF + Pillow, plus Tesseract CLI (default); PaddleOCR optional.
No language-model rewriting, automatic sentence reversal, or silent normalisation.
"""
from __future__ import annotations

import argparse
import csv
from difflib import SequenceMatcher
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from statistics import mean
from typing import Any

try:
    import fitz
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
except ImportError as exc:
    raise SystemExit("Install: python -m pip install pymupdf pillow") from exc

PERSIAN_CHARS = re.compile(r"[\u0600-\u06ff]")
SUSPECT_BIDI = re.compile(r"[\u202a-\u202e\u2066-\u2069\ufffd]")


def page_selection(spec: str, total: int) -> list[int]:
    if not spec or spec.lower() == "all":
        return list(range(1, total + 1))
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not re.fullmatch(r"\d+(?:-\d+)?", part):
            raise ValueError(f"Invalid page selection: {part!r}")
        bounds = [int(x) for x in part.split("-")]
        start, end = (bounds[0], bounds[0]) if len(bounds) == 1 else bounds
        if start < 1 or end > total or end < start:
            raise ValueError(f"Page range {part} outside PDF (1–{total})")
        pages.update(range(start, end + 1))
    return sorted(pages)


def text_agreement(a: str, b: str) -> float:
    """Approximate comparison signal, NOT confidence or accuracy.

    Disabling SequenceMatcher autojunk matters for long Persian pages: common
    script characters otherwise get ignored and near-identical pages score ~0.
    Bound the comparison window to avoid excessive time on very large pages.
    """
    left = " ".join(a.split())[:3500]
    right = " ".join(b.split())[:3500]
    return round(SequenceMatcher(None, left, right, autojunk=False).ratio(), 4)


def embedded_diagnostics(text: str, minimum: int) -> tuple[bool, list[str]]:
    """Only a coarse screening; long extracted text can STILL have broken RTL order."""
    problems = []
    if len(text.strip()) < minimum:
        problems.append("low_extracted_character_count")
    if SUSPECT_BIDI.search(text):
        problems.append("replacement_or_bidi_control")
    if "\ufffd" in text:
        problems.append("unicode_replacement")
    return len(problems) == 0, problems


def safe_dpi_for(page, requested: int, max_pixels: int) -> int:
    estimated = (page.rect.width * requested / 72) * (page.rect.height * requested / 72)
    if estimated <= max_pixels:
        return requested
    import math
    dpi = int(requested * math.sqrt(max_pixels / estimated))
    if dpi < 75:
        raise ValueError("Page too large for pixel budget (needs <75 DPI)")
    return dpi


def render_grayscale(page, dpi: int, *, enhance: bool) -> Image.Image:
    pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY, alpha=False)
    img = Image.frombytes("L", (pix.width, pix.height), pix.samples)
    if enhance:
        img = ImageOps.autocontrast(img, cutoff=0.5)
        img = ImageEnhance.Contrast(img).enhance(1.15)
        img = img.filter(ImageFilter.UnsharpMask(radius=1.1, percent=120, threshold=3))
    return img


def check_tesseract(langs: str) -> None:
    executable = shutil.which("tesseract")
    if not executable:
        raise RuntimeError("tesseract executable not found in PATH")
    res = subprocess.run([executable, "--list-langs"], capture_output=True, text=True, check=True, timeout=30)
    found = {row.strip() for row in (res.stdout + "\n" + res.stderr).splitlines()}
    missing = set(langs.split("+")) - found
    if missing:
        raise RuntimeError("Missing Tesseract language data: " + ", ".join(sorted(missing)) +
                           ". Install the corresponding .traineddata files, preferably tessdata_best for fas.")


def tesseract_one(image: Image.Image, tmpdir: Path, *, lang: str, psm: int, tag: str, timeout: int) -> dict:
    inp = tmpdir / f"{tag}.png"
    base = tmpdir / f"{tag}-output"
    image.save(inp)
    # Tesseract can produce both plain text and TSV in a single recognition pass.
    cmd = ["tesseract", str(inp), str(base), "-l", lang, "--oem", "1", "--psm", str(psm), "txt", "tsv"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f"Tesseract exited {p.returncode}: {p.stderr[-1200:]}")
    text = base.with_suffix(".txt").read_text(encoding="utf-8-sig").strip()
    boxes = []
    with base.with_suffix(".tsv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row.get("level") != "5" or not row.get("text", "").strip():
                continue
            try:
                confidence = float(row.get("conf", "-1"))
                box = {key: int(row[key]) for key in ("left", "top", "width", "height")}
            except (ValueError, KeyError):
                continue
            boxes.append({"text": row["text"], "confidence": round(confidence, 2), "box": box})
    valid = [x["confidence"] for x in boxes if x["confidence"] >= 0]
    return {"text": text, "confidence": round(mean(valid), 2) if valid else None,
            "words": boxes, "engine": "tesseract", "psm": psm}


def paddle_one(image: Image.Image, ocr: Any) -> dict:
    import numpy as np  # optional paddle dependency
    result = ocr.predict(input=np.asarray(image.convert("RGB")))
    outputs = []
    for item in result:
        data = item.json
        section = data.get("res", data)
        txt = section.get("rec_texts", [])
        scores = section.get("rec_scores", [])
        boxes = section.get("rec_boxes", [])
        for idx, item_txt in enumerate(txt):
            if not str(item_txt).strip():
                continue
            box = (boxes[idx].tolist() if hasattr(boxes[idx], "tolist") else list(boxes[idx])) if idx < len(boxes) else None
            if box is not None:
                box = [int(x) for x in box]
            outputs.append({"text": str(item_txt), "confidence": round(float(scores[idx]) * 100, 2), "box": box})
    nums = [v["confidence"] for v in outputs]
    # Native Paddle ordering is preserved; do NOT blindly sort all lines by x/y.
    return {"text": "\n".join(o["text"] for o in outputs),
            "confidence": round(mean(nums), 2) if nums else None,
            "words": outputs, "engine": "paddleocr", "psm": None}


def recognize(image: Image.Image, *, engine: str, tesslang: str, psms: list[int], timeout: int,
              paddle: Any = None) -> dict:
    with tempfile.TemporaryDirectory(prefix="persian-ocr-") as d:
        if engine == "paddle":
            return paddle_one(image, paddle)
        candidates = [tesseract_one(image, Path(d), lang=tesslang, psm=psm,
                                     tag=f"pass-{n}-{psm}", timeout=timeout)
                      for n, psm in enumerate(psms)]
        # Confidence is a model metric, NOT verified transcription accuracy.
        # Prefer meaningful text if a pass emits nothing; otherwise higher mean confidence.
        return max(candidates, key=lambda item: (bool(item["text"].strip()), item["confidence"] or -1))


def save_text(path: Path, text: str):
    path.write_text(text.rstrip("\n") + "\n", encoding="utf-8")


def process_document(pdf: Path, dest: Path, *, mode: str = "compare", engine: str = "tesseract",
                     pages: str = "all", dpi: int = 300, min_text_chars: int = 80,
                     columns: int = 1, psms: list[int] | None = None,
                     enhance: bool = True, max_pixels: int = 22000000,
                     timeout: int = 120, tesslang: str = "fas+eng", qa: bool = False) -> dict:
    if not pdf.is_file():
        raise FileNotFoundError(pdf)
    if dest.resolve() == pdf.resolve() or dest.resolve() == pdf.parent.resolve():
        raise ValueError("Output directory must be distinct from PDF location")
    if mode not in {"auto", "ocr", "compare", "text"}:
        raise ValueError("mode must be auto, ocr, compare, or text")
    if engine not in {"tesseract", "paddle"}:
        raise ValueError("unknown OCR engine")
    if columns not in (1, 2):
        raise ValueError("columns must be 1 or 2")
    psms = psms or [3, 6]
    if any(p not in range(3, 14) for p in psms):
        raise ValueError("invalid PSM; use 3–13")
    if mode != "text" and engine == "tesseract":
        check_tesseract(tesslang)
    paddle = None
    if mode != "text" and engine == "paddle":
        try:
            from paddleocr import PaddleOCR
        except ImportError as exc:
            raise RuntimeError("PaddleOCR not installed. See README optional installation.") from exc
        paddle = PaddleOCR(lang="fa", ocr_version="PP-OCRv5", use_doc_orientation_classify=False,
                           use_doc_unwarping=False, use_textline_orientation=False)
    source_hash = hashlib.sha256()
    with pdf.open("rb") as f:
        for chunk in iter(lambda: f.read(2 ** 20), b""):
            source_hash.update(chunk)
    outpages = dest / "pages"
    outpages.mkdir(parents=True, exist_ok=True)
    entries = []
    markdown = ["# Persian PDF extraction — source-preserving output", "",
                f"Source SHA-256: `{source_hash.hexdigest()}`", "",
                "**Unverified transcription.** Check each page against original PDF.", ""]
    qa_records = []
    qa_check = None
    if qa:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ocr-support"))
        try:
            from check_ocr import check as qa_check  # noqa: PLC0415
        except ImportError as exc:
            raise RuntimeError("OCR QA checker not available at sibling ocr-support/check_ocr.py") from exc
    with fitz.open(pdf) as document:
        chosen = page_selection(pages, len(document))
        for number in chosen:
            pg = document[number-1]
            embedded = pg.get_text("text", sort=False).strip()
            good, issues = embedded_diagnostics(embedded, min_text_chars)
            needs_ocr = mode in ("ocr", "compare") or (mode == "auto" and not good)
            ocr_data = None
            effective_dpi = None
            if needs_ocr:
                effective_dpi = safe_dpi_for(pg, dpi, max_pixels)
                image = render_grayscale(pg, effective_dpi, enhance=enhance)
                if columns == 2:
                    # User-authorized explicit two-column layout. Persian column order: right -> left.
                    midpoint = image.width // 2
                    column_images = [image.crop((midpoint, 0, image.width, image.height)),
                                     image.crop((0, 0, midpoint, image.height))]
                    column_results = [recognize(crop, engine=engine, tesslang=tesslang, psms=psms,
                                                timeout=timeout, paddle=paddle) for crop in column_images]
                    # Coordinates are relative to each crop; record columns explicitly.
                    ocr_data = {"text": "\n\n".join(x["text"] for x in column_results if x["text"]),
                                "confidence": round(mean([x["confidence"] for x in column_results if x["confidence"] is not None]), 2)
                                              if any(x["confidence"] is not None for x in column_results) else None,
                                "columns": column_results, "engine": engine}
                else:
                    ocr_data = recognize(image, engine=engine, tesslang=tesslang, psms=psms,
                                         timeout=timeout, paddle=paddle)
            extracted = ocr_data["text"] if ocr_data is not None else embedded
            origin = "ocr" if ocr_data is not None else "embedded_text_layer"
            name = f"p{number:04d}"
            save_text(outpages / f"{name}-embedded.txt", embedded)
            if ocr_data is not None:
                save_text(outpages / f"{name}-{engine}.txt", ocr_data["text"])
                (outpages / f"{name}-geometry.json").write_text(
                    json.dumps(ocr_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            save_text(outpages / f"{name}-selected.txt", extracted)
            entry = {"page": number, "source": origin, "engine": engine if needs_ocr else None,
                     "selected_text": extracted, "embedded_text": embedded,
                     "ocr_text": ocr_data["text"] if ocr_data is not None else None,
                     "ocr_mean_confidence": ocr_data["confidence"] if ocr_data else None,
                     "quality_flag": (issues + (["embedded_and_ocr_differ_substantially"] if ocr_data and len(embedded) > min_text_chars and text_agreement(embedded, ocr_data["text"]) < 0.65 else [])),
                     "embedded_ocr_similarity": text_agreement(embedded, ocr_data["text"]) if ocr_data and embedded else None,
                     "effective_dpi": effective_dpi,
                     "columns_assumed": columns if needs_ocr else None,
                     "verification_status": "unverified_transcription"}
            entries.append(entry)
            markdown.extend([f"## PDF page {number}", "", extracted, ""])
            if qa_check:
                qa_records.extend(qa_check(extracted, source_id=name, page=number))
    with (dest / "pages.jsonl").open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    save_text(dest / "document.md", "\n".join(markdown))
    if qa:
        with (dest / "qa-report.jsonl").open("w", encoding="utf-8") as f:
            for r in qa_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest = {"input_filename": pdf.name, "input_sha256": source_hash.hexdigest(),
                "total_pdf_pages": None,
                "processed_pages": [x["page"] for x in entries],
                "mode": mode, "engine": engine, "dpi_requested": dpi,
                "columns_override": columns, "tesseract_languages": tesslang if engine == "tesseract" else None,
                "psms": psms if engine == "tesseract" else None,
                "qa_flags": len(qa_records), "source_preservation": "source PDF not changed; all text unverified"}
    with fitz.open(pdf) as d:
        manifest["total_pdf_pages"] = len(d)
    (dest / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pdf", type=Path, help="Source PDF (never modified)")
    p.add_argument("--out", type=Path, required=True, help="Destination output directory")
    p.add_argument("--engine", choices=["tesseract", "paddle"], default="tesseract")
    p.add_argument("--mode", choices=["auto", "ocr", "compare", "text"], default="compare")
    p.add_argument("--pages", default="all", help="1-indexed page list/range: 1,3-6")
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--min-text-chars", type=int, default=80)
    p.add_argument("--columns", type=int, choices=[1, 2], default=1)
    p.add_argument("--tess-langs", default="fas+eng")
    p.add_argument("--psm", type=int, action="append", help="Repeat to compare PSMs; default 3 and 6")
    p.add_argument("--max-pixels", type=int, default=22000000)
    p.add_argument("--timeout", type=int, default=120, help="Seconds per Tesseract call")
    p.add_argument("--no-enhance", action="store_true")
    p.add_argument("--qa", action="store_true", help="Run sibling QA checker on selected text")
    args = p.parse_args(argv)
    if args.dpi < 75 or args.dpi > 600:
        p.error("--dpi must be 75–600")
    if args.min_text_chars < 0 or args.max_pixels < 100000:
        p.error("invalid thresholds")
    if args.timeout < 1:
        p.error("--timeout must be positive")
    try:
        manifest = process_document(args.pdf, args.out, mode=args.mode, engine=args.engine,
                                    pages=args.pages, dpi=args.dpi, min_text_chars=args.min_text_chars,
                                    columns=args.columns, psms=args.psm, enhance=not args.no_enhance,
                                    max_pixels=args.max_pixels, timeout=args.timeout,
                                    tesslang=args.tess_langs, qa=args.qa)
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as ex:
        p.exit(2, f"Error: {ex}\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
