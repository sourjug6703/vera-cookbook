# Production batch 001

## Outcome

This batch contains five schema-valid recipe records backed by 37 clean source
regions from PDF pages 4, 5, 24, 25, and 52. A fresh direct visual source audit
performed locally by AI promoted four records to `source_checked`. A later
owner source decision classified `vera-r0001`’s outlined arrow as non-text
decoration, so all five records are now `source_checked`. No AI audit is
described as human verification.

The batch intentionally exercises the failure modes found in the Marker
bake-off:

- mixed fractions and temperatures;
- two recipes sharing one page;
- ingredient blocks emitted before their owning title;
- an OCR-omitted yield/preparation-time line;
- a recipe continuing across pages; and
- bilingual titles with Czech diacritics and different printed separators.

## Schema finding

The first production records exposed one data-contract gap. Separate English
and Czech title components did not preserve the punctuation of the complete
printed title line. Recipe schema v1.1 added the required
`identity.display_title` segment while retaining searchable language-specific
titles. Schema v1.2 separates AI `source_checked` evidence from genuine
`human_verified` states and records `performed_by`, `auditor_id`, and
`audited_at` on every audit check.

## Reproduce

Run the frozen local Marker cohort:

```sh
scripts/run_production_batch_001.sh
```

Rebuild records, evidence crops, and the review packet from the frozen audited
specification:

```sh
.venv/bin/python scripts/build_production_batch_001.py
```

The builder refuses to overwrite existing recipe files unless `--force` is
given. Use `--force` only when intentionally regenerating this frozen batch from
the audited specification; later manual changes must first be incorporated into
that specification.

Validate records, source identity, source references, and decoded-pixel crop
hashes:

```sh
.venv/bin/python scripts/validate_recipe_records.py
```

## Audit and human-verification boundary

Open `review/production-batch-001/index.html` and use each click/tap **View
source** control to expose page context and exact cited regions. The current AI
audit is recorded in canonical YAML. Browser checkboxes are an optional human
verification aid only; they do not mutate canonical YAML or change trust state.

Only direct visual checks recorded with `performed_by: human` may promote a
record to `human_verified` or `human_verified_two_person`. AI audit evidence
must never be relabeled as human verification.
