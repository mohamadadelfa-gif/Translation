# Suggested OCR tools, sources, and availability (10 October 2026)

**Purpose:** A research catalogue for a general-purpose OCR workflow, with a dedicated path for English–Persian dictionary scans. This is a **suggested source list**, not an installation manifest or a claim that all tools have been integrated. Machine-readable mirror: [SUGGESTED-SOURCES.jsonl](SUGGESTED-SOURCES.jsonl).

## Status vocabulary

- `repo_confirmed` — checked in the current GitHub `master`.
- `user_uploaded_zip_*` — source archive supplied in conversation; **not** evidence of an installed/running program.
- `optional_adapter_*` / `online_candidate` — integration or evaluation needed.
- `to_build` — planned source, not yet a completed dataset.
- The reusable generic Universal OCR ZIP was previously produced in chat; **its program files are not in this GitHub folder**.

## Available or previously provided

| Source | Availability | Best OCR role | Guardrail |
|---|---|---|---|
| [Aryanpour](../../translation-references/aryanpour/README.md) | Indexed JSONL and headword shards on `master` | Candidate English lemma/headword and lexical comparison | Confirm exact printed edition |
| [Hezareh](../../translation-references/hezareh/README.md) | Indexed on `master`, predominantly raw OCR | Corroborating candidate wording | Not a visual gold standard |
| [Saeed Yousef grammar / OCR modules](../../translation-references/grammar/persian/saeed-yousef/README.md) | Source navigation, QA checker, Tesseract PDF OCR engine on `master` | Existing baseline + morphological/grammar review | Never turn plausible Persian into unverified transcription |
| [Academy writing guide](../../translation-references/academy-orthography/README.md) | Structured reference on `master` | Orthographic review and ZWNJ judgments | Historical spellings may be intentionally different |
| [Najafi usage guide](../../translation-references/najafi/README.md) | Indexed, limited visually verified coverage | Review unusual Persian forms | Check book page before quoting |
| Surya `0.22.1` ZIP | Previously uploaded; installation/inference **not** verified | Layout / reading order / optional recognition | Code and model weights require separate licensing review |
| Hazm `0.12.1` ZIP | Previously uploaded; core normalization tested in isolation, not integrated | Persian-only OCR text diagnostics | Default normalization can remove diacritics, disrupt IPA |
| `English_Farsi_Advanced.BGL` | Previously supplied, edition not matched to scan | Potential candidate lexicon | Verify provenance, entry mapping and rights |
| Printed pages 57–59 | Previously supplied as images | Starting sample for bilingual dictionary benchmark | Not yet a complete visually transcribed gold set |

**Other existing lexical resources:** Persian thesaurus and Ashouri (for language study, not OCR ground truth). The original PDF or image—not any secondary lexicon—is the authority for the page being transcribed.

## Online candidates (checked sources)

| Priority | Source | Function | Main limitation |
|---|---|---|---|
| P0 | [PyMuPDF](https://pymupdf.readthedocs.io/) | PDF text layer + word/region coordinates | Internal text order can differ from reading order |
| P0 | [Surya](https://github.com/datalab-to/surya) | OCR, layout, reading order, tables | Current online version may differ from uploaded `0.22.1`; check weights license |
| P0 | [Tesseract tessdata_best](https://github.com/tesseract-ocr/tessdata_best) | `fas` / `eng` baseline OCR | Confidence is not accuracy |
| P0 | [PaddleOCR multilingual models](https://www.paddleocr.ai/main/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.html) | Alternative OCR for Persian + English | Must benchmark specific model and pages |
| P0 | [English Speller Database (ESDB)](https://github.com/en-wl/wordlist) | Rank uncertain English headword spellings | Dictionaries have nonstandard and specialized headwords |
| P1 | [IPA-dict](https://github.com/open-dict-data/ipa-dict) | US/UK pronunciation candidates | Not necessarily the dictionary's phonetic convention; source-specific licenses |
| P1 | [Wiktextract](https://github.com/tatuylonen/wiktextract) | Headword, sense, inflection, POS candidates | External lexical data, not printed-page evidence |
| P1 | [Unicode bidi UAX #9](https://www.unicode.org/reports/tr9/) and [segmentation UAX #29](https://www.unicode.org/reports/tr29/) | Logical order and character/word segmentation | Do not reverse strings blindly |
| P2 | [Arshasb](https://github.com/persiandataset/Arshasb) | Persian word/line localization dataset | Published 7,000-page subset has restricted font diversity |
| P2 | [Garshasp-70C](https://huggingface.co/datasets/AliShafiee2003/persian-ocr-garshasp-70c) | Synthetic line-recognition training/robustness | No substitute for real scanned-dictionary gold pages |
| P3 | [Kraken](https://github.com/mittagessen/kraken) | Optional edition/font-specific OCR training | Later, only if benchmarks warrant it |

## Priority principle

**Layout and correct entry association first; recognition accuracy second; linguistic suggestions third.** A correct English word linked to the wrong Persian definition is a more consequential extraction error than a single misspelled character.

## License/data policy

Before downloading, training or redistributing, inspect the exact repository/version and the **dataset or model-weights** license, not merely the code license. Do not commit source dictionary page scans, full copyrighted books, commercial BGL exports, or model weights to this public repository without permission. Keep local data paths and checksums in private manifests.

## Source provenance

Official documentation and linked repository descriptions were checked on 2026-10-10. The site descriptions establish what a project *claims/supports*, not performance on our scans. The exact uploaded Surya and Hazm version details and third-party dependencies require separate local install tests. See [workflow](RECOMMENDED-WORKFLOW.md) for how they would be tested.
