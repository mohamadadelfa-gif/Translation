"""Run: python -m unittest -v test_check_ocr.py (from this directory)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from check_ocr import check

class Checks(unittest.TestCase):
    def test_prefix_warning_and_preservation(self):
        raw = "او نمی توانست به خانه بر گردد."
        result = check(raw)
        self.assertTrue(any(x["rule_id"] == "W001_GAP_AFTER_MI" for x in result))
        self.assertEqual(raw, "او نمی توانست به خانه بر گردد.")
        self.assertTrue(all(x["verification_status"] == "unverified_candidate" for x in result))

    def test_arabic_yeh_kaf(self):
        hits = check("كتاب فارسي")
        self.assertGreaterEqual(sum(x["rule_id"] == "U002_ARABIC_KAF_YEH" for x in hits), 2)

    def test_possible_pdf_reverse_order(self):
        result = check("رفت دانشگاه به خانه از")
        self.assertTrue(any(x["rule_id"] == "O001_POSSIBLE_REVERSE_ORDER" for x in result))

    def test_clear_phrase_not_flagged(self):
        self.assertEqual(check("از خانه به دانشگاه رفت"), [])

    def test_cli_jsonl_and_source_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inp, out, summary = root / "in.jsonl", root / "out.jsonl", root / "summary.json"
            content = json.dumps({"id":"p1","page":151,"text":"رفت دانشگاه به خانه از"}, ensure_ascii=False) + "\n"
            inp.write_text(content, encoding="utf-8")
            proc = subprocess.run([sys.executable, "check_ocr.py", str(inp), "--format", "jsonl", "--output", str(out), "--summary", str(summary)],
                                  cwd=Path(__file__).resolve().parent, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(inp.read_text(encoding="utf-8"), content)
            issues = [json.loads(x) for x in out.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(issues[0]["page"], 151)
            self.assertEqual(json.loads(summary.read_text(encoding="utf-8"))["total_flags"], len(issues))

if __name__ == "__main__":
    unittest.main()
