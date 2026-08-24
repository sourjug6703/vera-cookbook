# TASK-005 delivery-asset benchmark

Status: local review evidence only. It does not alter the reader, canonical YAML, source evidence, retained PNG scans, hosting, privacy, Git history, or remote state.

## Decision being tested

For a future separately approved hosted reader, serve responsive AVIF with WebP fallback for recipe illustrations. Serve lossless WebP for grayscale source-reader pages, retaining the existing grayscale PNG as its fallback and evidence-preserving local master.

## Scope and method

- Illustrations: three low/median/high-complexity samples (`vera-r0079`, `vera-r0029`, `vera-r0004`) at 480, 720, and 1080 pixels wide. Each LANCZOS-resized PNG reference was encoded as AVIF q85 / 4:4:4 and WebP q82.
- Source-reader pages: three short/medium/tall grayscale samples (`vera-r0044-page-32`, `vera-r0041-page-30`, `vera-r0001-page-04`) encoded at original dimensions as lossless WebP.
- Visual evidence: `visual/recipe-720-comparison.png` and `visual/source-reader-comparison.png`. Quantitative checks: decoded illustration PSNR must clear a 30.0 dB screening floor; decoded source-reader pixels must exactly match the retained grayscale PNG.

## Result

- Illustration candidates passed: lowest decoded PSNR 32.19 dB; mean size reduction 84.4% versus their same-dimension PNG references.
- Source-reader candidates passed: pixel exact = `true`; mean size reduction 10.3% versus the current grayscale PNGs.
- Recommendation: retain PNG masters and use AVIF/WebP illustration `srcset` candidates only after separate implementation and hosting approval. Use lossless WebP for the source-reader path with the current grayscale PNG as explicit fallback; do not use lossy source-reader encodings.

## Measured files

| Kind | Sample | Output | Dimensions | PNG bytes | Candidate bytes | Reduction | Quality check |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| recipe | `vera-r0079.png` | `avif` | 480x360 | 306,961 | 50,821 | 83.4% | 40.40 dB |
| recipe | `vera-r0079.png` | `webp` | 480x360 | 306,961 | 38,544 | 87.4% | 36.11 dB |
| recipe | `vera-r0079.png` | `avif` | 720x540 | 641,400 | 96,248 | 85.0% | 41.16 dB |
| recipe | `vera-r0079.png` | `webp` | 720x540 | 641,400 | 75,886 | 88.2% | 37.12 dB |
| recipe | `vera-r0079.png` | `avif` | 1080x810 | 1,321,160 | 173,386 | 86.9% | 41.99 dB |
| recipe | `vera-r0079.png` | `webp` | 1080x810 | 1,321,160 | 136,492 | 89.7% | 38.20 dB |
| recipe | `vera-r0029.png` | `avif` | 480x360 | 344,132 | 64,473 | 81.3% | 35.72 dB |
| recipe | `vera-r0029.png` | `webp` | 480x360 | 344,132 | 52,584 | 84.7% | 32.19 dB |
| recipe | `vera-r0029.png` | `avif` | 720x540 | 727,849 | 129,611 | 82.2% | 37.30 dB |
| recipe | `vera-r0029.png` | `webp` | 720x540 | 727,849 | 105,688 | 85.5% | 33.42 dB |
| recipe | `vera-r0029.png` | `avif` | 1080x810 | 1,520,210 | 236,413 | 84.4% | 38.50 dB |
| recipe | `vera-r0029.png` | `webp` | 1080x810 | 1,520,210 | 193,614 | 87.3% | 35.05 dB |
| recipe | `vera-r0004.png` | `avif` | 480x360 | 389,728 | 79,371 | 79.6% | 35.14 dB |
| recipe | `vera-r0004.png` | `webp` | 480x360 | 389,728 | 63,290 | 83.8% | 32.28 dB |
| recipe | `vera-r0004.png` | `avif` | 720x540 | 858,285 | 171,969 | 80.0% | 36.26 dB |
| recipe | `vera-r0004.png` | `webp` | 720x540 | 858,285 | 137,250 | 84.0% | 32.84 dB |
| recipe | `vera-r0004.png` | `avif` | 1080x810 | 1,854,018 | 343,777 | 81.5% | 37.12 dB |
| recipe | `vera-r0004.png` | `webp` | 1080x810 | 1,854,018 | 278,570 | 85.0% | 34.04 dB |
| source-reader | `vera-r0044-page-32.png` | `webp-lossless` | 1673x476 | 124,235 | 105,318 | 15.2% | pixel exact: true |
| source-reader | `vera-r0041-page-30.png` | `webp-lossless` | 2000x861 | 515,641 | 472,374 | 8.4% | pixel exact: true |
| source-reader | `vera-r0001-page-04.png` | `webp-lossless` | 2000x1289 | 967,829 | 896,732 | 7.3% | pixel exact: true |

## Boundary

All benchmark candidates are confined to this review directory. `site/app.js`, `site/data/recipes.json`, `scripts/build_site_data.rb`, recipe YAML, `site/assets/recipes/*.png`, `site/assets/source-viewer/*.png`, and `site/assets/source-pilot/*.png` remain unchanged by this benchmark.
