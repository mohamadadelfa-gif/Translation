"""Phase 3 controls: provisional transcription must not be called gold standard."""
from __future__ import annotations
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_phase3 import ROOT, validate


class Phase3Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "benchmark").mkdir()
        for path in (
            "source_manifest.json",
            "benchmark/first_pass_v1.jsonl",
            "benchmark/complete_articles_first_pass.jsonl",
            "benchmark/visual_recheck_log_v1.jsonl",
            "benchmark/complete_article_evidence.json",
        ):
            shutil.copy2(ROOT / path, self.root / path)

    def read_rows(self, file):
        path = self.root / "benchmark" / file
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def write_rows(self, file, rows):
        path = self.root / "benchmark" / file
        path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n"
                                for row in rows), encoding="utf-8")

    def test_benchmark_counts_and_explicit_incomplete_review_status(self):
        result = validate(self.root)
        self.assertEqual(result["same_assistant_visual_rechecks"], 11)
        self.assertEqual(result["first_pass_complete_article_candidates"], 2)
        self.assertEqual(result["first_pass_source_pages"], [54, 96])
        self.assertEqual(result["independently_verified_complete_articles"], 0)
        self.assertEqual(result["ground_truth_gold_records"], 0)
        self.assertFalse(result["source_pdf_hash_checked_in_this_run"])

    def test_distinguishes_one_section_and_A_B_article(self):
        rows = self.read_rows("complete_articles_first_pass.jsonl")
        self.assertEqual([s["label"] for s in rows[0]["sections"]], [None])
        self.assertEqual([s["label"] for s in rows[1]["sections"]], ["A", "B"])
        self.assertEqual(rows[0]["headword_en_first_pass"], "spirit mediumship")
        self.assertEqual(rows[1]["headword_en_first_pass"], "natural increase")
        self.assertTrue(all(row["related_marker_first_pass"] == "نیز" for row in rows))

    def test_premature_gold_approval_rejected(self):
        rows = self.read_rows("complete_articles_first_pass.jsonl")
        rows[0]["second_independent_pass"] = True
        self.write_rows("complete_articles_first_pass.jsonl", rows)
        with self.assertRaisesRegex(ValueError, "unsupported editorial/gold-standard"):
            validate(self.root)

    def test_fabricated_source_section_rejected(self):
        rows = self.read_rows("complete_articles_first_pass.jsonl")
        rows[0]["sections"].append({"label": "B", "text_first_pass": "invented"})
        self.write_rows("complete_articles_first_pass.jsonl", rows)
        with self.assertRaisesRegex(ValueError, "unsupported or invented"):
            validate(self.root)

    def test_missing_review_rejected(self):
        rows = self.read_rows("visual_recheck_log_v1.jsonl")
        self.write_rows("visual_recheck_log_v1.jsonl", rows[:-1])
        with self.assertRaisesRegex(ValueError, "all 11"):
            validate(self.root)

    def test_false_independent_review_rejected(self):
        rows = self.read_rows("visual_recheck_log_v1.jsonl")
        rows[0]["independent_human_review"] = True
        self.write_rows("visual_recheck_log_v1.jsonl", rows)
        with self.assertRaisesRegex(ValueError, "unsupported independent review claim"):
            validate(self.root)

    def test_wrong_page_crop_rejected(self):
        rows = self.read_rows("complete_articles_first_pass.jsonl")
        rows[1]["source_pdf_page"] = 95
        self.write_rows("complete_articles_first_pass.jsonl", rows)
        with self.assertRaisesRegex(ValueError, "source locator mismatch"):
            validate(self.root)

    def test_false_reference_resolution_rejected(self):
        rows = self.read_rows("complete_articles_first_pass.jsonl")
        rows[1]["related_target_ids_verified"] = ["invented-id"]
        self.write_rows("complete_articles_first_pass.jsonl", rows)
        with self.assertRaisesRegex(ValueError, "unsupported editorial/gold-standard"):
            validate(self.root)

    def test_source_image_requires_original_pdf(self):
        with self.assertRaisesRegex(ValueError, "Cannot render source evidence"):
            validate(self.root, evidence_dir=self.root / "rendered")

    def test_wrong_source_pdf_rejected(self):
        pdf = self.root / "unrelated.pdf"
        pdf.write_bytes(b"not the original scanned dictionary")
        with self.assertRaisesRegex(ValueError, "PDF hash/size"):
            validate(self.root, pdf=pdf)

    def test_contributor_uncertainty_must_be_explicit(self):
        rows = self.read_rows("complete_articles_first_pass.jsonl")
        rows[0]["contributor_fa_review_status"] = "verified"
        self.write_rows("complete_articles_first_pass.jsonl", rows)
        with self.assertRaisesRegex(ValueError, "unknown contributor"):
            validate(self.root)


if __name__ == "__main__":
    unittest.main()
