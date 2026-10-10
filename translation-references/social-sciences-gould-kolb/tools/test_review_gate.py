"""Independent-review gate: no automatic approval of the 13 source candidates."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from review_gate import prepare, validate, save_jsonl, CHECKS, digest, base_candidates, ROOT


class IndependentReviewTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        (self.root / "benchmark").mkdir()
        for file in (
            "source_manifest.json",
            "benchmark/first_pass_v1.jsonl",
            "benchmark/complete_articles_first_pass.jsonl",
            "benchmark/visual_evidence_manifest.json",
            "benchmark/complete_article_evidence.json",
        ):
            shutil.copy2(ROOT / file, self.root / file)
        self.queue, self.forms = prepare(self.root)
        self.reviews_path = self.root / "review_responses.jsonl"
        self.write_forms()

    def write_forms(self):
        save_jsonl(self.reviews_path, self.forms)

    def approve(self, i=0, *, actor="external_reviewer_01"):
        q = self.queue[i]
        r = self.forms[i]
        r.update({
            "reviewer_id": actor,
            "reviewed_at": "2026-10-10T17:30:00+00:00",
            "reviewed_original_page_and_crop": True,
            "not_original_transcriber_attested": True,
            "decision": "approved",
            "image_checks": {key: True for key in CHECKS},
            "approved_transcription": q["first_pass_transcription"].copy(),
            "correction_notes": "Synthetic test fixture only, not real review.",
            "unresolved_details": [],
        })
        return r

    def test_queue_is_complete_and_not_approved(self):
        self.assertEqual(len(self.queue), 13)
        self.assertEqual(len(self.forms), 13)
        self.assertEqual(sum(x["candidate_type"] == "complete_referral"
                             for x in self.queue), 9)
        self.assertEqual(sum(x["candidate_type"] == "A_section_only"
                             for x in self.queue), 2)
        self.assertEqual(sum(x["candidate_type"] == "complete_article_candidate"
                             for x in self.queue), 2)
        self.assertTrue(all(x["decision"] == "pending" for x in self.forms))
        counts, approved = validate(self.root, self.reviews_path)
        self.assertEqual(counts["pending"], 13)
        self.assertEqual(approved, [])

    def test_output_is_deterministic(self):
        self.assertEqual(prepare(self.root), prepare(self.root))
        self.assertEqual(len({r["first_pass_sha256"] for r in self.queue}), 13)

    def test_stale_first_pass_fingerprint_rejected(self):
        self.forms[0]["first_pass_sha256"] = "0" * 64
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "stale review form"):
            validate(self.root, self.reviews_path)

    def test_duplicate_response_rejected(self):
        self.forms.append(self.forms[0].copy())
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "Unknown/duplicate"):
            validate(self.root, self.reviews_path)

    def test_missing_response_rejected(self):
        self.forms.pop()
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "Missing reviews"):
            validate(self.root, self.reviews_path)

    def test_pending_cannot_claim_approval(self):
        self.forms[0]["approved_transcription"] = {}
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "pending review"):
            validate(self.root, self.reviews_path)

    def test_original_assistant_cannot_attest_independence(self):
        self.approve(actor="chatgpt")
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "separate reviewer"):
            validate(self.root, self.reviews_path)

    def test_missing_photo_attestation_rejected(self):
        self.approve()
        self.forms[0]["reviewed_original_page_and_crop"] = False
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "source-page review attestation"):
            validate(self.root, self.reviews_path)

    def test_missing_check_rejected(self):
        self.approve()
        self.forms[0]["image_checks"]["checked_punctuation_and_zwnj"] = False
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "all image checks"):
            validate(self.root, self.reviews_path)

    def test_timezone_is_required(self):
        self.approve()
        self.forms[0]["reviewed_at"] = "2026-10-10T17:30:00"
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            validate(self.root, self.reviews_path)

    def test_correct_individual_review_is_still_partial(self):
        self.approve()
        self.write_forms()
        counts, approved = validate(self.root, self.reviews_path)
        self.assertEqual(counts["approved"], 1)
        self.assertEqual(len(approved), 1)
        self.assertEqual(approved[0]["approval_basis"],
                         "separate_reviewer_image_attestation_not_automated_visual_proof")
        with self.assertRaisesRegex(ValueError, "All 13"):
            validate(self.root, self.reviews_path, permit_partial=False)

    def test_main_article_missing_contributor_not_promotable(self):
        index = next(i for i, q in enumerate(self.queue)
                     if q["candidate_type"] == "complete_article_candidate"
                     and q["first_pass_transcription"]["contributor_fa_first_pass"] is None)
        self.approve(index)
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "unresolved contributor"):
            validate(self.root, self.reviews_path)

    def test_unverified_sections_cannot_be_added(self):
        i = next(i for i, q in enumerate(self.queue)
                 if q["candidate_type"] == "complete_article_candidate"
                 and len(q["first_pass_transcription"]["sections"]) == 2)
        self.approve(i)
        self.forms[i]["approved_transcription"]["sections"].append(
            {"label": "C", "text_first_pass": "fictional section"})
        self.write_forms()
        with self.assertRaisesRegex(ValueError, "source sections"):
            validate(self.root, self.reviews_path)

    def test_record_change_invalidates_review(self):
        path = self.root / "benchmark/first_pass_v1.jsonl"
        all_rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        all_rows[0]["notes"] += " added change "
        save_jsonl(path, all_rows)
        with self.assertRaisesRegex(ValueError, "stale review form"):
            validate(self.root, self.reviews_path)


if __name__ == "__main__":
    unittest.main()
