#!/usr/bin/env python3
import csv, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index"

def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("\xa0", " ").replace("ي", "ی").replace("ك", "ک")
    return re.sub(r"\s+", " ", s).strip().casefold()

def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    if len(sys.argv) < 2:
        print("usage: python thesaurus_lookup.py <Persian term or phrase>")
        raise SystemExit(2)

    q = norm(" ".join(sys.argv[1:]))

    # 1) Strong source-marked terms.
    lead = [r for r in load_csv(INDEX / "lead-terms.csv") if r["normalized_term"] == q]
    if lead:
        print("LEAD TERMS")
        for r in lead:
            print(f'{r["term"]} -> entry {r["entry_id"]} {r["entry_heading"]} -> {r["file"]}#{r["anchor"]}')
        return

    # 2) Occurrence index.
    first = q[:1]
    shard_map = [r for r in load_csv(INDEX / "TERM-SHARD-MAP.csv") if r["initial"] == first]
    found = []
    for sm in shard_map:
        for r in load_csv(ROOT / sm["file"]):
            if r["normalized_term"] == q:
                found.append(r)

    if not found:
        print("No exact indexed occurrence.")
        return

    print("OCCURRENCES — navigation only; inspect full entries")
    for r in found:
        print(f'{r["term"]} -> entry {r["entry_id"]} {r["entry_heading"]} -> {r["file"]}#{r["anchor"]}')

if __name__ == "__main__":
    main()
