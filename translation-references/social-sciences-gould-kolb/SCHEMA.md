# Gould/Kolb source-preserving digital dictionary schema

**Mandatory source guide:** [EDITORIAL_RULES.md](EDITORIAL_RULES.md) and [editorial_rules.json](editorial_rules.json) govern this schema. The Persian editor specifies A–E exposition sections, `see → ←`, `also → نیز`, contributor credits, and house editing conventions (physical PDF pp. 12–16). The build must validate the guide before publishing lookup records.

## Authority order

1. Exact PDF bytes and SHA256 registered in source_manifest.json
2. Original page images, physical PDF page number and column
3. Visually checked literal headword, European-language term, referral arrow and short back-glossary mapping
4. A fully transcribed definition only after visual comparison and review
5. Derived lookup keys and separate editorial interpretation

## Main dictionary entry

Record type: dictionary_entry; entry_kind: main, referral, also, or uncertain.
Use headword_fa_exact and headword_en_exact for literal source-heading forms. Slash-separated variants stay in their original heading string. Record start_pdf_page, start_column, and evidence_pdf_pages. A null end_pdf_page means no reviewed entry end has been established.

Article sections marked A, B, C, D and E are editorial exposition and **not automatically dictionary senses**. observed_section_labels means only that the printed labels were seen.

A referral requires marker ← and literal target text. An `also` entry requires separate `related_marker_literal: نیز` and `related_target_literal` fields, with an unverified relation status; never encode an `also` as a `see` referral. Keep target_resolution_status unverified until the referred-to main entry has been independently identified. Article_text_exact and contributors_exact remain null in Phase 1; semantic_review_status is not_started. Never fill these fields from model inference or unreviewed OCR.

## Back glossary row

record_type: glossary_row. Capture english_exact and persian_exact exactly as displayed, along with pdf_page, column, row_order_within_column, and evidence_pdf_page. The index occupies PDF pages 957–978 in *reverse alphabetic page order*. printed_glossary_page_inferred is not a directly reviewed printed folio for every page.

main_entry_id is null and main_entry_resolution_status is not_attempted until a matching full dictionary entry is verified. Glossary translation pairs are not substitutes for authored dictionary articles.

## Derived physical pages and provenance

Every physical page is represented in the source-verified inventory by PDF page number, source role, basis for range classification, provisional printed-page mapping, page dimensions, embedded image count, selectable text count, visual inspection flag and transcription status. A source-free CI build must report source_pdf_sha256_verified_in_this_run: false.

Two-column column flow, page-spanning articles, running page heads and author initials must not be inferred as article boundaries without image evidence. Preserve all Persian/English glyphs, punctuation and typography where recoverable. Keep normalization limited to derived retrieval fields.

Gould/Kolb and the unrelated Aryanpour LD2 dictionary are separate sources with separate conventions.
