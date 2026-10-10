# فرهنگ علوم اجتماعی — Gould/Kolb digital dictionary

**Phase 1: structural pilot, not a complete dictionary.**

Source: Persian فرهنگ علوم اجتماعی, edited by محمدجواد زاهدی مازندرانی; English A Dictionary of the Social Sciences, editors Julius Gould and William L. Kolb. The user-supplied 980-page PDF is scanned, with no selectable text on any page in the full local inventory. The original PDF is not uploaded to GitHub; its exact size and SHA-256 are in [source_manifest.json](source_manifest.json).

## Editorial rules come first

Read [**EDITORIAL_RULES.md**](EDITORIAL_RULES.md) before extracting any entry. Its [machine-checkable register](editorial_rules.json) anchors 12 source-authored rules to the Persian introduction (physical PDF pages 12–16). The catalog builder refuses to run if this register is missing, has unsupported provenance claims, or omits required structural conventions. In particular, the editorial `see/←` referral and `also/نیز` association are **different relationships**; A–E mark explanatory sections, **not automatically lexical senses**.

## Source page structure

| Physical PDF pages | Component |
|---|---|
| 1–19 | Front matter and editorial introduction |
| 20–956 | Main two-column Persian dictionary (right-to-left reading) |
| 957–978 | European–Persian glossary (PDF pages run in reverse alphabetical order, Z toward A) |
| 979–980 | English title / final blank |

The editor's introduction (physical pages 12–14) defines main explanatory entries, arrow (←) referral entries, and related (نیز) entries. Lettered A–E sections structure the exposition, not automatically separate lexical senses.

## Implemented files

- [source_manifest.json](source_manifest.json) – source identity, boundaries, inspected pages and provisional printed-page mapping
- [pilot/entries.jsonl](pilot/entries.jsonl) – 5 visually reviewed heading/referral observations, with complete definitions intentionally null
- [pilot/glossary_rows.jsonl](pilot/glossary_rows.jsonl) – 6 visually reviewed English–Persian back-glossary rows from PDF page 978, distinct from main articles
- [tools/build_catalog.py](tools/build_catalog.py) – strict source hash checker and 980-page inventory, plus pilot-only lookup generator (no OCR)
- [tools/test_build_catalog.py](tools/test_build_catalog.py) – validation tests rejecting invented definitions or prematurely resolved references
- [SCHEMA.md](SCHEMA.md) – source authority and field definitions
- [**benchmark/REVIEW_HANDOFF.md**](benchmark/REVIEW_HANDOFF.md) explains how a genuinely separate reviewer checks all 13 first-pass records, submits corrections and source-image attestations, and triggers a fail-closed gold-standard gate.
- [**tools/review_gate.py**](tools/review_gate.py) and [test_review_gate.py](tools/test_review_gate.py) prepare review forms, reject stale source digests, and refuse gold-standard promotion until every record has been approved after independent review. Generated blank templates are included in CI artifacts.
- [**benchmark/PHASE3.md**](benchmark/PHASE3.md) — 11 image-based visual recheck decisions and two bounded complete-article **first-pass** candidates (`احضار روح` and `افزایش طبیعی`), with explicit second-review requirements.
- [Complete-article records](benchmark/complete_articles_first_pass.jsonl), [recheck log](benchmark/visual_recheck_log_v1.jsonl), and [source crop locators](benchmark/complete_article_evidence.json); [Phase 3 validator](tools/validate_phase3.py) rejects any unsupported independent approval or source-link claim.
- [**benchmark/README.md**](benchmark/README.md) – first-pass, source-located transcription benchmark: **9 complete referral entries and two partial A-section transcriptions**, with the image-crop manifest and strict review status.
- [**tools/validate_benchmark.py**](tools/validate_benchmark.py) and [**tests**](tools/test_validate_benchmark.py) – source-bound benchmark validation and optional locally regenerated page excerpts.

The full local build creates generated/physical_pages.jsonl (980 pages), generated/pilot_lookup.jsonl (11 first-pass visual observations), and generated/build_report.json. All but source metadata and reviewed observations are reproducible generated outputs.

## Run locally

Install Python 3.10+ and PyMuPDF. The full source-aware invocation is:

    python -m pip install pymupdf
    python translation-references/social-sciences-gould-kolb/tools/build_catalog.py --pdf "/path/to/farhang-eolum-eejtemaii-g-k@bamun1.pdf" --output translation-references/social-sciences-gould-kolb/generated
    python -m unittest discover -s translation-references/social-sciences-gould-kolb/tools -p 'test_*.py' -v

Without the actual PDF, the builder validates the existing pilot and produces its lookup, **but explicitly reports that the source has not been checked in that run**. GitHub Actions runs the source-free validation because the copyrighted source PDF is not stored in the repository. The full source-verified page inventory was run separately against the user-supplied PDF.

## Next gate

The project now has **11 first-pass referral/A-section records**, a same-assistant image-recheck log for all 11, and **two complete explanatory-article candidates transcribed in a first visual pass**. See [Phase 3 documentation](benchmark/PHASE3.md). These are **not independently approved gold-standard texts**; two article candidates do not constitute a completed dictionary.

The [independent-review queue and gate](benchmark/REVIEW_HANDOFF.md) are now implemented. The next gate is a **distinct second reviewer**, comparing each candidate's exact Persian characters, punctuation, ZWNJ, heading boundary and contributor credits with the original page image. Resolve issues in a separate correction/adjudication file; do not rewrite the original first-pass evidence silently.

Once the reviewed benchmark has been approved, expand the verified glossary sample and quantitatively evaluate OCR/vision extraction. Do not assess OCR accuracy against unverified first-pass text.

No printed-edition authority, Persian editorial normalization, whole-book entry count or full OCR is claimed. This dictionary's conventions must not be transferred to Aryanpour without its own evidence.
