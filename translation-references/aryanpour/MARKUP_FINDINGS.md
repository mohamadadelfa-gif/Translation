# Aryanpour Phase 2 — LD2 markup findings and interpretation policy

**Result:** Corpus-wide inventory completed and verified in GitHub Actions on 2026-10-10.
**Scope:** All 50,259 records in the frozen \`aryanpour-english-persian.jsonl\` export.
**Audit code:** [\`tools/analyze_markup.py\`](tools/analyze_markup.py), with [tests](tools/test_analyze_markup.py).
**Verification:** GitHub Actions run [38062023966](https://github.com/mohamadadelfa-gif/Translation/actions/runs/38062023966) (passed); [workflow](../../.github/workflows/aryanpour-audit.yml) stores an inventory report and 50,259 review-only observations as run artifacts.

## 1. Empirical results

| Property | Whole-corpus result |
|---|---:|
| Canonical LD2-derived entries examined | 50,259 |
| Unique tag names | 6: \`C\`, \`F\`, \`H\`, \`I\`, \`N\`, \`Ò\` |
| Distinct tag signatures | **1** |
| Records with tag nesting / bracket issues detected | 0 |
| Records without markup tags | 0 |
| Records starting with parenthesized text | **9,088** |
| Records containing parenthesized text anywhere | **12,276** |
| Existing source-character-damaged entries | 3 |

**The same tag sequence occurs in every record:**

\`\`\`text
<C><F><H /><I><N><Ò>...source definition text...</Ò></N></I></F></C>
\`\`\`

The exact signature is \`C F H I N Ò Ò N I F C\`. All 50,259 entries contain one opening and one closing instance of each of \`C\`, \`F\`, \`I\`, \`N\`, and \`Ò\`, plus one self-closing \`H\`. These tokens cannot distinguish senses from one another because the wrapper is invariant.

**Conclusion supported by data:** This LD2 export is structurally reliable as *headword + definition text*, but its current markup provides **no internal per-sense boundary markers**. Assigning semantic meanings to these tag names would not, by itself, extract individual senses, usage examples, grammatical labels, or references.

**What remains unverified:** Whether original printed dictionary typography, editorial conventions, or earlier intermediate resources contain more precise lexicographic structure. The attribution to a particular printed edition was not independently established by the LD2 extraction audit.

## 2. Why parentheses are not one uniform phenomenon

Examples below are backed by the frozen source's extraction samples and the full inventory's recorded candidate observations.

| Headword | Parenthesized text | Tentative reading | Source-safe treatment |
|---|---|---|---|
| \`aardwolf\` | \`(ج. ش.)\` | domain or dictionary abbreviation | **label candidate**, not confirmed label |
| \`a la carte\` | \`(در مورد کاغذ)\` | explanatory usage context | **usage-note candidate**, not a part of speech |
| \`abaxial\` | \`(=abaxile)\` | a reference to another headword | **cross-reference candidate**, unresolved |
| \`abaxile\` | \`(=abaxial)\` | a reciprocal reference | **cross-reference candidate**, unresolved |
| \`history\` | \`( طب )\`, later in definition | possible subject label within an unsegmented definition | **embedded candidate**; not necessarily label for all equivalents |

The leading-parenthetical strings themselves have frequent spelling/spacing variants: \`(طب)\`, \`( طب )\`, \`(طب )\`; \`(ج. ش.)\`, \`( ج. ش. )\`, etc. Search normalization may group candidates for investigation, but **must not rewrite source transcription**.

Among leading-parenthetical candidates, examples by original string include \`گ . ش. \` (859), \`ج. ش. \` (597), \`ش. \` (212), \` طب \` (198), \`طب\` (181), \`تش. \` (149), and \`مو. \` (103). These are raw counts, not counts of verified semantic categories.

## 3. Binding interpretation rules

### A. Headword and definition
- Every canonical record has an ID, an English headword, readable Persian definition, untouched LD2 markup, and a source-character-issue flag.
- This *entry-level* boundary is verified by export integrity checks; **do not conflate entry boundaries with internal sense boundaries**.
- Same-spelled headwords with different source IDs remain separate.

### B. Lexical sense boundaries
- **Never segment by comma, period, or the uniform markup wrapper.** Commas often separate equivalents within one presentation; periods may mark phrasing rather than discrete lexicographic senses.
- Create a verified sense only when an explicit structural cue or independently reviewed dictionary convention establishes the boundary.
- In the current automated output, \`sense_boundaries: null\` is mandatory. \`null\` means *not established*, not *one sense*.

### C. Grammatical labels, domains and abbreviations
- A parenthesized prefix is only a *candidate textual feature*.
- Maintain a dictionary-specific, evidence-backed register for abbreviation expansions (source rule, example IDs, review state). No expansion is authorized merely by a model's general linguistic knowledge.
- If a label may attach to only a subsection, keep its scope unresolved until reviewed.

### D. Examples
- No example is certified by the current markup schema.
- Do not infer an example from quoted text, an English substring, or an explanatory phrase alone. Record such spans as **example candidates** pending clear source conventions and review.

### E. Cross-references
- A leading parenthetical whose text begins with \`=\`, such as \`(=abaxile)\`, can be flagged as an **apparent-reference candidate**.
- Resolve a target only via an exact index lookup or a separately documented matching policy; preserve multiple matches and missing targets.
- Never assign a verified source relationship without an independently established convention. Parentheses without \`=\` do not automatically imply cross-reference.

### F. Verification and provenance
- Original wording remains frozen; candidates are maintained separately with \`canonical_id\`, \`headword\`, and original-markup SHA-256.
- Every interpretation records **observation**, **proposed role**, **evidence**, **reviewer**, **review status** and, if validated, **scope**.
- The Phase 2 candidate JSONL is expressly **review-only**: \`grammatical_labels\`, \`sense_boundaries\`, \`examples\`, and \`cross_references\` are \`null\`.
- Zero markup parsing errors is an engineering result, **not** evidence of perfect source semantics or translation correctness.

## 4. Output products and reproducibility

GitHub Actions runs:
\`\`\`powershell
python -m unittest discover -s translation-references/aryanpour/tools -p 'test_analyze_markup.py' -v
python translation-references/aryanpour/tools/analyze_markup.py --root translation-references/aryanpour --output aryanpour-markup-inventory.json --candidates aryanpour-markup-candidates.jsonl
\`\`\`

Reports are generated from the canonical JSONL; neither workflow nor analysis tool modifies dictionary data. The first file is a tag/parenthetical frequency report. The second is an **optional derived** record-per-entry observation layer, never a replacement for the canonical JSONL or a translator-approved glossary.

## 5. Release gates for any future semantic parser

Before promoting a candidate type into a verified automatic extraction rule:
1. Locate the dictionary's original abbreviation and usage guidance, or other compelling primary-source evidence.
2. Create a stratified human-checked test set: simple entries, polysemous entries, domains, embedded parentheses, reciprocal references, homographs, and damaged text.
3. Score **precision by candidate class**, not just the total number of extracted strings.
4. Require explicit review for ambiguous cases; never fill missing semantic fields through inference.
5. Keep automated candidates apart from translator-selected Persian equivalents.

**Decision:** The Phase 2 structural inventory is complete. **Semantic sense parsing is not validated and must not be introduced into the canonical source.** The next controlled step is a provenance-backed abbreviation/reference annotation pilot, rather than automatic sense splitting.
