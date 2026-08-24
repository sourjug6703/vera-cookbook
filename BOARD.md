# vera-cookbook Board

Last reviewed: 2026-08-24.

## North Star

Faithfully preserve every recipe in Vera Gaeta's scanned cookbook as a
versioned, source-checked, future-proof dataset with exact source provenance.
Keep the audit status honest about whether review was performed by AI or a
human, and keep the records suitable for a separately approved,
publication-safe cookbook reader.

## Now

- No active implementation task. `TASK-004` is complete as a local family-cook
  reader; do not enable GitHub Pages or publish without separate approval.

## Next

- `TASK-005` (not started): before any separately approved hosting decision,
  benchmark delivery copies: responsive AVIF/WebP recipe illustrations and
  lossless WebP reader scans with grayscale-PNG fallback. Keep original scans
  and canonical YAML untouched; keep the reader local without approval.

## Completed

- [x] `TASK-004` Completed and locally reviewed the dependency-free static
  family recipe reader. It presents all 110 source-checked records with
  source-order browsing, recipe and ingredient search, local saved recipes,
  full transcriptions, an exact source-proof path, and 110 local recipe
  illustrations in the approved Family Recipe Issue language. Source pages
  use a grayscale, deskewed reading copy and link to untouched scans. The
  family-cook pass made saving available from transcription, clarified an
  empty saved list, restored dialog focus, and kept the narrow mobile header
  usable. No hosting or public publication was enabled.
- [x] `TASK-002` Finalized the versioned YAML/JSON recipe-record schema, source-region provenance model, visual verification contract, promotion validator, and tested example fixture.
- [x] `TASK-001` Ran a reproducible 15-page Marker bake-off against an independently verified visual gold set. Adopt Marker as the local first-pass OCR/layout engine, with geometry-aware recipe segmentation and a separate visual source audit required before canonical promotion.
- [x] `TASK-003` Completed the source-audit gate for all 110 materialized
  cookbook records; genuine source ambiguities remain explicit rather than
  guessed.

## Waiting or blocked

- None. Human review is no longer a prerequisite; genuine source ambiguities must remain explicitly flagged rather than guessed.

## Current production result

- Batch 001: all five records are `source_checked`; the owner classified `vera-r0001`’s outlined arrow as non-text decoration.
- Batch 002: `vera-r0004` through `vera-r0008` are all `source_checked` by an AI source audit; none has an open issue.
- Batch 003: all five records are `source_checked`; the owner classified `vera-r0011`’s outlined arrow as non-text decoration.
- Batch 004: `vera-r0014` through `vera-r0018` are all `source_checked` by an AI source audit; none has an open issue. Machine-candidate snapshots were retained before promotion.
- Batch 005: all ten records are `source_checked`; the owner confirmed `vera-r0025`’s blue handwritten marginal word as `Curry`. Machine-candidate snapshots were retained before promotion.
- Batch 006: the nine new records across `vera-r0029` through `vera-r0038` are all `source_checked` by a fresh direct local AI source audit. Existing `vera-r0031` was read back unchanged; reserved alias-only positions `vera-r0039` and `vera-r0040` were not materialized. Machine-candidate snapshots were retained before promotion.
- Batch 007: all ten new records are `source_checked`; the owner classified the pale marks in `vera-r0044`–`vera-r0046` as non-text artifacts. Reserved alias-only `vera-r0048` was not materialized, and the FIRST/SECOND section boundary was preserved. Machine-candidate snapshots were retained before promotion.
- Batch 008: all ten new records across `vera-r0052` through `vera-r0061` are `source_checked` by a fresh direct local AI source audit. `vera-r0051` was read back unchanged for the page-36 boundary, and `vera-r0061` owns its page-41 continuation; no batch-008 record needs attention. Machine-candidate snapshots were retained before promotion.
- Batch 009: all eleven new records across `vera-r0062` through `vera-r0072` are `source_checked` by a fresh direct local AI source audit; the SECOND/THIRD boundary, Tripe soup continuation, and split Wine/Beer soup ingredient ownership are preserved. Machine-candidate snapshots were retained before promotion.
- Batch 010: all ten new records are `source_checked`; the owner classified `vera-r0077`’s ornament as non-text decoration. Existing `vera-r0079` was read back unchanged and Czech doughnuts owns its continuation. Machine-candidate snapshots were retained before promotion.
- Batch 011 and 012: all twenty new records across `vera-r0084` through `vera-r0103` are `source_checked` by fresh direct local AI source audits; the empty Easter braid ingredient array and the composite fritter-family ownership are preserved. Machine-candidate snapshots were retained before promotion.
- Batch 013: all ten new records are `source_checked`; the owner adopted `vera-r0110`’s handwritten `2 1/2` flour correction. Machine-candidate snapshots were retained before promotion.
- Full inventory: all 110 complete recipe/component records through `vera-r0113` exist, plus three reserved alias-only source positions. All 110 are `source_checked`; no complete records or source-policy decisions remain.

## Operating guardrails

- Treat the first Now item as the current objective.
- Keep one current objective and no more than three Now items.
- Link task IDs to `PLAN.md` when a Plan exists.
- Move durable choices to the Decisions role.
- Move historical work to unique session records.
- Put project-specific safety and approval limits here only when they affect current work.
- Treat the source PDF as immutable evidence.
- Treat Marker, OCR, parser, and model outputs as rebuildable candidates, never authoritative recipe text.
- Require page and region provenance plus a distinct source audit before promoting any transcription.
- Never label an AI source audit as human verification.
- Do not send the cookbook to a remote model or service without explicit approval.
