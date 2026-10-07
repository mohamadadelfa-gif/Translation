# Translation Progress — Live Dashboard

آخرین به‌روزرسانی: ۲۰۲۶-۱۰-۰۷

این فایل فقط وضعیت زندهٔ کار را نگه می‌دارد. تاریخچهٔ مفصل جلسات و checkpointهای قدیمی در `archive/progress/` نگه‌داری می‌شود.

## Current position

- **Chapter:** `C01` — Stephen Brockmann, *German Culture at the ‘Zero Hour’*
- **Translation unit:** `C01-S01`
- **Current Practice Chunk:** `C01-S01-P02`
- **Current stage:** **Preliminary analysis**
- **Approval:** هیچ متن C01 هنوز تأیید نشده است.
- **Active working source:** [translation-preparation/C01.md](translation-preparation/C01.md)
- **Saved learner checkpoint:** [drafts/C01/C01-S01-opening-draft-01.md](drafts/C01/C01-S01-opening-draft-01.md) — historical filename; its exact source coverage is now mapped to `C01-S01-P01`.
- **Saved preliminary mentor review:** [drafts/C01/C01-S01-opening-reviewed-01.md](drafts/C01/C01-S01-opening-reviewed-01.md) — historical filename; its exact source coverage is now mapped to `C01-S01-P01`.

## Practice Chunk boundaries

- **`C01-S01-P01` — 338 source words.** Starts with the Kristijana Gunnars epigraph (“We do not know what happens at Zero...”) and ends with: “Humanity shudders in horror at Germany!” said Thomas Mann.[^brockmann-2]
- **`C01-S01-P02` — 254 source words.** Starts with: “The elderly Mann, who had become the most powerful representative...” and ends with the Franz Werfel block quotation concluding: “...a few party bureaucrats and bums...”[^brockmann-3]
- These boundaries are encoded directly in [translation-preparation/C01.md](translation-preparation/C01.md) with non-source HTML comments. They preserve paragraph/quotation logic and are not part of the source text.
- Existing `C01-S01-opening-*` artifacts are retained without cosmetic renaming. The next new saved C01 artifact must use the canonical `C01-S01-P02-...` filename pattern.

## Current sentence under review

> The elderly Mann, who had become the most powerful representative of a better, more democratic Germany abroad during the years of Hitler’s Third Reich, was not the only intellectual to view Germany’s situation in such stark terms.

The saved learner checkpoint ends exactly at the end of `C01-S01-P01`. The sentence above is the first sentence of `C01-S01-P02`. Work on it has begun in chat but has **not yet been saved as a new P02 draft/review artifact**.

## Resolved terminology decisions

- **`special concentration camps` → «اردوگاه‌های مرگ» — approved by Adel, 2026-10-07, for C01-S01-P01.** The choice identifies the historical referent in the clause about Nazi mass exterminations. It does **not** mean `special = مرگ` generally; any later occurrence must be checked in its own historical context.

## Open translation questions

- `most powerful representative`: contextual Persian choice still open; do not treat «پرنفوذترین» as a documented dictionary equivalent without evidence.
- `representative of a better, more democratic Germany`: preserve the noun relation to **Germany**; avoid the ambiguous «آلمانی بهتر».
- `in such stark terms`: contextual phrase, not `terms = اصطلاحات`; tone and semantic-family choice still require contextual Persian judgment.
- Persian usage/syntax must receive the relevant Najafi control where a concrete construction question arises.
- Persian semantic-family and register choices should be checked against the approved فرهنگ طیفی and the surrounding translated sentences.
- Paragraph / Practice Chunk evidence gate remains open until the required source groups have explicit outcomes under `MENTOR_WORKFLOW.md`.

## Exact continuation

After the current sentence, the next source sentence is:

> In view of German crimes against humanity, the Austrian writer Franz Werfel, born in 1890 to a Jewish family but devoted to Catholicism himself, wrote a speech “To the German People,” which was published a week after Mann’s speech in the same edition of the Munich newspaper *Bayerische Landeszeitung* as news of the Holocaust itself.

Do not create a new saved checkpoint with the historical `opening` naming. When the next save is authorized, use `drafts/C01/C01-S01-P02-draft-01.md` and the corresponding reviewed/review-notes filenames.

## Active controls

- **Single workflow authority:** [MENTOR_WORKFLOW.md](MENTOR_WORKFLOW.md)
- **Operational entry rules:** [AGENTS.md](AGENTS.md)
- **Reference roles and retrieval routes:** [translation-references/SOURCE-REGISTER.md](translation-references/SOURCE-REGISTER.md)
- **Primary-source provenance:** [translation-references/SOURCE-PROVENANCE.md](translation-references/SOURCE-PROVENANCE.md)
- **Project terminology:** [translation-references/GLOSSARY.md](translation-references/GLOSSARY.md)
- **German concepts:** [translation-references/GERMAN-CONCEPTS.md](translation-references/GERMAN-CONCEPTS.md)
- **Draft organization:** chapter folders under `drafts/Cxx/`
- **Translation-craft corpus:** `translation-references/translation-craft/corpus/`
- **Structural validator:** `tools/audit_repository.py` + `.github/workflows/structural-audit.yml`

## Source / working-layer rule

`sources/` is a frozen snapshot of supplied repository material. Do not write new segmentation, mentor notes, or translation changes there.

All active book segmentation and working structural changes belong in `translation-preparation/`.

## Historical state

C00 body review reached its final paragraph, but C00 is **not approved as a whole** and older chunk boundaries/submissions remain partly unreconciled. Historical details, deferred research, and older checkpoints are preserved in:

[archive/progress/PROGRESS-2026-10-07-pre-dashboard.md](archive/progress/PROGRESS-2026-10-07-pre-dashboard.md)
