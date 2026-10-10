# قواعد تألیف، ارجاع و ویرایش در فرهنگ علوم اجتماعی

**Authority:** the *Persian editorial introduction of this edition*, not a generic dictionary convention. Source: user-supplied scanned PDF `farhang-eolum-eejtemaii-g-k@bamun1.pdf`, **physical PDF pages 12–16** (printed introduction pages نه through سیزده). The accompanying [machine-checkable rules](editorial_rules.json) paraphrase the evidence; neither file is a complete verbatim transcription of the introduction.

## The book's own structure

### Sections within an explanatory article (PDF p. 13)

| Printed section marker | Stated function | Digital preservation rule |
|---|---|---|
| **A** | Main precise meaning of the term, or its widespread/general use in one or multiple social-science fields | Record the literal A section and its paragraphs; **do not automatically equate A with sense 1** |
| **B** | Historical background of the term or a more detailed treatment of its common meaning | Preserve as exposition, not automatic sense 2 |
| **C, D, E, …** | Historical development, specialist use in different disciplines, theoretical disagreements, competing meanings and debates | Preserve exact marker order and paragraphs; functions can vary by article |

The introduction demonstrates this with **شناخت — cognition**. It describes a general account in A, historical developments in B, specialized psychology in C and contemporary simulation-oriented research in D (PDF pp. 13–14). The example demonstrates that lettered portions are **discursive sections, not a simple bilingual translation list**. Entries may be differently long, and not every entry contains all letters.

### Three types of headword entry (PDF p. 14)

| Entry kind | Editorial term | Printed cue | Retrieval interpretation |
|---|---|---|---|
| Main article | مدخل اصلی | Explanatory article beneath heading | Store an independently transcribed article and its optional section structure |
| See referral | مدخل ارجاعی | The English **see** convention appears as **←** in Persian | Preserve literal target; **not** a standalone definition or automatic synonym |
| Also-linked article | مدخل همراه یا همگروه | English **also** appears as **نیز** in Persian | Entry remains in alphabetical sequence; preserve related main-entry reference **separately from ←** |

Do not treat a running page header as a new article, or assume that an `also` association means semantic synonymy.

### Contributor attribution (PDF p. 12)

The Persian introduction states that articles in the source were prepared by specialists and the names of responsible writers together with translator information may be placed at the end of individual articles. Such names are **bibliographic metadata**. A name between neighboring articles must not be attached to the wrong one merely by column position.

## Translation and typography rules of this Persian edition

Source section **«شیوۀ ترجمه و ویرایش مقالات»** (PDF pp. 14–16):

1. **Terminology was reviewed across specialties.** Translators and editors considered different available Persian renderings; source wording must be copied verbatim before any *project-specific* equivalent is selected. A printed chosen Persian headword is not an automatically approved translation equivalent for our own book.
2. **The translation was compared with the English source.** The PDF supplied to this project is the Persian version only. We must **not claim independent English-original verification** until a genuinely matching English original is available.
3. **Some subsidiary explanations appear between paired dashes.** Preserve the original punctuation and surrounding syntactic structure; never strip the delimited span as noise or assume all dashes delimit dictionary senses.
4. **Personal names were generally transcribed by original-language pronunciation, subject to exceptions.** Do not silently repair or standardize names; store a separate searchable comparison key if needed.
5. **House spelling conventions were adopted.** The printed orthography is evidence. Modernized spelling, if desired, belongs in a *separate derived overlay*.

These are statements about the editorial practice described in this **specific** Persian edition. They are not authorization to normalize text from the independent Aryanpour LD2 dictionary.

## Extraction requirements derived from the editorial rules

For every new Gould/Kolb entry, the extractor must retain:
- PDF page, column and original entry boundary evidence;
- **literal Persian headword and original-language headword**;
- `entry_kind`: main / referral / also / uncertain;
- **literal** source reference marker (← vs «نیز») and any target, without claiming resolved links;
- observed section labels and their **exact** text only when individually reviewed;
- independent author / translator credits where boundaries are verified;
- exact source punctuation including inserted explanations;
- transcription, review and source-original-verification statuses.

**Stop condition:** A source rule with no image-located evidence, a normalized rewriting without raw source, or an asserted cross-reference without a literal marker prevents promotion to a source-verified record. An OCR result, regardless of confidence, is a **draft candidate** until checked against page images.

## Development contract

- [editorial_rules.json](editorial_rules.json) is a **machine-readable, source-page-anchored register** of 12 observed editorial conventions.
- [tools/build_catalog.py](tools/build_catalog.py) requires it and rejects missing evidence pages and unsupported claims of verification against the original English book.
- [tools/test_build_catalog.py](tools/test_build_catalog.py) asserts **see/←** and **also/نیز** remain distinct and that reported authority never exceeds the actual source.

**Scope limit:** This is a careful reading of the **Persian editorial instructions** (PDF pp. 12–16), not a recovered complete editorial manual or a full comparison with the English-language source. Some printed typography and editorial details elsewhere in the book may require further inspection.
