#!/usr/bin/env ruby
# frozen_string_literal: true

# Creates a reading-oriented derivative of retained local source scans. The
# originals in site/assets/source-pilot remain untouched and authoritative for
# the reader's evidence link.

require "fileutils"

ROOT = File.expand_path("..", __dir__)
SOURCE_DIRECTORY = File.join(ROOT, "site", "assets", "source-pilot")
OUTPUT_DIRECTORY = File.join(ROOT, "site", "assets", "source-viewer")
MAX_EDGE = "2000x2000>"
PAPER = "#f5f5f5"

abort "Missing retained scans: #{SOURCE_DIRECTORY}" unless Dir.exist?(SOURCE_DIRECTORY)

FileUtils.mkdir_p(OUTPUT_DIRECTORY)
files = Dir[File.join(SOURCE_DIRECTORY, "*.png")].sort
abort "No retained scans found in #{SOURCE_DIRECTORY}" if files.empty?

files.each do |source|
  output = File.join(OUTPUT_DIRECTORY, File.basename(source))
  command = [
    "magick", source,
    "-colorspace", "Gray",
    "-background", PAPER,
    "-alpha", "remove", "-alpha", "off",
    "-deskew", "40%",
    "-resize", MAX_EDGE,
    "-strip",
    "-define", "png:compression-level=9",
    output
  ]
  abort "Could not build #{output}" unless system(*command)
end

puts "Wrote #{files.length} grayscale, deskewed source-viewer images to #{OUTPUT_DIRECTORY}"
