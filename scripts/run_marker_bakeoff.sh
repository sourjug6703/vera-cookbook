#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd "${script_dir}/.." && pwd)"
source_pdf="${project_dir}/source/Culinary Adventures - Vera Gaeta.pdf"
output_dir="${project_dir}/pilot/marker-bakeoff-v1/marker-output"

if [[ ! -x "${project_dir}/.venv/bin/marker_single" ]]; then
  echo "Marker is not installed in ${project_dir}/.venv" >&2
  exit 1
fi

"${project_dir}/.venv/bin/marker_single" \
  "${source_pdf}" \
  --mode balanced \
  --force_ocr \
  --page_range "1,2,3,4,10,16,24,33,34,35,40,45,46,51,74" \
  --output_format json \
  --disable_image_extraction \
  --debug \
  --debug_json \
  --debug_layout_images \
  --debug_data_folder "${output_dir}/debug" \
  --output_dir "${output_dir}"
