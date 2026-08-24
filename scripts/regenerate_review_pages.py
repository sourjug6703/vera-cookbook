#!/usr/bin/env python3
"""Regenerate local review pages from canonical records without rewriting them."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

import build_production_batch_001 as shared


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", nargs="+", help="three-digit production batch IDs")
    args = parser.parse_args()

    for batch in args.batch:
        review_dir = ROOT / "review" / f"production-batch-{batch}"
        review_path = review_dir / "index.html"
        prior = review_path.read_text(encoding="utf-8")
        ids = re.findall(r'<article class="recipe" id="([^"]+)">', prior)
        records = [
            yaml.safe_load((ROOT / "data" / "recipes" / f"{recipe_id}.yaml").read_text(encoding="utf-8"))
            for recipe_id in ids
        ]
        overviews = {
            recipe_id: sorted(ROOT.glob(f"evidence/*/overview/{recipe_id}/page-*.png"))
            for recipe_id in ids
        }
        if any(not paths for paths in overviews.values()):
            raise SystemExit(f"Missing overview evidence for production batch {batch}")
        shared.BATCH_ID = f"production-batch-{batch}"
        shared.BATCH_TITLE = f"Production batch {batch} source review"
        shared.BATCH_COPY_TITLE = f"Vera Cookbook production batch {batch} review status"
        shared.BATCH_SUMMARY = (
            "Canonical transcription after local source audit and recorded owner source decisions. "
            "This review page does not claim human verification unless a record says so."
        )
        review_path.write_text(shared.render_review_html(records, overviews), encoding="utf-8")
        print(review_path.relative_to(ROOT), len(records))


if __name__ == "__main__":
    main()
