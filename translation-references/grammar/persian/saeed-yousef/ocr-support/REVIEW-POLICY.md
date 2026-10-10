# Review and source-fidelity policy

1. Preserve the original PDF/image, original raw UTF-8 output and its checksum. **Never silently rewrite source text.**
2. All automated issues are marked unverified_candidate even if severity is high. Severity represents review priority, not confidence of a correction.
3. Grammar supports plausibility checks; the **visual source** establishes exact spelling, characters, punctuation and reading order.
4. Keep an audit ledger: source ID, printed/PDF page and optional crop, raw span, proposed reading, reason, reviewer, date, state and any derivative change. Keep reversible raw and reviewed layers.
5. Distinguish source capture method: optical OCR, PDF embedded text-layer extraction, and editorial normalization. Do not conflate them.
6. Respect privacy and copyright when emitting sample snippets in issue reports or committing them to public GitHub.

## Decision states
- unverified_candidate: machine suspicion only
- visually_checked_confirmed: page/image comparison confirms a mismatch
- visually_checked_false_positive: page/image confirms the raw text is faithful
- deferred: source page not checked
- editorial_option: faithful source but potential modernized typography or style
- reviewed_change_applied: explicit approval recorded on a derived copy only

## One verified short example (not generalized)
PDF page 151, printed page 132, Chapter 9 §9.1 has a visually inspected example. A raw PDF text-layer extraction yielded an inverted word sequence. See VALIDATION-CASES.jsonl. This case **does not authorize automatically reversing other lines**.

## Required review steps
Verify source locator; examine page layout and reading direction; compare glyphs and morphology against the actual page; separate spelling/style modernization from extraction repair; record decision and reviewer; retain false-positive cases for precision measurement.
