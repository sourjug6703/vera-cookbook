# Marker bake-off v1 report

## Result

Marker passed **262/283 normalized gold checks (92.6%)** on the frozen 15-page cohort.

This is a consequential-probe benchmark, not a full-page character-error-rate benchmark. Marker output remains non-authoritative until source review.

## Decision

**Adopt Marker as the local first-pass OCR and page-layout engine. Do not use its flattened output as the canonical recipe extractor.**

Marker is materially useful here: it preserved most consequential text, ran entirely locally, retained page/block geometry, and produced visual debug artifacts. Its primary weakness is structural rather than cosmetic. On dense multi-recipe pages it sometimes emitted an ingredient list before the recipe title that owns it, and it occasionally dropped repeated yield/preparation lines near page bottoms. Those errors can silently create a plausible but incorrect recipe record.

The production extraction pipeline should therefore:

1. Preserve Marker's page blocks, polygons, and raw text as rebuildable evidence.
2. Segment recipes using page geometry and explicit recipe entities, not the flattened Markdown/JSON reading sequence alone.
3. Recover and review footer-like blocks so yield and preparation-time lines cannot disappear silently.
4. Flag mixed fractions, temperatures, quantities, units, Czech diacritics, repeated lines, continuations, and cross-references for visual review.
5. Promote text to the canonical dataset only after a human verifies it against the cited page region.

## Metrics

| Metric | Passed | Total | Percent |
|---|---:|---:|---:|
| Exact | 118 | 124 | 95.2% |
| Numeric | 68 | 71 | 95.8% |
| Diacritic | 32 | 35 | 91.4% |
| Title | 14 | 17 | 82.4% |
| Order | 19 | 19 | 100.0% |
| Ownership | 10 | 14 | 71.4% |
| Count | 1 | 3 | 33.3% |

The 100% order result covers the benchmark's adjacent inventory-title checks; it does not mean whole-page recipe association was perfect. The ownership and occurrence-count metrics expose that distinction.

## Page-level misses

### PDF page 2 / printed page 1

Page type: section inventory.

Missing or altered exact probes:
- `Stuffed veal breast - Telecí hrudí nadivané.`

### PDF page 4 / printed page 3

Page type: recipe.

Missing or altered exact probes:
- `1-1/2 cups sour cream`

Failed ownership checks:
- `Roast beef tenderloin in sour cream sauce owns 1-1/2 cups sour cream`

### PDF page 5 / printed page 4

Page type: two recipes.

Failed ownership checks:
- `Beef croquettes owns 3/4 cup bread crumbs`

Failed occurrence-count checks:
- `Serves 6 - Preparation time: 1 hour expected 2, found 1`

### PDF page 11 / printed page 10

Page type: two recipes.

Missing or altered titles:
- `Veal chops with caraway seeds - Telecí žebírka na kmíně`
- `Breaded veal chops - Telecí žebírka smažená`

Failed occurrence-count checks:
- `Serves 6 - Preparation time: 45 minutes expected 2, found 1`

### PDF page 17 / printed page 16

Page type: recipe.

Missing or altered exact probes:
- `Serves 6 - Preparation time: 2 hours 30 minutes`

### PDF page 25 / printed page 24

Page type: continuation plus two recipes.

Missing or altered titles:
- `Duckling with Madeira wine - Kachna na víně`

### PDF page 34 / printed page 33

Page type: recipe with ingredient subgroup.

Missing or altered exact probes:
- `1-1/2 quarts water`

### PDF page 35 / printed page 34

Page type: section inventory.

Missing or altered exact probes:
- `Dumplings with croutons - Houskové knedlíky.`
- `Tripe soup - Dršťková polévka.`

### PDF page 52 / printed page 51

Page type: three related recipes.

Failed ownership checks:
- `Vanilla sauce owns 1 tablespoon corn starch`
- `White wine froth owns 1 cup white table wine`

## Interpretation boundary

A passed probe means the normalized source string was present in Marker output. It does not prove that unprobed text is correct or that the page is ready for canonical promotion. Missing/invented text outside the probes and exact visual punctuation require further review.

## Execution record

- Candidate: `marker-pdf==2.0.0` with `surya-ocr==0.22.1`.
- Cohort: 15 frozen PDF pages spanning inventories, single recipes, multi-recipe pages, continuations, ingredient subgroups, and the index.
- Gold set: 124 visually verified exact probes, 14 ownership checks, and 3 repeated-occurrence checks.
- Mode: balanced local VLM layout plus forced full-page OCR; optional LLM enhancement was not enabled and no cookbook page was sent to a remote model.
- Elapsed Marker run time: 195.48 seconds on this machine.
