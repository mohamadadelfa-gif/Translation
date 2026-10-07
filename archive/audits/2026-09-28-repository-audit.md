# Translation Mentor repository audit — 2026-09-28

This is an audit record, not an active workflow or a translation approval.

Repository: https://github.com/mohamadadelfa-gif/Translation

Initial audit baseline: `28331f0972c05823fe4187dba06ec9c004ad7dbb`.

Resumed audit baseline: `master` at `3f1086e13256ba0df0a08ce02316398494a9c185`. The GitHub branches API and local HEAD matched on 2026-09-28. Earlier audit corrections were already present in this live commit when work resumed. New Hezareh and thesaurus materials had also arrived. The current pass therefore checked this newer state rather than treating the earlier inventory as current.

The resumed pass made local changes only. It did not commit, push, or publish files. The supplied untracked `sources/Hezareh_translation_ready_markdown.zip` was preserved and was not treated as part of the live repository.

## A. Repository health summary

The existing system is coherent and usable after the mechanical corrections below. Its authority chain distinguishes supplied material, working preparation, reference policies, learner drafts, mentor proposals, and explicit approvals. The four levels below the book are Chapter, Translation Unit, Practice Chunk, and Sentence. Structural `S` units remain distinct from approximately 250–350-word `P` exercises; sentence identifiers are optional.

The main remaining limitation is incomplete archival evidence for reported progress. `PROGRESS.md` declares `C00-S02-P03`, beginning “Once this route was taken…”. That sentence is present in C00-S02, immediately after the quoted “Thus, renegotiating…” sentence. However, the saved draft and mentor revision stop earlier. This is a recovery gap, not evidence that translation never happened. The audit preserved the declared continuation point and added a qualification rather than guessing a different position.

The active lexical policies now treat Ariyanpour and Hezareh as peers. The supplied Hezareh index is a retrieval aid with explicit evidence-status limits. German-concept research state is separate from approval of a Persian rendering. No translation, historical interpretation, or glossary approval was added by this audit.

### Verification performed

- The resumed live baseline contains 76 tracked files. The Markdown inspection covered 46 files, including 23 active documents outside `sources/` and `archive/`, before this report was added.
- No missing Markdown file-link targets, unresolved local footnotes, or unbalanced triple-backtick fences were found in active documents after fixes. Six broken TOC anchors remain in immutable `sources/front-matter.md`; the working copy has functioning chapter links. Four source-dictionary passages resemble Markdown links; see B14.
- All six working chapter files and the complete structured book remain byte-identical to their matching supplied snapshots. Working guides and standalone front-matter navigation intentionally differ; synchronization is not assumed.
- The preparation generator was run from a separate temporary project directory, using the original Desktop input. It produced six chapter files and 32 units. Chapter files and the complete structured book matched the working versions after line-ending normalization. Generated map and standalone front matter differed only in final-newline/blank-line formatting. The generator's own source-restoration checks passed. It was not run against the working preparation directory.
- The retired migration helper was invoked and stopped with its retirement error before any file operation.
- All eight current Hezareh extraction hashes matched the supplied manifest exactly. SQLite `integrity_check` returned `ok`. SQLite and dictionary JSONL counts agreed at 38,957 records: 186 marked `visually_checked` and 38,771 marked `raw_ocr` in SQLite. All JSONL source line ranges referred to existing files and valid line bounds.
- Six lookup smoke cases passed: `maximum`, `manner`, `mannerism`, `reprehensible`, `may`, and `thinkable`. In these cases, the lookup kept `manner` separate from `mannerism`, returned numbered senses for `may`, and preferred supplied checked records over competing raw OCR. The database hash was unchanged after lookup.
- These checks validate retrieval and package consistency, not the accuracy of the original dictionary OCR, the original PDF, every index boundary, or the translation value of an equivalent.
- `git diff --check` passed. The resumed pass produced no changes under `sources/`, `drafts/`, or `approved-translations/`.

## B. Problems found

Locations use section names to remain useful after line shifts. “Earlier fix” means a correction made during the initial audit that was already present in the resumed live baseline. “Current fix” means a local correction in this resumed pass.

### B1. Reported completion exceeds saved draft coverage

- **Severity:** Important.
- **File:** `PROGRESS.md`; `drafts/C00/C00-introduction-progress-2026-09-27.txt`; `drafts/C00/C00-introduction-reviewed-01.md`; `drafts/C00/C00-introduction-review-notes-01.md`.
- **Location:** Progress completion labels and last/next sentence sections; draft endpoints; review-notes opening scope statement.
- **Problem:** P01/P02 are reported complete, but the saved draft and review stop at “a new interest and understanding of the past”. The later “Thus…” translation appears in PROGRESS, while the intervening “This operation…”, “Today we rarely remember…”, and “Although the meetings…” translations are not in those saved artifacts. Exact P01/P02 boundaries are also absent.
- **Why it matters:** A new session could confuse reported work with recoverable files or infer approval from completion.
- **Recommended fix:** Recover the actual submissions and identify exact source boundaries with Adel. Do not reconstruct missing learner wording from mentor prose.
- **Status:** Earlier fix added an explicit recovery/evidence note and retained the cursor. Archival reconciliation remains open. No approved translation file exists.

### B2. Derived guides could be mistaken for source authority

- **Severity:** Important.
- **File:** `MENTOR_WORKFLOW.md`; `translation-references/SOURCE-REGISTER.md`.
- **Location:** Workflow §5; register §2.
- **Problem:** Earlier wording gave both the English source and structural guides authority over meaning; active guide paths pointed to the supplied snapshots.
- **Why it matters:** A derived summary or stale guide could override the book or encourage editing immutable material.
- **Recommended fix:** Give meaning authority to the book, use preparation guides for navigation, and identify the source-directory copies as snapshots.
- **Status:** Earlier fix applied. No source copy was overwritten.

### B3. General vocabulary policy gave inconsistent weight to Hezareh

- **Severity:** Important.
- **File:** `translation-references/WORD-CHOICE-POLICY.md`; `MENTOR_WORKFLOW.md`; `AGENTS.md`.
- **Location:** Word-choice procedure item 1; workflow §5; AGENTS reference discipline.
- **Problem:** The earlier procedure named only Ariyanpour at the normal lookup step, although the source register treated both dictionaries as active peers.
- **Why it matters:** Consequential choices could be made without the intended comparison.
- **Recommended fix:** Compare relevant senses in both dictionaries and record unavailable or inconclusive lookups; preserve OCR qualifications.
- **Status:** Earlier fix applied. No dictionary entry or Persian equivalent was approved.

### B4. Thesaurus format and additional version were not accurately registered

- **Severity:** Important.
- **File:** `translation-references/WORD-CHOICE-POLICY.md`; `translation-references/SOURCE-REGISTER.md`.
- **Location:** Policy item 5; register §7.
- **Problem:** An earlier policy referred to a PDF instead of the active Word file. The resumed baseline also contained a new Markdown version without a defined relationship to Word.
- **Why it matters:** The mentor might search an absent file or assume conversion guarantees textual reliability.
- **Recommended fix:** Link Word as the active reference and describe Markdown as an available lookup aid whose equivalence has not been fully verified.
- **Status:** Earlier PDF-to-Word correction retained; current fix registers the Markdown version. Neither supplied file was edited.

### B5. Research state and translation approval were mixed

- **Severity:** Important.
- **File:** `translation-references/GERMAN-CONCEPTS.md`; `MENTOR_WORKFLOW.md`.
- **Location:** Concept status rules, entry template and initial index; workflow §§6.9 and 9.
- **Problem:** The concept index used “Status” for `research needed`, while the decision system used candidate/approved/reconsider/retired.
- **Why it matters:** Research completion could be confused with approval of a Persian equivalent.
- **Recommended fix:** Maintain separate research-state and translation-decision fields, and identify the initial table as a research backlog.
- **Status:** Earlier fix applied. No concept definition or equivalent was invented or promoted.

### B6. Obsolete root migration helper could overwrite active decisions

- **Severity:** Important.
- **File:** Former root `apply-structure-fix.ps1` and `STRUCTURE-CHANGESET.md`, now in `archive/migration/`.
- **Location:** Helper force-copy block; changeset proposed replacement list.
- **Problem:** The old migration copied a partial bundle over current workflow, glossary, and policy files and no longer described the active architecture.
- **Why it matters:** Running it could discard current instructions and terminology decisions.
- **Recommended fix:** Retain as historical material, remove from the active root, and stop the helper before writes.
- **Status:** Earlier fix moved both files, marked the note historical, and added an unconditional retirement error. Current test confirmed the early stop.

### B7. Working context guide claimed translation had not begun

- **Severity:** Minor.
- **File:** `translation-preparation/CONTEXT-AND-STRUCTURE.md`.
- **Location:** Opening project-state note.
- **Problem:** “No translation has begun” contradicted active drafts and PROGRESS.
- **Why it matters:** A session could restart preparation unnecessarily.
- **Recommended fix:** Refer readers to PROGRESS for the current state.
- **Status:** Earlier fix applied only in the working guide. The matching source snapshot remains historical supplied material.

### B8. C01 map missed an original subsection

- **Severity:** Minor.
- **File:** `translation-preparation/START-HERE.md`; `tools/organize.ps1`.
- **Location:** C01-S02/S03 map rows; generator subsection detection.
- **Problem:** The source heading “The Origins of the Term ‘Zero Hour’” is bold rather than a level-three heading. The map labeled both units “Opening discussion”, and the generator would recreate that error.
- **Why it matters:** Navigation obscured the author's actual section structure.
- **Recommended fix:** Recognize this original bold subsection and label both existing units correctly.
- **Status:** Earlier map fix retained; current generator fix passed isolated regeneration. Existing chapter text and unit numbering did not change.

### B9. Preparation entry point did not fully explain practice chunks

- **Severity:** Minor.
- **File:** `translation-preparation/START-HERE.md`; `tools/organize.ps1`; `AGENTS.md`; `MENTOR_WORKFLOW.md`.
- **Location:** Map opening instructions; generator map preamble; hierarchy descriptions.
- **Problem:** Users entering through the map could mistake large structural units for daily sessions; “four levels” also needed qualification as levels below the book.
- **Why it matters:** It encourages mechanical 300-word division or incorrect chunk identifiers.
- **Recommended fix:** Explain S/P distinctions, argument-led boundaries, optional sentence identifiers, and exact boundary recording in PROGRESS.
- **Status:** Earlier documentation fix retained; current generator now preserves the map explanation on regeneration.

### B10. Standalone front matter had six broken chapter anchors

- **Severity:** Minor.
- **File:** `translation-preparation/front-matter.md`; `sources/front-matter.md`; `tools/organize.ps1`.
- **Location:** Table of contents, chapter entries (source snapshot lines 65–70).
- **Problem:** Same-document links target headings located in separate chapter files. Those anchors work in the complete structured book, but not in standalone front matter.
- **Why it matters:** The standalone TOC cannot navigate to chapters.
- **Recommended fix:** Use C00.md–C05.md in the working standalone file and retain original anchors in the complete book.
- **Status:** Earlier working-file fix retained; current generator preserves this distinction. Immutable source snapshot links are deliberately left unchanged.

### B11. Reference integration and style-evidence limits needed clarification

- **Severity:** Minor; teaching detail is an optional improvement.
- **File:** `README.md`; `translation-references/GERMAN-CONCEPTS.md`; `translation-references/SOURCE-REGISTER.md`; `MENTOR_WORKFLOW.md`.
- **Location:** README navigation; concept title; register prose-reference section; workflow opening.
- **Problem:** The main navigation omitted the concept layer; one project title used “Zero-Hour”; prose-reference guidance did not explicitly distinguish observing Persian craft from proving a source-to-translation transformation. B1 teaching expectations also needed carrying forward explicitly.
- **Why it matters:** Resources become harder to find, and style analysis could imply a comparison that has not occurred.
- **Recommended fix:** Link the concept file, standardize the project title, require paired passages for transformation claims, and retain stepwise B1 instruction.
- **Status:** Earlier fixes applied. No English Faulkner counterpart was inspected or fabricated.

### B12. Current Hezareh paths were broken after the package import

- **Severity:** Critical: breaks documented reference lookup.
- **File:** `translation-references/SOURCE-REGISTER.md`; `README.md`.
- **Location:** Register §3.2; README main references.
- **Problem:** All eight registered top-level `.txt` files were absent at the resumed live commit. Current extractions are `.md` files inside `sources/Hezareh_Dictionary_Index/source/`.
- **Why it matters:** Following the authoritative register cannot locate the intended dictionary parts.
- **Recommended fix:** Correct all eight paths and identify the supplied retrieval package.
- **Status:** Current fix applied; paths and manifest hashes checked. The audit did not rename or restore source files. Hash checks establish consistency with the current supplied manifest, not identity with the former text editions or the original PDF.

### B13. Imported index documentation needed a project-specific boundary

- **Severity:** Important.
- **File:** `sources/Hezareh_Dictionary_Index/README.md`; `translation-references/SOURCE-REGISTER.md`.
- **Location:** Supplied package “Integration principle” and source-pointer examples; register §3.2.
- **Problem:** The package illustrates a different root architecture and uses package-relative `source/...` pointers. It also carries supplied `visually_checked` labels that a mentor could overstate as fresh verification.
- **Why it matters:** A reader could reorganize the repository unnecessarily, resolve pointers from the wrong directory, or confuse inherited metadata with checked evidence.
- **Recommended fix:** Explain pointer resolution and evidence status in the active register, retaining the supplied package unchanged.
- **Status:** Current fix applied. The package is read-only; its example tree does not govern this repository. No tracked original Hezareh PDF is available for independent visual checking.

### B14. Supplied dictionary text includes Markdown-looking punctuation

- **Severity:** Minor.
- **File:** `sources/Hezareh_Dictionary_Index/source/Hezareh_Part_03_PDF_0501-0750.md`, Part 04, Part 05, and Part 06 in the same directory.
- **Location:** Lines 25711, 7424, 23016, and 10900 respectively in the resumed source snapshot.
- **Problem:** Four dictionary passages contain bracket-plus-parenthesis sequences that a simple Markdown checker reads as links to Persian prose rather than files.
- **Why it matters:** Rendering may interpret lexical punctuation as navigation, and automated link checks may report false path failures.
- **Recommended fix:** Read these passages as source data. If a rendering correction becomes necessary, make it in a clearly derived presentation copy after checking the passage, not in the supplied snapshot.
- **Status:** Preserved; not counted as broken active project navigation. Balanced fences and literal escaped grammatical labels in supplied dictionaries are not automatically formatting bugs.

## C. Changes actually made

### Earlier audit corrections already present in the resumed live commit

| File | Exact change category |
| --- | --- |
| `AGENTS.md` | Clarified four working levels below the book, dictionary-peer comparison, and separate conceptual research state. |
| `MENTOR_WORKFLOW.md` | Restored B1 teaching expectations; clarified hierarchy, source-versus-guide authority, bilingual comparison, conceptual research sequence, and separate evidence/decision states. |
| `PROGRESS.md` | Added archival-evidence limits and defined the copied continuation footnote. Kept the draft wording and resume position. |
| `README.md` | Added concept-layer navigation and clarified the references directory's purpose. |
| `archive/README.md` | Documented the historical migration directory. |
| `archive/migration/STRUCTURE-CHANGESET.md` | Moved the obsolete root note and added a historical-status warning. |
| `archive/migration/apply-structure-fix.ps1` | Moved the old root helper and added an unconditional stop before file operations. |
| `translation-preparation/CONTEXT-AND-STRUCTURE.md` | Replaced stale project-state claim and reconciled the note about the C01 map. |
| `translation-preparation/START-HERE.md` | Explained practice chunks and corrected two C01 section labels. |
| `translation-preparation/front-matter.md` | Replaced six standalone chapter anchors with chapter-file destinations. |
| `translation-references/GERMAN-CONCEPTS.md` | Standardized the title and separated research state from translation-decision status in rules, template, and index. |
| `translation-references/SOURCE-REGISTER.md` | Directed active guide references to preparation; clarified source snapshots and the evidence needed for prose-transformation comparisons. |
| `translation-references/WORD-CHOICE-POLICY.md` | Made bilingual comparison explicit and replaced the absent thesaurus PDF reference with Word. |

### Local changes in the resumed pass

| File | Exact change category |
| --- | --- |
| `README.md` | Linked the actual Hezareh package and named its current Markdown extraction directory. |
| `translation-references/SOURCE-REGISTER.md` | Repaired eight Hezareh paths; documented package-relative pointers, read-only status and inherited verification labels; registered the supplied thesaurus Markdown with a verification limit. |
| `translation-references/WORD-CHOICE-POLICY.md` | Added Markdown thesaurus lookup guidance while retaining Word comparison for doubtful extraction. |
| `tools/organize.ps1` | Preserved the chunk explanation in generated maps; recognized C01's original bold subsection; generated chapter-file links only in standalone front matter, with a six-link count check. |
| `tools/README.md` | Documented corrected generation behavior and temporary-directory verification. |
| `archive/audits/2026-09-28-repository-audit.md` | Added this report and verification record. |

The newer Hezareh package, removal of old top-level Hezareh text paths, and addition of the thesaurus Markdown predated the resumed edits and are not claimed as audit changes. No supplied source, learner translation, approved translation, or lexical decision was changed in this pass.

## D. Human decisions still required

1. Reconcile the original submissions and exact P01/P02 boundaries before treating completed chunks as fully archived. The earlier chat contains later learner passages, but this audit has not selected, relabeled, or approved versions of them as repository drafts.
2. Explicitly accept or revise Persian terminology and translation proposals when they are reviewed. Pending terms in PROGRESS remain unresolved; no approval is inferred from this audit.
3. Supply an original dictionary page when a consequential OCR reading cannot be resolved from the supplied extraction. Independent historical sources are likewise needed where the German-concept research remains open.
4. A paired English Faulkner passage is needed if the task is to demonstrate how Daryabandari transformed that particular source sentence. The Persian text can already support observations about Persian prose, within that narrower scope.

None of these decisions requires a redesign of the repository. Archival reconciliation does not prevent a clearly labeled sentence-review session at the declared continuation point.

## E. Remaining technical debt

- The preparation and LD2 tools still depend on original Desktop inputs and can overwrite their documented derived outputs. Explicit input/output parameters or staging safeguards would be useful later; ordinary translation does not require running them.
- The supplied Hezareh package includes build rules and results but no index-building program. Its lookup script uses a normal SQLite connection rather than an enforced read-only connection. It was tested only with the existing intact database; a future derived maintenance tool could improve reproducibility and defensive file access without altering the snapshot.
- Original source snapshots retain navigation/formatting limitations described above. Working navigation is repaired; wholesale source cleanup is neither necessary nor authorized.
- The thesaurus Markdown has not received a full Word-to-Markdown content comparison. Sample-level checking should accompany actual consequential lookups.
- `GLOSSARY.md` remains a valid empty template, while unresolved candidates appear in PROGRESS. Record evidence and scoped candidates during actual review rather than bulk-approving old proposals.
- The untracked Hezareh ZIP remains local. It was not unpacked, removed, or uploaded by this audit.

## F. Readiness verdict

**ready for translation work**

Use the declared `C00-S02-P03` continuation, beginning “Once this route was taken…”, with the surrounding C00-S02 argument and endnotes. Keep the archival gap explicit: readiness for a new mentoring session does not certify that P01/P02 are fully recoverable or approved. Historical-concept checks and doubtful lexical evidence must still be handled during the relevant translation decisions.

The remaining local corrections and this report have not been pushed to GitHub. No further reorganization is needed before returning to the mentoring workflow.
