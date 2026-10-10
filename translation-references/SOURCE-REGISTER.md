# Translation Reference Register

Updated 2026-10-07.

This file defines the approved reference set and the role of each source in the English-to-Persian translation of *Revisiting Zero Hour 1945*.

Files under `sources/` are frozen snapshots of supplied repository material and must not receive new working edits, segmentation, mentor notes, or translation changes. Existing conversion/segmentation artifacts already present in those snapshots are preserved rather than silently cleaned.

The presence of a source in this register means that it is available and approved for the stated role. It does **not** mean that every entry, page, definition, OCR result, or interpretation in that source has already been checked.

No dictionary or reference has automatic authority over the translation.

The source text, context, argument, specialist meaning, Persian usage, and Adel's final decision govern the final choice.

---

## 1. Primary source text

### Main book

Primary provenance and authority are recorded in [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md).

The original 115-page PDF has been recovered and visually identified; its SHA-256 is recorded there. The PDF is the canonical visual authority, but the binary is not yet tracked in GitHub.

Tracked searchable snapshot:

`sources/revisiting-zero-hour-1945-structured.md`

Active working derivative:

`translation-preparation/revisiting-zero-hour-1945-structured.md`

Use the structured text for searchable access to:

- source wording;
- argument;
- terminology;
- quotations;
- paragraph structure;
- endnotes;
- relations between chapters.

When wording, layout, quotation, page, or extraction is consequential or disputed, verify against the original PDF when available. The source author's meaning and argumentative distinctions have priority over dictionary convenience.

### Chapter working files

```text
translation-preparation/C00.md
translation-preparation/C01.md
translation-preparation/C02.md
translation-preparation/C03.md
translation-preparation/C04.md
translation-preparation/C05.md
```

These files provide the **active chapter-level working access** used during translation sessions. They are derived/project working files and may contain translation-unit markers or other navigation aids.

The matching `sources/C00.md`–`sources/C05.md` files are frozen supplied snapshots. Do not edit or synchronize them during ordinary work. Use the active files in `translation-preparation/` for local context, paragraph structure, endnotes, and future segmentation changes.

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

## 2.2 Persian grammar and OCR/text-extraction quality assurance

### Saeed Yousef — *Persian: A Comprehensive Grammar* (Routledge, 2018)

Reusable index and conservative checker:

`translation-references/grammar/persian/saeed-yousef/`

The [OCR support module](grammar/persian/saeed-yousef/ocr-support/README.md) contains a tested, non-destructive Python issue reporter, grammar-section pointers, machine-readable error taxonomy, visually checked example, and review policy. Use it to flag possible spacing, letter-encoding, bidirectional-text, and word-order extraction anomalies; **never automatically correct** raw source text. It also supports standalone use outside the translation project.

Canonical visual authority is the **user-supplied 2018 PDF**, SHA-256 `d7fe1280e629caa8488db6436b51f7fee4550a37303364e0d43c8d3005e5ca2d`. The PDF and the private full-book extraction are not published in this public repository. The map gives **printed-page locators**, not verified grammatical quotations or rules; inspect the relevant PDF page before attributing substantive guidance to Yousef. For normative orthography use the Academy writing guide and compare the actual page. The one visually checked case is a **PDF text-layer reading-order problem**, not an OCR-engine error.

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

The index is a retrieval aid, not independent lexical evidence. Resolve its `source/...#L...` pointers relative to `sources/Hezareh_Dictionary_Index/`, inspect the cited extraction, and retain the PDF page and verification status. `visually_checked` records report the supplied package's review status; they do not establish that the current mentor checked the original PDF. `verification_status: raw_ocr` and `boundary_confidence: hint_only` require different qualifications as recorded below. The original Hezareh PDF is not present in the tracked source collection; request the relevant page when extraction cannot support a consequential choice.

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
5. when a matching record-ID annotation exists under `translation-references/hezareh/revisions-v2/`, inspect it as supplementary machine interpretation;
6. retain the inherited evidence-quality metadata in the reference account.

The Profile v2 overlay does not replace the original record. It may separate likely grammar/context labels or identify boundary contamination, but it cannot by itself promote `raw_ocr` to `visually_checked`, raise boundary confidence, or approve Persian terminology.

Evidence interpretation:

- `visually_checked`: inherited status from the supplied Hezareh package; do not imply a new current-session page check;
- `raw_ocr`: qualified OCR evidence; verify exact wording against the original page when consequential and available;
- `hint_only`: navigation/page hint only, not lexical evidence;
- multiple records for one normalized headword remain separate and must not be silently collapsed.

Match semantics:

- distinguish **exact headword**, **exact base-headword**, **verified exact alias**, **prefix**, and **full-text fallback**;
- establish a verified alias only from an actual alias record plus checked source evidence, not from a phrase merely appearing inside OCR;
- a prefix or full-text hit is a retrieval clue, not proof that the queried expression has its own Hezareh entry;
- the current lookup tool does not expose match type directly, so classify it from inspected records when possible and otherwise leave the match type unspecified rather than inventing one.

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

A–Z structural extraction is complete: 26,333 records, with 12,875 currently flagged for visual/OCR review in the supplied report. These counts describe extraction, not manual certification. Retrieve the entry and its QC record first. The PDF remains authoritative. A structured/OCR hit may locate a candidate, but an Ashouri equivalent must not be labelled `Documented equivalent` until the relevant original PDF page has been visually checked and applicable QC uncertainty has been inspected.

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

### Wiechert speech — derived searchable text (added 2026-10-10)

- Searchable German transcription: [*Rede an die deutsche Jugend 1945*](german-historical-sources/wiechert-1945/wiechert-rede-an-die-deutsche-jugend-1945.md).
- Source profile and extraction QA: [Wiechert source profile](german-historical-sources/wiechert-1945/SOURCE-PROFILE.md).
- Basis: user-supplied 14-page 2023 PDF transcription; original German speech delivered on 11 November 1945. The supplied PDF SHA-256 and provenance caveats are recorded in the profile. The uploaded binary PDF is not currently committed in this repository.
- **Authority boundary:** this later transcription is a German historical comparison source; Brockmann's English remains the target text for Persian translation. The PDF has not been collated against the original 1945 printed edition, and it does not contain Kuby's 1947 response.


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
- finding related Persian expressions and semantic families;
- comparing plausible formulations after the English meaning has been established;
- matching candidate wording to the tone, register, and rhetorical force of the English passage;
- comparing candidates with the surrounding translated sentences so the local Persian voice remains coherent;
- identifying neighboring concepts;
- examining explicit source cross-references;
- widening or narrowing Persian candidate wording.

**Project status:** فرهنگ طیفی is a fully approved project reference. Its canonical DOCX is authoritative for its internal structure and wording. This approval concerns the reliability and role of the reference itself; it does not mean that every co-occurring term is a synonym or that any candidate translation is automatically approved.

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

The Najafi retrieval layer at `translation-references/najafi/` now has two navigation paths. `index/headwords-master.csv` is the smaller body-heading layer verified directly against scanned dictionary pages. `index/source-index-master.csv` is the complete navigation-candidate representation of Najafi's own printed *فهرست راهنما* on PDF pages 449–478, with `index/source-index-page-map.csv` preserving source-index location. Because the scan has no usable Persian text layer, OCR was used only to digitize this printed index for navigation; those candidate rows are **not** Najafi evidence. Lookup order is: verified body-heading match → exact/fuzzy printed-source-index candidate → open the indicated canonical dictionary-body page → visually verify the actual heading and entry. A machine-index miss or malformed candidate still does not prove that Najafi lacks the entry; inspect the relevant printed source-index/body range directly. Record usable evidence as `Najafi — «<headword>» — PDF p. <pdf_page> / printed p. <printed_page> — visually_checked — finding — effect on translation`. Entry transcription under `translation-references/najafi/entries/` remains incremental and must preserve the PDF as canonical.

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

- [Paired sections CSV](translation-craft/corpus/paired-sections.csv)
- [Paired sections JSONL](translation-craft/corpus/paired-sections.jsonl)
- [English per-section corpus](translation-craft/corpus/faulkner-as-i-lay-dying/text/)
- [Persian per-section corpus](translation-craft/corpus/daryabandari-as-i-lay-dying/text/)
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

## 13. Workflow ownership and deferred source state

This register defines **what each source is, where it lives, how to retrieve its evidence, and what limitations attach to that evidence**.

The authoritative rules for **when** a source must be checked, sentence-vs-paragraph scope, evidence outcomes, review readiness, approval, confidence labels, and file-state transitions live only in:

`MENTOR_WORKFLOW.md`

Do not create a second evidence gate or review sequence in this register.

Current source-state notes:

- the Babylon Ariyanpour BDC comparison remains deferred unless Adel explicitly resumes it;
- Cronin, K1, RTS, or other frameworks mentioned in older planning materials are not active lexical, historical, or translation authorities unless the relevant source documents are actually supplied and reviewed;
- source availability or inclusion in this register never implies that a particular entry/page has been checked for the current passage.

No rule in this register overrides `MENTOR_WORKFLOW.md`.
