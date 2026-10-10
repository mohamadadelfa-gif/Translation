"""Protect the first-pass scanned-dictionary benchmark against overclaims."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from validate_benchmark import ROOT, validate


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "benchmark").mkdir()
        for path in ("source_manifest.json", "benchmark/first_pass_v1.jsonl",
                     "benchmark/visual_evidence_manifest.json"):
            shutil.copy2(ROOT / path, self.root / path)

    def rows(self):
        file = self.root / "benchmark/first_pass_v1.jsonl"
        return file, [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()]

    def replace_rows(self, rows):
        file = self.root / "benchmark/first_pass_v1.jsonl"
        file.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                        encoding="utf-8")

    def test_first_pass_without_pdf_does_not_claim_image_verification(self):
        report = validate(self.root)
        self.assertFalse(report["source_pdf_hash_checked_this_run"])
        self.assertEqual(report["complete_referrals_transcribed_first_pass"], 9)
        self.assertEqual(report["individual_A_sections_transcribed_first_pass"], 2)
        self.assertEqual(report["full_explanatory_articles_verified"], 0)
        self.assertEqual(report["independently_second_pass_reviewed"], 0)
        self.assertEqual(report["semantic_references_resolved"], 0)

    def test_two_adab_entries_must_remain_separate(self):
        _, records = self.rows()
        adab = [r for r in records if r["headword_fa_readable"] == "آداب"]
        self.assertEqual(len(adab), 2)
        self.assertEqual({r["headword_en_readable"] for r in adab}, {"mores", "rite"})
        self.assertEqual({r["referral_target_fa_readable"] for r in adab},
                         {"شیوه‌های عامیانه", "مراسم و آیین"})

    def test_referral_cannot_be_mislabeled_as_article(self):
        _, records = self.rows()
        records[0]["entry_completeness"] = "complete_explanatory_article"
        self.replace_rows(records)
        with self.assertRaisesRegex(ValueError, "Referral wrongly modeled"):
            validate(self.root)

    def test_excerpt_cannot_be_promoted_to_full_article(self):
        _, records = self.rows()
        excerpt = next(r for r in records if r["record_type"] == "article_section_excerpt")
        excerpt["entry_completeness"] = "complete_explanatory_article"
        self.replace_rows(records)
        with self.assertRaisesRegex(ValueError, "Unverified full-article"):
            validate(self.root)

    def test_fake_second_pass_rejected(self):
        _, records = self.rows()
        records[0]["second_independent_pass"] = True
        self.replace_rows(records)
        with self.assertRaisesRegex(ValueError, "Unjustified verification"):
            validate(self.root)

    def test_unverified_semantic_target_rejected(self):
        _, records = self.rows()
        records[0]["authoritative_semantic_target_id"] = "invented-target"
        self.replace_rows(records)
        with self.assertRaisesRegex(ValueError, "Unjustified verification"):
            validate(self.root)

    def test_wrong_crop_page_rejected(self):
        _, records = self.rows()
        records[0]["source_pdf_page"] = 23
        self.replace_rows(records)
        with self.assertRaisesRegex(ValueError, "image-backed PDF locator"):
            validate(self.root)

    def test_duplicate_record_id_rejected(self):
        _, records = self.rows()
        records[1]["record_id"] = records[0]["record_id"]
        self.replace_rows(records)
        with self.assertRaisesRegex(ValueError, "duplicate record ID"):
            validate(self.root)

    def test_fake_source_pdf_rejected(self):
        pdf = self.root / "other.pdf"
        pdf.write_bytes(b"wrong file, not the PDF")
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate(self.root, pdf=pdf)

    def test_evidence_cannot_be_rendered_without_source_pdf(self):
        with self.assertRaisesRegex(ValueError, "without --pdf"):
            validate(self.root, evidence_dir=self.root / "evidence")


if __name__ == "__main__":
    unittest.main()
