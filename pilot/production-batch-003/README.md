# Production batch 003

This batch is the third governed production extraction cohort for `TASK-003`.
It contains the next five recipes in source order, `vera-r0009` through
`vera-r0013`, and spans PDF pages 11–13.

## Frozen boundary

The page range was frozen only after inspecting the surrounding scans. PDF page
10 is entirely the stuffing continuation owned by `vera-r0008`. PDF pages 11
and 12 each contain two complete recipes. PDF page 13 contains the fifth recipe,
“Pork roast,” followed by “Fresh ham in cream sauce,” which continues onto PDF
page 14 and is therefore excluded from this batch.

## Trust result

Four records are `source_checked` after a fresh direct visual source audit
performed by AI:

- `vera-r0009` — Veal chops with caraway seeds
- `vera-r0010` — Breaded veal chops
- `vera-r0012` — Veal goulash
- `vera-r0013` — Pork roast

The owner later classified `vera-r0011`’s outlined right-arrow ornament as
non-text decoration. Its readable note text is retained without a glyph
placeholder, and all five batch-003 records are now `source_checked`.

The audit corrected Marker's missing Czech diacritics and preserved the printed
centered-dot forms `2·3`, `3·4`, and `1·1/2`, along with the visible title
separators, fractions, inch marks, punctuation, temperatures, times, and yields.
Marker exposed the Breaded veal chops yield region geometrically even though its
HTML text candidate was empty; the direct source audit recovered and checked the
visible yield line.

## Local reproduction

```sh
scripts/run_production_batch_003.sh
.venv/bin/python scripts/build_production_batch_003.py --stage candidate
# Perform a separate direct visual audit of every full-page context and crop.
.venv/bin/python scripts/build_production_batch_003.py --stage audited --force
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

The OCR command uses only the local Marker pipeline. Marker metadata reports
zero LLM requests and zero LLM tokens for all three pages; no cookbook page was
sent to a remote model or service.

The generated local review page is
`review/production-batch-003/index.html`. Each record has a click/tap **View
source** control, exact cited-region disclosure, and an optional human review
checklist. The checklist is local browser state only and does not change the
canonical trust status.

Responsive QA passed at 1440×1000 and 390×844. Both widths had no horizontal
overflow; the disclosure control updated `aria-expanded` and its accessible
label; exact cited regions opened at phone width; and the page produced no
browser console errors.
