# Faulkner — *As I Lay Dying* — Structured English Source

This package is designed to pair directly with the Daryabandari Persian Markdown corpus.

## Contents

```text
faulkner-as-i-lay-dying-md/
├── README.md
├── 00-front-matter.md
├── 01-main-corpus.md
├── 02-publisher-and-editorial-notes.md
├── text/
│   ├── 001-darl.md
│   ├── 002-cora.md
│   └── ...
│   └── 059-cash.md
├── index/
│   ├── chapter-map.csv
│   └── alignment-map.csv
├── raw-pages/
└── qc/
    └── conversion-report.md
```

## Alignment principle

Section numbers are aligned one-to-one with the 59-section Daryabandari corpus.

Example:

```text
English: text/001-darl.md
Persian: text/001-darl.md
```

The two corpora can therefore be compared by `section` without relying on page numbers.

## Next research step

Use `index/alignment-map.csv` to select passages and build a translation-operation corpus:

```text
Faulkner source
→ Daryabandari rendering
→ identify operation
→ formulate Persian translation-craft rule
```

## Status

- English structural conversion: complete
- 59-section alignment: verified structurally
- Sentence-level English↔Persian alignment: not yet performed
