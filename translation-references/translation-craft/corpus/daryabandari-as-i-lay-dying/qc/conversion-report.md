# Conversion Report

## Source

- Work: *As I Lay Dying* / «گور به گور»
- Persian translator: نجف دریابندری
- Source format: image-based scanned PDF
- PDF pages processed: 157
- Main narrative pages: 6–154
- Narrator sections reconstructed: 59

## Method

1. Rendered the scan at 200 DPI.
2. Performed Persian OCR with the `fas` language model.
3. Preserved a raw OCR Markdown file for every PDF page under `raw-pages/`.
4. Reconstructed the 59 narrator-section boundaries from visible narrator headings in the scan.
5. Added PDF/printed-page markers to every structured section.
6. Joined OCR line wraps only within OCR-detected paragraphs; no stylistic rewriting was performed.

## Trust status

This is an **OCR-assisted working transcription**, not a certified diplomatic transcription.

Use it for:

- search;
- passage discovery;
- narrator comparison;
- preliminary translation-craft analysis;
- alignment preparation.

Before quoting exact wording or deriving a translation principle from a specific phrase, compare that passage with the corresponding PDF page image.

## Known OCR risks

- Persian letters with close visual forms;
- colloquial spellings;
- character names;
- punctuation and quotation marks;
- diacritics;
- page-top narrator headings;
- numerals and endnotes;
- tightly spaced words.

The `raw-pages/` files are retained so that later corrections to the structured files remain auditable.
