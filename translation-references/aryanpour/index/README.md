# Aryanpour — verified navigation index

**Dictionary:** Aryanpour English–Persian (user-supplied attribution, printed edition not independently verified)  
**Source:** Original structured Lingoes `.ld2` export, **not** OCR.  
**Entries:** 50,259 canonical records across **45** Markdown dictionary shards.  
**Index status:** Referential integrity validated against the frozen canonical export and all Markdown shards by the [GitHub Actions audit](https://github.com/mohamadadelfa-gif/Translation/actions/runs/38063140171). This does *not* establish printed-edition attribution, lexical correctness, or independently verified semantic senses.

## Complete master indexes

- [**headwords-master.csv**](headwords-master.csv) — complete English-headword to entry-ID and Markdown-location index. Best for human filtering or import into spreadsheet tools.
- [**headwords-master.jsonl**](headwords-master.jsonl) — equivalent complete index for machine/AI retrieval.
- [**SHARD-MAP.csv**](SHARD-MAP.csv) — all 45 Markdown shards, with first/last headword, row count and UTF-8 bytes.
- [**Canonical dictionary JSONL**](../aryanpour-english-persian.jsonl) — immutable source of record, **not** interchangeable with the headword index.
- [**Manifest and source hashes**](../manifest.json) — source identity and integrity.
- [**Source character issues**](../source-character-issues.json) — three known source defects, preserved verbatim.

**Schema for each navigation row:**
`headword, normalized_headword, entry_id, file, anchor, source_character_issue`

- `headword`: original source headword; never silently modify it.
- `normalized_headword`: NFKC + whitespace collapse + case-folding **for searching only**.
- `entry_id`: original frozen-export entry ID; primary lookup key; identical headwords can have distinct IDs.
- `file`: Markdown shard relative to `translation-references/aryanpour/`.
- `anchor`: in-file entry anchor. A web link can be formed from `../` + `file` + `#` + `anchor`.
- `source_character_issue`: `true` for records containing a known U+FFFD character defect.

## A–Z navigation

| Letter | Indexed entries | Dictionary shards |
|---|---:|---:|
| [A](A-headwords.csv) | 3,221 | 2 |
| [B](B-headwords.csv) | 2,453 | 2 |
| [C](C-headwords.csv) | 4,205 | 3 |
| [D](D-headwords.csv) | 2,774 | 2 |
| [E](E-headwords.csv) | 1,906 | 2 |
| [F](F-headwords.csv) | 2,299 | 2 |
| [G](G-headwords.csv) | 1,741 | 2 |
| [H](H-headwords.csv) | 1,957 | 2 |
| [I](I-headwords.csv) | 2,265 | 2 |
| [J](J-headwords.csv) | 463 | 1 |
| [K](K-headwords.csv) | 370 | 1 |
| [L](L-headwords.csv) | 1,936 | 2 |
| [M](M-headwords.csv) | 2,568 | 2 |
| [N](N-headwords.csv) | 859 | 1 |
| [O](O-headwords.csv) | 1,076 | 1 |
| [P](P-headwords.csv) | 4,392 | 3 |
| [Q](Q-headwords.csv) | 254 | 1 |
| [R](R-headwords.csv) | 2,401 | 2 |
| [S](S-headwords.csv) | 6,544 | 4 |
| [T](T-headwords.csv) | 3,016 | 2 |
| [U](U-headwords.csv) | 905 | 1 |
| [V](V-headwords.csv) | 911 | 1 |
| [W](W-headwords.csv) | 1,426 | 1 |
| [X](X-headwords.csv) | 38 | 1 |
| [Y](Y-headwords.csv) | 138 | 1 |
| [Z](Z-headwords.csv) | 141 | 1 |
| **TOTAL** | **50,259** | **45** |

The letter indexes above are navigation aids. Open the matching `file#anchor` to inspect the **whole** entry. Do not infer Persian equivalents solely from the index.

## Retrieval example

For `criterion`:

1. Open [C-headwords.csv](C-headwords.csv), or use the master CSV.
2. Locate the exact headword `criterion` and `entry_id = 9416`.
3. Follow [criterion — entry 9416](../dictionary/C/C-03.md#entry-9416-criterion).
4. Read the complete Persian definition *in context*. Any candidate interpretation remains distinct from an approved translation choice.

Alternatively, in a local checkout:

```powershell
python translation-references/aryanpour/tools/aryanpour_lookup.py "criterion"
```

## Validation and preservation

The last audited source export had SHA-256:
`d4394a34f65874a311177a5884360b15a02290d66e5fc5fbc4d8245d6ff3a919`.

No reconstructed OCR page numbers exist for this LD2 source. Neither indexes nor annotations should invent them.

Do not write inferred grammatical labels, sense boundaries, cross-references, spelling changes, or translation decisions back into the canonical export. The ongoing [annotation pilot](../pilot/README.md) stores provisional observations separately.

**Reproducibility:** the generated indexes and shards are derived from the canonical JSONL, and the [integrity auditor](../tools/audit_aryanpour.py) verifies the navigation references.
