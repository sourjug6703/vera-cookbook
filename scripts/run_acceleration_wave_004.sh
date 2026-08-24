#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd "${script_dir}/.." && pwd)"
source_pdf="${project_dir}/source/Culinary Adventures - Vera Gaeta.pdf"
output_dir="${project_dir}/pilot/acceleration-wave-004/marker-output"

if [[ ! -x "${project_dir}/.venv/bin/marker_single" ]]; then
  echo "Marker is not installed in ${project_dir}/.venv" >&2
  exit 1
fi

# PDF pages 35-42 are zero-based Marker indexes 34-41. Pages 35 and 42 give
# adjacent layout context around batch 008's pages 36-41.
"${project_dir}/.venv/bin/marker_single" \
  "${source_pdf}" \
  --mode balanced \
  --force_ocr \
  --page_range "34-41" \
  --output_format json \
  --disable_image_extraction \
  --debug \
  --debug_json \
  --debug_layout_images \
  --debug_pdf_images \
  --debug_data_folder "${output_dir}/debug" \
  --output_dir "${output_dir}"
