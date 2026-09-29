# Build rules

1. The canonical package under `sources/Hezareh_Dictionary_Index/` is immutable.
2. Every JSONL record must appear exactly once in the derived Markdown layer.
3. Record IDs, headwords, `entry_text`, verification status, boundary confidence, PDF/page metadata, and source pointers are preserved.
4. `entry_text` is copied verbatim. Do not silently correct OCR, spelling, punctuation, spacing, or damaged characters.
5. Multiple records for the same normalized headword are preserved and kept in the same shard.
6. The index is only a navigation layer. It is not lexical evidence.
7. A Hezareh attribution requires inspection of the actual Markdown record and its source text.
8. `hint_only` records are not lexical evidence. They are lookup/page hints requiring verification.
9. `raw_ocr` evidence must remain explicitly qualified; consequential wording should be checked against the original source when available.
10. `visually_checked` means the supplied package carried that status; it does not mean a new visual check happened during this build.
