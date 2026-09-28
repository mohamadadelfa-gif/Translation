# Ashouri — Structured Reference Extraction

Designed for the existing repository path:

```text
translation-references/ashouri/
```

## Current completed structural unit

`dictionary/E.md` covers the complete **E** section: PDF pages 135–161 (printed pages 134–160). PDF page 162 visibly begins **F**.

## Translation workflow role

```text
source passage
  → Ashouri lookup
  → compare with other references
  → contextual analysis
  → translation-references/GLOSSARY.md decision
  → draft / review
```

Ashouri supplies reference evidence; `GLOSSARY.md` remains the project decision layer.

## Accuracy model

- English entry boundaries: source typography + scan OCR.
- Cross-references: preserved from scan when detected.
- Persian equivalents: column-aware Persian OCR.
- Exact final terminology: check the scan when an entry appears in `qc/E-uncertain-readings.md`.
