# Preparation tools

- `organize.ps1`: rebuilds working chapter divisions from the original Markdown on Adel's Desktop. It writes to `translation-preparation/` and can overwrite those working files; do not run routinely or after manual changes without reviewing them.
  The generated map distinguishes structural units from practice chunks and recognizes the original bold subsection in C01. Standalone front-matter links target chapter files; the complete structured source retains its original internal anchors. Test regeneration in a separate temporary project directory before replacing working files.
- `test-dictionary.cjs`: validates the original LD2 file on Adel's Desktop and exports test samples to `archive/dictionary-test/`. The `--export-full` option regenerates the full glossary under `translation-references/aryanpour/`.

Both tools resolve output paths from this project's root regardless of the shell's current directory. Original Desktop inputs must still be available. Neither tool should alter uploaded files in `sources/`.
