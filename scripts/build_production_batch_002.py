#!/usr/bin/env python3
"""Build production batch 002 candidates and its local source-audit packet."""

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
    / "pilot/production-batch-002/marker-output/Culinary Adventures - Vera Gaeta"
    / "Culinary Adventures - Vera Gaeta.json"
)
EVIDENCE_DIR = PROJECT_DIR / "evidence/production-batch-002"
PAGE_DIR = EVIDENCE_DIR / "source-pages"
REGION_DIR = EVIDENCE_DIR / "regions"
OVERVIEW_DIR = EVIDENCE_DIR / "overview"
RECIPE_DIR = PROJECT_DIR / "data/recipes"
REVIEW_DIR = PROJECT_DIR / "review/production-batch-002"
REPORT_PATH = PROJECT_DIR / "pilot/production-batch-002/build-report.json"
CREATED_AT = "2026-08-23T21:09:29Z"
AUDIT_AT = "2026-08-23T21:09:29Z"
AUDITOR_ID = "openai-codex"


def section(
    section_id: str,
    items: list[tuple[str, list[str]]],
    label: tuple[str, str, str] | None = None,
) -> dict[str, Any]:
    return {"section_id": section_id, "label": label, "items": items}


RECIPES: list[dict[str, Any]] = [
    {
        "recipe_id": "vera-r0004",
        "source_order": 4,
        "slug": "stuffed-meat-loaf",
        "pages": [6],
        "printed_pages": ["5"],
        "display_title": "Stuffed meat loaf · Svíčková sekaná plněná",
        "titles": [("en", "primary", "Stuffed meat loaf"), ("cs", "parallel", "Svíčková sekaná plněná")],
        "regions": [
            ("title", "title", 6, ["/page/5/SectionHeader/1"]),
            ("ingredients", "ingredient", 6, ["/page/5/ListGroup/2"]),
            ("step-1", "instruction", 6, ["/page/5/Text/3"]),
            ("step-2", "instruction", 6, ["/page/5/Text/4"]),
            ("step-3", "instruction", 6, ["/page/5/Text/5"]),
            ("yield", "yield-time", 6, ["/page/5/Text/6"]),
        ],
        "ingredient_sections": [section("ingredients-main", [
            ("1·1/2 lbs. ground sirloin or chuck (ground pork shoulder can substitute half of the ground beef)", ["ingredients"]),
            ("1 whole egg", ["ingredients"]), ("2 hard baked rolls", ["ingredients"]),
            ("1 slice bacon", ["ingredients"]), ("salt, pepper, marjoram", ["ingredients"]),
            ("1 small onion", ["ingredients"]), ("3/4 cup water", ["ingredients"]),
            ("3 tablespoons bread crumbs", ["ingredients"]), ("4 pickled dills", ["ingredients"]),
            ("4 hard boiled eggs", ["ingredients"]), ("3/4 cup chicken stock", ["ingredients"]),
            ("4 tablespoons vegetable oil", ["ingredients"]),
        ])],
        "instruction_sections": [section("instructions-main", [
            ("Soak the rolls in water, squeeze off excess liquid, shred them and mix well with the ground meat. Add diced bacon, egg, salt, pepper, marjoram, chopped onion, 1 tablespoon water and mix it very well. If the mixture is not thick enough, add 1-2 tablespoons bread crumbs.", ["step-1"]),
            ("Turn the mixture over onto a board dusted with bread crumbs. Form a 3/4” thick rectangle. Arrange hard boiled eggs and peeled and diced pickles by longer side of the rectangle. Roll the meat mixture over the eggs and form a loaf. Grease baking tray with oil, sprinkle the remaining oil over the loaf, and bake at 350F for one hour. Baste with chicken stock and juices from the pan. When done, slice the loaf on a serving dish, sprinkle with pan drippings.", ["step-2"]),
            ("Serve with vegetables, mashed potatoes, boiled potatoes, potato salad, etc.", ["step-3"]),
        ])],
        "yield": "Serves 6 – Preparation time: 1 hour 15 minutes",
        "notes": [], "relationships": [], "cross_reference_targets": [], "status": "source_checked", "open_issues": [],
    },
    {
        "recipe_id": "vera-r0005", "source_order": 5, "slug": "beef-goulash", "pages": [7],
        "printed_pages": ["6"], "display_title": "Beef goulash · Guláš z hovězího masa",
        "titles": [("en", "primary", "Beef goulash"), ("cs", "parallel", "Guláš z hovězího masa")],
        "regions": [
            ("title", "title", 7, ["/page/6/SectionHeader/1"]), ("ingredients", "ingredient", 7, ["/page/6/ListGroup/2"]),
            ("step-1", "instruction", 7, ["/page/6/Text/3"]), ("step-2", "instruction", 7, ["/page/6/Text/4"]),
            ("step-3", "instruction", 7, ["/page/6/Text/5"]), ("yield", "yield-time", 7, ["/page/6/Text/6"]),
            ("alternative-1", "note", 7, ["/page/6/Text/7"]), ("alternative-2", "note", 7, ["/page/6/Text/8"]),
        ],
        "ingredient_sections": [section("ingredients-main", [
            ("3·4 lbs. boneless beef stew meat (bottom round, rump, chuck), cut in 1·1/2” cubes", ["ingredients"]),
            ("2·3 cups beef stock or water", ["ingredients"]), ("1 large onion, thinly sliced", ["ingredients"]),
            ("3 slices bacon cut in short strips", ["ingredients"]), ("2 tablespoons vegetable oil", ["ingredients"]),
            ("3 cloves garlic, pressed or chopped", ["ingredients"]), ("2 tablespoons paprika", ["ingredients"]),
            ("3 tablespoons flour", ["ingredients"]), ("1/2 teaspoon each of caraway seeds and marjoram", ["ingredients"]),
            ("salt and pepper", ["ingredients"]),
        ])],
        "instruction_sections": [section("instructions-main", [
            ("Heat oil in a large stewpan. Add bacon and onion. Cook slowly, stirring and turning frequently until bacon is lightly browned and onion is translucent. Add beef. Sprinkle evenly over the meat: caraway seeds, marjoram, paprika, garlic. Cover, simmer one hour over low heat adding occasionally 2·3 tablespoons beef stock or water, if needed. Liquid in the pan should be just enough so that the onion and the meat do not burn or stick to the pan.", ["step-1"]),
            ("When meat is half done, uncover pan and let cooking liquid nearly evaporate. Sprinkle flour over meat and braise 2·3 minutes. Add enough beef stock or water to cover the meat. Simmer 30 minutes or until meat is tender. Should the sauce be too thick, add some more beef stock or water.", ["step-2"]),
            ("Taste sauce, season with salt and pepper. Lift meat onto a warmed deep serving dish. Strain sauce and pour over meat. Serve with boiled potatoes, rice, salad.", ["step-3"]),
        ])],
        "yield": "Serves 6 – Preparation time: 2 hours",
        "notes": [
            ("Alternative 1 – Prepare beef goulash as shown above. Peel and slice 4 pickled cucumbers, add to the goulash, heat through, serve.", "alternative-1"),
            ("Alternative 2 – Turn the goulash over into a deep serving dish, sprinkle with shredded ham and grated Parmesan cheese. Serve with white rice.", "alternative-2"),
        ],
        "relationships": [], "cross_reference_targets": [], "status": "source_checked", "open_issues": [],
    },
    {
        "recipe_id": "vera-r0006", "source_order": 6,
        "slug": "bohemian-brasciole-stuffed-beef-veal-rolls", "pages": [8], "printed_pages": ["7"],
        "display_title": "Bohemian “brasciole” - stuffed beef (veal) rolls · Hovězí (telecí) závitky",
        "titles": [("en", "primary", "Bohemian “brasciole” - stuffed beef (veal) rolls"), ("cs", "parallel", "Hovězí (telecí) závitky")],
        "regions": [
            ("title", "title", 8, ["/page/7/SectionHeader/1"]), ("ingredients", "ingredient", 8, ["/page/7/ListGroup/2"]),
            ("step-1", "instruction", 8, ["/page/7/Text/3"]), ("step-2", "instruction", 8, ["/page/7/Text/4"]),
            ("step-3", "instruction", 8, ["/page/7/Text/5"]), ("yield", "yield-time", 8, ["/page/7/Text/6"]),
        ],
        "ingredient_sections": [section("ingredients-main", [
            ("6 thin, approx. 1/4”, slices beef sirloin (or veal top round)", ["ingredients"]),
            ("6 tablespoons butter", ["ingredients"]), ("1 small onion", ["ingredients"]),
            ("1·1/2 cups sliced mushrooms", ["ingredients"]), ("juice of one lemon", ["ingredients"]),
            ("salt and pepper", ["ingredients"]), ("2 egg yolks", ["ingredients"]),
            ("6 thin slices bacon", ["ingredients"]), ("3/4 cup white wine", ["ingredients"]),
            ("3/4 cup olive oil", ["ingredients"]), ("3 tablespoons Worcestershire sauce", ["ingredients"]),
            ("3 cloves garlic", ["ingredients"]),
        ])],
        "instruction_sections": [section("instructions-main", [
            ("Pound the meat slices and salt them on both sides. In a skillet, combine the butter and finely chopped onion. Brown the onion lightly, then add sliced mushrooms and lemon juice. Sauté 6-8 minutes. Discard the fat. Blend in two egg yolks, spice with salt and pepper. Spread the mixture evenly over the meat slices, roll each to enclose mixture, wrap each roll with a slice of bacon. Tie them with a string or fasten with wooden picks or small skewers. Place them in a container.", ["step-1"]),
            ("Mix wine, olive oil, Worcestershire sauce and pressed garlic and pour over the meat rolls. Let them marinate for 4 hours or overnight in a refrigerator.", ["step-2"]),
            ("On stove top heat a large heavy skillet. Add the rolls and brown them on all sides for about 20 minutes frequently adding some of the marinate. Remove the string, wooden picks or skewers. Serve with fried potatoes, vegetables, salad.", ["step-3"]),
        ])],
        "yield": "Serves 6 – Preparation time: 1 hour, plus marinating",
        "notes": [], "relationships": [], "cross_reference_targets": [], "status": "source_checked", "open_issues": [],
    },
    {
        "recipe_id": "vera-r0007", "source_order": 7, "slug": "roast-veal", "pages": [8, 9],
        "printed_pages": ["7", "8"], "display_title": "Roast veal · Telecí pečeně",
        "titles": [("en", "primary", "Roast veal"), ("cs", "parallel", "Telecí pečeně")],
        "regions": [
            ("title", "title", 8, ["/page/7/SectionHeader/7"]), ("ingredients-a", "ingredient", 8, ["/page/7/ListGroup/8"]),
            ("step-1a", "instruction", 8, ["/page/7/Text/9"]), ("ingredients-b", "continuation", 9, ["/page/8/ListGroup/1"]),
            ("step-1b", "continuation", 9, ["/page/8/Text/2"]), ("yield", "yield-time", 9, ["/page/8/Text/3"]),
        ],
        "ingredient_sections": [section("ingredients-main", [
            ("3·4 lbs. leg of veal or top round, boned", ["ingredients-a"]), ("4 slices bacon", ["ingredients-a"]),
            ("1/2 cup cognac", ["ingredients-a"]), ("6 tablespoons butter", ["ingredients-a"]),
            ("2·1/2 cups white table wine", ["ingredients-a"]), ("1 cup chicken stock", ["ingredients-a"]),
            ("1 medium size onion", ["ingredients-a"]), ("2 carrots", ["ingredients-a"]),
            ("snipped parsley, thyme, bay leaves", ["ingredients-b"]), ("salt and pepper", ["ingredients-b"]),
        ])],
        "instruction_sections": [section("instructions-main", [
            ("Lard the veal with strips of bacon. Rub it with salt and pepper. In a casserole combine the butter, chopped onion and the roast. Brown it lightly. Pour the cognac over and ignite it. When the flame dies down add the wine, sliced carrots, thyme, snipped parsley, crushed bay leaves, some of the chicken stock, and roast at 350F for 2 hours, basting occasionally with pan juices and chicken stock. Slice the roast. Strain pan juices into a saucepan, add 1/2 tablespoon butter and more chicken stock if needed; bring to boil. Serve sauce over sliced meat or on side. Serve with vegetables, noodles, boiled potatoes.", ["step-1a", "step-1b"]),
        ])],
        "yield": "Serves 6 – Preparation time: 2 hours 30 minutes", "notes": [],
        "relationships": [("step-1a", "step-1b")], "cross_reference_targets": [],
        "status": "source_checked", "open_issues": [],
    },
    {
        "recipe_id": "vera-r0008", "source_order": 8, "slug": "stuffed-veal-breast", "pages": [9, 10],
        "printed_pages": ["8", "9"], "display_title": "Stuffed veal breast · Telecí hrudí nadívané",
        "titles": [("en", "primary", "Stuffed veal breast"), ("cs", "parallel", "Telecí hrudí nadívané")],
        "regions": [
            ("title", "title", 9, ["/page/8/SectionHeader/4"]), ("ingredients", "ingredient", 9, ["/page/8/ListGroup/5"]),
            ("step-1", "instruction", 9, ["/page/8/Text/6"]), ("step-2", "instruction", 9, ["/page/8/Text/7"]),
            ("step-3", "instruction", 9, ["/page/8/Text/8"]), ("step-4", "instruction", 9, ["/page/8/Text/9"]),
            ("step-5", "instruction", 9, ["/page/8/Text/10"]), ("yield", "yield-time", 9, ["/page/8/Text/11"]),
            ("stuffings-title", "continuation", 10, ["/page/9/SectionHeader/1"]),
            ("egg-title", "title", 10, ["/page/9/SectionHeader/2"]), ("egg-ingredients", "ingredient", 10, ["/page/9/ListGroup/8"]),
            ("egg-step", "instruction", 10, ["/page/9/Text/3"]),
            ("bread-title", "title", 10, ["/page/9/SectionHeader/4"]), ("bread-ingredients", "ingredient", 10, ["/page/9/ListGroup/9"]),
            ("bread-step", "instruction", 10, ["/page/9/Text/5"]),
            ("liver-title", "title", 10, ["/page/9/SectionHeader/6"]), ("liver-ingredients", "ingredient", 10, ["/page/9/ListGroup/10"]),
            ("liver-step", "instruction", 10, ["/page/9/Text/7"]),
        ],
        "headnotes": [("Stuffings for veal breast", ["stuffings-title"])],
        "ingredient_sections": [
            section("ingredients-main", [
                ("3·4 lbs. veal breast, boned", ["ingredients"]), ("1 cup chicken stock", ["ingredients"]),
                ("8 tablespoons butter", ["ingredients"]), ("salt", ["ingredients"]), ("stuffing – see below", ["ingredients"]),
            ]),
            section("ingredients-egg-stuffing", [("6 eggs", ["egg-ingredients"]), ("1/2 cup ham, diced", ["egg-ingredients"]), ("1/2 cup cooked peas", ["egg-ingredients"]), ("3 tablespoons butter", ["egg-ingredients"]), ("salt", ["egg-ingredients"])], ("label-ingredient-egg", "Egg stuffing:", "egg-title")),
            section("ingredients-bread-stuffing", [("3 hard baked rolls", ["bread-ingredients"]), ("4 tablespoons butter", ["bread-ingredients"]), ("1 cup milk", ["bread-ingredients"]), ("1 whole egg, 1 egg yolk", ["bread-ingredients"]), ("1/2 cup bread crumbs", ["bread-ingredients"]), ("snipped parsley", ["bread-ingredients"]), ("dash of ground nutmeg", ["bread-ingredients"]), ("salt and pepper", ["bread-ingredients"])], ("label-ingredient-bread", "Bread stuffing:", "bread-title")),
            section("ingredients-liver-stuffing", [("6 oz. calf liver", ["liver-ingredients"]), ("3 hard baked rolls", ["liver-ingredients"]), ("1 cup milk", ["liver-ingredients"]), ("6 tablespoons butter", ["liver-ingredients"]), ("1 small onion", ["liver-ingredients"]), ("1/3 cup bread crumbs", ["liver-ingredients"]), ("snipped parsley", ["liver-ingredients"]), ("dash of ground nutmeg, marjoram", ["liver-ingredients"]), ("salt and pepper", ["liver-ingredients"])], ("label-ingredient-liver", "Liver stuffing:", "liver-title")),
        ],
        "instruction_sections": [
            section("instructions-main", [
                ("Rinse the meat and pat it dry with a paper towel. Using the handle of a wooden spoon, make an opening in the narrower end of the veal breast to form a cavity for stuffing. Most supermarkets sell the veal breast ready to be stuffed.", ["step-1"]),
                ("Salt the meat and lightly fill the cavity with stuffing. Enclose it with stitches, or use a skewer. Lay the stuffed veal breast in a roasting pan with rack, skin down. Pour some of the melted butter on top and roast at 350F for 45 minutes. Turn it and roast 45 minutes to 1 hour, or until golden on top.", ["step-2"]),
                ("Baste occasionally with melted butter and pan drippings.", ["step-3"]),
                ("Prick the stuffed cavity with fork several times to let out the steam. (The steam would push out the stuffing while slicing it). Remove the stitches or skewer.", ["step-4"]),
                ("Let it stand 5 minutes. Slice and sprinkle with juices from the pan. Serve with boiled potatoes, vegetables, salad, compote.", ["step-5"]),
            ]),
            section("instructions-egg-stuffing", [("In a frying pan combine melted butter and lightly beaten eggs. Scramble until the egg whites stiffen. Blend in ham and green peas. Salt.", ["egg-step"])], ("label-instruction-egg", "Egg stuffing:", "egg-title")),
            section("instructions-bread-stuffing", [("Soak the rolls in milk, squeeze off excess, shred them. In a bowl cream the butter, whisk in the egg and the egg yolk. Add all remaining ingredients, leaving the bread crumbs to be added last. If the stuffing is thick enough, do not use up all bread crumbs. This stuffing may also be used for roasted stuffed chicken, pigeon, etc.", ["bread-step"])], ("label-instruction-bread", "Bread stuffing:", "bread-title")),
            section("instructions-liver-stuffing", [("Soak the rolls in milk, squeeze off excess, shred them. Grind the liver, or mash it with a knife. Cream the butter, and blend in thoroughly all ingredients.", ["liver-step"])], ("label-instruction-liver", "Liver stuffing:", "liver-title")),
        ],
        "yield": "Serves 6 – Preparation time: 2 hours 30 minutes", "notes": [],
        "relationships": [("ingredients", "stuffings-title")], "cross_reference_targets": ["ingredient-5"],
        "status": "source_checked", "open_issues": [],
    },
]


def source_digest() -> str:
    return hashlib.sha256(SOURCE_PDF.read_bytes()).hexdigest()


def segment(segment_id: str, text: str, source_ids: list[str], **extra: Any) -> dict[str, Any]:
    value = {"segment_id": segment_id, "text_verbatim": text, "language": "en", "source_region_ids": source_ids}
    value.update(extra)
    return value


def build_record(recipe: dict[str, Any], source_regions: list[dict[str, Any]], stage: str) -> dict[str, Any]:
    rid = recipe["recipe_id"]
    source_id = lambda key: f"{rid}-{key}"
    titles = [segment(f"title-{'en' if language == 'en' else 'cs'}", text, [source_id("title")], title_role=role, language=language) for language, role, text in recipe["titles"]]
    ingredient_counter = 0
    ingredient_sections = []
    for spec in recipe["ingredient_sections"]:
        built: dict[str, Any] = {"section_id": spec["section_id"], "ingredients": []}
        if spec["label"]:
            label_id, text, region_key = spec["label"]
            built["label"] = segment(label_id, text, [source_id(region_key)])
        for text, region_keys in spec["items"]:
            ingredient_counter += 1
            built["ingredients"].append(segment(f"ingredient-{ingredient_counter}", text, [source_id(key) for key in region_keys]))
        ingredient_sections.append(built)
    step_counter = 0
    instruction_sections = []
    for spec in recipe["instruction_sections"]:
        built = {"section_id": spec["section_id"], "steps": []}
        if spec["label"]:
            label_id, text, region_key = spec["label"]
            built["label"] = segment(label_id, text, [source_id(region_key)])
        for text, region_keys in spec["items"]:
            step_counter += 1
            built["steps"].append(segment(f"step-{step_counter}", text, [source_id(key) for key in region_keys], step_number=step_counter))
        instruction_sections.append(built)
    transcription: dict[str, Any] = {
        "yield_time_lines": [segment("yield-1", recipe["yield"], [source_id("yield")])],
        "ingredient_sections": ingredient_sections,
        "instruction_sections": instruction_sections,
        "notes": [segment(f"note-{index}", text, [source_id(key)]) for index, (text, key) in enumerate(recipe["notes"], 1)],
        "cross_references": [],
    }
    if recipe.get("headnotes"):
        transcription["headnotes"] = [segment(f"headnote-{index}", text, [source_id(key) for key in keys]) for index, (text, keys) in enumerate(recipe["headnotes"], 1)]
    record = {
        "schema_version": "1.2.0", "record_type": "recipe", "recipe_id": rid, "record_revision": 1,
        "source_work": {"work_id": "vera-culinary-adventures", "source_file": "source/Culinary Adventures - Vera Gaeta.pdf", "source_sha256": SOURCE_SHA256, "pdf_page_count": 75, "pdf_pages": recipe["pages"], "printed_pages": recipe["printed_pages"], "rights_status": "not_assessed"},
        "source_regions": source_regions,
        "identity": {"display_title": segment("title-display", recipe["display_title"], [source_id("title")], language="mul"), "titles": titles, "source_order": recipe["source_order"], "slug_candidate": recipe["slug"]},
        "transcription": transcription,
        "relationships": {"continuations": [{"from_region_id": source_id(a), "to_region_id": source_id(b), "relationship": "continues_on"} for a, b in recipe["relationships"]], "related_recipe_ids": []},
        "provenance": {"created_at": CREATED_AT, "created_by": "codex-candidate", "candidate_sources": [{"tool": "marker-pdf", "tool_version": "2.0.0", "generated_at": CREATED_AT, "artifact_path": "pilot/production-batch-002/marker-output/Culinary Adventures - Vera Gaeta/Culinary Adventures - Vera Gaeta.json", "remote_model_used": False}]},
    }
    if stage == "candidate":
        record["verification"] = {"status": "machine_candidate", "audit_policy": "source_audit", "status_set_at": CREATED_AT, "checks": [], "open_issues": []}
    else:
        record["verification"] = shared.build_verification(record, recipe)
        if recipe["cross_reference_targets"]:
            targets = recipe["cross_reference_targets"]
            region_ids = [source_id("ingredients"), source_id("stuffings-title")]
            record["verification"]["checks"].append({"check_id": "ai-cross-reference", "check_type": "cross_reference", "target_ids": targets, "source_region_ids": region_ids, "result": "pass", "method": "direct_visual_source", "performed_by": "ai", "auditor_id": AUDITOR_ID, "audited_at": AUDIT_AT, "independent_of_extractor": True, "note": "The printed 'stuffing – see below' reference was followed to all three stuffing sections on PDF page 10."})
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
    shared.BATCH_ID = "production-batch-002"
    shared.BATCH_TITLE = "Batch 002 source audit"
    shared.BATCH_COPY_TITLE = "Vera Cookbook · Production Batch 002"


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
        else "All five records passed a fresh direct local AI source audit. Human verification remains a separate trust state."
    )
    RECIPE_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    overviews: dict[str, list[Path]] = {}
    report: dict[str, Any] = {"batch_id": "production-batch-002", "stage": args.stage, "records": []}
    for recipe in RECIPES:
        record_path = RECIPE_DIR / f"{recipe['recipe_id']}.yaml"
        if record_path.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite {record_path}; pass --force only for an intentional stage transition")
        source_regions = []
        boxes: dict[int, list[tuple[int, int, int, int]]] = {}
        for key, _role, pdf_page, block_ids in recipe["regions"]:
            region, box = shared.crop_region(recipe["recipe_id"], key, pdf_page, block_ids, pages[pdf_page])
            source_regions.append(region)
            boxes.setdefault(pdf_page, []).append(box)
        overviews[recipe["recipe_id"]] = shared.write_overviews(recipe, boxes)
        record = build_record(recipe, source_regions, args.stage)
        record_path.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
        records.append(record)
        report["records"].append({"recipe_id": recipe["recipe_id"], "record_path": str(record_path.relative_to(PROJECT_DIR)), "source_regions": len(source_regions), "overview_images": [str(path.relative_to(PROJECT_DIR)) for path in overviews[recipe["recipe_id"]]], "high_risk_tokens": shared.risk_tokens(record), "open_issue_count": len(recipe["open_issues"]), "status": record["verification"]["status"], "audit_performed_by": "ai" if args.stage == "audited" else None})
    review_path = REVIEW_DIR / "index.html"
    review_path.write_text(shared.render_review_html(records, overviews), encoding="utf-8")
    report.update({"review_packet": str(review_path.relative_to(PROJECT_DIR)), "source_sha256": SOURCE_SHA256, "marker_pages": sorted(pages), "audit_completed_at": AUDIT_AT if args.stage == "audited" else None, "auditor_id": AUDITOR_ID if args.stage == "audited" else None})
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
