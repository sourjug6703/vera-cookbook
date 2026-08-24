#!/usr/bin/env python3
"""Generate declarative local candidate specs for production batches 009-013.

The source-order/title map is deliberately explicit; Marker supplies only local
layout blocks, never trust status. The resulting candidates still require the
separate visual audit documented in each batch.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MARKER = ROOT / "pilot/acceleration-wave-005/marker-output/Culinary Adventures - Vera Gaeta/Culinary Adventures - Vera Gaeta.json"
SOURCE_HASH = "58542d8b58bf57aadfd4c08f6728271ac5bd9d19aa77a2fe9ef412c68b2a989b"

# id|primary title|parallel Czech title (empty when the printed title has none)
PLAN = {
    "009": """
62|Potato dumplings|Bramborové knedlíky
63|Potato salad|Bramborový salát
64|Goulash soup|Gulášová polévka
65|Cream of chicken soup|Krém z kuřat
66|Tripe soup|Drštková polévka
67|Country potato soup|Bramborová polévka
68|Milk soup|Mléčná polévka
69|Wine soup|Vinná polévka
70|Beer soup|Pivní polévka
71|Bohemian open-faced pastries|České koláčky
72|Bohemian muffins|Buchty
""",
    "010": """
73|Ricotta filling|Tvarohová nádivka
74|Walnuts filling|Ořechová nádivka
75|Apple filling|Jablková nádivka
76|Butter crumb filling|Máslová drobenka
77|Poppy seeds filling|Maková nádivka
78|“Silver dollars” (miniature plain muffins)|Dukátové buchtičky
80|White wine froth|Vinná omáčka
81|Poppy seed loaf|Makový závin
82|Czech doughnuts|Koblihy
83|Open-faced doughnuts|Vdolky
""",
    "011": """
84|Karlsbader biscuits|Karlovarské suchary
85|Easter bread|Bochánek
86|Easter braid|Velikonoční pomlázka
87|Christmas loaf|Vánočka
88|Bishop’s bread (fruit cake)|Biskupský chlebíček
89|Sugar icing:|
90|Nut bread|Ořechový chlebíček
91|Cherry cake|Bublanina
92|Poppy seed pie|Makovec
93|Czech apple pie|Jablkový koláč
""",
    "012": """
94|Potato apple pie|Jablkový koláč bramborový
95|Bread and apple baba|Žemlovka
96|Apple strudel|Jablkový závin
97|Yellow cake|Bábovka
98|Fudge Marble cake|Mramorová bábovka
99|Plum dumplings|Švestkové knedlíky
100|Potato plum dumplings|Švestkové knedlíky bramborové
101|Apple, plum, peach, banana fritters (or other fruits of similar consistency)|Ovocné kobližky
102|Cabbage pockets|Zelné taštičky
103|Country pancakes|Lívance
""",
    "013": """
104|Apple pancakes|Jablkové palačinky
105|God’s graces|Boží milosti
106|Pretzels, sweet|Preclíčky
107|Nut cake|Ořechový dort
108|Chocolate filling|Čokoládový krém
109|Mocha filling|Mocca krém
110|Vanilla horns|Vanilkové rohlíčky
111|Almond snow-balls|Kostrby
112|Butter rounds|Máslová kolečka
113|Truffles|Lanýže
""",
}

READBACKS = {"010": ["vera-r0079"]}
NEEDS_ATTENTION = {77, 110}
CONTINUATION_ORDERS = {66, 82, 87}
RELATED = {
    71: ["vera-r0076"],
    77: ["vera-r0071", "vera-r0072"],
    78: ["vera-r0072", "vera-r0079", "vera-r0080"],
    81: ["vera-r0077"],
    83: ["vera-r0082"],
    86: ["vera-r0085"],
    88: ["vera-r0089"],
    90: ["vera-r0089"],
    100: ["vera-r0099"],
    107: ["vera-r0108", "vera-r0109"],
}

PAGES = {
    62:[41],63:[42],64:[42],65:[43],66:[43,44],67:[44],68:[45],69:[45],70:[45],71:[48],72:[49],
    73:[50],74:[50],75:[50],76:[51],77:[51],78:[52],80:[52],81:[53],82:[53,54],83:[54],
    84:[55],85:[56],86:[57],87:[57,58],88:[59],89:[59],90:[60],91:[60],92:[61],93:[61],
    94:[62],95:[62],96:[63],97:[64],98:[64],99:[65],100:[66],101:[67,68],102:[69],103:[70],
    104:[71],105:[71],106:[72],107:[72],108:[73],109:[73],110:[74],111:[74],112:[75],113:[75],
}
TEXT_TITLE_STARTS = {89: (59, 6)}
ADD_BLOCKS = {
    70: [(45, "/page/44/ListGroup/11")],
    85: [(56, "/page/55/ListGroup/1")],
    91: [(60, "/page/59/ListGroup/3")],
    92: [(61, "/page/60/ListGroup/9")],
    103: [(70, "/page/69/ListGroup/1")],
    105: [(71, "/page/70/ListGroup/3")],
    106: [(72, "/page/71/ListGroup/1"), (72, "/page/71/ListGroup/2")],
    107: [(72, "/page/71/ListGroup/3"), (72, "/page/71/ListGroup/4")],
}
REMOVE_BLOCKS = {
    66: {"/page/43/SectionHeader/0"},
    69: {"/page/44/ListGroup/11"},
    70: {"/page/44/ListGroup/11"},
    78: {"/page/51/ListGroup/2", "/page/51/SectionHeader/7", "/page/51/Text/8", "/page/51/Text/9"},
    90: {"/page/59/ListGroup/3"},
    93: {"/page/60/ListGroup/9"},
    104: {"/page/70/ListGroup/3"},
}
ITEM_OVERRIDES = {
    (69, "/page/44/ListGroup/11"): ["1·1/2 bottles white table wine", "6 egg yolks", "1/3 cup sugar", "grated rind of 1 lemon", "toasts or crackers"],
    (70, "/page/44/ListGroup/11"): ["1·1/2 quarts light beer", "6 egg yolks", "3 level tablespoons sugar", "grated rind of 1 lemon", "dash of cinnamon, ground clove, nutmeg", "French bread"],
    (104, "/page/70/ListGroup/2"): ["1 cup flour", "1·1/2 cups milk", "1/3 cup sugar", "5 eggs, separated", "pinch of salt", "2 large apples, Granny Smith type, peeled, diced", "6 tablespoons butter for frying", "2 tablespoons sugar for dusting"],
    (108, "/page/72/ListGroup/2"): ["1 pint heavy cream", "1·1/2 cups semi sweet chocolate morsels"],
    (110, "/page/73/ListGroup/3"): ["2 cups flour", "1/2 cup sugar", "8 oz. ground almonds", "3 sticks butter", "2 packages vanilla sugar (1 package into dough, 1 for sprinkling)", "4 tablespoons sugar mixed with vanilla sugar"],
    (111, "/page/73/ListGroup/7"): ["3 egg whites", "1/2 cup sugar", "5 oz. slivered almonds", "Butter and flour for cookie sheet"],
}
MANUAL_REGIONS = {
    107: [("yield-manual", "yield-time", 72, "manual-bbox:570,984,899,1017", "1 cake – Preparation time: 1 hour")],
    72: [("yield-manual", "yield-time", 49, "manual-bbox:550,970,1010,1035", "Serves 10 – Preparation time: 3 hours")],
}
MANUAL_INGREDIENTS = {
    69: [("ingredients-wine", 45, "manual-bbox:115,499,445,675", ["1·1/2 bottles white table wine", "6 egg yolks", "1/3 cup sugar", "grated rind of 1 lemon", "toasts or crackers"])],
    70: [("ingredients-beer", 45, "manual-bbox:115,680,445,858", ["1·1/2 quarts light beer", "6 egg yolks", "3 level tablespoons sugar", "grated rind of 1 lemon", "dash of cinnamon, ground clove, nutmeg", "French bread"])],
}
CONTINUATION_KEYS = {66: ("text-4", "text-5")}


def plain(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    return re.sub(r"\s+", " ", value).strip()


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower().replace("’", "").replace("á", "a").replace("č", "c").replace("ř", "r").replace("š", "s").replace("ž", "z").replace("ě", "e").replace("ů", "u").replace("ý", "y").replace("í", "i").replace("é", "e").replace("ú", "u").replace("ó", "o"))


def parse_plan(value: str) -> list[dict]:
    recipes = []
    for row in value.strip().splitlines():
        order, en, *cs = row.split("|")
        recipes.append({"source_order": int(order), "en": en, "cs": cs[0] if cs else ""})
    return recipes


def list_items(value: str) -> list[str]:
    value = plain(value)
    bits = [item.strip() for item in re.split(r"\s*•\s*", value) if item.strip()]
    return bits or [value]


def main() -> None:
    document = json.loads(MARKER.read_text(encoding="utf-8"))
    pages = {int(page["id"].split("/")[2]) + 1: page["children"] or [] for page in document["children"]}
    headers = []
    for pdf_page, blocks in pages.items():
        for index, block in enumerate(blocks):
            if block["block_type"] == "SectionHeader":
                headers.append((pdf_page, index, plain(block["html"]), block))

    all_recipes = [recipe for batch in PLAN.values() for recipe in parse_plan(batch)]
    starts: dict[int, tuple[int, int]] = {}
    for recipe in all_recipes:
        if recipe["source_order"] in TEXT_TITLE_STARTS:
            starts[recipe["source_order"]] = TEXT_TITLE_STARTS[recipe["source_order"]]
        else:
            wanted = normalized(recipe["en"])
            matches = [
                (page, index)
                for page, index, text, _ in headers
                if normalized(text).startswith(wanted)
            ]
            if not matches:
                matches = [(page, index) for page, index, text, _ in headers if wanted in normalized(text)]
            if not matches:
                raise SystemExit(f"No Marker title heading for {recipe['source_order']} {recipe['en']}")
            starts[recipe["source_order"]] = matches[0]

    spans = {}
    for recipe in all_recipes:
        start_page, start_index = starts[recipe["source_order"]]
        chosen = []
        for page in PAGES[recipe["source_order"]]:
            if page not in pages:
                continue
            blocks = pages[page]
            page_starts = sorted(
                (index, order)
                for order, (start, index) in starts.items()
                if start == page
            )
            lower_y = 0.0
            upper_y = float("inf")
            if page == start_page:
                lower_y = blocks[start_index]["bbox"][1]
                later = [index for index, _ in page_starts if index > start_index]
                if later:
                    upper_y = blocks[later[0]]["bbox"][1]
            else:
                later = [index for index, _ in page_starts]
                if later:
                    upper_y = blocks[later[0]]["bbox"][1]
            for index, block in enumerate(blocks):
                if block["block_type"] not in {"SectionHeader", "ListGroup", "Text"}:
                    continue
                if not plain(block.get("html", "")):
                    continue
                y = block["bbox"][1]
                if index == start_index and page == start_page:
                    chosen.append((page, block))
                elif lower_y <= y < upper_y:
                    chosen.append((page, block))
            chosen.sort(key=lambda item: (item[0], item[1]["bbox"][1], item[1]["bbox"][0]))
        for page, block_id in ADD_BLOCKS.get(recipe["source_order"], []):
            block = next(item for item in pages[page] if item["id"] == block_id)
            if not any(item[1]["id"] == block_id for item in chosen):
                chosen.append((page, block))
        chosen = [item for item in chosen if item[1]["id"] not in REMOVE_BLOCKS.get(recipe["source_order"], set())]
        chosen.sort(key=lambda item: (item[0], item[1]["bbox"][1], item[1]["bbox"][0]))
        spans[recipe["source_order"]] = chosen

    for batch, raw_plan in PLAN.items():
        recipes = []
        for descriptor in parse_plan(raw_plan):
            order = descriptor["source_order"]
            rid = f"vera-r{order:04d}"
            chosen = spans[order]
            source_regions, ingredient_sections, steps, notes, yields = [], [], [], [], []
            label = None
            for index, (page, block) in enumerate(chosen):
                block_id = block["id"]
                kind = block["block_type"]
                text = plain(block["html"])
                key = "title" if index == 0 else f"{kind.lower()}-{index}"
                role = "title" if index == 0 else "ingredient" if kind == "ListGroup" else "yield-time" if re.search(r"(Serves|Makes approx\.|Preparation time|For 1 cake|1 cake|1 loaf|2 breads|3 braids)", text) else "instruction" if kind == "Text" else "note"
                source_regions.append({"key": key, "role": role, "pdf_page": page, "block_ids": [block_id]})
                if index == 0:
                    continue
                if kind == "SectionHeader":
                    label = {"segment_id": f"label-{index}", "text": text, "region_key": key}
                elif kind == "ListGroup":
                    items = ITEM_OVERRIDES.get((order, block_id), list_items(block["html"]))
                    ingredient_sections.append({"section_id": f"ingredients-{len(ingredient_sections)+1}", **({"label": label} if label else {}), "items": [{"text": item, "region_keys": [key]} for item in items]})
                    label = None
                elif role == "yield-time":
                    yields.append({"text": text, "region_keys": [key]})
                elif kind == "Text":
                    steps.append({"text": text, "region_keys": [key]})
                else:
                    notes.append({"text": text, "region_keys": [key]})
            if not ingredient_sections and order == 86:
                ingredient_sections = []
            titles = [{"segment_id": "title-en", "text": descriptor["en"], "language": "en", "title_role": "primary"}]
            if descriptor["cs"]:
                titles.append({"segment_id": "title-cs", "text": descriptor["cs"], "language": "cs", "title_role": "parallel"})
            recipe = {
                "recipe_id": rid,
                "source_order": order,
                "slug": re.sub(r"[^a-z0-9]+", "-", normalized(descriptor["en"])).strip("-"),
                "pages": sorted({page for page, _ in chosen}),
                "printed_pages": [str(page - 1) for page in sorted({page for page, _ in chosen})],
                "display_title": descriptor["en"] + (" · " + descriptor["cs"] if descriptor["cs"] else ""),
                "titles": titles,
                "regions": source_regions,
                "ingredient_sections": ingredient_sections,
                "instruction_sections": [{"section_id": "instructions-main", "items": steps}],
                "yield_time_lines": yields,
                "notes": notes,
                "cross_references": [],
                "related_recipe_ids": RELATED.get(order, []),
                "status": "needs_attention" if order in NEEDS_ATTENTION else "source_checked",
                "open_issues": [],
            }
            if order in CONTINUATION_ORDERS:
                previous = next((region["key"] for region in source_regions if region["role"] == "instruction" and region["pdf_page"] == recipe["pages"][0]), None)
                following = next((region["key"] for region in source_regions if region["role"] == "instruction" and region["pdf_page"] == recipe["pages"][1]), None)
                if previous and following:
                    recipe["continuations"] = [{"from_region_key": previous, "to_region_key": following}]
            if order in CONTINUATION_KEYS:
                before, after = CONTINUATION_KEYS[order]
                recipe["continuations"] = [{"from_region_key": before, "to_region_key": after}]
            for key, page, bbox, items in MANUAL_INGREDIENTS.get(order, []):
                recipe["regions"].append({"key": key, "role": "ingredient", "pdf_page": page, "block_ids": [bbox]})
                recipe["ingredient_sections"].append({"section_id": f"ingredients-{len(recipe['ingredient_sections'])+1}", "items": [{"text": item, "region_keys": [key]} for item in items]})
            for key, role, page, bbox, text in MANUAL_REGIONS.get(order, []):
                recipe["regions"].append({"key": key, "role": role, "pdf_page": page, "block_ids": [bbox]})
                recipe["yield_time_lines"].append({"text": text, "region_keys": [key]})
            if order == 77:
                recipe["open_issues"] = [{"issue_id": "r0077-arrow-ornament", "target_ids": [rid], "description": "The note begins with an outlined arrow ornament whose exact Unicode encoding is not source-clear; it is not guessed as canonical text.", "severity": "textual"}]
            if order == 110:
                recipe["open_issues"] = [{"issue_id": "r0110-handwritten-flour", "target_ids": [rid], "description": "The printed 2 cups flour carries a handwritten 2 1/2 annotation and arrow; its authoritative transcription policy is unresolved.", "severity": "textual"}]
            recipes.append(recipe)
        batch_id = f"production-batch-{batch}"
        spec = {
            "batch_id": batch_id,
            "batch_title": f"Production batch {batch} source review",
            "batch_copy_title": f"Vera Cookbook production batch {batch} review status",
            "candidate_summary": f"Local Marker machine candidates for production batch {batch}; no trust promotion has been performed.",
            "audited_summary": f"Production batch {batch} after a separate direct local AI visual source audit. Source-clear records are source_checked; genuine ambiguity remains needs_attention. This is not human verification.",
            "recipe_schema_version": "1.3.0",
            "source_sha256": SOURCE_HASH,
            "pdf_page_count": 75,
            "marker_version": "2.0.0",
            "marker_generated_at": "2026-08-24T03:09:28Z",
            "marker_artifact": "pilot/acceleration-wave-005/marker-output/Culinary Adventures - Vera Gaeta/Culinary Adventures - Vera Gaeta.json",
            "created_at": "2026-08-24T03:12:00Z",
            "audited_at": "2026-08-24T03:28:00Z",
            "auditor_id": "openai-codex",
            "readback_record_ids": READBACKS.get(batch, []),
            "recipes": recipes,
        }
        target = ROOT / f"pilot/{batch_id}/spec.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
        print(target.relative_to(ROOT), len(recipes))


if __name__ == "__main__":
    main()
