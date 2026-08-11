#!/usr/bin/env python3
"""Project selected Pizza OWL semantics into a small application-facing JSON model.

The source ontology remains authoritative. This script deliberately projects only
selected graph-shaped semantics and verifies the checked-in JSON representation
against the current repository-owned Pizza source through OAK.
"""

from __future__ import annotations

import argparse
import difflib
import json
import shutil
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from oaklib import get_adapter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "src" / "ontology" / "pizza-edit.owl"
CONFIG_PATH = HERE / "projection-config.json"
SCHEMA_PATH = HERE / "projection.schema.json"
GOLDEN_PATH = HERE / "pizza-concepts.json"

RDFS_SUBCLASS = "rdfs:subClassOf"
HAS_TOPPING = "pizza:hasTopping"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def entity_reference(adapter, curie: str) -> dict[str, str]:
    iri = adapter.curie_to_uri(curie)
    require(iri is not None, f"OAK could not expand CURIE: {curie}")
    return {"id": curie, "iri": str(iri)}


def build_projection() -> dict:
    config = load_json(CONFIG_PATH)
    require(SOURCE.is_file(), f"Pizza source ontology not found: {SOURCE}")

    namespace = config["sourceEntityNamespace"]

    # The ODK editor ontology is Functional Syntax with a historical .owl file
    # name. Give the local OAK adapter an explicit .ofn syntax hint using a
    # byte-identical temporary copy, just as the established OAK access slice does.
    with tempfile.TemporaryDirectory(prefix="pizza-projection-") as temp_dir:
        oak_input = Path(temp_dir) / "pizza-edit.ofn"
        shutil.copyfile(SOURCE, oak_input)
        require(
            SOURCE.read_bytes() == oak_input.read_bytes(),
            "temporary OAK input must be byte-identical to the repository source",
        )

        adapter = get_adapter(str(oak_input))
        adapter.prefix_map()["pizza"] = namespace

        concepts: list[dict] = []
        for requested in config["concepts"]:
            entity = requested["id"]
            entity_ref = entity_reference(adapter, entity)
            require(
                entity_ref["iri"].startswith(namespace),
                f"projected entity is outside the historical Pizza namespace: {entity_ref['iri']}",
            )

            relationships = list(adapter.relationships([entity]))
            require(relationships, f"OAK returned no relationships for {entity}")

            direct_superclasses = sorted(
                {
                    str(obj)
                    for subject, predicate, obj in relationships
                    if str(subject) == entity and str(predicate) == RDFS_SUBCLASS
                }
            )
            required_toppings = sorted(
                {
                    str(obj)
                    for subject, predicate, obj in relationships
                    if str(subject) == entity and str(predicate) == HAS_TOPPING
                }
            )

            require(
                direct_superclasses,
                f"projection expects at least one asserted named superclass for {entity}",
            )
            require(
                required_toppings,
                f"projection expects at least one hasTopping existential relationship for {entity}",
            )

            concepts.append(
                {
                    "id": entity,
                    "iri": entity_ref["iri"],
                    "displayLabel": requested["displayLabel"],
                    "displayLabelSource": "projection-config",
                    "directSuperClasses": [
                        entity_reference(adapter, curie) for curie in direct_superclasses
                    ],
                    "requiredToppings": [
                        entity_reference(adapter, curie) for curie in required_toppings
                    ],
                    "traceability": {
                        "sourceEntityIri": entity_ref["iri"],
                        "superclassSemantics": "asserted named rdfs:subClassOf projected by OAK",
                        "toppingSemantics": "OWL hasTopping existential restrictions flattened by OAK graph projection",
                    },
                }
            )

    return {
        "$schema": "./projection.schema.json",
        "projection": {
            "id": config["projectionId"],
            "type": "PizzaConceptCatalog",
            "version": config["projectionVersion"],
        },
        "sourceSemanticModel": {
            "ontologyIri": config["sourceOntologyIri"],
            "versionIri": config["sourceVersionIri"],
            "entityNamespace": namespace,
            "repositoryPath": "src/ontology/pizza-edit.owl",
            "accessLayer": "OAK graph projection",
        },
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
        "concepts": concepts,
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
            "through the OAK graph-projection boundary."
        )
    else:
        print(canonical_json(projection), end="")


if __name__ == "__main__":
    main()
