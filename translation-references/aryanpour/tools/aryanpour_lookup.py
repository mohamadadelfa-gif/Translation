#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, unicodedata

ROOT = Path(__file__).resolve().parents[1]

def norm(s):
    return " ".join(unicodedata.normalize("NFKC", s).split()).casefold()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("headword")
    ap.add_argument("--prefix", action="store_true")
    args = ap.parse_args()

    q = norm(args.headword)
    first = args.headword.strip()[:1].upper()
    idx = ROOT / "index" / f"{first}-headwords.csv"
    if not idx.exists():
        print("No index bucket.")
        return

    with idx.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if args.prefix:
        hits = [r for r in rows if r["normalized_headword"].startswith(q)]
    else:
        hits = [r for r in rows if r["normalized_headword"] == q]

    if not hits:
        print("No match.")
        return

    for r in hits:
        print(f'{r["headword"]} | entry {r["entry_id"]}')
        print(f'{r["file"]}#{r["anchor"]}')
        print(f'source_character_issue={r["source_character_issue"]}')
        print()

if __name__ == "__main__":
    main()
