#!/usr/bin/env python3
"""Aryanpour Phase 4: source-evidence audit, NOT a semantic dictionary parser.

Reads frozen LD2 export + source-anchored convention register; inventories
candidate abbreviation forms, apparent references and bracket notations.
No automatic meaning/label/link approval and no canonical writes.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

from build_annotation_pilot import load_records, search_key

PAREN = re.compile(r"\(([^()\r\n]{1,120})\)")
SQUARE = re.compile(r"\[([^\[\]\r\n]{1,120})\]")
MIRRORED = re.compile(r"\]([^\[\]\r\n]{1,120})\[")
ACCEPTED_CLASSES = {
    "abbreviation_shape", "reference_surface", "usage_context_surface",
    "embedded_parenthetical", "reversed_bracket_surface",
}


def compare_form(value: str) -> str:
    """Only comparison key. Source spelling and spacing stay unchanged."""
    return re.sub(r"\s+", "", value)


def reference_shape(raw: str):
    """Detect equals-sign position WITHOUT declaring a cross-reference."""
    text = raw.strip()
    before, after = text.startswith("="), text.endswith("=")
    if before and after:
        return "ambiguous_both_ends", None
    if before:
        target = text[1:].strip()
        return ("prefix_equals", target) if target else ("empty_equals", None)
    if after:
        target = text[:-1].strip()
        return ("suffix_equals", target) if target else ("empty_equals", None)
    return None, None


def spans(text: str):
    """Yield literal non-overlapping simple bracket/parenthesis spans."""
    matches = []
    for matcher, kind in ((PAREN, "parenthesis"), (SQUARE, "square_bracket"),
                          (MIRRORED, "mirrored_square_bracket")):
        for match in matcher.finditer(text):
            matches.append((match.start(), match.end(), kind, match.group(0),
                            match.group(1)))
    matches.sort()
    for index, item in enumerate(matches):
        if index and item[0] < matches[index - 1][1]:
            raise ValueError("Overlapping syntactic spans; manual investigation needed")
        yield item


def verify_register(path: Path, entries: dict[int, dict]):
    seen = set()
    result = []
    with path.open(encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            rule_id = item.get("rule_id")
            ident = item.get("canonical_id")
            if not isinstance(rule_id, str) or rule_id in seen:
                raise ValueError(f"Invalid/duplicate convention ID {rule_id!r}")
            seen.add(rule_id)
            if item.get("candidate_class") not in ACCEPTED_CLASSES:
                raise ValueError(f"Unrecognized candidate class {rule_id}")
            if (item.get("editorial_status") != "unverified" or
                    item.get("evidence_grade") != "export_surface_only" or
                    item.get("source_documentation_status") != "not_located" or
                    item.get("semantic_expansion") is not None or
                    item.get("verified_scope") is not None or
                    item.get("verified_reference_relation") is not None):
                raise ValueError(f"Semantic claim not supported for {rule_id}")
            row = entries.get(ident)
            if not row or item.get("source_field") != "persian":
                raise ValueError(f"Missing or invalid source row for {rule_id}")
            surface = item.get("source_text")
            if not isinstance(surface, str) or not surface or surface not in row["persian"]:
                raise ValueError(f"Source surface not present for {rule_id}")
            if not isinstance(item.get("surface_key"), str):
                raise ValueError(f"Missing comparison key in {rule_id}")
            # Registered surface must correspond to the literal observed bracket.
            if item["candidate_class"] == "reversed_bracket_surface":
                expected = "]" + item["surface_key"] + "["
                if expected != surface:
                    raise ValueError(f"Bracket surface mismatch in {rule_id}")
            elif (surface.startswith("(") and surface.endswith(")") and
                  compare_form(surface[1:-1]) != compare_form(item["surface_key"])):
                raise ValueError(f"Parenthesis surface mismatch in {rule_id}")
            result.append(item)
    if not result:
        raise ValueError("Empty evidence register")
    return result


def scan(root: Path, register: Path, output_candidates: Path | None = None, max_examples: int = 5):
    if max_examples < 1:
        raise ValueError("max_examples must be >= 1")
    rows, headword_index, canonical_hash = load_records(root)
    entries = {row["id"]: row for row in rows}
    rules = verify_register(register, entries)
    form_keys = {compare_form(x["surface_key"]) for x in rules
                 if x["candidate_class"] == "abbreviation_shape"}
    count = Counter()
    forms = Counter()
    ref_statuses = Counter()
    examples = defaultdict(list)
    candidates_count = 0
    file_handle = None
    try:
        if output_candidates is not None:
            output_candidates.parent.mkdir(parents=True, exist_ok=True)
            file_handle = output_candidates.open("w", encoding="utf-8")
        for row in rows:
            text = row["persian"]
            for start, end, kind, literal, interior in spans(text):
                if literal != text[start:end]:
                    raise ValueError(f"Broken source offset for {row['id']}")
                ref_form, target = reference_shape(interior)
                candidate = {
                    "canonical_id": row["id"],
                    "headword": row["english"],
                    "source_field": "persian",
                    "span": [start, end],
                    "surface_literal": literal,
                    "bracket_shape": kind,
                    "candidate_type": None,
                    "semantic_role_verified": False,
                    "lexical_sense": None,
                    "label_scope": None,
                    "review_status": "unverified",
                }
                if ref_form:
                    candidate["candidate_type"] = "apparent_reference_surface"
                    candidate["equals_position"] = ref_form
                    candidate["target_literal"] = target
                    ids = headword_index.get(search_key(target), []) if target else []
                    candidate["target_exact_lookup_ids"] = list(ids)
                    status = ("unique_exact_text_match" if len(ids) == 1 else
                              "multiple_exact_text_matches" if ids else
                              "no_exact_text_match")
                    candidate["target_lookup_status"] = status
                    candidate["verified_link"] = None
                    ref_statuses[f"{ref_form}:{status}"] += 1
                elif kind == "mirrored_square_bracket":
                    candidate["candidate_type"] = "mirrored_bracket_surface"
                elif compare_form(interior) in form_keys:
                    candidate["candidate_type"] = "registered_abbreviation_shape"
                    candidate["proposed_expansion"] = None
                else:
                    candidate["candidate_type"] = "unclassified_enclosed_text"
                label = candidate["candidate_type"]
                count[label] += 1
                count["all_enclosed_candidates"] += 1
                count["bracket:" + kind] += 1
                forms[(label, compare_form(interior))] += 1
                if len(examples[label]) < max_examples:
                    examples[label].append({
                        "id": row["id"], "headword": row["english"],
                        "surface": literal, "offset": [start, end],
                        "target_status": candidate.get("target_lookup_status"),
                    })
                if file_handle is not None:
                    file_handle.write(json.dumps(candidate, ensure_ascii=False) + "\n")
                candidates_count += 1
    finally:
        if file_handle is not None:
            file_handle.close()

    return {
        "schema": "aryanpour.convention-audit.v1",
        "canonical_sha256": canonical_hash,
        "canonical_records": len(rows),
        "source_verified_evidence_cases": len(rules),
        "semantic_conventions_approved": 0,
        "candidate_occurrences": candidates_count,
        "candidate_counts": dict(sorted(count.items())),
        "reference_lookup_statuses": dict(sorted(ref_statuses.items())),
        "top_forms": [
            {"candidate_type": kind, "comparison_key": key, "occurrences": n}
            for (kind, key), n in forms.most_common(30)
        ],
        "examples": dict(examples),
        "interpretation_limits": [
            "No signed-off source edition or abbreviation guide",
            "An exact target headword match does not prove an editorial cross-reference",
            "Visual bracket orientation can be affected by RTL rendering",
            "Registry text verifies substrings in LD2 export, not original print conventions",
            "No semantic field may be approved by this automated scan",
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--register", type=Path)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--candidates", type=Path)
    args = ap.parse_args()
    report = scan(args.root, args.register or args.root / "conventions" / "register.jsonl",
                  output_candidates=args.candidates)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "canonical_records": report["canonical_records"],
        "source_evidence_cases": report["source_verified_evidence_cases"],
        "semantic_conventions_approved": 0,
        "candidate_counts": report["candidate_counts"],
        "reference_lookup_statuses": report["reference_lookup_statuses"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
