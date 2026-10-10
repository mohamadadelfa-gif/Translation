# Real OCR candidate pilot — Gould/Kolb Persian social-sciences dictionary

**Status: real OCR executed; outputs unverified; no OCR accuracy established.** Unlike the earlier synthetic software tests, this pilot actually invoked Tesseract on the original user-supplied PDF.

## Original source and reproducibility

- Original scanned dictionary: `farhang-eolum-eejtemaii-g-k@bamun1.pdf` (980 PDF pages, 20,753,450 bytes).
- Source SHA-256: `73b4e10a6d3d259aebbc2ebf30031e5a85f5abbede2552af94c9a7743f2c42de`. The physical source was **hash-verified in the local run**.
- [REGIONS.json](REGIONS.json) fixes 7 crop locations on six physical pages (22, 23, 32, 36, 54, 96).
- [LOCAL_RUN_SUMMARY.json](LOCAL_RUN_SUMMARY.json) records the actual 14 local Tesseract runs and word-box diagnostics, without uploading unverified source text publicly.
- [run_raw_ocr_pilot.py](../tools/run_raw_ocr_pilot.py) regenerates source crops, runs `tesseract -l fas+eng` in `--psm 4` and `--psm 6`, and writes raw candidate JSONL, a run report, and a source-image/outputs side-by-side HTML page.
- [test_raw_ocr_pilot.py](../tools/test_raw_ocr_pilot.py) verifies crop metadata and that an unrelated PDF fails **before** attempting OCR.

The user's conversation-local **Gould_Kolb_Raw_OCR_Pilot.zip** holds the seven source PNG crops, 14 actual raw Tesseract outputs and an openable HTML comparison page. The original full PDF is not in the repository or archive. **Raw OCR has not been integrated into the canonical dictionary or its index.**

## Run on a local checkout

Requires Python 3.10+, `pymupdf`, executable `tesseract`, and Tesseract `fas` and `eng` traineddata. Keep the original PDF separately from the public repository.

```powershell
python -m pip install pymupdf
python translation-references/social-sciences-gould-kolb/tools/run_raw_ocr_pilot.py --pdf "C:\path\to\farhang-eolum-eejtemaii-g-k@bamun1.pdf" --output "gould-kolb-ocr-local"
```

Then open `gould-kolb-ocr-local/review_side_by_side.html` in a browser. Inspect each source crop alongside both raw OCR runs. Source-page coordinates are measured in original PDF points and rendered at 3× scale.

**Never fill the existing structured prediction template by copying the old first-pass transcription.** If you later extract individual fields from these actual raw model results, attach the raw candidate ID, region, engine, run PSM and exact source page. Do not infer article boundaries from a crop enclosing neighboring headings.

## What is observed (not a measured OCR error rate)

The output is demonstrably imperfect: Persian text is mixed with invented or garbled Latin fragments when the source spans languages. For example the `p054_spirit_mediumship` region loses parts of the quoted Persian phrase and retains the next article's heading; `p096_natural_increase` misrecognizes part of the Persian heading and the A/B labels. The two PSM choices also yield visibly different text for the same scanned region.

The engine's TSV word confidence is a **self-reported recognition diagnostic**, not precision, recall, CER, or WER. The mean can be misleading on bidirectional text and cannot determine which output is semantically correct.

| Evaluation dimension | Status |
|---|---|
| Original PDF hash checked | Complete for local run |
| Actual OCR runs | 14 across 7 crops |
| OCR/vision systems compared | Only Tesseract here; PSM 4 versus PSM 6 |
| Editorial section recovery verified | No |
| Entry-boundary and multi-column reading-order quality measured | No |
| Gold-standard human review | **0/13 complete** |
| Credible CER/WER | **Not available** |

## Next process: targeted correction and controlled evaluation

1. Send the existing [independent-review handoff](../benchmark/REVIEW_HANDOFF.md) and its visual source pack to a *different reviewer*. Source text and typography must be checked from the original scan.
2. Have a separate editor inspect the completed reviews and sign off on their exact bytes. The [OCR evaluation protocol](../benchmark/OCR_EVALUATION.md) rejects missing review approvals.
3. With an approved corpus, write an **explicitly documented segmentation adapter** from raw OCR crop text to structured fields (or run a structured extraction system independently), preserving hallucinated/missing text and article boundaries.
4. Evaluate strict Unicode CER/WER and heading/section/reference structural mistakes on the independently approved entries. **Do not score these raw whole-crop strings against source subparagraphs**—they cover different spans.
5. Expand the gold set to varied multi-column, multi-page entries before any full-book batch extraction.

**Provenance policy:** PDF images are authoritative; Tesseract output is a machine-generated hypothesis; first-pass assistant transcription is also provisional. None of these by themselves constitute independently reviewed ground truth.
