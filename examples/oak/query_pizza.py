#!/usr/bin/env python3
"""Explore the preserved Pizza ontology through broader OAK access queries.

This specimen is intentionally an ontology-access example rather than an
application model. It asks bounded questions of the repository-owned Pizza
source through OAK and keeps graph traversal distinct from OWL reasoning.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from oaklib import get_adapter

PIZZA_NS = "http://www.co-ode.org/ontologies/pizza/pizza.owl#"
IS_A = "rdfs:subClassOf"
HAS_TOPPING = "pizza:hasTopping"

NAMED_PIZZA = "pizza:NamedPizza"
PIZZA_TOPPING = "pizza:PizzaTopping"
AMERICAN_HOT = "pizza:AmericanHot"
MARGHERITA = "pizza:Margherita"
JALAPENO = "pizza:JalapenoPepperTopping"

SELECTED_PIZZAS = [AMERICAN_HOT, MARGHERITA]
SELECTED_ENTITIES = [NAMED_PIZZA, PIZZA_TOPPING, HAS_TOPPING, *SELECTED_PIZZAS]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def entity_reference(adapter, curie: str) -> dict[str, object]:
    return {
        "id": curie,
        "iri": str(adapter.curie_to_uri(curie)),
        "label": adapter.label(curie),
    }


def direct_superclasses(adapter, entity: str) -> list[str]:
    return sorted(
        {
            str(obj)
            for subject, predicate, obj in adapter.relationships([entity])
            if str(subject) == entity and str(predicate) == IS_A
        }
    )


def projected_targets(adapter, entity: str, predicate: str) -> list[str]:
    return sorted(
        {
            str(obj)
            for subject, rel, obj in adapter.relationships([entity])
            if str(subject) == entity and str(rel) == predicate
        }
    )


def is_a_ancestors(adapter, entity: str) -> list[str]:
    return sorted(
        {
            str(ancestor)
            for ancestor in adapter.ancestors(
                entity,
                predicates=[IS_A],
                reflexive=False,
            )
        }
    )


def is_a_descendants(adapter, entity: str) -> list[str]:
    return sorted(
        {
            str(descendant)
            for descendant in adapter.descendants(
                entity,
                predicates=[IS_A],
                reflexive=False,
            )
        }
    )


def direct_children_from_descendants(adapter, parent: str, descendants: list[str]) -> list[str]:
    """Identify asserted direct children from a bounded descendant closure."""
    direct_children = []
    for descendant in descendants:
        if parent in direct_superclasses(adapter, descendant):
            direct_children.append(descendant)
    return sorted(direct_children)


def bounded_references(adapter, entities: list[str], limit: int = 12) -> list[dict[str, object]]:
    return [entity_reference(adapter, entity) for entity in entities[:limit]]


def search_capability(adapter, query: str) -> dict[str, object]:
    """Exercise SearchInterface only when implemented by the selected adapter."""
    method = getattr(adapter, "basic_search", None)
    if method is None:
        return {
            "supported": False,
            "query": query,
            "results": [],
            "note": "The selected adapter does not expose OAK basic_search().",
        }

    try:
        results = sorted({str(result) for result in method(query)})
    except NotImplementedError:
        return {
            "supported": False,
            "query": query,
            "results": [],
            "note": (
                "OAK defines basic_search through its Search Interface, but the selected "
                "local Functional-Syntax adapter does not implement it."
            ),
        }

    return {
        "supported": True,
        "query": query,
        "resultCount": len(results),
        "results": bounded_references(adapter, results, limit=10),
        "note": (
            "Search ranking/matching is adapter-specific; this example reports the selected "
            "backend's results without making them a Pizza semantic contract."
        ),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: query_pizza.py PATH_TO_PIZZA_OFN")

    ontology_path = Path(sys.argv[1]).resolve()
    require(ontology_path.is_file(), f"ontology file not found: {ontology_path}")

    adapter = get_adapter(str(ontology_path))
    adapter.prefix_map()["pizza"] = PIZZA_NS

    # 1. Entity identity / labels. Labels are display metadata; CURIE/IRI remains
    # the deterministic identity used by the access contract.
    entity_lookup = [entity_reference(adapter, entity) for entity in SELECTED_ENTITIES]
    for entity in entity_lookup:
        require(entity["iri"].startswith(PIZZA_NS), f"unexpected Pizza entity IRI: {entity}")

    # 2. Compare asserted direct parents with transitive is-a graph traversal.
    hierarchy = {}
    for pizza in SELECTED_PIZZAS:
        direct = direct_superclasses(adapter, pizza)
        ancestors = is_a_ancestors(adapter, pizza)
        require(direct, f"expected at least one asserted named superclass for {pizza}")
        require(
            set(direct).issubset(set(ancestors)),
            f"direct superclasses must be contained in the is-a ancestor closure for {pizza}",
        )
        hierarchy[pizza] = {
            "directSuperClasses": bounded_references(adapter, direct),
            "isAAncestorCount": len(ancestors),
            "isAAncestors": bounded_references(adapter, ancestors),
        }

    # 3. Inspect the graph projection of selected OWL existential restrictions.
    topping_targets = {
        pizza: projected_targets(adapter, pizza, HAS_TOPPING)
        for pizza in SELECTED_PIZZAS
    }
    require(
        JALAPENO in topping_targets[AMERICAN_HOT],
        "AmericanHot must expose hasTopping some JalapenoPepperTopping through OAK",
    )
    require(
        all(topping_targets[pizza] for pizza in SELECTED_PIZZAS),
        "selected Pizza examples must expose at least one projected hasTopping target",
    )

    # 4. Traverse downward as a distinct access question. Descendants are graph
    # closure over asserted/projected relationships here, not a classification run.
    named_pizza_descendants = is_a_descendants(adapter, NAMED_PIZZA)
    pizza_topping_descendants = is_a_descendants(adapter, PIZZA_TOPPING)

    require(AMERICAN_HOT in named_pizza_descendants, "AmericanHot must descend from NamedPizza")
    require(MARGHERITA in named_pizza_descendants, "Margherita must descend from NamedPizza")
    require(JALAPENO in pizza_topping_descendants, "JalapenoPepperTopping must descend from PizzaTopping")

    named_pizza_direct_children = direct_children_from_descendants(
        adapter,
        NAMED_PIZZA,
        named_pizza_descendants,
    )
    require(
        AMERICAN_HOT in named_pizza_direct_children,
        "AmericanHot must be an asserted direct child of NamedPizza",
    )
    require(
        MARGHERITA in named_pizza_direct_children,
        "Margherita must be an asserted direct child of NamedPizza",
    )

    # 5. Search is an optional interface capability. The local adapter is allowed
    # to report that it does not support lexical search; that is an adapter
    # boundary, not a failure of the Pizza semantic source.
    lexical_search = search_capability(adapter, "Margherita")

    result = {
        "ontology": str(ontology_path),
        "adapter": type(adapter).__name__,
        "questions": {
            "entityLookup": entity_lookup,
            "hierarchy": hierarchy,
            "projectedHasToppingTargets": {
                pizza: bounded_references(adapter, targets)
                for pizza, targets in topping_targets.items()
            },
            "descendantTraversal": {
                "namedPizza": {
                    "descendantCount": len(named_pizza_descendants),
                    "descendants": bounded_references(adapter, named_pizza_descendants),
                    "assertedDirectChildCount": len(named_pizza_direct_children),
                    "assertedDirectChildren": bounded_references(adapter, named_pizza_direct_children),
                },
                "pizzaTopping": {
                    "descendantCount": len(pizza_topping_descendants),
                    "descendants": bounded_references(adapter, pizza_topping_descendants),
                },
            },
            "lexicalSearchCapability": lexical_search,
        },
        "boundaries": {
            "accessNotReasoning": (
                "ancestors/descendants are OAK graph traversal over the selected adapter; "
                "OWL classification remains a separate reasoning concern"
            ),
            "searchIsBackendDependent": True,
            "resultsRemainNonAuthoritative": (
                "OAK query results are views over the preserved semantic source, not a new semantic model"
            ),
        },
    }

    print(json.dumps(result, indent=2, default=str, sort_keys=True))
    print(
        "SUCCESS: broader OAK exploration verified entity lookup, direct/transitive hierarchy, "
        "projected topping relationships, descendant traversal, and search capability boundaries."
    )


if __name__ == "__main__":
    main()
