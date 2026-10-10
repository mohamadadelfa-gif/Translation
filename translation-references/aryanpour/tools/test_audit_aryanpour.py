"""Regression tests for the read-only Aryanpour integrity auditor.

These tests use synthetic examples, not substitutes for full-corpus validation.
"""
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from audit_aryanpour import audit, readable_from_markup


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "index").mkdir()
        (self.root / "dictionary/X").mkdir(parents=True)
        self.entries = [
            {
                "id": 1,
                "english": "x ray therapy",
                "persian": "(طب) درمان  با اشعه  مجهول.",
                "original_definition_markup": "<C>(طب) درمان  با اشعه  مجهول.</C>",
                "source_character_issue": False,
            },
            {
                "id": 2,
                "english": "x word",
                "persian": "پیغ�مبر",
                "original_definition_markup": "<C>پیغ�مبر</C>",
                "source_character_issue": True,
            },
        ]
        self.write_canonical()
        fields = ["headword", "normalized_headword", "entry_id", "file",
                  "anchor", "source_character_issue"]
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            with (self.root / "index" / f"{letter}-headwords.csv").open(
                "w", encoding="utf-8", newline=""
            ) as stream:
                writer = csv.writer(stream)
                writer.writerow(fields)
                if letter == "X":
                    writer.writerow(["x ray therapy", "x ray therapy", "1",
                                     "dictionary/X/X-01.md", "entry-1-x-ray-therapy", "false"])
                    writer.writerow(["x word", "x word", "2",
                                     "dictionary/X/X-01.md", "entry-2-x-word", "true"])
        tick = chr(96)
        text = (
            f'<a id="entry-1-x-ray-therapy"></a>\n'
            f'### x ray therapy\n\n- Entry ID: {tick}1{tick}\n'
            f'- Source character issue: {tick}false{tick}\n\n'
            f'(طب) درمان  با اشعه  مجهول.\n\n'
            f'<a id="entry-2-x-word"></a>\n'
            f'### x word\n\n- Entry ID: {tick}2{tick}\n'
            f'- Source character issue: {tick}true{tick}\n\n'
            f'پیغ�مبر\n'
        )
        (self.root / "dictionary/X/X-01.md").write_text(text, encoding="utf-8")

    def write_canonical(self):
        path = self.root / "aryanpour-english-persian.jsonl"
        path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n"
                                for item in self.entries), encoding="utf-8")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.root / "manifest.json").write_text(json.dumps({
            "entries_total": len(self.entries),
            "letters": {"X": len(self.entries)},
            "shards_total": 1,
            "source_files": {path.name: {"sha256": digest}},
        }), encoding="utf-8")
        damaged = [item for item in self.entries
                   if "�" in item["english"] or "�" in item["original_definition_markup"]]
        (self.root / "conversion-report.json").write_text(json.dumps({
            "entries": len(self.entries),
            "exportedEntries": len(self.entries),
            "entriesWithReplacementCharacters": len(damaged),
        }), encoding="utf-8")
        (self.root / "source-character-issues.json").write_text(
            json.dumps(damaged, ensure_ascii=False), encoding="utf-8")

    def test_projection(self):
        self.assertEqual(readable_from_markup("<x>a<n/>b</x>"), "a\nb")

    def test_good_fixture(self):
        self.assertTrue(audit(self.root, check_shards=True)["ok"])

    def test_definition_mutation_is_caught(self):
        self.entries[0]["persian"] = "درمان با اشعه مجهول."
        self.write_canonical()
        result = audit(self.root, check_shards=True)
        self.assertFalse(result["ok"])
        self.assertTrue(any("persian !=" in msg for msg in result["errors"]))

    def test_wrong_damage_flag_is_caught(self):
        self.entries[1]["source_character_issue"] = False
        self.write_canonical()
        result = audit(self.root, check_shards=True)
        self.assertFalse(result["ok"])
        self.assertTrue(any("issue flag inconsistent" in msg for msg in result["errors"]))

    def test_digest_mismatch_is_caught(self):
        path = self.root / "aryanpour-english-persian.jsonl"
        path.write_bytes(path.read_bytes() + b"\n")
        result = audit(self.root, check_shards=True)
        self.assertFalse(result["ok"])
        self.assertTrue(any("SHA256 mismatch" in msg for msg in result["errors"]))

    def test_index_headword_mutation_is_caught(self):
        path = self.root / "index/X-headwords.csv"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "x ray therapy,x ray therapy,", "x ray therapy,wrong key,"
        ), encoding="utf-8")
        result = audit(self.root, check_shards=True)
        self.assertFalse(result["ok"])
        self.assertTrue(any("Index normalization differs" in msg for msg in result["errors"]))

    def test_markdown_definition_mutation_is_caught(self):
        path = self.root / "dictionary/X/X-01.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "درمان  با اشعه", "درمان با اشعه"
        ), encoding="utf-8")
        result = audit(self.root, check_shards=True)
        self.assertFalse(result["ok"])
        self.assertTrue(any("Derived definition differs" in msg for msg in result["errors"]))

    def test_issue_file_content_mismatch_is_caught(self):
        path = self.root / "source-character-issues.json"
        items = json.loads(path.read_text(encoding="utf-8"))
        items[0]["persian"] = "corrupted"
        path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
        result = audit(self.root, check_shards=True)
        self.assertFalse(result["ok"])
        self.assertTrue(any("Character issue file persian disagrees" in msg
                            for msg in result["errors"]))

    def test_manifest_listed_companion_hash_is_checked(self):
        path = self.root / "manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        companion = self.root / "aryanpour-english-persian.txt"
        companion.write_text("unchanged", encoding="utf-8")
        manifest["source_files"][companion.name] = {
            "sha256": hashlib.sha256(companion.read_bytes()).hexdigest()
        }
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(audit(self.root, check_shards=True)["ok"])
        companion.write_text("damaged", encoding="utf-8")
        result = audit(self.root, check_shards=True)
        self.assertFalse(result["ok"])
        self.assertTrue(any("Source file SHA256 mismatch" in msg
                            for msg in result["errors"]))


if __name__ == "__main__":
    unittest.main()
