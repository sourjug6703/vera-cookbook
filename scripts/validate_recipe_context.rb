#!/usr/bin/env ruby
# frozen_string_literal: true

require "set"
require "yaml"

ROOT = File.expand_path("..", __dir__)
CONTEXT_PATH = File.join(ROOT, "context", "recipe-context.yml")
RECIPE_PATHS = File.join(ROOT, "data", "recipes", "*.yaml")

def fail_with(errors)
  errors.each { |error| warn "ERROR: #{error}" }
  exit 1
end

document = YAML.load_file(CONTEXT_PATH)
errors = []
errors << "context document must be a mapping" unless document.is_a?(Hash)
errors << "schema_version must be 1" unless document["schema_version"] == 1

sources = document.fetch("sources", [])
entries = document.fetch("entries", [])
groups = document.fetch("groups", [])
errors << "sources must be an array" unless sources.is_a?(Array)
errors << "entries must be an array" unless entries.is_a?(Array)
errors << "groups must be an array" unless groups.is_a?(Array)
fail_with(errors) unless errors.empty?

source_ids = Set.new
sources.each_with_index do |source, index|
  prefix = "sources[#{index}]"
  unless source.is_a?(Hash)
    errors << "#{prefix} must be a mapping"
    next
  end
  %w[source_id publisher title url accessed_on].each do |key|
    errors << "#{prefix}.#{key} is required" if source[key].to_s.strip.empty?
  end
  errors << "#{prefix}.url must be https" unless source["url"].to_s.start_with?("https://")
  errors << "duplicate source_id #{source['source_id']}" if source_ids.include?(source["source_id"])
  source_ids << source["source_id"]
end

recipe_ids = Dir[RECIPE_PATHS].map { |path| YAML.load_file(path).fetch("recipe_id") }.to_set
entry_recipe_ids = Set.new
context_entries = entries.each_with_index.map { |entry, index| [entry, "entries[#{index}]"] }
groups.each_with_index do |group, index|
  prefix = "groups[#{index}]"
  unless group.is_a?(Hash)
    errors << "#{prefix} must be a mapping"
    next
  end
  group_recipe_ids = group["recipe_ids"]
  errors << "#{prefix}.recipe_ids must be a non-empty array" unless group_recipe_ids.is_a?(Array) && !group_recipe_ids.empty?
  shared_entry = group.reject { |key, _| key == "recipe_ids" }
  Array(group_recipe_ids).each_with_index do |recipe_id, member_index|
    context_entries << [shared_entry.merge("recipe_id" => recipe_id), "#{prefix}.recipe_ids[#{member_index}]"]
  end
end

context_entries.each do |entry, prefix|
  unless entry.is_a?(Hash)
    errors << "#{prefix} must be a mapping"
    next
  end
  %w[recipe_id label note scope].each do |key|
    errors << "#{prefix}.#{key} is required" if entry[key].to_s.strip.empty?
  end
  errors << "#{prefix}.recipe_id does not exist: #{entry['recipe_id']}" unless recipe_ids.include?(entry["recipe_id"])
  errors << "duplicate context for #{entry['recipe_id']}" if entry_recipe_ids.include?(entry["recipe_id"])
  entry_recipe_ids << entry["recipe_id"]
  if entry["note"].to_s.length < 80
    errors << "#{prefix}.note must be at least 80 characters"
  end
  citations = entry["source_ids"]
  errors << "#{prefix}.source_ids must be a non-empty array" unless citations.is_a?(Array) && !citations.empty?
  Array(citations).each do |source_id|
    errors << "#{prefix} references unknown source #{source_id}" unless source_ids.include?(source_id)
  end
end

fail_with(errors) unless errors.empty?

puts "Recipe context valid: #{entry_recipe_ids.length}/#{recipe_ids.length} recipes have cited context; #{sources.length} sources registered."
