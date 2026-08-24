# Production batch 009

Batch 009 adds eleven source-order records, `vera-r0062` through `vera-r0072`,
from PDF pages 41–49. The page-41 Yeast dumplings continuation remains owned
by the previously completed `vera-r0061`; this batch begins with Potato
dumplings. The SECOND/THIRD section boundary is preserved: the two page-46/47
directories and Baking guidelines are not recipe records.

## Trust result

All eleven new records are `source_checked` after a separate fresh direct local
AI visual source audit, not human verification. Tripe soup’s literal page-43 to
44 continuation was followed. Wine soup and Beer soup use two separate,
source-audited coordinate crops from Marker’s merged list; Bohemian muffins has
its otherwise missed printed yield/time crop. Original `machine_candidate`
snapshots are preserved under `machine-candidates/` before promotion.

Evidence contains seven full-page source images, twelve recipe-overview images,
and 65 cited-region crops with decoded-pixel hashes and dimensions. The local
review page is `review/production-batch-009/index.html`.

## Local reproduction

```sh
scripts/run_acceleration_wave_005.sh
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-009/spec.yaml --stage candidate
# Perform the separate fresh direct local AI source audit.
.venv/bin/python scripts/build_production_batch.py --spec pilot/production-batch-009/spec.yaml --stage audited --force
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

Marker ran locally with no remote LLM, page upload, or remote extraction
service. Wave-005 Marker JSON SHA-256 is
`52c4d222a40eafbf25664a7030dfa5174a7e419c8c8350847bec6817aaf0720d`; its
metadata SHA-256 is
`cbb92c798a0648f810942568282cb857164558d5e77cc6ea83c8197029aec48d`.
