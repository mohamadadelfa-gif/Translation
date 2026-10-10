# Universal OCR — proposed source catalogue and workflow

**Documentation only; not an installed new OCR system.** Prepared 2026-10-10 for a portable OCR project with Persian and bilingual dictionaries as first-class cases.

Start here:
- [**SUGGESTED-SOURCES.md**](SUGGESTED-SOURCES.md) — existing resources, user-provided archives, external candidates, roles, priorities, cautions.
- [**SUGGESTED-SOURCES.jsonl**](SUGGESTED-SOURCES.jsonl) — machine-readable inventory using stable IDs/statuses.
- [**RECOMMENDED-WORKFLOW.md**](RECOMMENDED-WORKFLOW.md) — source-preserving OCR process and implementation milestones.
- [**REVIEW-AND-EVALUATION.md**](REVIEW-AND-EVALUATION.md) — review record schema, error distinctions, gold/evaluation and release gates.

**What already runs:** The Persian Tesseract pipeline and rule-based QA are in [the Saeed Yousef OCR modules](../../translation-references/grammar/persian/saeed-yousef/README.md). **What is not yet established:** Surya 0.22.1 and Hazm archives are user uploads, not integrated runtime dependencies; generic Universal OCR implementation was produced earlier as a standalone chat artifact and has not been committed at this location. PaddleOCR integration requires testing. No high-accuracy universal benchmark has been established.

The short-term experiment is the 57–59 bilingual dictionary page sample. It requires entry-level **human gold** before any accuracy claim. Never treat an English headword existing in a wordlist as proof it belongs on the scanned page.

This directory is intentionally separate from the book-specific grammar reference so it can later become its own independent OCR toolkit without assuming translation-project-specific files exist. Its paths to internal references are navigational convenience only.
