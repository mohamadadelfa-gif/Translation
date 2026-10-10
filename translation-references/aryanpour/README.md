# Aryanpour model retrieval layer

This directory is a **derived lookup layer** for the Translation project. It is designed for reliable GitHub/LLM retrieval while keeping the existing Aryanpour exports as the canonical source.

## Canonical source

Keep these existing files unchanged in `translation-references/aryanpour/`:

- `aryanpour-english-persian.jsonl` — canonical machine-readable export
- `aryanpour-english-persian.txt` — readable full export
- `conversion-report.json` — extraction/encoding report
- `source-character-issues.json` — known source-character problems

The `dictionary/` and `index/` directories in this package are derived from those files. They do **not** replace the canonical JSONL.

## Routine interactive lookup

For an English headword such as `criterion`:

1. Open the letter index, e.g. `index/C-headwords.csv`.
2. Find the exact `headword` or `normalized_headword`.
3. Follow the `file` and `anchor`.
4. Read the complete entry in the referenced Markdown shard.
5. Attribute an equivalent to Aryanpour only after inspecting that entry.
6. If the entry cannot be retrieved or is inconclusive, report `Ariyanpour lookup incomplete/inconclusive`.
7. Compare consequential or uncertain vocabulary with Hezareh as required by `WORD-CHOICE-POLICY.md`.

Do not treat the first listed Persian equivalent as automatically correct. Context, register, specialist terminology, and the source author's argument govern selection.

## Files

- `dictionary/A/` ... `dictionary/Z/`: small Markdown shards containing readable entries.
- `index/A-headwords.csv` ... `index/Z-headwords.csv`: letter-level navigation.
- `index/headwords-master.csv`: complete navigation index.
- `index/headwords-master.jsonl`: compact machine navigation index.
- `index/SHARD-MAP.csv`: shard ranges and byte sizes.
- `qc/`: supplied conversion report, known character issues, and build validation.
- `manifest.json`: build provenance and integrity data.
- `tools/aryanpour_lookup.py`: local exact/prefix locator.
- `BUILD_RULES.md`: reproducibility and non-normalization rules.


## Entry standard and automated audit

- [ENTRY_STANDARD.md](ENTRY_STANDARD.md) defines the frozen-source entry contract, evidence hierarchy, and limits of semantic interpretation.
- [tools/audit_aryanpour.py](tools/audit_aryanpour.py) validates SHA-256 digests, all canonical entry IDs, dictionary projections, damaged-character records, navigation indexes, and readable Markdown shards.
- [tools/test_audit_aryanpour.py](tools/test_audit_aryanpour.py) provides synthetic regression tests.
- [Aryanpour dictionary integrity](../../.github/workflows/aryanpour-audit.yml) runs the tests and full-corpus read-only validation in GitHub Actions, and uploads the JSON report.

To repeat the full audit from the repository root:

```powershell
python translation-references/aryanpour/tools/audit_aryanpour.py --root translation-references/aryanpour --check-shards --output aryanpour-audit.json
```

Passing checks establish extraction/retrieval integrity; they do not verify the source's printed edition, lexicographic accuracy, or approval of translation equivalents.

## Reference-account locator

Use:

`Aryanpour — <headword> — Entry ID <id> — <file>#<anchor> — finding — effect on translation`

The locator points to the derived retrieval layer; the canonical JSONL remains the source of record.
