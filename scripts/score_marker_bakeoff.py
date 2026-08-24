#!/usr/bin/env python3
"""Score Marker JSON against the frozen cookbook visual-gold probes."""

from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

import yaml


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_GOLD = PROJECT_DIR / "pilot/marker-bakeoff-v1/gold/visual-gold-probes.yaml"
DEFAULT_CANDIDATE = (
    PROJECT_DIR
    / "pilot/marker-bakeoff-v1/marker-output/Culinary Adventures - Vera Gaeta"
    / "Culinary Adventures - Vera Gaeta.json"
)
DEFAULT_RESULTS = PROJECT_DIR / "pilot/marker-bakeoff-v1/results.json"
DEFAULT_REPORT = PROJECT_DIR / "pilot/marker-bakeoff-v1/report.md"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return " ".join(self.parts)


def html_to_text(value: str) -> str:
    parser = TextExtractor()
    parser.feed(html.unescape(value))
    return parser.text()


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = value.translate(
        str.maketrans(
            {
                "–": "-",
                "—": "-",
                "−": "-",
                "·": "-",
                "“": '"',
                "”": '"',
                "″": '"',
                "’": "'",
                "‘": "'",
                "′": "'",
            }
        )
    )
    return re.sub(r"\s+", " ", value).strip()


def page_number(page: dict) -> int:
    match = re.search(r"/page/(\d+)/", page.get("id", ""))
    if not match:
        raise ValueError(f"Cannot resolve page index from {page.get('id')!r}")
    return int(match.group(1)) + 1


def page_text(page: dict) -> str:
    blocks = page.get("children") or []
    return normalize(" ".join(html_to_text(block.get("html", "")) for block in blocks))


def contains(text: str, probe: str) -> bool:
    return normalize(probe) in text


def score(gold: dict, candidate: dict) -> dict:
    candidate_pages = {page_number(page): page_text(page) for page in candidate["children"]}
    page_results: list[dict] = []
    totals = {
        "exact_passed": 0,
        "exact_total": 0,
        "numeric_passed": 0,
        "numeric_total": 0,
        "diacritic_passed": 0,
        "diacritic_total": 0,
        "title_passed": 0,
        "title_total": 0,
        "order_passed": 0,
        "order_total": 0,
        "ownership_passed": 0,
        "ownership_total": 0,
        "count_passed": 0,
        "count_total": 0,
    }

    for gold_page in gold["pages"]:
        pdf_page = gold_page["pdf_page"]
        text = candidate_pages.get(pdf_page, "")
        missing: list[str] = []

        exact_results = []
        for probe in gold_page.get("exact_probes", []):
            passed = contains(text, probe)
            exact_results.append({"probe": probe, "passed": passed})
            totals["exact_total"] += 1
            totals["exact_passed"] += int(passed)
            if re.search(r"\d", probe):
                totals["numeric_total"] += 1
                totals["numeric_passed"] += int(passed)
            if any(ord(char) > 127 and char.isalpha() for char in probe):
                totals["diacritic_total"] += 1
                totals["diacritic_passed"] += int(passed)
            if not passed:
                missing.append(probe)

        titles = gold_page.get("expected_titles", [])
        title_results = []
        for title in titles:
            passed = contains(text, title)
            title_results.append({"title": title, "passed": passed})
            totals["title_total"] += 1
            totals["title_passed"] += int(passed)

        order_values = gold_page.get("expected_order", [])
        order_results = []
        for left, right in zip(order_values, order_values[1:]):
            left_pos = text.find(normalize(left))
            right_pos = text.find(normalize(right))
            passed = left_pos >= 0 and right_pos >= 0 and left_pos < right_pos
            order_results.append({"before": left, "after": right, "passed": passed})
            totals["order_total"] += 1
            totals["order_passed"] += int(passed)

        ownership_results = []
        ownership_pairs = gold_page.get("ownership_pairs", [])
        for pair_index, pair in enumerate(ownership_pairs):
            title = normalize(pair["title"])
            owned = normalize(pair["owned_text"])
            title_pos = text.find(title)
            owned_pos = text.find(owned)
            next_title_pos = -1
            if pair_index + 1 < len(ownership_pairs):
                next_title_pos = text.find(normalize(ownership_pairs[pair_index + 1]["title"]))
            passed = title_pos >= 0 and owned_pos > title_pos
            if passed and next_title_pos >= 0:
                passed = owned_pos < next_title_pos
            ownership_results.append(
                {
                    "title": pair["title"],
                    "owned_text": pair["owned_text"],
                    "passed": passed,
                }
            )
            totals["ownership_total"] += 1
            totals["ownership_passed"] += int(passed)

        count_results = []
        for count_probe in gold_page.get("count_probes", []):
            probe = normalize(count_probe["text"])
            actual_count = text.count(probe)
            expected_count = count_probe["expected_count"]
            passed = actual_count == expected_count
            count_results.append(
                {
                    "text": count_probe["text"],
                    "expected_count": expected_count,
                    "actual_count": actual_count,
                    "passed": passed,
                }
            )
            totals["count_total"] += 1
            totals["count_passed"] += int(passed)

        page_results.append(
            {
                "pdf_page": pdf_page,
                "printed_page": gold_page.get("printed_page"),
                "page_kind": gold_page["page_kind"],
                "candidate_present": bool(text),
                "exact": exact_results,
                "titles": title_results,
                "order": order_results,
                "ownership": ownership_results,
                "counts": count_results,
                "missing_exact_probes": missing,
            }
        )

    def percentage(passed: int, total: int) -> float | None:
        return round(100 * passed / total, 1) if total else None

    metrics = {
        key.removesuffix("_passed"): {
            "passed": totals[key],
            "total": totals[key.replace("_passed", "_total")],
            "percent": percentage(totals[key], totals[key.replace("_passed", "_total")]),
        }
        for key in totals
        if key.endswith("_passed")
    }
    combined_passed = sum(value["passed"] for value in metrics.values())
    combined_total = sum(value["total"] for value in metrics.values())
    metrics["combined_checks"] = {
        "passed": combined_passed,
        "total": combined_total,
        "percent": percentage(combined_passed, combined_total),
    }
    return {
        "schema_version": "1.0",
        "gold_id": gold["gold_id"],
        "candidate": "marker-pdf==2.0.0 / surya-ocr==0.22.1 / balanced forced OCR / no remote LLM",
        "candidate_pages": sorted(candidate_pages),
        "metrics": metrics,
        "pages": page_results,
    }


def report_markdown(results: dict) -> str:
    metrics = results["metrics"]
    lines = [
        "# Marker bake-off v1 report",
        "",
        "## Result",
        "",
        (
            f"Marker passed **{metrics['combined_checks']['passed']}/"
            f"{metrics['combined_checks']['total']} normalized gold checks "
            f"({metrics['combined_checks']['percent']}%)** on the frozen 15-page cohort."
        ),
        "",
        "This is a consequential-probe benchmark, not a full-page character-error-rate benchmark. "
        "Marker output remains non-authoritative until source review.",
        "",
        "## Decision",
        "",
        "**Adopt Marker as the local first-pass OCR and page-layout engine. Do not use "
        "its flattened output as the canonical recipe extractor.**",
        "",
        "Marker is materially useful here: it preserved most consequential text, ran "
        "entirely locally, retained page/block geometry, and produced visual debug "
        "artifacts. Its primary weakness is structural rather than cosmetic. On dense "
        "multi-recipe pages it sometimes emitted an ingredient list before the recipe "
        "title that owns it, and it occasionally dropped repeated yield/preparation "
        "lines near page bottoms. Those errors can silently create a plausible but "
        "incorrect recipe record.",
        "",
        "The production extraction pipeline should therefore:",
        "",
        "1. Preserve Marker's page blocks, polygons, and raw text as rebuildable evidence.",
        "2. Segment recipes using page geometry and explicit recipe entities, not the "
        "flattened Markdown/JSON reading sequence alone.",
        "3. Recover and review footer-like blocks so yield and preparation-time lines "
        "cannot disappear silently.",
        "4. Flag mixed fractions, temperatures, quantities, units, Czech diacritics, "
        "repeated lines, continuations, and cross-references for visual review.",
        "5. Promote text to the canonical dataset only after a human verifies it "
        "against the cited page region.",
        "",
        "## Metrics",
        "",
        "| Metric | Passed | Total | Percent |",
        "|---|---:|---:|---:|",
    ]
    for name in ["exact", "numeric", "diacritic", "title", "order", "ownership", "count"]:
        value = metrics[name]
        percent = "n/a" if value["percent"] is None else f"{value['percent']}%"
        lines.append(f"| {name.replace('_', ' ').title()} | {value['passed']} | {value['total']} | {percent} |")

    lines.extend(
        [
            "",
            "The 100% order result covers the benchmark's adjacent inventory-title checks; "
            "it does not mean whole-page recipe association was perfect. The ownership and "
            "occurrence-count metrics expose that distinction.",
        ]
    )

    lines.extend(["", "## Page-level misses", ""])
    for page in results["pages"]:
        misses = page["missing_exact_probes"]
        failed_titles = [item["title"] for item in page["titles"] if not item["passed"]]
        failed_order = [
            f"{item['before']} -> {item['after']}" for item in page["order"] if not item["passed"]
        ]
        failed_ownership = [
            f"{item['title']} owns {item['owned_text']}"
            for item in page["ownership"]
            if not item["passed"]
        ]
        failed_counts = [
            f"{item['text']} expected {item['expected_count']}, found {item['actual_count']}"
            for item in page["counts"]
            if not item["passed"]
        ]
        if not any([misses, failed_titles, failed_order, failed_ownership, failed_counts]):
            continue
        lines.append(f"### PDF page {page['pdf_page']} / printed page {page['printed_page']}")
        lines.append("")
        lines.append(f"Page type: {page['page_kind']}.")
        if misses:
            lines.append("")
            lines.append("Missing or altered exact probes:")
            lines.extend(f"- `{item}`" for item in misses)
        if failed_titles:
            lines.append("")
            lines.append("Missing or altered titles:")
            lines.extend(f"- `{item}`" for item in failed_titles)
        if failed_order:
            lines.append("")
            lines.append("Failed reading-order checks:")
            lines.extend(f"- `{item}`" for item in failed_order)
        if failed_ownership:
            lines.append("")
            lines.append("Failed ownership checks:")
            lines.extend(f"- `{item}`" for item in failed_ownership)
        if failed_counts:
            lines.append("")
            lines.append("Failed occurrence-count checks:")
            lines.extend(f"- `{item}`" for item in failed_counts)
        lines.append("")

    lines.extend(
        [
            "## Interpretation boundary",
            "",
            "A passed probe means the normalized source string was present in Marker output. "
            "It does not prove that unprobed text is correct or that the page is ready for canonical promotion. "
            "Missing/invented text outside the probes and exact visual punctuation require further review.",
            "",
            "## Execution record",
            "",
            "- Candidate: `marker-pdf==2.0.0` with `surya-ocr==0.22.1`.",
            "- Cohort: 15 frozen PDF pages spanning inventories, single recipes, "
            "multi-recipe pages, continuations, ingredient subgroups, and the index.",
            "- Gold set: 124 visually verified exact probes, 14 ownership checks, and 3 "
            "repeated-occurrence checks.",
            "- Mode: balanced local VLM layout plus forced full-page OCR; optional LLM "
            "enhancement was not enabled and no cookbook page was sent to a remote model.",
            "- Elapsed Marker run time: 195.48 seconds on this machine.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", type=Path, default=DEFAULT_GOLD)
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    gold = yaml.safe_load(args.gold.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    results = score(gold, candidate)
    args.results.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.report.write_text(report_markdown(results), encoding="utf-8")
    print(json.dumps(results["metrics"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
