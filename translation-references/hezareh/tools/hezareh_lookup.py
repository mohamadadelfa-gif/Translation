#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index"

def norm(s):
    import re, unicodedata
    s = unicodedata.normalize("NFKC", s or "")
    return re.sub(r"\s+", " ", s.strip()).casefold()

def letter_for(s):
    if not s: return "OTHER"
    c = s[0].upper()
    return c if "A" <= c <= "Z" else "OTHER"

def main():
    if len(sys.argv) < 2:
        print("usage: python hezareh_lookup.py <headword>")
        raise SystemExit(2)
    q = norm(" ".join(sys.argv[1:]))
    p = INDEX / f"{letter_for(q)}-headwords.csv"
    if not p.exists():
        print("No index for query.")
        return
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    exact = [r for r in rows if r["normalized_headword"] == q]
    base = [r for r in rows if r["base_normalized_headword"] == q and r["normalized_headword"] != q]
    results = exact or base
    if not results:
        print("No exact normalized/base-normalized match.")
        return
    for r in results:
        print(json.dumps({
            "headword": r["headword"],
            "record_id": r["record_id"],
            "verification_status": r["verification_status"],
            "boundary_confidence": r["boundary_confidence"],
            "pdf_page": r["pdf_page"],
            "file": r["file"],
            "anchor": r["anchor"],
            "source_pointer": r["source_pointer"],
        }, ensure_ascii=False))

if __name__ == "__main__":
    main()
