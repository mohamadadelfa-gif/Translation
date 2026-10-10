# Implementation status (2026-10-10)

| Capability | Status | Evidence |
| --- | --- | --- |
| PDF rasterisation, grayscale/contrast/sharpening, DPI/pixel limits | implemented | PyMuPDF + Pillow |
| Extract embedded PDF text; preserve unchanged | implemented/tested | `test_text_only_source_preservation` |
| Tesseract `fas+eng` OCR, image/PDF-page geometry, confidence | implemented/tested | real PDF p.151, PSM3, 190 DPI |
| Tesseract alternative page segmentation mode selection | implemented | test PSM3 successful; multiple PSM run not benchmarked |
| Optional PaddleOCR `fa` recognizer | adapter written, **not installed or runtime tested** | upstream documented API |
| Explicit right-first two-column crop | implemented, **not visually validated** | crop algorithm; splits full-width headings |
| `compare` embedded-vs-OCR retained separately | implemented/tested | p.151 sample |
| Intelligent selection of most accurate text | **not implemented** | cannot be inferred from OCR confidence alone |
| OCR QA issue-report integration | implemented/tested | p.151 reported 31 candidate flags |
| Full-page accuracy benchmark | scorer implemented, **no gold benchmark yet** | requires visually checked full-page text |
| Searchable PDF with hidden text layer | **not implemented** | export `.md` + `.jsonl` only |
| Automatic complex RTL/multi-column reading order reconstruction | **not implemented** | needs layout validation against page images |

This is a functional initial OCR pipeline, **not an established high-accuracy benchmark**. Improve accuracy by testing `tessdata_best` against PaddleOCR `fa` on verified pages and adding layout detection and/or page-image review.
