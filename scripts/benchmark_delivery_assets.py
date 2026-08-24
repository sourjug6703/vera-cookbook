#!/usr/bin/env python3
"""Create a small, review-only delivery-asset benchmark for TASK-005.

This script reads the current local reader assets and writes derivative
candidates below review/delivery-asset-benchmark. It never changes recipe YAML,
source evidence, retained PNGs, site data, or reader code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "review" / "delivery-asset-benchmark"
RECIPE_SAMPLES = ("vera-r0079.png", "vera-r0029.png", "vera-r0004.png")
SCAN_SAMPLES = (
    "vera-r0044-page-32.png",
    "vera-r0041-page-30.png",
    "vera-r0001-page-04.png",
)
RECIPE_WIDTHS = (480, 720, 1080)
# PSNR is a screening signal, not a substitute for the rendered visual review.
# The high-grain illustration language deliberately scores lower than a smooth
# photograph at equal perceived quality, so 30 dB is the conservative floor.
RECIPE_PSNR_MIN_DB = 30.0


@dataclass
class Result:
    kind: str
    sample: str
    format: str
    width: int
    height: int
    source_bytes: int
    candidate_bytes: int
    byte_reduction_pct: float
    psnr_db: float | None
    pixel_exact: bool | None
    source_pixel_sha256: str
    candidate_pixel_sha256: str
    source: str
    candidate: str


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def pixel_payload(image: Image.Image, mode: str) -> bytes:
    converted = image.convert(mode)
    return f"{converted.width}x{converted.height}|{mode}|".encode() + converted.tobytes()


def pixel_sha256(image: Image.Image, mode: str) -> str:
    return sha256_bytes(pixel_payload(image, mode))


def psnr(reference: Image.Image, candidate: Image.Image) -> float:
    left = reference.convert("RGB")
    right = candidate.convert("RGB")
    if left.size != right.size:
        raise ValueError(f"decoded dimensions differ: {left.size} vs {right.size}")
    squared_error = sum((a - b) ** 2 for a, b in zip(left.tobytes(), right.tobytes()))
    if squared_error == 0:
        return math.inf
    mean_squared_error = squared_error / len(left.tobytes())
    return 10 * math.log10((255**2) / mean_squared_error)


def require_tool(name: str) -> None:
    if not shutil.which(name):
        raise RuntimeError(f"Required encoder is unavailable: {name}")


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)


def resized_copy(source: Path, width: int, destination: Path) -> Image.Image:
    with Image.open(source) as opened:
        image = opened.convert("RGB")
    height = round(image.height * width / image.width)
    resized = image.resize((width, height), Image.Resampling.LANCZOS)
    destination.parent.mkdir(parents=True, exist_ok=True)
    resized.save(destination, format="PNG", optimize=True)
    return resized


def encode_recipe(reference: Path, output: Path, format_name: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if format_name == "avif":
        run(["avifenc", "--no-overwrite", "-q", "85", "-s", "6", "-y", "444", str(reference), str(output)])
    elif format_name == "webp":
        run(["cwebp", "-quiet", "-q", "82", "-m", "6", "-sharp_yuv", "-metadata", "none", str(reference), "-o", str(output)])
    else:
        raise ValueError(f"Unsupported recipe format: {format_name}")


def encode_scan(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    run(["cwebp", "-quiet", "-lossless", "-m", "6", "-metadata", "none", str(source), "-o", str(output)])


def label(draw: ImageDraw.ImageDraw, position: tuple[int, int], text: str) -> None:
    draw.text(position, text, fill=25 if draw.mode == "L" else "#191611", font=ImageFont.load_default())


def recipe_contact_sheet(output: Path, results: list[Result]) -> None:
    columns = ("PNG reference", "AVIF q85", "WebP q82")
    panel_width = 360
    panel_height = 270
    margin = 20
    label_height = 36
    rows = len(RECIPE_SAMPLES)
    canvas = Image.new("RGB", (margin * 2 + panel_width * 3, margin * 2 + label_height + rows * (panel_height + label_height)), "#f4ede1")
    draw = ImageDraw.Draw(canvas)
    for index, title in enumerate(columns):
        label(draw, (margin + index * panel_width, margin), title)
    benchmark_root = output.parent.parent
    for row, sample in enumerate(RECIPE_SAMPLES):
        y = margin + label_height + row * (panel_height + label_height)
        label(draw, (margin, y), sample)
        paths = [
            benchmark_root / "references" / "recipes" / f"{Path(sample).stem}-720.png",
            benchmark_root / "recipes" / "avif" / f"{Path(sample).stem}-720.avif",
            benchmark_root / "recipes" / "webp" / f"{Path(sample).stem}-720.webp",
        ]
        for column, path in enumerate(paths):
            with Image.open(path) as image:
                panel = image.convert("RGB").resize((panel_width, panel_height), Image.Resampling.LANCZOS)
            canvas.paste(panel, (margin + column * panel_width, y + label_height))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def scan_contact_sheet(output: Path) -> None:
    panel_width = 640
    margin = 20
    label_height = 32
    rows: list[tuple[str, Image.Image, Image.Image]] = []
    benchmark_root = output.parent.parent
    for sample in SCAN_SAMPLES:
        original_path = ROOT / "site" / "assets" / "source-viewer" / sample
        webp_path = benchmark_root / "source-reader" / "webp-lossless" / f"{Path(sample).stem}.webp"
        with Image.open(original_path) as original, Image.open(webp_path) as webp:
            original_panel = original.convert("L")
            webp_panel = webp.convert("L")
            height = round(original_panel.height * panel_width / original_panel.width)
            rows.append((sample, original_panel.resize((panel_width, height), Image.Resampling.LANCZOS), webp_panel.resize((panel_width, height), Image.Resampling.LANCZOS)))
    total_height = margin * 2 + label_height + sum(label_height + image.height for _, image, _ in rows)
    canvas = Image.new("L", (margin * 3 + panel_width * 2, total_height), 244)
    draw = ImageDraw.Draw(canvas)
    label(draw, (margin, margin), "Grayscale PNG fallback")
    label(draw, (margin * 2 + panel_width, margin), "Lossless WebP candidate")
    y = margin + label_height
    for sample, original, webp in rows:
        label(draw, (margin, y), sample)
        y += label_height
        canvas.paste(original, (margin, y))
        canvas.paste(webp, (margin * 2 + panel_width, y))
        y += original.height
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def markdown_report(results: list[Result]) -> str:
    recipe_results = [result for result in results if result.kind == "recipe"]
    scan_results = [result for result in results if result.kind == "source-reader"]
    recipe_reduction = sum(result.byte_reduction_pct for result in recipe_results) / len(recipe_results)
    scan_reduction = sum(result.byte_reduction_pct for result in scan_results) / len(scan_results)
    lowest_psnr = min(result.psnr_db for result in recipe_results if result.psnr_db is not None)
    all_exact = all(result.pixel_exact for result in scan_results)
    lines = [
        "# TASK-005 delivery-asset benchmark",
        "",
        "Status: local review evidence only. It does not alter the reader, canonical YAML, source evidence, retained PNG scans, hosting, privacy, Git history, or remote state.",
        "",
        "## Decision being tested",
        "",
        "For a future separately approved hosted reader, serve responsive AVIF with WebP fallback for recipe illustrations. Serve lossless WebP for grayscale source-reader pages, retaining the existing grayscale PNG as its fallback and evidence-preserving local master.",
        "",
        "## Scope and method",
        "",
        "- Illustrations: three low/median/high-complexity samples (`vera-r0079`, `vera-r0029`, `vera-r0004`) at 480, 720, and 1080 pixels wide. Each LANCZOS-resized PNG reference was encoded as AVIF q85 / 4:4:4 and WebP q82.",
        "- Source-reader pages: three short/medium/tall grayscale samples (`vera-r0044-page-32`, `vera-r0041-page-30`, `vera-r0001-page-04`) encoded at original dimensions as lossless WebP.",
        "- Visual evidence: `visual/recipe-720-comparison.png` and `visual/source-reader-comparison.png`. Quantitative checks: decoded illustration PSNR must clear a 30.0 dB screening floor; decoded source-reader pixels must exactly match the retained grayscale PNG.",
        "",
        "## Result",
        "",
        f"- Illustration candidates passed: lowest decoded PSNR {lowest_psnr:.2f} dB; mean size reduction {recipe_reduction:.1f}% versus their same-dimension PNG references.",
        f"- Source-reader candidates passed: pixel exact = `{str(all_exact).lower()}`; mean size reduction {scan_reduction:.1f}% versus the current grayscale PNGs.",
        "- Recommendation: retain PNG masters and use AVIF/WebP illustration `srcset` candidates only after separate implementation and hosting approval. Use lossless WebP for the source-reader path with the current grayscale PNG as explicit fallback; do not use lossy source-reader encodings.",
        "",
        "## Measured files",
        "",
        "| Kind | Sample | Output | Dimensions | PNG bytes | Candidate bytes | Reduction | Quality check |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        quality = f"{result.psnr_db:.2f} dB" if result.psnr_db is not None else f"pixel exact: {str(result.pixel_exact).lower()}"
        lines.append(
            f"| {result.kind} | `{result.sample}` | `{result.format}` | {result.width}x{result.height} | {result.source_bytes:,} | {result.candidate_bytes:,} | {result.byte_reduction_pct:.1f}% | {quality} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "All benchmark candidates are confined to this review directory. `site/app.js`, `site/data/recipes.json`, `scripts/build_site_data.rb`, recipe YAML, `site/assets/recipes/*.png`, `site/assets/source-viewer/*.png`, and `site/assets/source-pilot/*.png` remain unchanged by this benchmark.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="New review-only output directory")
    args = parser.parse_args()
    output = args.output.resolve()
    try:
        output.relative_to((ROOT / "review").resolve())
    except ValueError as error:
        raise SystemExit("Output must stay inside review/") from error
    if output.exists():
        raise SystemExit(f"Refusing to overwrite existing benchmark output: {output}")
    require_tool("avifenc")
    require_tool("cwebp")

    recipe_sources = [ROOT / "site" / "assets" / "recipes" / sample for sample in RECIPE_SAMPLES]
    scan_sources = [ROOT / "site" / "assets" / "source-viewer" / sample for sample in SCAN_SAMPLES]
    for source in recipe_sources + scan_sources:
        if not source.is_file():
            raise SystemExit(f"Missing benchmark source: {source.relative_to(ROOT)}")

    before = {source: sha256_bytes(source.read_bytes()) for source in recipe_sources + scan_sources}
    results: list[Result] = []
    for source in recipe_sources:
        for width in RECIPE_WIDTHS:
            reference = output / "references" / "recipes" / f"{source.stem}-{width}.png"
            reference_image = resized_copy(source, width, reference)
            source_bytes = reference.stat().st_size
            source_hash = pixel_sha256(reference_image, "RGB")
            for format_name in ("avif", "webp"):
                candidate = output / "recipes" / format_name / f"{source.stem}-{width}.{format_name}"
                encode_recipe(reference, candidate, format_name)
                with Image.open(candidate) as opened:
                    decoded = opened.convert("RGB")
                quality = psnr(reference_image, decoded)
                if quality < RECIPE_PSNR_MIN_DB:
                    raise RuntimeError(f"{candidate.name} quality {quality:.2f} dB is below {RECIPE_PSNR_MIN_DB:.1f} dB")
                results.append(
                    Result(
                        kind="recipe",
                        sample=source.name,
                        format=format_name,
                        width=decoded.width,
                        height=decoded.height,
                        source_bytes=source_bytes,
                        candidate_bytes=candidate.stat().st_size,
                        byte_reduction_pct=100 * (1 - candidate.stat().st_size / source_bytes),
                        psnr_db=quality,
                        pixel_exact=None,
                        source_pixel_sha256=source_hash,
                        candidate_pixel_sha256=pixel_sha256(decoded, "RGB"),
                        source=str(reference.relative_to(ROOT)),
                        candidate=str(candidate.relative_to(ROOT)),
                    )
                )
    for source in scan_sources:
        candidate = output / "source-reader" / "webp-lossless" / f"{source.stem}.webp"
        encode_scan(source, candidate)
        with Image.open(source) as original, Image.open(candidate) as opened:
            original_gray = original.convert("L")
            decoded = opened.convert("L")
        original_hash = pixel_sha256(original_gray, "L")
        candidate_hash = pixel_sha256(decoded, "L")
        exact = original_hash == candidate_hash
        if not exact:
            raise RuntimeError(f"{candidate.name} does not decode exactly to its grayscale PNG source")
        results.append(
            Result(
                kind="source-reader",
                sample=source.name,
                format="webp-lossless",
                width=decoded.width,
                height=decoded.height,
                source_bytes=source.stat().st_size,
                candidate_bytes=candidate.stat().st_size,
                byte_reduction_pct=100 * (1 - candidate.stat().st_size / source.stat().st_size),
                psnr_db=None,
                pixel_exact=True,
                source_pixel_sha256=original_hash,
                candidate_pixel_sha256=candidate_hash,
                source=str(source.relative_to(ROOT)),
                candidate=str(candidate.relative_to(ROOT)),
            )
        )

    after = {source: sha256_bytes(source.read_bytes()) for source in before}
    changed_sources = [str(source.relative_to(ROOT)) for source in before if before[source] != after[source]]
    if changed_sources:
        raise RuntimeError(f"Benchmark changed protected source files: {', '.join(changed_sources)}")

    recipe_contact_sheet(output / "visual" / "recipe-720-comparison.png", results)
    scan_contact_sheet(output / "visual" / "source-reader-comparison.png")
    (output / "results.json").write_text(json.dumps([asdict(result) for result in results], indent=2) + "\n", encoding="utf-8")
    (output / "README.md").write_text(markdown_report(results), encoding="utf-8")
    print(f"Benchmark passed: {len(results)} candidate encodes written to {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
