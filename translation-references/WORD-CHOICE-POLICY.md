# Word choice for the English–Persian translation

User instruction: use the supplied Ariyanpour dictionary as one of the preferred references for word choice, alongside other relevant dictionaries, specialist sources, and the Persian thesaurus.

## One of the preferred references

- Treat `aryanpour/aryanpour-english-persian.jsonl` as the canonical machine-readable source and `aryanpour/aryanpour-english-persian.txt` as the full readable export.
- For routine interactive lookup, use the derived retrieval layer in `aryanpour/index/` and `aryanpour/dictionary/`; do not search the large canonical JSONL as the normal lookup path.
- These files contain 50,259 entries extracted from the user's LD2 dictionary. Ariyanpour attribution was supplied by the user; the edition is not independently verified.
- The Babylon BDC comparison remains deferred at the user's request.

### Required Ariyanpour lookup protocol

For every consequential or uncertain English headword that requires an Ariyanpour check:

1. Open the matching letter index, for example `aryanpour/index/C-headwords.csv`.
2. Find the exact `headword` or exact normalized-headword match.
3. Follow the recorded `file` and `anchor` into the relevant Markdown shard under `aryanpour/dictionary/`.
4. Inspect the complete entry before attributing any Persian equivalent to Ariyanpour.
5. Record the lookup as: `Ariyanpour — <headword> — Entry ID <id> — <file>#<anchor> — finding — effect on translation`.
6. If no exact headword is present, record `exact headword not found`. A related lemma, inflected form, or neighboring entry may then be checked separately, but it must not be represented as the exact requested entry.
7. If the index or shard cannot be retrieved, record the Ariyanpour check as incomplete. If the retrieved entry does not resolve the translation question, record it as inconclusive.
8. Never infer Ariyanpour support from the master index alone. The actual shard entry must be inspected.

The canonical JSONL remains the source of record; the index and Markdown shards are a derived retrieval layer for reliable lookup and citation-like locators.

### Required Hezareh lookup protocol

For every consequential or uncertain English headword that requires a Hezareh check:

1. Open the matching letter index under `hezareh/index/`.
2. Search for an exact `normalized_headword`; if none exists, check an exact `base_normalized_headword`.
3. Follow the recorded `file` and `anchor` into the relevant Markdown shard under `hezareh/dictionary/`.
4. Inspect the complete record, including `verification_status`, `boundary_confidence`, PDF page, source pointer, and `Source text`.
5. Record a usable lookup as: `Hezareh — <headword> — <record_id> — PDF p. <page> — <verification_status>/<boundary_confidence> — <file>#<anchor> — finding — effect on translation`.
6. Treat `visually_checked` as a status inherited from the supplied package; do not imply that the current mentor independently rechecked the original page.
7. Treat `raw_ocr` as qualified evidence. Preserve OCR uncertainty and verify consequential wording against the corresponding source page when available.
8. Treat `hint_only` as navigation only, not lexical evidence. If no reconstructed entry text is available, report `exact entry unavailable / hint_only — verification needed`.
9. Preserve multiple records for the same normalized headword. Do not silently collapse or clean them into a single dictionary entry.
10. Never infer Hezareh support from an index row alone. The actual Markdown record and its source text must be inspected.

The canonical Hezareh extraction package remains under `../sources/Hezareh_Dictionary_Index/`. The `hezareh/` directory is a derived model-retrieval layer, not a replacement for the source package.

### Required Persian thesaurus retrieval protocol

The Persian thesaurus is a semantic-field reference, not an English–Persian dictionary. Use it only after the English meaning and initial Persian candidates have been established.

1. Use the derived retrieval layer under `persian-thesaurus/` for routine lookup.
2. If the candidate is a numbered semantic-field heading or a source-bold lead term, use `persian-thesaurus/index/entries-master.csv` or `persian-thesaurus/index/lead-terms.csv`.
3. For any other Persian candidate term or phrase, use `persian-thesaurus/index/TERM-SHARD-MAP.csv` to locate the relevant reverse-occurrence shard under `persian-thesaurus/index/terms/`.
4. Follow the resulting `file` and `anchor` into the complete semantic entry under `persian-thesaurus/entries/`.
5. Inspect the whole entry before drawing a semantic conclusion. A term's occurrence in an entry means only that it occurs in that semantic field; it does not establish synonymy, equivalence, broader/narrower relation, or recommendation.
6. When useful, inspect `persian-thesaurus/index/explicit-cross-references.csv`, which records only explicit source `⍃` cross-references.
7. Record the lookup as: `Persian thesaurus — entry <id> «<heading>» — <file>#<anchor> — finding — effect on translation`.
8. The canonical source is `../sources/فرهنگ طیفی - تزاروس فارسی.docx`. The supplied Markdown is an audit/search aid. If a structural or wording ambiguity matters, resolve it against the DOCX rather than inferring from Markdown heading syntax.
9. Never say that the thesaurus “recommends” a translation merely because a word appears in the same semantic field.

The derived thesaurus layer contains all 991 numbered semantic entries. Its build audit records three known Markdown structural misclassifications; the retrieval layer is generated from the canonical DOCX structure rather than those Markdown headings.

## Selection rules

Consult [SOURCE-REGISTER.md](SOURCE-REGISTER.md) for the uploaded reference collection, including Hezareh, Ashouri, Najafi, the Academy orthography guide, the Persian thesaurus, and the prose sample.

Adel confirmed this reference set on 2026-09-27. Use the source book for meaning and context; Hezareh and Ariyanpour for general bilingual vocabulary; Ashouri for humanities terminology; the Persian thesaurus for alternative expressions; Najafi for usage questions; and the Academy guide for orthography. Use the supplied novel for prose study without importing its narrative voice wholesale. No dictionary has automatic priority: contextual accuracy and the author's argument govern the final proposal, with Adel retaining the final choice.

1. For significant or uncertain English vocabulary, compare relevant senses in Ariyanpour and Hezareh as active peers. Complete the source-specific indexed lookup protocol above before claiming support from either dictionary. Record exact-entry misses, hint-only results, unavailable lookups, or inconclusive lookups instead of implying that both sources were checked successfully. For Hezareh, preserve the supplied verification status and boundary confidence and verify consequential raw OCR against an original page when available.
2. Select the Persian sense appropriate to the sentence, the author's argument, and the historical or philosophical context. Do not automatically take the first equivalent.
3. Treat Ariyanpour as one of the preferred vocabulary references, without automatic priority over other relevant sources. Weigh alternatives by contextual accuracy, clarity, specialist usage, idiomatic Persian, and the agreed scholarly tone. Do not use any dictionary as a mandatory word-for-word substitution list.
4. For technical terms where the dictionary is insufficient, distinguish a context-based proposal or a separately verified specialist equivalent from the dictionary's own wording. Explain consequential departures briefly.
5. Use the Persian thesaurus through the indexed retrieval protocol above to explore semantic fields and related Persian expressions after source meaning has been established. The canonical DOCX remains authoritative; the supplied Markdown is an audit/search aid. Related words are not necessarily interchangeable, and an occurrence in the reverse term index is navigation rather than synonym evidence.
6. Maintain consistent equivalents for recurring concepts unless the author changes the sense; record approved choices in the project glossary as they are established.
7. Preserve dictionary source text. Do not silently reproduce damaged characters or assume dated spelling, typographical errors, or unsuitable senses are binding.
8. The three known damaged entries are listed in `aryanpour/source-character-issues.json`.

## Required paragraph-level supplementary checks

Per Adel's instruction of 2026-09-28, every paragraph review must also check the Persian thesaurus, a relevant passage of Daryabandari's Persian prose, and the relevant terminology/usage/orthography material in Ashouri, Najafi, and the Academy guide. Follow the three supplementary-check groups in [MENTOR_WORKFLOW.md](../MENTOR_WORKFLOW.md#required-supplementary-checks-for-every-paragraph).

Report each source's actual locator, finding, and effect on the proposed wording, including decisions to retain Adel's wording. For Ariyanpour, the locator must include the headword, Entry ID, shard path, and anchor when an exact entry is found. For Hezareh, include the headword, record ID, PDF page, verification status, boundary confidence, shard path, and anchor when a usable record is found. For the Persian thesaurus, include semantic entry ID, heading, shard path, anchor, finding, and effect. Clearly distinguish a checked passage, reused documented evidence, an unsuccessful scoped search, and an incomplete check caused by unavailable or unreadable material. Do not attribute a proposal to any of these sources without inspecting relevant evidence, or claim a source-to-translation comparison from Persian prose alone.

For historically significant German concepts, follow [GERMAN-CONCEPTS.md](GERMAN-CONCEPTS.md) and record practical translation decisions in [GLOSSARY.md](GLOSSARY.md). Research evidence and candidate/approved decision status are separate; no candidate becomes approved without Adel's explicit decision.

This policy guides this project's translation work. It does not mean the dictionary has been incorporated into permanent model training or that every entry has been memorized.
