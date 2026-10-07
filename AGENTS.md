# Translation Mentor — Project Instructions

This repository is the working environment for Adel's English-to-Persian translation of *Revisiting Zero Hour 1945* and for learning translation through guided practice.

## Authority and control

Use these roles when project files overlap:

1. `MENTOR_WORKFLOW.md` is the **single authoritative workflow** for pedagogy, review stages, reference gating, approval, and file-state transitions.
2. `sources/` is a read-only snapshot of supplied material. Never write new working segmentation, mentor notes, or translation edits into it.
3. `translation-references/SOURCE-REGISTER.md` defines source roles and retrieval routes; it does not create a second workflow.
4. `PROGRESS.md` is the live dashboard for the current position, open checks, and next action only.
5. `translation-preparation/` contains derived working structure and reading aids.
6. `drafts/Cxx/` contains Adel's drafts, mentor proposals, and review notes for that chapter.
7. `approved-translations/` contains only text explicitly approved by Adel.
8. `archive/` contains historical or superseded material and is not an active instruction source.
9. `translation-references/WORD-CHOICE-POLICY.md` is a compatibility pointer to the authoritative workflow/reference documents, not an independent policy authority.

If any subordinate or archived document conflicts with `MENTOR_WORKFLOW.md`, follow `MENTOR_WORKFLOW.md`.

## Human authority

Adel retains final authority over every translation decision. Never turn a mentor proposal into an approved translation without Adel's explicit approval.

Keep these categories visibly distinct:

- English source
- Adel's draft
- mentor analysis
- mentor revision
- reference evidence
- approved translation

## Working hierarchy

The translation workflow uses four working levels below the book:

```text
Book
└── Chapter
    └── Translation Unit
        └── Practice Chunk
            └── Sentence
```

- **Chapter:** `C00`, `C01`, etc.
- **Translation Unit:** `C00-S02`, etc. These are structural working divisions and may be much longer than one mentoring session.
- **Practice Chunk:** approximately 250–350 words, normally identified as `C00-S02-P01`, `C00-S02-P02`, etc.
- **Sentence:** a sentence inside a practice chunk. Sentence-level work does not create a new source structure.

Translation units are not automatically 300-word exercises.

## File-state rules

Preferred naming for new work:

- Adel draft: `drafts/C00/C00-S02-P01-draft-01.md`
- Mentor-reviewed proposal: `drafts/C00/C00-S02-P01-reviewed-01.md`
- Review notes: `drafts/C00/C00-S02-P01-review-notes-01.md`
- Approved text: `approved-translations/C00/C00-S02-P01-approved.md`

Existing historical filenames do not need to be renamed solely to satisfy this convention.

## Source and preparation layers

Treat `sources/` as an immutable snapshot of what was supplied to the repository. Existing source snapshots may already contain earlier conversion or segmentation artifacts; preserve them exactly rather than retroactively cleaning them.

Treat `translation-preparation/` as the only active working layer for chapter maps, reading notes, practical translation divisions, and future structural edits. Never sync working edits back into `sources/`.

## Reference discipline

Do not claim that Ariyanpour, Hezareh, Ashouri, Najafi, the Academy guide, the Persian thesaurus, or any other named source supports a wording unless the relevant entry or passage was actually checked.

Unverified Cronin, K1, RTS, or other external frameworks are not lexical or historical evidence merely because an older plan mentioned them.

Use the confidence labels defined in `MENTOR_WORKFLOW.md`.

For consequential or uncertain general vocabulary, compare Ariyanpour and Hezareh as active peers according to `MENTOR_WORKFLOW.md`; use `translation-references/SOURCE-REGISTER.md` for the retrieval routes. Use `translation-references/GERMAN-CONCEPTS.md` for historical-conceptual research; its research state is distinct from approval of a Persian equivalent.

### Hezareh lookup discipline

For Hezareh, use the supplied dictionary index as the default retrieval route rather than manually searching the eight source files first.

The lookup tool is:

`sources/Hezareh_Dictionary_Index/dictionary-index/hezareh_lookup.py`

For a consequential or uncertain English term:

1. query the Hezareh index for the word or phrase;
2. prefer exact or base-headword matches before broader matches;
3. record the returned headword, PDF page, verification status, boundary confidence, and source pointer;
4. follow the source pointer into the corresponding Markdown extraction before attributing wording to Hezareh;
5. distinguish `verification_status` (`visually_checked`, `raw_ocr`) from `boundary_confidence` (`high`, `medium`, `low`, `hint_only`);
6. do not treat the index record itself as independent lexical evidence.

For `raw_ocr`, report that the wording is OCR-derived and requires source verification when it materially affects the translation.

For `boundary_confidence: hint_only`, use the result only to locate the relevant page; do not treat it as a reconstructed dictionary entry.

A `visually_checked` status records the supplied Hezareh package's verification state. It does not mean that the current mentor independently inspected an original PDF page.

The original Hezareh PDF is not currently present in the tracked repository. If the extraction is insufficient for a consequential lexical decision, preserve the uncertainty rather than inventing verification.

### Hezareh match semantics

Distinguish exact headword, exact base-headword, verified exact alias, prefix, and full-text fallback matches. Establish a verified exact alias from the actual alias record and its checked source, not merely from a phrase appearing in OCR. Follow the source pointer before attribution in every case.

A prefix or full-text hit is a retrieval clue, not an exact dictionary entry for the query. For example, `make up for` returning `loss-making` because the phrase occurs within OCR text is only a broad retrieval hit/navigation clue. Do not attribute the searched expression to Hezareh unless an exact/base/verified-alias entry has actually been established.

The current lookup tool does not expose match type directly. Report that limitation; establish a classification from inspected records where possible, otherwise leave it unspecified rather than inventing one. Do not modify the supplied Hezareh package.

### Evidence-status discipline

Structured or OCR-derived reference material is retrieval evidence, not automatically verified evidence.

For Ashouri:

- a structured Markdown entry may be used to locate a candidate equivalent;
- if the relevant original PDF page has not been visually checked, do not label the equivalent as `Documented equivalent`;
- report it as extracted or OCR-derived evidence and state that source verification is still needed;
- if the QC files flag the entry as uncertain, preserve that uncertainty explicitly.

For historically significant German terms already listed in `translation-references/GERMAN-CONCEPTS.md`, use the confidence labels defined in `MENTOR_WORKFLOW.md`.

If the concept itself still requires historical or conceptual verification, use:

`German concept source check needed`

Do not replace this with a broader confidence label unless the uncertainty concerns a different historical claim rather than the German concept itself.

## Glossary discipline

Use `translation-references/GLOSSARY.md` for project terminology.

A proposed equivalent may be recorded as a candidate, but it becomes **approved** only after Adel explicitly accepts it. Do not treat a candidate as a binding project-wide translation.

## Session start

At the beginning of continuing work:

1. Read `PROGRESS.md`.
2. Locate the relevant chapter/unit in `translation-preparation/`.
3. Read enough surrounding source context to understand the argument.
4. Follow `MENTOR_WORKFLOW.md`.
5. Preserve uncertainty instead of inventing certainty.