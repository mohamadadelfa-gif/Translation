# Source Conversion Information

## Source
- Title: دستور خطّ فارسی (ویراست جدید)
- Publisher/author body: فرهنگستان زبان و ادب فارسی (نشر آثار، تهران ١۴٠١)
- Language: Persian
- Source format: PDF (89 pages, A5, text layer present, Acrobat Distiller 11.0)
- Conversion type: faithful PDF-to-Markdown transcription (text-layer extraction with geometric reconstruction; no OCR engine was needed)

## Editorial policy
- Source wording preserved. No translation, rewriting, modernization or normalization of terminology.
- Only extraction artefacts were repaired: presentation-form glyphs mapped to base letters (NFKC), RTL/bidi order rebuilt, diacritics re-attached to their letters, duplicated shadda marks removed, missing/hidden spaces and half-spaces (ZWNJ) restored from glyph geometry.
- Arabic letters ي/ك and Persian ی/ک were NOT globally unified; characters are kept as encoded in the PDF text layer.
- Digits are kept as encoded in the PDF (a mixture of Arabic-Indic ٠١٢٣٨٩ and Persian ۴۵۶٧ code points that render alike). Do not normalise them if you need exact source matching.
- Page boundaries preserved with `<!-- pdf-page: N | printed-page: M -->` comments. Printed numbers are the book's own numerals; front-matter pages 1–4 are unnumbered.
- Footnotes preserved as Markdown footnotes with unique IDs `[^p<pdf-page>-<n>]`; every definition starts with `[یادداشت n در متن اصلی]`.
- Tables reconstructed as Markdown tables (`<!-- table-start -->` / `<!-- table-end -->`). Repeated table headers on continuation pages are kept as printed.
- Running header «دستور خطّ فارسی» and printed page numbers were removed from body text (page numbers live in the page markers).
- Manually transcribed against the page image: colophon (PDF p. 4) and the table of contents (PDF pp. 5–6) because the text layer lacks spaces/half-spaces there.

See `CONVERSION-REPORT.md` for the full page-by-page accounting (chapters, footnotes, tables detected, and every page flagged for manual verification).

## File structure
- `00-front-matter.md` — (front matter, pp. 1–6)
- `01-introduction.md` — مقدّمه
- `02-preface-fourth-printing.md` — مقدّمۀ چاپ چهارم از ویراست نخست
- `03-preface-new-edition.md` — مقدّمۀ ویراست جدید
- `04-general-rules.md` — قواعد کلّی
- `05-features-of-persian-script.md` — ویژگی‌های خطّ فارسی
- `06-spelling-of-words-prefixes-suffixes.md` — املای بعضی از واژه‌ها و پیشوندها و پسوندها
- `07-copula-forms.md` — مجموعۀ ام، ای، است، ایم، اید، اند
- `08-possessive-and-object-pronouns.md` — ضمایر ملکی و مفعولی
- `09-indefinite-masdar-and-nisba-ye.md` — یای نکره و مصدری و نسبت
- `10-ezafe-kasra.md` — کسرۀ اضافه
- `11-hamza.md` — نشانۀ همزه
- `12-arabic-derived-words.md` — واژه‌ها و ترکیب‌ها و عبارت‌های برگرفته از عربی
- `13-tanvin-tashdid-harakat.md` — تنوین، تشدید، حرکت‌گذاری، هجای میانی و پایانی «ـ وو ـ»
- `14-compounds.md` — ترکیب‌ها
- `15-compound-prepositions-conjunctions.md` — فاصله‌گذاری در حروف اضافۀ مرکّب و حروف ربط مرکّب
- `16-multi-spelling-words.md` — واژه‌های چنداملایی
- `17-index.md` — نمایه
- `CONVERSION-REPORT.md` — full conversion report

## Known limitations
- Multi-line/merged cells in tables are approximated; see the Conversion Report list of pages needing manual verification.
- Book structure: the PDF has no chapters or endnotes; its top-level units are the sections listed in the printed table of contents.
