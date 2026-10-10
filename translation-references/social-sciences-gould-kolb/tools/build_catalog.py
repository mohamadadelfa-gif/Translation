#!/usr/bin/env python3
"""Evidence-first Gould/Kolb scanned dictionary catalog builder.

Requires PyMuPDF only when --pdf is provided. Without --pdf, validates
reviewed pilot metadata but does NOT claim to have checked source pages.
Does not run OCR, infer article text, or approve semantic references.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def jsonl(path):
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number}: invalid JSON") from exc


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def load_manifest(path):
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for key in ("source_pdf_sha256", "source_pdf_bytes",
                "physical_pages", "physical_page_regions"):
        if key not in manifest:
            raise ValueError(f"Missing manifest key: {key}")
    if not re.fullmatch(r"[0-9a-f]{64}", manifest["source_pdf_sha256"]):
        raise ValueError("Invalid SHA-256")
    count = manifest["physical_pages"]
    if type(count) is not int or count < 1:
        raise ValueError("Invalid page count")
    covered = []
    for region in manifest["physical_page_regions"]:
        a, b = region["first"], region["last"]
        if not 1 <= a <= b <= count:
            raise ValueError("Out-of-bounds region")
        covered.extend(range(a, b + 1))
    if covered != list(range(1, count + 1)):
        raise ValueError("Source page regions must cover every page exactly once")
    if any(not 1 <= n <= count for n in manifest.get("visually_inspected_pages", [])):
        raise ValueError("Invalid visually inspected page")
    return manifest



def load_editorial_rules(root, manifest):
    """Require the source's editorial conventions before compiling any index.

    This registry is based on visually inspected Persian introductory pages.
    It does not purport to check the absent original English dictionary.
    """
    path = root / "editorial_rules.json"
    ruleset = json.loads(path.read_text(encoding="utf-8"))
    if (ruleset.get("schema") != "gould-kolb.editorial-rules.v1"
            or ruleset.get("scope") != "gould-kolb-persian-edition-only"):
        raise ValueError("Missing or incompatible Gould/Kolb editorial rules")
    if ruleset.get("transcription_status") != "rules_paraphrased_not_verbatim":
        raise ValueError("Editorial rules cannot masquerade as exact transcription")
    rules = ruleset.get("rules")
    if not isinstance(rules, list) or len(rules) < 10:
        raise ValueError("Incomplete editorial rule register")
    seen, categories = set(), set()
    for r in rules:
        ident = r.get("rule_id")
        if (not isinstance(ident, str) or not ident.startswith("gk-")
                or ident in seen):
            raise ValueError("Duplicate or invalid editorial rule ID")
        seen.add(ident)
        categories.add(r.get("category"))
        source = r.get("source")
        if not isinstance(source, dict) or source.get(
                "evidence_basis") != "visually_inspected_persian_editorial_introduction":
            raise ValueError(f"{ident}: editorial source evidence is missing")
        pages = source.get("physical_pdf_pages")
        if (not isinstance(pages, list) or not pages
                or any(type(n) is not int or n not in range(10, 18)
                       or n not in manifest["visually_inspected_pages"]
                       for n in pages)):
            raise ValueError(f"{ident}: unverified introductory PDF page locator")
        if (r.get("review_status") != "source_rule_identified"
                or r.get("independently_checked_against_original_english") is not False
                or r.get("authoritative_for") != "gould_kolb_persian_edition_only"):
            raise ValueError(f"{ident}: editorial authority is overstated")
        if (not isinstance(r.get("editorial_claim_paraphrase_en"), str)
                or not r["editorial_claim_paraphrase_en"]
                or not isinstance(r.get("extraction_implication_en"), str)
                or not r["extraction_implication_en"]):
            raise ValueError(f"{ident}: incomplete rule explanation")
    expected = {"article_structure", "section_A", "section_B", "sections_CDE",
                "see_referral", "also_related_entry", "editorial_interpolation",
                "proper_names", "orthography", "source_comparison"}
    if not expected <= categories:
        raise ValueError(f"Missing source-defined categories: {sorted(expected - categories)}")
    return rules


def region_at(manifest, page):
    for region in manifest["physical_page_regions"]:
        if region["first"] <= page <= region["last"]:
            return region
    raise ValueError(f"Page not classified: {page}")


def inferred_printed_page(region, page):
    if region["role"] == "main_dictionary":
        return page - 19
    if region["role"] == "european_persian_glossary":
        return 979 - page
    return None


def validate_pilot(root, manifest):
    entries = list(jsonl(root / "pilot/entries.jsonl"))
    glossary = list(jsonl(root / "pilot/glossary_rows.jsonl"))
    seen = set()
    for entry in entries:
        ident = entry.get("record_id")
        if (not isinstance(ident, str) or not ident.startswith("gk-entry-")
                or ident in seen):
            raise ValueError(f"Invalid/duplicate entry ID: {ident}")
        seen.add(ident)
        a, b = entry.get("start_pdf_page"), entry.get("end_pdf_page")
        if type(a) is not int or region_at(manifest, a)["role"] != "main_dictionary":
            raise ValueError(f"{ident}: invalid start page")
        if b is not None and (type(b) is not int or b < a
                              or region_at(manifest, b)["role"] != "main_dictionary"):
            raise ValueError(f"{ident}: invalid end page")
        if entry.get("record_type") != "dictionary_entry":
            raise ValueError(f"{ident}: wrong record type")
        if entry.get("entry_kind") not in ("main", "referral", "also", "uncertain"):
            raise ValueError(f"{ident}: unknown entry kind")
        if any(not isinstance(entry.get(k), str) or not entry[k] for k in
               ("headword_fa_exact", "headword_en_exact")):
            raise ValueError(f"{ident}: missing literal heading")
        if entry.get("transcription_status") not in (
                "heading_only_visual", "heading_and_referral_visual"):
            raise ValueError(f"{ident}: unsupported transcription status")
        if (entry.get("article_text_exact") is not None
                or entry.get("contributors_exact") is not None
                or entry.get("semantic_review_status") != "not_started"):
            raise ValueError(f"{ident}: unverified textual or semantic claim")
        labels = entry.get("observed_section_labels")
        if (not isinstance(labels, list)
                or any(x not in list("ABCDE") for x in labels)):
            raise ValueError(f"{ident}: invalid exposition section marker")
        if entry["entry_kind"] == "referral":
            if (entry.get("referral_marker_literal") != "←"
                    or not entry.get("referral_target_literal")
                    or entry.get("target_resolution_status") != "unverified"):
                raise ValueError(f"{ident}: unverified referral invariant")
        elif entry.get("referral_target_literal") is not None:
            raise ValueError(f"{ident}: fabricated referral")
        # "also"/نیز is a different source-defined relation from "see"/←.
        if entry["entry_kind"] == "also":
            if (entry.get("related_marker_literal") != "نیز"
                    or not entry.get("related_target_literal")
                    or entry.get("related_resolution_status") != "unverified"):
                raise ValueError(f"{ident}: also/نیز requires an unverified related target")
        elif (entry.get("related_marker_literal") is not None
                or entry.get("related_target_literal") is not None):
            raise ValueError(f"{ident}: unrelated entry cannot invent نیز reference")
        pages = entry.get("evidence_pdf_pages")
        if (not isinstance(pages, list) or a not in pages
                or any(type(p) is not int or
                       region_at(manifest, p)["role"] != "main_dictionary"
                       for p in pages)):
            raise ValueError(f"{ident}: invalid image evidence locator")
    positions = set()
    for row in glossary:
        ident, p = row.get("record_id"), row.get("pdf_page")
        if (not isinstance(ident, str) or not ident.startswith("gk-gloss-")
                or ident in seen):
            raise ValueError(f"Invalid/duplicate glossary ID: {ident}")
        seen.add(ident)
        if type(p) is not int or region_at(manifest, p)["role"] != "european_persian_glossary":
            raise ValueError(f"{ident}: invalid glossary physical page")
        if row.get("record_type") != "glossary_row":
            raise ValueError(f"{ident}: wrong record type")
        if any(not isinstance(row.get(k), str) or not row[k] for k in
               ("english_exact", "persian_exact")):
            raise ValueError(f"{ident}: missing source headword/equivalent")
        if (row.get("column") not in ("left", "right")
                or type(row.get("row_order_within_column")) is not int):
            raise ValueError(f"{ident}: invalid glossary reading order")
        if (row.get("transcription_status") != "visual_checked"
                or row.get("main_entry_id") is not None
                or row.get("main_entry_resolution_status") != "not_attempted"):
            raise ValueError(f"{ident}: invented main-entry link")
        if row.get("printed_glossary_page_inferred") != inferred_printed_page(
                region_at(manifest, p), p):
            raise ValueError(f"{ident}: printed page mapping mismatch")
        pos = (p, row["column"], row["row_order_within_column"])
        if pos in positions:
            raise ValueError(f"Duplicate glossary source position: {pos}")
        positions.add(pos)
    return entries, glossary


def inventory_pdf(pdf, manifest):
    # Hash before attempting to parse an unrelated or damaged file.
    if pdf.stat().st_size != manifest["source_pdf_bytes"] or sha256(pdf) != manifest["source_pdf_sha256"]:
        raise ValueError("Supplied PDF does not match the frozen source hash and size")
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("Install PyMuPDF: python -m pip install pymupdf") from exc
    doc = fitz.open(pdf)
    if len(doc) != manifest["physical_pages"]:
        raise ValueError("Physical page count differs from source manifest")
    output = []
    for n, page in enumerate(doc, 1):
        region = region_at(manifest, n)
        printed = inferred_printed_page(region, n)
        output.append({
            "pdf_page": n,
            "role": region["role"],
            "role_classification_basis": region["region_status"],
            "printed_page_inferred": printed,
            "printed_page_review_status":
                "inferred_from_checked_samples" if printed is not None else "not_applicable",
            "page_width_pt": round(page.rect.width, 3),
            "page_height_pt": round(page.rect.height, 3),
            "embedded_image_count": len(page.get_images(full=True)),
            "selectable_text_characters": len(page.get_text("text").strip()),
            "visually_inspected_for_pilot": n in manifest["visually_inspected_pages"],
            "transcription_status": "not_transcribed",
        })
    doc.close()
    return output


def save_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                    encoding="utf-8")


def build(root, output, pdf=None):
    manifest = load_manifest(root / "source_manifest.json")
    editorial_rules = load_editorial_rules(root, manifest)
    entries, glossary = validate_pilot(root, manifest)
    verified = pdf is not None
    pages = inventory_pdf(Path(pdf), manifest) if verified else None
    if pages is not None:
        save_jsonl(output / "physical_pages.jsonl", pages)
    index = [
        {"id": row["record_id"], "headword": row["headword_fa_exact"],
         "english": row["headword_en_exact"], "pdf_page": row["start_pdf_page"],
         "record_type": "dictionary_entry", "transcription_status": row["transcription_status"]}
        for row in entries
    ] + [
        {"id": row["record_id"], "headword": row["persian_exact"],
         "english": row["english_exact"], "pdf_page": row["pdf_page"],
         "record_type": "glossary_row", "transcription_status": row["transcription_status"]}
        for row in glossary
    ]
    save_jsonl(output / "pilot_lookup.jsonl", index)
    report = {
        "schema_version": "gould-kolb.build-report.v1",
        "editorial_rules_validated": len(editorial_rules),
        "editorial_authority": "source_persian_editorial_introduction_only",
        "source_pdf_sha256_expected": manifest["source_pdf_sha256"],
        "source_pdf_sha256_verified_in_this_run": verified,
        "physical_pages_expected": manifest["physical_pages"],
        "physical_pages_examined_in_this_run": len(pages) if pages else 0,
        "pages_with_selectable_text": (
            sum(bool(p["selectable_text_characters"]) for p in pages) if pages else None),
        "main_dictionary_pilot_records": len(entries),
        "glossary_pilot_rows": len(glossary),
        "full_definitions_transcribed": 0,
        "referral_targets_verified": 0,
        "glossary_to_main_links_verified": 0,
        "release_status": "structural_pilot_not_complete_dictionary",
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "build_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--pdf", type=Path, help="Required for 980-page source-verified inventory")
    p.add_argument("--output", type=Path, default=ROOT / "generated")
    args = p.parse_args()
    print(json.dumps(build(args.root, args.output, args.pdf), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
