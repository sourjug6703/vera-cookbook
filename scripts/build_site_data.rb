#!/usr/bin/env ruby
# frozen_string_literal: true

# Builds a browser-safe derivative from the canonical recipe YAML. This script
# never writes to the canonical records and publishes only source-checked data.

require "json"
require "fileutils"
require "time"
require "yaml"

ROOT = File.expand_path("..", __dir__)
RECIPES_PATH = File.join(ROOT, "data", "recipes", "*.yaml")
CONTEXT_PATH = File.join(ROOT, "context", "recipe-context.yml")
OUTPUT_PATH = File.join(ROOT, "site", "data", "recipes.json")
SOURCE_PREVIEW_OUTPUT_DIRECTORY = File.join(ROOT, "site", "assets", "source-pilot")
SOURCE_VIEWER_OUTPUT_DIRECTORY = File.join(ROOT, "site", "assets", "source-viewer")
RECIPE_ILLUSTRATION_DIRECTORY = File.join(ROOT, "site", "assets", "recipes")

def section_for(source_order)
  case source_order
  when 1..44 then "Meats & poultry"
  when 45..50 then "Fish"
  when 51..63 then "Sides & dumplings"
  when 64..70 then "Soups"
  else "Baking & sweets"
  end
end

def source_preview_for(record)
  source_region = record.fetch("source_regions").first
  batch = source_region.fetch("region_image").split("/")[1]
  pdf_pages = record.dig("source_work", "pdf_pages").to_a
  printed_pages = record.dig("source_work", "printed_pages").to_a
  pages = []
  pdf_pages.each_with_index do |pdf_page, index|
    source_path = File.join(ROOT, "evidence", batch, "overview", record.fetch("recipe_id"), format("page-%02d.png", pdf_page))
    next unless File.file?(source_path)

    filename = format("%s-page-%02d.png", record.fetch("recipe_id"), pdf_page)
    FileUtils.cp(source_path, File.join(SOURCE_PREVIEW_OUTPUT_DIRECTORY, filename))
    viewer_path = File.join(SOURCE_VIEWER_OUTPUT_DIRECTORY, filename)
    pages << {
      pdfPage: pdf_page,
      printedPage: printed_pages[index],
      image: File.file?(viewer_path) ? File.join("assets", "source-viewer", filename) : File.join("assets", "source-pilot", filename),
      originalImage: File.join("assets", "source-pilot", filename)
    }
  end

  return if pages.empty?

  { label: "Retained source scan", pages: pages }
end

def illustration_for(record)
  filename = "#{record.fetch("recipe_id")}.png"
  path = File.join(RECIPE_ILLUSTRATION_DIRECTORY, filename)
  return unless File.file?(path)

  {
    image: File.join("assets", "recipes", filename),
    alt: "Illustrated serving of #{record.dig("identity", "display_title", "text_verbatim")}"
  }
end

def history_for(recipe_id, entries, sources)
  entry = entries[recipe_id]
  return unless entry

  {
    label: entry.fetch("label"),
    note: entry.fetch("note"),
    scope: entry.fetch("scope"),
    citations: entry.fetch("source_ids").map do |source_id|
      source = sources.fetch(source_id)
      {
        title: source.fetch("title"),
        publisher: source.fetch("publisher"),
        url: source.fetch("url"),
        accessedOn: source.fetch("accessed_on")
      }
    end
  }
end

def normalized_context_entries(document)
  individual_entries = document.fetch("entries", [])
  grouped_entries = document.fetch("groups", []).flat_map do |group|
    recipe_ids = group.fetch("recipe_ids")
    shared_entry = group.reject { |key, _| key == "recipe_ids" }
    recipe_ids.map { |recipe_id| shared_entry.merge("recipe_id" => recipe_id) }
  end

  individual_entries + grouped_entries
end

FileUtils.mkdir_p(SOURCE_PREVIEW_OUTPUT_DIRECTORY)

context_document = YAML.load_file(CONTEXT_PATH)
context_sources = context_document.fetch("sources").to_h { |source| [source.fetch("source_id"), source] }
context_by_recipe_id = normalized_context_entries(context_document).to_h { |entry| [entry.fetch("recipe_id"), entry] }

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
    sourcePreview: source_preview_for(record),
    illustration: illustration_for(record),
    history: history_for(record.fetch("recipe_id"), context_by_recipe_id, context_sources),
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
