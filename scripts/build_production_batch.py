#!/usr/bin/env python3
"""Build any declarative production batch and its local source-audit packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

import build_production_batch_001 as shared


PROJECT_DIR = Path(__file__).resolve().parents[1]
SOURCE_PDF = PROJECT_DIR / "source/Culinary Adventures - Vera Gaeta.pdf"


def segment(
    segment_id: str,
    text: str,
    source_ids: list[str],
    language: str = "en",
    **extra: Any,
) -> dict[str, Any]:
    value = {
        "segment_id": segment_id,
        "text_verbatim": text,
        "language": language,
        "source_region_ids": source_ids,
    }
    value.update(extra)
    return value


def section_items(
    recipe_id: str,
    section_specs: list[dict[str, Any]],
    item_key: str,
    item_prefix: str,
    numbered: bool = False,
) -> list[dict[str, Any]]:
    built_sections = []
    counter = 0
    for section_spec in section_specs:
        built: dict[str, Any] = {"section_id": section_spec["section_id"], item_key: []}
        label = section_spec.get("label")
        if label:
            built["label"] = segment(
                label["segment_id"],
                label["text"],
                [f"{recipe_id}-{label['region_key']}"],
                language=label.get("language", "en"),
            )
        for item in section_spec.get("items", []):
            counter += 1
            item_id = item.get("segment_id", f"{item_prefix}-{counter}")
            extra = {"step_number": counter} if numbered else {}
            value = segment(
                item_id,
                item["text"],
                [f"{recipe_id}-{key}" for key in item["region_keys"]],
                language=item.get("language", "en"),
                **extra,
            )
            if item.get("uncertainties"):
                value["uncertainties"] = item["uncertainties"]
            built[item_key].append(value)
        built_sections.append(built)
    return built_sections


def build_record(
    recipe: dict[str, Any],
    source_regions: list[dict[str, Any]],
    batch: dict[str, Any],
    stage: str,
) -> dict[str, Any]:
    rid = recipe["recipe_id"]
    source_id = lambda key: f"{rid}-{key}"
    titles = [
        segment(
            item["segment_id"],
            item["text"],
            [source_id("title")],
            language=item["language"],
            title_role=item["title_role"],
        )
        for item in recipe["titles"]
    ]
    ingredient_sections = section_items(
        rid, recipe.get("ingredient_sections", []), "ingredients", "ingredient"
    )
    instruction_sections = section_items(
        rid, recipe["instruction_sections"], "steps", "step", numbered=True
    )

    def simple_segments(specs: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
        values = []
        for index, item in enumerate(specs, 1):
            value = segment(
                item.get("segment_id", f"{prefix}-{index}"),
                item["text"],
                [source_id(key) for key in item["region_keys"]],
                language=item.get("language", "en"),
            )
            if item.get("uncertainties"):
                value["uncertainties"] = item["uncertainties"]
            values.append(value)
        return values

    transcription: dict[str, Any] = {
        "yield_time_lines": simple_segments(recipe["yield_time_lines"], "yield"),
        "ingredient_sections": ingredient_sections,
        "instruction_sections": instruction_sections,
        "notes": simple_segments(recipe.get("notes", []), "note"),
        "cross_references": simple_segments(
            recipe.get("cross_references", []), "cross-reference"
        ),
    }
    if recipe.get("headnotes"):
        transcription["headnotes"] = simple_segments(recipe["headnotes"], "headnote")

    continuations = [
        {
            "from_region_id": source_id(item["from_region_key"]),
            "to_region_id": source_id(item["to_region_key"]),
            "relationship": item.get("relationship", "continues_on"),
        }
        for item in recipe.get("continuations", [])
    ]
    record = {
        "schema_version": batch.get("recipe_schema_version", "1.2.0"),
        "record_type": "recipe",
        "recipe_id": rid,
        "record_revision": recipe.get("record_revision", 1),
        "source_work": {
            "work_id": "vera-culinary-adventures",
            "source_file": "source/Culinary Adventures - Vera Gaeta.pdf",
            "source_sha256": batch["source_sha256"],
            "pdf_page_count": batch.get("pdf_page_count", 75),
            "pdf_pages": recipe["pages"],
            "printed_pages": recipe["printed_pages"],
            "rights_status": "not_assessed",
        },
        "source_regions": source_regions,
        "identity": {
            "display_title": segment(
                "title-display",
                recipe["display_title"],
                [source_id("title")],
                language="mul",
            ),
            "titles": titles,
            "source_order": recipe["source_order"],
            "slug_candidate": recipe["slug"],
        },
        "transcription": transcription,
        "relationships": {
            "continuations": continuations,
            "related_recipe_ids": recipe.get("related_recipe_ids", []),
        },
        "provenance": {
            "created_at": batch["created_at"],
            "created_by": "codex-candidate",
            "candidate_sources": [
                {
                    "tool": "marker-pdf",
                    "tool_version": batch.get("marker_version", "2.0.0"),
                    "generated_at": batch["marker_generated_at"],
                    "artifact_path": batch["marker_artifact"],
                    "remote_model_used": False,
                }
            ],
        },
    }
    if stage == "candidate":
        record["verification"] = {
            "status": "machine_candidate",
            "audit_policy": "source_audit",
            "status_set_at": batch["created_at"],
            "checks": [],
            "open_issues": [],
        }
    else:
        record["verification"] = shared.build_verification(record, recipe)
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--stage", choices=["candidate", "audited"], required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--skip-existing-candidates",
        action="store_true",
        help="Resume an interrupted candidate build without rewriting preserved snapshots.",
    )
    args = parser.parse_args()

    spec_path = args.spec if args.spec.is_absolute() else PROJECT_DIR / args.spec
    batch = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    recipes = batch["recipes"]
    readback_record_ids = batch.get("readback_record_ids", [])
    batch_id = batch["batch_id"]
    marker_json = PROJECT_DIR / batch["marker_artifact"]
    evidence_dir = PROJECT_DIR / "evidence" / batch_id
    page_dir = evidence_dir / "source-pages"
    region_dir = evidence_dir / "regions"
    overview_dir = evidence_dir / "overview"
    recipe_dir = PROJECT_DIR / "data/recipes"
    review_dir = PROJECT_DIR / "review" / batch_id
    report_path = spec_path.parent / f"build-report-{args.stage}.json"
    candidate_snapshot_dir = spec_path.parent / "machine-candidates"

    digest = hashlib.sha256(SOURCE_PDF.read_bytes()).hexdigest()
    if digest != batch["source_sha256"]:
        raise SystemExit("Source PDF SHA-256 does not match the batch specification")

    for recipe in recipes:
        recipe["regions"] = [
            (item["key"], item["role"], item["pdf_page"], item["block_ids"])
            for item in recipe["regions"]
        ]
        recipe.setdefault("open_issues", [])

    shared.SOURCE_PDF = SOURCE_PDF
    shared.SOURCE_SHA256 = batch["source_sha256"]
    shared.MARKER_JSON = marker_json
    shared.EVIDENCE_DIR = evidence_dir
    shared.PAGE_DIR = page_dir
    shared.REGION_DIR = region_dir
    shared.OVERVIEW_DIR = overview_dir
    shared.RECIPE_DIR = recipe_dir
    shared.REVIEW_DIR = review_dir
    shared.REPORT_PATH = report_path
    shared.AUDIT_AT = batch["audited_at"]
    shared.AUDITOR_ID = batch.get("auditor_id", "openai-codex")
    shared.RECIPES = recipes
    shared.BATCH_ID = batch_id
    shared.BATCH_TITLE = batch["batch_title"]
    shared.BATCH_COPY_TITLE = batch["batch_copy_title"]
    shared.BATCH_SUMMARY = (
        batch["candidate_summary"] if args.stage == "candidate" else batch["audited_summary"]
    )

    pages = shared.marker_pages()
    expected_pages = {page for recipe in recipes for page in recipe["pages"]}
    missing_pages = expected_pages - set(pages)
    if missing_pages:
        raise SystemExit(f"Marker output is missing required PDF pages: {sorted(missing_pages)}")

    recipe_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    records = []
    overviews: dict[str, list[Path]] = {}
    report: dict[str, Any] = {"batch_id": batch_id, "stage": args.stage, "records": []}
    for recipe in recipes:
        record_path = recipe_dir / f"{recipe['recipe_id']}.yaml"
        if (
            args.stage == "candidate"
            and args.skip_existing_candidates
            and record_path.exists()
        ):
            record = yaml.safe_load(record_path.read_text(encoding="utf-8"))
            if record["verification"]["status"] != "machine_candidate":
                raise SystemExit(
                    "Can only skip an existing machine candidate: " f"{record_path}"
                )
            overview_paths = sorted(
                (overview_dir / recipe["recipe_id"]).glob("page-*.png")
            )
            if not overview_paths:
                raise SystemExit(
                    f"No overview evidence exists for resumed candidate {record_path}"
                )
            records.append(record)
            overviews[recipe["recipe_id"]] = overview_paths
            report["records"].append(
                {
                    "recipe_id": recipe["recipe_id"],
                    "record_path": str(record_path.relative_to(PROJECT_DIR)),
                    "source_regions": len(record["source_regions"]),
                    "overview_images": [
                        str(path.relative_to(PROJECT_DIR)) for path in overview_paths
                    ],
                    "high_risk_tokens": shared.risk_tokens(record),
                    "open_issue_count": len(recipe["open_issues"]),
                    "status": "machine_candidate",
                    "audit_performed_by": None,
                    "resumed_without_rewrite": True,
                }
            )
            continue
        if record_path.exists() and not args.force:
            raise SystemExit(
                f"Refusing to overwrite {record_path}; pass --force only for an intentional stage transition"
            )
        source_regions = []
        boxes: dict[int, list[tuple[int, int, int, int]]] = {}
        for key, _role, pdf_page, block_ids in recipe["regions"]:
            region, box = shared.crop_region(
                recipe["recipe_id"], key, pdf_page, block_ids, pages[pdf_page]
            )
            source_regions.append(region)
            boxes.setdefault(pdf_page, []).append(box)
        overviews[recipe["recipe_id"]] = shared.write_overviews(recipe, boxes)
        record = build_record(recipe, source_regions, batch, args.stage)
        record_path.write_text(
            yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8",
        )
        if args.stage == "candidate":
            candidate_snapshot_dir.mkdir(parents=True, exist_ok=True)
            (candidate_snapshot_dir / record_path.name).write_text(
                yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=100),
                encoding="utf-8",
            )
        records.append(record)
        report["records"].append(
            {
                "recipe_id": recipe["recipe_id"],
                "record_path": str(record_path.relative_to(PROJECT_DIR)),
                "source_regions": len(source_regions),
                "overview_images": [
                    str(path.relative_to(PROJECT_DIR))
                    for path in overviews[recipe["recipe_id"]]
                ],
                "high_risk_tokens": shared.risk_tokens(record),
                "open_issue_count": len(recipe["open_issues"]),
                "status": record["verification"]["status"],
                "audit_performed_by": "ai" if args.stage == "audited" else None,
            }
        )

    new_record_ids = {recipe["recipe_id"] for recipe in recipes}
    duplicate_readbacks = new_record_ids.intersection(readback_record_ids)
    if duplicate_readbacks:
        raise SystemExit(
            "Read-back records must not also be generated: "
            f"{sorted(duplicate_readbacks)}"
        )
    for recipe_id in readback_record_ids:
        record_path = recipe_dir / f"{recipe_id}.yaml"
        if not record_path.exists():
            raise SystemExit(f"Read-back record does not exist: {record_path}")
        record = yaml.safe_load(record_path.read_text(encoding="utf-8"))
        overview_paths = sorted(
            PROJECT_DIR.glob(f"evidence/*/overview/{recipe_id}/page-*.png")
        )
        if not overview_paths:
            raise SystemExit(f"No overview evidence found for read-back record {recipe_id}")
        records.append(record)
        overviews[recipe_id] = overview_paths
        performed_by = sorted(
            {
                check.get("performed_by")
                for check in record["verification"].get("checks", [])
                if check.get("performed_by")
            }
        )
        report["records"].append(
            {
                "recipe_id": recipe_id,
                "record_path": str(record_path.relative_to(PROJECT_DIR)),
                "source_regions": len(record["source_regions"]),
                "overview_images": [
                    str(path.relative_to(PROJECT_DIR)) for path in overview_paths
                ],
                "high_risk_tokens": shared.risk_tokens(record),
                "open_issue_count": len(
                    record["verification"].get("open_issues", [])
                ),
                "status": record["verification"]["status"],
                "audit_performed_by": performed_by[0] if len(performed_by) == 1 else None,
                "read_back_only": True,
            }
        )

    records.sort(key=lambda item: item["identity"]["source_order"])
    report["records"].sort(
        key=lambda item: next(
            record["identity"]["source_order"]
            for record in records
            if record["recipe_id"] == item["recipe_id"]
        )
    )

    review_path = review_dir / (
        "machine-candidate.html" if args.stage == "candidate" else "index.html"
    )
    review_path.write_text(shared.render_review_html(records, overviews), encoding="utf-8")
    report.update(
        {
            "spec": str(spec_path.relative_to(PROJECT_DIR)),
            "review_packet": str(review_path.relative_to(PROJECT_DIR)),
            "source_sha256": batch["source_sha256"],
            "marker_pages_available": sorted(pages),
            "marker_pages_used": sorted(expected_pages),
            "audit_completed_at": batch["audited_at"] if args.stage == "audited" else None,
            "auditor_id": shared.AUDITOR_ID if args.stage == "audited" else None,
        }
    )
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if args.stage == "audited":
        (spec_path.parent / "build-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
