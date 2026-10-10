#!/usr/bin/env python3
"""Deterministic, non-authoritative Aryanpour annotation pilot.

Produces stratified evidence records and tentative candidates. Never rewrites
dictionary entries or approves lexical senses, labels, or cross-references.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import unicodedata

PAREN = re.compile(r"\(([^()\r\n]{1,120})\)")
# Observed strings for pilot triage, NOT verified abbreviations or expansions.
LABEL_SHAPES = frozenset({
    "طب", "ج.ش.", "گ.ش.", "مو.", "حق.", "ش.", "تش.", "نظ.",
    "مع.", "نج.", "ز.ع.", "ر.", "م.م.", "د.گ.", "د.",
})
GROUPS = (
    "leading_equals", "abbreviation_form", "other_leading_parenthetical",
    "embedded_parenthetical", "multi_comma_unsegmented", "plain_definition",
    "source_character_issue", "unusual_headword", "duplicate_headword",
)
SEED_IDS = (3, 4, 12, 25, 28, 34, 35, 2176, 2588, 2589, 9674,
            19758, 30098, 36203, 37142, 49948)


def search_key(value: str) -> str:
    """Search-only comparison; source fields remain unmodified."""
    return " ".join(unicodedata.normalize("NFKC", value).split()).casefold()


def abbreviation_key(value: str) -> str:
    return re.sub(r"\s+", "", value)


def preceding_parenthetical_group(text: str, start: int) -> bool:
    return re.fullmatch(r"\s*(?:\([^()\r\n]*\)\s*)*", text[:start]) is not None


def observations(record: dict, headwords: dict[str, list[int]]):
    text = record["persian"]
    candidates, groups = [], set()
    parens = list(PAREN.finditer(text))
    for match in parens:
        inner = match.group(1)
        prefix = preceding_parenthetical_group(text, match.start())
        candidate = {
            "span": [match.start(), match.end()],
            "source_text": match.group(0),
            "source_field": "persian",
            "status": "unverified_candidate",
            "verified_semantic_role": None,
        }
        if inner.lstrip().startswith("="):
            target = inner.strip()[1:].strip()
            ids = headwords.get(search_key(target), []) if target else []
            candidate.update({
                "candidate_type": "apparent_reference",
                "target_literal": target,
                "target_exact_lookup_ids": list(ids),
                "target_lookup_status": (
                    "unique_exact_text_match" if len(ids) == 1 else
                    "multiple_exact_text_matches" if ids else "not_found"),
                "verified_cross_reference": None,
            })
            groups.add("leading_equals" if prefix else "embedded_parenthetical")
        elif prefix and abbreviation_key(inner) in LABEL_SHAPES:
            candidate.update({
                "candidate_type": "abbreviation_form",
                "abbreviation_form_key": abbreviation_key(inner),
                "abbreviation_expansion": None,
                "verified_label": None,
            })
            groups.add("abbreviation_form")
        elif prefix:
            candidate["candidate_type"] = "other_leading_parenthetical"
            groups.add("other_leading_parenthetical")
        else:
            candidate["candidate_type"] = "embedded_parenthetical"
            groups.add("embedded_parenthetical")
        candidates.append(candidate)
    if not parens:
        groups.add("multi_comma_unsegmented" if
                   text.count("،") >= 3 or text.count(",") >= 3
                   else "plain_definition")
    if record["source_character_issue"]:
        groups.add("source_character_issue")
    if any(c in record["english"] for c in (chr(96), "(", ")", "<", ">")):
        groups.add("unusual_headword")
    if len(headwords[search_key(record["english"])]) > 1:
        groups.add("duplicate_headword")
    return candidates, groups


def load_records(root: Path):
    rows, headwords = [], defaultdict(list)
    digest = hashlib.sha256()
    with (root / "aryanpour-english-persian.jsonl").open("rb") as f:
        for line_num, raw in enumerate(f, 1):
            digest.update(raw)
            row = json.loads(raw.decode("utf-8"))
            if (type(row.get("id")) is not int or
                    not all(isinstance(row.get(k), str) for k in
                            ("english", "persian", "original_definition_markup")) or
                    type(row.get("source_character_issue")) is not bool):
                raise ValueError(f"Invalid canonical record {line_num}")
            rows.append(row)
            headwords[search_key(row["english"])].append(row["id"])
    if len(rows) != len({r["id"] for r in rows}):
        raise ValueError("Duplicate canonical IDs")
    return rows, dict(headwords), digest.hexdigest()


def load_index(root: Path):
    path = root / "index" / "headwords-master.csv"
    result = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            ident = int(row["entry_id"])
            if ident in result:
                raise ValueError(f"Duplicate index id {ident}")
            result[ident] = {"shard": row["file"], "anchor": row["anchor"]}
    return result


def load_reviews(path: Path, records: dict[int, dict]):
    reviews = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            ident = row["canonical_id"]
            if ident in reviews or ident not in records:
                raise ValueError(f"Duplicate/missing review ID {ident}")
            if row["headword"] != records[ident]["english"]:
                raise ValueError(f"Review headword mismatch at {ident}")
            field, surface = row["source_field"], row["observed_surface"]
            if field not in ("english", "persian") or not surface or surface not in records[ident][field]:
                raise ValueError(f"Review evidence absent from source entry {ident}")
            if (row.get("review_scope") != "ld2_export_surface_only" or
                    row.get("semantic_interpretation_status") != "not_verified"):
                raise ValueError(f"Unjustified semantic review at {ident}")
            reviews[ident] = row
    return reviews


def build(root: Path, *, reviews_path: Path, quota: int = 12,
          seed: str = "aryanpour-phase3-v1", seed_ids=SEED_IDS):
    if quota < 1:
        raise ValueError("quota must be positive")
    records, headwords, source_hash = load_records(root)
    index = load_index(root)
    by_id = {row["id"]: row for row in records}
    if set(index) != set(by_id):
        raise ValueError("Master index and canonical IDs differ")
    reviews = load_reviews(reviews_path, by_id)
    required = set(seed_ids) | set(reviews)
    if not required <= set(by_id):
        raise ValueError(f"Missing seed IDs: {sorted(required - set(by_id))}")
    population = Counter()
    rankings = {group: [] for group in GROUPS}
    for item in records:
        _, groups = observations(item, headwords)
        population.update(groups)
        for group in groups:
            rank = hashlib.sha256(f"{seed}:{group}:{item['id']}".encode("utf-8")).hexdigest()
            rankings[group].append((rank, item["id"]))
    selections = {group: [ident for _, ident in sorted(rankings[group])[:quota]]
                  for group in GROUPS}
    selected = required | {i for picks in selections.values() for i in picks}
    sample, sample_populations = [], Counter()
    for ident in sorted(selected):
        item = by_id[ident]
        candidates, groups = observations(item, headwords)
        for candidate in candidates:
            start, end = candidate["span"]
            if item["persian"][start:end] != candidate["source_text"]:
                raise ValueError(f"Invalid candidate span at {ident}")
        sample_populations.update(groups)
        sample.append({
            "schema": "aryanpour.annotation-pilot.v1",
            "canonical_id": ident,
            "english_exact": item["english"],
            "persian_exact": item["persian"],
            "original_markup_sha256": hashlib.sha256(
                item["original_definition_markup"].encode("utf-8")).hexdigest(),
            "source_character_issue": item["source_character_issue"],
            "source_locator": index[ident],
            "sample_strata": sorted(groups),
            "candidates": candidates,
            "export_surface_review": reviews.get(ident),
            "verified_senses": None,
            "verified_labels": None,
            "verified_cross_references": None,
            "verified_examples": None,
            "translation_approval": False,
        })
    report = {
        "schema": "aryanpour.annotation-pilot.report.v1",
        "canonical_sha256": source_hash,
        "entries_scanned": len(records),
        "sampling_seed": seed,
        "quota_per_group": quota,
        "sampling_algorithm": "SHA256(seed:group:id) ascending",
        "population_per_group": {g: population[g] for g in GROUPS},
        "quota_selected_ids": selections,
        "sample_size": len(sample),
        "sample_memberships_per_group": {g: sample_populations[g] for g in GROUPS},
        "curated_surface_reviews": len(reviews),
        "semantically_approved_records": 0,
        "limits": [
            "Source is LD2 export, not OCR or independently verified printed edition",
            "Parenthetical roles remain candidates; label expansions are unverified",
            "Exact reference target lookup is not verified lexicographic linkage",
            "Never segment comma-separated equivalents into automatic senses",
        ],
    }
    return report, sample


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--reviews", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--sample", type=Path, required=True)
    p.add_argument("--quota", type=int, default=12)
    p.add_argument("--seed", default="aryanpour-phase3-v1")
    a = p.parse_args()
    report, rows = build(a.root, reviews_path=a.reviews or
                         a.root / "pilot" / "reviewed_surfaces.jsonl",
                         quota=a.quota, seed=a.seed)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.sample.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    a.sample.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows),
                        encoding="utf-8")
    print(json.dumps({
        "entries_scanned": report["entries_scanned"],
        "population_per_group": report["population_per_group"],
        "sample_size": report["sample_size"],
        "curated_surface_reviews": report["curated_surface_reviews"],
        "semantically_approved_records": 0,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
