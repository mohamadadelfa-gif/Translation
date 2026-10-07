# Narrator Heading Recovery

The narrator headings were treated as structural metadata and checked separately from body OCR.

Notable OCR recoveries include:

- `دازل` -> `دارل` (obvious OCR error in the heading glyphs)
- `وردهن` / `ورتمن` -> `وردمن`
- `آزنستید` / `آزفستید` -> `آرمستید`
- PDF p. 11: `جوئل` was recovered from the visible page heading after body OCR omitted it.
- PDF p. 40: `تل` was recovered by visual inspection after body OCR omitted the heading.
- PDF p. 71: `تل` was recovered by visual inspection after body OCR omitted the heading.

These corrections affect headings/section boundaries only. Body prose was not silently rewritten to match a preferred spelling.
