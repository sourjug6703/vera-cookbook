# Recipe context

This directory holds a research-owned layer for the reader's short history and
cook-learning notes. It is deliberately separate from `data/recipes/`:

- Canonical YAML remains the exact, source-checked transcription of Vera's
  cookbook.
- A context note describes a wider dish, ingredient, or holiday tradition. It
  never proves that Vera's printed recipe is traditional, complete, or the same
  as any cited outside recipe.
- Every visible note must name at least one source from the registry. The
  reader displays those citations as links.
- No citation means no public note. Unknown or weakly supported history stays
  absent rather than being filled with a generic claim.

`recipe-context.yml` is a small human-maintained registry. Sources record the
publisher, title, URL, and access date; entries map a short, plain-language
note to a stable recipe ID. A `groups` entry can apply one carefully bounded
dish-family note to several listed recipe IDs; it is used only when the same
context is genuinely useful for each member. The validator checks source
references and full recipe coverage, while `scripts/build_site_data.rb` turns
only valid entries into a browser derivative.
