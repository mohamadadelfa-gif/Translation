"""Gould/Kolb source-preserving catalog regression tests."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from build_catalog import (ROOT, build, inventory_pdf, load_manifest,
                           region_at, inferred_printed_page, validate_pilot,
                           load_editorial_rules)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "pilot").mkdir()
        for filename in ("source_manifest.json", "editorial_rules.json", "pilot/entries.jsonl",
                         "pilot/glossary_rows.jsonl"):
            shutil.copy2(ROOT / filename, self.root / filename)
        self.manifest = load_manifest(self.root / "source_manifest.json")

    def test_boundaries_and_page_order(self):
        self.assertEqual(self.manifest["physical_pages"], 980)
        self.assertEqual(region_at(self.manifest, 20)["role"], "main_dictionary")
        self.assertEqual(region_at(self.manifest, 956)["role"], "main_dictionary")
        self.assertEqual(region_at(self.manifest, 957)["role"], "european_persian_glossary")
        self.assertEqual(region_at(self.manifest, 978)["role"], "european_persian_glossary")
        self.assertEqual(inferred_printed_page(region_at(self.manifest, 20), 20), 1)
        self.assertEqual(inferred_printed_page(region_at(self.manifest, 956), 956), 937)
        self.assertEqual(inferred_printed_page(region_at(self.manifest, 957), 957), 22)
        self.assertEqual(inferred_printed_page(region_at(self.manifest, 978), 978), 1)

    def test_incomplete_regions_rejected(self):
        item = json.loads((self.root / "source_manifest.json").read_text())
        item["physical_page_regions"][1]["first"] = 21
        (self.root / "source_manifest.json").write_text(json.dumps(item))
        with self.assertRaisesRegex(ValueError, "cover every page"):
            load_manifest(self.root / "source_manifest.json")

    def test_no_source_run_does_not_claim_source_verified(self):
        result = build(self.root, self.root / "generated")
        self.assertFalse(result["source_pdf_sha256_verified_in_this_run"])
        self.assertEqual(result["physical_pages_examined_in_this_run"], 0)
        self.assertEqual(result["main_dictionary_pilot_records"], 5)
        self.assertEqual(result["glossary_pilot_rows"], 6)
        self.assertEqual(result["full_definitions_transcribed"], 0)
        self.assertEqual(result["editorial_rules_validated"], 12)
        self.assertFalse((self.root / "generated/physical_pages.jsonl").exists())
        self.assertEqual(len((self.root / "generated/pilot_lookup.jsonl").read_text(
            encoding="utf-8").splitlines()), 11)

    def test_rejects_unreviewed_article_text(self):
        p = self.root / "pilot/entries.jsonl"
        rows = [json.loads(x) for x in p.read_text().splitlines()]
        rows[0]["article_text_exact"] = "unsupported invented definition"
        p.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n")
        with self.assertRaisesRegex(ValueError, "unverified textual"):
            validate_pilot(self.root, self.manifest)

    def test_rejects_premature_target_resolution(self):
        p = self.root / "pilot/entries.jsonl"
        rows = [json.loads(x) for x in p.read_text().splitlines()]
        referral = next(x for x in rows if x["entry_kind"] == "referral")
        referral["target_resolution_status"] = "verified"
        p.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n")
        with self.assertRaisesRegex(ValueError, "referral invariant"):
            validate_pilot(self.root, self.manifest)

    def test_rejects_glossary_entry_on_main_dictionary_page(self):
        p = self.root / "pilot/glossary_rows.jsonl"
        rows = [json.loads(x) for x in p.read_text().splitlines()]
        rows[0]["pdf_page"] = 20
        p.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n")
        with self.assertRaisesRegex(ValueError, "invalid glossary physical page"):
            validate_pilot(self.root, self.manifest)

    def test_rejects_pdf_hash_mismatch(self):
        fake = self.root / "other.pdf"
        fake.write_bytes(b"not the user-supplied PDF")
        with self.assertRaisesRegex(ValueError, "frozen source"):
            inventory_pdf(fake, self.manifest)

    def test_editorial_rule_set_is_required_for_build(self):
        (self.root / "editorial_rules.json").unlink()
        with self.assertRaises(FileNotFoundError):
            build(self.root, self.root / "generated")

    def test_editorial_rules_map_to_checked_intro_pages(self):
        found = load_editorial_rules(self.root, self.manifest)
        self.assertGreaterEqual(len(found), 12)
        by_kind = {row["category"]: row for row in found}
        self.assertEqual(by_kind["see_referral"]["source"]["physical_pdf_pages"], [14])
        self.assertEqual(by_kind["also_related_entry"]["source"]["physical_pdf_pages"], [14])
        self.assertNotEqual(by_kind["see_referral"]["rule_id"],
                            by_kind["also_related_entry"]["rule_id"])

    def test_unsupported_semantic_authority_is_rejected(self):
        path = self.root / "editorial_rules.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["rules"][0]["independently_checked_against_original_english"] = True
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "authority is overstated"):
            build(self.root, self.root / "generated")

    def test_uninspected_rule_page_is_rejected(self):
        path = self.root / "editorial_rules.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["rules"][0]["source"]["physical_pdf_pages"] = [19]
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unverified introductory"):
            build(self.root, self.root / "generated")

    def test_source_categories_are_kept_separate(self):
        main, glossary = validate_pilot(self.root, self.manifest)
        self.assertEqual(len(main), 5)
        self.assertEqual(len(glossary), 6)
        self.assertEqual(sum(x["entry_kind"] == "referral" for x in main), 1)
        self.assertTrue(all(x["article_text_exact"] is None for x in main))
        self.assertTrue(all(x["main_entry_id"] is None for x in glossary))


if __name__ == "__main__":
    unittest.main()
