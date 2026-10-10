# Persian Grammar Reference — Saeed Yousef (2018)

**Scope:** A portable, source-aware index and OCR/text-extraction quality-assurance module for Persian documents. It can be reused outside this translation project.

**Reference:** Saeed Yousef, assisted by Hayedeh Torabi, *Persian: A Comprehensive Grammar* (Routledge, 2018), ISBN 978-1-138-92702-5. The user-supplied PDF has 393 pages, with 19 chapters. In the main body, **PDF page = printed page + 19**. The original PDF, not this index, is the visual authority.

## Start here

- [OCR support — overview, CLI and scope](ocr-support/README.md)
- [Grammar-section-to-OCR-issue map](ocr-support/OCR-RULE-MAP.md)
- [Review and evidence rules](ocr-support/REVIEW-POLICY.md)
- [Machine-readable error taxonomy](ocr-support/ERROR-TAXONOMY.jsonl)
- [Visually checked validation examples](ocr-support/VALIDATION-CASES.jsonl)
- [Run the checker](ocr-support/check_ocr.py) and [tests](ocr-support/test_check_ocr.py)

## Source classification and copyright

The original PDF was uploaded in conversation on 2026-10-10 and **is not tracked in this public repository**. No complete book text, chapter transcripts, publisher illustrations, or large quotations are published here. This module contains **original analysis, software and short metadata**, plus a minimal visually checked Persian example for extraction testing. Exact book examples, tables, and any substantive attribution to Yousef require reinspection of the corresponding PDF page.

**Source fingerprint:** SHA-256 `d7fe1280e629caa8488db6436b51f7fee4550a37303364e0d43c8d3005e5ca2d` (user-supplied PDF). Reference pagination comes from the book's printed contents and was checked against its embedded text layer. It is **not** a full page-by-page visual audit.

**Known extraction limitation:** The PDF text layer can reverse Persian word order in English/Persian lines. OCR QA rules are not a substitute for document layout and source-image verification. The source-specific validation example at PDF p. 151 is separately visually checked.

This directory is a **reference and software module**, not an authoritative digital transcription. The project's other Persian usage and orthographic references remain distinct; the Academy writing guide is the preferred reference for normative spelling questions.

## PDF text recognition (new)

A standalone PDF → Persian OCR pipeline is available under [`ocr-engine/`](ocr-engine/README.md). The tested Tesseract backend and optional (untested) PaddleOCR `fa` adapter produce page-by-page Markdown, JSONL with source text alternatives, geometry/confidence, and optional flags from this sibling QA checker. **Accuracy is not yet benchmarked**; source-image checking is required before using the output as a faithful quotation.
