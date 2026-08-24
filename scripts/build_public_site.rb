#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"

root = File.expand_path("..", __dir__)
site = File.join(root, "site")
output = File.join(root, "dist")

files = %w[index.html app.js styles.css]
asset_entries = %w[
  BarlowSemiCondensed-400.ttf
  BarlowSemiCondensed-500.ttf
  BarlowSemiCondensed-600.ttf
  BarlowSemiCondensed-700.ttf
  BarlowSemiCondensed-800.ttf
  BodoniModa-400.ttf
  BodoniModa-600.ttf
  BodoniModa-700.ttf
  BodoniModa-800.ttf
  delivery
  fish.webp
  meats.webp
  sides.webp
  soups.webp
  source-pilot
  source-viewer
  sweets.webp
]

abort "Expected local reader at #{site}" unless Dir.exist?(site)
abort "Refusing to build outside the repository" unless output.start_with?("#{root}/")

FileUtils.rm_rf(output)
FileUtils.mkdir_p(File.join(output, "assets"))

files.each { |name| FileUtils.cp(File.join(site, name), output) }
FileUtils.cp_r(File.join(site, "data"), output)
asset_entries.each do |entry|
  FileUtils.cp_r(File.join(site, "assets", entry), File.join(output, "assets"))
end
File.write(File.join(output, ".nojekyll"), "")

puts "Built public reader at #{output}"
