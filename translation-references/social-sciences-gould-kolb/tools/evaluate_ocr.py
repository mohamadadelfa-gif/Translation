#!/usr/bin/env python3
"""Compare OCR/vision *structured candidates* against independently attested text.

Gold texts are accepted ONLY via existing review_gate.validate() with ALL
13 reviewed and no unresolved records. This tool does not run OCR and cannot
verify that the human attestation is truthful; a project editor must sign off
on the source-image review before interpreting metrics as genuine accuracy.

The primary CER is raw-Unicode-codepoint exact. NFC CER is diagnostic only.
WER splits on whitespace only; ZWNJ remains inside tokens. No transliteration,
Persian normalisation or spelling correction is applied to gold strings.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import unicodedata

from review_gate import ROOT, prepare, rows, validate


def distance(x, y):
    """Levenshtein distance for sequences, memory O(min(len(x),len(y)))."""
    if len(x) < len(y):
        x, y = y, x
    prev = list(range(len(y) + 1))
    for i, a in enumerate(x, 1):
        curr = [i]
        for j, b in enumerate(y, 1):
            curr.append(min(prev[j] + 1, curr[j - 1] + 1,
                            prev[j - 1] + (a != b)))
        prev = curr
    return prev[-1]


def field_class(key):
    if key.startswith("headword"):
        return "headword"
    if key.startswith("contributor"):
        return "contributor"
    if key.startswith("referral") or key.startswith("related"):
        return "reference_notation"
    if key in ("sections", "section_text_readable"):
        return "article_exposition"
    if key == "section_label":
        return "article_section_label"
    return "other"


def load_predictions(path, queue):
    by_id = {r["record_id"]: r for r in queue}
    preds = {}
    identity = None
    for row in rows(path):
        if row.get("schema") != "gould-kolb.ocr-structured-prediction.v1":
            raise ValueError("Unexpected prediction format")
        ident = row.get("record_id")
        if ident not in by_id or ident in preds:
            raise ValueError(f"Unknown or duplicated prediction ID: {ident}")
        origin = by_id[ident]
        if (row.get("source_pdf_sha256") != origin["source_pdf_sha256"]
                or row.get("source_pdf_page") != origin["source_pdf_page"]
                or row.get("source_column") != origin["source_column"]):
            raise ValueError(f"Source PDF provenance does not match: {ident}")
        engine, version = row.get("engine_id"), row.get("engine_version")
        if not isinstance(engine, str) or not engine.strip():
            raise ValueError(f"Missing OCR/vision engine identity: {ident}")
        if not isinstance(version, str) or not version.strip():
            raise ValueError(f"Missing OCR/vision engine version: {ident}")
        if identity is None:
            identity = (engine, version)
        elif identity != (engine, version):
            raise ValueError("Mixed OCR engines or versions: evaluate separately")
        fields = row.get("fields")
        if not isinstance(fields, dict):
            raise ValueError(f"Candidate fields must be an object: {ident}")
        unknown = set(fields) - set(origin["required_field_names"])
        if unknown:
            raise ValueError(f"Unexpected candidate field(s) at {ident}: {sorted(unknown)}")
        for name, value in fields.items():
            if name == "sections":
                if not isinstance(value, list):
                    raise ValueError(f"Expected section array in {ident}")
                for s in value:
                    if (not isinstance(s, dict) or set(s) != {"label", "text_first_pass"}
                            or s["label"] is not None and
                            not isinstance(s["label"], str)
                            or not isinstance(s["text_first_pass"], str)):
                        raise ValueError(f"Malformed candidate section in {ident}")
            elif value is not None and not isinstance(value, str):
                raise ValueError(f"Candidate value must be text, null or sections: {ident}")
        preds[ident] = fields
    if not preds:
        raise ValueError("No OCR predictions provided")
    return preds, identity


def add_text(reference, candidate, cls, metrics):
    """Score a strict literal text comparison; missing prediction is not ignored."""
    a = reference
    b = candidate if isinstance(candidate, str) else ""
    category = metrics[cls]
    category["fields_scored"] += 1
    category["reference_characters"] += len(a)
    category["character_edits"] += distance(a, b)
    category["reference_words"] += len(a.split())
    category["word_edits"] += distance(a.split(), b.split())
    category["nfc_character_edits"] += distance(
        unicodedata.normalize("NFC", a),
        unicodedata.normalize("NFC", b))
    category["nfc_reference_characters"] += len(unicodedata.normalize("NFC", a))
    if reference != candidate:
        category["nonidentical_fields"] += 1
    if candidate is None:
        category["unreturned_fields"] += 1


def evaluate(root, responses_path, predictions_path):
    queue, _ = prepare(root)
    # Reject EVERY attempt to evaluate against a partial or unapproved corpus.
    review_counts, gold = validate(root, responses_path, permit_partial=False)
    if len(gold) != len(queue) or review_counts["approved"] != len(queue):
        raise ValueError("Independent gold review incomplete")
    gold_by_id = {g["record_id"]: g for g in gold}
    preds, engine = load_predictions(predictions_path, queue)
    metrics = defaultdict(Counter)
    records = []
    total = Counter()
    for q in queue:
        ident = q["record_id"]
        expected = gold_by_id[ident]["approved_transcription"]
        predicted = preds.get(ident, {})
        per_record = defaultdict(Counter)
        rec = {"record_id": ident, "candidate_type": q["candidate_type"],
               "source_pdf_page": q["source_pdf_page"],
               "prediction_supplied": ident in preds, "fields": []}
        if ident not in preds:
            total["missing_entry_predictions"] += 1
        for key in q["required_field_names"]:
            cls = field_class(key)
            a = expected[key]
            b = predicted.get(key)
            if key not in predicted:
                total["missing_fields"] += 1
            if key == "sections":
                a_sections = a
                b_sections = b if isinstance(b, list) else []
                la = [x["label"] for x in a_sections]
                lb = [x["label"] for x in b_sections]
                if la != lb:
                    total["wrong_section_sequences"] += 1
                total["missing_sections"] += max(len(la)-len(lb), 0)
                total["extra_sections"] += max(len(lb)-len(la), 0)
                for i, section in enumerate(a_sections):
                    candidate_section = b_sections[i] if i < len(b_sections) else {}
                    add_text(section["text_first_pass"],
                             candidate_section.get("text_first_pass"),
                             cls, metrics)
                    add_text(section["text_first_pass"],
                             candidate_section.get("text_first_pass"),
                             cls, per_record)
                rec["fields"].append({
                    "name": "sections", "reference_labels": la,
                    "candidate_labels": lb, "labels_exact": la == lb})
                continue
            if a is None:
                if b is not None:
                    total["hallucinated_null_fields"] += 1
                    rec["fields"].append({"name": key, "status": "unexpected_nonempty_text"})
                else:
                    rec["fields"].append({"name": key, "status": "both_null"})
                continue
            add_text(a, b, cls, metrics)
            add_text(a, b, cls, per_record)
            rec["fields"].append({
                "name": key, "exact": a == b,
                "character_edits": distance(a, b if isinstance(b, str) else ""),
                "reference_characters": len(a)})
            if key in ("referral_marker", "related_expression_first_pass",
                       "referral_target_fa_readable") and a != b:
                total["reference_field_mismatches"] += 1
            if key == "section_label" and a != b:
                total["section_label_mismatches"] += 1
        rec["strict_metrics"] = {
            kind: {"character_edits": m["character_edits"],
                   "reference_characters": m["reference_characters"],
                   "CER": m["character_edits"] / m["reference_characters"]
                   if m["reference_characters"] else None}
            for kind, m in per_record.items()
        }
        records.append(rec)

    summary = {}
    for cls, m in sorted(metrics.items()):
        summary[cls] = {
            **dict(m),
            "CER": m["character_edits"] / m["reference_characters"]
                   if m["reference_characters"] else None,
            "WER": m["word_edits"] / m["reference_words"]
                   if m["reference_words"] else None,
            "NFC_CER_diagnostic_only":
                m["nfc_character_edits"] / m["nfc_reference_characters"]
                if m["nfc_reference_characters"] else None,
        }
    char_denominator = sum(m["reference_characters"] for m in metrics.values())
    word_denominator = sum(m["reference_words"] for m in metrics.values())
    report = {
        "schema": "gould-kolb.ocr-benchmark-report.v1",
        "benchmark_scope": "independently_attested_13_structured_entries_only",
        "gold_reference_basis":
            "review_gate_approved_attested_external_review_requires_editor_signoff",
        "no_pdf_or_page_image_verified_during_scoring": True,
        "ocr_engine_id": engine[0],
        "ocr_engine_version": engine[1],
        "gold_records": len(gold),
        "predicted_records": len(preds),
        "strict_character_error_rate":
            sum(m["character_edits"] for m in metrics.values()) /
            char_denominator if char_denominator else None,
        "strict_word_error_rate":
            sum(m["word_edits"] for m in metrics.values()) /
            word_denominator if word_denominator else None,
        "per_field_class": summary,
        "structural_errors": dict(total),
        "limitations": [
            "Measures extracted structured fields, not raw whole-page reading order",
            "CER uses Unicode codepoints, not grapheme clusters",
            "WER uses whitespace splitting; ZWNJ is preserved, punctuation retained",
            "NFC error rates are diagnostic; source transcription is never rewritten",
            "Independent reviewer identity and factual correctness cannot be proven by code",
            "This report must not be used before editor checks external review responses",
        ],
    }
    return report, records


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--review-responses", type=Path, required=True)
    p.add_argument("--predictions", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--per-record", type=Path, required=True)
    args = p.parse_args()
    report, records = evaluate(args.root, args.review_responses, args.predictions)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.per_record.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    args.per_record.write_text(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in records),
        encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
