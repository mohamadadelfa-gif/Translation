# Repository Structural Audit — 2026-10-07

**Repository:** `mohamadadelfa-gif/Translation`  
**Branch:** `master`  
**Audited head:** `99532e15ca9398a9466bc555e3ce47cbb997e602`  
**Purpose:** verify repository architecture after the 2026-10-07 structural cleanup before further translation-state mutations.

This audit is deliberately broader than a single-file edit. It checks authority, source provenance, working-layer separation, path integrity, draft/approval state, reference subsystems, corpus consistency, and tool reproducibility.

## Audit method

The audit inspected the recursive Git tree and the active control documents, then checked the current working-state paths and reference subsystem layouts.

Repository snapshot at audit:

- 834 tracked files
- 114 directories
- 562 Markdown files
- 189 CSV files
- 51 JSON/JSONL files
- 6 Python files
- 13 active control/readme documents checked for clickable internal Markdown links
- 62 internal clickable links checked
- 0 broken clickable links

The audit also checked:

- current draft paths and naming patterns;
- current approved-translation state;
- cross-layer identical blobs between `sources/` and `translation-preparation/`;
- translation-craft corpus path integrity;
- reference subsystem presence of README/index/QC/tool layers;
- hard-coded external/local dependencies in repository tools.

## Severity model

- **P0 — structural blocker:** can invalidate provenance, authority, or the state machine.
- **P1 — high priority:** likely to cause drift, failed retrieval, or non-reproducible work.
- **P2 — maintenance:** does not currently block translation but should be normalized before scale increases.

---

# Findings

## P0-1 — Primary book source provenance is incomplete inside the repository

**Status:** FAIL

The tracked `sources/` tree does not contain the original *Revisiting Zero Hour 1945* PDF.

The repository does contain:

- `sources/revisiting-zero-hour-1945-structured.md`
- `sources/C00.md` through `sources/C05.md`
- `sources/front-matter.md`

The front matter identifies the Markdown as:

> `Structured Markdown converted from the supplied PDF`

The structured Markdown also contains project/editorial markers such as:

> `<!-- translation-preparation: added unit heading -->`

Therefore the repository can currently preserve the **supplied structured snapshot**, but it cannot independently verify that structured text against the original book PDF from repository-held evidence.

This matters because Adel has now defined:

> `sources/` = exact supplied material, preserved untouched.

### Required remediation

Preferred:

1. add the original supplied book PDF unchanged under `sources/` (or a clearly named `sources/book/` subdirectory);
2. record its checksum and provenance;
3. identify the PDF as the canonical visual/source authority;
4. classify the structured Markdown and chapter splits as derived/source-access representations, not substitutes for the original PDF.

If the PDF cannot be tracked in Git, record that limitation explicitly with an immutable checksum/provenance manifest and mark visual verification as externally dependent.

Do **not** rewrite the existing frozen source snapshots to make them look pristine.

---

## P0-2 — Active workflow contains real stale dependencies

**Status:** FAIL

Two concrete wiring defects were verified in `MENTOR_WORKFLOW.md`:

1. it references `translation-references/TRANSLATION-PROFILE.md`, but that file does not exist in the current tree;
2. it refers to `tools/najafi_lookup.py`, but the actual tracked tool is:

   `translation-references/najafi/tools/najafi_lookup.py`

These are not stylistic issues; they can make a session-entry or reference-check route fail.

### Required remediation

- Decide whether `TRANSLATION-PROFILE.md` is genuinely needed.
  - If not, remove the ghost dependency.
  - If a separate translation-style profile is genuinely required, define its unique role so it does not duplicate `MENTOR_WORKFLOW.md`.
- Correct the Najafi tool path in the authoritative workflow.
- Run the structural validator proposed in P1-4 after the fix.

---

## P0-3 — Declared Practice Chunk state is not instantiated in active C01 work

**Status:** FAIL

The authoritative hierarchy is:

`Chapter → Translation Unit → Practice Chunk → Sentence`

New work is supposed to use IDs such as:

`C01-S01-P01`

However:

- current progress is at `C01-S01`;
- the current saved files are:
  - `drafts/C01/C01-S01-opening-draft-01.md`
  - `drafts/C01/C01-S01-opening-reviewed-01.md`
- no exact `C01-S01-P01` boundary is recorded;
- all 11 existing draft artifacts are historical/nonconforming with the new `Pxx` file pattern.

Historical C00 files do not need cosmetic renaming. The structural problem is **continuing new C01 work without establishing the first Practice Chunk boundary**.

### Required remediation

Before the next substantial C01 save:

1. inspect `translation-preparation/C01.md`;
2. establish the exact start/end boundary for `C01-S01-P01` using paragraph/argument logic;
3. record that boundary in `PROGRESS.md`;
4. preserve the existing `C01-S01-opening-*` files as historical checkpoint artifacts;
5. start subsequent saved work with the canonical `C01-S01-P01-...` naming scheme.

---

## P1-1 — Single workflow authority is declared but not yet fully enforced

**Status:** PARTIAL

The repository now correctly declares `MENTOR_WORKFLOW.md` as the single workflow authority.

However, operational logic is still duplicated in other active documents.

### `AGENTS.md`

It still contains detailed Hezareh lookup semantics, evidence-status rules, and Ashouri verification rules that substantially overlap with `MENTOR_WORKFLOW.md` and `SOURCE-REGISTER.md`.

### `SOURCE-REGISTER.md`

Sections 13–18 contain:

- evidence discipline;
- reference-use rules;
- source-selection principles;
- practical lookup sequences;
- final workflow-like rules.

These are useful rules, but they overlap with the authoritative workflow and therefore remain a drift surface.

### Required remediation

Refactor roles:

- `MENTOR_WORKFLOW.md` — **how the translation/review process runs**;
- `SOURCE-REGISTER.md` — **what each source is, where it lives, how its evidence is retrieved, and its limitations**;
- `AGENTS.md` — **short operational entrypoint and non-negotiable repository rules**;
- `WORD-CHOICE-POLICY.md` — compatibility pointer only, as now intended.

Do not delete useful evidence instructions; move or consolidate them so each rule has one authoritative home.

---

## P1-2 — Derived working layers are not reproducible from repository-held inputs

**Status:** FAIL / external dependency

Two active tools contain hard-coded local dependencies:

### `tools/organize.ps1`

Hard-coded input:

`C:\Users\Adel\Desktop\revisiting-zero-hour-1945.md`

The required unsegmented input is not tracked in the repository.

### `tools/test-dictionary.cjs`

Hard-coded input:

`C:/Users/Adel/Desktop/Ariyan Pour Dictionary/Generic English-Persian Dictionary.ld2`

The LD2 source is not tracked in the repository.

This means a fresh machine cannot deterministically rebuild these derived layers from the repository alone.

### Required remediation

For each tool:

1. replace hard-coded source paths with explicit parameters/configuration;
2. document whether the source is repository-held or external;
3. store expected source checksum(s);
4. fail clearly when the required external source is absent;
5. never silently regenerate over manually reviewed working files;
6. ideally support a `--check` or dry-run mode.

For the book preparation tool, prefer a tracked canonical input if the original source can legally/practically be stored.

---

## P1-3 — Approval layout does not mirror the chapter-organized draft layout

**Status:** OPEN DESIGN DECISION

Drafts are now organized as:

`drafts/C00/`, `drafts/C01/`, ...

But `approved-translations/README.md` still specifies flat output such as:

`approved-translations/C00-S02-P01-approved.md`

There are currently no approved translation files, so this is the ideal time to decide the permanent layout.

### Recommended remediation

Mirror chapter organization:

`approved-translations/C01/C01-S01-P01-approved.md`

This preserves symmetry:

`drafts/C01/... → approved-translations/C01/...`

Do this before the first approved file is created.

---

## P1-4 — No automated repository-structure validator exists

**Status:** FAIL

The repository has specialized validation for the translation-craft corpus, but no repository-wide guardrail checks the architecture that this audit just had to inspect manually.

### Recommended validator

Add a read-only `tools/audit_repository.py` that checks at minimum:

- required control files exist;
- forbidden/ghost control dependencies do not exist;
- active control Markdown links resolve;
- no old `translation-preparation/translation-craft-corpus/` paths remain;
- draft files are chapter-scoped;
- new draft filenames follow the `Cxx-Sxx-Pxx-...` convention;
- approved files, once present, follow the chosen approval layout;
- `PROGRESS.md` points to existing active files;
- the current Practice Chunk ID/boundaries are declared;
- reference lookup tool paths exist;
- translation-craft alignment paths resolve;
- no temporary/cache files are tracked;
- source snapshots are not accidentally replaced by derived working outputs.

Run it before structural commits and optionally in CI.

---

## P1-5 — Source/preparation duplication is intentional but needs an immutable baseline rule

**Status:** PASS WITH RISK

Seven current files are byte-identical across the frozen and working layers:

- C00
- C01
- C02
- C03
- C04
- C05
- complete structured book Markdown

This is not itself a defect now that the roles are explicit:

- `sources/` = frozen snapshot;
- `translation-preparation/` = active working layer.

The risk is future accidental reverse synchronization.

### Recommended remediation

Record baseline source blob/checksum metadata and make the repository validator fail if a workflow tool attempts to treat `sources/` as an output destination.

No cosmetic deduplication is required.

---

## P2-1 — Existing source snapshots already contain earlier editorial markers

**Status:** DOCUMENTED LIMITATION

The initial repository commit already contained source-side Markdown with project-style translation-unit markers.

Because Adel chose the rule “exact supplied material, untouched,” those snapshots should remain frozen exactly as received in the repository rather than retroactively cleaned.

The architectural distinction must therefore be:

- **frozen supplied repository snapshot** — what is currently under `sources/`;
- **original visual authority** — the original source document when available;
- **active working layer** — `translation-preparation/`.

Do not call the structured Markdown “pristine original text” merely because it is under `sources/`.

---

## P2-2 — Historical draft names remain nonconforming

**Status:** ACCEPTED HISTORICAL STATE

All 11 current draft artifacts predate or bypass the new `Pxx` naming convention.

This is acceptable for historical artifacts, provided:

- they are not silently renamed merely for cosmetic consistency;
- new C01 work begins using an established Practice Chunk ID;
- historical files are clearly treated as checkpoints rather than examples for new naming.

No bulk rename is recommended.

---

# Verified passes

## PASS — Active Markdown link integrity

Checked 62 internal clickable Markdown links across 13 active control/readme documents.

**Broken clickable links: 0**

This does not excuse the stale code-path dependencies identified in P0-2, because those are written as operational paths rather than Markdown links.

## PASS — Translation-craft corpus relocation

Current corpus location:

`translation-references/translation-craft/corpus/`

- 139 corpus files tracked at the new location;
- no files remain under the old `translation-preparation/translation-craft-corpus/` tree;
- 59 English/Persian section pairs;
- 118 referenced section files checked structurally;
- 0 missing referenced section files.

The checksum validator was not executed as part of this GitHub-connector audit; structural path resolution was verified.

## PASS — Reference subsystem structure

The following active reference systems have identifiable retrieval/documentation layers:

- Ariyanpour — README, manifest, index, shards, QC, lookup tool;
- Hezareh — README, manifest, index, shards, QC, lookup tool;
- Ashouri — README(s), per-letter indexes, extensive QC;
- Najafi — README, manifest, indexes, QC, lookup tool;
- Persian thesaurus — README, manifest, semantic indexes, QC, lookup tool;
- Academy orthography — README and structured sections;
- Huddleston/Pullum/Reynolds grammar layer — README and chapter map;
- Daryabandari/Faulkner translation-craft — corpus plus analytical layer.

No conclusion about lexical correctness follows merely from this structural pass.

## PASS — Repository hygiene

No tracked `__pycache__`, `.DS_Store`, `Thumbs.db`, obvious temporary backup files, or similar junk patterns were found.

## PASS — Approval integrity

`approved-translations/` currently contains only its README.

No unapproved translation text is present there.

## PASS — Progress/history separation

`PROGRESS.md` is now a live dashboard.

The previous long-form progress record is preserved under:

`archive/progress/PROGRESS-2026-10-07-pre-dashboard.md`

## PASS — Legacy word-choice policy preservation

The old standalone policy is archived under:

`archive/policies/WORD-CHOICE-POLICY-2026-10-07-legacy.md`

The active `WORD-CHOICE-POLICY.md` is now a compatibility pointer rather than an independent authority.

---

# Remediation order

Do not resume normal structural editing in arbitrary order.

## Batch A — restore architectural correctness

1. Resolve the primary-book source provenance gap.
2. Remove/resolve the nonexistent `TRANSLATION-PROFILE.md` dependency.
3. Correct the Najafi lookup-tool path.
4. Establish `C01-S01-P01` exact boundaries and record them in the live dashboard.
5. Decide and document the chapter-based layout for future approved translations.

## Batch B — eliminate drift surfaces

6. Slim `AGENTS.md` to operational rules.
7. Refactor workflow-like material out of `SOURCE-REGISTER.md` into the single authoritative workflow while preserving source-specific retrieval facts.
8. Keep `WORD-CHOICE-POLICY.md` as a compatibility pointer only.

## Batch C — make the structure enforceable

9. Parameterize local-only tools and document external inputs/checksums.
10. Add `tools/audit_repository.py`.
11. Run the structural validator.
12. Only after the validator passes, resume routine C01 translation and save new work using the established `Pxx` chunk structure.

---

# Audit conclusion

The repository is **materially improved but not yet structurally closed**.

The folder move itself succeeded, but the audit found three blockers that should be resolved before treating the architecture as stable:

1. primary book provenance is incomplete inside the repo;
2. the authoritative workflow contains stale/nonexistent paths;
3. the active C01 work has not yet entered the declared Practice Chunk state machine.

The correct next move is therefore **Batch A as one coherent repair set**, followed by a repository validator, not another isolated wording or path edit.
