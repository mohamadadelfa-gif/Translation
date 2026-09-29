# Persian Thesaurus — model retrieval layer

Derived retrieval layer for **فرهنگ طیفی (تزاروس فارسی)** by جمشید فراروی.

## Permanent source architecture

Canonical source:

`sources/فرهنگ طیفی - تزاروس فارسی.docx`

Supplied full Markdown extraction (audit/search aid):

`sources/فرهنگ طیفی - تزاروس فارسی.md`

Routine model retrieval:

`translation-references/persian-thesaurus/`

The canonical DOCX is authoritative. This layer is derived from DOCX paragraph styles and run formatting, not from Markdown heading syntax.

## Why DOCX drives the build

The supplied Markdown contains all 991 numbered semantic entries in sequence, but three DOCX body paragraphs were accidentally promoted to Markdown headings:

- entry 316 — `مقولات هگل`
- entry 708 — `طبقۀ اجتماعی`
- entry 868 — `طبقۀحاکمه`

Those are recorded in `qc/markdown-structural-anomalies.csv`. The retrieval layer therefore reconstructs structure directly from the DOCX.

## What an entry means

A numbered thesaurus entry is a **Persian semantic field**, not an English→Persian dictionary definition.

Do not treat words appearing in one entry as automatically interchangeable synonyms.

## Retrieval order

1. If you know the semantic-field heading, search `index/entries-master.csv`.
2. For a strong source-marked term, search `index/lead-terms.csv`.
3. For any Persian candidate word or phrase, use `index/TERM-SHARD-MAP.csv` to select the relevant occurrence-index shard under `index/terms/`.
4. Follow `file` + `anchor` to the complete numbered entry under `entries/`.
5. Inspect the full semantic field and its explicit cross-references before using it in translation analysis.

The occurrence index records only that a string **occurs in an entry**. It does not claim synonymy, equivalence, broader/narrower relation, or recommendation.

## Role in the Translation Mentor

Correct sequence:

```text
English source + context
        ↓
Ariyanpour + Hezareh
        ↓
Ashouri / specialist evidence when needed
        ↓
initial Persian candidates
        ↓
Persian thesaurus semantic-field exploration
        ↓
usage / orthography / prose reconstruction
        ↓
translation proposal
        ↓
Adel's decision
```

The thesaurus explores Persian semantic neighborhoods after source meaning has been established.

## Reference account

Use:

`Persian thesaurus — entry <id> «<heading>» — <file>#<anchor> — relevant terms/relations — effect on proposal`

Do not say that the thesaurus “recommends” a translation merely because a word appears in the same field.

## Indexes

- `index/entries-master.csv` — all 991 semantic entries + hierarchy + shard locators.
- `index/lead-terms.csv` — numbered headings and source-bold lead terms.
- `index/terms/` — sharded reverse occurrence index for Persian words/phrases.
- `index/TERM-SHARD-MAP.csv` — maps initial normalized character to occurrence-index shards.
- `index/explicit-cross-references.csv` — only explicit `⍃` source cross-references.
- `index/ENTRY-SHARD-MAP.csv` — semantic-entry shard map.

## QC

`qc/build-validation.json` validates numbering, source checksums, shard counts, and Markdown-vs-DOCX structural anomalies.

`qc/markdown-structural-anomalies.csv` records extraction structure that must not be mistaken for the canonical DOCX hierarchy.
