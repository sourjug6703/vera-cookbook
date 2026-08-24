#!/usr/bin/env ruby
# frozen_string_literal: true

# Builds a browser-safe derivative from the canonical recipe YAML. This script
# never writes to the canonical records and publishes only source-checked data.

require "json"
require "time"
require "yaml"

ROOT = File.expand_path("..", __dir__)
RECIPES_PATH = File.join(ROOT, "data", "recipes", "*.yaml")
OUTPUT_PATH = File.join(ROOT, "site", "data", "recipes.json")

def section_for(source_order)
  case source_order
  when 1..44 then "Meats & poultry"
  when 45..50 then "Fish"
  when 51..63 then "Sides & dumplings"
  when 64..70 then "Soups"
  else "Baking & sweets"
  end
end

records = Dir[RECIPES_PATH].sort.map do |path|
  record = YAML.load_file(path)
  next unless record.dig("verification", "status") == "source_checked"

  ingredients = record.dig("transcription", "ingredient_sections").to_a.flat_map do |section|
    section.fetch("ingredients", []).map { |line| line.fetch("text_verbatim") }
  end
  instructions = record.dig("transcription", "instruction_sections").to_a.flat_map do |section|
    section.fetch("steps", []).map { |step| step.fetch("text_verbatim") }
  end
  source_order = record.dig("identity", "source_order")

  {
    id: record.fetch("recipe_id"),
    sourceOrder: source_order,
    title: record.dig("identity", "display_title", "text_verbatim"),
    titleEnglish: record.dig("identity", "titles").to_a.find { |title| title["language"] == "en" }&.fetch("text_verbatim", nil),
    titleCzech: record.dig("identity", "titles").to_a.find { |title| title["language"] == "cs" }&.fetch("text_verbatim", nil),
    section: section_for(source_order),
    yieldTime: record.dig("transcription", "yield_time_lines").to_a.map { |line| line.fetch("text_verbatim") },
    ingredients: ingredients,
    instructions: instructions,
    notes: record.dig("transcription", "notes").to_a.map { |note| note.fetch("text_verbatim") },
    sourcePages: record.dig("source_work", "printed_pages").to_a,
    sourceRegions: record.fetch("source_regions").select { |region| region["role"] == "title" }.map { |region| region["region_image"] },
    verification: record.dig("verification", "status")
  }
end.compact

payload = {
  generatedAt: Time.now.utc.iso8601,
  recordCount: records.length,
  recipes: records.sort_by { |record| record[:sourceOrder] }
}

File.write(OUTPUT_PATH, JSON.pretty_generate(payload) + "\n")
puts "Wrote #{records.length} source-checked recipes to #{OUTPUT_PATH}"
