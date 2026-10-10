"""Phase 4 tests: surface classification and fail-closed evidence validation."""
import json
from pathlib import Path
import tempfile
import unittest

from audit_conventions import (
    compare_form, reference_shape, spans, scan, verify_register,
)


def row(rule_id, cls, key, ident, literal):
    return {
        "rule_id": rule_id, "candidate_class": cls, "surface_key": key,
        "canonical_id": ident, "source_field": "persian", "source_text": literal,
        "evidence_grade": "export_surface_only",
        "source_documentation_status": "not_located",
        "semantic_expansion": None, "verified_scope": None,
        "verified_reference_relation": None,
        "editorial_status": "unverified",
    }


class Phase4Tests(unittest.TestCase):
    def test_equals_prefix_and_suffix(self):
        self.assertEqual(reference_shape("=abaxile"), ("prefix_equals", "abaxile"))
        self.assertEqual(reference_shape("abaxile="), ("suffix_equals", "abaxile"))
        self.assertEqual(reference_shape("=abaxile="), ("ambiguous_both_ends", None))
        self.assertEqual(reference_shape("="), ("ambiguous_both_ends", None))
        self.assertEqual(reference_shape("plain"), (None, None))

    def test_literal_bracket_spans_with_offsets(self):
        text = "الف (=abaxial) و ]طب[ و [حق.]"
        cases = list(spans(text))
        self.assertEqual(len(cases), 3)
        self.assertEqual([kind for _, _, kind, _, _ in cases],
                         ["parenthesis", "mirrored_square_bracket", "square_bracket"])
        for a, b, kind, literal, interior in cases:
            self.assertEqual(text[a:b], literal)

    def test_crossed_brackets_remain_visible_as_ambiguous(self):
        text = "]a[b]"
        shapes = list(spans(text))
        self.assertEqual(len(shapes), 2)
        self.assertEqual([x[2] for x in shapes],
                         ["mirrored_square_bracket", "square_bracket"])
        self.entries[0]["persian"] = text
        self.entries[0]["original_definition_markup"] = "<C>" + text + "</C>"
        (self.root / "aryanpour-english-persian.jsonl").write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n"
                    for item in self.entries), encoding="utf-8")
        # An overlapping source string has no registered semantics.
        self.rules = [r for r in self.rules if r["canonical_id"] != 1]
        self.write_register()
        generated = self.root / "overlapping.jsonl"
        report = scan(self.root, self.register, generated)
        candidates = [json.loads(line) for line in
                      generated.read_text(encoding="utf-8").splitlines()]
        overlaps = [x for x in candidates if x["canonical_id"] == 1]
        self.assertEqual(len(overlaps), 2)
        self.assertTrue(all(x["overlaps_another_candidate"] for x in overlaps))
        self.assertGreaterEqual(report["candidate_counts"]["ambiguous_overlapping_spans"], 2)

    def test_whitespace_comparison_is_not_source_mutation(self):
        actual = " گ . ش. "
        self.assertEqual(compare_form(actual), "گ.ش.")
        self.assertEqual(actual, " گ . ش. ")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        cases = [
            (1, "abaxial", "(=abaxile) (گ . ش.) دورازمحور."),
            (2, "abaxile", "(abaxial=) ]طب[ دورازمحور."),
            (3, "abaxile", "(=unknown) دورازمحور."),
            (4, "other", "(=abaxile) (در مورد کاغذ) [حق.]"),
            (5, "x ray therapy", "(طب) درمان."),
        ]
        self.entries = [
            {"id": ident, "english": english, "persian": persian,
             "original_definition_markup": "<C>" + persian + "</C>",
             "source_character_issue": False}
            for ident, english, persian in cases
        ]
        (self.root / "aryanpour-english-persian.jsonl").write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n"
                    for item in self.entries), encoding="utf-8")
        (self.root / "conventions").mkdir()
        self.register = self.root / "conventions/register.jsonl"
        self.rules = [
            row("abbr", "abbreviation_shape", "گ.ش.", 1, "(گ . ش.)"),
            row("ref", "reference_surface", "=abaxile", 1, "(=abaxile)"),
            row("mirrored", "reversed_bracket_surface", "طب", 2, "]طب["),
            row("context", "usage_context_surface", "در مورد کاغذ",
                4, "(در مورد کاغذ)"),
        ]
        self.write_register()

    def write_register(self):
        self.register.write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n"
                    for item in self.rules), encoding="utf-8")

    def test_evidence_register_accepts_real_substrings_only(self):
        found = verify_register(self.register, {x["id"]: x for x in self.entries})
        self.assertEqual(len(found), 4)

    def test_missing_evidence_rejected(self):
        self.rules[0]["source_text"] = "(something not in source)"
        self.write_register()
        with self.assertRaisesRegex(ValueError, "not present"):
            scan(self.root, self.register)

    def test_semantic_claim_rejected(self):
        self.rules[0]["semantic_expansion"] = "approved without evidence"
        self.write_register()
        with self.assertRaisesRegex(ValueError, "Semantic claim"):
            scan(self.root, self.register)

    def test_unjustified_editorial_status_rejected(self):
        self.rules[0]["editorial_status"] = "approved"
        self.write_register()
        with self.assertRaisesRegex(ValueError, "Semantic claim"):
            scan(self.root, self.register)

    def test_register_spelling_mismatch_rejected(self):
        self.rules[1]["surface_key"] = "=other"
        self.write_register()
        with self.assertRaisesRegex(ValueError, "Parenthesis surface mismatch"):
            scan(self.root, self.register)

    def test_reversed_bracket_mismatch_rejected(self):
        self.rules[2]["surface_key"] = "wrong"
        self.write_register()
        with self.assertRaisesRegex(ValueError, "Bracket surface mismatch"):
            scan(self.root, self.register)

    def test_full_scan_conservative_and_deterministic(self):
        before = (self.root / "aryanpour-english-persian.jsonl").read_bytes()
        out = self.root / "generated_candidates.jsonl"
        result = scan(self.root, self.register, out)
        again = scan(self.root, self.register)
        self.assertEqual(result, again)
        self.assertEqual(result["canonical_records"], 5)
        self.assertEqual(result["semantic_conventions_approved"], 0)
        self.assertEqual(result["source_verified_evidence_cases"], 4)
        self.assertGreater(result["candidate_counts"]["apparent_reference_surface"], 0)
        self.assertGreater(result["candidate_counts"]["mirrored_bracket_surface"], 0)
        self.assertEqual(result["reference_lookup_statuses"]["prefix_equals:multiple_exact_text_matches"], 2)
        self.assertEqual(result["reference_lookup_statuses"]["suffix_equals:unique_exact_text_match"], 1)
        self.assertEqual(result["reference_lookup_statuses"]["prefix_equals:no_exact_text_match"], 1)
        extracted = [json.loads(s) for s in out.read_text(
            encoding="utf-8").splitlines()]
        self.assertEqual(len(extracted), result["candidate_occurrences"])
        for item in extracted:
            target = self.entries[item["canonical_id"] - 1]["persian"]
            a, b = item["span"]
            self.assertEqual(target[a:b], item["surface_literal"])
            self.assertFalse(item["semantic_role_verified"])
            self.assertEqual(item["review_status"], "unverified")
        self.assertEqual(
            (self.root / "aryanpour-english-persian.jsonl").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
