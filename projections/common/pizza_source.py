#!/usr/bin/env python3
"""Shared OAK-backed extraction for selected Pizza implementation projections.

This module owns only the source-access boundary. Target-specific projection
logic remains in each projection directory so JSON, OpenAPI, and future targets
can evolve independently without copying OWL interpretation code.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from oaklib import get_adapter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "src" / "ontology" / "pizza-edit.owl"

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


def extract_selected_concepts(config: dict) -> dict:
    """Extract the selected graph-shaped source semantics from Pizza OWL.

    The configuration supplies source identity, the historical entity namespace,
    and selected concept/display-label choices. The returned structure is neutral
    with respect to the eventual target representation.
    """

    require(SOURCE.is_file(), f"Pizza source ontology not found: {SOURCE}")
    namespace = config["sourceEntityNamespace"]

    # The ODK editor ontology is Functional Syntax with a historical .owl file
    # name. Give the local OAK adapter an explicit .ofn syntax hint using a
    # byte-identical temporary copy, matching the established OAK access slice.
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
        "sourceSemanticModel": {
            "ontologyIri": config["sourceOntologyIri"],
            "versionIri": config["sourceVersionIri"],
            "entityNamespace": namespace,
            "repositoryPath": "src/ontology/pizza-edit.owl",
            "accessLayer": "OAK graph projection",
        },
        "concepts": concepts,
    }
