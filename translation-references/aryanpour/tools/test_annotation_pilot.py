"""Phase 3 pilot tests: genuine surface examples plus synthetic integration."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from build_annotation_pilot import (
    observations, build, search_key, abbreviation_key, GROUPS,
)


class ObservationTests(unittest.TestCase):
    def test_reference_target_is_candidate_only(self):
        record = {"id": 34, "english": "abaxial",
                  "persian": "(=abaxile) (گ . ش.) دورازمحور.",
                  "source_character_issue": False}
        candidates, groups = observations(record, {"abaxial": [34], "abaxile": [35]})
        self.assertEqual(len(candidates), 2)
        self.assertEqual(candidates[0]["target_exact_lookup_ids"], [35])
        self.assertEqual(candidates[0]["target_lookup_status"], "unique_exact_text_match")
        self.assertIsNone(candidates[0]["verified_cross_reference"])
        self.assertEqual(candidates[1]["abbreviation_form_key"], "گ.ش.")
        self.assertIsNone(candidates[1]["verified_label"])
        self.assertIn("leading_equals", groups)
        self.assertIn("abbreviation_form", groups)
        for item in candidates:
            start, end = item["span"]
            self.assertEqual(record["persian"][start:end], item["source_text"])

    def test_missing_target_is_not_invented(self):
        record = {"id": 1, "english": "a",
                  "persian": "(=not-in-dictionary) الف",
                  "source_character_issue": False}
        found, _ = observations(record, {"a": [1]})
        self.assertEqual(found[0]["target_exact_lookup_ids"], [])
        self.assertEqual(found[0]["target_lookup_status"], "not_found")

    def test_ambiguous_exact_target_preserved(self):
        record = {"id": 1, "english": "a", "persian": "(=duplicate) الف",
                  "source_character_issue": False}
        found, _ = observations(record, {"a": [1], "duplicate": [3, 4]})
        self.assertEqual(found[0]["target_exact_lookup_ids"], [3, 4])
        self.assertEqual(found[0]["target_lookup_status"], "multiple_exact_text_matches")

    def test_plain_parenthesis_is_not_verified_label(self):
        item = {"id": 3, "english": "a la carte",
                "persian": "(در مورد کاغذ) جداجدا سفارش داده  شده .",
                "source_character_issue": False}
        candidates, groups = observations(item, {"a la carte": [3]})
        self.assertEqual(candidates[0]["candidate_type"], "other_leading_parenthetical")
        self.assertIsNone(candidates[0]["verified_semantic_role"])
        self.assertIn("other_leading_parenthetical", groups)

    def test_unknown_short_parenthesis_not_pseudo_abbreviation(self):
        item = {"id": 1, "english": "a", "persian": "(هابیل) الف",
                "source_character_issue": False}
        candidates, _ = observations(item, {"a": [1]})
        self.assertEqual(candidates[0]["candidate_type"], "other_leading_parenthetical")

    def test_embedded_parentheses_unresolved(self):
        item = {"id": 19758, "english": "history",
                "persian": "تاریخ، سابقه ، ( طب ) بیمارنامه .",
                "source_character_issue": False}
        candidates, groups = observations(item, {"history": [19758]})
        self.assertEqual(candidates[0]["candidate_type"], "embedded_parenthetical")
        self.assertIn("embedded_parenthetical", groups)

    def test_commas_do_not_create_senses(self):
        item = {"id": 9674, "english": "culture",
                "persian": "برز، فرهنگ ، پرورش، تمدن .",
                "source_character_issue": False}
        candidates, groups = observations(item, {"culture": [9674]})
        self.assertEqual(candidates, [])
        self.assertIn("multi_comma_unsegmented", groups)

    def test_unusual_headword_detection(self):
        item = {"id": 1, "english": "s " + chr(96) + "words" + chr(96),
                "persian": "شمشیر زن", "source_character_issue": False}
        _, groups = observations(item, {search_key(item["english"]): [1]})
        self.assertIn("unusual_headword", groups)

    def test_duplicate_headwords_not_merged(self):
        item = {"id": 1, "english": "a", "persian": "الف",
                "source_character_issue": False}
        _, groups = observations(item, {"a": [1, 2]})
        self.assertIn("duplicate_headword", groups)

    def test_search_normalization_never_rewrites_source(self):
        text = "  A   B "
        self.assertEqual(search_key(text), "a b")
        self.assertEqual(text, "  A   B ")
        self.assertEqual(abbreviation_key(" ج . ش. "), "ج.ش.")


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.records = [
            {"id": 1, "english": "abaxial", "persian": "(=abaxile) (گ . ش.) دورازمحور.",
             "original_definition_markup": "<C>(=abaxile) (گ . ش.) دورازمحور.</C>",
             "source_character_issue": False},
            {"id": 2, "english": "abaxile", "persian": "(=abaxial) دورازمحور.",
             "original_definition_markup": "<C>(=abaxial) دورازمحور.</C>",
             "source_character_issue": False},
            {"id": 3, "english": "culture", "persian": "برز، فرهنگ ، پرورش، تمدن .",
             "original_definition_markup": "<C>برز، فرهنگ ، پرورش، تمدن .</C>",
             "source_character_issue": False},
            {"id": 4, "english": "apostle", "persian": "پیغ�مبر",
             "original_definition_markup": "<C>پیغ�مبر</C>",
             "source_character_issue": True},
        ]
        (self.root / "aryanpour-english-persian.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in self.records),
            encoding="utf-8")
        (self.root / "index").mkdir()
        with (self.root / "index/headwords-master.csv").open(
            "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["headword", "normalized_headword", "entry_id",
                             "file", "anchor", "source_character_issue"])
            for row in self.records:
                writer.writerow([row["english"], search_key(row["english"]),
                                 row["id"], "dictionary/A/A-01.md",
                                 f"entry-{row['id']}", str(row["source_character_issue"]).lower()])
        (self.root / "pilot").mkdir()
        self.reviews = self.root / "pilot/reviewed_surfaces.jsonl"
        self.reviews.write_text(
            json.dumps({
                "canonical_id": 1, "headword": "abaxial",
                "source_field": "persian", "observed_surface": "(=abaxile)",
                "review_scope": "ld2_export_surface_only",
                "semantic_interpretation_status": "not_verified",
                "observation_note": "Text only; no semantic approval"
            }, ensure_ascii=False) + "\n", encoding="utf-8")

    def test_build_deterministic_and_preserves_source(self):
        before = (self.root / "aryanpour-english-persian.jsonl").read_bytes()
        report, sample = build(self.root, reviews_path=self.reviews, quota=2,
                               seed_ids=(1, 2, 3, 4))
        self.assertEqual(report["entries_scanned"], 4)
        self.assertEqual(report["curated_surface_reviews"], 1)
        self.assertEqual(report["semantically_approved_records"], 0)
        self.assertEqual(len(sample), 4)
        self.assertEqual(report["population_per_group"]["leading_equals"], 2)
        self.assertEqual(report["population_per_group"]["source_character_issue"], 1)
        self.assertIsNone(sample[0]["verified_senses"])
        self.assertEqual(sample[0]["export_surface_review"]["observed_surface"], "(=abaxile)")
        self.assertEqual((self.root / "aryanpour-english-persian.jsonl").read_bytes(), before)
        second, again = build(self.root, reviews_path=self.reviews,
                              quota=2, seed_ids=(1, 2, 3, 4))
        self.assertEqual(report, second)
        self.assertEqual(sample, again)

    def test_corrupt_review_fails_closed(self):
        self.reviews.write_text(self.reviews.read_text(encoding="utf-8").replace(
            "(=abaxile)", "(=made_up)"
        ), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "evidence absent"):
            build(self.root, reviews_path=self.reviews, seed_ids=(1,), quota=1)


if __name__ == "__main__":
    unittest.main()
