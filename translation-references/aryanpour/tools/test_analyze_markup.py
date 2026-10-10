"""Conservative Phase 2 markup inventory tests; no external dependencies."""
import json
import tempfile
import unittest
from pathlib import Path

from analyze_markup import analyze, markup_observation, projection


REAL_CULTURE_MARKUP = (
    "<C><F><H /><I><N><Ò>"
    "کشت میکرب در آزمایشگاه ، برز، فرهنگ ، پرورش، تمدن ."
    "</Ò></N></I></F></C>"
)
REAL_HISTORY_MARKUP = (
    "<C><F><H /><I><N><Ò>"
    "تاریخ، تاریخچه ، سابقه ، پیشینه ، ( طب ) بیمارنامه ."
    "</Ò></N></I></F></C>"
)


class MarkupTests(unittest.TestCase):
    def test_actual_sample_tag_signature(self):
        obs = markup_observation(REAL_CULTURE_MARKUP)
        self.assertEqual(obs["markup_issues"], [])
        self.assertEqual(obs["tag_names"], ["C", "F", "H", "I", "N", "Ò",
                                            "Ò", "N", "I", "F", "C"])
        self.assertEqual(obs["empty_tags"], {"H": 1})
        self.assertIsNone(obs["sense_boundaries"])
        self.assertIsNone(obs["cross_references"])

    def test_comma_does_not_create_senses(self):
        obs = markup_observation(REAL_CULTURE_MARKUP)
        self.assertIsNone(obs["sense_boundaries"])
        self.assertIsNone(obs["grammatical_labels"])
        self.assertIsNone(obs["examples"])

    def test_parenthesized_subject_not_automatically_label(self):
        obs = markup_observation(REAL_HISTORY_MARKUP)
        self.assertEqual(obs["parenthetical_occurrences"], [" طب "])
        self.assertIsNone(obs["leading_parenthetical_candidate"])
        self.assertIsNone(obs["grammatical_labels"])

    def test_leading_parenthetical_is_unverified(self):
        obs = markup_observation("<C>(طب) درمان  با اشعه  مجهول.</C>")
        self.assertEqual(obs["leading_parenthetical_candidate"], "طب")
        self.assertIsNone(obs["grammatical_labels"])

    def test_newline_projection_follows_original_export(self):
        self.assertEqual(projection("<C>الف<n />ب</C>"), "الف\nب")
        self.assertEqual(projection("<C>الف<n/>ب</C>"), "الف\nب")

    def test_malformed_markup_is_reported_without_repair(self):
        obs = markup_observation("<C><Ò>الف</C>")
        self.assertIn("mismatched_closing_tag", obs["markup_issues"])
        self.assertIsNone(obs["sense_boundaries"])

    def test_unmatched_bracket_reported(self):
        obs = markup_observation("<C>الف < ب</C>")
        self.assertIn("unmatched_angle_bracket", obs["markup_issues"])

    def test_inventory_export_preserves_uncertainty(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / "aryanpour-english-persian.jsonl"
            observations = [
                {"id": 1, "english": "culture",
                 "persian": projection(REAL_CULTURE_MARKUP),
                 "original_definition_markup": REAL_CULTURE_MARKUP,
                 "source_character_issue": False},
                {"id": 2, "english": "history",
                 "persian": projection(REAL_HISTORY_MARKUP),
                 "original_definition_markup": REAL_HISTORY_MARKUP,
                 "source_character_issue": False},
            ]
            p.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n"
                                 for record in observations), encoding="utf-8")
            out = root / "candidates.jsonl"
            report = analyze(root, sample_limit=2, candidates_path=out)
            self.assertEqual(report["entries_examined"], 2)
            self.assertEqual(report["distinct_tag_names"], 6)
            self.assertEqual(report["counts"]["records_with_markup_issues"], 0)
            self.assertEqual(report["distinct_tag_signatures"], 1)
            candidates = [json.loads(line) for line in out.read_text(
                encoding="utf-8").splitlines()]
            self.assertEqual(len(candidates), 2)
            self.assertTrue(all(candidate["sense_boundaries"] is None
                                for candidate in candidates))
            self.assertTrue(all(candidate["cross_references"] is None
                                for candidate in candidates))

    def test_projection_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "aryanpour-english-persian.jsonl").write_text(
                json.dumps({"id": 1, "english": "a", "persian": "wrong",
                            "original_definition_markup": "<C>actual</C>",
                            "source_character_issue": False}) + "\n",
                encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "projection mismatch"):
                analyze(root)


if __name__ == "__main__":
    unittest.main()
