# Gould/Kolb — first-pass visual transcription benchmark

**Status:** first visual transcription pass; NOT a final, independently reviewed gold standard and NOT a complete dictionary.

**Authority:** the original user-supplied 980-page scanned Persian edition of *فرهنگ علوم اجتماعی*. The exact source SHA-256 is pinned in [source_manifest.json](../source_manifest.json). Source interpretations follow the [Persian editors' published entry rules](../EDITORIAL_RULES.md). The original scan and its cropped evidence images are **not committed to GitHub**.

## Material transcribed

| Physical PDF page | Column | Sample | Verified scope |
|---|---|---|---|
| 22 | right | آیین شمنی → شمن | complete printed referral |
| 22 | right | آیین نجسی-پاکی (*ritual pollution*) | complete A paragraph **only**, article still incomplete |
| 23 | left | آداب (*mores*) → شیوه‌های عامیانه | complete printed referral |
| 23 | left | آداب (*rite*) → مراسم و آیین | complete printed referral |
| 23 | left | آداب گذر (*rites de passage*) | complete A paragraph **only**, article still incomplete |
| 32 | left | آسیب‌شناسی اجتماعی → بی‌سازمانی اجتماعی | complete printed referral |
| 32 | left | آسیب‌شناسی روانی → روان‌آسیب‌شناسی | complete printed referral; no English label printed |
| 36 | right | آمار اقتصادی → اقتصاد ریاضی | complete printed referral |
| 36 | right | آموزش و پرورش → تعلیم و تربیت | complete printed referral |
| 36 | left | انبوه خلق → جماعت | complete printed referral |
| 36 | left | آنترپرنور → کارفرما | complete printed referral |

**Total: 11 records**, comprising **9 complete referral entries + 2 A-section excerpts** from four physical PDF pages.

Some printed English terms wrap with hyphenation between lines (e.g. *social patho-* / *logy*). The digital `headword_en_readable` is a reconstructed search representation, not a claimed facsimile transcription of physical line breaks. Persian spelling, intra-word half-spaces and diacritics still need an **independent second visual pass**. The 11 records were not automatically OCR-extracted.

## Why this matters

The editors distinguish a **see/← referral** from a **also/نیز related entry**. These records preserve the former without asserting synonymy, resolving targets, or treating referrals as full explanatory articles. The two different English headwords paired with **آداب** remain **two records**, not a merged dictionary sense.

The A excerpts demonstrate the main dictionary's section convention but are **partial articles**. B/C/D sections, contributor attributions and page continuations have not been fully transcribed. There are **zero verified complete explanatory articles** in this first tranche. That limit is enforced by automated tests.

## Files and provenance

- [first_pass_v1.jsonl](first_pass_v1.jsonl): readable Persian transcriptions and literal referrals, typed by completeness and accompanied by source column/page, crop locator and explicit review status.
- [visual_evidence_manifest.json](visual_evidence_manifest.json): five exact crop rectangles in PDF points. Generated evidence images are intentionally not committed.
- [validate_benchmark.py](../tools/validate_benchmark.py): validates shapes and statuses; with the actual source PDF provided, checks its bytes against SHA-256 and regenerates crops; without it, **does not claim to have inspected original pages**.
- [test_validate_benchmark.py](../tools/test_validate_benchmark.py): source and semantic guardrails.
- [GitHub workflow](https://github.com/mohamadadelfa-gif/Translation/actions/workflows/gould-kolb-pilot.yml): runs both existing structural-pilot and benchmark validations.

## Reproduce source images and check records

From a checkout of the Translation repository, with the original PDF stored separately:

```powershell
python -m pip install pymupdf
python translation-references/social-sciences-gould-kolb/tools/validate_benchmark.py --pdf "C:\path\to\farhang-eolum-eejtemaii-g-k@bamun1.pdf" --evidence-dir "gould-kolb-benchmark-evidence" --report "gould-kolb-benchmark-report.json"
```

This verifies the source PDF and re-renders the original evidence regions; **it does not automatically determine the accuracy of the Persian transcription**. Accuracy needs manual, image-versus-text comparison. Use the individual section or referral record's `evidence_crop` to locate its page excerpt.

## Promotion requirements (not completed)

1. Have a **second, independent image-based review** of the Persian text, punctuation, semispaces and proper names; log all corrections separately.
2. Choose **two genuinely short complete explanatory articles** and establish their exact start/end boundaries. Do not confuse an A subsection or a referral with a complete article.
3. Verify section A–E boundaries, column order, contributor/translator credits and cross-page continuations.
4. Only then use those corrected records as ground truth to measure candidate OCR, character errors, column-merging errors and lost sections.
5. Promote source-backed records into the main lookup architecture, preserving their editorial kind and original source page; do not silently rewrite the source or borrow Aryanpour's structural conventions.

The benchmark currently represents a **safe transcription starting point**, not OCR accuracy evidence.
