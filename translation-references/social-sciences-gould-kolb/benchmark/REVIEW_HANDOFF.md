# Independent image-based review — Gould/Kolb benchmark

**Current status:** 13 records awaiting a genuinely separate reviewer. No source text is approved as a machine-learning gold standard. The first-pass transcriber and its follow-up image rechecks were the **same assistant**, so they are not independent.

This package applies the Persian editors' original [entry conventions](../EDITORIAL_RULES.md) to the [first 11 referral/section observations](first_pass_v1.jsonl) and [2 complete-article candidates](complete_articles_first_pass.jsonl). The source remains the original 980-page scanned PDF, whose SHA-256 is in [source_manifest.json](../source_manifest.json).

## What the reviewer checks

For each of the 13 records:

1. Open the relevant **full source-PDF page**, then the matching high-resolution image crop. The page number, physical column, crop filename, source SHA-256, and all first-pass fields are included in the generated queue.
2. Compare every Persian character, diacritic, space/ZWNJ and punctuation mark against the printed scan. Recheck the original-language headword separately. Do not replace source spellings with modern conventions.
3. Verify the **boundaries** of the entry, surrounding headings, original A/B lettering (where present), paragraph sequence, and any cross-column or cross-page continuations.
4. Keep **see/←** referrals distinct from **also/نیز** associated terms. Do not assign resolved source IDs or synonymy without independent entry evidence.
5. Check the author's English name and Persian contributor/translator credits against the article ending. For the first complete article, a Persian attribution currently remains **unresolved**.
6. Mark ambiguous details **unresolved** rather than silently completing them from context or another dictionary.

## Machine-generated review forms

After checking out the repository, run:

```bash
python translation-references/social-sciences-gould-kolb/tools/review_gate.py \
  --queue gould-kolb-review-queue.jsonl \
  --response-template gould-kolb-review-responses.jsonl
```

The first file contains the source's first-pass text, the crop locator and a SHA-256 digest **of each first-pass record**. The second is a writable **empty review template**. Every status starts `pending`; no reviewer identity or approval is prefilled. GitHub Actions also uploads these two files as artifacts, but cannot check the original PDF because it is not stored on GitHub.

Send both JSONL files and the [Phase 3 crop images](complete_article_evidence.json) to a **different person** to review. If a reviewer cannot open the original page or cannot confidently read a glyph, the response must remain `unresolved`.

## How a reviewer submits a decision

For each JSONL response row, fill:

- `reviewer_id`: identifiable label for the reviewer, distinct from the original assistant/transcriber;
- `reviewed_at`: timestamp with timezone, e.g. `2026-10-10T21:00:00+03:30`;
- `reviewed_original_page_and_crop: true`: only after actually viewing both;
- `not_original_transcriber_attested: true`: only when this is genuinely a separate reviewer;
- `decision`: `approved`, `needs_changes`, or `unresolved` (pending otherwise);
- all seven `image_checks`: set to true **only after checking that aspect**;
- `approved_transcription`: complete source-text fields supplied by the reviewer when approved (the reviewer must explicitly provide every field, not merely click approve);
- `correction_notes`: cite disagreements or explain any source-preserving edits;
- `unresolved_details`: list remaining uncertain glyphs, print layout or attributions.

**Approval blockers:** unreviewed source PDF; missing/unclear Persian contributor; missing or rearranged A/B section markers; unsupported null text; unresolved ambiguities; mixed source-PDF revisions; or an unknown/stale first-pass SHA-256.

## Validate, then promote (only after real independent review)

```bash
python translation-references/social-sciences-gould-kolb/tools/review_gate.py \
  --queue gould-kolb-review-queue.jsonl \
  --response-template gould-kolb-review-template.jsonl \
  --responses independently-reviewed-responses.jsonl
```

This reports `pending`, `approved`, `needs_changes`, and `unresolved`, but **does not create a gold-standard corpus**.

Only after **all 13 records** pass their independent image checks can you explicitly run:

```bash
python translation-references/social-sciences-gould-kolb/tools/review_gate.py \
  --queue gould-kolb-review-queue.jsonl \
  --response-template gould-kolb-review-template.jsonl \
  --responses independently-reviewed-responses.jsonl \
  --promote gould-kolb-gold-v1.jsonl
```

If even one record remains pending, ambiguous, unreviewed, or stale, gold promotion **fails closed**. Synthetic regression-test fixtures are never legitimate independent review evidence.

**Technical limit:** Software can check that the attestation, evidence reference, fields and checks are present. It cannot independently establish the reviewer's identity or visually prove their answers accurate. A project editor must still inspect the submitted review and sign off on the corpus before citing any OCR accuracy results.

**Next task:** obtain this independent sign-off; then run *candidate* OCR/vision text against the approved corpus and report character/word errors, lost A/B sections, column order, references and contributor attribution separately.
