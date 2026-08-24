---
name: "Vera's Family Recipes"
description: "A private, source-grounded family recipe reader with a practical kitchen-book character."
colors:
  paper: "#f6f2e9"
  paper-strong: "#fffdf7"
  ink: "#10100f"
  tomato-red: "#bd2c1f"
  tomato-red-dark: "#852116"
  rule-ink: "#161615"
  muted-copy: "#726d65"
  soft-rule: "#ddd7ca"
  dialog-shadow-ink: "rgba(0,0,0,.48)"
  dialog-backdrop-ink: "rgba(16,16,15,.72)"
typography:
  display:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "clamp(2rem, 3.4vw, 3.65rem)"
    fontWeight: 400
    lineHeight: 0.9
    letterSpacing: "-0.045em"
  body:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.2
  label:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "0.045em"
  wordmark:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "clamp(2.25rem, 4vw, 4.3rem)"
    lineHeight: 0.82
    letterSpacing: "-0.055em"
  wordmark-mobile:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "clamp(2.15rem, 10vw, 2.75rem)"
  search:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "1.13rem"
  saved-action:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.2rem"
    fontWeight: 700
  saved-icon-only:
    fontSize: "0"
  panel-label:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.64rem"
    fontWeight: 700
  navigation:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.98rem"
    fontWeight: 600
  navigation-count:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.85rem"
  source-note:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.88rem"
  library-summary:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.93rem"
  study-label:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.61rem"
    fontWeight: 800
    letterSpacing: "0.065em"
  recipe-order:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.71rem"
    fontWeight: 800
    letterSpacing: "0.09em"
  card-title:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "clamp(1.35rem, 2vw, 2.05rem)"
    lineHeight: 0.95
    letterSpacing: "-0.04em"
  card-meta:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.83rem"
  action-label:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 800
    letterSpacing: "0.045em"
  load-more:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.08rem"
  empty-state:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.7rem"
  featured-stamp:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.62rem"
    fontWeight: 800
    letterSpacing: "0.08em"
  featured-title:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "clamp(2.1rem, 3.2vw, 3.5rem)"
    lineHeight: 0.88
    letterSpacing: "-0.055em"
  ingredients-heading:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.35rem"
    fontWeight: 700
  ingredient-preview:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.91rem"
  featured-action:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.1rem"
    fontWeight: 700
  feature-empty:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.8rem"
  dialog-eyeline:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.76rem"
    fontWeight: 800
    letterSpacing: "0.12em"
  dialog-title:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "clamp(3rem, 7vw, 6rem)"
    lineHeight: 0.84
    letterSpacing: "-0.065em"
  source-dialog-title:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "clamp(2.5rem, 5vw, 4.75rem)"
    lineHeight: 0.88
    letterSpacing: "-0.04em"
  dialog-meta:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 700
  dialog-section-title:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.7rem"
  source-stamp:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.8rem"
  navigation-mobile:
    fontFamily: "Barlow Kitchen, Arial, sans-serif"
    fontSize: "0.86rem"
  card-title-mobile:
    fontFamily: "Bodoni Cookbook, Didot, serif"
    fontSize: "1.45rem"
rounded:
  control: "5px"
  pill: "99px"
  circle: "50%"
spacing:
  compact: "0.45rem"
  control: "0.75rem"
  card: "0.8rem"
  grid: "1rem"
  section: "1.6rem"
  page: "2.35rem"
components:
  button-primary:
    backgroundColor: "{colors.tomato-red}"
    textColor: "#fff"
    typography: "{typography.display}"
    rounded: "{rounded.control}"
    padding: "0.75rem 1rem"
    height: "2.95rem"
  button-saved:
    backgroundColor: "{colors.tomato-red}"
    textColor: "#fffaf2"
    typography: "{typography.display}"
    rounded: "{rounded.control}"
    padding: "0.75rem 1rem"
    height: "3.45rem"
  input-search:
    backgroundColor: "rgba(255,253,247,.72)"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    padding: "0 0.95rem"
    height: "3.45rem"
  nav-tab:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    padding: "0.6rem 0.45rem"
  recipe-card:
    backgroundColor: "{colors.paper-strong}"
    textColor: "{colors.ink}"
    rounded: "0"
    padding: "0.8rem"
  recipe-dialog:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "0"
    padding: "2.4rem"
---

# Design System: Vera's Family Recipes

## Overview

**Creative North Star: "Family Recipe Issue"**

This is a practical recipe library with the material character of a family kitchen book: ivory paper, black ink, tomato red, framed food studies, and display typography used with restraint. The reader keeps browsing, saved recipes, and a featured recipe on one shared work surface instead of turning the cookbook into a magazine-style sequence of pages.

The visual system supports a private, source-grounded family collection. Strong rules, source-order labels, and small source-checked stamps make provenance visible while the generous display type keeps recipes easy to scan. The result is editorial in character but utility-led in operation.

**Key Characteristics:**

- Ivory paper texture framed by a black outer field.
- High-contrast Bodoni titles paired with condensed, direct utility copy.
- Tomato red reserved for active, saved, and source-signaling moments.
- Thin ink rules and rectangular image frames structure the archive.
- A responsive practical-library layout, not magazine-page navigation.

## Colors

The palette is a warm paper-and-ink base with one culinary red accent; the contrast of those materials does the organizational work.

### Primary

- **Tomato Red:** active collection tabs, recipe-order labels, ingredient bullets, icon accents, and the principal recipe action.
- **Deep Tomato Red:** the darker edge for tomato-red controls and underlined recovery actions.

### Neutral

- **Ivory Paper:** the main reader field and recipe-dialog surface.
- **Clean Recipe Paper:** card and control surface that separates content from the textured field.
- **Kitchen Ink:** default copy, marks, and the outer browser field.
- **Rule Ink:** the strong structural stroke for shell, cards, controls, and dialog edges.
- **Quiet Gray:** secondary recipe metadata and source context.
- **Soft Paper Rule:** the lighter internal divider within a recipe card.

### Named Rules

**The One Accent Rule.** Tomato red is a locator and an action signal, not a wash. Keep the paper-and-ink field dominant; use red for current selection, saved state, source evidence, and the clearest next action.

## Typography

**Display Font:** Bodoni Cookbook, with Didot and serif fallbacks.

**Body Font:** Barlow Kitchen, with Arial and sans-serif fallbacks.

**Character:** High-contrast display faces give recipe names and kitchen-book labels their familial, printed character. Condensed Barlow carries counts, search, navigation, metadata, and source language compactly enough to preserve a working surface.

### Hierarchy

- **Display** (400, `clamp(2rem, 3.4vw, 3.65rem)`, 0.9 line-height): collection heading; the frontmatter records the distinct wordmark, featured, card, and dialog display clamps alongside their mobile variants.
- **Headline** (400, `clamp(2.1rem, 3.2vw, 3.5rem)`, 0.88 line-height): featured recipe title.
- **Title** (400–700, `clamp(1.35rem, 2vw, 2.05rem)`, 0.95 line-height): card titles, panel labels, and smaller section heads.
- **Body** (400, 1rem, 1.2 line-height): searching, browse labels, metadata, and ingredient previews; dialog recipe lists open to 1.48 line-height for cooking readability.
- **Label** (800, 0.71–0.82rem, tracked uppercase): recipe order, source stamps, image studies, and direct action labels.

### Named Rules

**The Title-Then-Utility Rule.** Let Bodoni identify the recipe or section; let Barlow explain its order, time, source, and action. Do not use display typography to turn dense operational copy into decoration.

## Layout

The reader is capped at 1680px and centered inside a full-height paper shell. At large sizes, the main work surface is a three-column grid: a 238px collection rail, a flexible recipe library, and a 330px featured-recipe panel. The header uses a three-part grid for wordmark, search, and saved-recipes control; its 2px rule establishes the page's strongest horizontal boundary.

The recipe library uses a three-column card grid with a 1rem gap, 1.45rem horizontal inset, and 1.6rem top inset. Card copy is compact while card images use a 1.27:1 frame. Major page insets use 2.35rem; the system repeats close 0.45–0.8rem intervals for control and card internals, then opens to 1–1.6rem between groups.

At 1120px, search moves beneath the wordmark and saved control; the featured panel becomes a full-width horizontal module beneath the rail and library. At 780px, the reader becomes a vertical flow, browse groups become horizontally scrollable pills, the grid becomes two columns, and the featured recipe returns to a vertical card. At 470px, the grid becomes one column and the library heading stacks.

## Elevation & Depth

The system is flat by default. Paper surfaces, thin ink rules, and the framed-food-image treatment establish hierarchy without ambient cards. Motion creates the only everyday lift: a hovered recipe card moves up 3px and takes a small shadow; the recipe dialog alone receives a deep modal shadow and a blurred dark backdrop.

### Shadow Vocabulary

- **Card Hover** (`0 10px 22px rgba(16,16,15,.18)`): reserved for the interactive lift of a recipe card.
- **Recipe Dialog** (`0 20px 80px rgba(0,0,0,.48)`): isolates the complete transcription above the reader; its separate backdrop uses dialog-backdrop-ink with a 3px blur.

### Named Rules

**The Paper-First Rule.** Build separation with paper tones and ink rules at rest. Use shadow only for a hover response or an explicitly modal reading state.

## Shapes

The form language is mostly square and printed: cards, food studies, panels, and dialogs use crisp rectangular frames with visible rules. Controls that invite direct action soften only slightly with a 5px radius. On narrow screens, collection tabs become 99px pills to make their compact, horizontal navigation role obvious; counters and source dots are circular. The bookmark action has a clipped bookmark silhouette rather than a generic icon container.

## Components

### Buttons

Buttons are confident kitchen-book controls: direct labels, firm ink outlines, small 5px corners, and no decorative fill treatment beyond the tomato-red primary action.

- **Saved recipes:** a display-face red button with a 3.45rem minimum height; its active state switches to Kitchen Ink and an optional paper counter appears.
- **Featured primary:** a tomato-red, display-face button with a 2.95rem minimum height; the adjacent save control keeps the same frame but returns to transparent paper.
- **Read recipe:** a borderless, tracked uppercase action with a tomato-red northeast arrow.
- **Hover / Focus:** cards animate over 180ms; all buttons, inputs, and links receive a 3px tomato-red focus outline offset by 3px.

### Inputs / Fields

- **Search:** a 3.45rem-high, ink-ruled field on translucent clean paper with a leading stroked search icon and an unboxed input interior.
- **Focus:** the shared tomato-red 3px outline is the visible keyboard treatment; the input itself suppresses its native outline.

### Cards / Containers

- **Corner Style:** square, visibly ruled rectangular cards.
- **Background:** clean recipe paper inside the textured ivory reader field.
- **Shadow Strategy:** flat at rest; card hover uses the Card Hover shadow only.
- **Border:** a 1px rule-ink frame with a lighter internal action divider.
- **Internal Padding:** 0.8rem around recipe copy; images preserve a 1.27:1 landscape study.

### Navigation

- **Collection rail:** a vertical stack of ink labels divided by light ink rules. Each item begins with a simple mark: a diamond for a collection and a circle for All recipes.
- **Active state:** selected label and mark turn tomato red; counts remain quiet gray and use tabular numerals.
- **Mobile treatment:** at 780px, items become compact 99px outlined pills in one horizontally scrollable row, and counts disappear.

### Recipe Dialog

- **Style:** a large square paper sheet with a 2px rule-ink edge, dark translucent blurred backdrop, a circular sticky close control, and generous transcription padding.
- **Content rhythm:** a red uppercase eyeline leads into a large display title; double rules frame source metadata; ingredients and preparation form a two-column reading grid before stacking on mobile.

### Source Evidence Viewer

- **Style:** a second paper-sheet dialog opens above the transcription for every source-checked recipe.
- **Content rhythm:** the source label, preserved recipe title, and exact PDF/printed-page caption frame a full-width scan. The viewer presents only the retained scan matched to that recipe's canonical provenance.

## Do's and Don'ts

### Do:

- **Do** keep the ivory paper, Kitchen Ink, and thin-rule base visually dominant; use Tomato Red for state and action.
- **Do** pair Bodoni recipe or section titles with Barlow operational text, counts, source context, and controls.
- **Do** retain strong rectangular content frames and source-order labels when extending collection views.
- **Do** preserve the responsive shift from three-part reader to horizontal browse pills and a single-column reading flow.
- **Do** make keyboard focus visible with the established tomato-red outlined treatment.

### Don't:

- **Don't** recast this as a generic public recipe feed or a magazine-page navigation experience.
- **Don't** introduce broad color washes, soft card stacks, or routine shadows that compete with the paper-and-ink hierarchy.
- **Don't** replace compact source and utility labels with oversized display type.
- **Don't** use tomato red as decorative background across an entire surface; its rarity is part of its meaning.
