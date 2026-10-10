# فرهنگ علوم اجتماعی — Gould/Kolb digital dictionary

**Phase 1: structural pilot, not a complete dictionary.**

Source: Persian فرهنگ علوم اجتماعی, edited by محمدجواد زاهدی مازندرانی; English A Dictionary of the Social Sciences, editors Julius Gould and William L. Kolb. The user-supplied 980-page PDF is scanned, with no selectable text on any page in the full local inventory. The original PDF is not uploaded to GitHub; its exact size and SHA-256 are in [source_manifest.json](source_manifest.json).

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

The full local build creates generated/physical_pages.jsonl (980 pages), generated/pilot_lookup.jsonl (11 verified literal observations), and generated/build_report.json. All but source metadata and reviewed observations are reproducible generated outputs.

## Run locally

Install Python 3.10+ and PyMuPDF. The full source-aware invocation is:

    python -m pip install pymupdf
    python translation-references/social-sciences-gould-kolb/tools/build_catalog.py --pdf "/path/to/farhang-eolum-eejtemaii-g-k@bamun1.pdf" --output translation-references/social-sciences-gould-kolb/generated
    python -m unittest discover -s translation-references/social-sciences-gould-kolb/tools -p 'test_*.py' -v

Without the actual PDF, the builder validates the existing pilot and produces its lookup, **but explicitly reports that the source has not been checked in that run**. GitHub Actions runs the source-free validation because the copyrighted source PDF is not stored in the repository. The full source-verified page inventory was run separately against the user-supplied PDF.

## Next gate

Transcribe and verify two short complete articles, one referral, and 10–20 glossary rows against high-resolution page images; mark continuation across columns/pages, uncertain glyphs, author credits, section labels, and reference links separately. Evaluate OCR only after manual gold-standard examples exist.

No printed-edition authority, Persian editorial normalization, whole-book entry count, full OCR or complete definitions are claimed. This dictionary's conventions must not be transferred to Aryanpour without its own evidence.
