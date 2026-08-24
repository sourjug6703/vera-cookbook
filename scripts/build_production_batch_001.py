#!/usr/bin/env python3
"""Build production batch 001 and its local source-audit packet."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml
from PIL import Image


PROJECT_DIR = Path(__file__).resolve().parents[1]
SOURCE_PDF = PROJECT_DIR / "source/Culinary Adventures - Vera Gaeta.pdf"
SOURCE_SHA256 = "58542d8b58bf57aadfd4c08f6728271ac5bd9d19aa77a2fe9ef412c68b2a989b"
MARKER_JSON = (
    PROJECT_DIR
    / "pilot/production-batch-001/marker-output/Culinary Adventures - Vera Gaeta"
    / "Culinary Adventures - Vera Gaeta.json"
)
EVIDENCE_DIR = PROJECT_DIR / "evidence/production-batch-001"
PAGE_DIR = EVIDENCE_DIR / "source-pages"
REGION_DIR = EVIDENCE_DIR / "regions"
OVERVIEW_DIR = EVIDENCE_DIR / "overview"
RECIPE_DIR = PROJECT_DIR / "data/recipes"
REVIEW_DIR = PROJECT_DIR / "review/production-batch-001"
REPORT_PATH = PROJECT_DIR / "pilot/production-batch-001/build-report.json"
AUDIT_AT = "2026-08-23T20:32:18Z"
AUDITOR_ID = "openai-codex"
BATCH_ID = "production-batch-001"
BATCH_TITLE = "Batch 001 source audit"
BATCH_COPY_TITLE = "Vera Cookbook · Production Batch 001"
BATCH_SUMMARY = (
    "Four records passed a direct local AI source audit. One remains <b>needs attention</b> "
    "because its decorative arrow glyph cannot be encoded exactly without guessing. Human "
    "verification is a separate trust state."
)


def issue(issue_id: str, targets: list[str], description: str, severity: str) -> dict[str, Any]:
    return {
        "issue_id": issue_id,
        "target_ids": targets,
        "description": description,
        "severity": severity,
    }


YIELD_ROLE = "yield\u005ftime"
YIELD_LINES_KEY = "yield\u005ftime_lines"


RECIPES: list[dict[str, Any]] = [
    {
        "recipe_id": "vera-r0001",
        "source_order": 1,
        "slug": "roast-beef-tenderloin-sour-cream-sauce",
        "pages": [4],
        "printed_pages": ["3"],
        "display_title": "Roast beef tenderloin in sour cream sauce - Svíčková",
        "titles": [
            ("en", "primary", "Roast beef tenderloin in sour cream sauce"),
            ("cs", "parallel", "Svíčková"),
        ],
        "regions": [
            ("title", "title", 4, ["/page/3/SectionHeader/1"]),
            ("ingredients", "ingredient", 4, ["/page/3/ListGroup/2"]),
            ("step-1", "instruction", 4, ["/page/3/Text/3"]),
            ("step-2", "instruction", 4, ["/page/3/Text/4"]),
            ("step-3a", "instruction", 4, ["/page/3/Text/5"]),
            ("step-3b", "continuation", 4, ["/page/3/Text/6"]),
            ("step-4", "instruction", 4, ["/page/3/Text/7"]),
            ("step-5", "instruction", 4, ["/page/3/Text/8"]),
            ("step-6a", "instruction", 4, ["/page/3/Text/9"]),
            ("step-6b", "continuation", 4, ["/page/3/Text/10"]),
            ("yield", "yield_time", 4, ["/page/3/Text/11"]),
            ("alternative", "note", 4, ["/page/3/Text/12"]),
            ("tip", "note", 4, ["/page/3/Text/13"]),
        ],
        "ingredients": [
            "4 lbs. beef tenderloin",
            "3 slices bacon",
            "1/2 cup vegetable oil",
            "2 cups sliced soup greens (carrots, parsnips, celery root)",
            "1 medium onion, sliced",
            "few grains allspice, whole black pepper, thyme, bay leaves, nutmeg",
            "2 tablespoons flour",
            "1 cup beef stock",
            "juice of one lemon",
            "1·1/2 cups sour cream",
            "salt and pepper",
        ],
        "steps": [
            ("Tenderloin must be aged and all the fat trimmed off. Cut small slits along the grain of the meat and stuff them with thin strips of bacon. Salt and pepper the meat and set aside.", ["step-1"]),
            ("In a large frying pan combine the oil, half of the sliced soup greens and the onion; place the roast on top and brown on all sides.", ["step-2"]),
            ("In the meantime preheat the oven to 350F. Transfer the roast and the vegetables into a roasting pan, add the remaining vegetables and spices. Roast 40-45 minutes, basting with beef stock and juices from the pan. Remove the roast, keep it warm. Pour the pan drippings into a large stewpan, skim the fat, set pan over medium heat and deglaze, using stock or water. Add the flour, simmer five minutes. Place the roast in the sauce, add the lemon juice and simmer until the meat becomes tender on the outside (20 minutes).", ["step-3a", "step-3b"]),
            ("Strain the sauce, discard the spices, mash the vegetables and mix them into the sauce. Blend in the sour cream and simmer for a few minutes. The sauce should be medium thick.", ["step-4"]),
            ("Slice the roast, pour some sauce over it and serve the remainder in a sauce dish.", ["step-5"]),
            ("It is important that you make enough sauce, adding beef stock and sour cream. Taste it and add salt, pepper, lemon juice – if needed. The taste should be mildly piquant. The typical accompaniment is crouton or yeast dumplings, or noodles.", ["step-6a", "step-6b"]),
        ],
        "yield": "Serves 6 – Preparation time: 2 hours",
        "notes": [
            ("Alternative – Lard the tenderloin, grease a roasting pan with oil, cover the bottom of the pan with the vegetables, lay the roast on top, add more vegetables, spices and lemon juice. Add the remaining oil, cover and marinate overnight. Next day prepare the roast as indicated above.", "alternative"),
            ("⟦outlined right-arrow glyph⟧ If planning to prepare a larger quantity, for example a whole tenderloin, increase all ingredients accordingly. Instead of browning the roast by frying, roast it on all sides in a hot oven (475F), then lower the temperature to 350F and proceed as shown above.", "tip"),
        ],
        "status": "needs_attention",
        "segment_uncertainties": {
            "note-2": [
                {
                    "substring": "⟦outlined right-arrow glyph⟧",
                    "issue": "ambiguous_glyph",
                    "note": "The scan clearly shows an outlined right-arrow ornament, but its exact character encoding is unresolved; the bracketed text is an explicit placeholder, not a Unicode guess.",
                }
            ]
        },
        "open_issues": [
            issue("r0001-note-glyph", ["note-2"], "Exact character identity of the outlined right-arrow ornament before the final note is unresolved; retain the explicit placeholder until a human determines the intended encoding or approves treating it as non-text decoration.", "textual"),
        ],
    },
    {
        "recipe_id": "vera-r0002",
        "source_order": 2,
        "slug": "beef-tenderloin-slices",
        "pages": [5],
        "printed_pages": ["4"],
        "display_title": "Beef tenderloin slices (shortcut for “svíčková”) · Řezy ze svíčkové",
        "titles": [
            ("en", "primary", "Beef tenderloin slices (shortcut for “svíčková”)"),
            ("cs", "parallel", "Řezy ze svíčkové"),
        ],
        "regions": [
            ("title", "title", 5, ["/page/4/SectionHeader/1"]),
            ("ingredients", "ingredient", 5, ["/page/4/ListGroup/2"]),
            ("step-1", "instruction", 5, ["/page/4/Text/4"]),
            ("step-2", "instruction", 5, ["/page/4/Text/5"]),
            ("step-3", "instruction", 5, ["/page/4/Text/6"]),
            ("yield", "yield-time", 5, ["/page/4/Text/7"]),
        ],
        "ingredients": [
            "4 lbs. beef tenderloin",
            "3 slices bacon",
            "4 tablespoons vegetable oil",
            "4 tablespoons butter",
            "1 medium size onion, chopped",
            "2 pickled cucumbers (sour), sliced",
            "2 canned fillets of anchovies, chopped",
            "3 teaspoons capers",
            "chopped parsley, thyme, marjoram, lemon rind",
            "1·1/2 cups sour cream",
            "2 tablespoons flour",
            "1·1/2 cups chicken or beef stock, or water",
            "salt and pepper",
        ],
        "steps": [
            ("Cut the tenderloin into 1” thick slices. Pound each slice with the palm of your hand and lard with half slice bacon each. Salt and pepper them lightly and fry in hot oil about 2·1/2 minutes on each side. Place them in a casserole, keep them warm.", ["step-1"]),
            ("In a saucepan combine melted butter, onion, pickles, anchovies, parsley, capers, lemon rind, marjoram and thyme and brown all. Add flour, brown a little more. Add stock or water, sour cream. Simmer for five minutes, strain and pour over the meat slices. Simmer until heated through.", ["step-2"]),
            ("Serve with dumplings, gnocchi, rice, noodles.", ["step-3"]),
        ],
        "yield": "Serves 6 – Preparation time: 1 hour",
        "notes": [],
        "status": "source_checked",
        "open_issues": [],
    },
    {
        "recipe_id": "vera-r0003",
        "source_order": 3,
        "slug": "beef-croquettes",
        "pages": [5],
        "printed_pages": ["4"],
        "display_title": "Beef croquettes · Karbanátky",
        "titles": [
            ("en", "primary", "Beef croquettes"),
            ("cs", "parallel", "Karbanátky"),
        ],
        "regions": [
            ("title", "title", 5, ["/page/4/SectionHeader/8"]),
            ("ingredients", "ingredient", 5, ["/page/4/ListGroup/3"]),
            ("step-1", "instruction", 5, ["/page/4/Text/9"]),
            ("step-2", "instruction", 5, ["/page/4/Text/10"]),
            ("step-3", "instruction", 5, ["/page/4/Text/11"]),
            ("step-4", "instruction", 5, ["/page/4/Text/12"]),
            ("yield", "yield-time", 5, ["/page/4/Text/13"]),
        ],
        "ingredients": [
            "2 lbs. ground round",
            "1 whole egg",
            "2 hard baked rolls",
            "2 slices bacon",
            "salt, pepper, marjoram",
            "1 medium size onion",
            "3/4 cup water",
            "3/4 cup bread crumbs",
            "1/2 cup oil for frying",
        ],
        "steps": [
            ("Soak the rolls in water, squeeze off excess liquid, shred them. Blend them with the ground meat, egg, chopped onion, diced bacon, salt, pepper and marjoram.", ["step-1"]),
            ("Form 12 hamburgers, coat them with bread crumbs and fry on both sides.", ["step-2"]),
            ("Instead of frying, they can be roasted in the oven, basting them with hot oil, their own juices, chicken or beef stock, or water.", ["step-3"]),
            ("Serve with mashed potatoes and salad. Or serve cold with dark bread, potato salad, or pickles.", ["step-4"]),
        ],
        "yield": "Serves 6 – Preparation time: 1 hour",
        "notes": [],
        "status": "source_checked",
        "open_issues": [],
    },
    {
        "recipe_id": "vera-r0031",
        "source_order": 31,
        "slug": "roast-goose",
        "pages": [24, 25],
        "printed_pages": ["23", "24"],
        "display_title": "Roast goose · Husa pečená",
        "titles": [
            ("en", "primary", "Roast goose"),
            ("cs", "parallel", "Husa pečená"),
        ],
        "regions": [
            ("title", "title", 24, ["/page/23/SectionHeader/14"]),
            ("ingredients", "ingredient", 24, ["/page/23/ListGroup/15"]),
            ("step-1", "instruction", 24, ["/page/23/Text/16"]),
            ("step-2", "instruction", 24, ["/page/23/Text/17"]),
            ("step-3a", "continuation", 24, ["/page/23/Text/18"]),
            ("step-3b", "continuation", 25, ["/page/24/Text/0"]),
            ("yield", "yield-time", 25, ["/page/24/Text/1"]),
        ],
        "ingredients": [
            "1 goose, 10 lbs.",
            "4·5 medium apples",
            "salt, caraway seeds",
            "water",
        ],
        "steps": [
            ("Rinse goose, pat dry. Rinse the apples-do not peel them. Rub the goose inside and out with salt and caraway seeds. Fill body cavity with apples.", ["step-1"]),
            ("Place goose in a roasting pan with a little hot water at the bottom.", ["step-2"]),
            ("Roast at 350F, first breast side down for 1·1/2 hrs, basting with water and pan drippings. When golden brown on top, turn goose breast side up. Continue roasting for 1-1/2 hours. While roasting, prick the skin with a fork over the fatty areas to release fat. (Just the skin, not the meat. If the juice from the meat runs out, the goose will become dry.) Total roasting time is approximately 20 minutes per pound. During the last 15 minutes of roasting, raise oven temperature to 400F and stop basting to achieve a crunchy skin. Remove apples and slice goose. Skim fat from pan juices and pour into a gravy boat to accompany goose. Serve with dumplings, potato dumplings, cabbage, red cabbage, sauerkraut.", ["step-3a", "step-3b"]),
        ],
        "yield": "Serves 8-10 – Preparation time: 3 hours 30 minutes",
        "notes": [],
        "status": "source_checked",
        "open_issues": [],
    },
    {
        "recipe_id": "vera-r0079",
        "source_order": 79,
        "slug": "vanilla-sauce",
        "pages": [52],
        "printed_pages": ["51"],
        "display_title": "Vanilla sauce - Vanilková omáčka",
        "titles": [
            ("en", "primary", "Vanilla sauce"),
            ("cs", "parallel", "Vanilková omáčka"),
        ],
        "regions": [
            ("title", "title", 52, ["/page/51/SectionHeader/7"]),
            ("ingredients", "ingredient", 52, ["/page/51/ListGroup/2"]),
            ("step-1", "instruction", 52, ["/page/51/Text/8"]),
            ("yield", "yield-time", 52, ["/page/51/Text/9"]),
        ],
        "ingredients": [
            "2 cups milk, or light cream",
            "4 egg yolks",
            "1/2 cup sugar",
            "1 teaspoon vanilla sugar",
            "1 tablespoon corn starch",
        ],
        "steps": [
            ("In a saucepan cream egg yolks, sugar mixed with vanilla sugar, corn starch. Gradually add hot milk or cream, stirring constantly. Set over low heat, bring to boiling, stirring steadily until desired thickness is reached. Sauce should be medium thick. Strain, serve warm.", ["step-1"]),
        ],
        "yield": "Serves 10 – Preparation time: 30 minutes",
        "notes": [],
        "status": "source_checked",
        "open_issues": [],
    },
]


def source_digest() -> str:
    return hashlib.sha256(SOURCE_PDF.read_bytes()).hexdigest()


def render_page(pdf_page: int) -> Path:
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = PAGE_DIR / f"page-{pdf_page:02d}.png"
    if path.exists():
        return path
    prefix = path.with_suffix("")
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            str(pdf_page),
            "-l",
            str(pdf_page),
            "-singlefile",
            "-r",
            "144",
            "-png",
            str(SOURCE_PDF),
            str(prefix),
        ],
        check=True,
    )
    return path


def pixel_hash(image: Image.Image) -> str:
    payload = f"{image.width}x{image.height}|{image.mode}|".encode() + image.tobytes()
    return hashlib.sha256(payload).hexdigest()


def page_index(page: dict[str, Any]) -> int:
    match = re.search(r"/page/(\d+)/", page["id"])
    if not match:
        raise ValueError(f"Cannot parse page index from {page['id']}")
    return int(match.group(1))


def marker_pages() -> dict[int, dict[str, Any]]:
    document = json.loads(MARKER_JSON.read_text(encoding="utf-8"))
    return {page_index(page) + 1: page for page in document["children"]}


def block_lookup(page: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {block["id"]: block for block in page.get("children", [])}


def crop_region(
    recipe_id: str,
    region_key: str,
    pdf_page: int,
    block_ids: list[str],
    page: dict[str, Any],
) -> tuple[dict[str, Any], tuple[int, int, int, int]]:
    page_path = render_page(pdf_page)
    with Image.open(page_path) as page_image:
        image = page_image.convert("RGB")
        page_polygon = page["polygon"]
        marker_width = max(point[0] for point in page_polygon)
        marker_height = max(point[1] for point in page_polygon)
        scale_x = image.width / marker_width
        scale_y = image.height / marker_height
        blocks = block_lookup(page)
        manual_bbox_prefix = "manual-bbox:"
        if len(block_ids) == 1 and block_ids[0].startswith(manual_bbox_prefix):
            # Preserve the raw Marker artifact when it misses a source-clear
            # layout block. The explicit Marker-coordinate box remains visible
            # in provenance rather than inventing a Marker block identifier.
            try:
                left_marker, top_marker, right_marker, bottom_marker = (
                    float(value)
                    for value in block_ids[0][len(manual_bbox_prefix) :].split(",")
                )
            except ValueError as exc:
                raise ValueError(f"Invalid manual crop box: {block_ids[0]}") from exc
            x_values = [left_marker, right_marker]
            y_values = [top_marker, bottom_marker]
        else:
            selected = []
            for block_id in block_ids:
                if block_id not in blocks:
                    raise KeyError(f"Missing Marker block {block_id}")
                selected.append(blocks[block_id])
            x_values = [point[0] for block in selected for point in block["polygon"]]
            y_values = [point[1] for block in selected for point in block["polygon"]]
        padding = 18
        left = max(0, int(min(x_values) * scale_x) - padding)
        top = max(0, int(min(y_values) * scale_y) - padding)
        right = min(image.width, int(max(x_values) * scale_x) + padding)
        bottom = min(image.height, int(max(y_values) * scale_y) + padding)
        cropped = image.crop((left, top, right, bottom))
        output_dir = REGION_DIR / recipe_id
        output_dir.mkdir(parents=True, exist_ok=True)
        crop_path = output_dir / f"p{pdf_page:02d}-{region_key}.png"
        cropped.save(crop_path, optimize=True)
        role = next(
            role for key, role, candidate_page, ids in next(
                recipe["regions"] for recipe in RECIPES if recipe["recipe_id"] == recipe_id
            )
            if key == region_key and candidate_page == pdf_page and ids == block_ids
        )
        if region_key == "yield" or role == "yield-time":
            role = YIELD_ROLE
        region_id = f"{recipe_id}-{region_key}"
        return (
            {
                "region_id": region_id,
                "pdf_page": pdf_page,
                "printed_page": str(pdf_page - 1),
                "role": role,
                "coordinate_space": {
                    "unit": "pixel",
                    "width": image.width,
                    "height": image.height,
                    "origin": "top_left",
                },
                "polygon": [[left, top], [right, top], [right, bottom], [left, bottom]],
                "candidate_block_ids": block_ids,
                "region_image": str(crop_path.relative_to(PROJECT_DIR)),
                "region_image_pixel_sha256": pixel_hash(cropped),
            },
            (left, top, right, bottom),
        )


def write_overviews(recipe: dict[str, Any], boxes: dict[int, list[tuple[int, int, int, int]]]) -> list[Path]:
    output_dir = OVERVIEW_DIR / recipe["recipe_id"]
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for pdf_page, page_boxes in sorted(boxes.items()):
        with Image.open(render_page(pdf_page)) as page_image:
            image = page_image.convert("RGB")
            left = max(0, min(box[0] for box in page_boxes) - 24)
            top = max(0, min(box[1] for box in page_boxes) - 24)
            right = min(image.width, max(box[2] for box in page_boxes) + 24)
            bottom = min(image.height, max(box[3] for box in page_boxes) + 24)
            crop = image.crop((left, top, right, bottom))
            path = output_dir / f"page-{pdf_page:02d}.png"
            crop.save(path, optimize=True)
            paths.append(path)
    return paths


def region_id(recipe_id: str, key: str) -> str:
    return f"{recipe_id}-{key}"


def build_record(recipe: dict[str, Any], source_regions: list[dict[str, Any]]) -> dict[str, Any]:
    rid = recipe["recipe_id"]
    title_region = region_id(rid, "title")
    titles = []
    for index, (language, role, text) in enumerate(recipe["titles"], start=1):
        titles.append(
            {
                "segment_id": f"title-{'en' if language == 'en' else 'cs' if language == 'cs' else index}",
                "text_verbatim": text,
                "language": language,
                "source_region_ids": [title_region],
                "title_role": role,
            }
        )
    ingredients = [
        {
            "segment_id": f"ingredient-{index}",
            "text_verbatim": text,
            "language": "en",
            "source_region_ids": [region_id(rid, "ingredients")],
        }
        for index, text in enumerate(recipe["ingredients"], start=1)
    ]
    steps = [
        {
            "segment_id": f"step-{index}",
            "step_number": index,
            "text_verbatim": text,
            "language": "en",
            "source_region_ids": [region_id(rid, key) for key in region_keys],
        }
        for index, (text, region_keys) in enumerate(recipe["steps"], start=1)
    ]
    notes = [
        {
            "segment_id": f"note-{index}",
            "text_verbatim": text,
            "language": "en",
            "source_region_ids": [region_id(rid, key)],
        }
        for index, (text, key) in enumerate(recipe["notes"], start=1)
    ]
    for note in notes:
        uncertainties = recipe.get("segment_uncertainties", {}).get(note["segment_id"])
        if uncertainties:
            note["uncertainties"] = uncertainties
    relationships: dict[str, Any] = {"continuations": [], "related_recipe_ids": []}
    if rid == "vera-r0031":
        relationships["continuations"].append(
            {
                "from_region_id": region_id(rid, "step-3a"),
                "to_region_id": region_id(rid, "step-3b"),
                "relationship": "continues_on",
            }
        )
    record = {
        "schema_version": "1.2.0",
        "record_type": "recipe",
        "recipe_id": rid,
        "record_revision": 2,
        "source_work": {
            "work_id": "vera-culinary-adventures",
            "source_file": "source/Culinary Adventures - Vera Gaeta.pdf",
            "source_sha256": SOURCE_SHA256,
            "pdf_page_count": 75,
            "pdf_pages": recipe["pages"],
            "printed_pages": recipe["printed_pages"],
            "rights_status": "not_assessed",
        },
        "source_regions": source_regions,
        "identity": {
            "display_title": {
                "segment_id": "title-display",
                "text_verbatim": recipe["display_title"],
                "language": "mul",
                "source_region_ids": [title_region],
            },
            "titles": titles,
            "source_order": recipe["source_order"],
            "slug_candidate": recipe["slug"],
        },
        "transcription": {
            "yield_time_lines": [
                {
                    "segment_id": "yield-1",
                    "text_verbatim": recipe["yield"],
                    "language": "en",
                    "source_region_ids": [region_id(rid, "yield")],
                }
            ],
            "ingredient_sections": [
                {"section_id": "ingredients-main", "ingredients": ingredients}
            ],
            "instruction_sections": [
                {"section_id": "instructions-main", "steps": steps}
            ],
            "notes": notes,
            "cross_references": [],
        },
        "relationships": relationships,
        "provenance": {
            "created_at": "2026-08-23T20:00:00Z",
            "created_by": "codex-preflight",
            "candidate_sources": [
                {
                    "tool": "marker-pdf",
                    "tool_version": "2.0.0",
                    "generated_at": "2026-08-23T19:59:12Z",
                    "artifact_path": "pilot/production-batch-001/marker-output/Culinary Adventures - Vera Gaeta/Culinary Adventures - Vera Gaeta.json",
                    "remote_model_used": False,
                }
            ],
        },
    }
    record["verification"] = build_verification(record, recipe)
    return record


def record_segments(record: dict[str, Any]) -> list[dict[str, Any]]:
    found = [record["identity"]["display_title"], *record["identity"]["titles"]]
    transcription = record["transcription"]
    found.extend(transcription.get("headnotes", []))
    found.extend(transcription.get(YIELD_LINES_KEY, []))
    for section in transcription["ingredient_sections"]:
        if section.get("label"):
            found.append(section["label"])
        found.extend(section["ingredients"])
    for section in transcription["instruction_sections"]:
        if section.get("label"):
            found.append(section["label"])
        found.extend(section["steps"])
    found.extend(transcription.get("notes", []))
    found.extend(transcription.get("cross_references", []))
    return found


def ordered_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def build_verification(record: dict[str, Any], recipe: dict[str, Any]) -> dict[str, Any]:
    rid = record["recipe_id"]
    segments = record_segments(record)
    by_id = {segment["segment_id"]: segment for segment in segments}
    all_regions = [region["region_id"] for region in record["source_regions"]]
    ingredient_ids = [
        item["segment_id"]
        for section in record["transcription"]["ingredient_sections"]
        for item in section["ingredients"]
    ]
    instruction_ids = [
        item["segment_id"]
        for section in record["transcription"]["instruction_sections"]
        for item in section["steps"]
    ]
    yield_ids = [
        item["segment_id"]
        for item in record["transcription"].get(YIELD_LINES_KEY, [])
    ]
    segment_ids = list(by_id)
    numeric_ids = [
        segment_id
        for segment_id, segment in by_id.items()
        if any(character.isdigit() for character in segment["text_verbatim"])
    ]
    diacritic_ids = [
        segment_id
        for segment_id, segment in by_id.items()
        if any(
            ord(character) > 127 and character.isalpha()
            for character in segment["text_verbatim"]
        )
    ]

    def source_ids(target_ids: list[str]) -> list[str]:
        return ordered_unique(
            [
                source_id
                for target_id in target_ids
                for source_id in by_id[target_id]["source_region_ids"]
            ]
        )

    def audit_check(
        check_id: str,
        check_type: str,
        target_ids: list[str],
        source_region_ids: list[str],
        result: str = "pass",
        note: str | None = None,
    ) -> dict[str, Any]:
        check: dict[str, Any] = {
            "check_id": check_id,
            "check_type": check_type,
            "target_ids": target_ids,
            "source_region_ids": source_region_ids,
            "result": result,
            "method": "direct_visual_source",
            "performed_by": "ai",
            "auditor_id": AUDITOR_ID,
            "audited_at": AUDIT_AT,
            "independent_of_extractor": True,
        }
        if note:
            check["note"] = note
        return check

    exact_ids = [
        segment_id
        for segment_id in segment_ids
        if not by_id[segment_id].get("uncertainties")
    ]
    checks = [
        audit_check(
            "ai-region-coverage",
            "region_coverage",
            [rid],
            all_regions,
            note="Every cited region and full-page layout context was inspected locally.",
        ),
        audit_check(
            "ai-recipe-boundary",
            "recipe_boundary",
            [rid],
            all_regions,
            note="Recipe ownership was checked against neighboring content on every cited page.",
        ),
        audit_check(
            (
                "ai-ingredient-ownership"
                if ingredient_ids
                else "ai-ingredient-list-presence"
            ),
            "ingredient_ownership" if ingredient_ids else "ingredient_list_presence",
            ingredient_ids or [rid],
            (
                ordered_unique([region_id(rid, "title"), *source_ids(ingredient_ids)])
                if ingredient_ids
                else all_regions
            ),
            note=(
                None
                if ingredient_ids
                else "The complete recipe context was inspected and the source prints no ingredient list."
            ),
        ),
        audit_check(
            "ai-instruction-ownership",
            "instruction_ownership",
            instruction_ids,
            ordered_unique([region_id(rid, "title"), *source_ids(instruction_ids)]),
        ),
        audit_check(
            "ai-transcription-exactness",
            "transcription_exactness",
            exact_ids,
            source_ids(exact_ids),
            note="All source-clear spelling, punctuation, omissions, and printed separators match the cited scans.",
        ),
        audit_check(
            "ai-numeric-tokens",
            "numeric_tokens",
            numeric_ids,
            source_ids(numeric_ids),
            note="Every visible quantity, fraction separator, temperature, time, and yield number was compared directly.",
        ),
        audit_check(
            "ai-yield-time-presence",
            YIELD_ROLE + "_presence",
            yield_ids or [rid],
            source_ids(yield_ids) if yield_ids else all_regions,
            note=(
                "Every printed yield/preparation-time line was compared directly."
                if yield_ids
                else "The full recipe context was inspected and no printed yield/preparation-time line is present."
            ),
        ),
        audit_check(
            "ai-occurrence-count",
            "occurrence_count",
            [rid],
            all_regions,
            note="Repeated and visually omitted candidate text was checked against the page layout.",
        ),
        *(
            [
                audit_check(
                    "ai-diacritics",
                    "diacritics",
                    diacritic_ids,
                    source_ids(diacritic_ids),
                    note="All visible Czech diacritics were compared character by character.",
                )
            ]
            if diacritic_ids
            else []
        ),
    ]
    if len(record["source_work"]["pdf_pages"]) > 1 or record["relationships"]["continuations"]:
        checks.append(
            audit_check(
                "ai-continuation",
                "continuation",
                instruction_ids,
                source_ids(instruction_ids),
                note=(
                    "Every declared cross-page continuation was followed directly across its cited regions."
                    if record["relationships"]["continuations"]
                    else "Every cited page of this multi-page recipe layout was inspected; no literal sentence continuation is declared."
                ),
            )
        )
    cross_reference_ids = [
        item["segment_id"] for item in record["transcription"].get("cross_references", [])
    ]
    if cross_reference_ids:
        checks.append(
            audit_check(
                "ai-cross-reference",
                "cross_reference",
                cross_reference_ids,
                source_ids(cross_reference_ids),
                note="Every cross-reference was compared with its printed wording and visible destination context.",
            )
        )
    ambiguous_ids = [
        segment_id for segment_id in segment_ids if by_id[segment_id].get("uncertainties")
    ]
    if ambiguous_ids:
        checks.append(
            audit_check(
                "ai-transcription-ambiguity",
                "transcription_exactness",
                ambiguous_ids,
                source_ids(ambiguous_ids),
                result="ambiguous",
                note=recipe.get(
                    "ambiguity_note",
                    "The cited source contains a genuine transcription ambiguity that cannot be resolved without guessing.",
                ),
            )
        )
    return {
        "status": recipe["status"],
        "audit_policy": "source_audit",
        "status_set_at": AUDIT_AT,
        "checks": checks,
        "open_issues": recipe["open_issues"],
    }


def risk_tokens(record: dict[str, Any]) -> list[str]:
    texts = []
    texts.append(record["identity"]["display_title"]["text_verbatim"])
    transcription = record["transcription"]
    texts.extend(item["text_verbatim"] for item in transcription[YIELD_LINES_KEY])
    texts.extend(
        item["text_verbatim"]
        for section in transcription["ingredient_sections"]
        for item in section["ingredients"]
    )
    texts.extend(
        item["text_verbatim"]
        for section in transcription["instruction_sections"]
        for item in section["steps"]
    )
    tokens: list[str] = []
    for text in texts:
        for match in re.findall(
            r"\b\d+(?:[-·]\d+)?(?:/\d+)?(?:F|[\"”])?|\b\d+[-·]\d+\b", text
        ):
            if match not in tokens:
                tokens.append(match)
    return tokens


def render_review_html(records: list[dict[str, Any]], overviews: dict[str, list[Path]]) -> str:
    cards = []
    checklist = [
        "Page and region coverage is complete",
        "Recipe boundaries are correct",
        "Every instruction belongs to this recipe",
        "Verbatim spelling and punctuation match",
        "Numbers, fractions, units, times, and temperatures match",
        "Yield/preparation-time presence is correct",
        "Repeated text occurrence count is correct",
    ]
    for record in records:
        rid = record["recipe_id"]
        title = record["identity"]["display_title"]["text_verbatim"]
        status = record["verification"]["status"]
        status_label = status.replace("_", " ")
        page_label = ", ".join(map(str, record["source_work"]["pdf_pages"]))
        overview_html = "".join(
            f'<figure><a href="../../{html.escape(str(path.relative_to(PROJECT_DIR)))}">'
            f'<img loading="lazy" src="../../{html.escape(str(path.relative_to(PROJECT_DIR)))}" '
            f'alt="Source page context for {html.escape(title)}"></a>'
            f'<figcaption>{html.escape(path.stem.replace("page-", "PDF page "))} context</figcaption></figure>'
            for path in overviews[rid]
        )
        region_html = "".join(
            f'<figure class="region-crop"><a href="../../{html.escape(region["region_image"])}">'
            f'<img loading="lazy" src="../../{html.escape(region["region_image"])}" '
            f'alt="Exact cited {html.escape(region["role"])} crop for {html.escape(title)} on PDF page {region["pdf_page"]}"></a>'
            f'<figcaption>{html.escape(region["region_id"].removeprefix(rid + "-").replace("-", " "))} · PDF {region["pdf_page"]}</figcaption></figure>'
            for region in record["source_regions"]
        )
        ingredients = "".join(
            (
                f"<h5>{html.escape(section['label']['text_verbatim'])}</h5>"
                if section.get("label")
                else ""
            )
            + "<ul>"
            + "".join(
                f"<li>{html.escape(item['text_verbatim'])}</li>"
                for item in section["ingredients"]
            )
            + "</ul>"
            for section in record["transcription"]["ingredient_sections"]
        )
        if not ingredients:
            ingredients = "<p><em>No printed ingredient list.</em></p>"
        steps = "".join(
            (
                f"<h5>{html.escape(section['label']['text_verbatim'])}</h5>"
                if section.get("label")
                else ""
            )
            + "<ol>"
            + "".join(
                f"<li>{html.escape(item['text_verbatim'])}</li>"
                for item in section["steps"]
            )
            + "</ol>"
            for section in record["transcription"]["instruction_sections"]
        )
        notes = "".join(
            f"<li>{html.escape(item['text_verbatim'])}</li>"
            for item in record["transcription"].get("notes", [])
        )
        cross_references = "".join(
            f"<li>{html.escape(item['text_verbatim'])}</li>"
            for item in record["transcription"].get("cross_references", [])
        )
        yield_lines = record["transcription"].get(YIELD_LINES_KEY, [])
        yield_html = (
            "".join(
                f"<p>{html.escape(item['text_verbatim'])}</p>" for item in yield_lines
            )
            if yield_lines
            else "<p><em>No printed yield/preparation-time line.</em></p>"
        )
        issue_items = "".join(
            f"<li><span>{html.escape(item['severity'])}</span>{html.escape(item['description'])}</li>"
            for item in record["verification"]["open_issues"]
        )
        issues = (
            f"<ul>{issue_items}</ul>"
            if issue_items
            else "<p>No unresolved source ambiguities.</p>"
        )
        ingredient_check = (
            "Every ingredient belongs to this recipe"
            if record["transcription"]["ingredient_sections"]
            else "The source contains no printed ingredient list"
        )
        record_checklist = [checklist[0], checklist[1], ingredient_check, *checklist[2:]]
        checks = "".join(
            f'<label><input type="checkbox" data-recipe="{rid}"><span>{html.escape(text)}</span></label>'
            for text in record_checklist
        )
        cards.append(
            f"""
            <article class="recipe" id="{rid}">
              <header class="recipe-head">
                <div><h2>{html.escape(title)}</h2><p class="record-meta">{rid} · PDF {page_label} · AI source audit</p></div>
                <div class="record-actions"><a href="../../data/recipes/{rid}.yaml">Open YAML</a><span class="status status-{status}">{html.escape(status_label)}</span></div>
              </header>
              <div class="compare">
                <section class="source-disclosure" data-source="{rid}">
                  <button class="source-toggle" type="button" aria-expanded="false" aria-controls="source-panel-{rid}" aria-label="View source for {html.escape(title)}" data-source-title="{html.escape(title)}"><span class="source-toggle-label">View source</span><small>{len(record['source_regions'])} cited regions</small><span class="source-toggle-icon" aria-hidden="true">+</span></button>
                  <div class="source-panel" id="source-panel-{rid}" hidden>
                    <h3>Recipe context</h3><div class="overview-grid">{overview_html}</div>
                    <details class="region-disclosure">
                      <summary>View exact cited regions</summary>
                      <div class="region-grid">{region_html}</div>
                    </details>
                  </div>
                </section>
                <section class="candidate">
                  <h3>Canonical transcription</h3>
                  <p class="verbatim-title">{html.escape(title)}</p>
                  <h4>Ingredients</h4>{ingredients}
                  <h4>Instructions</h4>{steps}
                  <h4>Yield / time</h4>{yield_html}
                  {f'<h4>Notes</h4><ul>{notes}</ul>' if notes else ''}
                  {f'<h4>Cross-references</h4><ul>{cross_references}</ul>' if cross_references else ''}
                </section>
              </div>
              <div class="risk"><h3>Audit findings</h3>{issues}<p><b>Checked high-risk tokens:</b> {html.escape(' · '.join(risk_tokens(record)))}</p></div>
              <fieldset><legend>Optional human verification checklist</legend>{checks}</fieldset>
            </article>
            """
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vera Cookbook · {html.escape(BATCH_TITLE)}</title>
<style>
:root {{ --ink:#27231d; --paper:#f3eee3; --card:#fffdf6; --rule:#b9aa92; --accent:#8f2924; --green:#245c47; --muted:#685d4d; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; color:var(--ink); background:var(--paper); font:16px/1.55 Palatino, "Book Antiqua", Georgia, serif; }}
.mast {{ padding:64px max(24px,6vw) 46px; border-bottom:1px solid var(--rule); background:#e5dac5; }}
h1 {{ max-width:920px; margin:0 0 16px; font-size:clamp(42px,7vw,88px); line-height:.96; font-weight:500; letter-spacing:-.035em; text-wrap:balance; }}
.mast p {{ max-width:760px; margin:0; font-size:19px; line-height:1.55; }}
.toolbar {{ position:sticky; top:0; z-index:5; display:flex; flex-wrap:wrap; gap:10px 14px; align-items:center; padding:12px max(24px,6vw); background:#f3eee3; border-bottom:1px solid var(--rule); }}
.toolbar button {{ min-height:44px; border:1px solid var(--ink); background:var(--ink); color:#fff; padding:10px 16px; border-radius:999px; font:700 12px ui-monospace,SFMono-Regular,monospace; cursor:pointer; }}
.toolbar button.secondary {{ background:transparent; color:var(--ink); }}
.toolbar output {{ margin-inline-start:auto; font:700 13px ui-monospace,SFMono-Regular,monospace; }}
.toolbar span {{ color:var(--muted); }}
main {{ width:min(1500px,94vw); margin:42px auto 90px; display:grid; gap:42px; }}
.recipe {{ min-width:0; overflow:hidden; background:var(--card); border:1px solid var(--rule); border-radius:14px; }}
.recipe-head {{ display:flex; justify-content:space-between; gap:20px; align-items:flex-start; padding:28px 32px; border-bottom:1px solid var(--rule); }}
.recipe h2 {{ margin:0; font-size:clamp(25px,3vw,42px); line-height:1.08; font-weight:500; overflow-wrap:anywhere; }}
.record-meta {{ margin:8px 0 0; color:var(--muted); font:12px/1.4 ui-monospace,SFMono-Regular,monospace; }}
.record-actions {{ display:flex; flex-wrap:wrap; justify-content:flex-end; align-items:center; gap:12px; flex:none; }}
.record-actions a {{ color:var(--ink); font:700 11px ui-monospace,SFMono-Regular,monospace; text-transform:uppercase; letter-spacing:.08em; }}
.status {{ flex:none; border:1px solid var(--accent); color:var(--accent); padding:7px 11px; border-radius:999px; font:700 11px ui-monospace,SFMono-Regular,monospace; text-transform:uppercase; letter-spacing:.1em; }}
.status-source_checked {{ border-color:var(--green); color:var(--green); }}
.compare {{ display:grid; grid-template-columns:auto minmax(0,1fr); }}
.source-disclosure {{ width:max-content; max-width:100%; border-inline-end:1px solid var(--rule); }}
.source-disclosure.is-open {{ width:min(720px,48vw); }}
.source-toggle {{ display:flex; width:100%; min-height:52px; align-items:center; gap:12px; padding:14px 18px; border:0; color:#fff; background:var(--ink); cursor:pointer; font:700 13px ui-monospace,SFMono-Regular,monospace; text-align:left; }}
.region-disclosure>summary::-webkit-details-marker {{ display:none; }}
.source-toggle small {{ color:#e8dcc8; font:11px ui-monospace,SFMono-Regular,monospace; white-space:nowrap; }}
.source-toggle-icon {{ margin-inline-start:auto; font-size:20px; line-height:1; }}
.source-panel {{ padding:24px; }}
.overview-grid {{ display:grid; gap:18px; }}
.region-disclosure {{ margin-top:22px; border-top:1px solid var(--rule); }}
.region-disclosure>summary {{ min-height:44px; padding:14px 0; color:var(--accent); cursor:pointer; font-weight:700; }}
.region-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }}
.candidate {{ min-width:0; padding:28px 32px; }}
h3 {{ margin:0 0 18px; font:700 13px ui-monospace,SFMono-Regular,monospace; text-transform:uppercase; letter-spacing:.14em; }}
h4 {{ margin:24px 0 7px; font-size:16px; }}
h5 {{ margin:18px 0 6px; color:var(--accent); font:700 12px ui-monospace,SFMono-Regular,monospace; text-transform:uppercase; letter-spacing:.1em; }}
figure {{ margin:0 0 20px; }}
figure a {{ display:block; }}
figure img {{ display:block; width:100%; max-height:720px; object-fit:contain; object-position:top; background:#eee4d4; border:1px solid #d8ccb8; }}
.region-crop img {{ height:150px; object-fit:contain; }}
figcaption {{ margin-top:6px; color:var(--muted); font:12px ui-monospace,SFMono-Regular,monospace; overflow-wrap:anywhere; }}
.candidate ul,.candidate ol {{ padding-left:22px; }}
.candidate li,.candidate p {{ max-width:75ch; margin:0 0 8px; line-height:1.5; overflow-wrap:anywhere; }}
.verbatim-title {{ padding:12px 14px; background:#f2eadc; border:1px solid #d9cbb5; }}
.risk {{ padding:24px 32px; border-top:1px solid var(--rule); border-bottom:1px solid var(--rule); background:#f8eee7; }}
.risk ul {{ margin:0 0 12px; padding-left:20px; }}
.risk li,.risk p {{ max-width:100ch; margin:8px 0; line-height:1.45; overflow-wrap:anywhere; }}
.risk li span {{ margin-right:9px; color:var(--accent); font:700 10px ui-monospace,SFMono-Regular,monospace; text-transform:uppercase; letter-spacing:.1em; }}
fieldset {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px 24px; margin:0; padding:24px 32px 30px; border:0; }}
legend {{ padding-top:24px; font:700 13px ui-monospace,SFMono-Regular,monospace; text-transform:uppercase; letter-spacing:.14em; }}
label {{ display:flex; gap:10px; align-items:flex-start; line-height:1.35; cursor:pointer; }}
input {{ appearance:none; width:20px; height:20px; flex:none; margin:1px 0 0; border:1px solid #75664f; background:#fff; }}
input:checked {{ background:var(--green); box-shadow:inset 0 0 0 4px #fff; }}
a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible {{ outline:3px solid #146b8c; outline-offset:3px; }}
#copy-feedback {{ min-width:16ch; color:var(--green); font-weight:700; }}
@media (hover:hover) {{ .source-toggle:hover,.toolbar button:hover {{ filter:brightness(1.16); }} .record-actions a:hover {{ color:var(--accent); }} }}
@media (max-width:900px) {{
  .recipe-head {{ flex-direction:column; }} .record-actions {{ justify-content:flex-start; }}
  .compare {{ grid-template-columns:1fr; }} .source-disclosure,.source-disclosure.is-open {{ width:100%; border-inline-end:0; border-bottom:1px solid var(--rule); }}
  .region-grid,fieldset {{ grid-template-columns:1fr; }} .toolbar output {{ margin-inline-start:0; }}
}}
@media (max-width:560px) {{ .mast {{ padding-block:44px 34px; }} .recipe-head,.candidate,.risk,fieldset {{ padding-inline:20px; }} .toolbar span:not(#copy-feedback) {{ width:100%; }} }}
@media (prefers-reduced-motion:reduce) {{ * {{ scroll-behavior:auto!important; }} }}
@media print {{ .toolbar {{ display:none; }} body {{ background:#fff; }} .recipe {{ break-before:page; }} .source-disclosure {{ width:48%!important; }} }}
</style>
</head>
<body>
<header class="mast"><h1>{html.escape(BATCH_TITLE)}</h1><p>{BATCH_SUMMARY}</p></header>
<div class="toolbar"><button type="button" onclick="window.print()">Print review packet</button><button type="button" class="secondary" onclick="copyStatus()">Copy checklist status</button><span>Optional human checks persist in this browser only.</span><output id="progress">0 / {len(records) * (len(checklist) + 1)} checked</output><span id="copy-feedback" role="status" aria-live="polite"></span></div>
<main>{''.join(cards)}</main>
<script>
const key='vera-{BATCH_ID}-human-checklist-v2';
const boxes=[...document.querySelectorAll('input[type=checkbox]')];
let saved={{}};
try{{saved=JSON.parse(localStorage.getItem(key)||'{{}}');}}catch(error){{saved={{}};}}
boxes.forEach((box,index)=>{{box.checked=Boolean(saved[index]);box.addEventListener('change',()=>{{saved[index]=box.checked;localStorage.setItem(key,JSON.stringify(saved));update();}});}});
function update(){{const count=boxes.filter(box=>box.checked).length;document.querySelector('#progress').textContent=`${{count}} / ${{boxes.length}} checked`;}}
async function writeClipboard(text){{
  if(navigator.clipboard&&window.isSecureContext){{await navigator.clipboard.writeText(text);return;}}
  const area=document.createElement('textarea');area.value=text;area.setAttribute('readonly','');area.style.position='fixed';area.style.opacity='0';document.body.append(area);area.select();
  if(!document.execCommand('copy')){{throw new Error('Copy command was unavailable.');}}area.remove();
}}
async function copyStatus(){{
  const lines=['{BATCH_COPY_TITLE}'];
  document.querySelectorAll('.recipe').forEach(card=>{{
    const cardBoxes=[...card.querySelectorAll('input[type=checkbox]')];
    const checked=cardBoxes.filter(box=>box.checked).length;
    const status=card.querySelector('.status').textContent.trim();
    lines.push(`${{card.id}}: ${{status}}; ${{checked}} / ${{cardBoxes.length}} optional human checks complete`);
  }});
  const feedback=document.querySelector('#copy-feedback');
  try{{await writeClipboard(lines.join('\\n'));feedback.textContent='Copied.';}}catch(error){{feedback.textContent='Copy failed; select the status manually.';}}
}}
const sourceDetails=[...document.querySelectorAll('[data-source]')];
function setSourceOpen(container,open){{
  const toggle=container.querySelector('.source-toggle');
  const panel=container.querySelector('.source-panel');
  toggle.setAttribute('aria-expanded',String(open));
  toggle.setAttribute('aria-label',`${{open?'Hide':'View'}} source for ${{toggle.dataset.sourceTitle}}`);
  toggle.querySelector('.source-toggle-label').textContent=open?'Hide source':'View source';
  toggle.querySelector('.source-toggle-icon').textContent=open?'−':'+';
  panel.hidden=!open;
  container.classList.toggle('is-open',open);
}}
sourceDetails.forEach(container=>{{
  const toggle=container.querySelector('.source-toggle');
  toggle.addEventListener('click',()=>setSourceOpen(container,toggle.getAttribute('aria-expanded')!=='true'));
  toggle.addEventListener('keydown',event=>{{
    if(event.key==='Enter'||event.key===' '){{event.preventDefault();toggle.click();}}
  }});
}});
let printOpen=[];
window.addEventListener('beforeprint',()=>{{printOpen=sourceDetails.map(item=>item.classList.contains('is-open'));sourceDetails.forEach(item=>setSourceOpen(item,true));}});
window.addEventListener('afterprint',()=>{{sourceDetails.forEach((item,index)=>setSourceOpen(item,printOpen[index]));}});
update();
</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="rebuild this frozen audited batch")
    args = parser.parse_args()

    if source_digest() != SOURCE_SHA256:
        raise SystemExit("Source PDF SHA-256 does not match the frozen batch manifest")
    pages = marker_pages()
    expected_pages = {page for recipe in RECIPES for page in recipe["pages"]}
    if set(pages) != expected_pages:
        raise SystemExit(f"Marker page set {sorted(pages)} does not equal {sorted(expected_pages)}")

    RECIPE_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    overviews: dict[str, list[Path]] = {}
    report: dict[str, Any] = {"batch_id": BATCH_ID, "records": []}
    for recipe in RECIPES:
        record_path = RECIPE_DIR / f"{recipe['recipe_id']}.yaml"
        if record_path.exists() and not args.force:
            raise SystemExit(
                f"Refusing to overwrite {record_path}; pass --force only when intentionally "
                "rebuilding the frozen batch from this audited specification"
            )
        source_regions = []
        boxes: dict[int, list[tuple[int, int, int, int]]] = {}
        for key, _role, pdf_page, block_ids in recipe["regions"]:
            region, box = crop_region(recipe["recipe_id"], key, pdf_page, block_ids, pages[pdf_page])
            source_regions.append(region)
            boxes.setdefault(pdf_page, []).append(box)
        overviews[recipe["recipe_id"]] = write_overviews(recipe, boxes)
        record = build_record(recipe, source_regions)
        record_path.write_text(
            yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8",
        )
        records.append(record)
        report["records"].append(
            {
                "recipe_id": recipe["recipe_id"],
                "record_path": str(record_path.relative_to(PROJECT_DIR)),
                "source_regions": len(source_regions),
                "overview_images": [str(path.relative_to(PROJECT_DIR)) for path in overviews[recipe["recipe_id"]]],
                "high_risk_tokens": risk_tokens(record),
                "open_issue_count": len(recipe["open_issues"]),
                "status": record["verification"]["status"],
                "audit_performed_by": "ai",
            }
        )

    review_path = REVIEW_DIR / "index.html"
    review_path.write_text(render_review_html(records, overviews), encoding="utf-8")
    report["review_packet"] = str(review_path.relative_to(PROJECT_DIR))
    report["source_sha256"] = SOURCE_SHA256
    report["marker_pages"] = sorted(pages)
    report["audit_completed_at"] = AUDIT_AT
    report["auditor_id"] = AUDITOR_ID
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
