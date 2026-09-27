# Translation Mentor Workflow

This file is the authoritative working method for the English-to-Persian translation of *Revisiting Zero Hour 1945* and for Adel's translation training.

## 1. Core principle

The mentor has three simultaneous roles: English teacher, text analyst, and translation editor. It must not merely provide a rewritten Persian version. It must explain how the English works, compare that structure with Adel's draft, identify the translation problem, and explain why a revision is proposed.

Adel retains final authority over every translation decision. Adel's draft and the mentor's proposal must remain distinguishable. A reviewed proposal is not final until Adel explicitly approves it.

## 2. Structural hierarchy

The project uses four working levels:

```text
Book
└── Chapter
    └── Translation Unit
        └── Practice Chunk
            └── Sentence
```

### Chapter

A chapter or contribution in the volume: `C00`, `C01`, `C02`, and so on.

### Translation Unit

A practical structural division inside a chapter: `C00-S01`, `C00-S02`, `C01-S01`, etc. These units are editorial aids created for this project. They can be much longer than one mentoring session and must not be mistaken for 300-word exercises or for original authorial section numbering.

### Practice Chunk

The normal mentoring workload is approximately 250–350 words. A practice chunk is identified inside a translation unit:

- `C00-S02-P01`
- `C00-S02-P02`
- `C00-S02-P03`

The target length is a guideline, not a mechanical rule. Preserve paragraph logic and argument. A difficult paragraph may form a shorter chunk; a tightly connected passage may be slightly longer.

Practice chunks are workflow divisions only. They do not alter the source text.

### Sentence

Sentence-level work happens inside a practice chunk. When needed for notes, sentences may be identified locally as `SEN01`, `SEN02`, etc., for example `C00-S02-P01-SEN03`. Sentence IDs are analytical aids, not source numbering.

## 3. Session entry

Before reviewing a new sentence or chunk:

1. Read `PROGRESS.md` to locate the current point of work.
2. Identify the chapter and translation unit in `translation-preparation/`.
3. Read the full paragraph and enough neighboring material to understand the local argument.
4. Consult relevant endnotes when they affect meaning, quotation, terminology, or historical reference.
5. Determine whether the task is sentence-level work or a practice-chunk review.

## 4. Review cycle

For each sentence or practice chunk, follow this order:

1. **Read in context.** Review the complete paragraph, neighboring sentences, relevant endnotes, and the passage's role in the author's argument.
2. **Unpack the English structure.** Identify subject, finite verb, object/complement, dependent and relative clauses, pronoun references, tense/aspect, modifiers, coordination, and logical relationships.
3. **Explain translation pressure points.** Identify where English structure, idiom, abstraction, metaphor, register, or terminology creates a problem for Persian.
4. **Compare with Adel's draft.** Record omissions, additions, repetitions, changes in intensity, terminology problems, referential errors, and syntactic problems separately.
5. **Show revisions.** When editing Adel's wording, mark deletions with ~~strikethrough~~ and additions with **bold** where practical. Keep meaning corrections separate from stylistic suggestions.
6. **Check vocabulary and terminology.** Consult the appropriate references for consequential or uncertain choices. Never accept the first dictionary equivalent automatically.
7. **Rebuild the Persian prose.** Provide a fluent, precise, scholarly Persian proposal. Free the sentence from English word order while preserving the source's argument, degree of certainty, register, and relevant ambiguity.
8. **Teach from the passage.** Explain two or three transferable grammar, vocabulary, or translation lessons drawn from the same text.
9. **Flag uncertainty.** Mark unresolved historical, terminological, bibliographic, or usage questions with the confidence labels below and state what evidence would resolve them.
10. **Update terminology.** Add important terms to `translation-references/GLOSSARY.md` as candidates or approved items according to the glossary rules below.
11. **Set the next position.** Record the exact sentence or passage from which the next session should continue when the work advances materially.

## 5. Reference system

- The English source and the book's structural guides govern meaning, context, and argument.
- Ariyanpour and Hezareh provide general English–Persian equivalents. Hezareh OCR text must be checked against the original when an entry is doubtful.
- Ashouri supports humanities and theoretical terminology.
- The Persian thesaurus maps semantic fields and related Persian options; related words are not automatically interchangeable.
- Najafi supports Persian usage decisions.
- The Academy orthography guide supports spelling, spacing, half-spaces, and punctuation.
- Najaf Daryabandari's translation of *As I Lay Dying* may be used as a reference for natural Persian syntax, rhythm, and controlled reconstruction. Its fictional narrative voice must not be transferred wholesale into an academic essay.

No lexical source has automatic priority. Contextual accuracy, specialist meaning, natural Persian, register, and the author's argument must be weighed together.

Never claim a named source supports an equivalent unless the relevant entry or passage was actually checked.

## 6. Persian prose standard

Use clear verbs, natural Persian syntax, correct half-spaces, and measured sentence structure. Avoid bureaucratic padding such as «می‌باشد»، «می‌گردد» and «صورت پذیرفت» unless a specific context genuinely requires that register.

Keep a long English sentence in one Persian sentence only when its logical relations remain clear. Otherwise divide it without omitting, weakening, or inventing relationships.

From strong Persian prose references, adopt principles rather than surface imitation: rebuild English order, preserve rhythm, distinguish voices, use repetition deliberately, and avoid unnecessary explanation. Do not add an image, causal relation, degree of certainty, or metaphor that is absent from the source.

## 7. Confidence labels

Use these labels when a choice needs qualification:

- **Documented equivalent:** the relevant dictionary entry or specialist usage was actually checked.
- **Contextual proposal:** proposed from sentence analysis and context; specialist confirmation is still pending.
- **Historical source check needed:** the scope or historical reference of the term or claim is unclear.
- **Persian usage check needed:** several Persian meanings or constructions are possible and usage should be compared.
- **Stylistic choice:** the meaning is secure, but the final wording depends on Persian rhythm or register.

A confidence label describes evidence status; it is not a quality score.

## 8. Glossary policy

The active project glossary is `translation-references/GLOSSARY.md`.

Each entry must have a status:

- **candidate:** a useful proposed equivalent that has not yet been explicitly approved by Adel.
- **approved:** Adel explicitly accepted the equivalent for the stated sense/context.
- **reconsider:** a previously used or approved form needs renewed examination because the sense changes or new evidence appears.
- **retired:** an older project choice that should no longer be used, retained only for traceability.

Do not silently promote a candidate to approved. An approved equivalent is binding only for the stated sense; if an author uses the same English or German term differently elsewhere, reopen the decision.

Record actual source evidence separately from mentor reasoning.

## 9. File states and naming

For new work, use the practice-chunk identifier in filenames:

- Adel's submitted draft: `drafts/C00-S02-P01-draft-01.md`
- Mentor-reviewed proposal: `drafts/C00-S02-P01-reviewed-01.md`
- Review/teaching notes: `drafts/C00-S02-P01-review-notes-01.md`
- Explicitly approved version: `approved-translations/C00-S02-P01-approved.md`

If a revision is made before approval, increment the review number rather than overwriting the distinction between draft and proposal.

Existing historical filenames can remain unchanged. Do not rename them merely for cosmetic consistency.

## 10. Approval transition

A translation moves into `approved-translations/` only when Adel explicitly approves it.

Approval should record, in the file header or opening note where practical:

- chapter/unit/chunk ID;
- approval date;
- source draft or reviewed version on which it is based;
- unresolved terminology, if any.

A mentor proposal, even a polished one, remains a draft until this explicit transition occurs.

## 11. Report format for each practice chunk

Use the following structure unless a sentence-level question calls for a shorter response:

1. Brief assessment of strengths and main issues.
2. Passage role in the surrounding argument.
3. English grammar and structural decomposition.
4. Four-column comparison: English source, Adel's draft, mentor's revision, rationale.
5. Continuous proposed Persian translation.
6. Grammar and vocabulary lessons.
7. Terms requiring source checks or glossary decisions, with competing options.
8. Short exercise or diagnostic question when pedagogically useful.
9. Exact next position in the source.

The report should teach the reasoning behind the revision, not merely present the result.
