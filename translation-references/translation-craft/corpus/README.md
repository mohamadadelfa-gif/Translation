# Translation-Craft Parallel Corpus

This directory is a **derived working layer** for studying English→Persian translation craft.

Canonical source PDFs remain under `sources/` and are authoritative.

## Corpora

```text
translation-preparation/translation-craft-corpus/
├── README.md
├── source-manifest.json
├── paired-sections.csv
├── paired-sections.jsonl
├── faulkner-as-i-lay-dying/
│   ├── 01-main-corpus.md
│   ├── text/001-darl.md ... text/059-cash.md
│   ├── index/
│   └── qc/
└── daryabandari-as-i-lay-dying/
    ├── 01-translators-note.md
    ├── 02-main-corpus.md
    ├── text/001-darl.md ... text/059-cash.md
    ├── index/
    └── qc/
```

## Layer discipline

```text
sources/
→ canonical supplied documents

translation-preparation/translation-craft-corpus/
→ derived, section-addressable working corpus

translation-references/translation-craft/daryabandari/
→ analytical rules and translation-craft knowledge
```

Do not treat the Markdown transcription as stronger evidence than the scanned source.

## Alignment

The two corpora are aligned structurally by section number: 59 English sections and 59 Persian sections.

Use `paired-sections.csv` or `paired-sections.jsonl` to retrieve the exact English/Persian pair.

Sentence-level alignment is **not** claimed globally. The current craft pilot contains only manually selected/aligned examples.

## Trust rule

For a claim such as “Daryabandari reordered/split/recast X”:

1. retrieve the exact English section;
2. retrieve the exact Persian section;
3. check both against their canonical PDF pages if consequential;
4. state the observed operation;
5. keep the interpretation separate from the source wording.
