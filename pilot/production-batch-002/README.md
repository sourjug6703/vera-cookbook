# Production batch 002

This batch is the second governed production extraction cohort for `TASK-003`.
It contains the next five recipes in source order, `vera-r0004` through
`vera-r0008`, and spans PDF pages 6–10.

## Trust result

All five records are `source_checked` after a fresh direct visual source audit
performed by AI. They are not human verified. No batch 002 record has an open
source ambiguity.

The audit corrected OCR's treatment of several printed centered-dot forms,
including `1·1/2`, `3·4`, `2·3`, and `2·1/2`. These forms remain verbatim even
where they appear to function as ranges or mixed fractions.

`vera-r0008` includes the complete “Stuffings for veal breast” continuation on
PDF page 10. The three stuffing sections belong to that recipe and were not
counted as additional standalone recipes.

## Local reproduction

```sh
scripts/run_production_batch_002.sh
.venv/bin/python scripts/build_production_batch_002.py --stage candidate
# Perform a separate direct visual audit of every full-page context and crop.
.venv/bin/python scripts/build_production_batch_002.py --stage audited --force
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

The OCR command uses only the local Marker pipeline and sets no remote LLM.
Cookbook pages must not be sent to a remote service.

The generated local review page is
`review/production-batch-002/index.html`. Each record has a click/tap **View
source** control, exact cited-region disclosure, and an optional human review
checklist. The checklist is local browser state only and does not change the
canonical trust status.
