# Persian OCR and PDF text-layer QA: conservative starter

This is a **working, standard-library Python 3.9+ anomaly reporter**, not an OCR engine or automatic Persian corrector. All findings are unverified candidates. It never changes the input file.

## Run from this directory
~~~bash
python check_ocr.py SAMPLE-INPUT.jsonl --format jsonl --output report.jsonl --summary summary.json
python check_ocr.py raw.txt --output report.jsonl --summary summary.json
python -m unittest -v test_check_ocr.py
~~~

## Input and output
- For plain UTF-8 text, each physical line becomes a record with its line number.
- For page-aware JSONL, supply one object per line with a required text string, optional id and optional positive integer page. See SAMPLE-INPUT.jsonl.
- report.jsonl contains rule ID, severity, source ID/page/line, Unicode character offsets, the suspicious span, surrounding context, and a candidate-only character suggestion where applicable.
- summary.json contains numbers of records scanned and flagged issues. Unflagged text is not automatically certified accurate.
- Reports quote snippets of input: **do not publish reports of private material**.

## Implemented checks
- U001–U005: replacement glyph, Arabic-variant kaf/yeh, bidirectional controls, tatweel, Arabic presentation-form characters.
- W001–W004: possible gaps after mi/nemi, before plural ha, repeated internal spaces, and ZWNJ next to non-letter/word edge.
- O001: a narrow, experimental heuristic for possibly reversed Persian word order in PDF text-layer output. It is deliberately low severity; it cannot recover reading order.

## Evidence and limitations
VALIDATION-CASES.jsonl has one **visually checked** case from Yousef 2018, PDF p.151 / printed p.132. It demonstrates a PDF text-layer reading-order error, not an OCR-engine recognition error. Other test strings are synthetic; neither proves what a historical source printed.
The PDF has bilingual examples and tables; rigorous OCR repair requires visual source pages, layout coordinates, and a larger manually adjudicated gold set. Use REVIEW-POLICY.md before any corrective action.

## Next milestones
1. Collect 30–100 visually checked samples from multiple genres and label text-layer vs OCR source.
2. Attach page-image coordinates to findings and track reviewer judgments.
3. Measure detection precision and false-positive rates.
4. Only then develop an optional, explicitly approved and fully logged derived-text correction exporter.
