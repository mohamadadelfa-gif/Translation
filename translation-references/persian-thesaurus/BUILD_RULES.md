# Build rules

1. The canonical DOCX under `sources/` is immutable.
2. The supplied Markdown remains an audit/search aid; it is not the structural build authority.
3. DOCX paragraph styles define part/class/section/bab/entry structure.
4. Numbered `title06` paragraphs define semantic entries. Unnumbered `title06` inside an entry remains an internal source subheading.
5. Source paragraph wording is preserved. Do not modernize, normalize, correct, or silently repair the source text.
6. Source bold formatting may be represented as Markdown bold; this is presentation markup only.
7. Index normalization is allowed only in dedicated search-key fields. It must not alter displayed source text.
8. `lead-terms.csv` reflects source headings/bold lead terms; it does not by itself establish synonymy.
9. The term-occurrence index is navigation only. `occurs in the same semantic entry` must not be converted into `is a synonym`.
10. Parse relations as explicit cross-references only when the source uses the `⍃` relation line. Other arrow-like notation remains in source text unless separately verified.
11. Translation-project decisions belong in `GLOSSARY.md`; never write them back into the thesaurus source.
12. The full semantic entry must be inspected before citing the thesaurus as evidence.
