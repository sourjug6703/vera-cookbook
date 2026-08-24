#!/usr/bin/env python3
"""Build production batch 003 candidates and its local source-audit packet."""

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
SOURCE_SHA256 = "58542d8b58bf57aadfd4c08f6728271ac5bd9d19aa77a2fe9ef412c68b2a989b"
MARKER_JSON = (
    PROJECT_DIR
    / "pilot/production-batch-003/marker-output/Culinary Adventures - Vera Gaeta"
    / "Culinary Adventures - Vera Gaeta.json"
)
EVIDENCE_DIR = PROJECT_DIR / "evidence/production-batch-003"
PAGE_DIR = EVIDENCE_DIR / "source-pages"
REGION_DIR = EVIDENCE_DIR / "regions"
OVERVIEW_DIR = EVIDENCE_DIR / "overview"
RECIPE_DIR = PROJECT_DIR / "data/recipes"
REVIEW_DIR = PROJECT_DIR / "review/production-batch-003"
REPORT_PATH = PROJECT_DIR / "pilot/production-batch-003/build-report.json"
CREATED_AT = "2026-08-23T21:31:00Z"
AUDIT_AT = "2026-08-23T21:35:39Z"
AUDITOR_ID = "openai-codex"


def issue(issue_id: str, targets: list[str], description: str, severity: str) -> dict[str, Any]:
    return {
        "issue_id": issue_id,
        "target_ids": targets,
        "description": description,
        "severity": severity,
    }


RECIPES: list[dict[str, Any]] = [
    {
        "recipe_id": "vera-r0009",
        "source_order": 9,
        "slug": "veal-chops-with-caraway-seeds",
        "pages": [11],
        "printed_pages": ["10"],
        "display_title": "Veal chops with caraway seeds · Telecí žebírka na kmíně",
        "titles": [
            ("title-en", "en", "primary", "Veal chops with caraway seeds"),
            ("title-cs", "cs", "parallel", "Telecí žebírka na kmíně"),
        ],
        "regions": [
            ("title", "title", 11, ["/page/10/SectionHeader/1"]),
            ("ingredients", "ingredient", 11, ["/page/10/ListGroup/2"]),
            ("step-1", "instruction", 11, ["/page/10/Text/3"]),
            ("step-2", "instruction", 11, ["/page/10/Text/4"]),
            ("step-3", "instruction", 11, ["/page/10/Text/5"]),
            ("yield", "yield-time", 11, ["/page/10/Text/6"]),
        ],
        "ingredients": [
            "6 veal chops",
            "1/2 cup flour",
            "1/2 cup vegetable oil",
            "2 tablespoons butter",
            "1 cup chicken stock",
            "1 small onion",
            "1 teaspoon caraway seeds",
            "salt",
        ],
        "steps": [
            ("Pound the veal chops lightly-they should not be more than 1/2” thick. Make a few short cuts on the edges to prevent curling, salt them on both sides, and dust with flour on one side. Brown chops in hot oil on both sides, floured side first. In a skillet combine the butter and finely chopped onion and set over medium heat.", ["step-1"]),
            ("When the onion becomes translucent add the caraway seeds, some of the chicken stock and the veal chops and simmer about 30 minutes or until the chops are tender.", ["step-2"]),
            ("Remove the veal chops. Bring the liquid to boil, blend in flour and remaining stock, and boil until the sauce thickens (about 5 minutes). Strain the sauce over the veal chops, simmer 5 minutes. Serve with noodles, rice, salad.", ["step-3"]),
        ],
        "yield": "Serves 6 – Preparation time: 45 minutes",
        "notes": [],
        "status": "source_checked",
        "open_issues": [],
    },
    {
        "recipe_id": "vera-r0010",
        "source_order": 10,
        "slug": "breaded-veal-chops",
        "pages": [11],
        "printed_pages": ["10"],
        "display_title": "Breaded veal chops · Telecí žebírka smažená",
        "titles": [
            ("title-en", "en", "primary", "Breaded veal chops"),
            ("title-cs", "cs", "parallel", "Telecí žebírka smažená"),
        ],
        "regions": [
            ("title", "title", 11, ["/page/10/SectionHeader/7"]),
            ("ingredients", "ingredient", 11, ["/page/10/ListGroup/8"]),
            ("step-1", "instruction", 11, ["/page/10/Text/9"]),
            ("step-2", "instruction", 11, ["/page/10/Text/10"]),
            ("yield", "yield-time", 11, ["/page/10/Text/11"]),
        ],
        "ingredients": [
            "6 veal chops",
            "1/2 cup flour",
            "2 eggs",
            "1/3 cup milk",
            "1 cup bread crumbs",
            "1 cup vegetable oil",
            "salt",
        ],
        "steps": [
            ("Pound the veal chops. Make a few short cuts on the edges to prevent curling, salt them on both sides. Dip each in milk, dredge in flour shaking off excess, then dip in beaten eggs and coat with bread crumbs.", ["step-1"]),
            ("Fry in hot oil in a covered pan for 5 minutes, turn them and finish frying uncovered. Drain on paper towel. Serve with potato salad, mashed potatoes, green vegetables, salad.", ["step-2"]),
        ],
        "yield": "Serves 6 – Preparation time: 45 minutes",
        "notes": [],
        "status": "source_checked",
        "open_issues": [],
    },
    {
        "recipe_id": "vera-r0011",
        "source_order": 11,
        "slug": "wiener-schnitzel-breaded-veal-scallops",
        "pages": [12],
        "printed_pages": ["11"],
        "display_title": "Wiener Schnitzel · Breaded veal scallops · Řízky",
        "titles": [
            ("title-en-1", "en", "primary", "Wiener Schnitzel"),
            ("title-en-2", "en", "parallel", "Breaded veal scallops"),
            ("title-cs", "cs", "parallel", "Řízky"),
        ],
        "regions": [
            ("title", "title", 12, ["/page/11/SectionHeader/1"]),
            ("ingredients", "ingredient", 12, ["/page/11/ListGroup/2"]),
            ("step-1", "instruction", 12, ["/page/11/Text/3"]),
            ("yield", "yield-time", 12, ["/page/11/SectionHeader/4"]),
            ("tip", "note", 12, ["/page/11/ListGroup/5"]),
        ],
        "ingredients": [
            "6 veal scallops – leg of veal or veal top round, thin sliced",
            "1/2 cup flour",
            "2 eggs",
            "1 cup bread crumbs",
            "1 cup vegetable oil",
            "salt",
        ],
        "steps": [
            ("Pound the scallops. Make a few short cuts on the edges to prevent curling, salt them on both sides. Dredge them in flour, shake off excess, dip in beaten eggs and coat with bread crumbs. Fry in hot oil in a covered pan about 4 minutes or until golden brown; turn and fry the other side uncovered. Drain on paper towel. Serve with potatoes, potato salad, mashed potatoes, green salad.", ["step-1"]),
        ],
        "yield": "Serves 6 – Preparation time: 45 minutes",
        "notes": [
            ("⟦outlined right-arrow glyph⟧ This is the correct way to prepare Wiener Schnitzels, a very popular meal in Bohemia. Thinly sliced boneless pork chops, beef tenderloin slices, boned and skinned chicken breast or cutlets may be prepared in the same manner.", "tip"),
        ],
        "segment_uncertainties": {
            "note-1": [
                {
                    "substring": "⟦outlined right-arrow glyph⟧",
                    "issue": "ambiguous_glyph",
                    "note": "The scan clearly shows an outlined right-arrow ornament, but its exact character encoding is unresolved; the bracketed text is an explicit placeholder, not a Unicode guess.",
                }
            ]
        },
        "status": "needs_attention",
        "open_issues": [
            issue(
                "r0011-note-glyph",
                ["note-1"],
                "Exact character identity of the outlined right-arrow ornament before the note is unresolved; retain the explicit placeholder until a human determines the intended encoding or approves treating it as non-text decoration.",
                "textual",
            )
        ],
    },
    {
        "recipe_id": "vera-r0012",
        "source_order": 12,
        "slug": "veal-goulash",
        "pages": [12],
        "printed_pages": ["11"],
        "display_title": "Veal goulash · Guláš telecí",
        "titles": [
            ("title-en", "en", "primary", "Veal goulash"),
            ("title-cs", "cs", "parallel", "Guláš telecí"),
        ],
        "regions": [
            ("title", "title", 12, ["/page/11/SectionHeader/6"]),
            ("ingredients", "ingredient", 12, ["/page/11/ListGroup/7"]),
            ("step-1", "instruction", 12, ["/page/11/Text/8"]),
            ("step-2", "instruction", 12, ["/page/11/Text/9"]),
            ("step-3", "instruction", 12, ["/page/11/Text/10"]),
            ("yield", "yield-time", 12, ["/page/11/SectionHeader/11"]),
        ],
        "ingredients": [
            "3 lbs. boneless veal shoulder, cut in 1” cubes",
            "6 tablespoons butter",
            "1 medium onion, finely chopped",
            "2 tablespoons paprika",
            "dash of hot curry powder",
            "2 cups chicken broth",
            "juice of 1 lemon",
            "4 tablespoons flour",
            "1 pint heavy cream",
            "salt and pepper",
        ],
        "steps": [
            ("Melt butter in a heavy 3 quart saucepan. Add onion and cook over medium heat until translucent. Add paprika, curry, veal, 2·3 tablespoons chicken broth.", ["step-1"]),
            ("Simmer over low heat about 1 hr. adding gradually chicken broth, if needed. The meat must be simmering in just enough liquid so that it does not stick to the pot. You may not use up all of the chicken broth. When the veal is tender, not overcooked, add lemon juice. Mix well flour and cream and blend the mixture into the stew. Bring to boil, simmer 5 minutes, stirring often. Season to taste with salt and pepper.", ["step-2"]),
            ("Serve with dumplings, noodles, salad.", ["step-3"]),
        ],
        "yield": "Serves 6 – Preparation time: 1 hour 30 minutes",
        "notes": [],
        "status": "source_checked",
        "open_issues": [],
    },
    {
        "recipe_id": "vera-r0013",
        "source_order": 13,
        "slug": "pork-roast",
        "pages": [13],
        "printed_pages": ["12"],
        "display_title": "Pork roast · Vepřová pečeně",
        "titles": [
            ("title-en", "en", "primary", "Pork roast"),
            ("title-cs", "cs", "parallel", "Vepřová pečeně"),
        ],
        "regions": [
            ("title", "title", 13, ["/page/12/SectionHeader/2"]),
            ("ingredients", "ingredient", 13, ["/page/12/ListGroup/1"]),
            ("step-1", "instruction", 13, ["/page/12/Text/3"]),
            ("step-2", "instruction", 13, ["/page/12/Text/4"]),
            ("step-3", "instruction", 13, ["/page/12/Text/5"]),
            ("step-4", "instruction", 13, ["/page/12/Text/6"]),
            ("step-5", "instruction", 13, ["/page/12/Text/7"]),
            ("yield", "yield-time", 13, ["/page/12/Text/8"]),
        ],
        "ingredients": [
            "3·4 lbs. center cut pork roast – (ask the butcher to saw across the rib bones of the roast, at the base of the backbone – separating the ribs from the backbone. It will ease the carving).",
            "2 cups chicken stock",
            "2 teaspoons caraway seeds",
            "3 cloves garlic, pressed",
            "2 bay leaves",
            "salt and pepper",
        ],
        "steps": [
            ("In a saucepan heat the chicken stock, caraway seeds, bay leaves and garlic.", ["step-1"]),
            ("Rinse and pat dry the meat and rub it with salt and pepper. Place it, skin down, on a rack in an open roasting pan. Pour half of the liquid from the saucepan over the meat and roast at 350F for 1 hour, basting frequently with the juices from the pan and the liquid from the saucepan. Turn the meat and continue roasting for 1·1/2 hours, until the top is golden brown and the meat tender. Allow 35 minutes per pound.", ["step-2"]),
            ("When done let it rest 5 minutes, carve.", ["step-3"]),
            ("Skim fat from the pan drippings, strain some over the roast, serve the rest in a saucedish.", ["step-4"]),
            ("Serve with dumplings, potato dumplings, boiled potatoes and sauerkraut.", ["step-5"]),
        ],
        "yield": "Serves 6 – Preparation time: 3 hours",
        "notes": [],
        "status": "source_checked",
        "open_issues": [],
    },
]


def source_digest() -> str:
    return hashlib.sha256(SOURCE_PDF.read_bytes()).hexdigest()


def segment(segment_id: str, text: str, source_ids: list[str], **extra: Any) -> dict[str, Any]:
    value = {
        "segment_id": segment_id,
        "text_verbatim": text,
        "language": "en",
        "source_region_ids": source_ids,
    }
    value.update(extra)
    return value


def build_record(recipe: dict[str, Any], source_regions: list[dict[str, Any]], stage: str) -> dict[str, Any]:
    rid = recipe["recipe_id"]
    source_id = lambda key: f"{rid}-{key}"
    titles = [
        segment(segment_id, text, [source_id("title")], language=language, title_role=role)
        for segment_id, language, role, text in recipe["titles"]
    ]
    ingredients = [
        segment(f"ingredient-{index}", text, [source_id("ingredients")])
        for index, text in enumerate(recipe["ingredients"], 1)
    ]
    steps = [
        segment(
            f"step-{index}",
            text,
            [source_id(key) for key in region_keys],
            step_number=index,
        )
        for index, (text, region_keys) in enumerate(recipe["steps"], 1)
    ]
    notes = [
        segment(f"note-{index}", text, [source_id(key)])
        for index, (text, key) in enumerate(recipe["notes"], 1)
    ]
    for note in notes:
        uncertainties = recipe.get("segment_uncertainties", {}).get(note["segment_id"])
        if uncertainties:
            note["uncertainties"] = uncertainties
    record = {
        "schema_version": "1.2.0",
        "record_type": "recipe",
        "recipe_id": rid,
        "record_revision": 1,
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
            "display_title": segment(
                "title-display", recipe["display_title"], [source_id("title")], language="mul"
            ),
            "titles": titles,
            "source_order": recipe["source_order"],
            "slug_candidate": recipe["slug"],
        },
        "transcription": {
            "yield_time_lines": [segment("yield-1", recipe["yield"], [source_id("yield")])],
            "ingredient_sections": [
                {"section_id": "ingredients-main", "ingredients": ingredients}
            ],
            "instruction_sections": [
                {"section_id": "instructions-main", "steps": steps}
            ],
            "notes": notes,
            "cross_references": [],
        },
        "relationships": {"continuations": [], "related_recipe_ids": []},
        "provenance": {
            "created_at": CREATED_AT,
            "created_by": "codex-candidate",
            "candidate_sources": [
                {
                    "tool": "marker-pdf",
                    "tool_version": "2.0.0",
                    "generated_at": "2026-08-23T21:29:23Z",
                    "artifact_path": "pilot/production-batch-003/marker-output/Culinary Adventures - Vera Gaeta/Culinary Adventures - Vera Gaeta.json",
                    "remote_model_used": False,
                }
            ],
        },
    }
    if stage == "candidate":
        record["verification"] = {
            "status": "machine_candidate",
            "audit_policy": "source_audit",
            "status_set_at": CREATED_AT,
            "checks": [],
            "open_issues": [],
        }
    else:
        record["verification"] = shared.build_verification(record, recipe)
    return record


def configure_shared() -> None:
    shared.SOURCE_PDF = SOURCE_PDF
    shared.SOURCE_SHA256 = SOURCE_SHA256
    shared.MARKER_JSON = MARKER_JSON
    shared.EVIDENCE_DIR = EVIDENCE_DIR
    shared.PAGE_DIR = PAGE_DIR
    shared.REGION_DIR = REGION_DIR
    shared.OVERVIEW_DIR = OVERVIEW_DIR
    shared.RECIPE_DIR = RECIPE_DIR
    shared.REVIEW_DIR = REVIEW_DIR
    shared.REPORT_PATH = REPORT_PATH
    shared.AUDIT_AT = AUDIT_AT
    shared.AUDITOR_ID = AUDITOR_ID
    shared.RECIPES = RECIPES
    shared.BATCH_ID = "production-batch-003"
    shared.BATCH_TITLE = "Batch 003 source audit"
    shared.BATCH_COPY_TITLE = "Vera Cookbook · Production Batch 003"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["candidate", "audited"], required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    configure_shared()
    if source_digest() != SOURCE_SHA256:
        raise SystemExit("Source PDF SHA-256 does not match the frozen batch manifest")
    pages = shared.marker_pages()
    expected_pages = {page for recipe in RECIPES for page in recipe["pages"]}
    if set(pages) != expected_pages:
        raise SystemExit(f"Marker page set {sorted(pages)} does not equal {sorted(expected_pages)}")
    shared.BATCH_SUMMARY = (
        "Five local machine candidates await a separate direct visual source audit. No candidate has been promoted."
        if args.stage == "candidate"
        else "Four records passed a fresh direct local AI source audit. One remains <b>needs attention</b> because its outlined arrow ornament cannot be encoded exactly without guessing. Human verification remains a separate trust state."
    )
    RECIPE_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    overviews: dict[str, list[Path]] = {}
    report: dict[str, Any] = {
        "batch_id": "production-batch-003",
        "stage": args.stage,
        "records": [],
    }
    for recipe in RECIPES:
        record_path = RECIPE_DIR / f"{recipe['recipe_id']}.yaml"
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
        record = build_record(recipe, source_regions, args.stage)
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
    review_path = REVIEW_DIR / "index.html"
    review_path.write_text(shared.render_review_html(records, overviews), encoding="utf-8")
    report.update(
        {
            "review_packet": str(review_path.relative_to(PROJECT_DIR)),
            "source_sha256": SOURCE_SHA256,
            "marker_pages": sorted(pages),
            "audit_completed_at": AUDIT_AT if args.stage == "audited" else None,
            "auditor_id": AUDITOR_ID if args.stage == "audited" else None,
        }
    )
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
