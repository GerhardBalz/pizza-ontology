#!/usr/bin/env python3
"""Project selected Pizza OWL semantics into a small application-facing JSON model.

The source ontology remains authoritative. This script deliberately projects only
selected graph-shaped semantics and verifies the checked-in JSON representation
against the current repository-owned Pizza source through the shared OAK boundary.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))

from common.pizza_source import extract_selected_concepts, load_json, require  # noqa: E402

CONFIG_PATH = HERE / "projection-config.json"
SCHEMA_PATH = HERE / "projection.schema.json"
GOLDEN_PATH = HERE / "pizza-concepts.json"


def build_projection() -> dict:
    config = load_json(CONFIG_PATH)
    source_slice = extract_selected_concepts(config)

    return {
        "$schema": "./projection.schema.json",
        "projection": {
            "id": config["projectionId"],
            "type": "PizzaConceptCatalog",
            "version": config["projectionVersion"],
        },
        "sourceSemanticModel": source_slice["sourceSemanticModel"],
        "projectionPolicy": {
            "preserved": [
                "historical Pizza entity IRIs",
                "selected asserted named superclass relationships",
                "selected hasTopping existential relationship targets",
            ],
            "transformed": [
                "OWL class identifiers are exposed as CURIE plus full IRI",
                "OWL hasTopping existential restrictions are flattened to requiredToppings references",
            ],
            "introduced": [
                "displayLabel is an application-facing projection choice from projection-config.json",
                "JSON object and array structure is an implementation representation",
            ],
            "omitted": [
                "universal topping closure restrictions",
                "country-of-origin restrictions",
                "inferred classifications",
                "disjointness axioms",
                "object-property characteristics and broader OWL axioms",
                "ontology annotations not required by this projection",
            ],
        },
        "concepts": source_slice["concepts"],
    }


def validate_projection(projection: dict) -> None:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(projection), key=lambda error: list(error.path))
    if errors:
        details = "\n".join(f"- {list(error.path)}: {error.message}" for error in errors)
        raise AssertionError(f"projection JSON Schema validation failed:\n{details}")


def canonical_json(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def check_golden(projection: dict) -> None:
    require(GOLDEN_PATH.is_file(), f"checked-in projection not found: {GOLDEN_PATH}")
    expected = load_json(GOLDEN_PATH)
    if expected != projection:
        expected_text = canonical_json(expected).splitlines(keepends=True)
        actual_text = canonical_json(projection).splitlines(keepends=True)
        diff = "".join(
            difflib.unified_diff(
                expected_text,
                actual_text,
                fromfile=str(GOLDEN_PATH),
                tofile="generated-from-Pizza-OWL",
            )
        )
        raise AssertionError(
            "checked-in projection no longer matches the current Pizza semantic source:\n" + diff
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate and compare with checked-in projection")
    mode.add_argument("--write", action="store_true", help="regenerate the checked-in projection")
    args = parser.parse_args()

    projection = build_projection()
    validate_projection(projection)

    if args.write:
        GOLDEN_PATH.write_text(canonical_json(projection), encoding="utf-8")
        print(f"Wrote {GOLDEN_PATH.relative_to(ROOT)}")
    elif args.check:
        check_golden(projection)
        print(
            "SUCCESS: checked-in JSON projection matches selected Pizza OWL semantics "
            "through the shared OAK source boundary."
        )
    else:
        print(canonical_json(projection), end="")


if __name__ == "__main__":
    main()
