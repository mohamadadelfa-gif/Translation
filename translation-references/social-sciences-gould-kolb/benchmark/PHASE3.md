# Phase 3 — complete-article first-pass and image-based recheck

**Current state:** First-pass transcriptions and a same-assistant visual recheck, **not independent gold-standard approval**. This is a structurally validated benchmark workbench, not certified OCR ground truth.

The authority remains the originally supplied Persian scan of *فرهنگ علوم اجتماعی*, keyed by the SHA-256 in [source_manifest.json](../source_manifest.json). The editors' own [rules](../EDITORIAL_RULES.md) control its entry structure, section lettering, cross-references and author credits.

## Two complete-article candidates

The two following entries have **visibly bounded full articles** on single physical PDF pages, with the next heading visible below:

| PDF page | Persian headword | English headword | Expository structure | Credit |
|---|---|---|---|---|
| 54, left column | احضار روح | spirit mediumship | One unlettered definition + «نیز» references | R. W. Firth; Persian-language credit not confidently transcribed |
| 96, left column | افزایش طبیعی | natural increase | A and B, followed by «نیز» references | William L. Kolb; Persian credit `م. میرزایی` **first pass** |

See [complete_articles_first_pass.jsonl](complete_articles_first_pass.jsonl). The `article_text_completeness` field is `complete_article_candidate_first_visual_pass`: it means the print layout shows a self-contained article whose transcription has been attempted. It does **not** mean the Persian characters have been independently confirmed.

Both records preserve `related_marker_first_pass: نیز`. This is **different from** a stand-alone `see/←` referral. The original formatting may show an arrow near `نیز`; do not automatically turn the association into synonymy or a verified headword link. `related_target_ids_verified` is empty.

## Existing 11 first-pass records

The [original 11 records](first_pass_v1.jsonl) have each received another same-assistant image comparison, with individual observations recorded in [visual_recheck_log_v1.jsonl](visual_recheck_log_v1.jsonl). That includes the two separate `آداب` referrals, the source-hyphenated English `social patho- / logy`, Persian half-space issues, and the difference between a complete referral and an **A section only**.

**Do not replace the original 11 records automatically.** The recheck log records what needs confirmation and does not claim a distinct human reviewer, approval of disputed characters or an independently checked gold standard.

## Source-page evidence

- [complete_article_evidence.json](complete_article_evidence.json) gives source-pdf physical page numbers and re-renderable crop coordinates for the new article candidates.
- [visual_evidence_manifest.json](visual_evidence_manifest.json) locates the five earlier crops.
- The original PDF and its cropped page images are intentionally **not in this GitHub directory**; local renders can be produced from the hash-matched PDF.

Regenerate the two article crops and validate the first-pass records using:

```powershell
python -m pip install pymupdf
python translation-references/social-sciences-gould-kolb/tools/validate_phase3.py --pdf "C:\path\to\farhang-eolum-eejtemaii-g-k@bamun1.pdf" --evidence-dir "gould-kolb-phase3-evidence" --report "gould-kolb-phase3-report.json"
```

Without `--pdf`, the validator checks structured records, source locators, and status claims **without asserting original-PDF verification**. The repository CI operates in that source-free mode.

## Independent review procedure (required before gold-standard promotion)

1. Have a **separate reviewer** compare each source-image crop with its corresponding JSONL record. Review the article heading; every word, diacritic, punctuation mark, space and ZWNJ; A/B and unlettered structure; next visible heading; contributor signature; and `نیز` associations.
2. Keep original first-pass text unchanged. Record each discrepancy with original source image, exact correction span, proposed reading, confidence/reviewer and status. Uncertain glyphs must remain unresolved rather than completed by context.
3. Reconcile disagreements with the full surrounding PDF page, not just a cropped image.
4. Mark any reviewed entry as verified only with reviewer identity, page-image evidence, reviewed timestamp, and a **separate approved corrected source-transcription file**. The current files deliberately contain no such approvals.
5. Compare OCR/vision text against **only the approved transcriptions**. Evaluate character error rate, word error rate, reading order, article-boundary mistakes, lost sections, and misattributed contributor/related-reference information separately. A passing software test is not a linguistic accuracy score.

## Protected invariants

The [Phase 3 validator](../tools/validate_phase3.py) fails if:
- either new full-article candidate is relabeled independently verified;
- section A or B is fabricated or omitted from the two source-observed patterns;
- the related-entry marker is replaced with a verified cross-reference;
- any of the 11 old benchmark records lacks a recheck-log row or claims a distinct independent reviewer;
- a crop points to a different physical PDF page or the original source hash does not match;
- the Persian contributor credit of the first article is promoted without being legible.

**Automated status:** 11 recheck observations, 2 full-article candidates, 0 independently approved articles, 0 gold records. This is deliberate. Proceed to OCR benchmarking **after** independent review, not before.
