# Recipe image direction

## Status and authority

Recipe illustrations are local, generated derivatives for the reader. They are
not source evidence, transcription, or a claim that the photographed/illustrated
presentation appears in Vera Gaeta's book. Canonical `data/recipes/*.yaml` and
their retained scan evidence remain authoritative for every dish's title,
ingredients, method, and provenance.

The reader may use a recipe-specific illustration when
`site/assets/recipes/<recipe-id>.png` exists. Otherwise it deliberately falls
back to the existing category study. The builder detects these local files; it
does not write or alter canonical recipe YAML.

## Locked visual language

The five existing category studies are the visual source of truth for the
illustration system:

- Landscape 4:3 elevated, near-overhead food studies on a warm ivory ground.
- A substantial dark charcoal or black vessel anchors the food. Its form may
  vary by dish: oval platter, handled enamel dish, round plate, casserole, or
  baking tray.
- A restrained black, brick tomato-red, cream, and muted-brown palette with
  occasional natural food colors only when they clarify the dish.
- Crisp ink contours, screenprint/linocut character, crosshatching or
  halftone, dry speckled grain, and an intentionally hand-printed finish.
- Sparse black botanical sprigs and a few tiny tomato-red berry or dot motifs
  frame the vessel. They support the composition and must not obscure food.
- No lettering, labels, people, glossy 3D, photorealism, or modern restaurant
  plating.

## Food direction

Present inviting, period-plausible Czech/Czechoslovak home cooking from the
1950s through the 1990s. Let the canonical recipe lead: make its signature
protein, dough, sauce, filling, or texture unmistakable. Research should add
plausible serving conventions and clarify how the dish is normally recognized,
without overwriting the canonical recipe.

Period-appropriate side dishes, lemon, herbs, a ramekin of whole spices,
pickles, simple salads, serving utensils, or modest tableware are permitted
when they make the food clearer or more generous. Do not make an unsupported
side dish the visual subject. Favor an honest, appetizing domestic serving when
a literal reconstruction would be visually unappealing or ambiguous.

## Per-recipe prompt process

1. Read the canonical recipe title, ingredients, instructions, and source
   notes; identify the signature visual cues.
2. Research the dish's customary Czech/Czechoslovak appearance and serving
   conventions, prioritizing reputable Czech-language culinary and historical
   sources where useful.
3. Write a bespoke prompt that distinguishes the dish from neighbouring
   recipes through the food, vessel shape, crop, arrangement, and restrained
   supporting details while retaining the locked visual language.
4. Inspect the generated output for food plausibility, recipe-specific cues,
   composition, 4:3 safety, and closeness to the category-study style before
   copying it into `site/assets/recipes/`.
5. Keep the prompt/research note with the generated asset so it can be audited
   or regenerated. Do not treat generated imagery as evidence.

## Calibration: recipes 001–005

The first five local assets establish the quality bar:

- `vera-r0001`: sliced bacon-larded beef with cream root-vegetable sauce,
  bread dumplings, lemon, cranberry preserve, and cream.
- `vera-r0002`: tenderloin medallions in a sour-cream, pickle, caper, and herb
  sauce with bread dumplings.
- `vera-r0003`: crumb-coated fried beef patties, mashed potatoes, cucumber
  salad, and pickles.
- `vera-r0004`: sliced baked meat loaf showing hard-boiled egg and pickle
  filling, potatoes, and a simple salad.
- `vera-r0005`: paprika-onion beef goulash with boiled potatoes and modest
  supporting mise en place.

Svíčková convention was checked against contemporary Czech serving references
that pair sliced beef and cream sauce with dumplings, lemon, cranberry, and
cream. Karbanátky and filled meat loaf references supported domestic potato,
salad, and pickle accompaniments. These references guide appearance only; the
canonical recipe remains the factual dish authority.
