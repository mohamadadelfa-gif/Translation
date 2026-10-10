"""Synthetic-only tests of OCR score computation and independent-review gate.

These fixture approvals are FICTIONAL software tests; never use them to
represent human reviews of the original dictionary.
"""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
import shutil
import tempfile
import unittest

from evaluate_ocr import evaluate, distance, load_predictions
from review_gate import ROOT, prepare, CHECKS, save_jsonl


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "benchmark").mkdir()
        for name in (
            "source_manifest.json",
            "benchmark/first_pass_v1.jsonl",
            "benchmark/complete_articles_first_pass.jsonl",
            "benchmark/visual_evidence_manifest.json",
            "benchmark/complete_article_evidence.json",
        ):
            shutil.copy2(ROOT / name, self.root / name)
        self.queue, self.forms = prepare(self.root)
        self.review = self.root / "fixture-only-not-real-reviews.jsonl"
        self.prediction = self.root / "synthetic-predictions.jsonl"
        self.signoff = self.root / "synthetic-editor-signoff.json"
        save_jsonl(self.review, self.forms)
        self.predictions = []
        for q in self.queue:
            self.predictions.append({
                "schema": "gould-kolb.ocr-structured-prediction.v1",
                "record_id": q["record_id"],
                "submission_status": "actual_model_output",
                "source_pdf_sha256": q["source_pdf_sha256"],
                "source_pdf_page": q["source_pdf_page"],
                "source_column": q["source_column"],
                "engine_id": "synthetic-test-engine-NOT-real-OCR",
                "engine_version": "fixture-v1",
                "fields": json.loads(json.dumps(q["first_pass_transcription"],
                                                ensure_ascii=False)),
            })
        save_jsonl(self.prediction, self.predictions)

    def approve_fixture_only(self):
        for q, r, pred in zip(self.queue, self.forms, self.predictions):
            fields = json.loads(json.dumps(q["first_pass_transcription"],
                                           ensure_ascii=False))
            if (q["candidate_type"] == "complete_article_candidate"
                    and fields["contributor_fa_first_pass"] is None):
                # Invented text for synthetic software testing ONLY.
                fields["contributor_fa_first_pass"] = "نام ساختگی فقط در آزمون"
            r.update({
                "reviewer_id": "FICTIONAL_TEST_FIXTURE_DO_NOT_USE_AS_REVIEW",
                "reviewed_at": "2026-10-10T15:00:00+00:00",
                "reviewed_original_page_and_crop": True,
                "not_original_transcriber_attested": True,
                "decision": "approved",
                "image_checks": {key: True for key in CHECKS},
                "approved_transcription": fields,
                "correction_notes": "Synthetic fixture, not actually read from PDF.",
                "unresolved_details": [],
            })
            pred["fields"] = json.loads(json.dumps(fields, ensure_ascii=False))
        save_jsonl(self.review, self.forms)
        save_jsonl(self.prediction, self.predictions)
        self.signoff.write_text(json.dumps({
            "schema": "gould-kolb.ocr-editor-signoff.v1",
            "review_responses_sha256": hashlib.sha256(self.review.read_bytes()).hexdigest(),
            "reviewed_record_count": 13,
            "reviewed_all_independent_attestations": True,
            "confirmed_source_images_reviewed_by_separate_reviewer": True,
            "approved_for_ocr_benchmark": True,
            "editor_id": "FICTIONAL_PROJECT_EDITOR_IN_TEST_FIXTURE",
            "signed_at": "2026-10-10T15:30:00+00:00"
        }), encoding="utf-8")

    def test_distance_exact_insert_remove(self):
        self.assertEqual(distance("فرهنگ", "فرهنگ"), 0)
        self.assertEqual(distance("فرهنگ", "فرهن"), 1)
        self.assertEqual(distance("فرهنگ", "فرهنگی"), 1)
        self.assertEqual(distance("کتاب".split(), "کتاب‌ها".split()), 1)

    def test_unreviewed_provisional_corpus_cannot_be_scored(self):
        with self.assertRaisesRegex(ValueError, "All 13"):
            evaluate(self.root, self.review, self.prediction, self.signoff)

    def test_synthetic_approved_fixture_scores_zero(self):
        self.approve_fixture_only()
        result, records = evaluate(self.root, self.review, self.prediction, self.signoff)
        self.assertEqual(result["gold_records"], 13)
        self.assertEqual(result["predicted_records"], 13)
        self.assertEqual(len(records), 13)
        self.assertEqual(result["strict_character_error_rate"], 0)
        self.assertEqual(result["strict_word_error_rate"], 0)
        self.assertEqual(result["structural_errors"], {})
        self.assertTrue(result["no_pdf_or_page_image_verified_during_scoring"])

    def test_source_character_change_is_counted(self):
        self.approve_fixture_only()
        first = self.predictions[0]["fields"]
        first["headword_fa_readable"] = first["headword_fa_readable"] + "ا"
        save_jsonl(self.prediction, self.predictions)
        result, _ = evaluate(self.root, self.review, self.prediction, self.signoff)
        self.assertGreater(result["strict_character_error_rate"], 0)
        self.assertGreater(result["per_field_class"]["headword"]["character_edits"], 0)

    def test_missing_prediction_is_penalized(self):
        self.approve_fixture_only()
        self.predictions.pop(0)
        save_jsonl(self.prediction, self.predictions)
        report, records = evaluate(self.root, self.review, self.prediction, self.signoff)
        self.assertEqual(report["structural_errors"]["missing_entry_predictions"], 1)
        self.assertGreater(report["strict_character_error_rate"], 0)
        self.assertFalse(records[0]["prediction_supplied"])

    def test_section_label_mismatch_is_reported(self):
        self.approve_fixture_only()
        full = next(x for x in self.predictions
                    if x["record_id"] == "gk-article-p096-natural-increase")
        full["fields"]["sections"][0]["label"] = "C"
        save_jsonl(self.prediction, self.predictions)
        report, _ = evaluate(self.root, self.review, self.prediction, self.signoff)
        self.assertEqual(report["structural_errors"]["wrong_section_sequences"], 1)

    def test_nfc_is_only_diagnostic(self):
        self.approve_fixture_only()
        first = self.predictions[0]["fields"]
        first["headword_fa_readable"] = first["headword_fa_readable"] + "\u0627\u0654"
        save_jsonl(self.prediction, self.predictions)
        report, _ = evaluate(self.root, self.review, self.prediction, self.signoff)
        self.assertGreater(report["strict_character_error_rate"], 0)
        self.assertIn("NFC_CER_diagnostic_only",
                      report["per_field_class"]["headword"])

    def test_hallucinated_nonexistent_english_is_reported(self):
        self.approve_fixture_only()
        item = next(x for x in self.predictions
                    if x["record_id"] == "gk-gt-p032-psychopathology")
        item["fields"]["headword_en_readable"] = "invented"
        save_jsonl(self.prediction, self.predictions)
        result, _ = evaluate(self.root, self.review, self.prediction, self.signoff)
        self.assertEqual(result["structural_errors"]["hallucinated_null_fields"], 1)

    def test_wrong_pdf_hash_is_rejected(self):
        self.approve_fixture_only()
        self.predictions[0]["source_pdf_sha256"] = "0" * 64
        save_jsonl(self.prediction, self.predictions)
        with self.assertRaisesRegex(ValueError, "PDF provenance"):
            evaluate(self.root, self.review, self.prediction, self.signoff)

    def test_mixed_engine_is_rejected(self):
        self.approve_fixture_only()
        self.predictions[3]["engine_id"] = "another-engine"
        save_jsonl(self.prediction, self.predictions)
        with self.assertRaisesRegex(ValueError, "Mixed OCR engines"):
            evaluate(self.root, self.review, self.prediction, self.signoff)

    def test_unexpected_field_is_rejected(self):
        self.approve_fixture_only()
        self.predictions[0]["fields"]["invented_annotation"] = "wrong"
        save_jsonl(self.prediction, self.predictions)
        with self.assertRaisesRegex(ValueError, "Unexpected candidate field"):
            evaluate(self.root, self.review, self.prediction, self.signoff)

    def test_same_assistant_cannot_mark_corpus_approved(self):
        self.approve_fixture_only()
        self.forms[0]["reviewer_id"] = "chatgpt"
        save_jsonl(self.review, self.forms)
        with self.assertRaisesRegex(ValueError, "separate reviewer"):
            evaluate(self.root, self.review, self.prediction, self.signoff)

    def test_unsolved_credit_blocks_gold_and_evaluation(self):
        self.approve_fixture_only()
        item = next(x for x in self.forms
                    if x["record_id"] == "gk-article-p054-spirit-mediumship")
        item["approved_transcription"]["contributor_fa_first_pass"] = None
        save_jsonl(self.review, self.forms)
        with self.assertRaisesRegex(ValueError, "unresolved contributor"):
            evaluate(self.root, self.review, self.prediction, self.signoff)


    def test_missing_editor_signoff_prevents_scoring(self):
        self.approve_fixture_only()
        with self.assertRaisesRegex(ValueError, "Editor signoff required"):
            evaluate(self.root, self.review, self.prediction)

    def test_stale_editor_signoff_prevents_scoring(self):
        self.approve_fixture_only()
        data = json.loads(self.signoff.read_text(encoding="utf-8"))
        data["review_responses_sha256"] = "0" * 64
        self.signoff.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not bound"):
            evaluate(self.root, self.review, self.prediction, self.signoff)

    def test_editor_is_distinct_from_reviewer(self):
        self.approve_fixture_only()
        data = json.loads(self.signoff.read_text(encoding="utf-8"))
        data["editor_id"] = "FICTIONAL_TEST_FIXTURE_DO_NOT_USE_AS_REVIEW"
        self.signoff.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Separate named project editor"):
            evaluate(self.root, self.review, self.prediction, self.signoff)

    def test_unfilled_ocr_template_rejected(self):
        self.approve_fixture_only()
        self.predictions[0]["submission_status"] = "unfilled_template"
        save_jsonl(self.prediction, self.predictions)
        with self.assertRaisesRegex(ValueError, "model outputs"):
            evaluate(self.root, self.review, self.prediction, self.signoff)


if __name__ == "__main__":
    unittest.main()
