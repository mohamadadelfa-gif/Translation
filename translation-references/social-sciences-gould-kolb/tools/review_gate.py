#!/usr/bin/env python3
"""Prepare and validate independent image-review records for Gould/Kolb.

Do not equate a passed machine check with accurate transcription or
an independently completed review. No record is promoted by default.
No original Persian text or canonical source PDF is modified.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    "checked_headword_and_original_language",
    "checked_all_persian_characters",
    "checked_punctuation_and_zwnj",
    "checked_column_and_article_boundaries",
    "checked_section_letters_and_order",
    "checked_reference_marker_and_target",
    "checked_contributor_and_credit",
)
FIELDS_REFERRAL = (
    "headword_fa_readable", "headword_en_readable",
    "referral_marker", "referral_target_fa_readable",
)
FIELDS_A_SECTION = (
    "headword_fa_readable", "headword_en_readable",
    "section_label", "section_text_readable",
)
FIELDS_ARTICLE = (
    "headword_fa_first_pass", "headword_en_first_pass",
    "sections", "related_expression_first_pass",
    "contributor_english_first_pass", "contributor_fa_first_pass",
)


def rows(path: Path):
    result = []
    with path.open(encoding="utf-8") as inp:
        for number, line in enumerate(inp, 1):
            if not line.strip():
                raise ValueError(f"Blank line in {path} at {number}")
            result.append(json.loads(line))
    return result


def digest(record):
    """Content-address the first-pass candidate to catch stale review forms."""
    data = json.dumps(record, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def type_and_fields(record):
    if record["record_type"] == "complete_referral":
        return "complete_referral", FIELDS_REFERRAL
    if record["record_type"] == "article_section_excerpt":
        return "A_section_only", FIELDS_A_SECTION
    if record["record_type"] == "explanatory_article":
        return "complete_article_candidate", FIELDS_ARTICLE
    raise ValueError("Unknown first-pass kind")


def base_candidates(root=ROOT):
    paths = [root / "benchmark/first_pass_v1.jsonl",
             root / "benchmark/complete_articles_first_pass.jsonl"]
    records = [r for path in paths for r in rows(path)]
    seen = set()
    for r in records:
        if r["record_id"] in seen:
            raise ValueError("Duplicate base entry ID")
        seen.add(r["record_id"])
    if len(records) != 13:
        raise ValueError(f"Expected 13 existing candidates; got {len(records)}")
    return records


def image_manifest(root):
    first = json.loads((root / "benchmark/visual_evidence_manifest.json").read_text(encoding="utf-8"))
    second = json.loads((root / "benchmark/complete_article_evidence.json").read_text(encoding="utf-8"))
    locators = {}
    for c in first["crops"]:
        locators[c["file"]] = c["page"]
    for c in second["evidence_regions"]:
        if c["file"] in locators:
            raise ValueError("Duplicate image evidence filename")
        locators[c["file"]] = c["page"]
    return locators


def baseline_transcription(record, fields):
    return {key: record.get(key) for key in fields}


def prepare(root=ROOT):
    source = json.loads((root / "source_manifest.json").read_text(encoding="utf-8"))
    locators = image_manifest(root)
    queue, drafts = [], []
    for r in base_candidates(root):
        kind, keys = type_and_fields(r)
        img = r["evidence_crop"]
        page = r["source_pdf_page"]
        if img not in locators or locators[img] != page:
            raise ValueError(f"{r['record_id']}: source crop does not match original page")
        row = {
            "schema": "gould-kolb.independent-review.v1",
            "record_id": r["record_id"],
            "candidate_type": kind,
            "source_pdf_sha256": source["source_pdf_sha256"],
            "source_pdf_page": page,
            "source_column": r["source_column"],
            "evidence_crop": img,
            "first_pass_sha256": digest(r),
            "first_pass_transcription": baseline_transcription(r, keys),
            "required_field_names": list(keys),
            "required_image_checks": list(CHECKS),
        }
        queue.append(row)
        drafts.append({
            "schema": "gould-kolb.independent-review-response.v1",
            "record_id": r["record_id"],
            "first_pass_sha256": digest(r),
            "reviewer_id": None,
            "reviewed_at": None,
            "reviewed_original_page_and_crop": False,
            "not_original_transcriber_attested": False,
            "decision": "pending",
            "image_checks": {key: False for key in CHECKS},
            "approved_transcription": None,
            "correction_notes": None,
            "unresolved_details": [],
        })
    return queue, drafts


def save_jsonl(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in data),
                    encoding="utf-8")


def validate(root, response_path, *, permit_partial=True):
    queue, _ = prepare(root)
    by_id = {item["record_id"]: item for item in queue}
    responses = rows(response_path)
    seen = set()
    approved = []
    breakdown = {"pending": 0, "approved": 0, "needs_changes": 0, "unresolved": 0}
    for r in responses:
        ident = r.get("record_id")
        if ident not in by_id or ident in seen:
            raise ValueError(f"Unknown/duplicate review record {ident}")
        seen.add(ident)
        q = by_id[ident]
        if (r.get("schema") != "gould-kolb.independent-review-response.v1"
                or r.get("first_pass_sha256") != q["first_pass_sha256"]):
            raise ValueError(f"{ident}: stale review form or invalid schema")
        status = r.get("decision")
        if status not in breakdown:
            raise ValueError(f"{ident}: invalid review decision")
        breakdown[status] += 1
        if status == "pending":
            if r.get("approved_transcription") is not None:
                raise ValueError(f"{ident}: pending review already claims approval")
            continue
        reviewer = r.get("reviewer_id")
        if (not isinstance(reviewer, str) or not reviewer.strip()
                or reviewer.strip().casefold() in (
                    "assistant", "chatgpt", "same_assistant_visual_comparison",
                    "assistant_first_visual_pass", "openai", "automated")):
            raise ValueError(f"{ident}: named separate reviewer is required")
        stamp = r.get("reviewed_at")
        try:
            dt = datetime.fromisoformat(stamp)
        except (ValueError, TypeError):
            raise ValueError(f"{ident}: ISO review datetime required")
        if dt.tzinfo is None:
            raise ValueError(f"{ident}: timezone-aware review date required")
        if (r.get("reviewed_original_page_and_crop") is not True
                or r.get("not_original_transcriber_attested") is not True):
            raise ValueError(f"{ident}: independent source-page review attestation missing")
        checks = r.get("image_checks")
        if not isinstance(checks, dict) or set(checks) != set(CHECKS):
            raise ValueError(f"{ident}: incomplete image review checklist")
        if status == "approved":
            if not all(checks.values()) or any(type(x) is not bool for x in checks.values()):
                raise ValueError(f"{ident}: all image checks must pass")
            source_text = r.get("approved_transcription")
            if not isinstance(source_text, dict) or set(source_text) != set(q["required_field_names"]):
                raise ValueError(f"{ident}: reviewer must supply every literal source field")
            for k, value in source_text.items():
                if k == "sections":
                    if (not isinstance(value, list) or not value or
                            any(not isinstance(s, dict) or
                                not isinstance(s.get("text_first_pass"), str) or
                                not s["text_first_pass"] for s in value)):
                        raise ValueError(f"{ident}: source section text missing")
                elif value is not None and (not isinstance(value, str) or not value.strip()):
                    raise ValueError(f"{ident}: invalid verified text in {k}")
            if r.get("unresolved_details"):
                raise ValueError(f"{ident}: unresolved ambiguities bar approval")
            approved.append({
                "schema": "gould-kolb.independent-gold.v1",
                "record_id": ident,
                "candidate_type": q["candidate_type"],
                "source_pdf_sha256": q["source_pdf_sha256"],
                "source_pdf_page": q["source_pdf_page"],
                "source_column": q["source_column"],
                "evidence_crop": q["evidence_crop"],
                "first_pass_sha256": q["first_pass_sha256"],
                "reviewer_id": reviewer,
                "reviewed_at": stamp,
                "approved_transcription": source_text,
                "correction_notes": r.get("correction_notes"),
                "approval_basis": "separate_reviewer_image_attestation_not_automated_visual_proof",
            })
        elif r.get("approved_transcription") is not None:
            raise ValueError(f"{ident}: unapproved record carries approved transcription")
    missing = set(by_id) - seen
    if missing:
        raise ValueError(f"Missing reviews for IDs {sorted(missing)}")
    if not permit_partial and breakdown["approved"] != len(queue):
        raise ValueError("All 13 records must be independently approved for full benchmark")
    return breakdown, approved


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--queue", type=Path, required=True)
    p.add_argument("--response-template", type=Path, required=True)
    p.add_argument("--responses", type=Path,
                   help="Optional completed independent review responses to validate")
    p.add_argument("--promote", type=Path,
                   help="Optional gold JSONL output; requires all 13 approved responses")
    args = p.parse_args()
    queue, forms = prepare(args.root)
    save_jsonl(args.queue, queue)
    save_jsonl(args.response_template, forms)
    result = {"queued": len(queue), "pending": len(queue),
              "approved": 0, "gold_promotion": "not_attempted"}
    if args.promote and not args.responses:
        raise ValueError("--promote requires --responses")
    if args.responses:
        breakdown, approved = validate(args.root, args.responses,
                                       permit_partial=args.promote is None)
        result = {"queued": len(queue), **breakdown,
                  "gold_promotion": "not_attempted"}
        if args.promote:
            if len(approved) != len(queue):
                raise ValueError("Incomplete gold-standard approval")
            save_jsonl(args.promote, approved)
            result["gold_promotion"] = "approved_by_attested_external_review"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
