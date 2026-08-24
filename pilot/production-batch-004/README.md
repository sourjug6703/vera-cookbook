# Production batch 004

Batch 004 contains the next five contiguous source-order recipes,
`vera-r0014` through `vera-r0018`, from PDF pages 13–16.

## Trust result

All five records are `source_checked` after a separate direct local visual
source audit performed by AI. They are not human verified. No batch 004 record
has an open source ambiguity.

The direct audit corrected Marker’s hyphen-like OCR output to the cookbook’s
visible centered-dot forms, including `3·4`, `1·1/2`, `2·3`, `10·15`, and the
unusual `lightly·they`. It also preserved the page 13–14 continuation in Fresh
ham in cream sauce and split printed instruction paragraphs that Marker had
combined.

The original machine candidates are retained under `machine-candidates/`.
Exact page images, region crops, decoded-pixel hashes, and dimensions are under
`evidence/production-batch-004/`.

## Local reproduction

```sh
scripts/run_acceleration_wave_001.sh
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-004/spec.yaml --stage candidate
# Perform a separate direct visual audit of every full page and cited region.
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-004/spec.yaml --stage audited --force
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

Marker processed the 22-page acceleration wave locally with zero LLM requests,
errors, or tokens. No cookbook page was sent to a remote LLM or page service.

The accessible local review page is `review/production-batch-004/index.html`.
Its click/tap **View source** control was exercised at 1440×900 and 390×844.
Both layouts had no horizontal overflow, all five controls were present, the
52-pixel source control opened correctly, and the browser reported no console
errors or warnings.
