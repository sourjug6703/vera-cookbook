# Recipe data contract v1.3

## Decision

The canonical recipe collection is one UTF-8 YAML file per recipe, validated
against `schemas/recipe-record.schema.json`. YAML is the human-review surface;
JSON is an equivalent interchange representation. Generated website JSON,
Schema.org `Recipe`, search indexes, databases, and normalized cooking fields
are derivatives, not the authority.

The contract separates three layers:

1. **Evidence:** the immutable PDF hash and exact page regions.
2. **Transcription:** verbatim titles, ingredient lines, instructions,
   yield/time lines, notes, and cross-references.
3. **Derivation:** optional normalized quantities, units, ingredient names,
   measurements, slugs, and later publication fields.

No derived value may overwrite or repair `text_verbatim`. A correction changes
the transcription, increments `record_revision`, and receives new visual-audit
evidence.

## Stable identity and files

- Store canonical records as `data/recipes/<recipe_id>.yaml`.
- Assign an opaque, stable `recipe_id`; never derive identity from a title or
  slug that may later be corrected.
- Preserve the complete bilingual title line, including the printed separator
  and quotation marks, in `identity.display_title`; keep language-specific
  title components alongside it for search and display.
- Keep `schema_version` independent from `record_revision`.
- Use one-based `pdf_page` values. Preserve printed page labels separately.
- Keep all paths repository-relative and all timestamps in ISO 8601 UTC.

## Source regions

Every transcribed segment cites one or more `source_region_ids`. A region stores
the page, role, coordinate system, polygon, and optional Marker block IDs. Its
coordinates are evidence for ownership and reading order, not merely display
metadata.

Use the smallest region that contains the complete visible text. When a line
wraps, one region may contain the full line. When a segment crosses regions or
pages, cite all of them in reading order and record a continuation relationship.
Region crops are rebuildable; when retained, hash decoded pixels plus dimensions
rather than encoded PNG bytes.

## Transcription rules

- Preserve spelling, capitalization, punctuation, units, fractions, unusual
  wording, and Czech diacritics exactly as printed.
- Do not modernize, translate, infer missing text, expand abbreviations, or
  repair probable errors inside `text_verbatim`.
- Preserve each printed ingredient line as its own segment.
- When the complete source context genuinely prints no ingredient list, use an
  empty `ingredient_sections` array under schema version `1.3.0`; do not infer
  ingredients from the instructions or a related recipe. Empty means a
  confirmed source-authored absence, never an extraction failure or unknown
  state. Keep the outer array empty; an ingredient section with an empty
  `ingredients` array remains invalid. Promotion requires a passing
  `ingredient_list_presence` check targeting the recipe ID and covering every
  declared source region.
- Preserve instruction paragraphs as ordered steps without silently splitting
  or combining sentences.
- Preserve yield/preparation-time lines separately, including genuine absence.
- Preserve alternatives, notes, and cross-references instead of folding them
  into normalized instructions.
- Record illegible or ambiguous text in `uncertainties`; a record with an open
  uncertainty cannot be promoted to `source_checked` or a human-verification
  state.

## Derived normalization

Normalized fields are optional and explicitly non-authoritative. Quantities use
strings, not binary floating-point numbers. Examples are `"3/4"`, `"1.5"`, or
the range `quantity_min: "5"` and `quantity_max: "6"`. Keep the printed form in
`quantity_text` and the whole ingredient line in `text_verbatim`.

Normalization can support search, scaling, shopping lists, accessibility, and
future Schema.org export. It must not be used to judge transcription accuracy.

## Source-audit and human-verification contract

Only direct visual comparison with the immutable source can promote a record.
Marker and other machine output can propose text and regions but cannot approve
their own output.

For every recipe, an auditor must pass:

- complete region coverage;
- recipe boundaries;
- ingredient ownership when ingredient lines are present, or confirmed absence
  of any printed ingredient list when none is present;
- instruction ownership;
- exact transcription of every authoritative segment;
- every numeric token, fraction, unit, time, and temperature;
- presence or confirmed absence of yield/preparation-time text; and
- repeated-text occurrence counts.

Audit Czech diacritics whenever non-ASCII letters occur. Audit continuations
for multi-page recipes and cross-references whenever they appear. A failed or
ambiguous check, an uncovered segment, or any open issue blocks promotion.

Every audit check records `performed_by: ai` or `performed_by: human`, plus an
`auditor_id` and `audited_at` timestamp. `source_checked` is reserved for a
complete direct visual source audit performed by AI. It is not human
verification. `human_verified` requires the complete promotion evidence to be
performed by a human. `human_verified_two_person` additionally requires two
distinct human auditors to inspect every authoritative segment independently.

The top-level `audit_policy` makes the intended evidence explicit:
`source_audit`, `human_single`, or `human_double`. Earlier AI checks may remain
in a later human-verified record as history, but they do not satisfy a human
promotion gate.

## Promotion states

- `machine_candidate`: extracted but not visually reviewed.
- `source_checked`: all applicable direct visual checks pass under an AI source
  audit, with no open issue or transcription uncertainty. This state must never
  be described as human verification.
- `needs_attention`: an AI or human audit found a failed or ambiguous check, an
  open issue, or a transcription uncertainty. Preserve the exact unresolved
  point; do not guess or silently normalize it.
- `human_verified`: all applicable checks pass with direct visual evidence from
  one human auditor.
- `human_verified_two_person`: all applicable checks pass with independent
  coverage from two distinct human auditors.
- `rejected`: the candidate record is unusable and must be rebuilt.

The validator enforces the schema, ID/reference integrity, source-page coverage,
auditor identity type, and promotion rules. It deliberately cannot decide
whether the visible transcription is true; that requires the direct visual
source audit represented by the checks.

## Local validation

Install the pinned data-contract dependencies in the project environment:

```sh
uv pip install --python .venv/bin/python -r requirements-data.txt
```

Validate all canonical records:

```sh
.venv/bin/python scripts/validate_recipe_records.py
```

Run the contract self-test and validate the example fixture:

```sh
.venv/bin/python scripts/validate_recipe_records.py --self-test
```

## Publication boundary

A future website may consume `source_checked`, `human_verified`, or
`human_verified_two_person` records, while displaying the trust state and source
evidence honestly. It must exclude `machine_candidate` and `needs_attention`
records from publication-ready output. It may generate Schema.org `Recipe`
JSON-LD, display-unit conversions, search facets, or translations, but those
outputs must link back to the stable `recipe_id` and must never be written over
the canonical transcription.
