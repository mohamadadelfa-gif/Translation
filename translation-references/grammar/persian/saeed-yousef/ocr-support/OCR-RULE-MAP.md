# OCR grammar rule map (verified navigation, not verified rules)

The references below were checked against the book's table of contents. Printed-page values are navigation locators, **not evidence** that the book endorses a particular regex or Unicode code-point operation. PDF pages for main text are +19.

| Category | Yousef 2018 sections | Printed pages | Appropriate use / limit |
|---|---|---|---|
| U002/U005 glyph forms | Ch.2 §§2.2.2–2.2.4 | 10, 15 | Alphabet and letter forms; Unicode normalization is an engineering proposal |
| U003 bidi/control | Ch.2 §2.2 | 10–24 | Direction and joining background; actual line order requires page-image inspection |
| W001 mi/nemi gap | Ch.11 §11.1; Ch.12 §§12.2, 12.5 | 174, 224, 233 | Verb structure; use Academy orthography for ZWNJ standards |
| W002 plural ha gap | Ch.3 §3.3.1 | 26 | Plural morphology; potential false positives |
| W004 ZWNJ anomaly | Ch.2 §2.2; Ch.14 §14.1 | 10–24, 323 | Word boundaries and writing; not automatically a verified source error |
| Future morphology | Ch.3 §3.2; Ch.10 §§10.1–10.2; Ch.11 §11.5 | 25, 158–173, 178–179 | Compounds and affixes; not implemented |
| Future clause check | Ch.13 §§13.1, 13.7, 13.13, 13.17 | 265, 289, 302, 312 | Syntax and relative/reported clauses; not implemented |
| Future punctuation | Ch.14 §§14.1–14.5 | 323–326 | Punctuation reconstruction; not implemented |
| O001 reversal case | Ch.9 §9.1 | 132 (PDF 151) | Visually confirmed PDF text-layer mismatch; do not auto-reverse |

Use this map to **find** relevant grammar sections, then actually read their PDF pages before attributing a substantive explanation. A PDF text-layer order failure is not evidence of a grammar violation or an OCR-engine recognition error.
