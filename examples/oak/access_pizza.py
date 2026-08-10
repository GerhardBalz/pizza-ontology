#!/usr/bin/env python3
"""Access the preserved Pizza ontology through OAK.

This example deliberately reads the repository-owned ontology artifact rather
than copying Pizza knowledge into application code. It demonstrates lookup,
OWL-to-graph relationship projection, ancestry, and ontology metadata access.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from oaklib import get_adapter

PIZZA_NS = "http://www.co-ode.org/ontologies/pizza/pizza.owl#"
AMERICAN_HOT = "pizza:AmericanHot"
NAMED_PIZZA = "pizza:NamedPizza"
HAS_TOPPING = "pizza:hasTopping"
JALAPENO = "pizza:JalapenoPepperTopping"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: access_pizza.py PATH_TO_PIZZA_OFN")

    ontology_path = Path(sys.argv[1]).resolve()
    require(ontology_path.is_file(), f"ontology file not found: {ontology_path}")

    adapter = get_adapter(str(ontology_path))

    # Pizza uses a semantic URI namespace that is not part of OAK's default
    # OBO-oriented prefix map. Register it explicitly and use CURIEs through
    # the OAK interface while retaining the historical IRIs in the ontology.
    adapter.prefix_map()["pizza"] = PIZZA_NS

    label = adapter.label(AMERICAN_HOT)
    require(label is not None, "OAK could not resolve the AmericanHot label")
    require("American" in label and "Hot" in label, f"unexpected AmericanHot label: {label!r}")

    relationships = list(adapter.relationships([AMERICAN_HOT]))
    require(relationships, "OAK returned no relationships for AmericanHot")

    named_parent = any(
        predicate == "rdfs:subClassOf" and obj == NAMED_PIZZA
        for _, predicate, obj in relationships
    )
    require(named_parent, "AmericanHot must expose NamedPizza as an asserted superclass")

    jalapeno_topping = any(
        predicate == HAS_TOPPING and obj == JALAPENO
        for _, predicate, obj in relationships
    )
    require(
        jalapeno_topping,
        "AmericanHot must expose its hasTopping some JalapenoPepperTopping restriction as an OAK relationship",
    )

    ancestors = list(
        adapter.ancestors(
            AMERICAN_HOT,
            predicates=["rdfs:subClassOf"],
            reflexive=False,
        )
    )
    require(
        NAMED_PIZZA in ancestors,
        "NamedPizza must be reachable as an is-a ancestor of AmericanHot",
    )

    metadata = adapter.ontology_metadata_map()
    require(metadata is not None, "OAK ontology metadata access returned no result")

    result = {
        "ontology": str(ontology_path),
        "entity": AMERICAN_HOT,
        "entityIri": adapter.curie_to_uri(AMERICAN_HOT),
        "label": label,
        "relationships": [
            {
                "subject": str(subject),
                "predicate": str(predicate),
                "object": str(obj),
                "objectLabel": adapter.label(obj),
            }
            for subject, predicate, obj in relationships
        ],
        "isAAncestors": [
            {"id": str(ancestor), "label": adapter.label(ancestor)}
            for ancestor in ancestors
        ],
        "ontologyMetadata": {str(key): value for key, value in metadata.items()},
    }

    print(json.dumps(result, indent=2, default=str, sort_keys=True))
    print("SUCCESS: OAK accessed Pizza labels, projected OWL relationships, ancestry, and ontology metadata.")


if __name__ == "__main__":
    main()
