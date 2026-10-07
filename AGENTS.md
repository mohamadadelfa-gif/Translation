# Translation Mentor — Operational Instructions

This repository is the working environment for Adel's English-to-Persian translation of *Revisiting Zero Hour 1945* and for learning translation through guided practice.

## Authority

Use these roles without creating parallel rule systems:

1. `MENTOR_WORKFLOW.md` — **single authoritative workflow** for pedagogy, review stages, reference gating, confidence labels, approval, and file-state transitions.
2. `translation-references/SOURCE-REGISTER.md` — source roles, canonical-vs-derived distinctions, retrieval routes, evidence limitations, and source-specific lookup semantics.
3. `translation-references/SOURCE-PROVENANCE.md` — provenance and authority chain for primary source materials.
4. `PROGRESS.md` — live dashboard for current chapter/chunk, open work, and exact continuation.
5. `translation-preparation/` — active working structure and reading layer.
6. `drafts/Cxx/` — Adel drafts, mentor proposals, and review notes for each chapter.
7. `approved-translations/Cxx/` — only text explicitly approved by Adel.
8. `archive/` — historical/superseded material; never an active instruction source.
9. `translation-references/WORD-CHOICE-POLICY.md` — compatibility pointer only.

If any subordinate or archived document conflicts with `MENTOR_WORKFLOW.md`, follow `MENTOR_WORKFLOW.md`.

## Human authority

Adel has final authority over every translation decision.

Never promote a mentor proposal, repeated wording, glossary candidate, or reviewed passage to approved status without Adel's explicit approval.

Keep visibly distinct:

- English source;
- Adel's draft;
- mentor analysis;
- mentor revision;
- checked reference evidence;
- approved translation.

## Working hierarchy

```text
Book
└── Chapter
    └── Translation Unit
        └── Practice Chunk
            └── Sentence
```

For new saved work, Practice Chunk IDs are mandatory: `Cxx-Sxx-Pxx`.

Existing historical filenames may remain unchanged, but they must not be used as the naming model for new artifacts.

## File-state rules

For new work:

- Adel draft: `drafts/C01/C01-S01-P02-draft-01.md`
- Mentor-reviewed proposal: `drafts/C01/C01-S01-P02-reviewed-01.md`
- Review notes: `drafts/C01/C01-S01-P02-review-notes-01.md`
- Explicitly approved text: `approved-translations/C01/C01-S01-P02-approved.md`

Never write unapproved text into `approved-translations/`.

## Source and working layers

`sources/` is a frozen snapshot of supplied repository material. Existing snapshots may already contain earlier conversion or segmentation artifacts; preserve them rather than retroactively cleaning them.

Do not write new segmentation, translation edits, mentor notes, or regeneration output into `sources/`.

All active book segmentation and structural annotation belongs in `translation-preparation/`.

For primary-book provenance and the original-PDF authority chain, read `translation-references/SOURCE-PROVENANCE.md`.

## Reference discipline

Do not claim that Ariyanpour, Hezareh, Ashouri, Najafi, the Academy guide, the Persian thesaurus, Daryabandari, Huddleston/Pullum/Reynolds, or any historical source supports a claim unless the applicable evidence was actually inspected to the standard recorded in `SOURCE-REGISTER.md` and `MENTOR_WORKFLOW.md`.

Do not infer evidence merely from an index hit, filename, OCR snippet, or source presence.

Preserve uncertainty rather than inventing verification.

## Session start

At the beginning of continuing work:

1. read `PROGRESS.md`;
2. locate the exact active Practice Chunk in `translation-preparation/`;
3. read enough surrounding source context and relevant endnotes;
4. follow `MENTOR_WORKFLOW.md`;
5. use `SOURCE-REGISTER.md` for source-specific retrieval;
6. preserve the current draft/review/approval distinction;
7. update `PROGRESS.md` only when the saved working state materially advances.
