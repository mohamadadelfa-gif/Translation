# Persian PDF OCR — recognition + source-preserving comparison

A **working** PDF → Persian OCR / Markdown / JSONL tool with two interchangeable OCR backends. Its purpose is faithful **transcription**, not language-model editing.

## Backends

- **Tesseract 5 LSTM** (tested): `fas` Persian language data (`fas+eng` for mixed-language books). Use official `tessdata_best` when available and speed allows. Model data must be installed locally. Runs on Windows, Linux, and macOS.
- **PaddleOCR PP-OCRv5 Arabic-script recognizer** (optional, **not tested in the build environment**): `lang="fa"` for Persian. The package and model weights are not included. It has separate Python dependencies and may download models on first use. Never silently fall back from PaddleOCR to Tesseract if setup fails.

No commercial AI APIs, remote image uploads, or cloud storage are required for the tested Tesseract path.

## Install

Python 3.9+ and Tesseract v5 with `fas` and ideally `eng` language files are required. On Windows, install the Tesseract executable and its Persian `fas.traineddata` and English `eng.traineddata`, then add the executable to `PATH`. `tesseract --list-langs` should show **fas** and **eng**. The `tessdata_best` family supports LSTM (`--oem 1`) and is generally slower than `tessdata_fast`; **benchmark on your pages**.

```powershell
python -m pip install -r requirements.txt
tesseract --list-langs
python persian_pdf_ocr.py "C:\books\my-scan.pdf" --out "C:\books\my-scan-ocr" --engine tesseract --mode compare --qa
```

For an **optional** PaddleOCR installation use the platform-appropriate PaddlePaddle instructions and `pip install paddleocr`. This tool calls the PaddleOCR v3 Python API with `ocr_version="PP-OCRv5"`, `lang="fa"`. Because this backend was not executed in our environment, verify its API and download policy after installation. First try a few pages.

## Modes

- `compare` **(default, thorough):** always run OCR, save **both** PDF-embedded text and OCR text. `selected_text` is OCR; PDF text layer is a separate reference. Similarity is a discrepancy signal, not correctness.
- `auto` **(faster):** prefer embedded PDF text if it passes simple screening; **does not detect many severe RTL text-layer inversions**. Use `compare` on important books.
- `ocr`: run OCR on every selected page, preserving embedded text alongside it.
- `text`: extract the PDF text layer without OCR (can contain reversed Persian words).

### Useful commands

```powershell
# First run on a few pages, with OCR vs embedded comparison
python persian_pdf_ocr.py "C:\books\book.pdf" --out ".\book-ocr-sample" --pages 10,11,14-16 --mode compare --dpi 300 --qa

# Full 300 DPI book; may be time-consuming on a CPU
python persian_pdf_ocr.py "C:\books\book.pdf" --out ".\book-ocr" --mode compare --engine tesseract --qa

# Pure Persian only (no English); choose layout mode when appropriate
python persian_pdf_ocr.py book.pdf --out output-fa --tess-langs fas --psm 3 --psm 6

# Explicitly a two-column Persian document (right column before left)
python persian_pdf_ocr.py book.pdf --out output-2col --columns 2 --mode ocr

# Optional PaddleOCR benchmark (when installed)
python persian_pdf_ocr.py book.pdf --out output-paddle --engine paddle --mode ocr --pages 1-3

# Unit tests without OCR model downloads
python -m unittest -v test_persian_pdf_ocr.py
```

**Column override warning:** `--columns 2` simply cuts each rendered page in half, processes the right half first, and stores the halves separately. It is only appropriate for known two-column Persian pages; full-width headings and figures may be split. Normal single-column mode leaves reading order to the OCR engine. No algorithm here guarantees correct RTL ordering for complex layouts.

## Output folder

```text
out/
  manifest.json                 input checksum, pages, processing settings
  document.md                   searchable page-separated transcription
  pages.jsonl                   selected + original text-layer + OCR text, flags, confidence
  qa-report.jsonl               optional candidate-only QA flags
  pages/
    p0001-selected.txt
    p0001-embedded.txt
    p0001-tesseract.txt          or p0001-paddle.txt
    p0001-geometry.json         word/line boxes and recognizer confidence
```

**Important:** OCR confidence is *not* transcription accuracy. Model-to-model agreement and OCR-to-embedded similarity are not ground truth. Preserve the original PDF, compare selected passages with page images, and use `benchmark_ocr.py` only when a full-page gold transcription has been visually verified.

### Scoring with gold pages

`benchmark_ocr.py` accepts a JSONL containing records shaped like:

```json
{"page": 5, "verified_text": "[complete visually checked text of PDF page 5]", "verification": "visual_full_page"}
```

The bracketed text here is a **placeholder**, not gold evidence. Benchmark input must have complete page text, not a fragment. Run:

```bash
python benchmark_ocr.py --gold verified-pages.jsonl --predicted output/pages.jsonl --output output/benchmark.json
```

Scores include character error rate (CER) and word error rate (WER); the scorer normalizes only Unicode NFC and whitespace **in memory for scoring** and never alters source or OCR output.

## Extraction limitations and the demonstrated page

A real test against the uploaded Yousef grammar book (2018), PDF page **151** / printed page **132**, was executed with `tesseract fas+eng`, 190 DPI, PSM 3, `--mode compare --qa`. The OCR output showed the correct *ordering* of one visually checked Persian example whose PDF text-layer extraction had inverted the word sequence. The sample run produced a mean Tesseract word confidence of **92.65** and 31 QA candidate flags. These figures are **not** accuracy or precision measurements; many QA flags may be false positives. The full-book OCR and PaddleOCR backend have **not** been benchmarked.

Potential problems: Nastaliq font recognition, degraded scans, handwriting, columns/tables, tight diacritics, formulas, footnotes, bilingual line-direction markers, split words, hyphens, and right-to-left reading order. No automatic correction or reconstruction is presented as authoritative. Review visually against PDF before use as evidence. The grammar book and source reference PDFs themselves are **not** committed to this public repository.

## Privacy and reproducibility

Files are processed locally. Outputs contain text copied from source documents: do not publish derived transcripts of copyrighted books or sensitive records. No OCR model weights are redistributed. `pages.jsonl` retains raw embedded/OCR alternatives. The original input PDF is opened read-only and never overwritten. Use a distinct output directory.

## Primary engine documentation

- Tesseract language support: https://tesseract-ocr.github.io/tessdoc/Data-Files.html
- Tesseract best models: https://github.com/tesseract-ocr/tessdata_best
- PaddleOCR Persian recognition (PP-OCRv5): https://www.paddleocr.ai/latest/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.html
- PaddleOCR v3 Python API: https://www.paddleocr.ai/v3.0.0/en/version3.x/pipeline_usage/OCR.html
