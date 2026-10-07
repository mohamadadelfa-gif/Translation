# Hezareh Profile v2 Package Audit — 2026-10-07

User-supplied package: `index.zip`

## Package identity

- SHA-256: `962aef1ee970ef6c54edc1cb93eaf618a92e6f636efc1fa75edc6f63846dad8a`
- Bytes: `9,438,236`
- Indexed records: `38,957`
- Dictionary shards: `174`
- `visually_checked`: `186`
- `raw_ocr`: `38,771`
- v2 revision blocks present: `38,098`
- records without a v2 revision block: `859`

## Comparison with current repository layer

The lexical/index inventory is not materially newer:

- record count remains exactly `38,957`;
- record IDs, verification states, boundary-confidence states, source pointers, and shard routing remain compatible;
- the apparent CSV-size increase is primarily CRLF-vs-LF line-ending churn;
- no exact `powerful` entry is added;
- no exact `shudder` entry is added.

The material improvement is in the dictionary shards. The package adds marked blocks of the form:

`HEZAREH-PROFILE-REVISION-V2`

These blocks:

- preserve the original extraction;
- add a machine-revised reading;
- separate grammar/context labels where detected;
- record unresolved source checks;
- explicitly state that no new visual verification occurred;
- keep human review pending.

Therefore the v2 block is **supplementary interpretation**, not stronger lexical evidence and not a replacement for the original `Source text`, `verification_status`, or `boundary_confidence`.

## Import policy

Do not replace the current index merely for line-ending changes.

Do not silently overwrite the preserved original extraction.

For records actively used in translation, import the useful v2 annotation into a separate overlay keyed by Hezareh `record_id`. When a v2 overlay exists:

1. inspect the normal index row;
2. inspect the original shard record and `Source text`;
3. inspect the v2 overlay;
4. retain the inherited evidence status;
5. if the v2 block says source check/human review is pending, do not promote the wording to visually checked or approved evidence.

Current imported overlay:

`translation-references/hezareh/revisions-v2/C01-active-records.md`
