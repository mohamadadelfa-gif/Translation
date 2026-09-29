# Conversion Report

- PDF pages processed: 89 (all)
- Printed page range: ۵ – ٨٨ (front matter pp. 1–4 and the last leaf, p. 89, are unnumbered in print)
- Markdown files created: 17 section files + `00-front-matter.md` + `README.md` (18 content files total)
- Chapters/sections detected: 17 (matching the printed table of contents exactly — مقدّمه; مقدّمۀ چاپ چهارم از ویراست نخست; مقدّمۀ ویراست جدید; قواعد کلّی; ویژگی‌های خطّ فارسی; املای بعضی از واژه‌ها و پیشوندها و پسوندها; مجموعۀ ام، ای، است، ایم، اید، اند؛ ضمایر ملکی و مفعولی؛ یای نکره و مصدری و نسبت؛ کسرۀ اضافه؛ نشانۀ همزه؛ واژه‌ها و ترکیب‌ها و عبارت‌های برگرفته از عربی؛ تنوین، تشدید، حرکت‌گذاری...؛ ترکیب‌ها؛ فاصله‌گذاری در حروف اضافۀ مرکّب...؛ واژه‌های چنداملایی؛ نمایه)
- Footnotes detected: 58 (all as printed footnotes at the foot of their page; the book has no separate endnotes section)
- Tables detected: 28 (ruling-line grid tables: pp. 29–33, 42–46, 52–53; two-column word-list/index tables reconstructed from visual column gaps: pp. 73–88)
- Figures/images detected: 1 (decorative "بسم الله الرحمن الرحیم" calligraphic graphic, PDF p. 7, marked `[تصویر: ...]`; it carries no printed caption)
- Pages requiring manual verification: 31 — see the list below
- Uncertain OCR passages: none. The PDF's embedded text layer was intact and correctly encoded (IRLotus/BNazanin fonts with standard Arabic-Presentation-Form glyphs and a normal Unicode cmap), so no image-based OCR pass was needed anywhere in the book. All repairs were geometric reconstruction (bidi/RTL reordering, presentation-form → base-letter normalization, diacritic re-attachment, hidden-space/ZWNJ inference from glyph spacing) rather than character guessing, and every page's output was checked against an independent re-extraction of the PDF's raw text (character-multiset audit) plus a visual comparison for the pages listed below. No `[ناخوانا]` or `[خوانش نیازمند بررسی]` markers were needed anywhere in the book.
- Missing/damaged pages: none. Page 2 is blank in the source PDF (marked `<!-- blank page -->`); page 89 is a blank final leaf (also marked).
- Other structural anomalies:
  - The colophon (PDF p. 4) has a severely disordered text layer (running the copyright/CIP block and the library cataloguing (فهرست‌نویسی) table together); it was transcribed by direct visual reading of the page image rather than by repairing the extracted order. The CIP table's right-hand column (the actual catalogue values) is not typeset as text in the PDF at all — only the field labels (سرشناسه، عنوان و نام پدیدآور، …) are printed, so no values could be transcribed.
  - The table of contents (PDF pp. 5–6) is missing a number of spaces and half-spaces (ZWNJ) in its text layer; it was reconstructed by comparison with the page image.
  - Two ruling-line tables (pp. 29–32) print each Arabic letter twice per cell — once in a modern Persian computer font, once in an older "IRLotus" style specifically to show the letter's true joining shape — because the two are visually distinguishable but re-encode to the same Unicode codepoint in the PDF's text layer, the traditional-style duplicate could not be reliably told apart from the modern one automatically; only the first (unambiguous) glyph of each cell was kept in text form, and the file is flagged for a manual check against the page image.
  - One page (PDF p. 43, `07-copula-forms.md`) has genuinely two lines of text stacked inside several cells of one column (e.g. "خشنودم" / "خشنودیم"); these were preserved with an inline `<br>` rather than merged into one line.

## Pages flagged for manual verification

| File | PDF page(s) | Reason |
|---|---|---|
| 00-front-matter.md | 4 | Colophon: transcribed by visual reading; CIP table has no printed values, only field labels |
| 00-front-matter.md | 5–6 | Table of contents: text layer lacks some spaces/half-spaces; repaired by comparison with the page image |
| 05-features-of-persian-script.md | 29–33 | Table 1/Table 2 (letter-shape grid): reconstructed from the ruling-line grid; the traditional-vs-modern duplicate glyph in each cell (pp. 29–32) was collapsed to one form — check against the image if the distinction matters |
| 07-copula-forms.md | 42–43 | Grid table with some two-line cells (rendered with `<br>`) |
| 08-possessive-and-object-pronouns.md | 44–45 | Grid table reconstructed from ruling lines |
| 09-indefinite-masdar-and-nisba-ye.md | 46 | Grid table reconstructed from ruling lines |
| 11-hamza.md | 52–53 | Grid table (Table 3) reconstructed from ruling lines |
| 16-multi-spelling-words.md | 73–85 | Two-column preferred-spelling word list; columns split by the visual gap between them, including a few multi-line explanatory remarks placed by position rather than by any printed table structure |
| 17-index.md | 86–88 | Two-column index (نمایه); columns split by the visual gap; page-number strings for each entry preserved exactly as printed, including ranges joined with "-" |

## Independent fidelity check performed

Every page's Markdown text was compared against an independent re-extraction of the same PDF page (`pdftotext`), by Persian-letter multiset (ignoring digits, punctuation, spacing and diacritics, so the comparison is immune to this project's own bidi/segmentation choices). Across the 86 non-blank, non-cover pages, the reconstructed text differs from the raw extraction only in these deliberate, policy-driven ways:
- the removed running header «دستور خطّ فارسی» (present at the top of nearly every body page, correctly stripped as page furniture per the task's header/footer policy), and
- page 4, transcribed manually for the reasons above.

No page showed an unexplained discrepancy. A further visual sample (beginning, middle, end, footnote-bearing pages, a quotation/poetry page, and several table pages) was checked directly against the rendered page images.
