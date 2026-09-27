#!/usr/bin/env python3
from pathlib import Path
import sqlite3, sys, re, unicodedata, json

DB = Path(__file__).with_name("hezareh_dictionary.sqlite")

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("‐", "-").replace("‑", "-")
    s = re.sub(r"\s+", " ", s.strip().casefold())
    return s.strip(" \t\r\n,;:.!?")

def base(s):
    return re.sub(r"\s*\(\d+\)\s*$", "", norm(s))

def rank(row):
    status = 0 if row["verification_status"] == "visually_checked" else 1
    conf = {"high":0, "medium":1, "low":2, "hint_only":3}.get(row["boundary_confidence"], 4)
    return (status, conf, row["pdf_page"], row["headword"])

def dedupe_and_override(rows):
    # Deduplicate same record target; visually checked wins over raw OCR
    # for the same base headword on the same canonical PDF page.
    rows = sorted(rows, key=rank)
    seen = set()
    checked_keys = {
        (r["pdf_page"], r["base_normalized_headword"])
        for r in rows if r["verification_status"] == "visually_checked"
    }
    out = []
    for r in rows:
        k = (r["pdf_page"], r["base_normalized_headword"])
        if r["verification_status"] == "raw_ocr" and k in checked_keys:
            continue
        dk = (r["headword"], r["pdf_page"], r["verification_status"], r["source_line_start"])
        if dk in seen:
            continue
        seen.add(dk)
        out.append(r)
    return out

def query(term, limit=12):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    qn, qb = norm(term), base(term)

    rows = list(con.execute("""
        SELECT * FROM entries
        WHERE normalized_headword = ? OR base_normalized_headword = ?
        ORDER BY CASE verification_status WHEN 'visually_checked' THEN 0 ELSE 1 END,
                 CASE boundary_confidence WHEN 'high' THEN 0 WHEN 'medium' THEN 1
                                          WHEN 'low' THEN 2 ELSE 3 END,
                 pdf_page
        LIMIT ?
    """, (qn, qb, limit * 3)))

    if not rows:
        # Exact alias/phrase match before prefix or broad full-text search.
        # Aliases come mainly from checked PHRASE lines inside verified entries.
        candidates = list(con.execute("""
            SELECT * FROM entries
            WHERE aliases_json LIKE ?
            ORDER BY CASE verification_status WHEN 'visually_checked' THEN 0 ELSE 1 END,
                     pdf_page
            LIMIT ?
        """, ("%" + term + "%", limit * 6)))
        exact_alias = []
        for r in candidates:
            try:
                aliases = json.loads(r["aliases_json"])
            except Exception:
                aliases = []
            if any(norm(a) == qn for a in aliases):
                exact_alias.append(r)
        rows = exact_alias

    if not rows:
        rows = list(con.execute("""
            SELECT * FROM entries
            WHERE normalized_headword LIKE ? OR base_normalized_headword LIKE ?
            ORDER BY CASE verification_status WHEN 'visually_checked' THEN 0 ELSE 1 END,
                     pdf_page
            LIMIT ?
        """, (qn + "%", qb + "%", limit * 3)))

    if not rows:
        # Quote the FTS phrase to keep punctuation-bearing dictionary queries stable.
        phrase = '"' + term.replace('"', '""') + '"'
        try:
            ids = [r[0] for r in con.execute(
                "SELECT id FROM entries_fts WHERE entries_fts MATCH ? LIMIT ?",
                (phrase, limit * 3)
            )]
        except sqlite3.OperationalError:
            ids = []
        if ids:
            marks = ",".join("?" for _ in ids)
            rows = list(con.execute(f"SELECT * FROM entries WHERE id IN ({marks})", ids))

    rows = dedupe_and_override(rows)[:limit]
    con.close()
    return rows

def show(r):
    print("=" * 76)
    print(f"{r['headword']}  | PDF p. {r['pdf_page']} | Part {r['part']:02d}")
    print(f"status: {r['verification_status']} | boundary: {r['boundary_confidence']}")
    print(f"source: {r['source_pointer']}")
    if r["verification_status"] == "raw_ocr":
        print("WARNING: raw OCR — verify against the source PDF when wording matters.")
    if r["entry_text"]:
        print()
        print(r["entry_text"])
    else:
        print()
        print("[Lookup hint only: no reliable entry boundary was reconstructed. Open the source page.]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python hezareh_lookup.py "headword or phrase"')
        raise SystemExit(2)
    term = " ".join(sys.argv[1:])
    results = query(term)
    if not results:
        print("No indexed headword match. Search the canonical page text as a fallback.")
        raise SystemExit(1)
    for r in results:
        show(r)
