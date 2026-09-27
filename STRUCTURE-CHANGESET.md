# Translation repository structural cleanup

Prepared after reviewing `mohamadadelfa-gif/Translation` on 2026-09-27.

## What this change set fixes

1. Makes `MENTOR_WORKFLOW.md` the single authoritative pedagogical workflow.
2. Replaces the obsolete local-path implementation plan in `AGENTS.md` with current repository instructions.
3. Defines the hierarchy `Chapter → Translation Unit → Practice Chunk → Sentence`.
4. Separates large `S` units from ~300-word mentoring `P` chunks.
5. Creates `translation-references/GLOSSARY.md` with explicit candidate/approved states.
6. Clarifies that `sources/` is the immutable canonical snapshot and `translation-preparation/` is a derived working layer.
7. Standardizes filenames for new drafts, reviews, notes, and approved chunks without renaming historical files.

## Files to replace

- `AGENTS.md`
- `MENTOR_WORKFLOW.md`
- `README.md`
- `drafts/README.md`
- `approved-translations/README.md`

## File to add

- `translation-references/GLOSSARY.md`

## Two additional edits still required in the repository

Because the GitHub connector is read-only in this session, this bundle does not overwrite the existing long files automatically. Apply these two small textual edits when committing the bundle:

### `translation-references/SOURCE-REGISTER.md`

Replace the final sentence:

> The mentor.md plan and current project instructions guide pedagogy rather than supply lexical evidence.

with:

> `MENTOR_WORKFLOW.md` and the current project instructions guide pedagogy rather than supply lexical evidence.

The following sentence about unprovided Cronin and K1 documents should remain.

### `translation-preparation/START-HERE.md`

After `## How to use this structure`, insert:

> The `Cxx-Sxx` identifiers below are structural translation units, not fixed 300-word mentoring sessions. For day-to-day practice, divide the current unit into coherent ~250–350-word practice chunks identified as `Cxx-Sxx-P01`, `P02`, and so on. Chunk boundaries are workflow aids and must not alter the source text or original section boundaries.

## Suggested commit message

`Clarify Translation Mentor hierarchy and glossary workflow`
