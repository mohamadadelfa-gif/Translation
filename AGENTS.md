# Agent Instructions — Translation Workshop (Revisiting Zero Hour 1945)

This repository supports the English→Persian translation of *Revisiting Zero Hour 1945: The Emergence of Postwar German Culture* (ed. Stephen Brockmann & Frank Trommler). Adel is the translator; final authority over every translation decision rests with him.

## Read this first

- [PROGRESS.md](PROGRESS.md) — current location in the text and what's still open.
- [MENTOR_WORKFLOW.md](MENTOR_WORKFLOW.md) — the review method to follow for every section.
- [translation-preparation/START-HERE.md](translation-preparation/START-HERE.md) — chapter/section map.
- [translation-preparation/CONTEXT-AND-STRUCTURE.md](translation-preparation/CONTEXT-AND-STRUCTURE.md) — book context and structure.
- [translation-references/SOURCE-REGISTER.md](translation-references/SOURCE-REGISTER.md) — approved reference sources.
- [translation-references/WORD-CHOICE-POLICY.md](translation-references/WORD-CHOICE-POLICY.md) — terminology rules.

## Repository layout

| Folder | Purpose |
|---|---|
| `sources/` | Uploaded reference material — **read-only**, for consultation only |
| `translation-preparation/` | Book structure, chapter breakdowns, study guide |
| `translation-references/` | Source and word-choice rules, extracted Aryanpour glossary |
| `drafts/` | Adel's drafts, proposed revisions, session notes |
| `approved-translations/` | Only translations Adel has explicitly approved |
| `tools/` | Preparation/extraction scripts — not needed for day-to-day translation work |
| `archive/` | Test samples, reports, PDF-review images |

## Rules for working in this repo

- Never edit, rename, move, or delete anything under `sources/`. It is reference material only.
- Do not add anything to `approved-translations/` unless Adel has explicitly approved it. Draft and proposed revisions belong in `drafts/`.
- Keep Adel's own draft and any mentor/agent-proposed revision visibly distinguishable (e.g. strikethrough for deletions, bold for additions, per MENTOR_WORKFLOW.md).
- No lexical source (Aryanpour, Hezareh, Ashouri, the Persian thesaurus, Najafi, the Academy orthography guide) has automatic priority — weigh context, specialist meaning, natural Persian, and the author's argument together, per MENTOR_WORKFLOW.md.
- Avoid bureaucratic passive padding in Persian prose (e.g. «می‌باشد»، «می‌گردد»، «صورت پذیرفت»).
- File naming for drafts: `C00-S01-draft-01.md`, and after approval, `C00-S01-approved.md`.
- Before starting new work, check PROGRESS.md for the current location and any open questions, and update it when a session changes that state.

## Known limitations (see PROGRESS.md for detail)

- Three entries in the extracted LD2 (Hezareh) glossary have corrupted characters in the source.
- The فرهنگ طیفی (Word) extraction has not yet been quality-checked.
- No chapter has yet been finalized into `approved-translations/`.

## Note on project history

This repo previously mirrored a ChatGPT-project plan with a different file layout (numbered files like `01_CHATGPT_PROJECT_INSTRUCTIONS.md` under a local `AI control room` folder). That plan is superseded — the structure and workflow above are current.
