#!/usr/bin/env python3
"""Validate canonical recipe records and their promotion evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from PIL import Image


PROJECT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_DIR / "schemas/recipe-record.schema.json"
RECIPE_DIR = PROJECT_DIR / "data/recipes"
EXAMPLE_PATH = PROJECT_DIR / "examples/recipe-record.example.yaml"
SHA256_CACHE: dict[Path, str] = {}

BASE_PROMOTION_CHECKS = {
    "region_coverage",
    "recipe_boundary",
    "ingredient_ownership",
    "instruction_ownership",
    "transcription_exactness",
    "numeric_tokens",
    "yield\u005ftime_presence",
    "occurrence_count",
}


def load_record(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        value = json.loads(text)
    else:
        value = yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError("top-level value must be an object")
    return value


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def segments(record: dict[str, Any]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    display_title = record.get("identity", {}).get("display_title")
    if display_title:
        found.append(display_title)
    found.extend(record.get("identity", {}).get("titles", []))
    transcription = record.get("transcription", {})
    for key in ("headnotes", "yield_time_lines", "notes", "cross_references"):
        found.extend(transcription.get(key, []))
    for section in transcription.get("ingredient_sections", []):
        if section.get("label"):
            found.append(section["label"])
        found.extend(section.get("ingredients", []))
    for section in transcription.get("instruction_sections", []):
        if section.get("label"):
            found.append(section["label"])
        found.extend(section.get("steps", []))
    return found


def ingredient_ids(record: dict[str, Any]) -> set[str]:
    return {
        line["segment_id"]
        for section in record.get("transcription", {}).get("ingredient_sections", [])
        for line in section.get("ingredients", [])
    }


def instruction_ids(record: dict[str, Any]) -> set[str]:
    return {
        step["segment_id"]
        for section in record.get("transcription", {}).get("instruction_sections", [])
        for step in section.get("steps", [])
    }


def format_schema_error(error: Any) -> str:
    location = "/" + "/".join(str(part) for part in error.absolute_path)
    return f"schema {location}: {error.message}"


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    recipe_id = record.get("recipe_id", "<unknown>")
    region_list = record.get("source_regions", [])
    region_ids = [region.get("region_id") for region in region_list]
    known_regions = set(region_ids)
    segment_list = segments(record)
    segment_ids = [segment.get("segment_id") for segment in segment_list]

    if record.get("schema_version") == "1.2.0" and not record.get(
        "transcription", {}
    ).get("ingredient_sections"):
        errors.append("schema_version 1.2.0 requires at least one ingredient section")

    all_ids = [recipe_id, *region_ids, *segment_ids]
    for section in record.get("transcription", {}).get("ingredient_sections", []):
        all_ids.append(section.get("section_id"))
    for section in record.get("transcription", {}).get("instruction_sections", []):
        all_ids.append(section.get("section_id"))
    duplicate_ids = sorted({item for item in all_ids if item and all_ids.count(item) > 1})
    if duplicate_ids:
        errors.append(f"duplicate identifiers: {', '.join(duplicate_ids)}")

    known_targets = {item for item in all_ids if item}
    for segment in segment_list:
        missing = set(segment.get("source_region_ids", [])) - known_regions
        if missing:
            errors.append(
                f"segment {segment.get('segment_id')} cites unknown regions: {sorted(missing)}"
            )

    declared_pages = set(record.get("source_work", {}).get("pdf_pages", []))
    region_pages = {region.get("pdf_page") for region in region_list}
    if declared_pages != region_pages:
        errors.append(
            f"source_work.pdf_pages {sorted(declared_pages)} must exactly match region pages "
            f"{sorted(region_pages)}"
        )
    page_count = record.get("source_work", {}).get("pdf_page_count", 0)
    invalid_pages = sorted(page for page in region_pages if not isinstance(page, int) or page > page_count)
    if invalid_pages:
        errors.append(f"source regions exceed pdf_page_count: {invalid_pages}")

    relationships = record.get("relationships", {})
    for relation in relationships.get("continuations", []):
        for key in ("from_region_id", "to_region_id"):
            if relation.get(key) not in known_regions:
                errors.append(f"continuation cites unknown region {relation.get(key)!r}")

    verification = record.get("verification", {})
    checks = verification.get("checks", [])
    check_ids = [check.get("check_id") for check in checks]
    duplicate_checks = sorted({item for item in check_ids if item and check_ids.count(item) > 1})
    if duplicate_checks:
        errors.append(f"duplicate verification check IDs: {', '.join(duplicate_checks)}")

    for check in checks:
        unknown_targets = set(check.get("target_ids", [])) - known_targets
        unknown_regions = set(check.get("source_region_ids", [])) - known_regions
        if unknown_targets:
            errors.append(
                f"check {check.get('check_id')} cites unknown targets: {sorted(unknown_targets)}"
            )
        if unknown_regions:
            errors.append(
                f"check {check.get('check_id')} cites unknown regions: {sorted(unknown_regions)}"
            )
    for issue in verification.get("open_issues", []):
        unknown_targets = set(issue.get("target_ids", [])) - known_targets
        if unknown_targets:
            errors.append(
                f"issue {issue.get('issue_id')} cites unknown targets: {sorted(unknown_targets)}"
            )

    status = verification.get("status")
    display_text = record.get("identity", {}).get("display_title", {}).get("text_verbatim", "")
    for title in record.get("identity", {}).get("titles", []):
        if title.get("text_verbatim") not in display_text:
            errors.append(
                f"display_title does not contain title segment {title.get('segment_id')!r}"
            )
    has_uncertainties = any(segment.get("uncertainties") for segment in segment_list)
    has_nonpassing_checks = any(
        check.get("result") in {"fail", "ambiguous"} for check in checks
    )
    has_open_issues = bool(verification.get("open_issues"))

    if status == "machine_candidate" and checks:
        errors.append("machine_candidate records cannot contain completed audit checks")
    if status == "needs_attention" and not (
        has_uncertainties or has_nonpassing_checks or has_open_issues
    ):
        errors.append(
            "needs_attention records must contain an uncertainty, non-passing audit check, "
            "or open issue"
        )

    promotion_performer = {
        "source_checked": "ai",
        "human_verified": "human",
        "human_verified_two_person": "human",
    }.get(status)
    if promotion_performer is None:
        return errors

    if has_uncertainties:
        errors.append(f"{status} records cannot contain transcription uncertainties")
    promotion_checks = [
        check for check in checks if check.get("performed_by") == promotion_performer
    ]
    nonpassing = [
        check.get("check_id")
        for check in promotion_checks
        if check.get("result") not in {"pass", "not_applicable"}
    ]
    if nonpassing:
        errors.append(f"{status} records contain non-passing promotion checks: {nonpassing}")

    passed_checks = [
        check for check in promotion_checks if check.get("result") == "pass"
    ]
    passed_types = {check.get("check_type") for check in passed_checks}
    required_types = set(BASE_PROMOTION_CHECKS)
    if not ingredient_ids(record):
        required_types.discard("ingredient_ownership")
        required_types.add("ingredient_list_presence")
    if any(any(ord(char) > 127 and char.isalpha() for char in segment.get("text_verbatim", "")) for segment in segment_list):
        required_types.add("diacritics")
    if len(declared_pages) > 1 or relationships.get("continuations"):
        required_types.add("continuation")
    if record.get("transcription", {}).get("cross_references"):
        required_types.add("cross_reference")
    missing_types = sorted(required_types - passed_types)
    if missing_types:
        errors.append(
            f"{status} record is missing passing {promotion_performer} promotion checks: "
            f"{missing_types}"
        )

    def covered(check_type: str) -> set[str]:
        return {
            target
            for check in passed_checks
            if check.get("check_type") == check_type
            for target in check.get("target_ids", [])
        }

    if not ingredient_ids(record):
        presence_checks = [
            check
            for check in passed_checks
            if check.get("check_type") == "ingredient_list_presence"
            and recipe_id in check.get("target_ids", [])
        ]
        if not presence_checks:
            errors.append("ingredient-list absence audit must target the recipe ID")
        elif not any(
            known_regions <= set(check.get("source_region_ids", []))
            for check in presence_checks
        ):
            errors.append(
                "ingredient-list absence audit must cover every declared source region"
            )

    authoritative_ids = set(segment_ids)
    missing_exact = sorted(authoritative_ids - covered("transcription_exactness"))
    if missing_exact:
        errors.append(f"segments lack passing transcription_exactness audit: {missing_exact}")
    missing_ingredient_ownership = sorted(ingredient_ids(record) - covered("ingredient_ownership"))
    if missing_ingredient_ownership:
        errors.append(
            "ingredients lack passing ownership audit: " + str(missing_ingredient_ownership)
        )
    missing_instruction_ownership = sorted(instruction_ids(record) - covered("instruction_ownership"))
    if missing_instruction_ownership:
        errors.append(
            "instruction steps lack passing ownership audit: " + str(missing_instruction_ownership)
        )
    numeric_ids = {
        segment["segment_id"]
        for segment in segment_list
        if any(char.isdigit() for char in segment.get("text_verbatim", ""))
    }
    missing_numeric = sorted(numeric_ids - covered("numeric_tokens"))
    if missing_numeric:
        errors.append(f"numeric segments lack passing numeric_tokens audit: {missing_numeric}")

    if status == "human_verified_two_person":
        exact_auditors: dict[str, set[str]] = {segment_id: set() for segment_id in segment_ids}
        for check in passed_checks:
            if check.get("check_type") != "transcription_exactness":
                continue
            for target in check.get("target_ids", []):
                if target in exact_auditors:
                    exact_auditors[target].add(check.get("auditor_id"))
        insufficient = sorted(
            segment_id for segment_id, auditors in exact_auditors.items() if len(auditors) < 2
        )
        if insufficient:
            errors.append(
                "two-person human verification lacks two distinct exactness auditors for: "
                + str(insufficient)
            )

    status_set_at = verification.get("status_set_at")
    audit_times = [
        check.get("audited_at") for check in promotion_checks if check.get("audited_at")
    ]
    if status_set_at and audit_times:
        try:
            if parse_timestamp(status_set_at) < max(
                parse_timestamp(value) for value in audit_times
            ):
                errors.append("status_set_at cannot precede the latest promotion audit check")
        except ValueError:
            pass
    return errors


def validate_record(record: dict[str, Any], validator: Draft202012Validator) -> list[str]:
    errors = [format_schema_error(error) for error in validator.iter_errors(record)]
    errors.extend(f"contract: {error}" for error in semantic_errors(record))
    return sorted(errors)


def canonical_file_errors(path: Path, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if path.stem != record.get("recipe_id"):
        errors.append(
            f"canonical filename {path.name!r} must match recipe_id {record.get('recipe_id')!r}"
        )
    source_value = record.get("source_work", {}).get("source_file")
    if not source_value:
        return errors
    source_path = (PROJECT_DIR / source_value).resolve()
    try:
        source_path.relative_to(PROJECT_DIR.resolve())
    except ValueError:
        errors.append("canonical source_file resolves outside the project")
        return errors
    if not source_path.is_file():
        errors.append(f"canonical source file does not exist: {source_value}")
        return errors
    digest = SHA256_CACHE.get(source_path)
    if digest is None:
        digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
        SHA256_CACHE[source_path] = digest
    expected = record.get("source_work", {}).get("source_sha256")
    if digest != expected:
        errors.append(f"source SHA-256 mismatch: expected {expected}, found {digest}")

    for region in record.get("source_regions", []):
        image_value = region.get("region_image")
        expected_pixel_hash = region.get("region_image_pixel_sha256")
        if not image_value or not expected_pixel_hash:
            continue
        image_path = (PROJECT_DIR / image_value).resolve()
        try:
            image_path.relative_to(PROJECT_DIR.resolve())
        except ValueError:
            errors.append(f"region {region.get('region_id')} image resolves outside the project")
            continue
        if not image_path.is_file():
            errors.append(f"region {region.get('region_id')} image is missing: {image_value}")
            continue
        with Image.open(image_path) as opened:
            image = opened.convert("RGB")
            payload = f"{image.width}x{image.height}|{image.mode}|".encode() + image.tobytes()
            actual_pixel_hash = hashlib.sha256(payload).hexdigest()
        if actual_pixel_hash != expected_pixel_hash:
            errors.append(
                f"region {region.get('region_id')} decoded-pixel hash mismatch: "
                f"expected {expected_pixel_hash}, found {actual_pixel_hash}"
            )
        polygon = region.get("polygon", [])
        if len(polygon) >= 4:
            xs = [point[0] for point in polygon]
            ys = [point[1] for point in polygon]
            expected_width = round(max(xs) - min(xs))
            expected_height = round(max(ys) - min(ys))
            if (image.width, image.height) != (expected_width, expected_height):
                errors.append(
                    f"region {region.get('region_id')} crop dimensions {image.width}x{image.height} "
                    f"do not match polygon bounds {expected_width}x{expected_height}"
                )
    return errors


def make_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def run_self_test(validator: Draft202012Validator) -> None:
    fixture = load_record(EXAMPLE_PATH)
    fixture_errors = validate_record(fixture, validator)
    if fixture_errors:
        raise AssertionError("valid fixture failed:\n" + "\n".join(fixture_errors))

    missing_numeric = copy.deepcopy(fixture)
    missing_numeric["verification"]["checks"] = [
        check
        for check in missing_numeric["verification"]["checks"]
        if check["check_type"] != "numeric_tokens"
    ]
    errors = validate_record(missing_numeric, validator)
    if not any("numeric_tokens" in error for error in errors):
        raise AssertionError("missing numeric audit was not rejected")

    missing_ownership = copy.deepcopy(fixture)
    missing_ownership["verification"]["checks"] = [
        check
        for check in missing_ownership["verification"]["checks"]
        if check["check_type"] != "ingredient_ownership"
    ]
    errors = validate_record(missing_ownership, validator)
    if not any("ingredient_ownership" in error for error in errors):
        raise AssertionError("missing ingredient ownership audit was not rejected")

    bad_region = copy.deepcopy(fixture)
    bad_region["transcription"]["ingredient_sections"][0]["ingredients"][0][
        "source_region_ids"
    ] = ["region-does-not-exist"]
    errors = validate_record(bad_region, validator)
    if not any("unknown regions" in error for error in errors):
        raise AssertionError("unknown source region was not rejected")

    mislabeled_human = copy.deepcopy(fixture)
    mislabeled_human["verification"]["status"] = "human_verified"
    mislabeled_human["verification"]["audit_policy"] = "human_single"
    errors = validate_record(mislabeled_human, validator)
    if not any("human promotion checks" in error for error in errors):
        raise AssertionError("AI audit mislabeled as human verification was not rejected")

    fake_double_review = copy.deepcopy(fixture)
    fake_double_review["verification"]["status"] = "human_verified_two_person"
    fake_double_review["verification"]["audit_policy"] = "human_double"
    for check in fake_double_review["verification"]["checks"]:
        check["performed_by"] = "human"
        check["auditor_id"] = "fixture-human-1"
    errors = validate_record(fake_double_review, validator)
    if not any("two distinct exactness auditors" in error for error in errors):
        raise AssertionError("fake two-person human promotion was not rejected")

    human_source_check = copy.deepcopy(fixture)
    for check in human_source_check["verification"]["checks"]:
        check["performed_by"] = "human"
    errors = validate_record(human_source_check, validator)
    if not any("ai promotion checks" in error for error in errors):
        raise AssertionError("source_checked without AI audit evidence was not rejected")

    empty_attention = copy.deepcopy(fixture)
    empty_attention["verification"]["status"] = "needs_attention"
    empty_attention["verification"]["open_issues"] = []
    empty_attention["verification"]["checks"] = [
        check
        for check in empty_attention["verification"]["checks"]
        if check["result"] in {"pass", "not_applicable"}
    ]
    errors = validate_record(empty_attention, validator)
    if not any("needs_attention records must contain" in error for error in errors):
        raise AssertionError("empty needs_attention state was not rejected")

    no_ingredients = copy.deepcopy(fixture)
    no_ingredients["schema_version"] = "1.3.0"
    removed_ingredient_ids = ingredient_ids(no_ingredients)
    no_ingredients["transcription"]["ingredient_sections"] = []
    for check in no_ingredients["verification"]["checks"]:
        if check["check_type"] == "ingredient_ownership":
            check["check_id"] = "ai-ingredient-list-presence"
            check["check_type"] = "ingredient_list_presence"
            check["target_ids"] = [no_ingredients["recipe_id"]]
            check["source_region_ids"] = [
                region["region_id"] for region in no_ingredients["source_regions"]
            ]
            check["note"] = (
                "The complete recipe context was inspected and the source prints no ingredient list."
            )
    for check in no_ingredients["verification"]["checks"]:
        check["target_ids"] = [
            target for target in check["target_ids"] if target not in removed_ingredient_ids
        ]
    errors = validate_record(no_ingredients, validator)
    if errors:
        raise AssertionError(
            "valid v1.3 source-authored ingredient absence failed:\n" + "\n".join(errors)
        )

    missing_absence_audit = copy.deepcopy(no_ingredients)
    missing_absence_audit["verification"]["checks"] = [
        check
        for check in missing_absence_audit["verification"]["checks"]
        if check["check_type"] != "ingredient_list_presence"
    ]
    errors = validate_record(missing_absence_audit, validator)
    if not any("ingredient_list_presence" in error for error in errors):
        raise AssertionError("missing ingredient-list absence audit was not rejected")

    wrong_absence_target = copy.deepcopy(no_ingredients)
    for check in wrong_absence_target["verification"]["checks"]:
        if check["check_type"] == "ingredient_list_presence":
            check["target_ids"] = ["title-en"]
    errors = validate_record(wrong_absence_target, validator)
    if not any("must target the recipe ID" in error for error in errors):
        raise AssertionError("mis-targeted ingredient-list absence audit was not rejected")

    partial_absence_regions = copy.deepcopy(no_ingredients)
    for check in partial_absence_regions["verification"]["checks"]:
        if check["check_type"] == "ingredient_list_presence":
            check["source_region_ids"] = check["source_region_ids"][:1]
    errors = validate_record(partial_absence_regions, validator)
    if not any("must cover every declared source region" in error for error in errors):
        raise AssertionError("partial ingredient-list absence audit was not rejected")

    inapplicable_absence = copy.deepcopy(no_ingredients)
    for check in inapplicable_absence["verification"]["checks"]:
        if check["check_type"] == "ingredient_list_presence":
            check["result"] = "not_applicable"
    errors = validate_record(inapplicable_absence, validator)
    if not any("ingredient_list_presence" in error for error in errors):
        raise AssertionError("not-applicable ingredient-list absence audit was not rejected")

    old_no_ingredients = copy.deepcopy(no_ingredients)
    old_no_ingredients["schema_version"] = "1.2.0"
    errors = validate_record(old_no_ingredients, validator)
    if not any("1.2.0 requires at least one ingredient section" in error for error in errors):
        raise AssertionError("v1.2 empty ingredient sections were not rejected")
    if not any("non-empty" in error.message for error in validator.iter_errors(old_no_ingredients)):
        raise AssertionError("v1.2 empty ingredients did not fail JSON Schema validation")

    print(
        "Self-test passed: valid AI source check accepted; missing numeric/ownership audit, "
        "bad provenance, AI-as-human labeling, false two-person verification, performer "
        "mismatch, and empty needs_attention rejected; v1.3 source-authored ingredient "
        "absence accepted only with an explicit presence audit while v1.2 absence is rejected."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, help="YAML or JSON recipe records")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    validator = make_validator()
    if args.self_test:
        run_self_test(validator)

    paths = args.paths
    if not paths and not args.self_test:
        paths = sorted(RECIPE_DIR.glob("*.yaml")) + sorted(RECIPE_DIR.glob("*.json"))
    elif not paths and args.self_test:
        paths = [EXAMPLE_PATH]

    failures = 0
    for path in paths:
        try:
            record = load_record(path)
            errors = validate_record(record, validator)
            try:
                path.resolve().relative_to(RECIPE_DIR.resolve())
            except ValueError:
                pass
            else:
                errors.extend(f"canonical: {error}" for error in canonical_file_errors(path, record))
        except Exception as error:  # keep batch validation readable
            errors = [str(error)]
        if errors:
            failures += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")

    print(f"Validated {len(paths)} record(s); {failures} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
