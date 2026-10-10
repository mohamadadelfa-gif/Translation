#!/usr/bin/env python3
"""Read-only integrity audit of the frozen Aryanpour LD2-derived dictionary.

Usage:
  python translation-references/aryanpour/tools/audit_aryanpour.py \
    --root translation-references/aryanpour --check-shards

This validates source/export consistency, not lexical correctness or attribution.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def readable_from_markup(markup: str) -> str:
    # Mirror the original LD2 converter's extraction, not semantic XML parsing.
    text = re.sub(r"<n\s*/>", "\n", markup, flags=re.IGNORECASE)
    return re.sub(r"<[^>]*>", "", text)


def norm_key(headword: str) -> str:
    # Navigation key only; canonical English/Persian are never normalized.
    return " ".join(unicodedata.normalize("NFKC", headword).split()).casefold()


def audit(root: Path, *, skip_manifest=False, skip_index=False, check_shards=False):
    failures = []
    advisories = []

    def fail(message):
        failures.append(message)

    canonical = root / "aryanpour-english-persian.jsonl"
    if not canonical.is_file():
        return {"ok": False, "errors": [f"Missing canonical file: {canonical}"]}

    manifest = {}
    if not skip_manifest:
        path = root / "manifest.json"
        if not path.is_file():
            fail("Missing manifest.json")
        else:
            try:
                manifest = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                fail(f"Unreadable manifest: {exc}")

    actual_hash = sha256_file(canonical)
    for name, metadata in manifest.get("source_files", {}).items():
        expected = metadata.get("sha256") if isinstance(metadata, dict) else None
        path = root / name
        if not path.is_file():
            fail(f"Missing manifest-listed source file: {name}")
        elif expected:
            observed = actual_hash if name == canonical.name else sha256_file(path)
            if observed != expected:
                label = "Canonical SHA256 mismatch" if name == canonical.name else f"Source file SHA256 mismatch for {name}"
                fail(f"{label}: expected {expected}, got {observed}")

    seen_ids = set()
    records = {}
    affected = []
    count = 0
    previous_id = 0
    with canonical.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                fail(f"Blank JSONL record at line {line_number}")
                continue
            count += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(f"Invalid JSON at line {line_number}: {exc}")
                continue
            if not isinstance(item, dict):
                fail(f"Not an object at line {line_number}")
                continue
            entry_id = item.get("id")
            if type(entry_id) is not int or entry_id <= 0:
                fail(f"Invalid id at line {line_number}: {entry_id!r}")
                continue
            if entry_id in seen_ids:
                fail(f"Duplicate entry id: {entry_id}")
            seen_ids.add(entry_id)
            if entry_id <= previous_id:
                fail(f"Out-of-order ID {entry_id} at line {line_number}")
            previous_id = entry_id
            for key in ("english", "persian", "original_definition_markup"):
                if not isinstance(item.get(key), str):
                    fail(f"Entry {entry_id}: missing/non-string {key}")
            english = item.get("english")
            persian = item.get("persian")
            markup = item.get("original_definition_markup")
            issue = item.get("source_character_issue")
            if type(issue) is not bool:
                fail(f"Entry {entry_id}: missing/non-boolean source_character_issue")
            if not all(isinstance(value, str) for value in (english, persian, markup)):
                continue
            if persian != readable_from_markup(markup):
                fail(f"Entry {entry_id}: persian != export-style reading of original markup")
            has_replacement = "\ufffd" in english or "\ufffd" in markup
            if isinstance(issue, bool) and issue != has_replacement:
                fail(f"Entry {entry_id}: source-character issue flag inconsistent with U+FFFD")
            if has_replacement:
                affected.append({"id": entry_id, "english": english})
            records[entry_id] = (english, issue, persian, markup)

    expected_count = manifest.get("entries_total")
    if expected_count is not None and count != expected_count:
        fail(f"Entry count mismatch: manifest={expected_count}, parsed={count}")
    if manifest and seen_ids != set(range(1, count + 1)):
        fail("Entry IDs are not exactly the consecutive sequence 1..entries_total")
    if manifest:
        report_path = root / "conversion-report.json"
        if not report_path.is_file():
            fail("Missing conversion-report.json")
        else:
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
                for name in ("entries", "exportedEntries"):
                    if name in report and report[name] != count:
                        fail(f"Conversion report {name} disagrees with canonical count")
                expected_damaged = report.get("entriesWithReplacementCharacters")
                if expected_damaged is not None and len(affected) != expected_damaged:
                    fail(f"Source-character damage count differs from conversion report: {len(affected)} vs {expected_damaged}")
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                fail(f"Could not read conversion report: {exc}")
        issues_path = root / "source-character-issues.json"
        if not issues_path.is_file():
            fail("Missing source-character-issues.json")
        else:
            try:
                issue_records = json.loads(issues_path.read_text(encoding="utf-8"))
                if not isinstance(issue_records, list):
                    fail("Source-character issues is not an array")
                else:
                    ids = [item.get("id") for item in issue_records if isinstance(item, dict)]
                    if len(ids) != len(issue_records) or len(ids) != len(set(ids)):
                        fail("Source-character-issues contains invalid or duplicate entries")
                    actual_ids = {item["id"] for item in affected}
                    if set(ids) != actual_ids:
                        fail(f"Source-character-issues IDs disagree: missing={sorted(actual_ids - set(ids))}, extra={sorted(set(ids) - actual_ids)}")
                    for item in issue_records:
                        if isinstance(item, dict) and item.get("id") in records:
                            english, flagged, persian, markup = records[item["id"]]
                            for key, expected in (
                                ("english", english),
                                ("persian", persian),
                                ("original_definition_markup", markup),
                                ("source_character_issue", flagged),
                            ):
                                if item.get(key) != expected:
                                    fail(f"Character issue file {key} disagrees for ID {item['id']}")
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                fail(f"Could not read source-character issues: {exc}")

    index_count = 0
    checked_shards = 0
    duplicate_headwords = 0
    if not skip_index:
        index_files = sorted((root / "index").glob("[A-Z]-headwords.csv"))
        if len(index_files) != 26:
            fail(f"Expected 26 letter indexes, found {len(index_files)}")
        index_ids = set()
        letters = Counter()
        by_headword = defaultdict(set)
        shard_anchors = defaultdict(set)
        for path in index_files:
            with path.open("r", encoding="utf-8", newline="") as stream:
                for row in csv.DictReader(stream):
                    index_count += 1
                    letters[path.stem[0]] += 1
                    try:
                        entry_id = int(row["entry_id"])
                    except (KeyError, ValueError, TypeError):
                        fail(f"{path.name}: invalid index entry ID at row {index_count}")
                        continue
                    if entry_id in index_ids:
                        fail(f"Index repeats entry id {entry_id}")
                    index_ids.add(entry_id)
                    original = records.get(entry_id)
                    if original is None:
                        fail(f"{path.name}: indexed id {entry_id} absent from canonical")
                        continue
                    if row.get("headword") != original[0]:
                        fail(f"Index headword differs from canonical for ID {entry_id}")
                    if row.get("normalized_headword") != norm_key(original[0]):
                        fail(f"Index normalization differs for ID {entry_id}")
                    if row.get("source_character_issue") != str(original[1]).lower():
                        fail(f"Index character issue flag differs for ID {entry_id}")
                    rel, anchor = row.get("file", ""), row.get("anchor", "")
                    if not rel.startswith("dictionary/") or not rel.endswith(".md"):
                        fail(f"Entry {entry_id}: invalid shard path {rel!r}")
                    if not anchor.startswith(f"entry-{entry_id}-"):
                        fail(f"Entry {entry_id}: unexpected anchor {anchor!r}")
                    by_headword[original[0]].add(rel)
                    shard_anchors[rel].add(anchor)
        if index_ids != seen_ids:
            fail(f"Index and canonical have different IDs: unindexed={len(seen_ids-index_ids)}, unknown={len(index_ids-seen_ids)}")
        for letter, wanted in manifest.get("letters", {}).items():
            if letters[letter] != wanted:
                fail(f"Letter {letter} count mismatch: {letters[letter]} vs {wanted}")
        duplicate_headwords = sum(1 for paths in by_headword.values() if len(paths) > 1)
        if duplicate_headwords:
            fail(f"{duplicate_headwords} identical headwords split across shard files")
        if check_shards:
            wanted_shards = manifest.get("shards_total")
            if wanted_shards is not None and len(shard_anchors) != wanted_shards:
                fail(f"Shard count differs from manifest: {len(shard_anchors)} vs {wanted_shards}")
            for rel, anchors in shard_anchors.items():
                shard = root / rel
                if not shard.is_file():
                    fail(f"Indexed shard missing: {rel}")
                    continue
                checked_shards += 1
                source = shard.read_text(encoding="utf-8")
                present = re.findall(r'<a id="([^"]+)"></a>', source)
                if len(present) != len(set(present)):
                    fail(f"Duplicate anchors in {rel}")
                if set(present) != anchors:
                    fail(f"Shard {rel} anchors inconsistent: missing={len(anchors-set(present))}, extra={len(set(present)-anchors)}")
                blocks = re.split(r'(?m)^<a id="([^"]+)"></a>\n', source)
                for i in range(1, len(blocks), 2):
                    anchor, body = blocks[i], blocks[i + 1]
                    match = re.match(
                        r'\A### ([^\n]*)\n\n- Entry ID: '+chr(96)+r'(\d+)'+chr(96)+r'\n- Source character issue: '+chr(96)+r'(true|false)'+chr(96)+r'\n\n',
                        body,
                    )
                    if not match:
                        fail(f"Could not parse derived entry block {rel}#{anchor}")
                        continue
                    entry_id = int(match.group(2))
                    if entry_id not in records:
                        continue
                    src_english, src_flag, src_persian, _ = records[entry_id]
                    if match.group(1) != src_english or match.group(3) != str(src_flag).lower():
                        fail(f"Derived heading/issue flag differs for {rel}#{anchor}")
                    remainder = body[match.end():]
                    if not (remainder.startswith(src_persian) and
                            remainder[len(src_persian):] in ("", "\n", "\n\n")):
                        fail(f"Derived definition differs from canonical for {rel}#{anchor}")

    if not manifest:
        advisories.append("Manifest checks skipped or unavailable; completeness is not certified.")
    if skip_index:
        advisories.append("Index checks skipped.")
    if not check_shards:
        advisories.append("Markdown shard checks not performed (use --check-shards).")
    advisories.append("Does NOT verify lexical correctness, edition attribution, or sense segmentation.")
    return {
        "ok": not failures,
        "checked": {
            "canonical_entries": count,
            "unique_ids": len(seen_ids),
            "indexed_entries": index_count if not skip_index else None,
            "markdown_shards": checked_shards,
        },
        "canonical_sha256": actual_hash,
        "source_character_issues": affected,
        "duplicate_headwords_split_across_shards": duplicate_headwords,
        "errors_count": len(failures),
        "errors": failures[:60],
        "advisories": advisories,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--skip-manifest", action="store_true", help="For isolated tests only")
    ap.add_argument("--skip-index", action="store_true", help="For isolated tests only")
    ap.add_argument("--check-shards", action="store_true")
    ap.add_argument("--output", type=Path, help="Optional JSON audit report destination")
    args = ap.parse_args()
    result = audit(args.root, skip_manifest=args.skip_manifest,
                   skip_index=args.skip_index, check_shards=args.check_shards)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
