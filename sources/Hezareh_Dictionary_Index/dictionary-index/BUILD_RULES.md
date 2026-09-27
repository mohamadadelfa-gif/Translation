# Build rules

The dictionary index is derived from the eight Markdown source files.

## Canonical page ownership
Only each part's primary PDF-page range is indexed. The intentionally duplicated preceding page in Parts 02–08 remains in `source/` but is excluded from the searchable index.

## Visually checked material
`ENTRY:` and standalone `PHRASE:` blocks inside `VISUALLY CHECKED EXCERPT` sections are indexed with:
- `verification_status = visually_checked`
- `boundary_confidence = high`

## Raw OCR
The source's `UNVERIFIED ENGLISH LOOKUP HINTS` are used only as navigation candidates.

A raw candidate is located using strict lexical boundaries. For example:
- `manner` must not match `mannerism`
- `think` must not match `thinkable`
- `man` must not match `man-made`

Candidate boundaries are estimated conservatively from the next located headword on the same canonical page, with a maximum retrieval span. If no safe location is found, the record is retained as `hint_only` and points to the source page instead of inventing an entry.

## Retrieval precedence
1. visually checked exact/base-headword match
2. raw OCR exact/base-headword match
3. prefix match
4. FTS fallback

If checked and raw records refer to the same base headword on the same page, checked wording suppresses raw OCR in the lookup output.
