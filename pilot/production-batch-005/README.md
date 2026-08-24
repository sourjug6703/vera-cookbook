# Production batch 005

Batch 005 contains ten contiguous source-order recipes, `vera-r0019` through
`vera-r0028`, from PDF pages 16–21.

## Trust result

Nine records are `source_checked` after a separate direct local visual source
audit performed by AI. A later owner source decision confirmed the blue
handwritten marginal word in `vera-r0025` as `Curry`, so all ten records are
now `source_checked`. They are not human verified by the AI audit.

The audit confirmed that `vera-r0021` is a complete cross-reference variation
with no printed ingredient list and no yield/time line. Data-contract v1.3
represents that source-authored absence as an empty outer ingredient-section
array plus a passing full-region presence audit; it does not copy ingredients
from the related lamb recipe. The audit also kept Chicken ragoût's lower
`or serve au gratin:` material inside `vera-r0026`, and treated the half-shell
preparation on the next page as the separate `vera-r0027` record.

The original machine candidates are retained under `machine-candidates/`.
Exact page-context images, 77 region crops, decoded-pixel hashes, and dimensions
are under `evidence/production-batch-005/`.

## Local reproduction

```sh
scripts/run_acceleration_wave_001.sh
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-005/spec.yaml --stage candidate
# Perform a separate direct visual audit of every full page and cited region.
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-005/spec.yaml --stage audited --force
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

Marker processed the 22-page acceleration wave locally with zero LLM requests,
errors, or tokens. No cookbook page was sent to a remote LLM or page service.

The accessible local review page is `review/production-batch-005/index.html`.
Its click/tap **View source** control was exercised for all ten records at
1440×1000 and again at 390×844. Both layouts had no horizontal overflow, all
controls had valid disclosure targets and a 52-pixel touch height, and the
browser reported no console errors or warnings.
