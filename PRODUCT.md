# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Local, dependency-free static HTML, CSS, and JavaScript. A Ruby build script
derives browser-safe recipe JSON from the canonical YAML records without
altering them. Any GitHub Pages deployment path remains a separate decision.

## Users

Family cooks using Vera Gaeta's cookbook to choose, understand, and prepare
recipes. This is not a general-public product.

## Product Purpose

Create a digital reader that lets family members explore and cook from the
complete Vera Gaeta cookbook collection while retaining its recipes, source
material, and family context.

## Positioning

The reader connects usable recipe records with the complete preserved cookbook
collection, rather than replacing that collection with a generic recipe site.

## Operating Context

Family members browse on the web while planning or preparing food. They may
move between recipe text, source scans, provenance, review material, and the
original cookbook as useful context.

## Capabilities and Constraints

- The local reader may use the full cookbook corpus; the owner has confirmed
  that no project material is secret.
- Canonical recipe records are the 110 source-checked YAML records under
  `data/recipes/`.
- Source scans, source-region crops, evidence, review material, and pilot
  records are available for the experience when useful.
- The reader is for family cooks, not general-public discovery or marketing.
- The first reader surface uses source-order sections as browse groups rather
  than inventing recipe taxonomy that is absent from canonical records.
- Selecting a deployment stack and enabling GitHub Pages remain open decisions;
  public hosting requires separate explicit approval.

## Evidence on Hand

- Canonical recipe records: `data/recipes/`
- Original cookbook source: `source/`
- Source and region evidence: `evidence/`
- Review pages and retained extraction material: `review/` and `pilot/`
- Recipe contract and inventory: `docs/`

## Product Principles

- Make a family recipe useful in the kitchen without severing it from its
  source.
- Treat the complete cookbook collection as a living family reference, not a
  generic content feed.
- Preserve exact wording and visible provenance when they matter to a cook's
  understanding.
- Let the family explore design possibilities before locking a stack or visual
  system.
