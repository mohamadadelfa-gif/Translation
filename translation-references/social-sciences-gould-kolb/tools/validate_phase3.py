#!/usr/bin/env python3
"""Phase 3 visual transcription benchmark: provisional, not independently gold.

Validates 11 recheck decisions and 2 full-article first-pass candidates.
Optionally checks the original PDF SHA-256 and renders source-image crops.
No OCR or unsupported promotion of Persian text to ground truth.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows_jsonl(path: Path):
    rows = []
    with path.open(encoding="utf-8") as source:
        for lineno, line in enumerate(source, 1):
            if not line.strip():
                raise ValueError(f"{path}:{lineno}: blank source line")
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise ValueError(f"{path}:{lineno}: expected object")
            rows.append(obj)
    return rows


def pdf_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def validate(root: Path = ROOT, pdf: Path | None = None,
             evidence_dir: Path | None = None):
    source = json.loads((root / "source_manifest.json").read_text(encoding="utf-8"))
    evidence = json.loads(
        (root / "benchmark/complete_article_evidence.json").read_text(encoding="utf-8"))
    if (evidence.get("schema") != "gould-kolb.complete-article-evidence.v1"
            or evidence.get("independent_second_pass") is not False
            or evidence.get("pdf_present_in_repository") is not False):
        raise ValueError("Incompatible or overstated image evidence manifest")
    crops = {}
    for row in evidence.get("evidence_regions", []):
        name = row.get("file")
        if name in crops or not isinstance(name, str) or not name.endswith(".png"):
            raise ValueError("Duplicate or invalid source-image crop")
        page, bounds = row.get("page"), row.get("pdf_rect")
        if (type(page) is not int or not 20 <= page <= 956
                or not isinstance(bounds, list) or len(bounds) != 4
                or any(type(x) not in (int, float) for x in bounds)
                or not bounds[0] < bounds[2] or not bounds[1] < bounds[3]):
            raise ValueError("Invalid article image locator")
        crops[name] = row

    articles = rows_jsonl(root / "benchmark/complete_articles_first_pass.jsonl")
    if len(articles) != 2:
        raise ValueError("Phase 3 expects two first-pass complete article candidates")
    ids, pages = set(), set()
    for article in articles:
        ident = article.get("record_id")
        if (not isinstance(ident, str) or not ident or ident in ids
                or article.get("schema") != "gould-kolb.complete-article-first-pass.v1"
                or article.get("record_type") != "explanatory_article"):
            raise ValueError("Invalid or duplicate complete article candidate")
        ids.add(ident)
        page = article.get("source_pdf_page")
        crop = crops.get(article.get("evidence_crop"))
        if (crop is None or crop["page"] != page
                or article.get("evidence_pdf_bbox") != crop["pdf_rect"]
                or article.get("source_column") not in ("left", "right")):
            raise ValueError(f"{ident}: source locator mismatch")
        pages.add(page)
        if (article.get("article_text_completeness")
                != "complete_article_candidate_first_visual_pass"
                or article.get("transcription_status") != "first_visual_pass"
                or article.get("second_independent_pass") is not False
                or article.get("semantic_approval") is not False
                or article.get("related_target_ids_verified") != []):
            raise ValueError(f"{ident}: unsupported editorial/gold-standard claim")
        if article.get("page_continuation_observed") is not False:
            raise ValueError(f"{ident}: article continuation not independently checked")
        if not isinstance(article.get("article_boundary_basis"), str) or not article["article_boundary_basis"]:
            raise ValueError(f"{ident}: boundary reasoning missing")
        for field in ("headword_fa_first_pass", "headword_en_first_pass",
                      "next_visible_heading_first_pass",
                      "contributor_english_first_pass"):
            if not isinstance(article.get(field), str) or not article[field]:
                raise ValueError(f"{ident}: missing source-visible field {field}")
        sections = article.get("sections")
        if not isinstance(sections, list) or not sections:
            raise ValueError(f"{ident}: missing article sections")
        section_labels = [s.get("label") for s in sections]
        if section_labels not in ([None], ["A", "B"]):
            raise ValueError(f"{ident}: unsupported or invented source section structure")
        for section in sections:
            if not isinstance(section.get("text_first_pass"), str) or not section["text_first_pass"]:
                raise ValueError(f"{ident}: missing first-pass transcription")
        if (article.get("related_marker_first_pass") != "نیز"
                or not isinstance(article.get("related_expression_first_pass"), str)
                or not article["related_expression_first_pass"].startswith("نیز")):
            raise ValueError(f"{ident}: unverified related-entry source marker")
        if (article.get("contributor_fa_first_pass") is None and
                article.get("contributor_fa_review_status")
                != "illegible_or_uncertain_requires_human_review"):
            raise ValueError(f"{ident}: unknown contributor must remain unresolved")
        if not isinstance(article.get("uncertain_details"), list):
            raise ValueError(f"{ident}: missing uncertainty register")

    pilot = rows_jsonl(root / "benchmark/first_pass_v1.jsonl")
    pilot_by_id = {row["record_id"]: row for row in pilot}
    if len(pilot_by_id) != len(pilot) or len(pilot) != 11:
        raise ValueError("Original 11-record pilot changed or contains duplicate IDs")
    reviews = rows_jsonl(root / "benchmark/visual_recheck_log_v1.jsonl")
    if len(reviews) != 11:
        raise ValueError("Second visual pass log must address all 11 original records")
    reviewed = set()
    for review in reviews:
        ident = review.get("record_id")
        if ident in reviewed or ident not in pilot_by_id:
            raise ValueError("Duplicate or unknown review record ID")
        reviewed.add(ident)
        if (review.get("schema") != "gould-kolb.benchmark-visual-recheck.v1"
                or review.get("source_pdf_page") != pilot_by_id[ident]["source_pdf_page"]
                or review.get("visual_recheck_performed") is not True
                or review.get("reviewer_type") != "same_assistant_visual_comparison"
                or review.get("independent_human_review") is not False
                or review.get("second_independent_pass") is not False
                or review.get("review_decision") != "retain_provisional_not_gold"
                or review.get("verified_literal_source_text") is not False
                or review.get("transcription_patch_approved") is not None):
            raise ValueError(f"{ident}: unsupported independent review claim")
        if not review.get("review_note") or not review.get("issue_code"):
            raise ValueError(f"{ident}: review reasoning missing")

    original_pdf_verified = False
    crops_written = 0
    if evidence_dir is not None and pdf is None:
        raise ValueError("Cannot render source evidence without the registered PDF")
    if pdf is not None:
        pdf = Path(pdf)
        if (pdf.stat().st_size != source["source_pdf_bytes"]
                or pdf_sha(pdf) != source["source_pdf_sha256"]):
            raise ValueError("PDF hash/size does not match original source")
        import fitz
        d = fitz.open(pdf)
        if len(d) != source["physical_pages"]:
            raise ValueError("Source PDF physical page count mismatched")
        original_pdf_verified = True
        for c in crops.values():
            page = d[c["page"] - 1]
            rect = fitz.Rect(*c["pdf_rect"])
            if not page.rect.contains(rect):
                raise ValueError(f"Out-of-bounds original PDF crop: {c['file']}")
            if evidence_dir is not None:
                evidence_dir.mkdir(parents=True, exist_ok=True)
                page.get_pixmap(matrix=fitz.Matrix(3.5, 3.5),
                                clip=rect, alpha=False).save(evidence_dir / c["file"])
                crops_written += 1
        d.close()

    return {
        "schema": "gould-kolb.phase3-benchmark-validation.v1",
        "source_pdf_hash_checked_in_this_run": original_pdf_verified,
        "same_assistant_visual_rechecks": len(reviews),
        "independently_verified_rechecks": 0,
        "first_pass_complete_article_candidates": len(articles),
        "first_pass_source_pages": sorted(pages),
        "independently_verified_complete_articles": 0,
        "ground_truth_gold_records": 0,
        "source_image_crops_written": crops_written,
        "editorially_resolved_references": 0,
        "release_status": "provisional_awaiting_independent_image_review",
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
