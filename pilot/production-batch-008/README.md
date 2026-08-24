# Production batch 008

Batch 008 adds ten source-order recipes across `vera-r0052` through
`vera-r0061` from PDF pages 36–41. `vera-r0051` was read back unchanged to
confirm the page-36 boundary: its yield ends before `vera-r0052` Stuffed
peppers begins. `vera-r0061` Yeast dumplings owns its page-41 continuation;
`vera-r0062` Potato dumplings begins below it and is outside this batch.

## Trust result

All ten new records are `source_checked` after a separate fresh direct local
visual source audit performed by AI: `vera-r0052`, `vera-r0053`,
`vera-r0054`, `vera-r0055`, `vera-r0056`, `vera-r0057`, `vera-r0058`,
`vera-r0059`, `vera-r0060`, and `vera-r0061`. They are not human verified.
No batch-008 record remains `needs_attention`.

The audit resolved ownership of all layouts, ingredients, yields, and
continuations. `vera-r0059` owns its `Alternative:` paragraph. `vera-r0061`
owns the optional fried-bread-crumbs ingredient, its page-41 continuation, and
the source form `tablespoonsfuls`. Verbatim source forms including Czech
diacritics, centered-dot ranges, `parsely`, and `brownned` are retained.

The original `machine_candidate` snapshots are retained under
`machine-candidates/`. Exact evidence under `evidence/production-batch-008/`
includes six full-page source images, 11 recipe-overview images, and 56 cited
region crops with decoded-pixel hashes and dimensions. Marker did not identify
the source-clear left-column ingredient blocks for Sauerkraut and Country
gnocchi, so their candidate records preserve explicit local image-coordinate
rectangles; the raw local Marker output remains unchanged and the subsequent
visual audit verified both crops directly.

## Local reproduction

```sh
scripts/run_acceleration_wave_004.sh
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-008/spec.yaml --stage candidate
# Perform a separate fresh direct visual audit of every full page and cited region.
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-008/spec.yaml --stage audited --force
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

Marker processed the eight-page local acceleration wave with zero remote LLM
requests, page uploads, or remote extraction-service calls. The Marker JSON
SHA-256 is
`6a8f9802ace8a6193772230efac78f9729faacc98c115238f8663dd130152e40`;
the metadata SHA-256 is
`4890040a89962fc4094463089cac6ce3617fa7b7699e4cab2eecb4d9fbffbb86`.

The validator self-test passed, and all 59 production records passed schema,
trust, source-hash, evidence-pixel-hash, and crop-dimension checks. All ten
preserved batch-008 snapshots remain `machine_candidate`.

The accessible local review page is `review/production-batch-008/index.html`.
All 11 click/tap **View source** controls (the `vera-r0051` read-back plus the
ten new records) and their cited-region disclosures were exercised at
1440×1000 and 390×844. Both layouts had no horizontal or card overflow; all 72
local evidence images loaded; all source disclosures expanded and relabeled
correctly; and the browser reported no console warnings or errors. The phone
layout reflowed to one column and retained expanded evidence inside its record
card. Static verification also found 83 unique local references (155
`href`/`src` uses), with no remote or missing target.
