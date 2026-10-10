# Persian grammar reference — Saeed Yousef (2018)

Saeed Yousef, assisted by Hayedeh Torabi, *Persian: A Comprehensive Grammar* (Routledge, first published 2018), ISBN 978-1-138-92702-5.

## Portable reference scope
This folder is a reusable, public-safe **navigation and OCR/text-extraction quality-assurance module**. It is not dependent on the Translation Mentor and does not contain the copyrighted complete book.
The user-supplied reference PDF contains 393 pages and 19 chapters. For main-body references: **PDF page = printed page + 19**. Full PDF SHA-256: d7fe1280e629caa8488db6436b51f7fee4550a37303364e0d43c8d3005e5ca2d.

## Entry points
- [OCR module, how to run and limitations](ocr-support/README.md)
- [Grammar-to-OCR error mapping](ocr-support/OCR-RULE-MAP.md)
- [Review policy](ocr-support/REVIEW-POLICY.md)
- [Error taxonomy](ocr-support/ERROR-TAXONOMY.jsonl)
- [Visually checked extraction case](ocr-support/VALIDATION-CASES.jsonl)
- [Runnable checker](ocr-support/check_ocr.py) and [tests](ocr-support/test_check_ocr.py)

## Authority, evidence and reuse
The original PDF is the visual authority for exact Persian examples and tables; the tool is only a triage layer. Extraction of mixed English–Persian pages may reverse the logical Persian reading order. A case at PDF p.151 (printed p.132) has been visually verified; this is **PDF text-layer extraction**, not optical OCR. Software heuristics are original project engineering decisions, not rules automatically attributed to Yousef.
Refer to the Academy orthographic guide for normative spelling and half-space decisions; a descriptive grammar reference alone cannot establish exact source wording. Do not redistribute the complete book publicly without appropriate rights.
