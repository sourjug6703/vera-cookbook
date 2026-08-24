# Production batch 006

Batch 006 adds nine source-order recipes across `vera-r0029` through
`vera-r0038` from PDF pages 22–29. Existing `vera-r0031` was read back for
source-order context without being overwritten. `vera-r0039` and `vera-r0040`
remain reserved alias-only positions and were not materialized as recipe
records.

## Trust result

All nine new records are `source_checked` after a separate fresh direct local
visual source audit performed by AI. They are not human verified. The audit
found no unresolved uncertainty in the nine records and confirmed:

- `vera-r0029` owns its Giblets, Chestnuts, Almond, and Raisins stuffing
  subsections, including the Chestnuts continuation from PDF page 22 to 23.
- `vera-r0030` owns its printed `Stuffing:` subsection.
- `vera-r0032` remains a complete source-authored recipe that cross-references
  `vera-r0031`.
- `vera-r0033` continues from PDF page 25 to 26.
- `vera-r0038` owns both the `Marinade:` and `Hare sauce:` ingredient sections;
  the following venison alias lines do not belong to that record.

The transcription preserves source forms such as `10·15`, `1·1/2`,
`top·of·range`, and `2 hours,plus marinating` rather than silently normalizing
them. No handwriting belongs to these nine records.

The original machine candidates are retained under `machine-candidates/`.
Exact evidence under `evidence/production-batch-006/` includes eight full-page
source images, 11 recipe-overview images, and 94 cited region crops with
decoded-pixel hashes and dimensions.

## Local reproduction

```sh
scripts/run_acceleration_wave_002.sh
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-006/spec.yaml --stage candidate
# Perform a separate fresh direct visual audit of every full page and cited region.
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-006/spec.yaml --stage audited --force
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

Marker processed the ten-page local acceleration wave with zero LLM requests,
errors, or tokens. No cookbook page was sent to a remote LLM or page service.
The Marker JSON SHA-256 is
`74b1b1c184c41d8dfba7b45f310f121c590a5cf7ff6c2e958c691c2abaeae9ca`;
the metadata SHA-256 is
`f34070280ac72128ba58ef799c0a816e4e0ebd3f23b4320a58e79606a944505d`.

The accessible local review page is `review/production-batch-006/index.html`.
Its ten click/tap **View source** controls, including the `vera-r0031`
read-back card, were exercised at 1440×1000 and 390×844. Both layouts had no
horizontal overflow; all disclosure targets resolved; source controls were 52
pixels high; all local image and YAML targets existed; and the browser reported
no console errors or warnings.
