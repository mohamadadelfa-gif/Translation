"""Portable unit tests; external OCR smoke tests run separately."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import fitz

from persian_pdf_ocr import (
    page_selection, embedded_diagnostics, process_document, safe_dpi_for,
)


class Tests(unittest.TestCase):
    def test_page_selection_valid(self):
        self.assertEqual(page_selection("3,1-2,2", 5), [1, 2, 3])

    def test_page_selection_outside(self):
        for spec in ["0", "2-1", "1,100", "a", "1-3-4"]:
            with self.subTest(spec=spec):
                with self.assertRaises(ValueError):
                    page_selection(spec, 5)

    def test_embedded_diagnostics(self):
        self.assertFalse(embedded_diagnostics("", 2)[0])
        self.assertFalse(embedded_diagnostics("\ufffd" * 10, 2)[0])
        self.assertTrue(embedded_diagnostics("فارسی نمونه", 3)[0])

    def test_render_dpi_budget(self):
        with fitz.open() as doc:
            page = doc.new_page(width=800, height=1100)
            self.assertLess(safe_dpi_for(page, 300, 1000000), 300)

    def test_text_only_source_preservation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            pdf = root / "example.pdf"
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((40, 60), "Page 1 source text")
            page = doc.new_page()
            page.insert_text((40, 60), "Page 2 source text")
            doc.save(pdf)
            doc.close()
            old = pdf.read_bytes()
            result = process_document(pdf, root / "out", mode="text", pages="2")
            self.assertEqual(pdf.read_bytes(), old)
            self.assertEqual(result["processed_pages"], [2])
            self.assertIn("Page 2 source text", (root / "out" / "document.md").read_text())
            self.assertNotIn("Page 1 source text", (root / "out" / "document.md").read_text())
            row = json.loads((root / "out" / "pages.jsonl").read_text().strip())
            self.assertEqual(row["source"], "embedded_text_layer")
            self.assertEqual(row["ocr_text"], None)

    def test_never_overwrite_input(self):
        with tempfile.TemporaryDirectory() as d:
            pdf = Path(d) / "a.pdf"
            doc = fitz.open()
            doc.new_page()
            doc.save(pdf)
            doc.close()
            with self.assertRaises(ValueError):
                process_document(pdf, pdf.parent, mode="text")

    def test_missing_paddle_explicit_error(self):
        with tempfile.TemporaryDirectory() as d:
            pdf = Path(d) / "a.pdf"
            doc = fitz.open()
            doc.new_page()
            doc.save(pdf)
            doc.close()
            try:
                import paddleocr  # noqa: F401
            except ImportError:
                with self.assertRaisesRegex(RuntimeError, "PaddleOCR not installed"):
                    process_document(pdf, Path(d) / "out", mode="ocr", engine="paddle")
            else:
                self.skipTest("PaddleOCR available: avoid downloading models in unit tests")


if __name__ == "__main__":
    unittest.main()
