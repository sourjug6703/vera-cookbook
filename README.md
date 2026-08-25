# vera-cookbook

## Start here

If this project feels confusing, run `aip atlas` to locate the AI Project Atlas, then read `BOARD.md` for the small set of things that matter now.

For an AI session, ask:

> Run the project doctor in read-only mode. If it finds a blocking manifest, path, secret, or Git problem, explain that first and do not load a possibly stale handoff. Otherwise validate PROJECT.yml, load its quick profile, and explain the current focus, blockers, live Git state, and safest next action without changing anything.

## What this project is

This project preserves every recipe in Vera Gaeta's scanned cookbook as a
granular, durable, source-grounded dataset. The immediate objective is highly
accurate extraction and a separate, source-backed AI audit. The current phase
also produces an optimized public reader for family cooks from the complete
cookbook collection.

## Boundaries

Use this project for:

- Preserving the original cookbook PDF as immutable evidence.
- Extracting bilingual recipe titles, ingredients, instructions, yields,
  preparation times, alternatives, notes, and cross-references.
- Evaluating OCR and document-layout tools against visually verified gold data.
- Producing versioned recipe records with exact PDF page and region provenance.

Do not use this project for:

- Treating machine-generated text as authoritative without a separate visual
  comparison to the cited source regions.
- Silently correcting, modernizing, translating, or normalizing the verbatim
  transcription.
- Sending cookbook pages to remote models or services without explicit
  approval.

## How to use or run it

1. Run `aip doctor` before loading project state.
2. Read `BOARD.md` for the current extraction or verification objective.
3. Keep source scans under `source/`; do not edit or replace them in place.
4. Run extraction candidates only through documented, reproducible pilot
   commands.
5. Promote text into canonical recipe records only after a distinct source
   audit against the cited page regions. Keep genuine ambiguities visible as
   `needs_attention`; never describe an AI audit as human verification.

### Local recipe reader

The first local reader is in `site/`. It is a dependency-free static site that
uses a generated derivative of source-checked records only. Regenerate its
browser data, then preview it locally:

```sh
ruby scripts/build_site_data.rb
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:4173/`. The reader supports source-order browsing,
recipe and ingredient search, local saved recipes, full preserved
transcriptions, and a reading-optimized source page for every source-checked
recipe. Each source page links to its untouched retained original scan. Its
browse groups follow cookbook order; they are not new canonical categories.
It is also the source for the public GitHub Pages release. Build the published
bundle with:

```sh
ruby scripts/build_public_site.rb
```

This writes an ignored `dist/` directory containing the reader, responsive
AVIF/WebP recipe studies, source-reader fallbacks, and original scans used by
the reader's existing source links. It deliberately excludes the larger
recipe-master PNGs, which are not needed for modern web delivery. The GitHub
Pages workflow publishes this generated bundle after a change to the reader.

## Canonical recipe format

Canonical recipes are human-readable UTF-8 YAML files under `data/recipes/`,
one file per stable recipe ID. They must validate against the versioned JSON
Schema in `schemas/recipe-record.schema.json` and the promotion rules enforced
by `scripts/validate_recipe_records.py`.

The format keeps immutable evidence, verbatim transcription, optional cooking
normalization, and source-audit evidence as separate layers. Future website
JSON, Schema.org Recipe data, search indexes, and databases are generated
derivatives; they do not replace the canonical YAML records or their cited scan
regions.

### Recipe context

Historical and cooking context lives separately in `context/`; it is not part
of a canonical recipe transcription. Each visible note must cite a source and
state that it describes the wider dish tradition, not the exact printed recipe.
The current registry covers all 110 materialized recipes with 14 registered
sources: 25 recipe-specific notes and 85 deliberately shared notes for closely
related dish families. This is reader-only derivative material; it does not
alter the canonical YAML, retained scans, or source-audit evidence.
Validate it with:

```sh
ruby scripts/validate_recipe_context.rb
```

Read `docs/RECIPE-DATA-CONTRACT.md` before creating or reviewing records. Run:

```sh
.venv/bin/python scripts/validate_recipe_records.py --self-test
.venv/bin/python scripts/validate_recipe_records.py
```

The thirteen production batches are documented under
`pilot/production-batch-001/`, `pilot/production-batch-002/`, and
`pilot/production-batch-003/`, `pilot/production-batch-004/`, and
`pilot/production-batch-005/`, `pilot/production-batch-006/`,
`pilot/production-batch-007/`, `pilot/production-batch-008/`,
`pilot/production-batch-009/`, `pilot/production-batch-010/`,
`pilot/production-batch-011/`, `pilot/production-batch-012/`, and
`pilot/production-batch-013/`, with local review pages under the matching
`review/` directories. All 110 production records are `source_checked`.
The project owner classified the outlined-arrow ornaments in `vera-r0001`,
`vera-r0011`, and `vera-r0077` as non-text decoration; confirmed the blue
handwritten `Curry` note in `vera-r0025`; excluded the pale page-32 overlaps in
`vera-r0044`–`vera-r0046` as non-text artifacts; and adopted the handwritten
`2 1/2` correction for `vera-r0110` Vanilla horns. The original evidence is
preserved alongside these decisions.
Every record exposes its page context and exact cited crops through a click/tap
**View source** control. Source pages replace the same central reader panel;
Back to recipe and Escape restore the selected transcription without losing
the reader state. Completing an optional browser checklist does not itself
change trust state or mutate canonical data.

The reconciled full inventory and thirteen-batch completion history are in
`docs/RECIPE-INVENTORY.md`. The cookbook contains 110 complete recipe/component
records, with three reserved alias-only source positions; no complete records
remain.

## Safety and external systems

- The project is local-only during extraction.
- Marker may run locally, but optional remote LLM services are out of scope
  unless explicitly approved.
- Store secret references only. Never store secret values here.

## Cross-platform notes

- Keep committed paths relative to the repository and use `/` inside `PROJECT.yml`.
- Put per-device clone roots and identity policy in trusted local configuration.
- Do not depend on symlinks for required control files.
- Record genuine platform differences here instead of copying an absolute user path.

## Project controls

`PROJECT.yml` is the machine-readable map. It selects the profile and maps logical roles such as board, plan, decisions, and registry to repository-relative paths.
