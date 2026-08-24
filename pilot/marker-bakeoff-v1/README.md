# Marker bake-off v1

This pilot evaluates Marker on a frozen, source-specific 15-page cohort from
the scanned cookbook. It does not authorize any machine output as canonical
recipe text.

## Reproduce

1. Create the isolated environment: `uv venv .venv`.
2. Install the pinned candidate: `uv pip install --python .venv/bin/python -r requirements-marker.txt`.
3. Run `scripts/run_marker_bakeoff.sh`.

The command deliberately omits `--use_llm`; no remote LLM service is used.
Balanced mode uses Marker's local VLM layout model and forced full-page OCR.
Marker page indexes are zero-based and are mapped to one-based PDF page
numbers in `cohort.yaml`.

Score the completed run with:

`.venv/bin/python scripts/score_marker_bakeoff.py`

The machine-readable scores are in `results.json`; the decision and reviewable
findings are in `report.md`.

## Evaluation contract

- The source PDF is immutable evidence.
- Gold probes must be established by direct visual inspection, independently
  of Marker output.
- Every gold assertion cites a one-based PDF page and a visible region.
- Marker output is scored for exact text, reading order, recipe boundaries,
  ownership, numbers/units, Czech diacritics, notes, alternatives, and
  cross-references.
- Plausible-looking output is still a failure when it moves text between
  recipes, changes a consequential token, omits text, or invents text.

## Outcome

Marker is accepted as the first-pass OCR/layout engine, not as the authority
for recipe boundaries or canonical text. The next phase must use its geometry
to build recipe entities and retain human verification as the promotion gate.
