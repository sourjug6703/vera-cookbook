#!/usr/bin/env ruby
# frozen_string_literal: true

# Builds prompt records for the local recipe-illustration production flow.
# It reads canonical recipe YAML but never writes to it. The output is a
# rebuildable planning derivative, not source evidence.

require "json"
require "time"
require "yaml"

ROOT = File.expand_path("..", __dir__)
RECIPES_PATH = File.join(ROOT, "data", "recipes", "*.yaml")
OUTPUT_PATH = File.join(ROOT, "site", "data", "image-prompts.json")

STYLE = <<~STYLE.strip
  Match the established Vera's Family Recipes category-art system: a finished
  landscape 4:3 elevated near-overhead food study on warm ivory paper; a
  period-appropriate dark charcoal or black vessel whose form varies with the
  dish; a restrained black, brick tomato-red, cream, and muted-brown palette;
  crisp printmaking/linocut outlines, tactile halftone and dry speckled grain;
  sparse black botanical sprigs and a few tiny tomato-red berry or dot motifs.
  Present inviting, period-plausible Czech/Czechoslovak home cooking from the
  1950s through the 1990s. No typography, labels, people, photorealism, glossy
  3D, or modern restaurant plating. Keep every essential food element inside
  the frame.
STYLE

def recipe_prompt(record)
  title = record.dig("identity", "display_title", "text_verbatim")
  czech_title = record.dig("identity", "titles").to_a.find { |entry| entry["language"] == "cs" }&.fetch("text_verbatim", nil)
  ingredients = record.dig("transcription", "ingredient_sections").to_a.flat_map do |section|
    section.fetch("ingredients", []).map { |ingredient| ingredient.fetch("text_verbatim") }
  end
  steps = record.dig("transcription", "instruction_sections").to_a.flat_map do |section|
    section.fetch("steps", []).map { |step| step.fetch("text_verbatim") }
  end

  <<~PROMPT.strip
    Create one bespoke recipe illustration for #{title}#{czech_title ? " (#{czech_title})" : ""}. The canonical recipe calls for: #{ingredients.join("; ")}. The preparation is: #{steps.join(" ")[0, 1200]}. Make its defining cooked form, texture, sauce, filling, or baked structure unmistakable. Use only modest, period-plausible accompaniments or mise en place that clarify this particular dish; do not let them replace the dish as the subject.

    #{STYLE}
  PROMPT
end

prompts = []
Dir[RECIPES_PATH].sort.each do |path|
  record = YAML.load_file(path)
  next unless record.dig("verification", "status") == "source_checked"

  prompts << {
    id: record.fetch("recipe_id"),
    sourceOrder: record.dig("identity", "source_order"),
    title: record.dig("identity", "display_title", "text_verbatim"),
    canonicalIngredients: record.dig("transcription", "ingredient_sections").to_a.flat_map { |section| section.fetch("ingredients", []).map { |ingredient| ingredient.fetch("text_verbatim") } },
    canonicalPreparation: record.dig("transcription", "instruction_sections").to_a.flat_map { |section| section.fetch("steps", []).map { |step| step.fetch("text_verbatim") } },
    researchBasis: "Canonical source-checked recipe record plus approved Czech/Czechoslovak 1950s–1990s serving convention.",
    prompt: recipe_prompt(record)
  }
end

payload = { generatedAt: Time.now.utc.iso8601, recordCount: prompts.length, prompts: prompts.sort_by { |prompt| prompt[:sourceOrder] } }
File.write(OUTPUT_PATH, JSON.pretty_generate(payload) + "\n")
puts "Wrote #{prompts.length} recipe image prompts to #{OUTPUT_PATH}"
