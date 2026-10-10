# Recommended workflow — source-faithful multilingual OCR and bilingual dictionaries

**Status: PROPOSED protocol, not a claim of implemented end-to-end software.** Focus: English–Persian dictionary pages 57–59; general PDF route is included. Compare all variants to page images.

## Goals and pass/fail principles

1. Preserve every printed token, diacritic, IPA symbol, sense number, part-of-speech label, paragraph, example, column and entry association.
2. Avoid unreviewed omissions, hallucinated dictionary definitions or English lexicon substitution.
3. Record the input image, every OCR engine output and each reviewer decision as separate immutable layers.
4. Measure accuracy against **visually adjudicated gold annotations**; OCR confidence is not a success metric.
5. Use a fail-closed policy: unresolved entry boundaries or definition/headword alignment stay `needs_review`, not automatically `verified`.

## Phase 0 — capture and classify each page (required)

Inputs: original PDF/image(s), scan edition, printed page number, PDF page index (if any), SHA-256. Do not crop away margin symbols, footnotes or running headers without preserving the full original.

Classify: `born_digital`, `hybrid`, `scanned_image`, `unreliable_text_layer`. If a text layer exists, extract it together with block/word coordinates (PyMuPDF) **and retain it**. Validate word order visually, especially on mixed RTL/LTR pages. A text layer is not necessarily a correct transcription.

Outputs: `source-manifest.json`, immutable page images, `embedded_text_raw.jsonl` when applicable.

## Phase 1 — layout BEFORE recognition

Detect page margins, columns, internal dictionary entries, headings, labels, phonetic strings, continuation markers, footer legend and header. Identify **separate column reading sequences** and within-entry reading order.

For page 57, treat left-column entries starting with `Arabist` and right-column entries starting with `Arcadian` as distinct sequences. Do not read across the central rule. Visually inspect table/callout continuation on page 58. Produce region polygons, image-space coordinates, region type and reading-order index.

Compare Surya's proposed regions with conservative geometric crops/lines; allow manual override. A layout error should never be disguised as an OCR spelling fix.

Output: `layout-regions.jsonl` with `page_id, region_id, bbox, column, region_type, reading_order, model_version, review_status`.

## Phase 2 — independent OCR readings

1. Run Tesseract `eng` (and `fas+eng` where appropriate) on the exact same regions, retaining raw outputs and TSV word boxes.
2. Run PaddleOCR Persian/English model as an **optional independently logged alternative** once actually installed and tested.
3. Run Surya OCR as a third option if its version, model and license permit it; do not assume the uploaded ZIP includes model weights.
4. Keep recognition inputs comparable: crop, orientation, DPI, preprocessing recipe and engine configuration must be logged.

Prefer region-specific recognition (English headword, IPA/phonetic text, Persian meanings) over applying one generic language model to the entire page. Preserve original punctuation and directionality codepoints.

Output: `ocr-alternatives.jsonl` for each engine, no merged text yet.

## Phase 3 — identify entries and attach their components spatially

An entry has a headword anchor and may have a POS marker, pronunciation(s), enumerated senses, Persian glosses, usage examples and continued content. Candidate association uses **x/y positions, boundaries, column, indentation and sequence**, not merely nearest textual string.

Proposed record:
~~~json
{
  "page_id": "57",
  "entry_id": "p57-left-001",
  "column": "left",
  "headword": {"raw": "Arabist", "bbox": [0, 0, 0, 0], "status": "candidate"},
  "pronunciations": [],
  "labels": [],
  "senses": [],
  "examples": [],
  "source_regions": [],
  "engines": ["tesseract", "paddle_optional"],
  "status": "needs_review"
}
~~~
Coordinates above are **schema placeholders**, not measured boxes. Never silently carry a Persian gloss across a column/entry boundary.

## Phase 4 — candidate validation; NO invisible rewriting

- Use Aryanpour index and ESDB to **rank** possible English headword spellings only after OCR identifies an actual page location.
- Compare UK/US IPA data or Wiktextract for alternative pronunciations, but preserve the printed symbols even if unusual.
- Run Hazm **only on isolated Persian spans** in a copy; prefer conservative Unicode diagnostics; do not default-normalize English, IPA, numbers or bilingual strings.
- Use Academy, Najafi and grammar references for *diagnostic* suggestions; historical/dictionary orthography is a source property.
- Record variants and reasons: `visual_evidence`, `ocr_agreement`, `lexicon_hint`, `orthography_suggestion`, `human_decision`. A dictionary hint never constitutes a confirmed OCR correction.

Output: `candidate-differences.jsonl` and `review-queue.jsonl`.

## Phase 5 — human visual verification

Sample visually adjudicated examples before calibrating anything. Prioritize low agreement, entry-boundary confusion, source/OCR disagreement, IPA damage, ZWNJ, mixed scripts, handwritten marginalia, and sense-number/footnote assignment.

For each change store: original screenshot/page/region, raw OCR text from each engine, chosen exact reading, decision reason, reviewer/time, and status. The original extraction remains immutable.

States: `candidate`, `confirmed_by_page`, `false_positive`, `deferred`, `editorial_option`. Only `confirmed_by_page` is eligible for faithful export.

## Phase 6 — gold data and quantitative evaluation

Start from pages 57–59 as *pilot*, then expand to diverse book typography and difficult pages. Include narrow columns, bold English, italic IPA, Persian diacritics, examples, ligatures, footers and repeated headers.

Keep separate training/development/test pages and maintain an untouched held-out evaluation split. Measure per-page and per-region:
- English headword exact-match and recall (including initial/final glyph drops);
- Persian **CER** and **WER** calculated with a documented exact-Unicode policy;
- IPA exact-match and phoneme-character error;
- entry segmentation precision/recall and headword→meaning assignment correctness;
- page column/line reading-order agreement;
- all-senses/all-footnotes completeness and proportion requiring manual review;
- runtime and memory. Report normalized results separately from source-faithful metrics.

Report confidence intervals or enough sample counts to prevent overinterpreting tiny pilots. Never report full-book accuracy from headword presence rates.

## Phase 7 — faithful deliverables

Each processed book emits:
- `source-manifest.json` + SHA-256 + original image references;
- `embedded_text_raw.jsonl` and per-engine `ocr-alternatives.jsonl`;
- `layout-regions.jsonl`, `entry-candidates.jsonl`, `review-queue.jsonl`;
- `dictionary.entries.reviewed.jsonl` for visually verified entries;
- `dictionary.readable.md` with page/entry anchors (no entries silently missing);
- `benchmark-report.json` / `benchmark-report.md` with method, version and limitations.

If working on general prose rather than dictionary pages, replace entry parsing with paragraphs, headings, footnotes, block quotes and tables, but keep the same evidence and evaluation rules.

## Recommended staged implementation order (cost-aware)

**A. Baseline:** Finish a small, visually verified pilot; rerun the already-working Tesseract path with column crops; measure where it fails.

**B. Layout:** Evaluate Surya against manual column/entry boxes. If it fails, use a conservative page-specific layout template before adding a new OCR engine.

**C. Headwords:** Add ESDB/Aryanpour **candidate ranking**, not dictionary text insertion; quantify headword gains *and* false corrections.

**D. Persian/IPA:** Install and independently benchmark PaddleOCR / optional Surya recognition and verify IPA characters. Add Hazm on Persian-only spans.

**E. Training:** Only if measurable residual failures remain, try Garshasp synthetic pretraining or Kraken model adaptation, keeping real held-out pages for evaluation.

## Definition of completion

A step is complete only after the code is reproducible, inputs and model versions are documented, side-by-side visual examples are stored privately, and a benchmark demonstrates improvements without reducing source fidelity. **A complete extracted page can still be unverified; label it honestly.**
