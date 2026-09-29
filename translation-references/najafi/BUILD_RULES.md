# Najafi build rules

1. The canonical source is `sources/Najafi — غلط ننویسیم.pdf`.
2. Never alter, normalize, or overwrite the canonical PDF.
3. The page image is authoritative; the embedded/extracted text layer is not trusted as Najafi's wording.
4. OCR or automated recognition may be used only to propose navigation candidates. It must never be promoted directly to source evidence.
5. A headword enters the verified index only after its page and visible heading have been checked against the scan.
6. Preserve the displayed headword as closely as practical. Normalization belongs only in `normalized_headword`.
7. If vowel marks, spelling, slash variants, or a heading boundary cannot be read confidently, put the item in `qc/unverified-headwords.csv` instead of guessing.
8. Cross-reference headings remain separate rows; do not collapse them into the destination entry.
9. `page-map.csv` is navigation only.
10. `headwords-master.csv` and letter indexes are navigation only.
11. A Najafi usage claim requires visual inspection of the actual scanned entry.
12. A full entry transcription may be added under `entries/` only after visual verification and must preserve Najafi's wording, punctuation, examples, quotations, and distinctions.
13. Do not silently correct historical spelling, typography, quotations, or apparent errors.
14. Every verified transcription must record both PDF page and printed page when available.
15. Incomplete index coverage must remain explicit in the manifest and QC files.
