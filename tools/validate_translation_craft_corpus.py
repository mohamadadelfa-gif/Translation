#!/usr/bin/env python3
from pathlib import Path
import csv, json, hashlib, sys

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "translation-preparation" / "translation-craft-corpus"
CSV = CORPUS / "paired-sections.csv"

def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

errors = []
if not CSV.exists():
    errors.append(f"Missing {CSV}")
else:
    with CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 59:
        errors.append(f"Expected 59 aligned sections, found {len(rows)}.")
    for r in rows:
        en = ROOT / r["english_path"]
        fa = ROOT / r["persian_path"]
        for kind, p, expected in [
            ("English", en, r["english_sha256"]),
            ("Persian", fa, r["persian_sha256"]),
        ]:
            if not p.exists():
                errors.append(f"Missing {kind} section {r['section']}: {p}")
            elif sha256(p) != expected:
                errors.append(f"Checksum mismatch {kind} section {r['section']}: {p}")

craft = ROOT / "translation-references" / "translation-craft" / "daryabandari" / "parallel-cases.jsonl"
if not craft.exists():
    errors.append(f"Missing {craft}")
else:
    for n, line in enumerate(craft.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        obj = json.loads(line)
        for key in ("english_source_path", "persian_source_path"):
            p = ROOT / obj[key]
            if not p.exists():
                errors.append(f"Pilot case {obj.get('id')} has broken {key}: {p}")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("VALIDATION OK")
print("- 59 English/Persian section pairs present")
print("- section checksums match")
print("- pilot source pointers resolve")
