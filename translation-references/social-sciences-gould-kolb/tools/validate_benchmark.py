#!/usr/bin/env python3
"""Validate the Gould/Kolb first-pass visual transcription benchmark.

No OCR is performed. CI can validate record structure and source locators
without possession of the PDF; PDF-based source hash and evidence crops
are checked only when --pdf is explicitly provided.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"complete_referral", "article_section_excerpt"}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as inp:
        for chunk in iter(lambda: inp.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_records(path):
    records = []
    with Path(path).open(encoding="utf-8") as inp:
        for lineno, line in enumerate(inp, 1):
            if not line.strip():
                raise ValueError(f"Blank benchmark line {lineno}")
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Benchmark line {lineno} is not an object")
            records.append(row)
    return records


def validate(root: Path, pdf: Path | None = None, evidence_dir: Path | None = None):
    manifest = json.loads((root / "source_manifest.json").read_text(encoding="utf-8"))
    ev = json.loads((root / "benchmark/visual_evidence_manifest.json").read_text(encoding="utf-8"))
    if ev.get("schema") != "gould-kolb.benchmark-evidence.v1":
        raise ValueError("Missing benchmark evidence schema")
    crops = {}
    for crop in ev["crops"]:
        filename, page = crop["file"], crop["page"]
        if filename in crops or type(page) is not int or not 1 <= page <= manifest["physical_pages"]:
            raise ValueError(f"Duplicate or invalid evidence locator {filename}")
        box = crop["bbox_pdf_points"]
        if (len(box) != 4 or not all(type(n) in (int, float) for n in box)
                or not box[0] < box[2] or not box[1] < box[3]):
            raise ValueError(f"Invalid evidence rectangle {filename}")
        crops[filename] = crop

    rows = load_records(root / "benchmark/first_pass_v1.jsonl")
    if not rows:
        raise ValueError("Empty transcription benchmark")
    ids, pairs, counts = set(), set(), Counter()
    for row in rows:
        ident = row.get("record_id")
        if not isinstance(ident, str) or not ident or ident in ids:
            raise ValueError(f"Invalid or duplicate record ID {ident}")
        ids.add(ident)
        if row.get("schema") != "gould-kolb.ground-truth.v1":
            raise ValueError(f"Unknown benchmark schema at {ident}")
        kind = row.get("record_type")
        if kind not in KINDS:
            raise ValueError(f"Unsupported benchmark kind: {ident}")
        counts[kind] += 1
        page = row.get("source_pdf_page")
        column = row.get("source_column")
        evidence = crops.get(row.get("evidence_crop"))
        if (not evidence or page != evidence["page"]
                or not isinstance(page, int) or not 20 <= page <= 956
                or column not in ("left", "right")):
            raise ValueError(f"Invalid image-backed PDF locator: {ident}")
        if (row.get("transcription_status") != "first_visual_pass"
                or row.get("second_independent_pass") is not False
                or row.get("original_english_volume_comparison") is not False
                or row.get("authoritative_semantic_target_id") is not None):
            raise ValueError(f"Unjustified verification or semantic claim: {ident}")
        if row.get("spacing_linewrap_policy") != "linewraps_joined_no_editorial_modernization":
            raise ValueError(f"Unknown transcription linewrap policy: {ident}")
        if not isinstance(row.get("headword_fa_readable"), str) or not row["headword_fa_readable"]:
            raise ValueError(f"Missing Persian headword: {ident}")
        english = row.get("headword_en_readable")
        if english is not None and (not isinstance(english, str) or not english):
            raise ValueError(f"Invalid English headword: {ident}")
        if kind == "complete_referral":
            if (row.get("entry_completeness") != "complete_referral_only"
                    or row.get("referral_marker") != "←"
                    or not isinstance(row.get("referral_target_fa_readable"), str)
                    or not row["referral_target_fa_readable"]
                    or row.get("related_marker") is not None
                    or row.get("section_label") is not None
                    or row.get("section_text_readable") is not None):
                raise ValueError(f"Referral wrongly modeled as article: {ident}")
            key = (page, row["headword_fa_readable"], english,
                   row["referral_target_fa_readable"])
        else:
            if (row.get("entry_completeness") != "partial_article_single_A_section"
                    or row.get("section_label") != "A"
                    or not isinstance(row.get("section_text_readable"), str)
                    or not row["section_text_readable"].strip()
                    or row.get("referral_marker") is not None
                    or row.get("referral_target_fa_readable") is not None
                    or row.get("related_marker") is not None):
                raise ValueError(f"Unverified full-article or section claim: {ident}")
            key = (page, row["headword_fa_readable"], english, "A")
        if key in pairs:
            raise ValueError(f"Duplicate source observation at {ident}")
        pairs.add(key)

    source_check = False
    source_pages_checked = 0
    evidence_written = 0
    if pdf is not None:
        pdf = Path(pdf)
        if (pdf.stat().st_size != manifest["source_pdf_bytes"]
                or sha256(pdf) != manifest["source_pdf_sha256"]):
            raise ValueError("Attached PDF does not match the registered source")
        import fitz
        doc = fitz.open(pdf)
        if len(doc) != manifest["physical_pages"]:
            raise ValueError("Source PDF page count mismatch")
        source_check = True
        source_pages_checked = len({p["page"] for p in crops.values()})
        if evidence_dir is not None:
            evidence_dir = Path(evidence_dir)
            evidence_dir.mkdir(parents=True, exist_ok=True)
            for p in crops.values():
                page = doc[p["page"] - 1]
                rect = fitz.Rect(*p["bbox_pdf_points"])
                if not page.rect.contains(rect):
                    raise ValueError(f"Crop lies outside source page: {p['file']}")
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3),
                                      clip=rect, alpha=False)
                pix.save(evidence_dir / p["file"])
                evidence_written += 1
        doc.close()
    elif evidence_dir is not None:
        raise ValueError("Cannot generate source-image evidence without --pdf")

    return {
        "schema": "gould-kolb.benchmark-validation.v1",
        "registered_pdf_sha256": manifest["source_pdf_sha256"],
        "source_pdf_hash_checked_this_run": source_check,
        "distinct_source_pages_checked_in_this_run": source_pages_checked,
        "complete_referrals_transcribed_first_pass": counts["complete_referral"],
        "individual_A_sections_transcribed_first_pass": counts["article_section_excerpt"],
        "full_explanatory_articles_verified": 0,
        "independently_second_pass_reviewed": 0,
        "image_evidence_files_written": evidence_written,
        "semantic_references_resolved": 0,
        "benchmark_stage": "first_visual_pass_not_final_gold_standard",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--pdf", type=Path)
    p.add_argument("--evidence-dir", type=Path)
    p.add_argument("--report", type=Path)
    args = p.parse_args()
    result = validate(args.root, args.pdf, args.evidence_dir)
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
