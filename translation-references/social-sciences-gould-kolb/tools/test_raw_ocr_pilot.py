"""Source identity and fail-closed tests for the RAW crop OCR trial.

CI has NO PDF and never OCRs a hidden/unverified source. These are metadata
tests, not recognition accuracy tests.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from run_raw_ocr_pilot import ROOT, load_regions, scan


class RawOcrMetadataTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "ocr_pilot").mkdir()
        shutil.copy2(ROOT / "ocr_pilot/REGIONS.json",
                     self.root / "ocr_pilot/REGIONS.json")

    def test_seven_source_anchored_regions(self):
        m = load_regions(self.root)
        self.assertEqual(len(m["regions"]), 7)
        self.assertEqual(m["psm_modes"], [4, 6])
        self.assertEqual(m["ocr_language_config"], "fas+eng")
        self.assertEqual(m["source_pdf_physical_pages"], 980)
        self.assertEqual(len(set(r["region_id"] for r in m["regions"])), 7)
        self.assertEqual(len(set(r["source_pdf_page"] for r in m["regions"])), 6)

    def test_duplicate_crop_rejected(self):
        p = self.root / "ocr_pilot/REGIONS.json"
        m = json.loads(p.read_text(encoding="utf-8"))
        m["regions"][1]["region_id"] = m["regions"][0]["region_id"]
        p.write_text(json.dumps(m), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid or repeated"):
            load_regions(self.root)

    def test_missing_crop_rejected(self):
        p = self.root / "ocr_pilot/REGIONS.json"
        m = json.loads(p.read_text(encoding="utf-8"))
        m["regions"].pop()
        p.write_text(json.dumps(m), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Expected 7"):
            load_regions(self.root)

    def test_out_of_bounds_page_rejected(self):
        p = self.root / "ocr_pilot/REGIONS.json"
        m = json.loads(p.read_text(encoding="utf-8"))
        m["regions"][0]["source_pdf_page"] = 981
        p.write_text(json.dumps(m), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid or repeated"):
            load_regions(self.root)

    def test_invalid_box_rejected(self):
        p = self.root / "ocr_pilot/REGIONS.json"
        m = json.loads(p.read_text(encoding="utf-8"))
        m["regions"][0]["crop_pdf_rect_points"] = [10, 40, 5, 9]
        p.write_text(json.dumps(m), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid or repeated"):
            load_regions(self.root)

    def test_wrong_source_pdf_fails_before_ocr(self):
        counterfeit = self.root / "unrelated.pdf"
        counterfeit.write_bytes(b"Not the Gould/Kolb source PDF")
        with self.assertRaisesRegex(ValueError, "user-supplied original PDF"):
            scan(counterfeit, self.root / "output", self.root)
        self.assertFalse((self.root / "output").exists())

    def test_source_manifest_hash_format(self):
        meta = load_regions(self.root)
        self.assertEqual(len(meta["source_pdf_sha256"]), 64)
        self.assertEqual(meta["source_pdf_sha256"],
                         "73b4e10a6d3d259aebbc2ebf30031e5a85f5abbede2552af94c9a7743f2c42de")


if __name__ == "__main__":
    unittest.main()
