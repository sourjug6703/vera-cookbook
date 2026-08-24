# Production batch 007

Batch 007 adds ten source-order recipes across `vera-r0041` through
`vera-r0051` from PDF pages 30–36. `vera-r0048` remains the reserved alias-only
position for the Perch, Pike, or Trout paprika-sauce cross-reference and was
not materialized as a recipe record. PDF page 35 is the SECOND section
directory rather than a recipe; `vera-r0051` on page 36 is the first complete
SECOND-section record.

## Trust result

Seven records were `source_checked` after a separate fresh direct local visual
source audit performed by AI. A later owner source decision classified the pale
page-32 overlaps in `vera-r0044`–`vera-r0046` as non-text artifacts, retaining
the source-clear printed words and punctuation. All ten records are now
`source_checked`; no AI audit is described as human verification.

The audit also confirmed the cross-page continuations for `vera-r0042` and
`vera-r0044`, the `vera-r0043` relationship to Roast pheasant, the reserved
alias ownership on page 33, and `vera-r0050` ownership of its `Sauce:`
subsection. Source forms such as `3·4`, `1·1/2`, `30·40`, `needed.Cook`, and
`Hand sauce separately.` remain verbatim.

The original machine candidates are retained under `machine-candidates/`.
Exact evidence under `evidence/production-batch-007/` includes six full-page
source images, 12 recipe-overview images, and 57 cited region crops with
decoded-pixel hashes and dimensions.

## Local reproduction

```sh
scripts/run_acceleration_wave_003.sh
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-007/spec.yaml --stage candidate
# Perform a separate fresh direct visual audit of every full page and cited region.
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-007/spec.yaml --stage audited --force
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

Marker processed the nine-page local acceleration wave with zero LLM requests,
errors, or tokens. No cookbook page was sent to a remote LLM or page service.
The Marker JSON SHA-256 is
`c10232fafe4421539ee717e5e42fe09364d62c3cec264c96aaaf0127ffbef90e`;
the metadata SHA-256 is
`5c4db9bfa0a002ae10688cf96e4380a2a0a9e4e7c570cf097bb17f70f968c1d2`.

The validator self-test passed, and all 49 production records passed schema,
trust, source-hash, evidence-pixel-hash, and crop-dimension checks. All ten
preserved snapshots remain `machine_candidate`.

The accessible local review page is `review/production-batch-007/index.html`.
Its ten click/tap **View source** controls were exercised at 1440×1000 and
390×844. Both layouts had no horizontal overflow; all disclosure targets
resolved; source controls were at least 52 pixels high and all interactive
controls at least 44 pixels high; all 148 references were local and present;
and the browser reported no console errors or warnings. The phone layout
reflowed to one column and kept expanded evidence inside the record card.
