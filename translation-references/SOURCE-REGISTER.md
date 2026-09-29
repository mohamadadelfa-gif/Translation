# Translation Reference Register

Updated 2026-09-29.

This file defines the approved reference set and the role of each source in the English-to-Persian translation of *Revisiting Zero Hour 1945*.

Files under `sources/` are treated as supplied source material and should remain unchanged during ordinary translation work.

The presence of a source in this register means that it is available and approved for the stated role. It does **not** mean that every entry, page, definition, OCR result, or interpretation in that source has already been checked.

No dictionary or reference has automatic authority over the translation.

The source text, context, argument, specialist meaning, Persian usage, and Adel's final decision govern the final choice.

---

## 1. Primary source text

### Main book

`sources/revisiting-zero-hour-1945-structured.md`

This is the main structured source text for *Revisiting Zero Hour 1945*.

Use it to determine:

- source wording;
- argument;
- terminology;
- quotations;
- paragraph structure;
- endnotes;
- relations between chapters.

The source author's meaning and argumentative distinctions have priority over dictionary convenience.

### Chapter files

```text
sources/C00.md
sources/C01.md
sources/C02.md
sources/C03.md
sources/C04.md
sources/C05.md
```

These files provide chapter-level working access to the source.

They should be used together with the structured source when local context, paragraph structure, or endnotes are needed.

---

## 2. Structural and contextual guides

### Front matter

`sources/front-matter.md`

Use this file for publication context and front-matter information.

### Translation map

[Active translation map](../translation-preparation/START-HERE.md)

### Context and structure guide

[Active context and structure guide](../translation-preparation/CONTEXT-AND-STRUCTURE.md)

These are derived working guides for navigating the book and understanding its structure. The matching files under `sources/` are immutable supplied snapshots, not current workflow instructions. Do not assume automatic synchronization between the two layers.

They are **editorial and project aids**, not independent historical authorities.

Their chapter codes, unit labels, and explanatory divisions should not be confused with authorial section numbering unless the source itself contains those divisions.

---

## 2.1 English grammar and sentence structure

### Huddleston, Pullum & Reynolds — *A Student's Introduction to English Grammar*

Canonical source:

`sources/grammar/english/Rodney Huddleston, Geoffrey K. Pullum, Brett Reynolds - A Student's Introduction to English Grammar (2022, Cambridge University Press) - libgen.li.pdf`

Derived navigation and mentoring layer:

`translation-references/grammar/english/huddleston-pullum-reynolds/`

Use this source to analyse the grammatical structure of the English source text before translation, especially:

- matrix versus subordinate clauses;
- subjects, objects, complements, modifiers, and adjuncts;
- noun-phrase and prepositional-phrase structure;
- relative constructions;
- finite and non-finite clauses;
- auxiliaries, tense, aspect, and modality;
- coordination;
- negation and scope;
- information structure and information-packaging constructions.

This grammar explains English structure. It does not determine the Persian translation by itself.

For a difficult sentence, identify the grammatical relationships first, then explain how those relationships affect meaning, and only then compare possible Persian structures.

Do not attribute an analysis to Huddleston, Pullum, and Reynolds unless the relevant chapter or section has actually been inspected. If the mentor analyses a sentence without a source check, label that part as mentor grammatical analysis.

Use [CHAPTER-MAP.md](grammar/english/huddleston-pullum-reynolds/CHAPTER-MAP.md) as navigation only. Inspect the relevant canonical PDF chapter/section before attribution and record chapter/section/page when practical. Distinguish FORM, FUNCTION, DEPENDENCY and SCOPE as required by `MENTOR_WORKFLOW.md`.

---

## 3. General English–Persian vocabulary

The project uses **two active general bilingual references**:

1. Ariyanpour
2. Hezareh

Neither automatically has priority over the other.

For consequential, ambiguous, recurrent, or difficult vocabulary, compare both when relevant.

---

## 3.1 Ariyanpour

Canonical machine-readable source:

`translation-references/aryanpour/aryanpour-english-persian.jsonl`

Full readable export:

`translation-references/aryanpour/aryanpour-english-persian.txt`

Routine model retrieval:

`translation-references/aryanpour/index/`
→ `translation-references/aryanpour/dictionary/`

The canonical JSONL remains the source of record; the indexed Markdown layer is the routine lookup path.

Ariyanpour is one of the project's preferred general English–Persian vocabulary references.

The extracted LD2 data contains approximately 50,259 entries.

The Ariyanpour attribution was supplied for the project; the exact edition has not been independently verified.

Three known damaged source-character cases are recorded in:

`translation-references/aryanpour/source-character-issues.json`

### Role

Use Ariyanpour for:

- general lexical meanings;
- alternative Persian equivalents;
- distinguishing senses of polysemous English words;
- comparison with Hezareh;
- checking recurrent vocabulary.

Do not automatically choose the first equivalent.

Do not attribute a wording to Ariyanpour unless the relevant entry has actually been checked.

---

## 3.2 Hezareh

The current supplied Hezareh package contains eight Markdown extractions:

```text
sources/Hezareh_Dictionary_Index/source/Hezareh_Part_01_PDF_0001-0250.md
sources/Hezareh_Dictionary_Index/source/Hezareh_Part_02_PDF_0251-0500.md
sources/Hezareh_Dictionary_Index/source/Hezareh_Part_03_PDF_0501-0750.md
sources/Hezareh_Dictionary_Index/source/Hezareh_Part_04_PDF_0751-1000.md
sources/Hezareh_Dictionary_Index/source/Hezareh_Part_05_PDF_1001-1250.md
sources/Hezareh_Dictionary_Index/source/Hezareh_Part_06_PDF_1251-1500.md
sources/Hezareh_Dictionary_Index/source/Hezareh_Part_07_PDF_1501-1750.md
sources/Hezareh_Dictionary_Index/source/Hezareh_Part_08_PDF_1751-1976.md
```

The former top-level `.txt` paths are historical and are no longer present in the current checkout. The package's nested `source/` directory is intentional; it is not a typo for the project's `sources/` directory.

The supplied [index package](../sources/Hezareh_Dictionary_Index/README.md) provides lookup records and a [lookup script](../sources/Hezareh_Dictionary_Index/dictionary-index/hezareh_lookup.py). Treat the whole supplied package as read-only. Its internal example architecture is package documentation, not a replacement for this project's layout or workflow.

The index is a retrieval aid, not independent lexical evidence. Resolve its `source/...#L...` pointers relative to `sources/Hezareh_Dictionary_Index/`, inspect the cited extraction, and retain the PDF page and verification status. `visually_checked` records report the supplied package's review status; they do not establish that the current mentor checked the original PDF. `verification_status: raw_ocr` and `boundary_confidence: hint_only` require different qualifications; see the field and match semantics in [AGENTS.md](../AGENTS.md#hezareh-match-semantics). The original Hezareh PDF is not present in the tracked source collection; request the relevant page when extraction cannot support a consequential choice.

Hezareh is an **active bilingual vocabulary reference**, not merely a backup for Ariyanpour.

### Model retrieval layer

Canonical/extraction package:

`sources/Hezareh_Dictionary_Index/`

Routine model retrieval:

`translation-references/hezareh/index/`
→ `translation-references/hezareh/dictionary/`

The model layer contains 38,957 preserved records across 174 small Markdown shards. It preserves `verification_status`, `boundary_confidence`, PDF-page metadata, source pointers, duplicate normalized headwords, and whether reconstructed entry text is actually available.

Lookup order:

1. exact `normalized_headword`;
2. exact `base_normalized_headword` when needed;
3. follow the index locator into the Markdown shard;
4. inspect the complete record and `Source text`;
5. retain evidence-quality metadata in the reference account.

Evidence interpretation:

- `visually_checked`: inherited status from the supplied Hezareh package; do not imply a new current-session page check;
- `raw_ocr`: qualified OCR evidence; verify exact wording against the original page when consequential and available;
- `hint_only`: navigation/page hint only, not lexical evidence;
- multiple records for one normalized headword remain separate and must not be silently collapsed.

The index is navigation only. Do not say “Hezareh gives…” until the actual shard record and its source text have been inspected.


### Role

Use Hezareh for:

- general English–Persian lexical lookup;
- comparison of senses with Ariyanpour;
- additional Persian candidates;
- checking idiomatic or context-sensitive possibilities;
- investigating words where one dictionary alone does not adequately represent the semantic range.

### OCR caution

The supplied Hezareh text contains machine-recognized material.

Therefore:

- distinguish reliable-looking entries from suspicious OCR;
- do not silently repair damaged wording and then attribute the repair to Hezareh;
- when an entry is doubtful, mark the uncertainty;
- verify against the original page when possible and when the lexical decision is consequential.

This evidence-quality issue does **not** make Hezareh secondary to Ariyanpour.

---

## 4. Default bilingual vocabulary procedure

For a significant or uncertain English word or phrase:

```text
SOURCE CONTEXT
      ↓
ARIYANPOUR + HEZAREH
      ↓
COMPARE RELEVANT SENSES
      ↓
SPECIALIST SOURCE IF NEEDED
      ↓
PERSIAN OPTIONS
      ↓
ADEL'S DECISION
```

Agreement between Ariyanpour and Hezareh can strengthen confidence in a general lexical sense.

However:

```text
dictionary agreement
≠
automatic contextual correctness
```

The meaning in the source passage remains decisive.

When the dictionaries disagree:

1. identify which senses they are representing;
2. compare those senses with the sentence and argument;
3. consult a specialist source when necessary;
4. explain significant differences;
5. leave the final Persian choice with Adel.

No dictionary is selected merely because it appears first in the project documentation.

---

## 5. Humanities and theoretical terminology

### Ashouri — فرهنگ علوم انسانی

`sources/Ashouri — فرهنگ علوم انسانی.pdf`

Default retrieval locations:

- [Per-letter Markdown](ashouri/dictionary/)
- [Master CSV index](ashouri/index/headwords-master.csv)
- [Master JSONL index](ashouri/index/headwords-master.jsonl)
- [A–Z QC report](ashouri/qc/AZ-cross-letter-audit.md)

A–Z structural extraction is complete: 26,333 records, with 12,875 currently flagged for visual/OCR review in the supplied report. These counts describe extraction, not manual certification. Retrieve the entry and its QC record first. The PDF remains authoritative; under `AGENTS.md`, do not label an Ashouri equivalent `Documented equivalent` without visual verification of the relevant original page.

Use this source for:

- humanities terminology;
- philosophical and theoretical vocabulary;
- social-science concepts;
- established Persian terminology in relevant intellectual fields.

Ashouri is a specialist terminology source, not a replacement for contextual analysis.

Do not claim that Ashouri supports an equivalent unless the relevant entry has actually been inspected.

For a technical term, the working sequence may be:

```text
SOURCE CONTEXT
      ↓
ARIYANPOUR + HEZAREH
      ↓
ASHOURI
      ↓
SPECIALIST / HISTORICAL EVIDENCE
      ↓
PERSIAN DECISION
```

---

## 6. German historical and conceptual terminology

Use:

`translation-references/GERMAN-CONCEPTS.md`

for terms whose German historical, institutional, legal, political, intellectual, academic, or literary identity materially affects translation.

### German historical source collection

Canonical PDF collection:

`sources/german-historical-sources/`

The current collection is PDF-only and should be treated as historical/conceptual source material, not as pre-interpreted evidence. Its present files include:

- `AUS Politik UND ZeitGESCHiCHTE.pdf`
- `Gemeinsame Deutsche  Nachkriegsgeschichte.pdf`
- `Groupe 47.pdf`

Use these PDFs when a German historical, literary, political, or intellectual concept requires source verification. Do not infer support merely from a filename, title, or the presence of a book in the repository.

When one of these sources is used:

1. inspect the relevant passage in the PDF;
2. record the exact source and page or other available locator;
3. distinguish what the source explicitly states from mentor interpretation;
4. record the resulting conceptual analysis in `translation-references/GERMAN-CONCEPTS.md` when it is relevant to a recurring project term;
5. keep the Persian equivalent as a candidate until Adel explicitly approves it in the project glossary.

No Markdown conversion of the full German source collection is required by default. Create a derived searchable extraction only when repeated use of a particular source justifies it.

Examples include:

- `Stunde Null`
- `Nullpunkt`
- `Kahlschlag`
- `Vergangenheitsbewältigung`
- `Wiedergutmachung`
- `Germanistik`
- `Germanisten`
- `Wissenschaft`
- `Feuilleton`
- `Nachholen`
- `nachgeholte Résistance`

General bilingual dictionaries may provide lexical possibilities, but they do not by themselves establish the historical meaning of these concepts.

For such terms, distinguish:

- literal meaning;
- dictionary evidence;
- historical or conceptual evidence;
- author-specific usage;
- mentor interpretation;
- Persian candidates;
- Adel's approved translation decision.

Follow the procedures defined in:

`MENTOR_WORKFLOW.md`

and:

`translation-references/GERMAN-CONCEPTS.md`

Do not infer historical meaning from the German word alone.

---

## 7. Persian semantic field and word exploration

### فرهنگ طیفی — تزاروس فارسی

Canonical source:

`sources/فرهنگ طیفی - تزاروس فارسی.docx`

Supplied full-text extraction / audit aid:

`sources/فرهنگ طیفی - تزاروس فارسی.md`

Routine model retrieval:

`translation-references/persian-thesaurus/`

The canonical DOCX is authoritative for structure and wording. The derived retrieval layer was built from DOCX paragraph styles and source run formatting, not from Markdown heading syntax.

Build validation currently establishes:

- 991 numbered semantic entries, complete from 1 through 991;
- 10 semantic-entry Markdown shards;
- 82 sharded reverse term-occurrence indexes;
- 3,674 explicit source `⍃` cross-reference records;
- 88,759 reverse term-occurrence records;
- zero numbered-entry heading mismatches between the DOCX and supplied Markdown after Markdown unescaping;
- three known Markdown structural misclassifications where DOCX body material was promoted to Markdown headings: entry 316 (`مقولات هگل`), entry 708 (`طبقۀ اجتماعی`), and entry 868 (`طبقۀحاکمه`).

These three anomalies are recorded in:

`translation-references/persian-thesaurus/qc/markdown-structural-anomalies.csv`

### Role

Use the thesaurus for:

- exploring Persian semantic fields;
- finding related Persian expressions;
- comparing plausible formulations after the English meaning has been established;
- identifying neighboring concepts;
- examining explicit source cross-references;
- widening or narrowing Persian candidate wording.

The thesaurus does **not** determine the meaning of the English source and is not an English–Persian dictionary.

Its role comes after source interpretation:

```text
SOURCE MEANING
      ↓
BILINGUAL / SPECIALIST EVIDENCE
      ↓
INITIAL PERSIAN CANDIDATES
      ↓
PERSIAN THESAURUS
      ↓
PERSIAN SEMANTIC-FIELD COMPARISON
```

### Retrieval protocol

1. For a known numbered semantic-field heading, use `persian-thesaurus/index/entries-master.csv`.
2. For a source-bold lead term, use `persian-thesaurus/index/lead-terms.csv`.
3. For another Persian candidate term or phrase, use `persian-thesaurus/index/TERM-SHARD-MAP.csv` to select the relevant reverse-occurrence shard under `persian-thesaurus/index/terms/`.
4. Follow the returned `file` and `anchor` into the complete semantic entry under `persian-thesaurus/entries/`.
5. Inspect the full semantic field before using it as evidence.
6. When relevant, use `persian-thesaurus/index/explicit-cross-references.csv`, which records only explicit source `⍃` relations.
7. If structure or wording is consequential or ambiguous, resolve it against the canonical DOCX.

The reverse term index is navigation only. A word appearing in one semantic entry does not by itself establish synonymy, equivalence, broader/narrower relation, or recommendation.

Do not write:

> “The thesaurus recommends X”

merely because X occurs in the same semantic field.

Use the reference-account form:

`Persian thesaurus — entry <id> «<heading>» — <shard>#<anchor> — finding — effect on translation`

Project translation decisions belong in `GLOSSARY.md`; they must not be written back into the thesaurus source or retrieval layer.

---

## 8. Persian usage

### Najafi — غلط ننویسیم

Canonical source:

`sources/Najafi — غلط ننویسیم.pdf`

The active canonical file is the clearer 480-page scan currently stored at this path. It replaced the earlier 150-page scan; the earlier scan is retired from the active workflow.

This PDF is a visual authority. Its machine-readable text layer is not reliable enough to treat as Najafi's wording. For consequential usage evidence, inspect the relevant scanned page visually before attributing a recommendation to Najafi.

Use Najafi for consequential questions of Persian usage.

Relevant uses include:

- questionable constructions;
- standard versus problematic usage;
- lexical usage questions;
- Persian syntactic conventions where the source is relevant.

Najafi is a Persian usage reference.

It does not determine the meaning of the English source.

Until a verified `translation-references/najafi/` entry layer exists, record the exact PDF page inspected and distinguish visual source evidence from mentor interpretation. Any future Najafi retrieval layer must preserve the PDF as canonical and must not promote unverified OCR to source evidence.

---

## 9. Persian orthography

### فرهنگستان — دستور خط فارسی

Canonical source:

`sources/فرهنگستان — دستور خط فارسی.pdf`

Searchable structured reference:

`translation-references/academy-orthography/`

Use the structured Markdown layer as the default retrieval route for locating relevant orthographic rules, examples, sections, and page references. It preserves PDF-page and printed-page markers and is intended to make the Academy guide searchable during translation review.

The original PDF remains the canonical source. When a consequential rule, table, ambiguous extraction, or edition-specific detail matters, verify the structured Markdown against the corresponding PDF page before making a categorical claim.

Use the Academy guide for:

- spelling;
- spacing;
- half-spaces;
- compounds;
- affixes;
- punctuation conventions where covered;
- Persian character and orthographic conventions.

The Academy guide regulates written form.

It is not a lexical or conceptual authority on the English source.

When citing or reporting an Academy finding, identify the relevant Markdown section and retained PDF/printed-page locator when available. Do not claim that a rule was checked if only a generic search result or file title was seen.

---

## 10. Persian translated-prose reference

### Najaf Daryabandari — *As I Lay Dying / گور به گور*

`sources/گور به گور - ویلیام فاکنر.pdf`

This file is the Persian translation of William Faulkner's *As I Lay Dying* (*گور به گور*) by Najaf Daryabandari.

Use it as a **translation-craft and Persian prose reference**.

It is not a general bilingual dictionary and should not normally be used as direct lexical authority.

### Retrieval and alignment

Canonical English source: `sources/Faulkner - As I Lay Dying - Corrected Text.pdf`; the Persian PDF above remains canonical for the translation.

- [Paired sections CSV](../translation-preparation/translation-craft-corpus/paired-sections.csv)
- [Paired sections JSONL](../translation-preparation/translation-craft-corpus/paired-sections.jsonl)
- [English per-section corpus](../translation-preparation/translation-craft-corpus/faulkner-as-i-lay-dying/text/)
- [Persian per-section corpus](../translation-preparation/translation-craft-corpus/daryabandari-as-i-lay-dying/text/)
- [Analytical pilot cases](translation-craft/daryabandari/parallel-cases.jsonl)

The 59-pair corpus is retrieval/alignment infrastructure at section level, not global sentence alignment. Resolve pilot `section` IDs through the alignment table; pilot cases are analytical examples, not independent source evidence. Inspect both actual passages before making a source-to-translation claim and verify consequential transcription against the PDFs. Valid checksums establish file integrity, not OCR/transcription correctness or translation quality.

### Main role

Study how a professional translator reconstructs English prose in Persian, especially:

- sentence restructuring;
- movement of clauses;
- release from English word order;
- selection of natural Persian verbs;
- rhythm;
- verbal economy;
- transitions;
- control of sentence length;
- deliberate repetition;
- preservation of logical relations during restructuring;
- balance between fidelity and natural Persian expression.

### Important limitation

*As I Lay Dying* is a literary work with multiple fictional voices.

Therefore, do not mechanically transfer:

- its narrative voice;
- colloquial features;
- characterization;
- dialectal effects;
- literary mannerisms;
- fictional rhythm

into the scholarly prose of *Revisiting Zero Hour 1945*.

Use **translation techniques**, not surface imitation.

### Evidence discipline

Do not make broad claims such as:

> “Daryabandari always translates this structure in this way.”

unless relevant passages have actually been inspected.

When using Daryabandari as evidence for a translation technique, identify the specific passage or pattern being examined whenever practical.

An observation about the Persian prose requires inspection of the Persian passage. A claim about a change from English to Persian (such as clause reordering, omission, or sentence splitting) also requires the corresponding English passage. If only the Persian is available, label the observation as Persian prose analysis, not a verified source-to-translation comparison.

---

## 11. Project glossary

Use:

`translation-references/GLOSSARY.md`

for practical recurring translation decisions.

This file records project choices; it is not itself a dictionary.

A glossary entry may record evidence such as:

```text
Ariyanpour + Hezareh
```

or:

```text
Hezareh + Ashouri
```

or:

```text
Ariyanpour + Hezareh + historical source
```

Do not write “dictionary confirmed” without identifying which source was actually checked.

Glossary status must follow:

- `candidate`
- `approved`
- `reconsider`
- `retired`

A candidate does not become approved merely because it has been used repeatedly.

Adel must explicitly approve it.

An approved term applies to the stated sense and context, not automatically to every occurrence of the same source word.

---

## 12. Source roles at a glance

| Source | Primary role |
| --- | --- |
| *Revisiting Zero Hour 1945* | meaning, argument, source wording, context |
| Huddleston, Pullum & Reynolds | English grammar and sentence-structure analysis |
| Ariyanpour | general English–Persian vocabulary |
| Hezareh | general English–Persian vocabulary |
| Ashouri | humanities and theoretical terminology |
| `GERMAN-CONCEPTS.md` + checked historical sources | German historical and conceptual terminology |
| فرهنگ طیفی | Persian semantic fields and alternative expressions |
| Najafi | Persian usage |
| فرهنگستان | orthography and writing conventions |
| Daryabandari, *As I Lay Dying / گور به گور* | translation craft and Persian prose reconstruction |
| `GLOSSARY.md` | recording project terminology decisions |

---

## 13. Evidence discipline

Always distinguish between the following categories.

### Source evidence

What the original English text actually says.

### Dictionary evidence

What Ariyanpour, Hezareh, or another checked dictionary actually records.

### Specialist evidence

What a checked specialist, historical, legal, philosophical, literary, or disciplinary source actually supports.

### Historical or conceptual evidence

What checked historical or conceptual sources establish about a historically specific term.

### Persian usage evidence

What a checked Persian usage or orthographic reference supports.

### Prose comparison

What can be observed in a specific translated-prose example such as Daryabandari.

### Mentor analysis

An interpretation or recommendation developed from context and comparison.

### Adel's decision

The final project translation choice.

These categories must not be silently collapsed.

---

## 14. Reference-use rule

Before saying:

> “Ariyanpour gives…”

check Ariyanpour.

Before saying:

> “Hezareh gives…”

check Hezareh.

Before saying:

> “Ashouri uses…”

inspect Ashouri.

Before saying:

> “Najafi recommends…”

inspect Najafi.

Before saying:

> “The Academy rule is…”

inspect the supplied Academy guide.

Before saying:

> “Daryabandari handles this structure by…”

inspect the relevant passage from *گور به گور*.

Before describing the historical meaning of a German concept, consult appropriate historical or specialist evidence.

Never fabricate source support.

---

## 15. Core source-selection principle

Different sources answer different questions.

```text
WHAT DOES THE ENGLISH MEAN?
→ source text + context

HOW IS THE ENGLISH SENTENCE STRUCTURED?
→ Huddleston, Pullum & Reynolds

WHAT LEXICAL SENSES ARE AVAILABLE?
→ Ariyanpour + Hezareh

IS THIS A SPECIALIST HUMANITIES TERM?
→ Ashouri + relevant specialist sources

IS THIS A GERMAN HISTORICAL CONCEPT?
→ GERMAN-CONCEPTS.md + checked historical sources

WHAT PERSIAN WORDING OPTIONS EXIST?
→ فرهنگ طیفی

IS THIS GOOD OR STANDARD PERSIAN USAGE?
→ Najafi

HOW SHOULD IT BE WRITTEN?
→ Academy orthography guide

HOW CAN ENGLISH PROSE BE REBUILT NATURALLY IN PERSIAN?
→ Daryabandari / گور به گور

WHAT HAS THIS PROJECT DECIDED?
→ GLOSSARY.md

WHO MAKES THE FINAL TRANSLATION DECISION?
→ Adel
```

No source should be used outside its evidentiary role without explanation.

---

## 16. Practical lookup sequence

For an ordinary but consequential lexical problem:

```text
1. Read the full sentence and paragraph
2. Determine the likely contextual sense
3. Check Ariyanpour
4. Check Hezareh
5. Compare relevant senses
6. Check Persian semantic options in فرهنگ طیفی when useful
7. Evaluate natural Persian usage
8. Present candidates
9. Adel decides
```

For a humanities or theoretical term:

```text
SOURCE CONTEXT
      ↓
ARIYANPOUR + HEZAREH
      ↓
ASHOURI / SPECIALIST SOURCE
      ↓
PERSIAN SEMANTIC OPTIONS
      ↓
ADEL'S DECISION
```

For a historically significant German concept:

```text
SOURCE CONTEXT
      ↓
EXACT GERMAN CONCEPT
      ↓
ARIYANPOUR + HEZAREH FOR LEXICAL RANGE
      ↓
HISTORICAL / DISCIPLINARY EVIDENCE
      ↓
GERMAN-CONCEPTS.md
      ↓
PERSIAN CANDIDATES
      ↓
ADEL'S DECISION
```

For Persian prose reconstruction:

```text
MEANING ALREADY ESTABLISHED
      ↓
ANALYZE ENGLISH SYNTAX
Huddleston, Pullum & Reynolds when needed
      ↓
REBUILD IN NATURAL PERSIAN
      ↓
CONSULT DARYABANDARI WHEN A COMPARABLE
TRANSLATION TECHNIQUE WOULD BE USEFUL
      ↓
CHECK PERSIAN USAGE / ORTHOGRAPHY
      ↓
FINAL PROPOSAL
```

Daryabandari should normally enter **after meaning has been established**, not before.

---

## 17. Deferred or unverified materials

The previously mentioned Babylon Ariyanpour BDC comparison remains deferred unless Adel chooses to resume it.

Cronin, K1, RTS, or other frameworks mentioned in older planning materials are not active lexical, historical, or translation authorities unless the relevant source documents are actually supplied and reviewed.

`MENTOR_WORKFLOW.md` and the current project instructions govern **method and pedagogy**.

They are not themselves lexical or historical evidence.

---

## 18. Final rule

The project should never ask only:

> “Which dictionary gives the best Persian word?”

The correct sequence is:

```text
SOURCE
   ↓
CONTEXT AND ARGUMENT
   ↓
ARIYANPOUR + HEZAREH
   ↓
SPECIALIST / HISTORICAL SOURCES WHEN NEEDED
   ↓
PERSIAN SEMANTIC AND USAGE SOURCES
   ↓
PROSE RECONSTRUCTION WHEN NEEDED
   ↓
COMPARISON OF OPTIONS
   ↓
ADEL'S DECISION
```

The purpose of the reference system is not to replace translation judgment.

It is to make that judgment more informed, explicit, teachable, and traceable.
