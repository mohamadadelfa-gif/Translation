# Najafi build rules

1. Canonical source: `sources/Najafi — غلط ننویسیم.pdf`.
2. Never alter or normalize the canonical PDF.
3. Scanned page images are authoritative; the PDF text layer is not trusted as Najafi wording.
4. OCR may be used only for navigation-candidate extraction where no usable text layer exists.
5. `index/headwords-master.csv` is the manually visually verified body-heading layer.
6. `index/source-index-master.csv` is the complete candidate representation of Najafi's own printed `فهرست راهنما` on PDF pp. 449–478.
7. Every source-index row is navigation only, regardless of apparent OCR confidence.
8. Preserve raw candidate uncertainty rather than silently turning OCR into source text.
9. Before attribution, open the indicated dictionary-body page and visually verify the heading and relevant entry.
10. If a candidate page locator is malformed or ambiguous, inspect the corresponding printed source-index page and dictionary body; do not guess.
11. `page-map.csv`, `headwords-master.csv`, letter indexes, `source-index-master.csv`, and `source-index-page-map.csv` are navigation aids, not evidence.
12. Full entry transcriptions may be added under `entries/` only after visual verification.
13. Preserve source wording, punctuation, examples, quotations, distinctions, and relevant typography; do not silently correct the source.
14. Every verified transcription must retain PDF and printed page locators when available.
15. Evidence account: `Najafi — «<headword>» — PDF p. <pdf_page> / printed p. <printed_page> — visually_checked — finding — effect`.
16. Phase 1 navigation is complete when all printed source-index pages are represented. Entry transcription remains incremental by actual translation need.
