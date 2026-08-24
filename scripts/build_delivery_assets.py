#!/usr/bin/env python3
"""Build non-authoritative delivery copies for the local cookbook reader.

The builder only reads existing PNG masters. It writes AVIF and WebP recipe
variants plus lossless WebP source-reader copies into site/assets/delivery.
It verifies every grayscale source-reader copy decodes to identical pixels and
checks that no input master changed during the run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RECIPE_DIRECTORY = ROOT / "site" / "assets" / "recipes"
SOURCE_READER_DIRECTORY = ROOT / "site" / "assets" / "source-viewer"
DEFAULT_OUTPUT = ROOT / "site" / "assets" / "delivery"
RECIPE_WIDTHS = (480, 720, 1080)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def gray_pixel_sha256(path: Path) -> str:
    with Image.open(path) as image:
        gray = image.convert("L")
    payload = f"{gray.width}x{gray.height}|L|".encode() + gray.tobytes()
    return hashlib.sha256(payload).hexdigest()


def run(command: list[str]) -> None:
    completed = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if completed.returncode:
        raise RuntimeError(f"encoder failed: {' '.join(command[:2])}: {completed.stderr.strip()}")


def encode_recipe(source: Path, output: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    with Image.open(source) as opened:
        master = opened.convert("RGB")
    with tempfile.TemporaryDirectory(prefix="vera-delivery-") as temporary:
        temporary_root = Path(temporary)
        for width in RECIPE_WIDTHS:
            height = round(master.height * width / master.width)
            reference = temporary_root / f"{source.stem}-{width}.png"
            master.resize((width, height), Image.Resampling.LANCZOS).save(reference, format="PNG", optimize=True)
            for format_name, command in (
                ("avif", ["avifenc", "--no-overwrite", "-q", "85", "-s", "6", "-j", "1", "-y", "444"]),
                ("webp", ["cwebp", "-quiet", "-q", "82", "-m", "6", "-sharp_yuv", "-metadata", "none"]),
            ):
                candidate = output / "recipes" / format_name / f"{source.stem}-{width}.{format_name}"
                run([*command, str(reference), *([] if format_name == "avif" else ["-o"]), str(candidate)])
                with Image.open(candidate) as decoded:
                    if decoded.size != (width, height):
                        raise RuntimeError(f"wrong dimensions: {candidate.relative_to(ROOT)}")
                results.append({
                    "kind": "recipe",
                    "source": str(source.relative_to(ROOT)),
                    "candidate": str(candidate.relative_to(ROOT)),
                    "format": format_name,
                    "width": width,
                    "height": height,
                    "bytes": candidate.stat().st_size,
                })
    return results


def encode_source_reader(source: Path, output: Path) -> dict[str, object]:
    candidate = output / "source-reader-webp" / f"{source.stem}.webp"
    run(["cwebp", "-quiet", "-lossless", "-m", "6", "-metadata", "none", str(source), "-o", str(candidate)])
    source_hash = gray_pixel_sha256(source)
    candidate_hash = gray_pixel_sha256(candidate)
    if source_hash != candidate_hash:
        raise RuntimeError(f"lossless pixel mismatch: {candidate.relative_to(ROOT)}")
    with Image.open(source) as image:
        width, height = image.size
    return {
        "kind": "source-reader",
        "source": str(source.relative_to(ROOT)),
        "candidate": str(candidate.relative_to(ROOT)),
        "format": "webp-lossless",
        "width": width,
        "height": height,
        "bytes": candidate.stat().st_size,
        "pixel_sha256": source_hash,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    output = args.output.resolve()
    if args.jobs < 1:
        raise SystemExit("--jobs must be positive")
    try:
        output.relative_to((ROOT / "site" / "assets").resolve())
    except ValueError as error:
        raise SystemExit("Output must remain inside site/assets/") from error
    if output.exists():
        raise SystemExit(f"Refusing to overwrite delivery output: {output.relative_to(ROOT)}")
    for tool in ("avifenc", "cwebp"):
        if not shutil.which(tool):
            raise SystemExit(f"Missing required encoder: {tool}")

    recipes = sorted(RECIPE_DIRECTORY.glob("*.png"))
    source_pages = sorted(SOURCE_READER_DIRECTORY.glob("*.png"))
    if not recipes or not source_pages:
        raise SystemExit("Expected PNG masters are missing")
    protected = {path: sha256_file(path) for path in [*recipes, *source_pages]}
    for directory in (output / "recipes" / "avif", output / "recipes" / "webp", output / "source-reader-webp"):
        directory.mkdir(parents=True, exist_ok=False)

    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(encode_recipe, recipe, output) for recipe in recipes]
        futures.extend(executor.submit(encode_source_reader, page, output) for page in source_pages)
        for future in as_completed(futures):
            result = future.result()
            results.extend(result if isinstance(result, list) else [result])

    changed = [str(path.relative_to(ROOT)) for path, digest in protected.items() if sha256_file(path) != digest]
    if changed:
        raise RuntimeError(f"protected PNG master changed during build: {', '.join(changed)}")
    manifest = {
        "recipe_master_count": len(recipes),
        "source_reader_master_count": len(source_pages),
        "candidate_count": len(results),
        "results": sorted(results, key=lambda item: str(item["candidate"])),
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {manifest['candidate_count']} delivery copies from {len(recipes)} recipe and {len(source_pages)} source-reader PNG masters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
