# Ashouri — Complete A–Z Structured Reference Extraction

Target repository path:

```text
translation-references/ashouri/
```

The original PDF should remain separately under `sources/`.

## Status

- Structural extraction: **complete for A–Z**
- Dictionary body: PDF pp. **4–505**
- Structured headword records: **26,333**
- Page provenance: retained
- Per-letter Markdown: generated
- Per-letter machine-readable indexes: generated
- Master A–Z index: generated
- OCR/QC queues: retained

This completes the **structural extraction stage**. It does **not** mean every Persian OCR reading has been manually certified.

## Main files

```text
dictionary/A.md ... dictionary/Z.md
index/headwords-master.csv
index/headwords-master.jsonl
index/letter-summary.csv
qc/AZ-cross-letter-audit.md
```

## Translation-project role

```text
source passage
  → Ashouri lookup
  → compare with Aryanpour / project references
  → contextual analysis
  → GLOSSARY.md translation decision
  → draft / review
```

Ashouri remains a **reference/evidence layer**. `translation-references/GLOSSARY.md` remains the project decision layer.
