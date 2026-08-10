#!/usr/bin/env python3
"""Access the preserved Pizza ontology through OAK.

This example deliberately reads the repository-owned ontology artifact rather
than copying Pizza knowledge into application code. It demonstrates lookup,
OWL-to-graph relationship projection, ancestry, and adapter capability
boundaries.
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
KNOWN_AMERICAN_HOT_RDFS_LABELS = {"AmericanHot", "AmericanaPicante"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def label_or_none(adapter, entity: str) -> str | None:
    return adapter.label(entity)


def label_language_capability(adapter) -> dict[str, object]:
    """Describe the language-selection boundary of the selected OAK adapter."""
    if type(adapter).__name__ == "FunOwlImplementation":
        return {
            "languageFilterSupportedByLabelMethod": False,
            "note": (
                "The current OAK FunOwlImplementation accepts the common label(..., lang=...) "
                "signature but does not apply the language argument when selecting among "
                "multiple rdfs:label values. The example therefore treats the returned "
                "multilingual label as backend-dependent instead of assuming English."
            ),
        }
    return {
        "languageFilterSupportedByLabelMethod": None,
        "note": "Language-selection behavior was not characterized for this adapter by this example.",
    }


def ontology_metadata_capability(adapter) -> dict[str, object]:
    """Report metadata support without assuming every OAK adapter implements it."""
    try:
        ontologies = list(adapter.ontologies())
        if not ontologies:
            return {
                "supported": True,
                "ontologyIds": [],
                "metadata": {},
                "note": "The adapter implements ontology enumeration but returned no ontology identifier.",
            }

        metadata = {
            str(ontology): {
                str(key): value
                for key, value in adapter.ontology_metadata_map(ontology).items()
            }
            for ontology in ontologies
        }
        return {
            "supported": True,
            "ontologyIds": [str(ontology) for ontology in ontologies],
            "metadata": metadata,
        }
    except NotImplementedError:
        return {
            "supported": False,
            "adapter": type(adapter).__name__,
            "note": (
                "This local Functional-Syntax adapter does not implement OAK ontology "
                "enumeration/metadata access. Use a metadata-capable backend for that operation."
            ),
        }


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

    # Pizza 2.0 contains both English and Portuguese rdfs:label values for
    # AmericanHot. The current local FunOwl adapter returns one of those values
    # without deterministic language filtering, so verify semantic label access
    # without making label ordering a false contract.
    label = label_or_none(adapter, AMERICAN_HOT)
    require(label is not None, "OAK could not resolve an AmericanHot rdfs:label")
    require(
        label in KNOWN_AMERICAN_HOT_RDFS_LABELS,
        f"unexpected AmericanHot rdfs:label: {label!r}",
    )

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

    result = {
        "ontology": str(ontology_path),
        "adapter": type(adapter).__name__,
        "entity": AMERICAN_HOT,
        "entityIri": adapter.curie_to_uri(AMERICAN_HOT),
        "label": label,
        "knownMultilingualRdfsLabels": sorted(KNOWN_AMERICAN_HOT_RDFS_LABELS),
        "labelLanguageCapability": label_language_capability(adapter),
        "relationships": [
            {
                "subject": str(subject),
                "predicate": str(predicate),
                "object": str(obj),
                "objectLabel": label_or_none(adapter, obj),
            }
            for subject, predicate, obj in relationships
        ],
        "isAAncestors": [
            {"id": str(ancestor), "label": label_or_none(adapter, ancestor)}
            for ancestor in ancestors
        ],
        "ontologyMetadataCapability": ontology_metadata_capability(adapter),
    }

    print(json.dumps(result, indent=2, default=str, sort_keys=True))
    print(
        "SUCCESS: OAK accessed Pizza labels, projected OWL relationships, ancestry, "
        "and reported the selected adapter's label/metadata capability boundaries."
    )


if __name__ == "__main__":
    main()
