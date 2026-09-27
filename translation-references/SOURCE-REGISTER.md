# Translation Reference Register

Updated 2026-09-27.

This file defines the approved reference set and the role of each source in the English-to-Persian translation of *Revisiting Zero Hour 1945*.

Files under `sources/` are treated as supplied source material and should remain unchanged during ordinary translation work.

## 1. Primary source text

### Main book

`sources/revisiting-zero-hour-1945-structured.md`
# 

# This is the main structured source text for:

# 

# \*Revisiting Zero Hour 1945\*

# 

# Use it to determine:

# 

# \- source wording;

# \- argument;

# \- terminology;

# \- quotations;

# \- paragraph structure;

# \- endnotes;

# \- relations between chapters.

# 

# The source author's meaning and argumentative distinctions have priority over dictionary convenience.

# 

# \### Chapter files

# 

# ```text

# sources/C00.md

# sources/C01.md

# sources/C02.md

# sources/C03.md

# sources/C04.md

# sources/C05.md

# ```

# 

# These files provide chapter-level working access to the source.

# 

# They should be used together with the structured source when local context, paragraph structure, or endnotes are needed.

# 

# \---

# 

# \## 2. Structural and contextual guides

# 

# \### Front matter

# 

# `source/front-matter.md`

# 

# Use for publication context and front-matter information.

# 

# \### Translation map

# 

# `source/START-HERE.md`

# 

# \### Context and structure guide

# 

# `source/CONTEXT-AND-STRUCTURE.md`

# 

# These are working guides for navigating the book and understanding its structure.

# 

# They are \*\*editorial and project aids\*\*, not independent historical authorities.

# 

# Their chapter codes, unit labels, and explanatory divisions should not be confused with authorial section numbering unless the source itself contains those divisions.

# 

# \---

# 

# \# 3. General English–Persian vocabulary

# 

# The project uses \*\*two active general bilingual references\*\*:

# 

# 1\. Ariyanpour

# 2\. Hezareh

# 

# Neither automatically has priority over the other.

# 

# For consequential or uncertain vocabulary, compare both when useful.

# 

# \---

# 

# \## 3.1 Ariyanpour

# 

# Readable reference:

# 

# `translation-references/aryanpour/aryanpour-english-persian.txt`

# 

# Lookup data:

# 

# `translation-references/aryanpour/aryanpour-english-persian.jsonl`

# 

# A copy also exists in:

# 

# `source/aryanpour-english-persian.txt`

# 

# Ariyanpour is one of the preferred general English–Persian vocabulary references.

# 

# The extracted LD2 data contains approximately 50,259 entries.

# 

# The Ariyanpour attribution was supplied for the project; the exact edition has not been independently verified.

# 

# Three known damaged source-character cases are recorded in:

# 

# `translation-references/aryanpour/source-character-issues.json`

# 

# \### Role

# 

# Use Ariyanpour for:

# 

# \- general lexical meanings;

# \- alternative Persian equivalents;

# \- distinguishing senses of polysemous English words;

# \- comparison with Hezareh;

# \- checking recurrent vocabulary.

# 

# Do not automatically choose the first equivalent.

# 

# Do not attribute a wording to Ariyanpour unless the relevant entry has actually been checked.

# 

# \---

# 

# \## 3.2 Hezareh

# 

# The supplied Hezareh dictionary is available in eight text files:

# 

# ```text

# sources/Hezareh\_Part\_01\_PDF\_0001-0250.txt

# sources/Hezareh\_Part\_02\_PDF\_0251-0500.txt

# sources/Hezareh\_Part\_03\_PDF\_0501-0750.txt

# sources/Hezareh\_Part\_04\_PDF\_0751-1000.txt

# sources/Hezareh\_Part\_05\_PDF\_1001-1250.txt

# sources/Hezareh\_Part\_06\_PDF\_1251-1500.txt

# sources/Hezareh\_Part\_07\_PDF\_1501-1750.txt

# sources/Hezareh\_Part\_08\_PDF\_1751-1976.txt

# ```

# 

# Hezareh is an \*\*active vocabulary reference\*\*, not merely a backup for Ariyanpour.

# 

# \### Role

# 

# Use Hezareh for:

# 

# \- general English–Persian lexical lookup;

# \- comparison of senses with Ariyanpour;

# \- additional Persian candidates;

# \- checking idiomatic or context-sensitive possibilities;

# \- investigating words where Ariyanpour alone does not adequately represent the semantic range.

# 

# \### OCR caution

# 

# The supplied text contains machine-recognized material.

# 

# Therefore:

# 

# \- distinguish reliable-looking entries from suspicious OCR;

# \- do not silently repair damaged wording and then attribute the repair to Hezareh;

# \- when an entry is doubtful, mark the uncertainty;

# \- verify against the original page when possible and when the lexical decision is consequential.

# 

# This evidence-quality issue does \*\*not\*\* make Hezareh secondary to Ariyanpour.

# 

# \---

# 

# \# 4. Default bilingual vocabulary procedure

# 

# For a significant or uncertain English word:

# 

# ```text

# SOURCE CONTEXT

# &#x20;     ↓

# ARIYANPOUR

# &#x20;     +

# HEZAREH

# &#x20;     ↓

# COMPARE RELEVANT SENSES

# &#x20;     ↓

# SPECIALIST SOURCE IF NEEDED

# &#x20;     ↓

# PERSIAN OPTIONS

# &#x20;     ↓

# ADEL'S DECISION

# ```

# 

# Agreement between Ariyanpour and Hezareh can strengthen confidence in a general lexical sense.

# 

# However:

# 

# ```text

# dictionary agreement

# ≠

# automatic contextual correctness

# ```

# 

# The meaning in the source passage remains decisive.

# 

# When the dictionaries disagree:

# 

# 1\. identify which senses they are representing;

# 2\. compare those senses with the sentence and argument;

# 3\. consult a specialist source when necessary;

# 4\. explain significant differences;

# 5\. leave the final Persian choice with Adel.

# 

# \---

# 

# \# 5. Humanities and theoretical terminology

# 

# \## Ashouri — فرهنگ علوم انسانی

# 

# `source/Ashouri — فرهنگ علوم انسانی.pdf`

# 

# Use this source for:

# 

# \- humanities terminology;

# \- philosophical and theoretical vocabulary;

# \- social-science concepts;

# \- established Persian terminology in relevant intellectual fields.

# 

# Ashouri is a specialist terminology source, not a replacement for contextual analysis.

# 

# Do not claim that Ashouri supports an equivalent unless the relevant entry has actually been inspected.

# 

# For a technical term, the working sequence may be:

# 

# ```text

# source context

# &#x20;     ↓

# Ariyanpour + Hezareh

# &#x20;     ↓

# Ashouri

# &#x20;     ↓

# specialist / historical evidence

# &#x20;     ↓

# Persian decision

# ```

# 

# \---

# 

# \# 6. German historical and conceptual terminology

# 

# Use:

# 

# `translation-references/GERMAN-CONCEPTS.md`

# 

# for terms whose German historical, institutional, legal, political, intellectual, academic, or literary identity materially affects translation.

# 

# Examples include:

# 

# \- `Stunde Null`

# \- `Nullpunkt`

# \- `Kahlschlag`

# \- `Vergangenheitsbewältigung`

# \- `Wiedergutmachung`

# \- `Germanistik`

# \- `Germanisten`

# \- `Wissenschaft`

# \- `Feuilleton`

# \- `Nachholen`

# \- `nachgeholte Résistance`

# 

# General bilingual dictionaries may provide lexical possibilities, but they do not by themselves establish the historical meaning of these concepts.

# 

# For these terms distinguish:

# 

# \- literal meaning;

# \- dictionary evidence;

# \- historical evidence;

# \- author-specific use;

# \- Persian candidate;

# \- Adel's approved choice.

# 

# Follow the procedure defined in `MENTOR\_WORKFLOW.md` and `GERMAN-CONCEPTS.md`.

# 

# \---

# 

# \# 7. Persian semantic field and word exploration

# 

# \## فرهنگ طیفی — تزاروس فارسی

# 

# Primary project file:

# 

# `source/فرهنگ طیفی - تزاروس فارسی.docx`

# 

# This Word document is the active project source for exploring Persian semantic relationships and related expressions.

# 

# \### Role

# 

# Use it for:

# 

# \- exploring semantic fields;

# \- finding related Persian words;

# \- comparing possible formulations;

# \- identifying neighboring concepts;

# \- expanding the range of candidate Persian expressions after the source meaning has been established.

# 

# The thesaurus does \*\*not\*\* determine the meaning of the English source.

# 

# Its correct role is:

# 

# ```text

# SOURCE MEANING

# &#x20;     ↓

# BILINGUAL / SPECIALIST EVIDENCE

# &#x20;     ↓

# PERSIAN THESAURUS

# &#x20;     ↓

# PERSIAN EXPRESSION OPTIONS

# ```

# 

# Related words are not automatically synonyms.

# 

# A semantic neighbor in the thesaurus must still be evaluated for:

# 

# \- precision;

# \- register;

# \- collocation;

# \- historical appropriateness;

# \- grammatical compatibility;

# \- suitability for scholarly Persian.

# 

# Do not choose a word merely because it appears near another word in the thesaurus.

# 

# \---

# 

# \# 8. Persian usage

# 

# \## Najafi — غلط ننویسیم

# 

# `source/Najafi — غلط ننویسیم.pdf`

# 

# Use Najafi for consequential questions of Persian usage.

# 

# Relevant uses include:

# 

# \- questionable constructions;

# \- standard versus problematic usage;

# \- lexical usage questions;

# \- Persian syntactic conventions where the source is relevant.

# 

# Najafi is a Persian usage reference.

# 

# It does not determine the meaning of the English source.

# 

# Always inspect the relevant entry before attributing a recommendation to Najafi.

# 

# \---

# 

# \# 9. Persian orthography

# 

# \## فرهنگستان — دستور خط فارسی

# 

# `source/فرهنگستان — دستور خط فارسی.pdf`

# 

# Use the Academy guide for:

# 

# \- spelling;

# \- spacing;

# \- half-spaces;

# \- compounds;

# \- affixes;

# \- punctuation conventions where covered;

# \- Persian character and orthographic conventions.

# 

# The Academy guide regulates written form.

# 

# It is not a lexical or conceptual authority on the English source.

# 

# Where edition-specific rules matter, inspect the supplied text before making a categorical claim.

# 

# \---

# 

# \# 10. Persian translated-prose reference

# 

# \## Najaf Daryabandari — \*As I Lay Dying / گور به گور\*

# 

# `source/گور به گور - ویلیام فاکنر.pdf`

# 

# This project identifies the supplied file as Najaf Daryabandari's Persian translation of William Faulkner's \*As I Lay Dying\* (\*گور به گور\*).

# 

# Use it as a \*\*translation-craft and Persian prose reference\*\*.

# 

# It is not a general bilingual dictionary.

# 

# \### Main role

# 

# Study how a professional translator reconstructs English prose in Persian, especially:

# 

# \- sentence restructuring;

# \- movement of clauses;

# \- release from English word order;

# \- selection of natural Persian verbs;

# \- rhythm;

# \- verbal economy;

# \- transitions;

# \- control of sentence length;

# \- deliberate repetition;

# \- preservation of logical relations during restructuring;

# \- balance between fidelity and natural Persian expression.

# 

# \### Important limitation

# 

# \*As I Lay Dying\* is a literary work with multiple fictional voices.

# 

# Therefore, do not mechanically transfer:

# 

# \- its narrative voice;

# \- colloquial features;

# \- characterization;

# \- dialectal effects;

# \- literary mannerisms;

# \- fictional rhythm

# 

# into the scholarly prose of \*Revisiting Zero Hour 1945\*.

# 

# Use \*\*translation techniques\*\*, not surface imitation.

# 

# \### Evidence discipline

# 

# Do not make broad claims such as:

# 

# > “Daryabandari always translates this structure in this way.”

# 

# unless relevant passages have actually been inspected.

# 

# When using Daryabandari as evidence for a translation technique, identify the specific passage or pattern being examined whenever practical.

# 

# \---

# 

# \# 11. Project glossary

# 

# Use:

# 

# `translation-references/GLOSSARY.md`

# 

# for practical recurring translation decisions.

# 

# This file records project choices; it is not itself a dictionary.

# 

# A glossary entry may record evidence such as:

# 

# ```text

# Ariyanpour + Hezareh

# ```

# 

# or:

# 

# ```text

# Hezareh + Ashouri

# ```

# 

# or:

# 

# ```text

# Ariyanpour + Hezareh + German historical source

# ```

# 

# Do not write “dictionary confirmed” without identifying which source was actually checked.

# 

# Glossary status must follow:

# 

# \- `candidate`

# \- `approved`

# \- `reconsider`

# \- `retired`

# 

# A candidate does not become approved merely because it has been used repeatedly.

# 

# Adel must explicitly approve it.

# 

# \---

# 

# \# 12. Source roles at a glance

# 

# | Source | Primary role |

# | --- | --- |

# | \*Revisiting Zero Hour 1945\* | meaning, argument, source wording and context |

# | Ariyanpour | general English–Persian vocabulary |

# | Hezareh | general English–Persian vocabulary |

# | Ashouri | humanities and theoretical terminology |

# | `GERMAN-CONCEPTS.md` + historical sources | German historical and conceptual terminology |

# | فرهنگ طیفی | Persian semantic field and alternative expressions |

# | Najafi | Persian usage |

# | فرهنگستان | orthography and writing conventions |

# | Daryabandari, \*As I Lay Dying / گور به گور\* | translation craft and Persian prose reconstruction |

# | `GLOSSARY.md` | recording project terminology decisions |

# 

# \---

# 

# \# 13. Evidence discipline

# 

# Always distinguish between:

# 

# \### Source evidence

# 

# What the original English text actually says.

# 

# \### Dictionary evidence

# 

# What Ariyanpour, Hezareh, or another dictionary actually records.

# 

# \### Specialist evidence

# 

# What a checked specialist, historical, legal, philosophical, or disciplinary source actually supports.

# 

# \### Persian usage evidence

# 

# What a checked Persian usage or orthographic reference supports.

# 

# \### Prose comparison

# 

# What can be observed in a specific translated-prose example such as Daryabandari.

# 

# \### Mentor analysis

# 

# An interpretation or recommendation developed from context.

# 

# \### Adel's decision

# 

# The final project translation choice.

# 

# These categories must not be silently collapsed.

# 

# \---

# 

# \# 14. Reference-use rule

# 

# Before saying:

# 

# > “Ariyanpour gives…”

# 

# check Ariyanpour.

# 

# Before saying:

# 

# > “Hezareh gives…”

# 

# check Hezareh.

# 

# Before saying:

# 

# > “Ashouri uses…”

# 

# inspect Ashouri.

# 

# Before saying:

# 

# > “Najafi recommends…”

# 

# inspect Najafi.

# 

# Before saying:

# 

# > “The Academy rule is…”

# 

# inspect the supplied Academy guide.

# 

# Before deriving a translation technique from Daryabandari, inspect the relevant passage.

# 

# Before describing the historical meaning of a German concept, consult appropriate evidence.

# 

# Never fabricate source support.

# 

# \---

# 

# \# 15. Core source-selection principle

# 

# Different sources answer different questions.

# 

# ```text

# WHAT DOES THE ENGLISH MEAN?

# → source text + context

# 

# WHAT LEXICAL SENSES ARE AVAILABLE?

# → Ariyanpour + Hezareh

# 

# IS THIS A SPECIALIST HUMANITIES TERM?

# → Ashouri + relevant specialist sources

# 

# IS THIS A GERMAN HISTORICAL CONCEPT?

# → GERMAN-CONCEPTS.md + historical sources

# 

# WHAT PERSIAN WORDING OPTIONS EXIST?

# → فرهنگ طیفی

# 

# IS THIS GOOD / STANDARD PERSIAN USAGE?

# → Najafi

# 

# HOW SHOULD IT BE WRITTEN?

# → Academy orthography guide

# 

# HOW CAN ENGLISH PROSE BE REBUILT NATURALLY IN PERSIAN?

# → Daryabandari / گور به گور

# 

# WHAT HAS THIS PROJECT DECIDED?

# → GLOSSARY.md

# 

# WHO MAKES THE FINAL TRANSLATION DECISION?

# → Adel

# ```

# 

# No source should be used outside its evidentiary role without explanation.

# 

# \---

# 

# \# 16. Deferred or unverified materials

# 

# The previously mentioned Babylon Ariyanpour BDC comparison remains deferred unless Adel chooses to resume it.

# 

# Cronin, K1, RTS, or other frameworks mentioned in older planning materials are not active lexical, historical, or translation authorities unless the relevant source documents are actually supplied and reviewed.

# 

# `MENTOR\_WORKFLOW.md` and the project instructions govern \*\*method and pedagogy\*\*. They are not themselves lexical or historical evidence.

# 

# \---

# 

# \# 17. Final rule

# 

# The project should never ask only:

# 

# > “Which dictionary gives the best Persian word?”

# 

# The correct sequence is:

# 

# ```text

# SOURCE

# &#x20;  ↓

# CONTEXT AND ARGUMENT

# &#x20;  ↓

# ARIYANPOUR + HEZAREH

# &#x20;  ↓

# SPECIALIST / HISTORICAL SOURCES WHEN NEEDED

# &#x20;  ↓

# PERSIAN SEMANTIC AND USAGE SOURCES

# &#x20;  ↓

# PROSE RECONSTRUCTION WHEN NEEDED

# &#x20;  ↓

# COMPARISON OF OPTIONS

# &#x20;  ↓

# ADEL'S DECISION

# ```

# 

# The purpose of the reference system is not to replace translation judgment.

# 

# It is to make that judgment more informed, explicit, teachable, and traceable.

