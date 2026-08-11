#!/usr/bin/env python3
"""Project selected Pizza OWL semantics into an OpenAPI 3.1 contract.

The historical Pizza ontology remains authoritative. This target deliberately
combines a source-verified semantic slice with API-specific contract concerns
without treating paths, HTTP behavior, or response envelopes as ontology facts.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

from openapi_spec_validator import validate_spec

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))

from common.pizza_source import extract_selected_concepts, load_json, require  # noqa: E402

CONFIG_PATH = HERE / "openapi-config.json"
GOLDEN_PATH = HERE / "pizza-concepts.openapi.json"


def canonical_json(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def ref(name: str) -> dict[str, str]:
    return {"$ref": f"#/components/schemas/{name}"}


def projection_policy() -> dict[str, list[str]]:
    return {
        "preserved": [
            "historical Pizza entity IRIs",
            "selected asserted named superclass relationships",
            "selected hasTopping existential relationship targets",
        ],
        "transformed": [
            "OWL class identifiers are exposed as CURIE plus full IRI",
            "selected OWL relationships are represented as OpenAPI response-schema fields and source-backed examples",
            "OWL hasTopping existential restrictions are flattened to requiredToppings references",
        ],
        "introduced": [
            "displayLabel is an application-facing choice from the shared projection selection config",
            "HTTP paths, GET operations, query parameters, status codes, response envelopes, and error schema are API-contract concerns",
            "OpenAPI and JSON Schema structures describe an implementation interface rather than ontology axioms",
        ],
        "omitted": [
            "universal topping closure restrictions",
            "country-of-origin restrictions",
            "inferred classifications",
            "disjointness axioms",
            "object-property characteristics and broader OWL axioms",
            "ontology annotations not required by this projection",
            "runtime deployment location and server bindings",
        ],
    }


def build_openapi() -> tuple[dict, dict]:
    api_config = load_json(CONFIG_PATH)
    source_config_path = (HERE / api_config["sourceSelectionConfig"]).resolve()
    source_config = load_json(source_config_path)
    source_slice = extract_selected_concepts(source_config)
    concepts = source_slice["concepts"]

    concept_ids = [concept["id"] for concept in concepts]
    topping_ids = sorted(
        {
            topping["id"]
            for concept in concepts
            for topping in concept["requiredToppings"]
        }
    )

    concept_examples = {
        concept["id"].split(":", 1)[-1]: {
            "summary": concept["displayLabel"],
            "value": concept,
        }
        for concept in concepts
    }

    document = {
        "openapi": "3.1.0",
        "jsonSchemaDialect": "https://json-schema.org/draft/2020-12/schema",
        "info": {
            "title": api_config["apiTitle"],
            "version": api_config["apiVersion"],
            "description": (
                "Application-facing OpenAPI projection of selected Pizza Ontology 2.0 semantics. "
                "The API contract is not the ontology and does not replace the preserved semantic source."
            ),
        },
        "tags": [
            {
                "name": "Pizza concepts",
                "description": "Read-only access to the selected source-verified Pizza concept projection.",
            }
        ],
        "x-pizza-projection": {
            "projection": {
                "id": api_config["projectionId"],
                "type": "OpenApiImplementationProjection",
                "version": api_config["projectionVersion"],
            },
            "sourceSemanticModel": source_slice["sourceSemanticModel"],
            "sourceSelectionConfig": api_config["sourceSelectionConfig"],
            "projectionPolicy": projection_policy(),
        },
        "paths": {
            api_config["collectionPath"]: {
                "get": {
                    "operationId": "listPizzaConcepts",
                    "summary": "List projected Pizza concepts",
                    "tags": ["Pizza concepts"],
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "required": False,
                            "description": "Application-level text filter over projected labels and identifiers.",
                            "schema": {"type": "string", "minLength": 1},
                        },
                        {
                            "name": "requiredTopping",
                            "in": "query",
                            "required": False,
                            "description": (
                                "Filter by a projected hasTopping some X existential requirement. "
                                "This does not mean the topping list is closed."
                            ),
                            "schema": ref("ToppingId"),
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Projected Pizza concepts matching the API-level filters.",
                            "content": {
                                "application/json": {
                                    "schema": ref("PizzaConceptCollection"),
                                    "examples": {
                                        "selectedProjection": {
                                            "summary": "Current selected source-backed projection",
                                            "value": {
                                                "count": len(concepts),
                                                "items": concepts,
                                            },
                                        }
                                    },
                                }
                            },
                        }
                    },
                }
            },
            api_config["itemPath"]: {
                "get": {
                    "operationId": "getPizzaConcept",
                    "summary": "Get one projected Pizza concept",
                    "tags": ["Pizza concepts"],
                    "parameters": [
                        {
                            "name": "conceptId",
                            "in": "path",
                            "required": True,
                            "description": "CURIE of a concept included in this selected projection.",
                            "schema": ref("PizzaConceptId"),
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "One source-backed projected Pizza concept.",
                            "content": {
                                "application/json": {
                                    "schema": ref("PizzaConcept"),
                                    "examples": concept_examples,
                                }
                            },
                        },
                        "404": {
                            "description": "The requested concept is not present in this selected API projection.",
                            "content": {
                                "application/json": {
                                    "schema": ref("Error"),
                                }
                            },
                        },
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "PizzaConceptId": {
                    "type": "string",
                    "description": "CURIE of a Pizza class selected for this implementation projection.",
                    "enum": concept_ids,
                },
                "ToppingId": {
                    "type": "string",
                    "description": "CURIE of a topping appearing in a projected existential requirement.",
                    "enum": topping_ids,
                },
                "SemanticReference": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "iri"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "pattern": "^pizza:",
                            "description": "Compact Pizza identifier used by the implementation contract.",
                        },
                        "iri": {
                            "type": "string",
                            "format": "uri",
                            "description": "Historical Pizza entity IRI; this remains the semantic identity.",
                        },
                    },
                },
                "Traceability": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "sourceEntityIri",
                        "superclassSemantics",
                        "toppingSemantics",
                    ],
                    "properties": {
                        "sourceEntityIri": {"type": "string", "format": "uri"},
                        "superclassSemantics": {"type": "string"},
                        "toppingSemantics": {"type": "string"},
                    },
                },
                "PizzaConcept": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "id",
                        "iri",
                        "displayLabel",
                        "displayLabelSource",
                        "directSuperClasses",
                        "requiredToppings",
                        "traceability",
                    ],
                    "properties": {
                        "id": ref("PizzaConceptId"),
                        "iri": {
                            "type": "string",
                            "format": "uri",
                            "description": "Historical Pizza entity IRI.",
                        },
                        "displayLabel": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Application-facing label chosen by projection configuration.",
                        },
                        "displayLabelSource": {
                            "type": "string",
                            "const": "projection-config",
                        },
                        "directSuperClasses": {
                            "type": "array",
                            "minItems": 1,
                            "items": ref("SemanticReference"),
                            "description": "Selected asserted named superclass relationships projected from OWL.",
                        },
                        "requiredToppings": {
                            "type": "array",
                            "minItems": 1,
                            "items": ref("SemanticReference"),
                            "description": (
                                "Targets of projected OWL hasTopping some X existential restrictions. "
                                "This is not a closed recipe or complete allowed-topping list."
                            ),
                        },
                        "traceability": ref("Traceability"),
                    },
                },
                "PizzaConceptCollection": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["count", "items"],
                    "properties": {
                        "count": {"type": "integer", "minimum": 0},
                        "items": {
                            "type": "array",
                            "items": ref("PizzaConcept"),
                        },
                    },
                },
                "Error": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["message"],
                    "properties": {
                        "message": {"type": "string"},
                    },
                },
            }
        },
    }

    return document, source_slice


def validate_projection(document: dict, source_slice: dict) -> None:
    validate_spec(document)

    require(document["openapi"] == "3.1.0", "OpenAPI projection must remain on OpenAPI 3.1.0")
    require("servers" not in document, "runtime deployment/server bindings do not belong in this projection")

    extension = document["x-pizza-projection"]
    require(
        extension["sourceSemanticModel"] == source_slice["sourceSemanticModel"],
        "OpenAPI projection source identity must match the shared OAK source slice",
    )

    schemas = document["components"]["schemas"]
    concept_ids = [concept["id"] for concept in source_slice["concepts"]]
    topping_ids = sorted(
        {
            topping["id"]
            for concept in source_slice["concepts"]
            for topping in concept["requiredToppings"]
        }
    )
    require(
        schemas["PizzaConceptId"]["enum"] == concept_ids,
        "OpenAPI concept-id enum must match the selected source concepts",
    )
    require(
        schemas["ToppingId"]["enum"] == topping_ids,
        "OpenAPI topping-id enum must match projected existential targets",
    )

    item_examples = document["paths"]["/concepts/{conceptId}"]["get"]["responses"]["200"]["content"]["application/json"]["examples"]
    example_ids = sorted(example["value"]["id"] for example in item_examples.values())
    require(example_ids == sorted(concept_ids), "OpenAPI item examples must cover every selected source concept")

    policy = extension["projectionPolicy"]
    require(
        "runtime deployment location and server bindings" in policy["omitted"],
        "projection policy must keep deployment out of the semantic/API projection",
    )
    require(
        "HTTP paths, GET operations, query parameters, status codes, response envelopes, and error schema are API-contract concerns"
        in policy["introduced"],
        "projection policy must make API-owned concerns explicit",
    )


def check_golden(document: dict) -> None:
    require(GOLDEN_PATH.is_file(), f"checked-in OpenAPI projection not found: {GOLDEN_PATH}")
    expected = load_json(GOLDEN_PATH)
    if expected != document:
        expected_text = canonical_json(expected).splitlines(keepends=True)
        actual_text = canonical_json(document).splitlines(keepends=True)
        diff = "".join(
            difflib.unified_diff(
                expected_text,
                actual_text,
                fromfile=str(GOLDEN_PATH),
                tofile="generated-openapi-from-Pizza-OWL",
            )
        )
        raise AssertionError(
            "checked-in OpenAPI projection no longer matches the current Pizza semantic source/API policy:\n"
            + diff
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate and compare with checked-in OpenAPI projection")
    mode.add_argument("--write", action="store_true", help="regenerate the checked-in OpenAPI projection")
    args = parser.parse_args()

    document, source_slice = build_openapi()
    validate_projection(document, source_slice)

    if args.write:
        GOLDEN_PATH.write_text(canonical_json(document), encoding="utf-8")
        print(f"Wrote {GOLDEN_PATH.relative_to(ROOT)}")
    elif args.check:
        check_golden(document)
        print(
            "SUCCESS: checked-in OpenAPI 3.1 projection is valid and matches selected Pizza OWL semantics "
            "through the shared OAK source boundary."
        )
    else:
        print(canonical_json(document), end="")


if __name__ == "__main__":
    main()
