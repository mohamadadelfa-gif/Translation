#!/usr/bin/env python3
"""Conservative Persian OCR/text-layer anomaly reporter (no corrections).

Input: UTF-8 plain text (one record per physical line), or JSONL with a required
text string plus optional id and page. Output: JSONL issue records.
Python 3.9+; standard library only. This is a QA aid, NOT a Persian spellchecker.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import unicodedata

PERSIAN = r"\u0621-\u064a\u0671-\u06d3\u06fa-\u06fc"
RULES = (
    ("U001_REPLACEMENT", "high", re.compile("\ufffd"),
     "Unicode replacement character: extraction may have lost a glyph", None),
    ("U002_ARABIC_KAF_YEH", "medium", re.compile("[\u0643\u064a]"),
     "Arabic-form kaf/yeh; compare with intended Persian character", {"\u0643": "\u06a9", "\u064a": "\u06cc"}),
    ("U003_BIDI_CONTROL", "low", re.compile("[\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]"),
     "Bidirectional control/mark; may be intentional in bilingual text", None),
    ("U004_TATWEEL", "low", re.compile("\u0640"),
     "Tatweel character; inspect visual source", None),
    ("W001_GAP_AFTER_MI", "low", re.compile(rf"(?<![{PERSIAN}])(ن?می)[ \t]+([{PERSIAN}]{{2,}})"),
     "Potential missing half-space after verbal mi-/nemi- prefix", None),
    ("W002_GAP_BEFORE_HA", "low", re.compile(rf"([{PERSIAN}]{{2,}})[ \t]+(ها)(?![{PERSIAN}])"),
     "Potential separated plural suffix -ha; alternative readings exist", None),
    ("W003_REPEATED_SPACES", "low", re.compile(r"(?<=\S) {2,}(?=\S)"),
     "Repeated internal spaces; may reflect page layout", None),
    ("W004_EDGE_ZWNJ", "medium", re.compile("(?<![\u0621-\u06fc])\u200c|\u200c(?![\u0621-\u06fc])"),
     "Zero-width non-joiner not surrounded by Persian/Arabic letters", None),
    ("O001_POSSIBLE_REVERSE_ORDER", "low", re.compile(r"^(?:رفت|آمد|بود|شد|کرد|گفت|خواند)(?:[ \t]+[\u0621-\u06fc]+){1,12}[ \t]+(?:از|به|با|در)$"),
     "Possible reversed Persian word order; heuristic only", None),
)
PRESENTATION = re.compile("[\ufb50-\ufdff\ufe70-\ufeff]")

def check(text: str, *, source_id: str | None = None, page: int | None = None,
          line: int | None = None) -> list[dict]:
    """Report suspicious spans; leave text unchanged."""
    findings = []
    for rule, severity, pattern, rationale, mapping in RULES:
        for m in pattern.finditer(text):
            span = m.group(0)
            suggestion = mapping.get(span) if mapping else None
            findings.append({
                "source_id": source_id, "page": page, "line": line,
                "rule_id": rule, "severity": severity,
                "start": m.start(), "end": m.end(), "observed": span,
                "context": text[max(0, m.start()-22): min(len(text), m.end()+22)],
                "candidate_only": suggestion, "message": rationale,
                "verification_status": "unverified_candidate",
            })
    for m in PRESENTATION.finditer(text):
        ch = m.group(0)
        findings.append({
            "source_id": source_id, "page": page, "line": line,
            "rule_id": "U005_PRESENTATION_FORM", "severity": "medium",
            "start": m.start(), "end": m.end(), "observed": ch,
            "context": text[max(0, m.start()-22):min(len(text), m.end()+22)],
            "candidate_only": unicodedata.normalize("NFKC", ch),
            "message": "Arabic presentation-form glyph; verify intended characters",
            "verification_status": "unverified_candidate",
        })
    return sorted(findings, key=lambda v: (v["start"], v["end"], v["rule_id"]))

def iter_documents(path: Path, mode: str):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for line_num, row in enumerate(f, 1):
            if mode == "lines":
                yield {"id": f"line-{line_num}", "page": None, "text": row.rstrip("\r\n"), "line": line_num}
            else:
                if not row.strip():
                    continue
                data = json.loads(row)
                if not isinstance(data, dict) or not isinstance(data.get("text"), str):
                    raise ValueError(f"Input JSONL line {line_num}: expected object with string 'text'")
                if data.get("page") is not None and (type(data["page"]) is not int or data["page"] < 1):
                    raise ValueError(f"Input JSONL line {line_num}: page must be a positive integer or null")
                yield {"id": str(data.get("id", f"record-{line_num}")), "page": data.get("page"),
                       "text": data["text"], "line": line_num}

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path, help="UTF-8 raw text or JSONL")
    p.add_argument("--format", choices=("lines", "jsonl"), default="lines")
    p.add_argument("--output", type=Path, required=True, help="Output review JSONL path")
    p.add_argument("--summary", type=Path, help="Optional summary JSON path")
    args = p.parse_args(argv)
    if args.input.resolve() == args.output.resolve():
        p.error("Output must not overwrite the input")
    if args.summary and (args.summary.resolve() == args.input.resolve() or args.summary.resolve() == args.output.resolve()):
        p.error("Summary path must be distinct from input and output")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    inspected = 0
    with args.output.open("w", encoding="utf-8", newline="\n") as out:
        for doc in iter_documents(args.input, args.format):
            inspected += 1
            for issue in check(doc["text"], source_id=doc["id"], page=doc["page"], line=doc["line"]):
                counts[issue["rule_id"]] += 1
                out.write(json.dumps(issue, ensure_ascii=False) + "\n")
    summary = {"input": str(args.input), "records_scanned": inspected,
               "total_flags": sum(counts.values()), "by_rule": dict(sorted(counts.items())),
               "status": "candidate_flags_only; no source modified"}
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
