# Gould/Kolb OCR/vision evaluation — gated protocol

**Status:** The evaluation software exists, but **no real OCR accuracy scores have been computed**. All 13 reference records are provisional. The original Persian scanned PDF is not stored in GitHub.

This protocol follows [the Persian editors' rules](../EDITORIAL_RULES.md) and the [independent-review handoff](REVIEW_HANDOFF.md). It measures candidate **structured entry fields**, not unsegmented whole-page OCR. The distinct later tasks of **detecting entry boundaries**, **reconstructing two-column page reading order**, and **identifying full-page entries** still need separate benchmarks.

## Mandatory release gates

1. A **different reviewer** examines the *actual source PDF pages and crop images* and returns completed `independently-reviewed-responses.jsonl` for all 13 candidates. The existing [review gate](../tools/review_gate.py) rejects missing reviews, unresolved fields, dubious contributor names, stale first-pass digests, and unsupported self-attestations.
2. A **separate project editor** checks the submitted responses and source evidence, resolves disagreements, and creates a signed-off JSON file using [the unapproved template](editor_signoff.template.json). No prefilled approval is valid.
3. The editor's sign-off binds the **SHA-256 of the exact reviewer-responses JSONL bytes** (not the candidate OCR file). Its `editor_id` must differ from the reviewer's ID; it includes a timezone-aware signature timestamp and explicit Boolean attestations.
4. A model or OCR engine is **actually run** on the hash-matched source scans. The structured predictions include engine/version/provenance and `submission_status: actual_model_output`. A generated template is explicitly marked `unfilled_template` and is **rejected**.
5. Only then may [evaluate_ocr.py](../tools/evaluate_ocr.py) compute an accuracy report. It will refuse to score unapproved gold data or mismatched source/engine metadata.

**Honesty note:** These are strong structural, provenance and human-attestation gates. A program cannot authenticate a human editor or determine whether someone truly read the scan. Editorial oversight remains essential.

## Prediction JSONL format

Produce an empty template with the 13 expected record IDs, page locators and source SHA-256:

```powershell
python translation-references/social-sciences-gould-kolb/tools/make_ocr_template.py --output ocr-prediction-template.jsonl
```

Each JSONL record uses `gould-kolb.ocr-structured-prediction.v1`:

```json
{
  "schema": "gould-kolb.ocr-structured-prediction.v1",
  "submission_status": "unfilled_template",
  "record_id": "gk-gt-p022-shamanism",
  "source_pdf_sha256": "<injected frozen source digest>",
  "source_pdf_page": 22,
  "source_column": "right",
  "engine_id": null,
  "engine_version": null,
  "fields": {
    "headword_fa_readable": null,
    "headword_en_readable": null,
    "referral_marker": null,
    "referral_target_fa_readable": null
  }
}
```

These **nulls are blank input slots** and must not be filled from the first-pass corpus. Extract them independently from images using the named engine; then set `submission_status: actual_model_output`, `engine_id`, and `engine_version`.

For explanatory articles, `fields.sections` is an array of `{"label": "A", "text_first_pass": "..."}` etc., matching the discovered section order. For a one-paragraph unlettered article, the section label is JSON `null`. The output can omit a field when extraction fails; missing content will be penalized rather than silently ignored. Do not invent Persian equivalents.

## Editorial sign-off

Copy `benchmark/editor_signoff.template.json` to a new, private JSON file once independent reviews are complete.

Set `review_responses_sha256` to the lowercase SHA-256 of the actual JSONL file (e.g. Windows PowerShell `(Get-FileHash .\independently-reviewed-responses.jsonl -Algorithm SHA256).Hash.ToLower()`).

Set `editor_id`, `signed_at` (timezone-aware ISO 8601), and, **only when true**, the three Boolean attestation fields:

- `reviewed_all_independent_attestations`
- `confirmed_source_images_reviewed_by_separate_reviewer`
- `approved_for_ocr_benchmark`

The sign-off is not valid if the responses later change. Do not commit personal identifying information or confidential reviewer responses to a public repository without permission.

## Score verified OCR candidates (future step)

```powershell
python translation-references/social-sciences-gould-kolb/tools/evaluate_ocr.py --review-responses independently-reviewed-responses.jsonl --editor-signoff editor-signoff.json --predictions actual-ocr-output.jsonl --report ocr-report.json --per-record ocr-details.jsonl
```

The report includes:
- Strict **character error rate** (CER), on Unicode codepoints without Persian character normalisation.
- Strict **word error rate** (WER), splitting only at whitespace, preserving zero-width non-joiners inside tokens.
- **NFC-only CER** for a clearly labeled diagnostic comparison; the canonical text stays unchanged.
- Per-class metrics for headwords, references, article exposition, section labels and contributors.
- Missing entries/fields, unmatched section sequences, missing/extra sections, nonexistent English terms and reference-field mismatches.

**Limitations:** Structured-field scoring assumes someone or something has already segmented the source into entries. This is *not* a measurement of the full 980-page OCR pipeline's reading order, page coverage, article recall, typographic fidelity, or OCR-versus-vision comparative quality. Those need a separately verified page-level benchmark. With only 13 reference records, the corpus is suitable for engineering trials, **not a statistically representative quality guarantee**.

## Current implementation state

The repository CI tests mathematical edit distances and failure scenarios using **synthetic, explicitly fictional review and OCR fixtures**. These are software tests only; they are not genuine reviews and do not constitute an OCR model run.

**Current real-world status:** 13 independent reviews pending; editor sign-off pending; real OCR submissions not yet present; **no accuracy results**.
