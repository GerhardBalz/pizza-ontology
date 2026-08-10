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
PREFERRED_LANGUAGE = "en"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def english_label(adapter, entity: str) -> str | None:
    return adapter.label(entity, lang=PREFERRED_LANGUAGE)


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

    # Pizza 2.0 contains multilingual rdfs:label values. Ask OAK explicitly
    # for English instead of relying on whichever label occurs first.
    label = english_label(adapter, AMERICAN_HOT)
    require(label is not None, "OAK could not resolve the English AmericanHot label")
    require("American" in label and "Hot" in label, f"unexpected English AmericanHot label: {label!r}")

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

    ontologies = list(adapter.ontologies())
    require(ontologies, "OAK did not expose an ontology identifier for the Pizza source")
    require(len(ontologies) == 1, f"expected one Pizza ontology, got {ontologies!r}")
    ontology_id = ontologies[0]
    metadata = adapter.ontology_metadata_map(ontology_id)
    require(metadata is not None, "OAK ontology metadata access returned no result")

    result = {
        "ontology": str(ontology_path),
        "ontologyId": str(ontology_id),
        "entity": AMERICAN_HOT,
        "entityIri": adapter.curie_to_uri(AMERICAN_HOT),
        "preferredLanguage": PREFERRED_LANGUAGE,
        "label": label,
        "relationships": [
            {
                "subject": str(subject),
                "predicate": str(predicate),
                "object": str(obj),
                "objectLabel": english_label(adapter, obj),
            }
            for subject, predicate, obj in relationships
        ],
        "isAAncestors": [
            {"id": str(ancestor), "label": english_label(adapter, ancestor)}
            for ancestor in ancestors
        ],
        "ontologyMetadata": {str(key): value for key, value in metadata.items()},
    }

    print(json.dumps(result, indent=2, default=str, sort_keys=True))
    print("SUCCESS: OAK accessed Pizza labels, projected OWL relationships, ancestry, and ontology metadata.")


if __name__ == "__main__":
    main()
