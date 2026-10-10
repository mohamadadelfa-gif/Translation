# Review and evaluation contract

Use this contract for **document OCR and dictionary OCR**. It complements the existing non-destructive Persian [QA review policy](../../translation-references/grammar/persian/saeed-yousef/ocr-support/REVIEW-POLICY.md).

## Immutable layers

`source_image` → `embedded_raw` → `engine_raw_A/B/C` → `layout_candidates` → `lexical_and_NLP_suggestions` → `human_reviewed` → `faithful_export`.

The arrows mean evidence flow, **not permission to overwrite an earlier layer**. Keep independent SHA-256 and page/crop locators.

## Minimum review record

~~~json
{
  "document_id": "local-document-id",
  "page_id": "57",
  "region_id": "entry-left-001",
  "bbox": [0, 0, 0, 0],
  "category": "headword_or_ipa_or_persian_or_layout",
  "raw_readings": [],
  "suggested_reading": null,
  "source_image_reference": "private-path-or-region-id",
  "verification_status": "candidate",
  "reviewer": null,
  "reviewed_at": null,
  "reason": null
}
~~~

The rectangle is a placeholder, not a recognized bounding box.

## Distinguish four types of errors

| Type | Example | Verification |
|---|---|---|
| Recognition | `rchaeological` vs printed `archaeological` | Check exact glyphs on crop |
| Layout/reading order | 2 columns interleaved | Inspect page geometry and order |
| Entry association | Correct Persian meaning attached to wrong headword | Check entry boundary and alignment |
| Editorial or normalized variant | Modernized half-space, stripped diacritic | Keep *separate*; source transcription unaffected |

## Benchmark measurement

Gold = page-image-verified transcription + manually checked layout/entry boundaries. OCR engine confidence, an LLM's plausibility judgment, and existing unverified dictionary OCR records **cannot** be the gold.

Report raw exact-codepoint CER and WER plus a clearly specified *secondary* normalized score (if needed). Track IPA separately, including stress symbols; preserve diacritics and spelling differences in source-faithful scores. Do not compare metrics from inconsistent normalization or different region sets. Document whether Unicode segmentation is at codepoint or grapheme level.

The initial 57–59 page exercise tested navigation and headword presence only; it is not proof of accurate Persian sense extraction or correct entry alignment.

## Release and privacy gate

Review license and publication rights for source scans, commercial dictionaries, model weights, third-party lists, generated reports with excerpts, and gold transcriptions. Store sensitive or copyrighted evaluation assets privately; public GitHub contains only code, original documentation, tiny illustrative fragments where justified and noncopyrighted aggregate metrics. Keep model and data SHA-256 + version + license decision in a private manifest.
