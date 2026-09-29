# Najafi retrieval layer

This directory is the project navigation and verified-entry layer for Abolhasan Najafi's *غلط ننویسیم*.

## Canonical source

`sources/Najafi — غلط ننویسیم.pdf`

The active canonical source is the clearer 480-page scan. The PDF page image is authoritative. The PDF's machine-readable text layer does not reliably contain Najafi's Persian text and must not be treated as source evidence.

## Purpose

This layer has two distinct jobs:

1. **navigation** — locate a Najafi headword and its PDF/printed page;
2. **verified evidence** — eventually store faithful transcriptions of individual entries that have actually been visually checked against the canonical scan.

Navigation is not evidence. A headword row or page-map row proves only where an entry can be found.

## Retrieval protocol

For a Persian usage question:

1. Search `index/headwords-master.csv` or the matching letter index.
2. Open the recorded page in the canonical PDF.
3. Visually inspect the relevant entry.
4. Only then attribute a usage claim to Najafi.
5. If the entry becomes recurrently useful, create a verified transcription under `entries/` with the exact PDF page, printed page, and verification status.
6. Record evidence as:
   `Najafi — «<headword>» — PDF p. <pdf_page> / printed p. <printed_page> — visually_checked — finding — effect on translation`.

## Verification statuses

- `page_verified` — headword and page locator visually checked; entry body not transcribed.
- `page_partially_verified` — page inspected, but at least one heading detail remains unresolved.
- `entry_visually_transcribed` — full relevant entry faithfully transcribed after visual inspection.
- `unverified_candidate` — machine/rough candidate only; never evidence.

## Current build status

Phase 1 is **incremental and incomplete**.

Initial verified coverage:
- PDF pages 13–30
- printed pages 1–18
- alphabetic sections currently covered: `آ`, then early `ا`

See `qc/build-validation.json` for current coverage counts.

Do not interpret incomplete coverage as absence of a Najafi entry. If a requested term is not yet indexed, search the canonical PDF visually or extend the navigation layer first.
