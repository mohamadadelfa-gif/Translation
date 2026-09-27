# Hezareh Dictionary Index

Derived lookup layer for the eight source Markdown files of **فرهنگ هزاره**.

## Design rule

The files in `source/` are the evidence layer and are not rewritten by this index.

The index is derived from:
- visually checked `ENTRY:` / `PHRASE:` blocks when available;
- otherwise the explicit **unverified English lookup hints** already present in the source extraction.

Lookup hints are used only to locate candidate entries. They are **not treated as definitions**.

## Files

- `source/` — the eight unchanged Markdown source files.
- `dictionary-index/hezareh_dictionary.jsonl` — one record per checked entry/phrase or raw OCR headword candidate.
- `dictionary-index/hezareh_pages.jsonl` — one record per canonical PDF page (1–1976).
- `dictionary-index/hezareh_dictionary.sqlite` — searchable SQLite database with exact indexes and FTS5.
- `dictionary-index/hezareh_lookup.py` — portable command-line lookup tool.
- `dictionary-index/manifest.json` — build statistics and checksums.

## Record schema

Important fields in `hezareh_dictionary.jsonl`:

- `headword`
- `normalized_headword`
- `base_normalized_headword`
- `aliases`
- `record_type`
- `verification_status`: `visually_checked` or `raw_ocr`
- `boundary_confidence`: `high`, `medium`, `low`, or `hint_only`
- `part`
- `pdf_page`
- `printed_page` when available
- `source_file`
- `source_line_start` / `source_line_end`
- `source_pointer`
- `entry_text`
- `review_scope`

## Precedence rule

For a headword on the same PDF page:

1. `visually_checked` wins over `raw_ocr`.
2. Raw OCR is retained for audit but should not override checked wording.
3. `hint_only` means the page is known from the source navigation hint, but an entry boundary could not be reconstructed safely.

## Boundary-page deduplication

Parts 02–08 contain the preceding PDF page intentionally for continuity. Those duplicated pages remain unchanged in `source/`, but the searchable index contains each PDF page **once**, assigned to its primary part.

Canonical page coverage: **1–1976**.

## Translation Mentor lookup policy

Recommended order:

1. Exact `normalized_headword`.
2. Exact `base_normalized_headword` (so `may` can reach `may (1)`).
3. Prefix lookup.
4. Full-text search as fallback.

When returning a result, the Mentor should always surface:

- headword;
- Persian source text;
- PDF page;
- verification status;
- source pointer.

For `raw_ocr`, show:

> Raw OCR — verify against the PDF if this wording affects the translation.

Never promote an OCR reading into an approved glossary entry automatically.

## Local lookup

From `dictionary-index/`:

```bash
python hezareh_lookup.py "maximum"
python hezareh_lookup.py "manner"
python hezareh_lookup.py "reprehensible"
```

`maximum` should prefer the visually checked entry on PDF page 1017.

## Integration principle

Use this repository structure:

```text
translation-project/
├── source/
│   └── hezareh/
│       └── [8 source Markdown files]
├── dictionary-index/
│   └── hezareh/
│       ├── hezareh_dictionary.jsonl
│       ├── hezareh_pages.jsonl
│       ├── hezareh_dictionary.sqlite
│       └── hezareh_lookup.py
├── translation/
├── glossary/
└── mentor/
```

The dictionary index is a **retrieval layer**, not a replacement for the source.
