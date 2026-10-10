#!/usr/bin/env python3
"""Read-only LD2 markup inventory for Aryanpour.

Produces a corpus-level evidence report and (optionally) conservative entry
observations. Does not interpret tags as senses, grammatical categories,
examples, or cross-references without independent evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

TAG = re.compile(r"<([^<>]*)>")
TAG_NAME = re.compile(r"^[^\W\d][\w.:-]*$", re.UNICODE)
LEADING_PARENTHETICAL = re.compile(r"^\s*\(([^()\r\n]{1,60})\)")
ANY_PARENTHETICAL = re.compile(r"\(([^()\r\n]{1,60})\)")


def projection(markup: str) -> str:
    """The exact historic export operation; no semantic normalization."""
    return re.sub(r"<[^>]*>", "", re.sub(r"<n\s*/>", "\n", markup, flags=re.I))


def markup_observation(markup: str) -> dict:
    """Lossless tag inventory and tentative text observations.

    'balanced' is lexical nesting validation, not proof that tag semantics
    are known or that an XML parser would accept the LD2 dialect.
    """
    tag_names = []
    openings = Counter()
    closings = Counter()
    empty_tags = Counter()
    errors = []
    stack = []
    seen_tag_spans = []
    for match in TAG.finditer(markup):
        body = match.group(1).strip()
        closing = body.startswith("/")
        empty = body.endswith("/") and not closing
        name_part = body[1:].strip() if closing else body[:-1].strip() if empty else body
        name = name_part.split(None, 1)[0] if name_part else ""
        if not TAG_NAME.fullmatch(name):
            errors.append("invalid_or_empty_tag_name")
            continue
        tag_names.append(name)
        seen_tag_spans.append([match.start(), match.end(), name])
        if closing:
            closings[name] += 1
            if not stack:
                errors.append("unexpected_closing_tag")
            elif stack[-1] != name:
                errors.append("mismatched_closing_tag")
                # Remain conservative; do not pretend we repaired the markup.
                if name in stack:
                    while stack and stack[-1] != name:
                        stack.pop()
                    if stack:
                        stack.pop()
            else:
                stack.pop()
        elif empty:
            empty_tags[name] += 1
        else:
            openings[name] += 1
            stack.append(name)
    if stack:
        errors.append("unclosed_tag")
    # Any literal angle brackets outside recognized <...> can indicate
    # truncation or data rather than markup; report without modifying text.
    uncovered = TAG.sub("", markup)
    if "<" in uncovered or ">" in uncovered:
        errors.append("unmatched_angle_bracket")
    visible = projection(markup)
    candidate = LEADING_PARENTHETICAL.search(visible)
    parentheticals = ANY_PARENTHETICAL.findall(visible)
    return {
        "tag_names": tag_names,
        "opening_tags": dict(openings),
        "closing_tags": dict(closings),
        "empty_tags": dict(empty_tags),
        "tag_spans": seen_tag_spans,
        "tag_signature": " ".join(tag_names),
        "markup_issues": sorted(set(errors)),
        "leading_parenthetical_candidate": candidate.group(1) if candidate else None,
        "parenthetical_occurrences": parentheticals,
        # Neither periods nor commas establish lexicographic senses.
        "sense_boundaries": None,
        "grammatical_labels": None,
        "examples": None,
        "cross_references": None,
        "interpretation_status": "unsegmented_requires_source_convention",
    }


def analyze(root: Path, sample_limit: int = 3, candidates_path: Path | None = None) -> dict:
    if sample_limit < 1:
        raise ValueError("sample_limit must be >= 1")
    canonical = root / "aryanpour-english-persian.jsonl"
    tags = Counter()
    opening = Counter()
    closing = Counter()
    empty = Counter()
    signatures = Counter()
    issue_types = Counter()
    parenthetical_values = Counter()
    stats = Counter()
    signature_examples = defaultdict(list)
    issue_examples = defaultdict(list)
    leading_examples = []
    non_standard = []
    # Use a short signature digest for automated comparison of this analysis;
    # canonical bytes are not changed or replicated in this report.
    h = hashlib.sha256()
    destination = None
    try:
        if candidates_path:
            candidates_path.parent.mkdir(parents=True, exist_ok=True)
            destination = candidates_path.open("w", encoding="utf-8")
        with canonical.open("rb") as source:
            for line_number, raw_line in enumerate(source, 1):
                h.update(raw_line)
                if not raw_line.strip():
                    raise ValueError(f"Blank canonical record at line {line_number}")
                item = json.loads(raw_line.decode("utf-8"))
                entry_id = item["id"]
                english = item["english"]
                markup = item["original_definition_markup"]
                visible = item["persian"]
                if not isinstance(markup, str) or not isinstance(visible, str):
                    raise ValueError(f"Invalid record text at line {line_number}")
                if projection(markup) != visible:
                    raise ValueError(f"Canonical projection mismatch at entry {entry_id}")
                obs = markup_observation(markup)
                stats["records"] += 1
                if not obs["tag_names"]:
                    stats["records_without_markup_tags"] += 1
                tags.update(obs["tag_names"])
                opening.update(obs["opening_tags"])
                closing.update(obs["closing_tags"])
                empty.update(obs["empty_tags"])
                signatures[obs["tag_signature"]] += 1
                if len(signature_examples[obs["tag_signature"]]) < sample_limit:
                    signature_examples[obs["tag_signature"]].append(
                        {"id": entry_id, "headword": english})
                if obs["markup_issues"]:
                    stats["records_with_markup_issues"] += 1
                for code in obs["markup_issues"]:
                    issue_types[code] += 1
                    if len(issue_examples[code]) < sample_limit:
                        issue_examples[code].append(
                            {"id": entry_id, "headword": english, "markup": markup[:300]})
                if obs["leading_parenthetical_candidate"] is not None:
                    stats["leading_parenthetical_candidates"] += 1
                    parenthetical_values[obs["leading_parenthetical_candidate"]] += 1
                    if len(leading_examples) < sample_limit * 4:
                        leading_examples.append(
                            {"id": entry_id, "headword": english,
                             "candidate": obs["leading_parenthetical_candidate"]})
                if obs["parenthetical_occurrences"]:
                    stats["records_with_parentheticals_anywhere"] += 1
                if item.get("source_character_issue"):
                    stats["source_character_flagged_records"] += 1
                if destination is not None:
                    record = {
                        "source": "aryanpour_ld2_export",
                        "canonical_id": entry_id,
                        "headword": english,
                        "original_markup_sha256": hashlib.sha256(markup.encode("utf-8")).hexdigest(),
                        "tag_signature": obs["tag_signature"],
                        "markup_issues": obs["markup_issues"],
                        "leading_parenthetical_candidate": obs["leading_parenthetical_candidate"],
                        "sense_boundaries": None,
                        "grammatical_labels": None,
                        "examples": None,
                        "cross_references": None,
                        "interpretation_status": obs["interpretation_status"],
                    }
                    destination.write(json.dumps(record, ensure_ascii=False) + "\n")
    finally:
        if destination is not None:
            destination.close()
    report = {
        "analysis_version": "aryanpour.markup.inventory.v1",
        "canonical_sha256": h.hexdigest(),
        "entries_examined": stats["records"],
        "scope": "structured LD2 export; not OCR",
        "counts": dict(stats),
        "distinct_tag_names": len(tags),
        "tag_occurrences": dict(tags.most_common()),
        "opening_tags": dict(opening.most_common()),
        "closing_tags": dict(closing.most_common()),
        "self_closing_tags": dict(empty.most_common()),
        "distinct_tag_signatures": len(signatures),
        "top_tag_signatures": [
            {"signature": signature, "count": count,
             "examples": signature_examples[signature]}
            for signature, count in signatures.most_common(20)
        ],
        "markup_issue_types": dict(issue_types.most_common()),
        "markup_issue_examples": dict(issue_examples),
        "top_leading_parenthetical_candidates": parenthetical_values.most_common(30),
        "leading_parenthetical_examples": leading_examples,
        "interpretation_policy": {
            "markup_tags": "inventory_only; no tag assigned a semantic role",
            "parentheses": "textual candidates only; not verified labels/references",
            "commas_and_periods": "not sense delimiters without explicit evidence",
            "senses": "unsegmented",
            "cross_references": "not resolved",
            "original_records_modified": False,
        },
    }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="Write full report JSON here")
    parser.add_argument("--candidates", type=Path, help="Optional derived review-only JSONL")
    parser.add_argument("--sample-limit", type=int, default=3)
    args = parser.parse_args()
    report = analyze(args.root, sample_limit=args.sample_limit, candidates_path=args.candidates)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    # Print reviewable evidence and counts into GitHub Actions job log.
    print(output)


if __name__ == "__main__":
    main()
