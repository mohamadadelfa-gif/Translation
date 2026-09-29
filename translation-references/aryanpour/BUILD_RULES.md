# BUILD RULES — Aryanpour retrieval layer

1. The canonical JSONL is immutable input.
2. Preserve `english` and `persian` values exactly as decoded in the canonical JSONL.
3. Never silently repair spelling, punctuation, spacing, or damaged characters in dictionary definitions.
4. `original_definition_markup` remains in the canonical JSONL; routine Markdown shards do not duplicate it.
5. Normalization is permitted only in navigation fields: Unicode NFKC, whitespace collapse, and case-folding.
6. Every canonical entry ID must occur exactly once in the generated dictionary layer.
7. Entries with the same exact English headword must remain in the same shard.
8. Keep shards small enough for reliable connector retrieval; current target: 300,000 UTF-8 bytes before the small shard header.
9. Surface `source_character_issue=true` in the derived entry.
10. Attribute a Persian equivalent to Aryanpour only after inspecting the actual referenced entry.
11. The derived layer is retrieval infrastructure, not an approved translation glossary.
12. Rebuilding must regenerate `manifest.json`, indexes, `SHARD-MAP.csv`, and QC validation.
